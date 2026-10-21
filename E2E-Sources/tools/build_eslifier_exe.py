"""Build E2E (ESLifier): one folder, no console, nothing to install but the .NET runtime.

    py -3.11 tools\\build_eslifier_exe.py

PyInstaller --onedir puts the Python app, its runtime, Tk, the record writer (Backend:
framework-dependent .NET 8, rolls forward to any newer .NET) and the licence notices
into build/exe/E2E/ (E2E.exe + _internal). A folder, not a single file, on purpose: a
single-file exe has to unpack itself into Windows' TEMP at every start, and E2E writes
NOTHING outside the work folder the user chooses. Nothing is installed or extracted.
"""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'eslifier'
OUT = ROOT / 'build/exe'
BACKEND = APP / 'backend/bin/Release/net8.0'
RUNTIME = ROOT / 'build/candidate-2026-10-18/LELightSupport.dll'  # the delivered SKSE plugin
LICENSES = ROOT / 'licenses'


def remove_build_tree(folder):
    folder=Path(folder).resolve()
    allowed=(ROOT/'build').resolve()
    if allowed not in folder.parents:
        raise ValueError('Refusing cleanup outside the project build folder: '+str(folder))
    shutil.rmtree(folder,ignore_errors=True)


def licences(target):
    """Every notice E2E must carry: GPL-3.0, dependencies, Python, Tcl/Tk, PyInstaller."""
    remove_build_tree(target)
    shutil.copytree(LICENSES, target)
    python = Path(sys.base_prefix)
    shutil.copy2(python / 'LICENSE.txt', target / 'Python-LICENSE.txt')
    shutil.copy2(python / 'tcl/tk8.6/license.terms', target / 'Tcl-Tk-license.terms')


def main():
    remove_build_tree(OUT)
    work = OUT / 'work'
    work.mkdir(parents=True)
    notices = work / 'Licenses'
    licences(notices)
    hidden = ['eslifier', 'eslifier_gui', 'general_convert', 'nif_worker', 'audit_plugin']
    hidden += ['lib.' + p.stem for p in sorted((APP / 'lib').glob('*.py'))]
    hidden += [p.stem for p in sorted((APP / 'lib').glob('*.py'))]  # also imported bare via sys.path
    command = [sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean', '--onedir', '--windowed', '--name', 'E2E',
               '--distpath', str(OUT), '--workpath', str(work), '--specpath', str(work),
               '--paths', str(APP), '--paths', str(APP / 'lib'),
               '--add-data', f'{BACKEND};Backend', '--add-data', f'{RUNTIME};Runtime', '--add-data', f'{notices};Licenses']
    for name in hidden:
        command += ['--hidden-import', name]
    # Never used by the app (no network, no tests, no docs).
    for name in ('ssl', '_ssl', 'unittest', 'pydoc', 'email', 'http', 'xmlrpc', 'lib2to3', 'distutils', 'test', 'PIL'):
        command += ['--exclude-module', name]
    command.append(str(APP / 'eslifier_app.py'))
    subprocess.run(command, check=True, cwd=str(APP))
    remove_build_tree(work)
    print(OUT / 'E2E/E2E.exe')


if __name__ == '__main__':
    main()
