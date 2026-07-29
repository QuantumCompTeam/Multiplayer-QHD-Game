# QHD Paper Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the QHD manuscript into a mathematically rigorous, readable, evidence-traceable quantum-game-theory paper organized around entanglement topology as a mechanism-design variable.

**Architecture:** Keep `paper/qhd.tex` as the single manuscript source and make `paper/main.tex` a compatibility wrapper. Build a dedicated `paper_figures` Python package that loads canonical committed artifacts, validates their provenance, and renders one scientific claim per figure under a shared style; existing plotting CLIs become thin wrappers around those pure functions. Rewrite the paper in narrative order only after the mathematical claims, literature set, and final figure assets are independently verified.

**Tech Stack:** Python 3.10+, NumPy 1.26.4, SciPy 1.13.1, Matplotlib 3.9.2, PyYAML, pytest 8+, Qiskit 1.3.2, Qiskit Aer 0.14.2, IEEEtran LaTeX, BibTeX/MiKTeX.

## Global Constraints

- `paper/qhd.tex` is canonical; `paper/main.tex` may only delegate to it.
- Do not rerun historical experiments merely to restyle figures.
- Use the canonical simulation source `results/n-scaling-advantage/2026-07-19T0901Z/` for the fixed-profile topology figures.
- Use `results/gamma-sweep/N4/` for the entanglement-angle figure.
- Use `results/hardware-n3/2026-07-16T013912Z/` for the N=3 validation figures.
- Use only the registered `{3,4,5}` same-chain scaling runs selected by the current `plot_hardware_scaling.py` logic; preserve calibration-epoch grouping and the registration anchor.
- Use `results/hardware-topology/2026-07-25T114621Z/` for topology, equilibrium, and wiring-permutation hardware figures.
- No composite A/B/C evidence figures; one primary claim per output file.
- Figure captions state quantity, sample, uncertainty, and one observation; interpretation belongs in the body.
- Equilibrium claims must say `restricted-menu equilibrium` unless a full SU(2) result is actually established.
- The expression `2+2\cos(2\pi/N)` is a proposition only if a derivation is independently verified; otherwise label it computational.
- Preserve negative results, model failures, uncertainty caveats, and registration scope.
- Use `conda run -n entangled-equilibria ...` for project Python commands.
- Do not add runtime dependencies beyond the versions already declared in `pyproject.toml`.

---

## File Map

### Create

- `src/paper_figures/__init__.py` — public rendering package.
- `src/paper_figures/style.py` — shared publication palette, axis styling, zero annotation, and save helper.
- `src/paper_figures/manifest.py` — typed loader and validator for figure provenance.
- `src/paper_figures/simulation.py` — canonical simulation-data loader and four simulation renderers.
- `src/paper_figures/hardware_n3.py` — N=3 distribution and player-payoff renderers.
- `src/paper_figures/hardware_scaling.py` — run selection, epoch aggregation, and three scaling renderers.
- `src/paper_figures/hardware_topology.py` — topology retention, deviation-gap, and wiring renderers.
- `paper/figure-manifest.yaml` — exact sources, outputs, and sample rules for every paper figure.
- `scripts/build_paper_figures.py` — one command that validates the manifest and writes all final assets to `paper/figs/`.
- `tests/test_paper_figure_style.py` — shared style and zero-annotation tests.
- `tests/test_paper_figure_manifest.py` — provenance and source-presence tests.
- `tests/test_paper_simulation_figures.py` — simulation extraction/rendering tests, including Player 0 at zero.
- `tests/test_paper_hardware_figures.py` — independent hardware output and aggregation tests.
- `tests/test_paper_claims.py` — mathematical claim guards used by the manuscript proofs.
- `tests/test_paper_source.py` — canonical-source, terminology, figure-reference, and section-structure checks.
- `paper/LITERATURE-AUDIT.md` — authoritative-source and DOI verification record.

### Modify

- `paper/qhd.tex` — complete narrative, mathematical, figure, appendix, abstract, and caption rewrite.
- `paper/main.tex` — compatibility wrapper only.
- `paper/README.md` — canonical build and figure-reproduction instructions.
- `paper/references.bib` — expanded, verified literature set.
- `scripts/plot_hardware_result.py` — thin CLI wrapper around `paper_figures.hardware_n3`.
- `scripts/plot_hardware_scaling.py` — thin CLI wrapper around `paper_figures.hardware_scaling`.
- `scripts/plot_hardware_topology.py` — thin CLI wrapper around `paper_figures.hardware_topology`.
- `paper/figs/*` — regenerated independent publication figures.

---

### Task 1: Establish the canonical manuscript and build contract

**Files:**
- Modify: `paper/qhd.tex:1-20`
- Replace: `paper/main.tex`
- Modify: `paper/README.md:1-70`
- Create: `tests/test_paper_source.py`

**Interfaces:**
- Consumes: existing `paper/qhd.tex`, `paper/references.bib`, and IEEEtran build.
- Produces: canonical build target `qhd.tex`; compatibility entry point `main.tex -> qhd.tex`; `paper_text()` test helper used by later tasks.

- [ ] **Step 1: Write canonical-source tests**

```python
# tests/test_paper_source.py
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER_DIR = ROOT / "paper"


def paper_text() -> str:
    return (PAPER_DIR / "qhd.tex").read_text(encoding="utf-8")


def test_qhd_is_canonical_source() -> None:
    qhd = paper_text()
    main = (PAPER_DIR / "main.tex").read_text(encoding="utf-8")
    readme = (PAPER_DIR / "README.md").read_text(encoding="utf-8")
    assert "\\documentclass[conference]{IEEEtran}" in qhd
    assert main.strip().endswith("\\input{qhd.tex}")
    assert "pdflatex --enable-installer -interaction=nonstopmode -halt-on-error qhd.tex" in readme
    assert "bibtex qhd" in readme


def test_qhd_build_comment_names_qhd() -> None:
    assert "% Build: latexmk -pdf qhd.tex" in paper_text()
```

- [ ] **Step 2: Run the tests and confirm they fail on the stale workflow**

Run:

```bash
conda run -n entangled-equilibria pytest tests/test_paper_source.py -q
```

Expected: FAIL because `main.tex` contains the old manuscript and `paper/README.md` builds `main.tex`.

- [ ] **Step 3: Make `qhd.tex` canonical**

Change the header in `paper/qhd.tex` to:

```tex
% Canonical IEEE QCE manuscript — Entangled Equilibria
% Build: latexmk -pdf qhd.tex
% Evidence policy: every numerical claim traces to a named results/ artifact.
```

Replace `paper/main.tex` with exactly:

```tex
% Compatibility entry point. The canonical manuscript is qhd.tex.
\input{qhd.tex}
```

Update the README build sequence to:

```powershell
pdflatex --enable-installer -interaction=nonstopmode -halt-on-error qhd.tex
bibtex qhd
pdflatex --enable-installer -interaction=nonstopmode -halt-on-error qhd.tex
pdflatex --enable-installer -interaction=nonstopmode -halt-on-error qhd.tex
```

State that the expected artifact is `paper/qhd.pdf` and that `main.tex` exists only for compatibility.

- [ ] **Step 4: Run the source tests**

Run:

```bash
conda run -n entangled-equilibria pytest tests/test_paper_source.py -q
```

Expected: PASS.

- [ ] **Step 5: Build the current manuscript under the canonical job name**

Run from `paper/`:

```powershell
pdflatex --enable-installer -interaction=nonstopmode -halt-on-error qhd.tex
bibtex qhd
pdflatex --enable-installer -interaction=nonstopmode -halt-on-error qhd.tex
pdflatex --enable-installer -interaction=nonstopmode -halt-on-error qhd.tex
```

Expected: `qhd.pdf` exists; no undefined-control-sequence or missing-file error.

- [ ] **Step 6: Commit the canonical-source contract**

```bash
git add paper/qhd.tex paper/main.tex paper/README.md tests/test_paper_source.py
git commit -m "paper: make qhd the canonical manuscript"
```

---

### Task 2: Add a shared publication figure style

**Files:**
- Create: `src/paper_figures/__init__.py`
- Create: `src/paper_figures/style.py`
- Create: `tests/test_paper_figure_style.py`

**Interfaces:**
- Produces:
  - `apply_paper_style() -> None`
  - `style_axis(ax: Axes, *, grid_axis: str = "y") -> None`
  - `annotate_zero(ax: Axes, x: float, *, label: str = "0.00", color: str = INK) -> Text`
  - `save_figure(fig: Figure, output_stem: Path, *, dpi: int = 300) -> tuple[Path, Path]`
- Consumed by: every renderer in Tasks 4-7.

- [ ] **Step 1: Write failing tests for style, zero annotation, and paired outputs**

```python
# tests/test_paper_figure_style.py
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from paper_figures.style import annotate_zero, save_figure, style_axis


def test_annotate_zero_makes_zero_value_visible() -> None:
    fig, ax = plt.subplots()
    text = annotate_zero(ax, 0.0)
    assert text.get_text() == "0.00"
    assert text.get_position()[1] > 0.0
    plt.close(fig)


def test_style_axis_removes_top_and_right_spines() -> None:
    fig, ax = plt.subplots()
    style_axis(ax)
    assert not ax.spines["top"].get_visible()
    assert not ax.spines["right"].get_visible()
    plt.close(fig)


def test_save_figure_writes_png_and_pdf(tmp_path: Path) -> None:
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    png, pdf = save_figure(fig, tmp_path / "example")
    assert png.stat().st_size > 0
    assert pdf.stat().st_size > 0
```

- [ ] **Step 2: Run the tests and confirm the package is missing**

```bash
conda run -n entangled-equilibria pytest tests/test_paper_figure_style.py -q
```

Expected: FAIL with `ModuleNotFoundError: paper_figures`.

- [ ] **Step 3: Implement the shared style**

```python
# src/paper_figures/style.py
from pathlib import Path
from typing import Literal

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.text import Text

DATA = "#2563eb"
DATA_LIGHT = "#93c5fd"
INK = "#111827"
MUTED = "#6b7280"
GRID = "#e5e7eb"
ACCENT = "#b91c1c"


def apply_paper_style() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9.5,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "axes.titlesize": 10.5,
        "axes.titleweight": "semibold",
    })


def style_axis(ax: Axes, *, grid_axis: Literal["x", "y", "both"] = "y") -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.tick_params(colors=INK, length=3)
    ax.set_axisbelow(True)
    ax.grid(True, axis=grid_axis, color=GRID, linewidth=0.8)


def annotate_zero(ax: Axes, x: float, *, label: str = "0.00", color: str = INK) -> Text:
    return ax.annotate(
        label,
        xy=(x, 0.0),
        xytext=(0, 7),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=8,
        color=color,
        fontweight="semibold",
        clip_on=False,
    )


def save_figure(fig: Figure, output_stem: Path, *, dpi: int = 300) -> tuple[Path, Path]:
    output_stem.parent.mkdir(parents=True, exist_ok=True)
    png = output_stem.with_suffix(".png")
    pdf = output_stem.with_suffix(".pdf")
    fig.savefig(png, dpi=dpi, bbox_inches="tight")
    fig.savefig(pdf, bbox_inches="tight")
    plt.close(fig)
    return png, pdf
```

Create `src/paper_figures/__init__.py` with a one-line package docstring.

- [ ] **Step 4: Run the style tests**

```bash
conda run -n entangled-equilibria pytest tests/test_paper_figure_style.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit the shared style**

```bash
git add src/paper_figures tests/test_paper_figure_style.py
git commit -m "feat: add shared paper figure style"
```

---

### Task 3: Define and validate the figure provenance manifest

**Files:**
- Create: `paper/figure-manifest.yaml`
- Create: `src/paper_figures/manifest.py`
- Create: `tests/test_paper_figure_manifest.py`

**Interfaces:**
- Produces:
  - `FigureEntry(key: str, sources: tuple[Path, ...], outputs: tuple[Path, ...], sample_rule: str)`
  - `load_manifest(path: Path, repo_root: Path) -> dict[str, FigureEntry]`
  - `validate_manifest(entries: dict[str, FigureEntry]) -> None`
- Consumed by: `scripts/build_paper_figures.py` in Task 8.

- [ ] **Step 1: Write failing manifest tests**

```python
# tests/test_paper_figure_manifest.py
from pathlib import Path

from paper_figures.manifest import load_manifest, validate_manifest

ROOT = Path(__file__).resolve().parents[1]


def test_manifest_sources_exist_and_outputs_are_unique() -> None:
    entries = load_manifest(ROOT / "paper" / "figure-manifest.yaml", ROOT)
    validate_manifest(entries)
    outputs = [path for entry in entries.values() for path in entry.outputs]
    assert len(outputs) == len(set(outputs))


def test_scaling_manifest_names_registered_same_chain_runs() -> None:
    entries = load_manifest(ROOT / "paper" / "figure-manifest.yaml", ROOT)
    scaling = entries["hardware_scaling"]
    assert len(scaling.sources) == 3
    assert all("hardware-scaling" in str(path) for path in scaling.sources)
    assert "same physical chain" in scaling.sample_rule.lower()
    assert "calibration epoch" in scaling.sample_rule.lower()
```

- [ ] **Step 2: Run tests and confirm the manifest module is missing**

```bash
conda run -n entangled-equilibria pytest tests/test_paper_figure_manifest.py -q
```

Expected: FAIL.

- [ ] **Step 3: Create the exact manifest**

```yaml
# paper/figure-manifest.yaml
figures:
  simulation_landscape:
    sources:
      - results/n-scaling-advantage/2026-07-19T0901Z/results.json
    outputs:
      - paper/figs/advantage_vs_N.png
      - paper/figs/advantage_vs_N.pdf
      - paper/figs/topology_heatmap.png
      - paper/figs/topology_heatmap.pdf
      - paper/figs/per_player_advantage_star.png
      - paper/figs/per_player_advantage_star.pdf
    sample_rule: "Canonical V=4, C=3, gamma=pi/2 fixed-profile sweep; no rerun."
  gamma_transition:
    sources:
      - results/gamma-sweep/N4/results.json
    outputs:
      - paper/figs/advantage_vs_gamma_N4.png
      - paper/figs/advantage_vs_gamma_N4.pdf
    sample_rule: "N=4 gamma sweep; filled points indicate the recorded restricted-menu equilibrium verdict."
  hardware_n3:
    sources:
      - results/hardware-n3/2026-07-16T013912Z/result.json
      - results/hardware-n3/2026-07-16T013912Z/calibration.json
    outputs:
      - paper/figs/hardware_n3_distribution.png
      - paper/figs/hardware_n3_distribution.pdf
      - paper/figs/hardware_n3_payoff.png
      - paper/figs/hardware_n3_payoff.pdf
    sample_rule: "Single registered N=3 GHZ hardware execution; 4096 shots."
  hardware_scaling:
    sources:
      - results/hardware-scaling/2026-07-16T074134Z/result.json
      - results/hardware-scaling/2026-07-17T014458Z/result.json
      - results/hardware-scaling/2026-07-26T090122Z/result.json
    outputs:
      - paper/figs/hardware_scaling_advantage.png
      - paper/figs/hardware_scaling_advantage.pdf
      - paper/figs/hardware_scaling_zne.png
      - paper/figs/hardware_scaling_zne.pdf
      - paper/figs/hardware_scaling_ground_state.png
      - paper/figs/hardware_scaling_ground_state.pdf
    sample_rule: "Registered N=3,4,5 batch only; same physical chain; runs sharing a calibration stamp form one calibration epoch; model curves use the registration anchor."
  hardware_topology:
    sources:
      - results/hardware-topology/2026-07-25T114621Z/result.json
    outputs:
      - paper/figs/hardware_topology_retention.png
      - paper/figs/hardware_topology_retention.pdf
      - paper/figs/hardware_equilibrium_gaps.png
      - paper/figs/hardware_equilibrium_gaps.pdf
      - paper/figs/hardware_star_wiring.png
      - paper/figs/hardware_star_wiring.pdf
    sample_rule: "Registered 49-pub topology batch; fold-1 mitigated values; identity wiring except the explicit star-wiring control."
```

- [ ] **Step 4: Implement typed loading and validation**

```python
# src/paper_figures/manifest.py
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class FigureEntry:
    key: str
    sources: tuple[Path, ...]
    outputs: tuple[Path, ...]
    sample_rule: str


def load_manifest(path: Path, repo_root: Path) -> dict[str, FigureEntry]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))["figures"]
    return {
        key: FigureEntry(
            key=key,
            sources=tuple(repo_root / p for p in value["sources"]),
            outputs=tuple(repo_root / p for p in value["outputs"]),
            sample_rule=str(value["sample_rule"]),
        )
        for key, value in raw.items()
    }


def validate_manifest(entries: dict[str, FigureEntry]) -> None:
    missing = [path for entry in entries.values() for path in entry.sources if not path.exists()]
    if missing:
        raise FileNotFoundError("missing figure sources: " + ", ".join(map(str, missing)))
    outputs = [path for entry in entries.values() for path in entry.outputs]
    if len(outputs) != len(set(outputs)):
        raise ValueError("figure outputs must be unique")
    if any(not entry.sample_rule.strip() for entry in entries.values()):
        raise ValueError("every figure entry requires a sample_rule")
```

- [ ] **Step 5: Run manifest tests**

```bash
conda run -n entangled-equilibria pytest tests/test_paper_figure_manifest.py -q
```

Expected: PASS.

- [ ] **Step 6: Commit the provenance contract**

```bash
git add paper/figure-manifest.yaml src/paper_figures/manifest.py tests/test_paper_figure_manifest.py
git commit -m "paper: add figure provenance manifest"
```

---

### Task 4: Render the four simulation figures from committed artifacts

**Files:**
- Create: `src/paper_figures/simulation.py`
- Create: `tests/test_paper_simulation_figures.py`
- Do not modify: canonical `results/**` artifacts.

**Interfaces:**
- Produces:
  - `SimulationCell`
  - `load_cells(path: Path) -> list[SimulationCell]`
  - `render_advantage_vs_n(cells, output_stem) -> tuple[Path, Path]`
  - `render_topology_heatmap(cells, output_stem) -> tuple[Path, Path]`
  - `render_gamma_transition(cells, output_stem) -> tuple[Path, Path]`
  - `plot_star_player_advantage(cells) -> tuple[Figure, Axes]`
  - `render_star_player_advantage(cells, output_stem) -> tuple[Path, Path]`
- Consumes: style helpers from Task 2.

- [ ] **Step 1: Write loader and Player 0 regression tests**

```python
# tests/test_paper_simulation_figures.py
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from paper_figures.simulation import (
    load_cells,
    plot_star_player_advantage,
    render_advantage_vs_n,
    render_gamma_transition,
    render_star_player_advantage,
    render_topology_heatmap,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "results" / "n-scaling-advantage" / "2026-07-19T0901Z" / "results.json"


def test_canonical_star_n4_contains_player_zero_at_zero() -> None:
    cells = load_cells(SOURCE)
    cell = next(c for c in cells if c.topology == "star" and c.N == 4)
    assert cell.advantage_vector == pytest.approx((0.0, 1.0, 1.0, 1.0), abs=1e-6)


def test_star_plot_explicitly_labels_zero_player() -> None:
    cells = load_cells(SOURCE)
    fig, ax = plot_star_player_advantage(cells)
    labels = {text.get_text() for text in ax.texts}
    assert "0.00" in labels
    assert [tick.get_text() for tick in ax.get_xticklabels()] == ["4", "5", "6"]
    plt.close(fig)
```

- [ ] **Step 2: Run tests and confirm the simulation module is missing**

```bash
conda run -n entangled-equilibria pytest tests/test_paper_simulation_figures.py -q
```

Expected: FAIL.

- [ ] **Step 3: Implement a strict canonical-result loader**

Use a frozen dataclass and reject malformed cells:

```python
@dataclass(frozen=True)
class SimulationCell:
    N: int
    topology: str
    gamma: float
    advantage: float
    q_is_nash: bool
    symmetric: bool
    advantage_vector: tuple[float, ...]


def load_cells(path: Path) -> list[SimulationCell]:
    raw = json.loads(path.read_text(encoding="utf-8"))["cells"]
    cells = []
    for row in raw:
        if row["status"] != "ok":
            raise ValueError(f"paper source contains failed cell: {row}")
        vector = tuple(float(v) for v in row["detail"]["advantage_vector"])
        if len(vector) != int(row["N"]):
            raise ValueError(f"wrong vector length for {row['topology']} N={row['N']}")
        cells.append(SimulationCell(
            N=int(row["N"]),
            topology=str(row["topology"]),
            gamma=float(row["gamma"]),
            advantage=float(row["advantage"]),
            q_is_nash=bool(row["q_is_nash"]),
            symmetric=bool(row["symmetric"]),
            advantage_vector=vector,
        ))
    return cells
```

- [ ] **Step 4: Implement the star fairness figure first**

Create grouped hub, leaf, and mean bars for only asymmetric star cells. Use `annotate_zero()` whenever `abs(value) < 1e-9`. Label the x-axis with the actual included values `4,5,6`; do not mention `N=2,3` in the title or caption.

Return `(fig, ax)` from `plot_star_player_advantage()` so tests can inspect labels, and use `render_star_player_advantage()` to save PNG/PDF.

- [ ] **Step 5: Run the Player 0 tests**

```bash
conda run -n entangled-equilibria pytest tests/test_paper_simulation_figures.py -q
```

Expected: PASS.

- [ ] **Step 6: Add tests for the remaining three simulation outputs**

```python
def test_all_simulation_renderers_write_independent_files(tmp_path: Path) -> None:
    landscape = load_cells(SOURCE)
    gamma = load_cells(ROOT / "results" / "gamma-sweep" / "N4" / "results.json")
    outputs = [
        render_advantage_vs_n(landscape, tmp_path / "advantage_vs_N"),
        render_topology_heatmap(landscape, tmp_path / "topology_heatmap"),
        render_gamma_transition(gamma, tmp_path / "advantage_vs_gamma_N4"),
        render_star_player_advantage(landscape, tmp_path / "per_player_advantage_star"),
    ]
    paths = [path for pair in outputs for path in pair]
    assert len(paths) == 8
    assert all(path.stat().st_size > 0 for path in paths)
```

- [ ] **Step 7: Implement the remaining renderers**

Requirements:

- advantage-vs-$N$: use a short external legend in fixed topology order, real computed markers, no spline overshoot, and an explicit ring $N=4$ zero annotation; do not place labels inside the data region;
- heatmap: fixed topology order `GHZ, W, ring, star, fully connected`; direct two-decimal labels; contrasting text chosen from cell luminance; explicit zero outline for ring $N=4$;
- gamma transition: filled markers only for recorded restricted-menu equilibrium; title describes the transition rather than repeating the axes;
- every renderer calls `apply_paper_style()`, `style_axis()`, and `save_figure()`.

- [ ] **Step 8: Run simulation figure tests**

```bash
conda run -n entangled-equilibria pytest tests/test_paper_simulation_figures.py -q
```

Expected: PASS.

- [ ] **Step 9: Commit simulation figure generation**

```bash
git add src/paper_figures/simulation.py tests/test_paper_simulation_figures.py
git commit -m "feat: rebuild simulation paper figures"
```

---

### Task 5: Split the N=3 hardware validation into two figures

**Files:**
- Create: `src/paper_figures/hardware_n3.py`
- Modify: `scripts/plot_hardware_result.py`
- Extend: `tests/test_paper_hardware_figures.py`

**Interfaces:**
- Produces:
  - `N3Data`
  - `load_n3_result(path: Path) -> N3Data`
  - `render_n3_distribution(data, output_stem) -> tuple[Path, Path]`
  - `render_n3_payoff(data, output_stem) -> tuple[Path, Path]`
- CLI output names: `hardware_n3_distribution.{png,pdf}` and `hardware_n3_payoff.{png,pdf}`.

- [ ] **Step 1: Write failing independent-output tests**

```python
# tests/test_paper_hardware_figures.py
from pathlib import Path

from paper_figures.hardware_n3 import load_n3_result, render_n3_distribution, render_n3_payoff

ROOT = Path(__file__).resolve().parents[1]
N3_RESULT = ROOT / "results" / "hardware-n3" / "2026-07-16T013912Z" / "result.json"


def test_n3_renderers_create_two_independent_figures(tmp_path: Path) -> None:
    data = load_n3_result(N3_RESULT)
    outputs = [
        render_n3_distribution(data, tmp_path / "hardware_n3_distribution"),
        render_n3_payoff(data, tmp_path / "hardware_n3_payoff"),
    ]
    assert all(path.stat().st_size > 0 for pair in outputs for path in pair)
    assert data.N == 3
    assert data.shots == 4096
```

- [ ] **Step 2: Run the test and confirm failure**

```bash
conda run -n entangled-equilibria pytest tests/test_paper_hardware_figures.py::test_n3_renderers_create_two_independent_figures -q
```

Expected: FAIL.

- [ ] **Step 3: Move pure loading and uncertainty calculations into `hardware_n3.py`**

Keep the current numerical definitions unchanged:

```python
probability_sigma = np.sqrt(probs * (1.0 - probs) / shots)
variance = (coefficients ** 2 * probs[:, None]).sum(0) - payoff ** 2
payoff_sigma = np.sqrt(np.clip(variance, 0.0, None) / shots)
```

Store values in a frozen `N3Data` dataclass so rendering does not reopen files.

- [ ] **Step 4: Implement two single-claim renderers**

- Distribution figure: measured and ideal probabilities over all eight outcomes; annotate only probabilities at or above 0.02.
- Player-payoff figure: three player bars with propagated uncertainty and directly labelled classical/quantum reference lines.
- No panel letters and no shared super-title.

- [ ] **Step 5: Replace the old CLI body with a thin wrapper**

```python
def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python scripts/plot_hardware_result.py <result.json>")
    result_path = Path(sys.argv[1])
    data = load_n3_result(result_path)
    out = result_path.parent / "plots"
    render_n3_distribution(data, out / "hardware_n3_distribution")
    render_n3_payoff(data, out / "hardware_n3_payoff")
```

Do not regenerate a composite `hardware_n3_validation.pdf`.

- [ ] **Step 6: Run the N=3 test and CLI smoke test**

```bash
conda run -n entangled-equilibria pytest tests/test_paper_hardware_figures.py::test_n3_renderers_create_two_independent_figures -q
conda run -n entangled-equilibria python scripts/plot_hardware_result.py results/hardware-n3/2026-07-16T013912Z/result.json
```

Expected: PASS; four independent output files written under the run's `plots/` directory.

- [ ] **Step 7: Commit the N=3 split**

```bash
git add src/paper_figures/hardware_n3.py scripts/plot_hardware_result.py tests/test_paper_hardware_figures.py
git commit -m "feat: split N3 hardware validation figures"
```

---

### Task 6: Split scaling, ZNE, and state quality while preserving sample rules

**Files:**
- Create: `src/paper_figures/hardware_scaling.py`
- Modify: `scripts/plot_hardware_scaling.py`
- Extend: `tests/test_paper_hardware_figures.py`

**Interfaces:**
- Produces:
  - `ScalingSample`
  - `load_scaling_sample(run_dirs: Sequence[Path]) -> ScalingSample`
  - `render_scaling_advantage(sample, output_stem)`
  - `render_zne_diagnostic(sample, output_stem)`
  - `render_ground_state(sample, output_stem)`
- Preserves: registered `{3,4,5}` series, same-chain validation, calibration-epoch grouping, oldest-run registration anchor.

- [ ] **Step 1: Write failing sample-selection tests**

```python
SCALING_DIRS = [
    ROOT / "results" / "hardware-scaling" / "2026-07-16T074134Z",
    ROOT / "results" / "hardware-scaling" / "2026-07-17T014458Z",
    ROOT / "results" / "hardware-scaling" / "2026-07-26T090122Z",
]


def test_scaling_sample_preserves_registered_population() -> None:
    sample = load_scaling_sample(SCALING_DIRS)
    assert sample.Ns == (3, 4, 5)
    assert sample.run_count == 3
    assert sample.epoch_count == 2
    assert all(run.chain == sample.chain for run in sample.runs)
    assert sample.anchor.job_id == sample.runs[0].job_id


def test_scaling_renderers_create_three_independent_figures(tmp_path: Path) -> None:
    sample = load_scaling_sample(SCALING_DIRS)
    outputs = [
        render_scaling_advantage(sample, tmp_path / "hardware_scaling_advantage"),
        render_zne_diagnostic(sample, tmp_path / "hardware_scaling_zne"),
        render_ground_state(sample, tmp_path / "hardware_scaling_ground_state"),
    ]
    assert all(path.stat().st_size > 0 for pair in outputs for path in pair)
```

- [ ] **Step 2: Run the scaling tests and confirm failure**

```bash
conda run -n entangled-equilibria pytest tests/test_paper_hardware_figures.py -k scaling -q
```

Expected: FAIL.

- [ ] **Step 3: Implement pure loading and validation**

The loader must raise `ValueError` when:

- a run's series is not exactly `{"3", "4", "5"}`;
- physical chains differ;
- shots differ;
- required `analysis`, `predictions`, or `zne` keys are absent.

Group runs by `calibration_at_submit.json`, falling back to `calibration.json`, and average within a stamp before computing the sample standard deviation across stamps. Keep the current single-epoch fallback to reported within-run sigma.

- [ ] **Step 4: Implement `render_scaling_advantage()`**

Show:

- ideal $3/N$;
- registration-anchor device model;
- registration-anchor effective-$p$ prediction;
- measured raw and measured readout-mitigated+ZNE values;
- retention annotations.

State visually that the ideal decreases as $3/N$ so the descending curve is not itself hardware decay. Do not include ZNE folds or ground-state probability in this figure.

- [ ] **Step 5: Implement `render_zne_diagnostic()`**

Use only the registration anchor. Plot fold factors $1,3,5$, weighted linear fits, and the extrapolated intercept at zero. Directly label each $N$ curve. The function must not use the cross-epoch aggregate for fold points.

- [ ] **Step 6: Implement `render_ground_state()`**

Plot measured aggregate ground-state probability with uncertainty against the anchor device-model prediction and ideal 1.0 line. Do not place the robustness interpretation in the figure title; the manuscript provides that argument.

- [ ] **Step 7: Replace the scaling CLI with a thin wrapper**

Keep the existing run discovery and explicit exclusion messages, but delegate all rendering to the three module functions and write:

```text
hardware_scaling_advantage.{png,pdf}
hardware_scaling_zne.{png,pdf}
hardware_scaling_ground_state.{png,pdf}
```

Replace the giant generated caption with a short `provenance.md` that records included runs, epochs, chain, shots, and uncertainty definition.

- [ ] **Step 8: Run tests and the canonical CLI**

```bash
conda run -n entangled-equilibria pytest tests/test_paper_hardware_figures.py -k scaling -q
conda run -n entangled-equilibria python scripts/plot_hardware_scaling.py results/hardware-scaling/2026-07-16T074134Z results/hardware-scaling/2026-07-17T014458Z results/hardware-scaling/2026-07-26T090122Z
```

Expected: tests PASS; six independent figure files written; output reports three runs, two epochs, one chain.

- [ ] **Step 9: Commit the scaling split**

```bash
git add src/paper_figures/hardware_scaling.py scripts/plot_hardware_scaling.py tests/test_paper_hardware_figures.py
git commit -m "feat: split hardware scaling diagnostics"
```

---

### Task 7: Split topology retention, equilibrium, and wiring evidence

**Files:**
- Create: `src/paper_figures/hardware_topology.py`
- Modify: `scripts/plot_hardware_topology.py`
- Extend: `tests/test_paper_hardware_figures.py`

**Interfaces:**
- Produces:
  - `TopologyBatch`
  - `load_topology_batch(path: Path) -> TopologyBatch`
  - `render_topology_retention(batch, output_stem)`
  - `render_equilibrium_gaps(batch, output_stem)`
  - `render_star_wiring(batch, output_stem)`

- [ ] **Step 1: Write failing scientific-extraction tests**

```python
TOPOLOGY_RESULT = ROOT / "results" / "hardware-topology" / "2026-07-25T114621Z" / "result.json"


def test_topology_batch_extracts_registered_claims() -> None:
    batch = load_topology_batch(TOPOLOGY_RESULT)
    gaps = batch.equilibrium_gaps
    assert len(gaps) == 3
    assert all(gap > 0.0 for gap in gaps)
    assert batch.star_wiring_payoffs.shape[1] == 4


def test_topology_renderers_create_three_independent_figures(tmp_path: Path) -> None:
    batch = load_topology_batch(TOPOLOGY_RESULT)
    outputs = [
        render_topology_retention(batch, tmp_path / "hardware_topology_retention"),
        render_equilibrium_gaps(batch, tmp_path / "hardware_equilibrium_gaps"),
        render_star_wiring(batch, tmp_path / "hardware_star_wiring"),
    ]
    assert all(path.stat().st_size > 0 for pair in outputs for path in pair)
```

- [ ] **Step 2: Run the tests and confirm failure**

```bash
conda run -n entangled-equilibria pytest tests/test_paper_hardware_figures.py -k topology -q
```

Expected: FAIL.

- [ ] **Step 3: Implement a strict batch loader**

Move `cooperative_cells()` and the current panel-specific extraction into pure typed data. Validate:

- all-Q cells use $\gamma=\pi/2$;
- identity wiring is used for retention;
- GHZ $N=3$ has one cooperative and three unilateral-Hawk series;
- star $N=4$ wiring-control series have four player payoffs;
- ring $N=4$ ideal advantage is exactly zero within tolerance and is therefore not assigned a retention percentage.

- [ ] **Step 4: Implement three renderers**

- Retention: one bar per runnable topology-$N$ cell, direct percentage labels, and a clearly separate `ideal advantage = 0` marker for ring $N=4$.
- Equilibrium gaps: three player bars with zero reference and positive-gap interpretation in the manuscript, not the title.
- Wiring: player-position x-axis with the hub explicitly named; three wiring series and noiseless reference; direct line labels where possible.

Do not create `hardware_topology.pdf`.

- [ ] **Step 5: Replace the topology CLI with a thin wrapper**

Write six independent files under the run's `plots/` directory and a short `provenance.md` containing job ID, shots, pinned qubits, and registered batch scope.

- [ ] **Step 6: Run tests and canonical CLI**

```bash
conda run -n entangled-equilibria pytest tests/test_paper_hardware_figures.py -k topology -q
conda run -n entangled-equilibria python scripts/plot_hardware_topology.py results/hardware-topology/2026-07-25T114621Z
```

Expected: PASS; independent retention, equilibrium, and wiring files written.

- [ ] **Step 7: Commit topology figure generation**

```bash
git add src/paper_figures/hardware_topology.py scripts/plot_hardware_topology.py tests/test_paper_hardware_figures.py
git commit -m "feat: split topology hardware evidence"
```

---

### Task 8: Build all canonical paper figures in one reproducible command

**Files:**
- Create: `scripts/build_paper_figures.py`
- Modify: `paper/README.md`
- Modify: `paper/figs/*`
- Extend: `tests/test_paper_figure_manifest.py`

**Interfaces:**
- Consumes: manifest and renderers from Tasks 3-7.
- Produces: `build_all(repo_root: Path, *, output_root: Path | None = None) -> list[Path]` and the final `paper/figs/` assets. When `output_root` is provided, manifest-relative outputs are written beneath it for tests.

- [ ] **Step 1: Write a failing end-to-end figure-build test**

```python
def test_manifest_build_writes_every_declared_output(tmp_path: Path) -> None:
    from build_paper_figures import build_all

    outputs = build_all(ROOT, output_root=tmp_path)
    assert outputs
    assert all(path.exists() and path.stat().st_size > 0 for path in outputs)
    assert len(outputs) == len(set(outputs))
```

The `output_root` argument must preserve manifest-relative names beneath the temporary directory.

- [ ] **Step 2: Run the test and confirm failure**

```bash
conda run -n entangled-equilibria pytest tests/test_paper_figure_manifest.py::test_manifest_build_writes_every_declared_output -q
```

Expected: FAIL because the orchestrator does not exist.

- [ ] **Step 3: Implement explicit dispatch**

`scripts/build_paper_figures.py` must:

1. load and validate `paper/figure-manifest.yaml`;
2. load each canonical artifact once;
3. call the exact renderer associated with each output;
4. verify every declared output exists and is non-empty;
5. print source paths and sample rules;
6. return the written paths.

Do not use filename guessing or dynamic imports. Use an explicit mapping so missing or extra figures are reviewable in code.

- [ ] **Step 4: Run the end-to-end test**

```bash
conda run -n entangled-equilibria pytest tests/test_paper_figure_manifest.py -q
```

Expected: PASS.

- [ ] **Step 5: Generate final assets**

```bash
conda run -n entangled-equilibria python scripts/build_paper_figures.py
```

Expected: all declared PNG/PDF assets appear under `paper/figs/`; no canonical result file changes.

- [ ] **Step 6: Visually inspect every generated figure**

Check at actual IEEE widths:

- 3.5-inch single column;
- 7.16-inch double column only when necessary.

Verify Player 0 `0.00`, ring $N=4$ zero, readable labels, no clipped annotations, no overlapping direct labels, and no panel letters.

- [ ] **Step 7: Document reproduction**

Add to `paper/README.md`:

```powershell
conda run -n entangled-equilibria python scripts/build_paper_figures.py
```

Explain that the command reads only committed canonical artifacts and writes paper assets.

- [ ] **Step 8: Commit the complete figure pipeline and assets**

```bash
git add scripts/build_paper_figures.py paper/figure-manifest.yaml paper/README.md paper/figs tests/test_paper_figure_manifest.py
git commit -m "paper: regenerate independent publication figures"
```

---

### Task 9: Add mathematical regression guards for the main-text proofs

**Files:**
- Create: `tests/test_paper_claims.py`
- Read only: `src/game/payoffs.py`, `src/circuits/topologies.py`, `src/circuits/topology_graphs.py`, `src/game/nash.py`

**Interfaces:**
- Produces verified facts used in `paper/qhd.tex`:
  - welfare identity;
  - GHZ cooperative payoff;
  - restricted-menu deviation values;
  - single-bit-flip mean-payoff invariance;
  - graph permutation covariance.

- [ ] **Step 1: Write the welfare and bit-flip tests**

```python
import itertools

import numpy as np
import pytest

from game.payoffs import expected_payoff


@pytest.mark.parametrize("N", [2, 3, 4, 5, 6])
def test_total_welfare_identity_for_every_basis_outcome(N: int) -> None:
    V, C = 4.0, 3.0
    for bits in itertools.product((0, 1), repeat=N):
        probs = np.zeros(2 ** N)
        probs[int("".join(map(str, bits)), 2)] = 1.0
        total = float(np.sum(expected_payoff(probs, N, V=V, C=C)))
        expected = V - (C if all(bits) else 0.0)
        assert total == pytest.approx(expected)


@pytest.mark.parametrize("N", [3, 4, 5, 6, 7])
def test_single_bit_flip_preserves_mean_payoff(N: int) -> None:
    zero = np.zeros(2 ** N); zero[0] = 1.0
    baseline = float(np.mean(expected_payoff(zero, N)))
    for player in range(N):
        flipped = np.zeros(2 ** N)
        flipped[1 << (N - 1 - player)] = 1.0
        assert float(np.mean(expected_payoff(flipped, N))) == pytest.approx(baseline)
```

- [ ] **Step 2: Add GHZ and restricted-deviation guards**

Use existing `compute_advantage()` and EWL helpers:

```python
from circuits.topologies import ghz_entangler
from game.nash import compute_advantage


@pytest.mark.parametrize("N", [2, 3, 4, 5, 6, 7])
def test_ghz_fixed_profile_has_analytic_advantage_three_over_n(N: int) -> None:
    result = compute_advantage(N=N, V=4.0, C=3.0, entangler=ghz_entangler)
    assert result["advantage"] == pytest.approx(3.0 / N, abs=1e-9)


@pytest.mark.parametrize("N", range(2, 9))
def test_recorded_hawk_deviation_identity(N: int) -> None:
    result = compute_advantage(N=N, V=4.0, C=3.0, entangler=ghz_entangler)
    measured = float(result["deviation_check"][(0, "H")]["deviation_payoff"])
    expected = 2.0 + 2.0 * np.cos(2.0 * np.pi / N)
    assert measured == pytest.approx(expected, abs=1e-9)
```

This test exercises the same payoff tensor and deviation path used by the published artifact; do not introduce a paper-only circuit implementation.

- [ ] **Step 3: Add permutation-covariance guards**

For star $N=4$, swap graph labels 0 and 1 and verify both the operator and payoff-vector covariance:

```python
import networkx as nx

from circuits.topologies import make_pairwise_entangler, star_entangler
from circuits.topology_graphs import topology_graph


def qubit_permutation_matrix(old_to_new: tuple[int, ...]) -> np.ndarray:
    N = len(old_to_new)
    matrix = np.zeros((2 ** N, 2 ** N), dtype=complex)
    for old_index in range(2 ** N):
        old_bits = [(old_index >> j) & 1 for j in range(N)]
        new_bits = [0] * N
        for old, new in enumerate(old_to_new):
            new_bits[new] = old_bits[old]
        new_index = sum(bit << j for j, bit in enumerate(new_bits))
        matrix[new_index, old_index] = 1.0
    return matrix


def test_star_permutation_covariance() -> None:
    N = 4
    permutation = (1, 0, 2, 3)
    mapping = {old: new for old, new in enumerate(permutation)}
    relabelled_graph = nx.relabel_nodes(topology_graph("star", N), mapping, copy=True)
    relabelled_entangler = make_pairwise_entangler(relabelled_graph)
    register_permutation = qubit_permutation_matrix(permutation)

    np.testing.assert_allclose(
        register_permutation @ star_entangler(N) @ register_permutation.conj().T,
        relabelled_entangler(N),
        atol=1e-10,
    )

    original = np.asarray(compute_advantage(
        N=N, V=4.0, C=3.0, entangler=star_entangler
    )["q_payoff_vector"])
    relabelled = np.asarray(compute_advantage(
        N=N, V=4.0, C=3.0, entangler=relabelled_entangler
    )["q_payoff_vector"])
    expected = np.empty_like(original)
    for old, new in enumerate(permutation):
        expected[new] = original[old]
    np.testing.assert_allclose(relabelled, expected, atol=1e-9)
```

This tests the graph-position statement from the model, independently of the hardware plot.

- [ ] **Step 4: Run the new claim tests and observe any unsupported assumptions**

```bash
conda run -n entangled-equilibria pytest tests/test_paper_claims.py -q
```

Expected: welfare, GHZ, and bit-flip tests PASS. If the closed-form deviation or permutation statement fails, stop and revise the intended manuscript statement before writing it as a proposition.

- [ ] **Step 5: Run the existing mathematical regression suite**

```bash
conda run -n entangled-equilibria pytest tests/test_payoffs.py tests/test_ewl.py tests/test_n_player.py tests/test_topologies.py tests/test_asymmetric_advantage.py tests/test_ne_guard.py tests/test_strategy_opt.py tests/test_gate_level.py tests/test_noise.py tests/test_hardware_mitigation.py tests/test_paper_claims.py -q
```

Expected: PASS.

- [ ] **Step 6: Commit the proof guards**

```bash
git add tests/test_paper_claims.py
git commit -m "test: guard mathematical paper claims"
```

---

### Task 10: Rebuild the literature audit and bibliography

**Files:**
- Create: `paper/LITERATURE-AUDIT.md`
- Modify: `paper/references.bib`
- Modify: `paper/qhd.tex:170-209` during the final prose step only after sources are verified.

**Interfaces:**
- Produces: verified BibTeX keys and a sentence-level evidence map consumed by Task 11.

- [ ] **Step 1: Create the audit table and inclusion rules**

Use this exact schema:

```markdown
| Strand | Claim supported | Candidate source | Authoritative URL | DOI/arXiv | BibTeX key | Verified metadata | Used in paper |
|---|---|---|---|---|---|---|---|
```

Add sections for:

1. EWL and foundational quantum games;
2. quantum Hawk--Dove/trading;
3. multiplayer quantum games;
4. graph states and topology-dependent entanglement;
5. quantum economics/mechanism design;
6. fairness in network games;
7. NISQ quantum-game experiments;
8. readout mitigation;
9. ZNE;
10. observable robustness versus fidelity.

- [ ] **Step 2: Search each strand using authoritative sources**

For each candidate, verify against one of:

- publisher article page;
- DOI resolver/Crossref metadata;
- arXiv record for preprints;
- official IBM/Qiskit documentation only for implementation details, not novelty claims.

Reject sources that are only loosely about “quantum finance” or do not support a sentence in the planned paper.

- [ ] **Step 3: Record the exact gap map**

For every retained source, write one sentence in `LITERATURE-AUDIT.md` stating:

- what the source established;
- what variable it did not jointly study;
- where the citation will appear.

Target a professional bibliography of roughly 25-40 verified sources, but stop adding citations when each planned literature strand and method claim is adequately supported.

- [ ] **Step 4: Add verified BibTeX entries**

Every entry must include author, title, venue, year, pages/article number where applicable, and DOI when one exists. Keep title capitalization protected for terms such as `{EWL}`, `{NISQ}`, `{IBM}`, `{GHZ}`, and `{N}`.

- [ ] **Step 5: Check for duplicate keys and duplicate DOIs**

Run:

```bash
python -c "import re, pathlib, collections; t=pathlib.Path('paper/references.bib').read_text(encoding='utf-8'); keys=re.findall(r'@\w+\{([^,]+),', t); dois=[d.lower() for d in re.findall(r'doi\s*=\s*\{([^}]+)\}', t, re.I)]; assert len(keys)==len(set(keys)), [k for k,c in collections.Counter(keys).items() if c>1]; assert len(dois)==len(set(dois)), [d for d,c in collections.Counter(dois).items() if c>1]; print(len(keys), 'unique references')"
```

Expected: unique keys and DOIs.

- [ ] **Step 6: Commit the verified literature set**

```bash
git add paper/LITERATURE-AUDIT.md paper/references.bib
git commit -m "paper: expand verified quantum game literature"
```

---

### Task 11: Rewrite the Introduction, Related Work, and Formal Model

**Files:**
- Modify: `paper/qhd.tex:12-365`
- Extend: `tests/test_paper_source.py`

**Interfaces:**
- Consumes: verified citations from Task 10 and claim tests from Task 9.
- Produces: definitions and notation used verbatim by all later result sections.

- [ ] **Step 1: Add source-structure tests before rewriting**

```python
def test_formal_model_defines_core_quantities_before_results() -> None:
    text = paper_text()
    required = [
        r"\newtheorem{proposition}{Proposition}",
        r"U(\theta,\alpha,\beta)",
        r"P_j(x)",
        r"\pi_j",
        r"\Delta_{\mathrm{circ}}",
        r"\Delta_{\mathrm{ana}}",
        r"S_\pi",
        r"\mathcal{D}_p",
    ]
    for token in required:
        assert token in text
    assert text.index(r"\section{Formal Model}") < text.index(r"\section{Analytical Predictions and Simulation Landscape}")


def test_equilibrium_scope_is_explicit() -> None:
    text = paper_text()
    assert "restricted-menu equilibrium" in text
    assert "not an unrestricted SU(2) Nash equilibrium" in text
```

- [ ] **Step 2: Run the tests and confirm the current source fails**

```bash
conda run -n entangled-equilibria pytest tests/test_paper_source.py -q
```

Expected: FAIL on missing formal definitions and new section names.

- [ ] **Step 3: Rewrite the Introduction around one research question**

Use this argument order:

1. classical multiplayer coordination problem;
2. quantum enforcement without a trusted intermediary;
3. why $N>2$ introduces topology as a design variable;
4. research question;
5. three concise contributions;
6. roadmap.

Do not include job IDs, calibration residuals, or the adaptation pilot in the Introduction.

- [ ] **Step 4: Rewrite Related Work as a gap argument**

Use four main subsections:

```tex
\subsection{Quantum Games and Hawk--Dove Mechanisms}
\subsection{Multiplayer Games and Entanglement Topology}
\subsection{Quantum Economics and Network Fairness}
\subsection{NISQ Validation and Error Mitigation}
```

Each subsection ends with a sentence identifying the unresolved variable combination. Cite only keys verified in `LITERATURE-AUDIT.md`.

- [ ] **Step 5: Add notation and theorem infrastructure**

In the preamble:

```tex
\usepackage{amsthm}
\newtheorem{proposition}{Proposition}
\newtheorem{lemma}{Lemma}
\newcommand{\E}{\mathbb{E}}
\newcommand{\Prob}{\mathbb{P}}
```

Add a notation table before the first proposition.

- [ ] **Step 6: Write the classical payoff model and welfare proof**

Include the full piecewise payoff tensor and a complete proof of:

```tex
\sum_{j=1}^{N}P_j(x)=V-C\mathbf{1}_{\{x=1^N\}},
\qquad
\bar\pi=\frac{V}{N}-\frac{C}{N}\Prob(1^N).
```

Follow the proof with a paragraph explaining that mean welfare depends only on all-Hawk mass, while player-level allocation can still change.

- [ ] **Step 7: Write SU(2), EWL, topology, payoff, and equilibrium definitions**

Include:

- the full $U(\theta,\alpha,\beta)$ matrix;
- exact $D,H,Q_N$ definitions matching code;
- $J_T^\dagger(\otimes_j U_j)J_T|0^N\rangle$;
- GHZ, graph-XX, and W constructions;
- output probability and expected payoff;
- the code-matched circuit-relative comparator
  \[
  \Delta_{\mathrm{circ}}(T,p)=\bar\pi_{T,p}(Q_N^{\otimes N})-
  \max_{s\in\operatorname{NE}(\{D,H\}^N;T,p)}\bar\pi_{T,p}(s),
  \]
  where the maximum is over pure Nash profiles of the restricted classical game evaluated through the same entangler and noise path;
- the analytic-baseline advantage
  \[
  \Delta_{\mathrm{ana}}(T,p)=\bar\pi_{T,p}(Q_N^{\otimes N})-\frac{V-C}{N};
  \]
- restricted deviation inequalities;
- payoff vector and $S_\pi$;
- depolarizing channels;
- readout correction and weighted ZNE equations.

Match `compute_advantage()` exactly: enumerate pure Nash profiles in the restricted classical tensor and select the one with the highest mean payoff; do not replace this with a maximum over only uniform profiles.

- [ ] **Step 8: Write full main-text proofs**

Include full derivations for:

- GHZ cooperative profile and $V/N$ payoff;
- $3/N$ analytic-baseline advantage for $V=4,C=3$;
- single-bit-flip mean-payoff invariance;
- permutation covariance and position locking.

For the Hawk-deviation identity, follow the Task 9 verdict:

- if independently derived and tested, present it as a proposition with proof;
- otherwise present finite tested values and call the expression a computational identity.

Every proof ends with `\paragraph{Interpretation.}` linking the algebra to mechanism design.

- [ ] **Step 9: Run source and mathematical tests**

```bash
conda run -n entangled-equilibria pytest tests/test_paper_source.py tests/test_paper_claims.py -q
```

Expected: PASS.

- [ ] **Step 10: Build LaTeX through the Formal Model**

Run the full four-pass build. Expected: all equations, theorem environments, and citations compile; no undefined references.

- [ ] **Step 11: Commit the mathematical foundation**

```bash
git add paper/qhd.tex tests/test_paper_source.py
git commit -m "paper: rebuild formal quantum game framework"
```

---

### Task 12: Rewrite the simulation section around predictions and mechanisms

**Files:**
- Modify: `paper/qhd.tex` section `Analytical Predictions and Simulation Landscape`
- Modify: figure references to Task 8 outputs.
- Extend: `tests/test_paper_source.py`

**Interfaces:**
- Consumes: formal definitions from Task 11 and simulation assets from Task 8.
- Produces: one question-driven subsection per simulation claim.

- [ ] **Step 1: Add figure-reference tests**

```python
def test_simulation_figures_are_independent_and_referenced() -> None:
    text = paper_text()
    for name in (
        "advantage_vs_N.png",
        "topology_heatmap.png",
        "advantage_vs_gamma_N4.png",
        "per_player_advantage_star.png",
    ):
        assert name in text
    assert "Player 0" in text
    assert "0.00" in text
    assert "N=4,5,6" in text.replace("{=}", "=")
```

- [ ] **Step 2: Write the section opener and hypotheses**

State four predictions before showing figures:

1. GHZ fixed profile yields $V/N$ but restricted equilibrium has an $N$ boundary;
2. topology changes the fixed-profile payoff landscape;
3. non-vertex-transitive topologies can break player symmetry;
4. equilibrium and payoff-gap robustness can disagree under noise.

- [ ] **Step 3: Rewrite zero-noise topology scaling**

Sequence:

1. proposition-derived GHZ expectation;
2. advantage-vs-$N$ figure;
3. explanation of fixed-profile versus topology-optimized interpretation;
4. heatmap figure;
5. direct explanation of ring $N=4$ zero;
6. limitation that the fixed GHZ-derived strategy is not each topology's optimum.

- [ ] **Step 4: Rewrite entanglement-angle dependence**

Define what filled markers mean before the figure. After the figure, explain the transition in restricted equilibrium separately from payoff magnitude. Do not repeat every plotted number in the caption.

- [ ] **Step 5: Rewrite star fairness with the corrected Figure 4**

Before the figure, state that Player 0 is the graph hub. After it, explain:

- $N=4$: hub advantage `0.00`, leaves `1.00`, mean `0.75`;
- the mean does not imply equal player benefit;
- the role is a graph position, not an intrinsic player label.

Use a short caption limited to the dataset, encodings, and zero annotation.

- [ ] **Step 6: Consolidate noise robustness**

Define the two criteria using Section III equations, present their different orderings, and retain W's per-gate-retention caveat. Move finite-round adaptation details to Appendix C and leave only one sentence in the main section explaining why adaptation does not repair the demonstrated mechanism.

- [ ] **Step 7: Run source tests and build**

```bash
conda run -n entangled-equilibria pytest tests/test_paper_source.py -q
```

Then run the four-pass LaTeX build. Expected: figures appear separately with explanatory text between them.

- [ ] **Step 8: Commit the simulation rewrite**

```bash
git add paper/qhd.tex tests/test_paper_source.py
git commit -m "paper: rebuild simulation narrative"
```

---

### Task 13: Rewrite hardware validation as registered tests of prior predictions

**Files:**
- Modify: `paper/qhd.tex` hardware section.
- Extend: `tests/test_paper_source.py`

**Interfaces:**
- Consumes: all independent hardware figures from Task 8 and definitions from Task 11.
- Produces: a registered-prediction sequence with uncertainty and scope stated next to each result.

- [ ] **Step 1: Add tests that reject the old composite figures**

```python
def test_hardware_figures_are_separate() -> None:
    text = paper_text()
    forbidden = [
        "hardware_n3_validation.pdf",
        "hardware_scaling.pdf",
        "hardware_topology.pdf",
    ]
    assert not any(name in text for name in forbidden)
    required = [
        "hardware_n3_distribution.pdf",
        "hardware_n3_payoff.pdf",
        "hardware_scaling_advantage.pdf",
        "hardware_scaling_zne.pdf",
        "hardware_scaling_ground_state.pdf",
        "hardware_topology_retention.pdf",
        "hardware_equilibrium_gaps.pdf",
        "hardware_star_wiring.pdf",
    ]
    assert all(name in text for name in required)
```

- [ ] **Step 2: Rewrite protocol and safeguards**

Present circuit identity, noiseless dry run, device-model rehearsal, persisted job IDs, crash-safe recovery, readout mitigation, and ZNE once. Move full job/qubit/calibration tables to Appendix E.

- [ ] **Step 3: Present N=3 distribution and payoff sequentially**

Order:

1. registered prediction;
2. output-distribution figure;
3. explain observed bit-flip mass;
4. player-payoff figure;
5. derive the measured mean and analytic-baseline advantage;
6. transition to scaling.

- [ ] **Step 4: Present the three former Figure 6 results separately**

Use three subsections:

```tex
\subsection{Payoff-Advantage Scaling Across Calibrations}
\subsection{Zero-Noise Extrapolation Diagnostic}
\subsection{State Quality and Observable Robustness}
```

For each subsection use setup -> figure -> interpretation -> limitation -> transition. Explicitly state:

- scaling and ground-state panels aggregate three runs into two epochs;
- ZNE fold data come from the registration anchor only;
- error bars exclude within-run terms where the current method says so;
- the repeated $N=5$ sign is observational unless registration supports the stronger claim.

- [ ] **Step 5: Present topology, equilibrium, and fairness separately**

Use three subsections and three figures. Preserve:

- retention relative to each cell's own ideal;
- ring $N=4$ has undefined retention because ideal advantage is zero;
- GHZ $N=3$ gaps are restricted-menu evidence;
- star wiring permutation identifies graph position rather than physical qubit as the disadvantaged role.

- [ ] **Step 6: Move secondary hardware diagnostics to appendices**

Move full one-parameter model ranking, $N=6,7$ extension details, absolute-prediction failures, and calibration tables to Appendices D/E. Keep concise main-text conclusions and cross-references.

- [ ] **Step 7: Run source tests and build**

```bash
conda run -n entangled-equilibria pytest tests/test_paper_source.py -q
```

Run the four-pass LaTeX build. Expected: no composite figure references; every hardware figure has body interpretation after it.

- [ ] **Step 8: Commit the hardware rewrite**

```bash
git add paper/qhd.tex tests/test_paper_source.py
git commit -m "paper: rebuild registered hardware narrative"
```

---

### Task 14: Write Discussion, appendices, conclusion, and final abstract

**Files:**
- Modify: `paper/qhd.tex` Discussion, appendices, Conclusion, Abstract.
- Extend: `tests/test_paper_source.py`

**Interfaces:**
- Consumes: stable main-body claims from Tasks 11-13.
- Produces: final manuscript synthesis without repeated result ledgers.

- [ ] **Step 1: Add anti-repetition and appendix-presence tests**

```python
def test_final_structure_has_discussion_and_appendices_without_novelty_section() -> None:
    text = paper_text()
    assert r"\section{Discussion}" in text
    assert r"\appendices" in text
    assert r"\section{Novelty and Technical Differentiation}" not in text
    for title in (
        "Extended Derivations",
        "Circuit Constructions",
        "Finite-Round Adaptation Pilot",
        "Noise Models and Extended Diagnostics",
        "Registration and Reproducibility",
    ):
        assert title in text
```

- [ ] **Step 2: Write Discussion as interpretation, not summary**

Use these subsections:

1. observable robustness versus state fidelity;
2. topology as a mechanism-design choice;
3. mean welfare versus player fairness;
4. cooperative fixed profiles versus equilibrium;
5. model failure and external validity;
6. application scope and limitations.

Each subsection cites prior equations/figures instead of restating all percentages.

- [ ] **Step 3: Write Appendix A — Extended Derivations**

Include algebra omitted from the main proofs: graph-XX commutation/unitarity, topology-specific expansions, and the full restricted-deviation derivation only if verified.

- [ ] **Step 4: Write Appendix B — Circuit Constructions**

Document GHZ, ring, star, fully connected, and W gate-native circuits, exact gate-count conventions, and matched-count controls.

- [ ] **Step 5: Write Appendix C — Finite-Round Adaptation Pilot**

Move the complete provisional update rule, tested $p$ values, convergence/non-convergence outcomes, simultaneous-update control, W $N=5$ extension, and all caveats into one location.

- [ ] **Step 6: Write Appendix D — Noise Models and Extended Diagnostics**

Place the depolarizing and CZ-exponential model race, fit-one-predict-many tests, $N=6,7$ failures, ranking inversion, and absolute-prediction caveats here.

- [ ] **Step 7: Write Appendix E — Registration and Reproducibility**

Include result directories, job IDs, physical chains, calibration stamps, shot counts, software versions, uncertainty definitions, and the figure manifest reference.

- [ ] **Step 8: Rewrite the Conclusion**

Answer the central research question in three parts:

1. topology changes payoff, equilibrium, and fairness;
2. the mechanisms remain measurable on hardware;
3. robustness of the observable does not imply state fidelity or universal equilibrium.

Keep it short and do not introduce new numbers.

- [ ] **Step 9: Rewrite the Abstract last**

Use five moves:

1. problem;
2. method;
3. topology/equilibrium/fairness result;
4. hardware/robustness result;
5. limitation and implication.

Retain only the minimum headline numbers needed to establish scale; remove job-level and model-ranking detail.

- [ ] **Step 10: Run source tests and build**

```bash
conda run -n entangled-equilibria pytest tests/test_paper_source.py -q
```

Run the four-pass build. Expected: all appendices, references, equations, and figures resolve.

- [ ] **Step 11: Commit the completed narrative**

```bash
git add paper/qhd.tex tests/test_paper_source.py
git commit -m "paper: complete discussion and appendices"
```

---

### Task 15: Perform final scientific, visual, and publication verification

**Files:**
- Modify if findings require: `paper/qhd.tex`, `paper/references.bib`, `paper/figs/*`, plotting modules, tests.
- Produce: `paper/qhd.pdf`, `paper/qhd.log` during local verification.

**Interfaces:**
- Consumes: all prior tasks.
- Produces: a tested, built, visually inspected final artifact.

- [ ] **Step 1: Run the complete test suite**

```bash
conda run -n entangled-equilibria pytest -q
```

Expected: PASS.

- [ ] **Step 2: Run lint on all new and modified Python files**

```bash
conda run -n entangled-equilibria ruff check src/paper_figures scripts/build_paper_figures.py scripts/plot_hardware_result.py scripts/plot_hardware_scaling.py scripts/plot_hardware_topology.py tests/test_paper_figure_style.py tests/test_paper_figure_manifest.py tests/test_paper_simulation_figures.py tests/test_paper_hardware_figures.py tests/test_paper_claims.py tests/test_paper_source.py
```

Expected: PASS.

- [ ] **Step 3: Rebuild every figure from the manifest**

```bash
conda run -n entangled-equilibria python scripts/build_paper_figures.py
```

Expected: all outputs regenerated; `git diff -- results/` is empty.

- [ ] **Step 4: Perform a clean LaTeX build**

Delete only generated `qhd.aux`, `qhd.bbl`, `qhd.blg`, `qhd.fdb_latexmk`, `qhd.fls`, `qhd.log`, `qhd.out`, and `qhd.pdf`, then run:

```powershell
pdflatex --enable-installer -interaction=nonstopmode -halt-on-error qhd.tex
bibtex qhd
pdflatex --enable-installer -interaction=nonstopmode -halt-on-error qhd.tex
pdflatex --enable-installer -interaction=nonstopmode -halt-on-error qhd.tex
```

Expected: clean `qhd.pdf` build.

- [ ] **Step 5: Audit LaTeX warnings**

Check `paper/qhd.log` for:

- `Undefined control sequence`;
- `LaTeX Warning: Reference ... undefined`;
- `Citation ... undefined`;
- overfull boxes larger than 5 pt;
- missing files;
- multiply defined labels.

Fix each substantive warning and rebuild.

- [ ] **Step 6: Perform page-by-page visual inspection**

Inspect every page of `paper/qhd.pdf` and verify:

- equations do not overflow columns;
- proof blocks remain readable;
- figures are not clipped or undersized;
- Player 0 at $N=4$ is explicitly visible;
- figure captions are short;
- figures appear after setup and before interpretation;
- no page begins or ends with an unexplained figure;
- appendix tables are legible;
- references render correctly.

- [ ] **Step 7: Perform claim-to-artifact audit**

For every numerical claim, verify an adjacent LaTeX comment or Appendix E entry names the source result directory. Compare displayed values against source JSON/CSV. Confirm that simulation, hardware, proof, and interpretation language remain distinct.

- [ ] **Step 8: Confirm restricted language and negative results**

Search the source for `Nash equilibrium`, `proves`, `state fidelity`, `retention`, and `model`. Verify each occurrence has correct scope. Confirm the model failures, ring $N=4$ caveat, $N=4,5$ cooperative-profile caveat, and exploratory adaptation status remain present.

- [ ] **Step 9: Review the final diff**

```bash
git status --short
git diff --stat
git diff --check
```

Expected: only intended manuscript, bibliography, figure-pipeline, test, documentation, and generated paper-asset changes.

- [ ] **Step 10: Commit final verification fixes**

```bash
git add paper/qhd.tex paper/qhd.pdf paper/main.tex paper/README.md paper/references.bib paper/LITERATURE-AUDIT.md paper/figure-manifest.yaml paper/figs src/paper_figures scripts/build_paper_figures.py scripts/plot_hardware_result.py scripts/plot_hardware_scaling.py scripts/plot_hardware_topology.py tests/test_paper_figure_style.py tests/test_paper_figure_manifest.py tests/test_paper_simulation_figures.py tests/test_paper_hardware_figures.py tests/test_paper_claims.py tests/test_paper_source.py
git commit -m "paper: finalize rigorous QHD manuscript redesign"
```

Do not stage `.aux`, `.bbl`, `.blg`, `.fdb_latexmk`, `.fls`, `.log`, or `.out` build intermediates.
