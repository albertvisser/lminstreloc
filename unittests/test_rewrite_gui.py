"""unittests for ./app/rewrite_gui.py
"""
import types
import mockgui.mockqtwidgets as mockqtw
from output_fixture import expected_output
from app import rewrite_gui as testee


class TestShowFiles:
    """unittest for rewrite_gui.ShowFiles
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for rewrite_gui.ShowFiles object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ShowFiles.__init__ with args', args)
        monkeypatch.setattr(testee.ShowFiles, '__init__', mock_init)
        testobj = testee.ShowFiles()
        assert capsys.readouterr().out == 'called ShowFiles.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for ShowFiles.__init__
        """
        def mock_app_init(self, *args):
            """stub
            """
            print('called qtw.QApplication.__init__()')
        def mock_init(self, *args):
            """stub
            """
            print('called qtw.QWidget.__init__()')
        def mock_setup(self, *args):
            """stub
            """
            print('called ShowFiles.setup_screen()')
        monkeypatch.setattr(testee.qtw.QApplication, '__init__', mock_app_init)
        monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
        monkeypatch.setattr(testee.ShowFiles, 'setup_screen', mock_setup)
        testobj = testee.ShowFiles('master')
        assert isinstance(testobj, testee.qtw.QWidget)
        assert testobj.master == 'master'
        assert testobj.filename == ''
        assert isinstance(testobj.app, testee.qtw.QApplication)
        assert capsys.readouterr().out == ('called qtw.QApplication.__init__()\n'
                                           'called qtw.QWidget.__init__()\n'
                                           'called ShowFiles.setup_screen()\n')

    def test_setup_screen(self, monkeypatch, capsys, expected_output):
        """unittest for ShowFiles.setup_screen
        """
        def mock_setWindowTitle(*args):
            print('called QWidget.setWindowTitle()')
        def mock_setLayout(*args):
            print('called QWidget.setLayout()')
        def mock_add(self, *args):
            print('called ShowFiles.add_file_line with args', args)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.os.path, 'exists', lambda x: True)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.setWindowTitle = mock_setWindowTitle
        testobj.setLayout = mock_setLayout
        testobj.add_file_line = mock_add
        testobj.setup_screen()
        assert testobj.file_lines == []
        # assert isinstance(testobj.file_lines[0][0], gui.qtw.QLineEdit)
        # assert isinstance(testobj.file_lines[0][1], gui.qtw.QLineEdit)
        # assert isinstance(testobj.file_lines[0][2], gui.qtw.QCheckBox)
        # assert isinstance(testobj.file_lines[0][3], gui.qtw.QCheckBox)
        # assert isinstance(testobj.file_lines[0][4], gui.qtw.QLineEdit)
        # assert isinstance(testobj.file_lines[0][5], gui.qtw.QLineEdit)
        # assert isinstance(testobj.file_lines[0][6], gui.qtw.QCheckBox)
        # assert isinstance(testobj.file_lines[0][7], gui.qtw.QCheckBox)
        # bindings = {'testobj': testobj}
        assert capsys.readouterr().out == expected_output['showfiles'].format(testobj=testobj)

    def test_show_screen(self, monkeypatch, capsys, expected_output):
        """unittest for ShowFiles.show_screen
        """
        def mock_addAction(*args):
            print('called Widget.addAction')
        def mock_show(*args):
            print('called Widget.show')
        def mock_exec():
            print('called Application.exec')
            return 'okcode'
        # monkeypatch.setattr(testee.ShowFiles, 'setup_screen', mock_setup)
        monkeypatch.setattr(testee.qgui, 'QAction', mockqtw.MockAction)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.addAction = mock_addAction
        testobj.show = mock_show
        testobj.app = types.SimpleNamespace(exec=mock_exec)
        assert testobj.show_screen() == 'okcode'
        assert capsys.readouterr().out == expected_output['showscreen'].format(testobj=testobj)

    def test_select(self, monkeypatch, capsys):
        """unittest for ShowFiles.select
        """
        def mock_get_open(*args, **kwargs):
            print('called FileDialog.getOpenFileName with args', args, kwargs)
            return 'qqq', True
        def mock_process(name):
            print(f"called Rewriter.process with arg '{name}'")
            return ['aaa', 'bbb']
        def mock_add(*args):
            print("called ShowFiles.add_file_line with args", args)
        def mock_remove(num):
            print(f"called ShowFiles.remove_file_line with arg {num}")
        def mock_count():
            print('called GridLayout.count')
            return 2
        monkeypatch.setattr(testee.qtw, 'QFileDialog', mockqtw.MockFileDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.filename = ''
        testobj.remove_file_line = mock_remove
        testobj.add_file_line = mock_add
        testobj.master = types.SimpleNamespace(process=mock_process, rootloc='xxxxxx')
        testobj.gbox = mockqtw.MockGridLayout()
        testobj.gbox.rowCount = mock_count
        testobj.modulename = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called Grid.__init__\ncalled LineEdit.__init__\n"
        testobj.select()
        assert not testobj.filename
        assert capsys.readouterr().out == (
                f"called FileDialog.getOpenFileName with args {testobj} ()"
                " {'caption': 'Select a module', 'directory': 'xxxxxx',"
                " 'filter': 'LMMS files (*.mmp, *.mmpz)'}\n")
        monkeypatch.setattr(mockqtw.MockFileDialog, 'getOpenFileName', mock_get_open)
        testobj.filename = 'yyyy/zzz'
        testobj.select()
        assert testobj.filename == 'qqq'
        assert capsys.readouterr().out == (
                f"called FileDialog.getOpenFileName with args ({testobj},)"
                " {'caption': 'Select a module', 'directory': 'yyyy',"
                " 'filter': 'LMMS files (*.mmp, *.mmpz)'}\n"
                "called LineEdit.setText with arg `qqq`\n"
                "called Rewriter.process with arg 'qqq'\n"
                "called GridLayout.count\n"
                "called ShowFiles.remove_file_line with arg 2\n"
                "called ShowFiles.remove_file_line with arg 1\n"
                f"called ShowFiles.add_file_line with args ({testobj.gbox}, 1, 'aaa')\n"
                f"called ShowFiles.add_file_line with args ({testobj.gbox}, 2, 'bbb')\n")

    def test_add_file_line(self, monkeypatch, capsys, expected_output):
        """unittest for ShowFiles.add_file_line
        """
        def mock_whereis(arg):
            print(f'called Rewriter.whereis with arg {arg}')
            return True, True
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(whereis=mock_whereis)
        testobj.grid = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == 'called Grid.__init__\n'
        testobj.file_lines = []
        # bij deze aanroep volgt `super-class __init__ of type ShowFiles was never called`
        testobj.add_file_line(testobj.grid, 1, 'old/filename')
        assert len(testobj.file_lines) == 1
        items = testobj.file_lines[0]
        assert isinstance(items[0], testee.qtw.QLineEdit)
        assert isinstance(items[1], testee.qtw.QLineEdit)
        assert isinstance(items[2], testee.qtw.QCheckBox)
        assert isinstance(items[3], testee.qtw.QCheckBox)
        assert isinstance(items[4], testee.qtw.QLineEdit)
        assert isinstance(items[5], testee.qtw.QLineEdit)
        assert isinstance(items[6], testee.qtw.QCheckBox)
        assert isinstance(items[7], testee.qtw.QCheckBox)
        assert capsys.readouterr().out == expected_output['addfileline'].format(testobj=testobj,
                                                                                path='old',
                                                                                name='filename',
                                                                                checkvalue='True')
        testobj.add_file_line(testobj.grid, 1, '')
        assert len(testobj.file_lines) == 2
        items = testobj.file_lines[1]
        assert isinstance(items[0], testee.qtw.QLineEdit)
        assert isinstance(items[1], testee.qtw.QLineEdit)
        assert isinstance(items[2], testee.qtw.QCheckBox)
        assert isinstance(items[3], testee.qtw.QCheckBox)
        assert isinstance(items[4], testee.qtw.QLineEdit)
        assert isinstance(items[5], testee.qtw.QLineEdit)
        assert isinstance(items[6], testee.qtw.QCheckBox)
        assert isinstance(items[7], testee.qtw.QCheckBox)
        assert capsys.readouterr().out == expected_output['addfileline2'].format(testobj=testobj,
                                                                                 path='', name='',
                                                                                 checkvalue='False')

    def test_remove_file_line(self, monkeypatch, capsys):
        """unittest for ShowFiles.remove_file_line
        """
        def mock_itematpos(self, *args):
            print("called GridLayout.itemAtPosition with args", args)
            return None
        def mock_itematpos_2(self, *args):
            print("called GridLayout.itemAtPosition with args", args)
            return mock_hbox
        def mock_colcount(self):
            print("called GridLayout.columnCount")
            return 2
        def mock_count(self):
            print("called HBoxLayout.count")
            return 2
        def mock_takeat(self, pos):
            print(f"called HBoxLayout.takeAt with arg {pos}")
            return types.SimpleNamespace(widget=mock_widget)  # QWidgetItem
        def mock_takeat_2(self, pos):
            print(f"called HBoxLayout.takeAt with arg {pos}")
            return types.SimpleNamespace(widget=mock_widget_2)  # QWidgetItem
        def mock_widget():
            print('called WidgetItem.widget')
            return None
        def mock_widget_2():
            print('called WidgetItem.widget')
            return mock_check
        monkeypatch.setattr(mockqtw.MockGridLayout, 'itemAtPosition', mock_itematpos)
        monkeypatch.setattr(mockqtw.MockGridLayout, 'columnCount', mock_colcount)
        monkeypatch.setattr(mockqtw.MockHBoxLayout, 'count', mock_count)
        monkeypatch.setattr(mockqtw.MockHBoxLayout, 'takeAt', mock_takeat)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gbox = mockqtw.MockGridLayout()
        mock_hbox = mockqtw.MockHBoxLayout()
        mock_check = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == ("called Grid.__init__\n"
                                           "called HBox.__init__\n"
                                           "called CheckBox.__init__\n")
        testobj.remove_file_line(1)
        assert capsys.readouterr().out == ("called GridLayout.columnCount\n"
                                           "called GridLayout.itemAtPosition with args (1, 0)\n"
                                           "called GridLayout.itemAtPosition with args (1, 1)\n")
        monkeypatch.setattr(mockqtw.MockGridLayout, 'itemAtPosition', mock_itematpos_2)
        testobj.remove_file_line(1)
        assert capsys.readouterr().out == ("called GridLayout.columnCount\n"
                                           "called GridLayout.itemAtPosition with args (1, 0)\n"
                                           "called GridLayout.itemAtPosition with args (1, 1)\n"
                                           "called HBoxLayout.count\n"
                                           "called HBoxLayout.takeAt with arg 1\n"
                                           "called WidgetItem.widget\n"
                                           "called HBoxLayout.takeAt with arg 0\n"
                                           "called WidgetItem.widget\n"
                                           f"called Grid.removeItem with args ({mock_hbox},)\n"
                                           "called HBoxLayout.count\n"
                                           "called HBoxLayout.takeAt with arg 1\n"
                                           "called WidgetItem.widget\n"
                                           "called HBoxLayout.takeAt with arg 0\n"
                                           "called WidgetItem.widget\n"
                                           f"called Grid.removeItem with args ({mock_hbox},)\n")
        monkeypatch.setattr(mockqtw.MockHBoxLayout, 'takeAt', mock_takeat_2)
        testobj.remove_file_line(1)
        assert capsys.readouterr().out == ("called GridLayout.columnCount\n"
                                           "called GridLayout.itemAtPosition with args (1, 0)\n"
                                           "called GridLayout.itemAtPosition with args (1, 1)\n"
                                           "called HBoxLayout.count\n"
                                           "called HBoxLayout.takeAt with arg 1\n"
                                           "called WidgetItem.widget\n"
                                           "called CheckBox.close\n"
                                           "called HBoxLayout.takeAt with arg 0\n"
                                           "called WidgetItem.widget\n"
                                           "called CheckBox.close\n"
                                           f"called Grid.removeItem with args ({mock_hbox},)\n"
                                           "called HBoxLayout.count\n"
                                           "called HBoxLayout.takeAt with arg 1\n"
                                           "called WidgetItem.widget\n"
                                           "called CheckBox.close\n"
                                           "called HBoxLayout.takeAt with arg 0\n"
                                           "called WidgetItem.widget\n"
                                           "called CheckBox.close\n"
                                           f"called Grid.removeItem with args ({mock_hbox},)\n")

    def test_check(self, monkeypatch, capsys):
        """unittest for ShowFiles.check
        """
        def mock_whereis(arg):
            """stub
            """
            print(f'called rewrite_app.whereis with arg `{arg}`')
            return True, False
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(whereis=mock_whereis)
        ns1a = mockqtw.MockLineEdit('path')
        ns1b = mockqtw.MockLineEdit('name')
        ns2a = mockqtw.MockLineEdit('new path')
        ns2b = mockqtw.MockLineEdit('new name')
        ns3a = mockqtw.MockLineEdit('path')
        ns3b = mockqtw.MockLineEdit('name')
        ns4a = mockqtw.MockLineEdit('')
        ns4b = mockqtw.MockLineEdit('')
        ns5 = mockqtw.MockCheckBox()  # types.SimpleNamespace(setChecked=mock_set)
        ns6a = mockqtw.MockLineEdit('path')
        ns6b = mockqtw.MockLineEdit('name')
        ns7a = mockqtw.MockLineEdit('')
        ns7b = mockqtw.MockLineEdit('new name')
        ns8a = mockqtw.MockLineEdit('path')
        ns8b = mockqtw.MockLineEdit('name')
        ns9a = mockqtw.MockLineEdit('new path')
        ns9b = mockqtw.MockLineEdit('')
        assert capsys.readouterr().out == ("called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called CheckBox.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\n")
        testobj.file_lines = [(ns1a, ns1b, '', '', ns2a, ns2b, ns5, ns5),
                              (ns3a, ns3b, '', '', ns4a, ns4b, ns5, ns5),
                              (ns6a, ns6b, '', '', ns7a, ns7b, ns5, ns5),
                              (ns8a, ns8b, '', '', ns9a, ns9b, ns5, ns5)]
        testobj.check()
        assert capsys.readouterr().out == ("called LineEdit.text\ncalled LineEdit.text\n"
                                           "called LineEdit.text\ncalled LineEdit.text\n"
                                           'called rewrite_app.whereis with arg `new path/new name`\n'
                                           'called CheckBox.setChecked with arg True\n'
                                           'called CheckBox.setChecked with arg False\n'
                                           "called LineEdit.text\ncalled LineEdit.text\n"
                                           "called LineEdit.text\ncalled LineEdit.text\n"
                                           "called LineEdit.text\ncalled LineEdit.text\n"
                                           "called LineEdit.text\ncalled LineEdit.text\n"
                                           'called LineEdit.setText with arg `path`\n'
                                           'called rewrite_app.whereis with arg `path/new name`\n'
                                           'called CheckBox.setChecked with arg True\n'
                                           'called CheckBox.setChecked with arg False\n'
                                           "called LineEdit.text\ncalled LineEdit.text\n"
                                           "called LineEdit.text\ncalled LineEdit.text\n"
                                           'called LineEdit.setText with arg `name`\n'
                                           'called rewrite_app.whereis with arg `new path/name`\n'
                                           'called CheckBox.setChecked with arg True\n'
                                           'called CheckBox.setChecked with arg False\n')

    def test_confirm(self, monkeypatch, capsys):
        """unittest for ShowFiles.confirm
        """
        def mock_update(*args):
            """stub
            """
            print('called ShowFiles.update_file with args', args)
            return 'done'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(update_file=mock_update)
        testobj.message = mockqtw.MockLabel()
        testobj.filename = 'xxx'
        ns1 = mockqtw.MockLineEdit('test')
        ns2 = mockqtw.MockLineEdit('new test')
        ns3 = mockqtw.MockLineEdit('more test')
        ns4 = mockqtw.MockLineEdit('')
        assert capsys.readouterr().out == ("called Label.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\n")
        testobj.file_lines = [(ns1, ns1, '', '', ns2, ns2), (ns3, ns3, '', '', ns4, ns4),
                              (ns1, ns1, '', '', ns4, ns2), (ns3, ns3, '', '', ns2, ns4)]
        testobj.confirm()
        assert capsys.readouterr().out == ("called LineEdit.text\ncalled LineEdit.text\n"
                                           "called LineEdit.text\ncalled LineEdit.text\n"
                                           "called LineEdit.text\ncalled LineEdit.text\n"
                                           "called LineEdit.text\ncalled LineEdit.text\n"
                                           "called LineEdit.text\ncalled LineEdit.text\n"
                                           "called LineEdit.text\ncalled LineEdit.text\n"
                                           "called LineEdit.text\ncalled LineEdit.text\n"
                                           "called LineEdit.text\ncalled LineEdit.text\n"
                                           "called ShowFiles.update_file with args"
                                           " ('xxx', [('test/test', 'new test/new test'),"
                                           " ('test/test', 'test/new test'),"
                                           " ('more test/more test', 'new test/more test')])\n"
                                           "called Label.setText with arg `done`\n")
