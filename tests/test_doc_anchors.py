"""Anchored-citation checker (G13 mitigation).

Verifies every anchored citation in docs/**/*.md against its target file, so a
stale anchor fails loud instead of reading as verified. Two conventions are
checked, matching the two formats actually used in the repo:

  A. path:line (`literal`)          — VERIFIED-FACTS.md style. The literal must
                                      appear verbatim in the target file. The
                                      line number is treated as a hint (G13:
                                      line numbers decay), not asserted.
  B. `path.md`, under the heading "..." [... containing "..."]
                                    — findings-doc prose style. Each quoted
                                      string must appear verbatim in the target.

Matching is against RAW target lines with no whitespace normalization: both
first-attempt anchor failures in this repo came from markdown line wraps, and a
normalizing matcher would have passed both. The CITING doc is paragraph-unwrapped
before extraction (citations legitimately wrap there); the TARGET is not.

Bare line ranges without a backticked literal are not anchored citations and are
out of scope here.
"""

from __future__ import annotations

import re
import subprocess
from functools import lru_cache
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
DOCS = sorted((REPO / "docs").rglob("*.md"))


@lru_cache(maxsize=1)
def _tracked_files() -> tuple[Path, ...]:
    out = subprocess.run(
        ["git", "ls-files"], cwd=REPO, capture_output=True, text=True, check=True
    ).stdout
    return tuple(REPO / line for line in out.splitlines())


def _candidates(rel: str) -> list[Path]:
    """Resolve a cited path to candidate target files. Full repo-relative paths
    resolve directly; bare filenames (VERIFIED-FACTS.md shorthand, where the
    directory was established earlier in the section) resolve to every tracked
    file with that name — the anchor literal disambiguates."""
    p = REPO / rel
    if p.exists():
        return [p]
    if "/" not in rel and "\\" not in rel:
        return [f for f in _tracked_files() if f.name == rel]
    return []

# A: path:line or path:line-line, immediately followed by (`literal`).
CITE_A = re.compile(
    r"((?:[A-Za-z0-9_.-]+/)*(?:[A-Za-z0-9_.-]+\.[A-Za-z0-9]+|\.gitignore))"
    r":(\d+)(?:-\d+)?\s*\(`([^`]+)`\)"
)

# B: `path.md`, under the heading "..." optionally followed (same paragraph)
# by containing "...".
CITE_B = re.compile(
    r"`([^`]+\.md)`, under the heading\s+\"([^\"]+)\""
    r"(?:[^\"]*?\bcontaining\s+\"([^\"]+)\")?"
)


def _unwrap(text: str) -> str:
    """Join wrapped lines within paragraphs (single newlines -> space) so
    citations that wrap in the citing doc are extractable. Paragraph breaks
    (blank lines) are preserved."""
    paragraphs = re.split(r"\n\s*\n", text)
    return "\n\n".join(re.sub(r"\s*\n\s*", " ", p) for p in paragraphs)


def _extract(doc: Path) -> list[tuple[str, str, str]]:
    """Return (target_path, anchor_literal, citation_repr) triples."""
    text = _unwrap(doc.read_text(encoding="utf-8"))
    out: list[tuple[str, str, str]] = []
    for m in CITE_A.finditer(text):
        path, line, literal = m.group(1), m.group(2), m.group(3)
        out.append((path, literal, f"{path}:{line} (`{literal}`)"))
    for m in CITE_B.finditer(text):
        path, heading, phrase = m.group(1), m.group(2), m.group(3)
        out.append((path, heading, f'`{path}` heading "{heading}"'))
        if phrase:
            out.append((path, phrase, f'`{path}` containing "{phrase}"'))
    return out


_CASES = [(doc, t) for doc in DOCS for t in _extract(doc)]


@pytest.mark.parametrize(
    "doc, cite",
    _CASES,
    ids=[f"{d.relative_to(REPO)}::{c[2][:60]}" for d, c in _CASES],
)
def test_anchor_resolves(doc: Path, cite: tuple[str, str, str]) -> None:
    target_rel, literal, repr_ = cite
    targets = _candidates(target_rel)
    assert targets, (
        f"{doc.relative_to(REPO)} cites {repr_}: no such file exists "
        f"(checked repo-relative and by filename against tracked files)"
    )
    for target in targets:
        lines = target.read_text(encoding="utf-8", errors="replace").splitlines()
        if any(literal in line for line in lines):
            return
    tried = ", ".join(str(t.relative_to(REPO)) for t in targets[:5])
    assert False, (
        f"{doc.relative_to(REPO)} cites {repr_}: anchor not found on any raw "
        f"line of any candidate ({tried}"
        f"{', ...' if len(targets) > 5 else ''}) — wrapped in the target, "
        f"edited, or never there"
    )


def test_conventions_are_present() -> None:
    """Guard the extractor itself: if the regexes rot and extract nothing, that
    must fail rather than green-wash an empty run."""
    assert len(_CASES) >= 100, (
        f"only {len(_CASES)} anchored citations extracted from docs/ — the "
        "extractor or the docs changed shape; expected 100+ (VERIFIED-FACTS.md "
        "alone carries ~104)"
    )
