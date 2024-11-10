"""uitlijst utilities meegeleverd met rewrite_lmmsfile
"""
import pathlib
# import datetime
import subprocess
# import lxml.etree as et
import xml.etree.ElementTree as et
from rewrite_lmmsfile import sysloc, userloc, find_filenames, whereis

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
            in_sysloc, in_userloc = whereis(name)
            exists = file.exists() or any((in_sysloc, in_userloc))
            if in_sysloc:
                result.append(f'{file}: file {name} exists in {sysloc}')
            elif in_userloc:
                result.append(f'{file}: file {name} exists in {userloc}')
            elif not exists:
                result.append(f'{file}: file {name} does not exist')
            else:
                result.append(f'{file}: file {name} not in standard locations')
    return result


def analyse_file(filename):
    """instrumentnamen uit LMMS module extraheren en ontdubbelen
    """
    # projectfile = pathlib.Path(filename)
    # project_name = projectfile.stem
    if filename.suffix == '.mmpz':
        tmp_file = tmp_root / (filename.stem + '.mmp')
        with tmp_file.open('w') as _out:
            subprocess.run(['lmms', 'dump', filename], check=False, stdout=_out)
    elif filename.suffix == '.mmp':
        tmp_file = filename
    else:
        return {}
    # find locations of filenames in XML
    data = et.ElementTree(file=str(tmp_file))
    return {x[-1] for x in find_filenames(data.getroot())}
