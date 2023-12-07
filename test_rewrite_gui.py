import types
import pytest
# import mockqtwidgets as mockqtw
import mockgui.mockqtwidgets as mockqtw
from output_fixture import expected_output
import rewrite_gui as gui

def test_gui_init(monkeypatch, capsys):
    def mock_app_init(self, *args):
        print('called qtw.QApplication.__init__()')
    def mock_init(self, *args):
        print('called qtw.QWidget.__init__()')
    def mock_setup(self, *args):
        print('called ShowFiles.setup_screen()')
    monkeypatch.setattr(gui.qtw.QApplication, '__init__', mock_app_init)
    monkeypatch.setattr(gui.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(gui.ShowFiles, 'setup_screen', mock_setup)
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


def test_setup_screen(monkeypatch, capsys, expected_output):
    """unittest voor setup_screen: ShowFiles aanroepen zonder deze te monkeypatchen
    tevens unittest voor add_file_line die hierin wordt aangeroepen
    (omdat een aparte unittest hiervoor niet lijkt te lukken)
    """
    def mock_app_init(self, *args):
        print('called QApplication.__init__()')
    def mock_init(self, *args):
        print('called QWidget.__init__()')
    def mock_setWindowTitle(self, *args):
        print('called QWidget.setWindowTitle()')
    def mock_setLayout(self, *args):
        print('called QWidget.setLayout()')
    monkeypatch.setattr(gui.qtw.QApplication, '__init__', mock_app_init)
    monkeypatch.setattr(gui.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(gui.qtw.QWidget, 'setWindowTitle', mock_setWindowTitle)
    monkeypatch.setattr(gui.qtw.QWidget, 'setLayout', mock_setLayout)
    monkeypatch.setattr(gui.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
    monkeypatch.setattr(gui.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    monkeypatch.setattr(gui.qtw, 'QLabel', mockqtw.MockLabel)
    monkeypatch.setattr(gui.qtw, 'QGridLayout',  mockqtw.MockGridLayout)
    monkeypatch.setattr(gui.qtw, 'QLineEdit',  mockqtw.MockLineEdit)
    monkeypatch.setattr(gui.qtw, 'QCheckBox',  mockqtw.MockCheckBox)
    monkeypatch.setattr(gui.qtw, 'QPushButton', mockqtw.MockPushButton)
    monkeypatch.setattr(gui.os.path, 'exists', lambda x: True)
    testobj = gui.ShowFiles(types.SimpleNamespace(filedata=[], whereis=lambda *x: (True, True)),
                            ['old_filename'])
    assert len(testobj.file_lines) == 1
    items = testobj.file_lines[0]
    assert isinstance(items[0], gui.qtw.QLineEdit)
    assert isinstance(items[1], gui.qtw.QLineEdit)
    assert isinstance(items[2], gui.qtw.QCheckBox)
    assert isinstance(items[3], gui.qtw.QCheckBox)
    assert isinstance(items[4], gui.qtw.QLineEdit)
    assert isinstance(items[5], gui.qtw.QLineEdit)
    assert isinstance(items[6], gui.qtw.QCheckBox)
    assert isinstance(items[7], gui.qtw.QCheckBox)
    # bindings = {'testobj': testobj}
    assert capsys.readouterr().out == expected_output['showfiles'].format(testobj=testobj)

def test_show_screen(monkeypatch, capsys, expected_output):
    def mock_app_init(self, *args):
        print('called QApplication.__init__()')
    def mock_app_exec(self, *args):
        print('called QApplication.exec()')
        return 'okcode'
    def mock_init(self, *args):
        print('called QWidget.__init__()')
    def mock_addAction(self, *args):
        print('called QWidget.addAction()')
    def mock_show(self, *args):
        print('called QWidget.show()')
    def mock_setup(self, *args):
        print('called ShowFiles.setup_screen()')
    monkeypatch.setattr(gui.qtw.QApplication, '__init__', mock_app_init)
    monkeypatch.setattr(gui.qtw.QApplication, 'exec', mock_app_exec)
    monkeypatch.setattr(gui.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(gui.qtw.QWidget, 'addAction', mock_addAction)
    monkeypatch.setattr(gui.qtw.QWidget, 'show', mock_show)
    monkeypatch.setattr(gui.qgui, 'QAction', mockqtw.MockAction)
    monkeypatch.setattr(gui.ShowFiles, 'setup_screen', mock_setup)
    # me = types.SimpleNamespace(conf={})
    testobj = gui.ShowFiles(types.SimpleNamespace(filedata=[]), [])
    assert testobj.show_screen() == 'okcode'
    assert capsys.readouterr().out == expected_output['showscreen'].format(testobj=testobj)


# werkt zo niet - wel tijdens aanroep van setup_screen testen
def _test_add_file_line(monkeypatch, capsys):
    def mock_app_init(self, *args):
        print('called QApplication.__init__()')
    def mock_init(self, *args):
        print('called QWidget.__init__()')
    def mock_setup(self, *args):
        print('called ShowFiles.setup_screen()')
        self.grid = MockGridLayout()
    monkeypatch.setattr(gui.qtw.QApplication, '__init__', mock_app_init)
    monkeypatch.setattr(gui.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(gui.qtw, 'QGridLayout',  mockqtw.MockGridLayout)
    monkeypatch.setattr(gui.qtw, 'QLineEdit',  mockqtw.MockLineEdit)
    monkeypatch.setattr(gui.qtw, 'QCheckBox',  mockqtw.MockCheckBox)
    monkeypatch.setattr(gui.ShowFiles, 'setup_screen', mock_setup)
    # breakpoint()
    testobj = gui.ShowFiles(types.SimpleNamespace(filedata=[]), [])
    testobj.file_lines = []
    testobj.add_file_lines(testobj.grid, 1, 'old filename')
    assert len(testobj.file_lines) == 1
    items = testobj.file_lines[0]
    assert isinstance(items[0], gui.qtw.QLineEdit)
    assert isinstance(items[1], gui.qtw.QCheckBox)
    assert isinstance(items[2], gui.qtw.QLineEdit)
    assert isinstance(items[3], gui.qtw.QCheckBox)
    assert capsys.readouterr().out == ('called QApplication.__init__()\n'
                                       'called QWidget.__init__()\n'
                                       'called ShowFiles.setup_screen()\n'
                                       'called checkbox.setChecked(False)\n'
                                       )

def test_check(monkeypatch, capsys):
    class MockLineEdit:
        def __init__(self, value):
            self._value = value
        def text(self):
            return self._value
        def setText(self, value):
            self.value = value
    def mock_app_init(self, *args):
        print('called QApplication.__init__()')
    def mock_init(self, *args):
        print('called QWidget.__init__()')
    def mock_setup(self, *args):
        print('called ShowFiles.setup_screen()')
    def mock_set(value):
        print(f'called checkbox.setChecked({value})')
    def mock_whereis(arg):
        print(f'called rewrite_app.whereis with arg `{arg}`')
        return True, False
    monkeypatch.setattr(gui.qtw.QApplication, '__init__', mock_app_init)
    monkeypatch.setattr(gui.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(gui.ShowFiles, 'setup_screen', mock_setup)
    testobj = gui.ShowFiles(types.SimpleNamespace(filedata=[], whereis=mock_whereis), [])
    ns1a = MockLineEdit('path')
    ns1b = MockLineEdit('name')
    ns2a = MockLineEdit('new path')
    ns2b = MockLineEdit('new name')
    ns3a = MockLineEdit('path')
    ns3b = MockLineEdit('name')
    ns4a = MockLineEdit('')
    ns4b = MockLineEdit('')
    ns5 = types.SimpleNamespace(setChecked=mock_set)
    ns6a = MockLineEdit('path')
    ns6b = MockLineEdit('name')
    ns7a = MockLineEdit('')
    ns7b = MockLineEdit('new name')
    ns8a = MockLineEdit('path')
    ns8b = MockLineEdit('name')
    ns9a = MockLineEdit('new path')
    ns9b = MockLineEdit('')
    testobj.file_lines = [(ns1a, ns1b, '', '', ns2a, ns2b, ns5, ns5),
                          (ns3a, ns3b, '', '', ns4a, ns4b, ns5, ns5),
                          (ns6a, ns6b, '', '', ns7a, ns7b, ns5, ns5),
                          (ns8a, ns8b, '', '', ns9a, ns9b, ns5, ns5)]
    testobj.check()
    assert capsys.readouterr().out == ('called QApplication.__init__()\n'
                                       'called QWidget.__init__()\n'
                                       'called ShowFiles.setup_screen()\n'
                                       'called rewrite_app.whereis with arg `new path/new name`\n'
                                       'called checkbox.setChecked(True)\n'
                                       'called checkbox.setChecked(False)\n'
                                       'called rewrite_app.whereis with arg `path/new name`\n'
                                       'called checkbox.setChecked(True)\n'
                                       'called checkbox.setChecked(False)\n'
                                       'called rewrite_app.whereis with arg `new path/name`\n'
                                       'called checkbox.setChecked(True)\n'
                                       'called checkbox.setChecked(False)\n')


def test_confirm(monkeypatch, capsys):
    class MockLineEdit:
        def __init__(self, value):
            self._value = value
        def text(self):
            return self._value
        def setText(self, value):
            self.value = value
    def mock_app_init(self, *args):
        print('called QApplication.__init__()')
    def mock_init(self, *args):
        print('called QWidget.__init__()')
    def mock_setup(self, *args):
        print('called ShowFiles.setup_screen()')
    def mock_close(self):
        print('called ShowFiles.close()')
    monkeypatch.setattr(gui.qtw.QApplication, '__init__', mock_app_init)
    monkeypatch.setattr(gui.qtw.QWidget, '__init__', mock_init)
    monkeypatch.setattr(gui.ShowFiles, 'setup_screen', mock_setup)
    monkeypatch.setattr(gui.ShowFiles, 'close', mock_close)
    testobj = gui.ShowFiles(types.SimpleNamespace(filedata=[]), [])
    ns1 = MockLineEdit('test')
    ns2 = MockLineEdit('new test')
    ns3 = MockLineEdit('more test')
    ns4 = MockLineEdit('')
    testobj.file_lines = [(ns1, ns1, '', '', ns2, ns2), (ns3, ns3, '', '', ns4, ns4),
                          (ns1, ns1, '', '', ns4, ns2), (ns3, ns3, '', '', ns2, ns4)]
    testobj.confirm()
    assert testobj.master.filedata == [('test/test', 'new test/new test'),
                                       ('test/test', 'test/new test'),
                                       ('more test/more test', 'new test/more test')]
    assert capsys.readouterr().out == ('called QApplication.__init__()\n'
                                       'called QWidget.__init__()\n'
                                       'called ShowFiles.setup_screen()\n'
                                       'called ShowFiles.close()\n')
