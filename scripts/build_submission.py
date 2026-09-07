"""Build a separate manuscript PDF and portable LaTeX source archive."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import zipfile


ROOT = Path(__file__).resolve().parents[1]


def main():
    paper = ROOT / 'paper'
    build = paper / '.journal-build'
    build.mkdir(exist_ok=True)
    commands = [
        ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', '-output-directory=.journal-build', 'qhd.tex'],
        ['bibtex', '.journal-build/qhd'],
        ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', '-output-directory=.journal-build', 'qhd.tex'],
        ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', '-output-directory=.journal-build', 'qhd.tex'],
    ]
    for index, command in enumerate(commands):
        result = subprocess.run(command, cwd=paper, capture_output=True, text=True, errors='replace')
        (build/f'pass-{index}.txt').write_text(result.stdout+'\n'+result.stderr, encoding='utf-8')
        if result.returncode:
            raise RuntimeError(f'{command[0]} failed; inspect {build}/pass-{index}.txt')
    log = (build/'qhd.log').read_text(encoding='utf-8', errors='replace')
    if 'There were undefined references' in log or 'Citation `' in log:
        raise RuntimeError('Unresolved references or citations in manuscript build')
    output = paper / 'submission'
    output.mkdir(exist_ok=True)
    shutil.copy2(build/'qhd.pdf', output/'qhd-submission-draft.pdf')
    files = []
    for pattern in ['*.tex', '*.bib', '*.cls', '*.sty', '*.bst', '*.png', '*.jpg', '*.eps']:
        files.extend(p for p in paper.glob(pattern) if p.name != 'main.tex')
    files.extend(p for p in (paper/'figs').rglob('*') if p.is_file())
    with zipfile.ZipFile(output/'qhd-latex-source.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(set(files)):
            archive.write(path, path.relative_to(paper).as_posix())
    manifest = {'files': {p.relative_to(paper).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(set(files))},
                'pdf_sha256': hashlib.sha256((output/'qhd-submission-draft.pdf').read_bytes()).hexdigest(),
                'git_head': subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip(),
                'git_status': subprocess.check_output(['git','status','--porcelain'], cwd=ROOT, text=True),
                'note': 'Source hashes identify exact content; git status records uncommitted work at build.'}
    (output/'build-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    print(output/'qhd-submission-draft.pdf')


if __name__ == '__main__':
    main()
