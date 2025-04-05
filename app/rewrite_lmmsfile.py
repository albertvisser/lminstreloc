"""rewrite_lmmsfile: a tool to correct filenames for instruments in LMMS modules
"""
import pathlib
import subprocess
# import lxml.etree as et
import xml.etree.ElementTree as et
from . import rewrite_gui

instr_root = {'audiofileprocessor': pathlib.Path('~/lmms/samples').expanduser(),
              'sf2player': pathlib.Path('~/lmms/soundfonts').expanduser()}
sysloc = pathlib.Path('/usr/share/lmms/samples')
userloc = pathlib.Path('~/lmms/samples').expanduser()
# er zijn meerdere paden per type instrument mogelijk: /usr/share/sounds o.i.d. is ook mogelijk
# een relatief pad kan ook in /usr/share/lmms/samples zitten of in /usr/share/soundfonts
# deze laatste is waar ik pacman/pamac de soundfonts heeft laten terechtkomen dus het zou kunnen
# zijn dat lmms die niet kent
# als ik ze in LMMS sleep vanuit de linkerbalk krijg ik relatieve locaties, als ik ze selecteer in de
# "instrumentblokjes" krijg ik absolute (volledige) paden
# ik kan dus beter de paden zoals ze zijn onthouden en uitproberen welke kloppen
temploc = pathlib.Path('/tmp/lminstreloc')


def whereis(filename):
    """bepalen op welke locaties een filenaam voorkomt

    geeft twee indicatoren terug: `staat op de systeemlocatie` en `staat op de userlocatie`
    """
    if filename.startswith('/'):
        path = pathlib.Path(filename)
        if path.exists():
            try:
                in_sysloc = path.is_relative_to(sysloc)
            except ValueError:
                in_sysloc = False
            try:
                in_userloc = path.is_relative_to(userloc)
            except ValueError:
                in_userloc = False
        else:
            in_sysloc = in_userloc = False
    else:
        in_sysloc = (sysloc / filename).exists()
        in_userloc = (userloc / filename).exists()
    return in_sysloc, in_userloc


class Rewriter:
    """entry point

    main function: analyse lmms module, present filenames and write back with changes
    """
    whereis = staticmethod(whereis)

    def __init__(self, rootloc):
        self.rootloc = rootloc
        self.sysloc = sysloc
        self.userloc = userloc
        gui = rewrite_gui.ShowFiles(self)
        gui.show_screen()

    def process(self, filename):
        """read filenames from the chosen file and return them to the caller
        """
        projectfile = pathlib.Path(filename)
        # project_copy = projectfile.with_suffix('.mmp')
        temploc.mkdir(exist_ok=True)
        project_copy = (temploc / projectfile.name).with_suffix('.mmp')
        # project_rewrite = project_copy.with_stem(project_name + '-2')
        # uncompress save file
        with project_copy.open('w') as _out:
            subprocess.run(['lmms', 'dump', projectfile], check=False, stdout=_out)
        # find locations of filenames in XML
        files = find_filenames(get_root(project_copy))
        # present filenames and ask for changes
        check_files = set(x[-1] for x in files)
        return check_files

    def update_file(self, filename, filedata):
        """(try to) write the changes back and return a message about the result
        """
        projectfile = pathlib.Path(filename)
        projloc = projectfile.parent
        project_name = projectfile.stem
        project_copy = (temploc / projectfile.name).with_suffix('.mmp')
        project_rewrite = project_copy.with_stem(project_name + '-relocated')
        changes, err = update_xml(filedata, project_copy, project_rewrite)
        if err:
            return err
        if changes:
            # print(f'{project_rewrite} written, recompress by loading into lmms and rewrite as mmpz')
            rewrite_compressed = (projloc / project_rewrite.stem).with_suffix('.mmpz')
            subprocess.run(['lmms', 'upgrade', project_rewrite, rewrite_compressed], check=False)
            return f'{filename} converted and saved as {rewrite_compressed}'
        return 'No changes'


def find_filenames(element):
    """search for instrument filenames in the given XML

    returns the locations (search paths, as 2-tuples) and the filenames themselves
    """
    result = []
    tracks = element.findall('./song/trackcontainer/track')
    for item in tracks:
        if item.get('type') == '0':
            instruments = item.findall('instrumenttrack/instrument')
            for instrument in instruments:
                if instrument[0].tag in ('audiofileprocessor', 'sf2player'):
                    # filename = str(instr_root[instrument[0].tag] / instrument[0].get('src'))
                    # result.append(((item, instrument[0]), '0', filename))
                    result.append(((item, instrument[0]), '0', instrument[0].get('src')))
        elif item.get('type') == '1':
            instruments = item.findall('bbtrack/trackcontainer/track/instrumenttrack/instrument')
            for instrument in instruments:
                if instrument[0].tag in ('audiofileprocessor', 'sf2player'):
                    # filename = str(instr_root[instrument[0].tag] / instrument[0].get('src'))
                    # result.append(((item, instrument[0]), '1', filename))
                    result.append(((item, instrument[0]), '1', instrument[0].get('src')))
    return result


def update_xml(dialog_data, project_copy, project_rewrite):
    """modify the filenames that need to be changed at the given locations in the XML
    """
    # gewoon maar met een text replace van alle gevonden en gewijzigde strings?
    # in dat geval moet ik het niet op de onderstaande manier terugschrijven
    # newroot = update_root(get_root(project_copy), dialog_data)  # apply changes to xml
    # newdata = et.ElementTree(newroot).write(str(project_rewrite))
    # maar met
    data = project_copy.read_text()
    changes = False
    mld = []
    for oldfile, newfile in dialog_data:
        ok = pathlib.Path(newfile).exists()
        if not ok:
            in_sysloc, in_userloc = whereis(newfile)
            ok = any((in_sysloc, in_userloc))
        # print(oldfile, newfile, ok)
        if ok:
            data = data.replace(oldfile, newfile)
            changes = True
        else:
            mld.append(f"new name {newfile} not used, file doesn't exist")
    if changes and not mld:
        project_rewrite.write_text(data)
    return changes, '\n'.join(mld)


def get_root(project_copy):
    "get the root of the xml file"
    data = et.ElementTree(file=str(project_copy))
    return data.getroot()
