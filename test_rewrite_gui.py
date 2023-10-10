import types
import pytest
import rewrite_gui as gui


class MockSignal:
    def __init__(self, *args):
        print('called signal.__init__()')
    def connect(self, *args):
        print('called signal.connect()')


class MockAction:
    triggered = MockSignal()
    def __init__(self, text, func):
        print('called action.__init__()')
        self.label = text
        self.callback = func
        self.shortcuts = []
        self.checkable = self.checked = False
        self.statustip = ''
    def setCheckable(self, state):
        self.checkable = state
    def setChecked(self, state):
        self.checked = state
    def setShortcut(self, data):
        print('call action.setShortcut with arg `{}`'.format(data))
    def setShortcuts(self, data):
        self.shortcuts = data
    def setStatusTip(self, data):
        self.statustip = data


class MockVBoxLayout:
    def __init__(self, *args):
        print('called MockVBoxLayout.__init__()')
    def addWidget(self, *args):
        print('called vbox.addWidget()')
    def addLayout(self, *args):
        print('called vbox.addLayout()')
    def addStretch(self, *args):
        print('called vbox.addStretch()')
    def addSpacing(self, *args):
        print('called vbox.addSpacing()')


class MockHBoxLayout:
    def __init__(self, *args):
        print('called MockHBoxLayout.__init__()')
    def addWidget(self, *args):
        print('called hbox.addWidget()')
    def addLayout(self, *args):
        print('called hbox.addLayout()')
    def addSpacing(self, *args):
        print('called hbox.addSpacing()')
    def addStretch(self, *args):
        print('called hbox.addStretch()')
    def insertStretch(self, *args):
        print('called hbox.insertStretch()')


class MockGridLayout:
    def __init__(self, *args):
        print('called MockGridLayout.__init__()')
    def addWidget(self, *args):
        print('called grid.addWidget()')
    def addLayout(self, *args):
        print('called grid.addLayout()')
    def addSpacing(self, *args):
        print('called grid.addSpacing()')
    def addStretch(self, *args):
        print('called grid.addStretch()')
    def insertStretch(self, *args):
        print('called grid.insertStretch()')


class MockLabel:
    def __init__(self, *args):
        print('called MockLabel.__init__()')


class MockCheckBox:
    def __init__(self, *args):
        print('called MockCheckBox.__init__()')
        self.checked = None
        self.textvalue = args[0]
    def setEnabled(self, value):
        print('called check.setEnabled({})'.format(value))
    def setChecked(self, value):
        print('called check.setChecked({})'.format(value))
        self.checked = value
    def isChecked(self):
        print('called check.isChecked()')
        return self.checked
    def text(self):
        return self.textvalue


class MockPushButton:
    def __init__(self, *args):
        print('called MockPushButton.__init__()')
        self.clicked = MockSignal()


class MockLineEdit:
    def __init__(self, *args):
        print('called MockLineEdit.__init__()')
        self.textvalue = ''
    def insert(self, text):
        self.textvalue += text
        print(f'called edit.insert(`{text}`)')
    def setReadOnly(self, value):
        print(f'called edit.setReadOnly(`{value}`)')


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


def test_setup_screen(monkeypatch, capsys):
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
    monkeypatch.setattr(gui.qtw, 'QVBoxLayout', MockVBoxLayout)
    monkeypatch.setattr(gui.qtw, 'QHBoxLayout', MockHBoxLayout)
    monkeypatch.setattr(gui.qtw, 'QLabel', MockLabel)
    monkeypatch.setattr(gui.qtw, 'QGridLayout',  MockGridLayout)
    monkeypatch.setattr(gui.qtw, 'QLineEdit',  MockLineEdit)
    monkeypatch.setattr(gui.qtw, 'QCheckBox',  MockCheckBox)
    monkeypatch.setattr(gui.qtw, 'QPushButton', MockPushButton)
    monkeypatch.setattr(gui.os.path, 'exists', lambda x: True)
    # me = types.SimpleNamespace(modbase='modbase')
    # me.conf = configparser.ConfigParser(allow_no_value=True)
    # me.conf.optionxform = str
    # me.conf.read_string( '\n'.join(('[one]', 'first', '', '[two]', '',
    #                                 '[Mod Directories]', 'one: one, eno', 'two: two',
    #                                 'first: first')))
    testobj = gui.ShowFiles(types.SimpleNamespace(filedata=[], whereis=lambda *x: (True, True)),
                            ['old_filename'])
    assert len(testobj.file_lines) == 1
    items = testobj.file_lines[0]
    assert isinstance(items[0], gui.qtw.QLineEdit)
    assert isinstance(items[1], gui.qtw.QCheckBox)
    assert isinstance(items[2], gui.qtw.QCheckBox)
    assert isinstance(items[3], gui.qtw.QLineEdit)
    assert isinstance(items[4], gui.qtw.QCheckBox)
    assert isinstance(items[5], gui.qtw.QCheckBox)
    assert capsys.readouterr().out == ('called QApplication.__init__()\n'
                                       'called QWidget.__init__()\n'
                                       'called QWidget.setWindowTitle()\n'
                                       'called MockVBoxLayout.__init__()\n'
                                       'called MockHBoxLayout.__init__()\n'
                                       'called MockLabel.__init__()\n'
                                       'called hbox.addWidget()\n'
                                       'called vbox.addLayout()\n'
                                       'called MockGridLayout.__init__()\n'
                                       'called MockLabel.__init__()\n'
                                       'called grid.addWidget()\n'
                                       'called MockLabel.__init__()\n'
                                       'called grid.addWidget()\n'
                                       'called MockLabel.__init__()\n'
                                       'called grid.addWidget()\n'
                                       'called MockLabel.__init__()\n'
                                       'called grid.addWidget()\n'
                                       'called MockLineEdit.__init__()\n'
                                       'called edit.insert(`old_filename`)\n'
                                       'called edit.setReadOnly(`True`)\n'
                                       'called grid.addWidget()\n'
                                       'called MockHBoxLayout.__init__()\n'
                                       'called MockCheckBox.__init__()\n'
                                       f'called check.setChecked(True)\n'
                                       'called check.setEnabled(False)\n'
                                       'called hbox.addWidget()\n'
                                       'called MockCheckBox.__init__()\n'
                                       f'called check.setChecked(True)\n'
                                       'called check.setEnabled(False)\n'
                                       'called hbox.addWidget()\n'
                                       'called grid.addLayout()\n'
                                       'called MockLineEdit.__init__()\n'
                                       'called grid.addWidget()\n'
                                       'called MockHBoxLayout.__init__()\n'
                                       'called MockCheckBox.__init__()\n'
                                       'called check.setEnabled(False)\n'
                                       'called hbox.addWidget()\n'
                                       'called MockCheckBox.__init__()\n'
                                       'called check.setEnabled(False)\n'
                                       'called hbox.addWidget()\n'
                                       'called grid.addLayout()\n'
                                       'called vbox.addLayout()\n'
                                       'called MockHBoxLayout.__init__()\n'
                                       'called hbox.addStretch()\n'
                                       'called MockPushButton.__init__()\n'
                                       'called signal.__init__()\n'
                                       'called signal.connect()\n'
                                       'called hbox.addWidget()\n'
                                       'called MockPushButton.__init__()\n'
                                       'called signal.__init__()\n'
                                       'called signal.connect()\n'
                                       'called hbox.addWidget()\n'
                                       'called MockPushButton.__init__()\n'
                                       'called signal.__init__()\n'
                                       'called signal.connect()\n'
                                       'called hbox.addWidget()\n'
                                       'called hbox.addStretch()\n'
                                       'called vbox.addLayout()\n'
                                       'called QWidget.setLayout()\n')


def test_show_screen(monkeypatch, capsys):
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
    monkeypatch.setattr(gui.qgui, 'QAction', MockAction)
    monkeypatch.setattr(gui.ShowFiles, 'setup_screen', mock_setup)
    # me = types.SimpleNamespace(conf={})
    testobj = gui.ShowFiles(types.SimpleNamespace(filedata=[]), [])
    assert testobj.show_screen() == 'okcode'
    assert capsys.readouterr().out == ('called QApplication.__init__()\n'
                                       'called QWidget.__init__()\n'
                                       'called ShowFiles.setup_screen()\n'
                                       'called action.__init__()\n'
                                       'called signal.connect()\n'
                                       'call action.setShortcut with arg `Ctrl+Enter`\n'
                                       'called QWidget.addAction()\n'
                                       'called action.__init__()\n'
                                       'called signal.connect()\n'
                                       'call action.setShortcut with arg `Escape`\n'
                                       'called QWidget.addAction()\n'
                                       'called QWidget.show()\n'
                                       'called QApplication.exec()\n')


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
    monkeypatch.setattr(gui.qtw, 'QGridLayout',  MockGridLayout)
    monkeypatch.setattr(gui.qtw, 'QLineEdit',  MockLineEdit)
    monkeypatch.setattr(gui.qtw, 'QCheckBox',  MockCheckBox)
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
    ns1 = types.SimpleNamespace(text=lambda *x: 'test')
    ns2 = types.SimpleNamespace(text=lambda *x: 'new test')
    ns3 = types.SimpleNamespace(text=lambda *x: 'more test')
    ns4 = types.SimpleNamespace(text=lambda *x: '')
    ns5 = types.SimpleNamespace(setChecked=mock_set)
    testobj.file_lines = [(ns1, '', '', ns2, ns5, ns5), (ns3, '', '', ns4, ns5, ns5)]
    # monkeypatch.setattr(gui.os.path, 'exists', lambda *x: False)
    testobj.check()
    assert capsys.readouterr().out == ('called QApplication.__init__()\n'
                                       'called QWidget.__init__()\n'
                                       'called ShowFiles.setup_screen()\n'
                                       'called rewrite_app.whereis with arg `new test`\n'
                                       'called checkbox.setChecked(True)\n'
                                       'called checkbox.setChecked(False)\n')
    # monkeypatch.setattr(gui.os.path, 'exists', lambda *x: True)
    # testobj.check()
    # assert capsys.readouterr().out == 'called checkbox.setChecked(True)\n'


def test_confirm(monkeypatch, capsys):
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
    ns1 = types.SimpleNamespace(text=lambda *x: 'test')
    ns2 = types.SimpleNamespace(text=lambda *x: 'new test')
    ns3 = types.SimpleNamespace(text=lambda *x: 'more test')
    ns4 = types.SimpleNamespace(text=lambda *x: '')
    testobj.file_lines = [(ns1, '', '', ns2), (ns3, '', '', ns4)]
    testobj.confirm()
    assert testobj.master.filedata == [('test', 'new test')]
    assert capsys.readouterr().out == ('called QApplication.__init__()\n'
                                       'called QWidget.__init__()\n'
                                       'called ShowFiles.setup_screen()\n'
                                       'called ShowFiles.close()\n')

