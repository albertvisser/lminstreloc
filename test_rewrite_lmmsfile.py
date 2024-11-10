"""unittests for ./rewrite_lmmsfile.py
"""
import pytest
import rewrite_lmmsfile as testee


whereis_absolute = """\
called path.exists for `/sample.file`
called path.is_relative_to for `/sample.file` and `{testee.sysloc}`
called path.is_relative_to for `/sample.file` and `{testee.userloc}`
"""
whereis_relative = """\
called path.exists for `{testee.sysloc}/sample.file`
called path.exists for `{testee.userloc}/sample.file`
"""
copyfile_min = ("called subprocess.run() with args (['lmms', 'dump', {filepath!r}],)"
                " {{'check': False, 'stdout': <_io.TextIOWrapper name='{filepath2}' mode='w'"
                " encoding='UTF-8'>}}\n"
                "called get_root with args ({filepath2!r},)\n"
                "called find_filenames with args ('root',)\n"
                "called ShowFiles() with args namespace(sysloc=PosixPath('/usr/share/lmms/samples'),"
                " userloc=PosixPath('/home/albert/lmms/samples'), whereis={testee.whereis})"
                " ['file1', 'file2']\n")
copyfile_show = "called ShowFiles.show_screen()\n"
copyfile_upd = "called update_xml() with args (['filedata'], {filepath2!r}, {filepath3!r})\n"
copyfile_rew = ("called subprocess.run() with args (['lmms', 'upgrade', {filepath3!r},"
                " {filepath4!r}],) {{'check': False}}\n")

@pytest.fixture
def expected_output():
    """output predictions
    """
    return {'whereis_absolute': whereis_absolute, 'whereis_relative': whereis_relative,
            'copyfile_minimal': copyfile_min + copyfile_show,
            'copyfile_update_xml': copyfile_min + copyfile_show + copyfile_upd,
            'copyfile_rewrite': copyfile_min + copyfile_show + copyfile_upd + copyfile_rew,
            'copyfile_error': copyfile_min}


def test_get_root(monkeypatch):
    """unittest for rewrite_lmmsfile.get_root
    """
    class MockTree:
        """stub
        """
        def __init__(self, *args, **kwargs):
            print('called ElementTree() with args', args, kwargs)
        def getroot(self):
            """stub
            """
            return 'root'
    monkeypatch.setattr(testee.et, 'ElementTree', MockTree)
    assert testee.get_root('test') == 'root'


def test_whereis(monkeypatch, capsys, expected_output):
    """unittest for rewrite_lmmsfile.whereis
    """
    counter = 0
    def mock_exists_no(path):
        """stub
        """
        print(f'called path.exists for `{path}`')
        return False
    def mock_exists_yes(path):
        """stub
        """
        print(f'called path.exists for `{path}`')
        return True
    def mock_exists_yes_then_no(path):
        """stub
        """
        nonlocal counter
        print(f'called path.exists for `{path}`')
        counter += 1
        if counter == 1:
            return True
        return False
    def mock_exists_no_then_yes(path):
        """stub
        """
        nonlocal counter
        print(f'called path.exists for `{path}`')
        counter += 1
        if counter == 1:
            return False
        return True
    def mock_is_relative_no_then_yes(path, loc):
        """stub
        """
        nonlocal counter
        print(f'called path.is_relative_to for `{path}` and `{loc}`')
        counter += 1
        if counter == 1:
            return False
        return True
    def mock_is_relative_yes_then_no(path, loc):
        """stub
        """
        nonlocal counter
        print(f'called path.is_relative_to for `{path}` and `{loc}`')
        counter += 1
        if counter == 1:
            return True
        return False
    def mock_is_relative_exc(path, loc):
        """stub
        """
        print(f'called path.is_relative_to for `{path}` and `{loc}`')
        raise ValueError
    monkeypatch.setattr(testee.pathlib.Path, 'exists', mock_exists_no)
    monkeypatch.setattr(testee.pathlib.Path, 'is_relative_to', mock_is_relative_no_then_yes)
    assert testee.whereis('/sample.file') == (False, False)
    assert capsys.readouterr().out == 'called path.exists for `/sample.file`\n'
    monkeypatch.setattr(testee.pathlib.Path, 'exists', mock_exists_yes)
    counter = 0
    assert testee.whereis('/sample.file') == (False, True)
    assert capsys.readouterr().out == expected_output['whereis_absolute'].format(testee=testee)
    monkeypatch.setattr(testee.pathlib.Path, 'is_relative_to', mock_is_relative_yes_then_no)
    counter = 0
    assert testee.whereis('/sample.file') == (True, False)
    assert capsys.readouterr().out == expected_output['whereis_absolute'].format(testee=testee)
    monkeypatch.setattr(testee.pathlib.Path, 'is_relative_to', mock_is_relative_exc)
    counter = 0
    assert testee.whereis('/sample.file') == (False, False)
    assert capsys.readouterr().out == expected_output['whereis_absolute'].format(testee=testee)
    counter = 0
    monkeypatch.setattr(testee.pathlib.Path, 'exists', mock_exists_yes_then_no)
    assert testee.whereis('sample.file') == (True, False)
    assert capsys.readouterr().out == expected_output['whereis_relative'].format(testee=testee)
    counter = 0
    monkeypatch.setattr(testee.pathlib.Path, 'exists', mock_exists_no_then_yes)
    assert testee.whereis('sample.file') == (False, True)
    assert capsys.readouterr().out == expected_output['whereis_relative'].format(testee=testee)


def test_find_filenames():
    """unittest for rewrite_lmmsfile.find_filenames
    """
    element = testee.et.ElementTree(file='data/testdata.xml').getroot()
    data = testee.find_filenames(element)
    newdata = []
    for track, tracktype, name in data:
        newtrack = [element.tag for element in track]
        newdata.append((newtrack, tracktype, name))
    assert newdata == [(['track', 'sf2player'], '0', '/home/albert/lmms/soundfonts/FluidR3_GM.sf2'),
                       (['track', 'sf2player'], '0', '/usr/share/sounds/sf2/FluidR3_GM.sf2'),
                       (['track', 'audiofileprocessor'], '1', 'drums/crash01.ogg'),
                       (['track', 'audiofileprocessor'], '1', 'drums/ride01.ogg'),
                       (['track', 'audiofileprocessor'], '0', 'reconstructed/flickbass.wav'),
                       (['track', 'audiofileprocessor'], '0', 'reconstructed/flickbass.wav'),
                       (['track', 'audiofileprocessor'], '0', 'reconstructed/Ledguitar2.wav'),
                       (['track', 'audiofileprocessor'], '0', 'reconstructed/Ledguitar2.wav'),
                       (['track', 'audiofileprocessor'], '1', 'drums/crash01.ogg')]


def test_update_xml(monkeypatch, capsys):
    """unittest for rewrite_lmmsfile.update_xml
    """
    def mock_write(*args):
        """stub
        """
        print('called path.write_text() with args', args)
    monkeypatch.setattr(testee.pathlib.Path, 'read_text', lambda *x: '')
    monkeypatch.setattr(testee.pathlib.Path, 'write_text', mock_write)
    monkeypatch.setattr(testee.pathlib.Path, 'exists', lambda *x: False)
    assert testee.update_xml([], testee.pathlib.Path('project_copy'),
                           testee.pathlib.Path('project_rewrite')) == (False, '')
    assert capsys.readouterr().out == ''
    assert testee.update_xml([('gargl', 'bargl'), ('oingo', 'boingo')],
                           testee.pathlib.Path('project_copy'),
                           testee.pathlib.Path('project_rewrite')) == (False,
                                   "new name bargl not used, file doesn't exist\n"
                                   "new name boingo not used, file doesn't exist")
    assert capsys.readouterr().out == ''
    monkeypatch.setattr(testee.pathlib.Path, 'read_text', lambda *x: 'gargl bargl oingo boingo')
    monkeypatch.setattr(testee.pathlib.Path, 'exists', lambda *x: True)
    assert testee.update_xml([('gargl', 'bargl'), ('oingo', 'boingo')],
                           testee.pathlib.Path('project_copy'),
                           testee.pathlib.Path('project_rewrite')) == (True, '')
    assert capsys.readouterr().out == ("called path.write_text() with args"
                                       " (PosixPath('project_rewrite'),"
                                       " 'bargl bargl boingo bboingo')\n")


def test_copyfile(monkeypatch, capsys, tmp_path, expected_output):
    """unittest for rewrite_lmmsfile.copyfile
    """
    def mock_run(*args, **kwargs):
        """stub
        """
        print('called subprocess.run() with args', args, kwargs)
    def mock_get_root(*args):
        """stub
        """
        print('called get_root with args', args)
        return 'root'
    def mock_find(*args):
        """stub
        """
        print('called find_filenames with args', args)
        return [('x', 'file1'), ('y', 'file2'), ('z', 'file1')]
    class MockShow:
        """stub
        """
        def __init__(self, me, files):
            print('called ShowFiles() with args', me, sorted(files))
            self.me = me
            self.me.filedata = []
        def show_screen(self):
            """stub
            """
            print('called ShowFiles.show_screen()')
            return 0
    class MockShow2:
        """stub
        """
        def __init__(self, me, files):
            print('called ShowFiles() with args', me, sorted(files))
            self.me = me
            self.me.filedata = ['filedata']
        def show_screen(self):
            """stub
            """
            print('called ShowFiles.show_screen()')
            return 0
    def mock_update(*args):
        """stub
        """
        print('called update_xml() with args', args)
        return True, ''
    def mock_update_message(*args):
        """stub
        """
        print('called update_xml() with args', args)
        return True, 'Message'
    def mock_update_nochanges(*args):
        """stub
        """
        print('called update_xml() with args', args)
        return False, ''
    monkeypatch.setattr(testee.subprocess, 'run', mock_run)
    monkeypatch.setattr(testee, 'get_root', mock_get_root)
    monkeypatch.setattr(testee, 'find_filenames', mock_find)
    monkeypatch.setattr(testee, 'temploc', tmp_path)
    monkeypatch.setattr(testee.rewrite_gui, 'ShowFiles', MockShow)
    monkeypatch.setattr(testee, 'update_xml', mock_update_message)
    filepath = tmp_path / 'test_testee.mmpz'
    filename = str(filepath)
    filepath2 = filepath.with_suffix('.mmp')
    filepath3 = filepath.with_name(f'{filepath.stem}-relocated.mmp')
    filepath4 = filepath3.with_suffix('.mmpz')
    assert testee.copyfile(filename) == 'Canceled'
    bindings = {'filepath': filepath, 'filepath2': filepath2, 'testee': testee}
    assert capsys.readouterr().out == expected_output['copyfile_minimal'].format(**bindings)

    monkeypatch.setattr(testee.rewrite_gui, 'ShowFiles', MockShow2)
    monkeypatch.setattr(testee, 'update_xml', mock_update_message)
    assert testee.copyfile(filename) == 'Message'
    bindings = {'filepath': filepath, 'filepath2': filepath2, 'filepath3': filepath3,
                'testee': testee}
    assert capsys.readouterr().out == expected_output['copyfile_update_xml'].format(**bindings)
    monkeypatch.setattr(testee, 'update_xml', mock_update_nochanges)
    assert testee.copyfile(filename) == 'No changes'
    bindings = {'filepath': filepath, 'filepath2': filepath2, 'filepath3': filepath3,
                'testee': testee}
    assert capsys.readouterr().out == expected_output['copyfile_update_xml'].format(**bindings)
            # klopt dit wel? moet hij de xml wel updaten als er niks veranderd is?
    monkeypatch.setattr(testee, 'update_xml', mock_update)
    assert testee.copyfile(filename) == f"{filename} converted and saved as {filepath4}"
    bindings = {'filepath': filepath, 'filepath2': filepath2, 'filepath3': filepath3,
                'filepath4': filepath4, 'testee': testee}
    assert capsys.readouterr().out == expected_output['copyfile_rewrite'].format(**bindings)
    monkeypatch.setattr(testee.rewrite_gui, 'ShowFiles', MockShow)
    monkeypatch.setattr(MockShow, 'show_screen', lambda *x: 1)
    monkeypatch.setattr(testee.rewrite_gui, 'ShowFiles', MockShow)
    monkeypatch.setattr(testee, 'update_xml', mock_update)
    assert testee.copyfile(filename) == 'Gui ended with nonzero returncode 1'
    bindings = {'filepath': filepath, 'filepath2': filepath2, 'testee': testee}
    assert capsys.readouterr().out == expected_output['copyfile_error'].format(**bindings)
