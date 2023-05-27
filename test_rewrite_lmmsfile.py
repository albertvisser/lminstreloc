import types
import pytest
import rewrite_lmmsfile as testee

def _test_update_root(monkeypatch, capsys):
    pass  # niet nodig als ik niet het vervangen niet via etree doe


def test_get_root(monkeypatch, capsys):
    class MockTree:
        def __init__(self, *args, **kwargs):
            print('called ElementTree() with args', args, kwargs)
        def getroot(self):
            return 'root'
    monkeypatch.setattr(testee.et, 'ElementTree', MockTree)
    assert testee.get_root('test') == 'root'


def test_whereis():
    path = str(testee.sysloc / 'sample.file')
    assert testee.whereis(path) == (True, False)
    path = str(testee.userloc / 'sample.file')
    assert testee.whereis(path) == (False, True)
    assert testee.whereis('/nowhere/sample.file') == (False, False)
    # dit is quick 'n dirty, ervan uitgaande dat deze bestanden op de betreffende locaties staan
    assert testee.whereis('drums/snare01.ogg') == (True, False)
    assert testee.whereis('audio-wav/guitar/Ledguitar2_reconstructed.wav') == (False, True)


def test_find_filenames(monkeypatch, capsys):
    element = testee.et.ElementTree(file='testdata.xml').getroot()
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
                       (['track', 'audiofileprocessor'], '0', 'reconstructed/Ledguitar2.wav')]


def test_update_xml(monkeypatch, capsys):
    def mock_write(*args):
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


def test_copyfile(monkeypatch, capsys, tmp_path):
    def mock_run(*args, **kwargs):
        print('called subprocess.run() with args', args, kwargs)
    def mock_get_root(*args):
        print('called get_root with args', args)
        return 'root'
    def mock_find(*args):
        print('called find_filenames with args', args)
        return [('x', 'file1'), ('y', 'file2'), ('z', 'file1')]
    class MockShow:
        def __init__(self, me, files):
            print('called ShowFiles() with args', me, sorted(files))
            self.me = me
            self.me.filedata = []
        def show_screen(self):
            print('called ShowFiles.show_screen()')
            return 0
    class MockShow2:
        def __init__(self, me, files):
            print('called ShowFiles() with args', me, sorted(files))
            self.me = me
            self.me.filedata = ['filedata']
        def show_screen(self):
            print('called ShowFiles.show_screen()')
            return 0
    def mock_update(*args):
        print('called update_xml() with args', args)
        return True, ''
    def mock_update_message(*args):
        print('called update_xml() with args', args)
        return True, 'Message'
    def mock_update_nochanges(*args):
        print('called update_xml() with args', args)
        return False, ''
    monkeypatch.setattr(testee.subprocess, 'run', mock_run)
    monkeypatch.setattr(testee, 'get_root', mock_get_root)
    monkeypatch.setattr(testee, 'find_filenames', mock_find)

    monkeypatch.setattr(testee.rewrite_gui, 'ShowFiles', MockShow)
    monkeypatch.setattr(testee, 'update_xml', mock_update_message)
    filepath = tmp_path / 'test_testee.mmpz'
    filename = str(filepath)
    filepath2 = filepath.with_suffix('.mmp')
    filepath3 = filepath.with_name(f'{filepath.stem}-2.mmp')
    testee.copyfile(filename)
    assert capsys.readouterr().out == (
            f"called subprocess.run() with args (['lmms', 'dump', {filepath!r}],)"
            f" {{'stdout': <_io.TextIOWrapper name='{filepath2}' mode='w' encoding='UTF-8'>}}\n"
            f"called get_root with args ({filepath2!r},)\n"
            "called find_filenames with args ('root',)\n"
            "called ShowFiles() with args namespace(sysloc=PosixPath('/usr/share/lmms/samples'),"
            f" userloc=PosixPath('/home/albert/lmms/samples'), whereis={testee.whereis})"
            " ['file1', 'file2']\n"
            "called ShowFiles.show_screen()\n"
            'Canceled\n')

    monkeypatch.setattr(testee.rewrite_gui, 'ShowFiles', MockShow2)
    monkeypatch.setattr(testee, 'update_xml', mock_update_message)
    testee.copyfile(filename)
    assert capsys.readouterr().out == (
            f"called subprocess.run() with args (['lmms', 'dump', {filepath!r}],)"
            f" {{'stdout': <_io.TextIOWrapper name='{filepath2}' mode='w' encoding='UTF-8'>}}\n"
            f"called get_root with args ({filepath2!r},)\n"
            "called find_filenames with args ('root',)\n"
            "called ShowFiles() with args namespace(sysloc=PosixPath('/usr/share/lmms/samples'),"
            f" userloc=PosixPath('/home/albert/lmms/samples'), whereis={testee.whereis})"
            " ['file1', 'file2']\n"
            "called ShowFiles.show_screen()\n"
            f"called update_xml() with args (['filedata'], {filepath2!r}, {filepath3!r})\n"
            'Message\n')
    monkeypatch.setattr(testee, 'update_xml', mock_update_nochanges)
    testee.copyfile(filename)
    assert capsys.readouterr().out == (
            f"called subprocess.run() with args (['lmms', 'dump', {filepath!r}],)"
            f" {{'stdout': <_io.TextIOWrapper name='{filepath2}' mode='w' encoding='UTF-8'>}}\n"
            f"called get_root with args ({filepath2!r},)\n"
            "called find_filenames with args ('root',)\n"
            "called ShowFiles() with args namespace(sysloc=PosixPath('/usr/share/lmms/samples'),"
            f" userloc=PosixPath('/home/albert/lmms/samples'), whereis={testee.whereis})"
            " ['file1', 'file2']\n"
            "called ShowFiles.show_screen()\n"
            f"called update_xml() with args (['filedata'], {filepath2!r}, {filepath3!r})\n"
            'No changes\n')
    monkeypatch.setattr(testee, 'update_xml', mock_update)
    testee.copyfile(filename)
    assert capsys.readouterr().out == (
            f"called subprocess.run() with args (['lmms', 'dump', {filepath!r}],)"
            f" {{'stdout': <_io.TextIOWrapper name='{filepath2}' mode='w' encoding='UTF-8'>}}\n"
            f"called get_root with args ({filepath2!r},)\n"
            "called find_filenames with args ('root',)\n"
            "called ShowFiles() with args namespace(sysloc=PosixPath('/usr/share/lmms/samples'),"
            f" userloc=PosixPath('/home/albert/lmms/samples'), whereis={testee.whereis})"
            " ['file1', 'file2']\n"
            "called ShowFiles.show_screen()\n"
            f"called update_xml() with args (['filedata'], {filepath2!r}, {filepath3!r})\n"
            f'{filepath3} written, recompress by loading into lmms and rewrite as mmpz\n')
    monkeypatch.setattr(testee.rewrite_gui, 'ShowFiles', MockShow)
    monkeypatch.setattr(MockShow, 'show_screen', lambda *x: 1)
    monkeypatch.setattr(testee.rewrite_gui, 'ShowFiles', MockShow)
    monkeypatch.setattr(testee, 'update_xml', mock_update)
    testee.copyfile(filename)
    assert capsys.readouterr().out == (
            f"called subprocess.run() with args (['lmms', 'dump', {filepath!r}],)"
            f" {{'stdout': <_io.TextIOWrapper name='{filepath2}' mode='w' encoding='UTF-8'>}}\n"
            f"called get_root with args ({filepath2!r},)\n"
            "called find_filenames with args ('root',)\n"
            "called ShowFiles() with args namespace(sysloc=PosixPath('/usr/share/lmms/samples'),"
            f" userloc=PosixPath('/home/albert/lmms/samples'), whereis={testee.whereis})"
            " ['file1', 'file2']\n"
            'Gui ended with nonzero returncode 1\n')
