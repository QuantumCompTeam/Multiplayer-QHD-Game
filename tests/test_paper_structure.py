import re
from pathlib import Path

PAPER = Path("paper/qhd.tex")


def _section_iii_block(text: str) -> str:
    """Section III = everything between \\label{sec:model} and \\label{sec:sim}."""
    start = text.index(r"\label{sec:model}")
    end = text.index(r"\label{sec:sim}")
    return text[start:end]


def test_restricted_equilibrium_is_not_overstated():
    text = PAPER.read_text(encoding="utf-8")
    prohibited = [
        "full SU(2) Nash equilibrium on hardware",
        "unrestricted quantum Nash equilibrium",
        "universal quantum Nash equilibrium",
    ]
    for phrase in prohibited:
        assert phrase not in text


def test_no_hype_adjectives():
    text = PAPER.read_text(encoding="utf-8").lower()
    for word in ["groundbreaking", "remarkable", "surprisingly"]:
        assert word not in text, f"style guide 7.1 bans '{word}'"


def test_section_iii_uses_canonical_target_state_name():
    # Scoped to Section III during Phase 1; later phase plans extend the ban
    # paper-wide as each section is rewritten.
    block = _section_iii_block(PAPER.read_text(encoding="utf-8"))
    assert "ground-state population" not in block
    assert "ground state population" not in block


def _section_iii_e_block(text: str) -> str:
    """III-E = its canonical heading through the next subsection boundary."""
    heading = r"\subsection{Expected Payoff, Advantage, Equilibrium, and Fairness}"
    start = text.index(heading)
    following = re.search(r"\n\\subsection\{", text[start + len(heading) :])
    assert following is not None, "III-E must be followed by another subsection"
    end = start + len(heading) + following.start()
    return text[start:end]


def _compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def test_section_iii_does_not_claim_unsupported_state_fidelity():
    block = _section_iii_block(PAPER.read_text(encoding="utf-8"))
    unsupported = block.replace("not state fidelity", "")
    assert "state fidelity" not in unsupported


def test_section_iii_e_has_canonical_heading_and_label():
    block = _section_iii_e_block(PAPER.read_text(encoding="utf-8"))
    assert block.startswith(
        r"\subsection{Expected Payoff, Advantage, Equilibrium, and Fairness}"
    )
    assert r"\label{sec:metrics}" in block


def test_section_iii_e_defines_expected_payoff_and_primary_vector():
    block = _compact(_section_iii_e_block(PAPER.read_text(encoding="utf-8")))
    assert r"\pi_j(\boldsymbolU;T)=\sum_xp_T(x\mid\boldsymbolU)P_j(x)" in block
    assert r"\boldsymbol\pi=(\pi_1,\ldots,\pi_N)" in block
    assert "payoffvectorremainstheprimaryevidence" in block.lower()


def test_section_iii_e_requires_both_deviations_for_every_player():
    block = _compact(_section_iii_e_block(PAPER.read_text(encoding="utf-8")))
    assert r"g_j(a)=\pi_j(Q_N^{\otimesN})-\pi_j(a,Q_{N,-j})" in block
    assert r"a\in\{D,H\}" in block
    lower = block.lower()
    assert "bothdeviations" in lower
    assert "everyplayer" in lower
    assert r"g_j(a)\geq0" in block


def test_section_iii_e_keeps_advantage_metrics_distinct():
    block = _section_iii_e_block(PAPER.read_text(encoding="utf-8"))
    compact = _compact(block)
    assert "analytic-baseline advantage" in block
    assert "circuit-relative payoff gap" in block
    assert (
        r"\Delta_{\mathrm{ana}}(\boldsymbolU;T)"
        r"=\bar\pi(\boldsymbolU;T)-\frac{V-C}{N}"
    ) in compact
    assert (
        r"\Delta_{\mathrm{circ}}(T)"
        r"=\bar\pi(Q_N^{\otimesN};T)"
        r"-\max_{\boldsymbola\in\mathcalE_T^{D,H}}\bar\pi(\boldsymbola;T)"
    ) in compact
    assert r"\begin{tabular}" in block
    assert compact.count("analytic-baselineadvantage") >= 2
    assert compact.count("circuit-relativepayoffgap") >= 2


def test_section_iii_e_defines_all_zero_population_as_not_fidelity():
    block = _section_iii_e_block(PAPER.read_text(encoding="utf-8"))
    compact = _compact(block)
    assert "all-zero target-state population" in block
    assert "target-state population" in block
    assert r"P(0^N)\equivp_T(0^N\mid\boldsymbolU)" in compact
    assert "not state fidelity" in block


def test_section_iii_e_defines_vector_first_fairness_summaries():
    block = _compact(_section_iii_e_block(PAPER.read_text(encoding="utf-8")))
    assert r"S_\pi=\max_j\pi_j-\min_j\pi_j" in block
    assert r"F_\pi=\min_j\pi_j" in block
    assert "fairnessrange" in block.lower()
    assert "playerfloor" in block.lower()
    assert "donotreplacethepayoffvector" in block.lower()


def test_section_iii_e_definitions_precede_summaries_and_table():
    block = _compact(_section_iii_e_block(PAPER.read_text(encoding="utf-8")))
    ordered = [
        r"\pi_j(\boldsymbolU;T)",
        r"\bar\pi(\boldsymbolU;T)",
        r"g_j(a)",
        r"\Delta_{\mathrm{ana}}(\boldsymbolU;T)",
        r"\Delta_{\mathrm{circ}}(T)",
        r"\begin{tabular}",
        r"P(0^N)\equiv",
        r"S_\pi=",
    ]
    positions = [block.index(item) for item in ordered]
    assert positions == sorted(positions)


def test_section_iii_defines_payoff_metrics_before_symbolic_use():
    block = _section_iii_block(PAPER.read_text(encoding="utf-8"))
    metrics = _section_iii_e_block(PAPER.read_text(encoding="utf-8"))
    assert block.index(r"\pi_j") == block.index(metrics) + metrics.index(r"\pi_j")
    assert block.index(r"\boldsymbol\pi") == block.index(metrics) + metrics.index(
        r"\boldsymbol\pi"
    )
    mean_definition = re.search(
        r"let\s+\$(\\bar\\pi)\$\s+be\s+the\s+resulting\s+mean\s+payoff\s+per\s+player",
        block,
    )
    assert mean_definition is not None
    assert block.index(r"\bar\pi") == mean_definition.start(1)
