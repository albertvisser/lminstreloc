import types
import pytest
import rewrite_lmmsfile as rwrt

def _test_update_root(monkeypatch, capsys):
    pass  # niet nodig als ik niet het vervangen niet via etree doe


def test_get_root(monkeypatch, capsys):
    class MockTree:
        def __init__(self, *args, **kwargs):
            print('called ElementTree() with args', args, kwargs)
        def getroot(self):
            return 'root'
    monkeypatch.setattr(rwrt.et, 'ElementTree', MockTree)
    assert rwrt.get_root('test') == 'root'


def test_find_filenames(monkeypatch, capsys):
    element = rwrt.et.ElementTree(file='testdata.xml').getroot()
    data = rwrt.find_filenames(element)
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
    monkeypatch.setattr(rwrt.pathlib.Path, 'read_text', lambda *x: '')
    monkeypatch.setattr(rwrt.pathlib.Path, 'write_text', mock_write)
    monkeypatch.setattr(rwrt.pathlib.Path, 'exists', lambda *x: False)
    assert rwrt.update_xml([], rwrt.pathlib.Path('project_copy'),
                           rwrt.pathlib.Path('project_rewrite')) == ''
    assert capsys.readouterr().out == ''
    assert rwrt.update_xml([('gargl', 'bargl'), ('oingo', 'boingo')],
                           rwrt.pathlib.Path('project_copy'),
                           rwrt.pathlib.Path('project_rewrite')) == (
                                   "new name bargl not used, file doesn't exist\n"
                                   "new name boingo not used, file doesn't exist")
    assert capsys.readouterr().out == ''
    monkeypatch.setattr(rwrt.pathlib.Path, 'read_text', lambda *x: 'gargl bargl oingo boingo')
    monkeypatch.setattr(rwrt.pathlib.Path, 'exists', lambda *x: True)
    assert rwrt.update_xml([('gargl', 'bargl'), ('oingo', 'boingo')],
                           rwrt.pathlib.Path('project_copy'),
                           rwrt.pathlib.Path('project_rewrite')) == ''
    assert capsys.readouterr().out == ("called path.write_text() with args"
                                       " (PosixPath('project_rewrite'),"
                                       " 'bargl bargl boingo bboingo')\n")


def _test_copyfile(monkeypatch, capsys):
    assert capsys.readouterr().out == ('project_rewrite written,'
                                       ' recompress by loading into lmms and rewrite as mmpz')
