import types
import pytest
import rewrite_gui as gui

def test_gui_init(monkeypatch, capsys):
    def mock_app_init(self, *args):
        print('called qtw.QApplication.__init__()')
    def mock_init(self, *args):
        print('called qtw.QWidget.__init__()')
    def mock_setup(self, *args):
        print('called ShowFiles.setup_screen()')
    # def mock_show(self, *args):
    #     print('called ShowFiles.show_screen()')
    monkeypatch.setattr(gui.qtw.QApplication, '__init__', mock_app_init)
    monkeypatch.setattr(gui.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(gui.ShowFiles, 'setup_screen', mock_setup)
    # monkeypatch.setattr(gui.ShowFiles, 'show_screen', mock_show)
    me = types.SimpleNamespace()
    testobj = gui.ShowFiles(me, ['file', 'name'])
    assert isinstance(testobj, gui.qtw.QWidget)
    assert testobj.master == me
    assert me.filedata == []
    assert testobj.filenames == ['file', 'name']
    assert hasattr(testobj, 'app')
    assert isinstance(testobj.app, gui.qtw.QApplication)
    assert capsys.readouterr().out == ('called qtw.QApplication.__init__()\n'
                                       'called qtw.QWidget.__init__()\n'
                                       'called ShowFiles.setup_screen()\n')
    # 'called ShowFiles.show_screen()\n')



def _test_setup_screen(monkeypatch, capsys):
    pass

def _test_show_screen(monkeypatch, capsys):
    pass

def _test_add_file_line(monkeypatch, capsys):
    pass

def _confirm(monkeypatch, capsys):
    pass
