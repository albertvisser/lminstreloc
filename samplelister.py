"""uitlijst utilities meegeleverd met rewrite_lmmsfile
"""
import pathlib
# import datetime
import subprocess
# import lxml.etree as et
import xml.etree.ElementTree as et
from rewrite_lmmsfile import find_filenames

sysloc = pathlib.Path('/usr/share/lmms/samples')
userloc = pathlib.Path('~/lmms/samples').expanduser()
tmp_root = pathlib.Path('/tmp/smplister')
tmp_root.mkdir(exist_ok=True)


def list_samples(path):
    """list files in sample directories gesorteerd op naam
    om te vergelijken en duplicaten te verwijderen
    """
    path = pathlib.Path(path)
    results = []
    for file in path.iterdir():
        if file.is_dir():
            results.extend(list_samples(file))
            continue
        strpath = str(path.resolve())
        results.append((file.name, strpath, file.stat().st_size, file.stat().st_mtime))
    return sorted(results)


def list_files(path):
    """uitlijsten instrument filenamen in alle LMMS modules
    """
    path = pathlib.Path(path)
    result = []
    for file in path.iterdir():
        if file.name.startswith('.'):
            continue
        if file.is_dir():
            result.extend(list_files(file))
            continue
        if file.suffix not in ('.mmp', '.mmpz'):
            continue
        instrument_files = analyse_file(file)
        for name in instrument_files:
            in_sysloc, in_userloc = check_for_locations(name)
            if in_sysloc:
                result.append(f'{file}: file {name} exists in {sysloc}')
            elif in_userloc:
                result.append(f'{file}: file {name} exists in {userloc}')
            else:
                result.append(f'{file}: file {name} not found')
    return result


def analyse_file(filename):
    """instrumentnamen uit LMMS module extraheren en ontdubbelen
    """
    # projectfile = pathlib.Path(filename)
    # project_name = projectfile.stem
    if filename.suffix == '.mmpz':
        tmp_file = tmp_root / (filename.stem + '.mmp')
        with tmp_file.open('w') as _out:
            subprocess.run(['lmms', 'dump', filename], stdout=_out)
    elif filename.suffix == '.mmp':
        tmp_file = filename
    # find locations of filenames in XML
    data = et.ElementTree(file=str(tmp_file))
    return {x[-1] for x in find_filenames(data.getroot())}


def check_for_locations(filename):
    """teruggeven op welke locaties een filenaam voorkomt
    """
    if filename.startswith('/'):
        path = pathlib.Path(filename)
        try:
            in_sysloc = path.relative_to(sysloc) == pathlib.Path(path.name)
        except ValueError:
            in_sysloc = False
        try:
            in_userloc = path.relative_to(userloc) == pathlib.Path(path.name)
        except ValueError:
            in_userloc = False
    else:
        in_sysloc = (sysloc / filename).exists()
        in_userloc = (userloc / filename).exists()
    return in_sysloc, in_userloc
