import types
import pytest
import rewrite_gui

def test_gui_init(monkeypatch, capsys):
    def mock_init(self, *args):
        print('called qtw.QApplication.__init__() with args', args)
    def mock_setup(self, *args):
        print('called ShowFiles.setup_screen()')
    def mock_show(self, *args):
        print('called ShowFiles.show_screen()')
    monkeypatch.setattr(rewrite_gui.qtw.QApplication, '__init__', mock_init)
    monkeypatch.setattr(rewrite_gui.ShowFiles, 'setup_screen', mock_setup)
    monkeypatch.setattr(rewrite_gui.ShowFiles, 'show_screen', mock_show)
    me = types.SimpleNamespace()
    testobj = rewrite_gui.ShowFiles(me, ['file', 'name'])
    assert type(testobj) == rewrite_gui.qtw.QWidget
    assert testobj.parent == me
    assert me.filedata == []
    assert testobj.filenames == ['file', 'name']
    assert hasattr(testobj, 'app')
    assert type(testobj.app) == rewrite_gui.qtw.QApplication
    assert capsys.readouterr().out == (
        'called qtw.QApplication.__init__() with args ()\n'
        'called Gui.setup_screen()\n'
        'called Gui.show_screen()\n')



def _test_setup_screen(monkeypatch, capsys):
    pass

def _test_show_screen(monkeypatch, capsys):
    pass

def _test_add_file_line(monkeypatch, capsys):
    pass

def _confirm(monkeypatch, capsys):
    pass
