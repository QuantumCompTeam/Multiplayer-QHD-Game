"""Build a separate manuscript PDF and portable LaTeX source archive."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import zipfile


def write_evidence_archive(root, output):
    """Package tracked research files, excluding accounts and local environments."""
    prefixes = ('src/', 'scripts/', 'tests/', 'experiments/', 'results/', 'docs/')
    named = {'pyproject.toml', 'environment.yml', 'environment.yaml', 'README.md',
             'LICENSE', 'WHAT-WAS-ADDED.md', 'paper/JOURNAL-REVISION-LOG.md',
             'paper/CLAIM-SOURCE-MAP.md', 'paper/LITERATURE-AUDIT.md',
             'paper/submission/README.md'}
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')
    hashes = {}
    destination = output/'qhd-code-and-data.zip'
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(tracked):
            paper_source = name.startswith('paper/') and (
                name.endswith(('.tex', '.bib', '.cls', '.md')) or name.startswith('paper/figs/'))
            root_document = '/' not in name and name.endswith('.md')
            if not name or not (name.startswith(prefixes) or name in named or paper_source or root_document):
                continue
            path = root/name
            if path.is_file():
                content = path.read_bytes()
                archive.writestr(name, content)
                hashes[name] = hashlib.sha256(content).hexdigest()
        # Preserve the exact pre-execution code as well as the audited current
        # code. Hardening validation must not rewrite a historical registration.
        frozen_revision = '76aa8fd'
        frozen = subprocess.check_output(
            ['git', 'ls-tree', '-r', '--name-only', frozen_revision,
             'src', 'scripts', 'experiments', 'pyproject.toml'], cwd=root).decode().splitlines()
        for name in frozen:
            content = subprocess.check_output(['git', 'show', f'{frozen_revision}:{name}'], cwd=root)
            target = f'frozen-phase-code/{name}'
            archive.writestr(target, content)
            hashes[target] = hashlib.sha256(content).hexdigest()
        archive.writestr('evidence-manifest.json', json.dumps(
            {'files': hashes, 'frozen_phase_revision': frozen_revision,
             'scope': 'Offline evidence; live execution still requires a committed Git checkout.'},
            indent=2)+'\n')
    return destination


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
    for pattern in ['*.tex', '*.bib', '*.sty', '*.bst']:
        files.extend(p for p in paper.glob(pattern) if p.name != 'main.tex')
    files.extend(p for p in (paper/'figs').rglob('*') if p.is_file())
    with zipfile.ZipFile(output/'qhd-latex-source.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(set(files)):
            archive.write(path, path.relative_to(paper).as_posix())
        ieee_class = Path(subprocess.check_output(['kpsewhich', 'IEEEtran.cls'], text=True).strip())
        archive.write(ieee_class, 'IEEEtran.cls')
        ieee_bst = Path(subprocess.check_output(['kpsewhich', 'IEEEtran.bst'], text=True).strip())
        if 'IEEEtran.bst' not in archive.namelist():
            archive.write(ieee_bst, 'IEEEtran.bst')
        archive.write(build/'qhd.bbl', 'qhd.bbl')
    evidence = write_evidence_archive(ROOT, output)
    manifest = {'files': {p.relative_to(paper).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(set(files))},
                'ieeetran_cls_sha256': hashlib.sha256(ieee_class.read_bytes()).hexdigest(),
                'ieeetran_bst_sha256': hashlib.sha256(ieee_bst.read_bytes()).hexdigest(),
                'bbl_sha256': hashlib.sha256((build/'qhd.bbl').read_bytes()).hexdigest(),
                'pdf_sha256': hashlib.sha256((output/'qhd-submission-draft.pdf').read_bytes()).hexdigest(),
                'code_and_data_sha256': hashlib.sha256(evidence.read_bytes()).hexdigest(),
                'git_head': subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip(),
                'git_status': subprocess.check_output(['git','status','--porcelain'], cwd=ROOT, text=True),
                'note': 'Source hashes identify exact content; git status records uncommitted work at build.'}
    (output/'build-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    print(output/'qhd-submission-draft.pdf')


if __name__ == '__main__':
    main()
