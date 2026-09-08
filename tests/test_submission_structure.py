"""Check the active paper structure across included files, not historical prose."""
from pathlib import Path
import re


def expanded(path):
    text = path.read_text(encoding='utf-8')
    text = re.sub(r'(?m)^\s*%.*$', '', text)
    return re.sub(r'\\input\{([^}]+)\}',
                  lambda m: expanded(path.parent / m.group(1)), text)


def test_fqcnn_reference_section_order_and_active_template():
    text = expanded(Path('paper/qhd.tex'))
    assert r'\documentclass[conference,letterpaper,10pt]{IEEEtran}' in text
    assert r'\IEEEauthorblockN{Prithvi Raghu}' in text
    assert r'\IEEEauthorblockN{Aasa Singh Bhui}' in text
    assert re.findall(r'\\section\{([^}]+)\}', text) == [
        'Introduction', 'Related Work', 'Evaluation Questions and Evidence Boundaries',
        'Proposed $N$-Player Quantum Hawk--Dove Framework',
        'Computation and Validation Protocol', 'Experimental Results and Analysis',
        'Discussion', 'Novelty and Technical Differentiation', 'Conclusion']
    assert r'\section*{Data and Code Availability}' in text


def test_included_manuscript_labels_are_unique_and_references_resolve():
    text = expanded(Path('paper/qhd.tex'))
    labels = re.findall(r'\\label\{([^}]+)\}', text)
    refs = re.findall(r'\\(?:eqref|ref)\{([^}]+)\}', text)
    assert len(labels) == len(set(labels))
    assert set(refs) <= set(labels)
