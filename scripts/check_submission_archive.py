"""Verify packaged hashes and compile the portable LaTeX archive in isolation."""
from pathlib import Path
import hashlib
import json
import subprocess
import tempfile
import zipfile


def main():
    root = Path(__file__).resolve().parents[1]
    output = root / 'paper' / 'submission'
    manifest = json.loads((output / 'build-manifest.json').read_text())
    for filename, key in [('qhd-submission-draft.pdf', 'pdf_sha256'),
                          ('qhd-code-and-data.zip', 'code_and_data_sha256')]:
        assert hashlib.sha256((output / filename).read_bytes()).hexdigest() == manifest[key]
    with zipfile.ZipFile(output / 'qhd-code-and-data.zip') as archive:
        assert archive.testzip() is None
        evidence = json.loads(archive.read('evidence-manifest.json'))
        for name, digest in evidence['files'].items():
            assert hashlib.sha256(archive.read(name)).hexdigest() == digest, name
        print(f"Verified {len(evidence['files'])} evidence-file hashes.")
    with tempfile.TemporaryDirectory(prefix='qhd-source-check-') as directory:
        with zipfile.ZipFile(output / 'qhd-latex-source.zip') as archive:
            assert archive.testzip() is None
            assert all(not Path(name).is_absolute() and '..' not in Path(name).parts
                       for name in archive.namelist())
            archive.extractall(directory)
        commands = [['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'qhd.tex'],
                    ['bibtex', 'qhd']]
        commands += [commands[0], commands[0]]
        for command in commands:
            result = subprocess.run(command, cwd=directory, capture_output=True)
            if result.returncode:
                raise RuntimeError(result.stdout.decode(errors='replace'))
        log = (Path(directory) / 'qhd.log').read_text(errors='replace')
        assert 'There were undefined references' not in log
        assert 'Citation `' not in log
        assert 'Overfull' not in log
    print('Portable source archive compiled; no unresolved citations/references or overfull boxes.')


if __name__ == '__main__':
    main()
