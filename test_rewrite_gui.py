import types
import pytest
# import mockqtwidgets as mockqtw
import mockgui.mockqtwidgets as mockqtw
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
    monkeypatch.setattr(gui.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
    monkeypatch.setattr(gui.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    monkeypatch.setattr(gui.qtw, 'QLabel', mockqtw.MockLabel)
    monkeypatch.setattr(gui.qtw, 'QGridLayout',  mockqtw.MockGridLayout)
    monkeypatch.setattr(gui.qtw, 'QLineEdit',  mockqtw.MockLineEdit)
    monkeypatch.setattr(gui.qtw, 'QCheckBox',  mockqtw.MockCheckBox)
    monkeypatch.setattr(gui.qtw, 'QPushButton', mockqtw.MockPushButton)
    monkeypatch.setattr(gui.os.path, 'exists', lambda x: True)
    # me = types.SimpleNamespace(modbase='modbase')
    # me.conf = configparser.ConfigParser(allow_no_value=True)
    # me.conf.optionxform = str
    # me.conf.read_string( '\n'.join(('[one]', 'first', '', '[two]', '',
    #                                 '[Mod Directories]', 'one: one, eno', 'two: two',
    #                                 'first: first')))
    # breakpoint()
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
                                       'called VBox.__init__\n'
                                       'called HBox.__init__\n'
                                       "called Label.__init__ with args"
                                       " ('Hieronder worden de namen getoond behorende bij de"
                                       " gebruikte samples en soundfonts.\\nOok wordt aangegeven"
                                       " of de bestanden werkelijk bestaan.\\nZo niet, dan kun je"
                                       " de naam wijzigen naar wat het wel moet zijn.\\nTijdens/na"
                                       " het invullen kun je controleren of de nieuwe namen wel"
                                       " bestaan\\nTenslotte kun je het hele proces afbreken of"
                                       f" de nieuwe namen laten vervangen in de xml', {testobj})\n"
                                       "called HBox.addWidget with arg of type"
                                       " <class 'mockgui.mockqtwidgets.MockLabel'>\n"
                                       "called VBox.addLayout with arg of type"
                                       " <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
                                       'called Grid.__init__\n'
                                       "called Label.__init__ with args"
                                       f" ('Old filename', {testobj})\n"
                                       "called Grid.addWidget with arg of type"
                                       " <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 0)\n"
                                       f"called Label.__init__ with args ('Sys/Usr', {testobj})\n"
                                       "called Grid.addWidget with arg of type"
                                       " <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 1)\n"
                                       "called Label.__init__ with args"
                                       f" ('New filename', {testobj})\n"
                                       "called Grid.addWidget with arg of type"
                                       " <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 2)\n"
                                       f"called Label.__init__ with args ('Sys/Usr', {testobj})\n"
                                       "called Grid.addWidget with arg of type"
                                       " <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 3)\n"
                                       'called LineEdit.__init__\n'
                                       'called LineEdit.insert with arg `old_filename`\n'
                                       'called LineEdit.setReadOnly with arg `True`\n'
                                       "called Grid.addWidget with arg of type"
                                       " <class 'mockgui.mockqtwidgets.MockLineEdit'> at (1, 0)\n"
                                       'called HBox.__init__\n'
                                       'called CheckBox.__init__\n'
                                       'called CheckBox.setChecked with arg True\n'
                                       'called CheckBox.setEnabled with arg False\n'
                                       'called HBox.addWidget with arg of type'
                                       " <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
                                       'called CheckBox.__init__\n'
                                       'called CheckBox.setChecked with arg True\n'
                                       'called CheckBox.setEnabled with arg False\n'
                                       'called HBox.addWidget with arg of type'
                                       " <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
                                       'called Grid.addLayout with arg of type'
                                       " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (1, 1)\n"
                                       'called LineEdit.__init__\n'
                                       "called Grid.addWidget with arg of type"
                                       " <class 'mockgui.mockqtwidgets.MockLineEdit'> at (1, 2)\n"
                                       'called HBox.__init__\n'
                                       'called CheckBox.__init__\n'
                                       'called CheckBox.setEnabled with arg False\n'
                                       'called HBox.addWidget with arg of type'
                                       " <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
                                       'called CheckBox.__init__\n'
                                       'called CheckBox.setEnabled with arg False\n'
                                       'called HBox.addWidget with arg of type'
                                       " <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
                                       "called Grid.addLayout with arg of type"
                                       " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (1, 3)\n"
                                       "called VBox.addLayout with arg of type"
                                       " <class 'mockgui.mockqtwidgets.MockGridLayout'>\n"
                                       'called HBox.__init__\n'
                                       'called HBox.addStretch\n'
                                       "called PushButton.__init__ with args"
                                       f" {'&Controleren', testobj}\n"
                                       f"called Signal.connect with args ({testobj.check},)\n"
                                       'called HBox.addWidget with arg of type'
                                       " <class 'mockgui.mockqtwidgets.MockPushButton'>\n"
                                       'called PushButton.__init__ with args'
                                       f" {'&Vervangen', testobj}\n"
                                       f'called Signal.connect with args ({testobj.confirm},)\n'
                                       'called HBox.addWidget with arg of type'
                                       " <class 'mockgui.mockqtwidgets.MockPushButton'>\n"
                                       'called PushButton.__init__ with args '
                                       f"{'&Afbreken', testobj}\n"
                                       f"called Signal.connect with args ({testobj.close},)\n"
                                       'called HBox.addWidget with arg of type'
                                       " <class 'mockgui.mockqtwidgets.MockPushButton'>\n"
                                       'called HBox.addStretch\n'
                                       "called VBox.addLayout with arg of type"
                                       " <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
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
    monkeypatch.setattr(gui.qgui, 'QAction', mockqtw.MockAction)
    monkeypatch.setattr(gui.ShowFiles, 'setup_screen', mock_setup)
    # me = types.SimpleNamespace(conf={})
    testobj = gui.ShowFiles(types.SimpleNamespace(filedata=[]), [])
    assert testobj.show_screen() == 'okcode'
    assert capsys.readouterr().out == ('called QApplication.__init__()\n'
                                       'called QWidget.__init__()\n'
                                       'called ShowFiles.setup_screen()\n'
                                       f"called Action.__init__ with args ('Done', {testobj})\n"
                                       f'called Signal.connect with args ({testobj.confirm},)\n'
                                       'called Action.setShortcut with arg `Ctrl+Enter`\n'
                                       'called QWidget.addAction()\n'
                                       f"called Action.__init__ with args ('Cancel', {testobj})\n"
                                       f'called Signal.connect with args ({testobj.close},)\n'
                                       'called Action.setShortcut with arg `Escape`\n'
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

