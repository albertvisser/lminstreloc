"""rewrite_lmmsfile: a tool to correct filenames for instruments in LMMS modules
"""
import pathlib
import types
import subprocess
# import lxml.etree as et
import xml.etree.ElementTree as et
import rewrite_gui

instr_root = {'audiofileprocessor': pathlib.Path('~/lmms/samples').expanduser(),
              'sf2player': pathlib.Path('~/lmms/soundfonts').expanduser()}
# er zijn meerdere paden per type instrument mogelijk: /usr/share/sounds o.i.d. is ook mogelijk
# een relatief pad kan ook in /usr/share/lmms/samples zitten of in /usr/share/soundfonts
# deze laatste is waar ik pacman/pamac de soundfonts heeft laten terechtkomen dus het zou kunnen
# zijn dat lmms die niet kent
# als ik ze sleep vanuit de linkerbalk krijg ik relatieve locaties, als ik ze selecteer in de
# "instrumentblokjes" krijg ik absolute (volledige) paden
# ik kan dus beter de paden zoals ze zijn onthouden en uitproberen welke kloppen


def copyfile(filename):
    """main function: analyse lmms module, present filenames and write back with changes
    """
    projectfile = pathlib.Path(filename)
    project_name = projectfile.stem
    project_copy = projectfile.with_suffix('.mmp')
    project_rewrite = project_copy.with_stem(project_name + '-2')
    # uncompress save file
    with project_copy.open('w') as _out:
        subprocess.run(['lmms', 'dump', projectfile], stdout=_out)
    # find locations of filenames in XML
    files = find_filenames(get_root(project_copy))
    # present filenames and ask for changes
    check_files = set(x[-1] for x in files)
    me = types.SimpleNamespace()
    gui = rewrite_gui.ShowFiles(me, check_files)
    value = gui.show_screen()
    if value:
        print(f"gui ended with nonzero returncode {value}")
        return
    # write back changes
    changes, err = update_xml(me.filedata, project_copy, project_rewrite)
    if err:
        print(err)
    elif changes:
        print(f'{project_rewrite} written, recompress by loading into lmms and rewrite as mmpz')
    else:
        print('Done.')


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
        if pathlib.Path(newfile).exists():
            for path in instr_root.values():
                first_part = str(path)
                # print(first_part)
                if oldfile.startswith(first_part):
                    oldfile = oldfile.replace(first_part, '')[1:]
                    changes = True
                if newfile.startswith(first_part):
                    newfile = newfile.replace(first_part, '')[1:]
                    changes = True
            # print(oldfile, newfile)
            data = data.replace(oldfile, newfile)
            changes = True
        else:
            mld.append(f"new name {newfile} not used, file doesn't exist")
    if changes and not mld:
        project_rewrite.write_text(data)
    return '\n'.join(mld)


def get_root(project_copy):
    "get the root of the xml file"
    data = et.ElementTree(file=str(project_copy))
    return data.getroot()


def update_root(element, filename_data):
    "update changes in the root (only needed if we do this using etree (which we don't)"
