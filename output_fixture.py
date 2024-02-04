"""output predictions for ./unittests/test_rewrite_gui.py
"""
import pytest

show_files = """\
called QApplication.__init__()
called QWidget.__init__()
called QWidget.setWindowTitle()
called VBox.__init__
called HBox.__init__
called Label.__init__ with args ('Hieronder worden de namen getoond behorende bij de gebruikte samples en soundfonts.\\nOok wordt aangegeven of de bestanden werkelijk bestaan.\\nZo niet, dan kun je de naam wijzigen naar wat het wel moet zijn (als je het een invult en het ander niet, dan blijft wat je niet invult ongewijzigd).\\nTijdens/na het invullen kun je laten controleren of de nieuwe namen wel bestaan\\nTenslotte kun je het hele proces afbreken of de nieuwe namen laten vervangen in de xml', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Grid.__init__
called Label.__init__ with args ('Old path / filename', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 0)
called Label.__init__ with args ('Sys/Usr', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 1)
called Label.__init__ with args ('New path / filename', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 2)
called Label.__init__ with args ('Sys/Usr', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 3)
called HBox.__init__
called LineEdit.__init__
called LineEdit.insert with arg ``
called LineEdit.setReadOnly with arg `True`
called LineEdit.setMinimumWidth with arg `250`
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'>
called LineEdit.__init__
called LineEdit.insert with arg `old_filename`
called LineEdit.setReadOnly with arg `True`
called LineEdit.setMinimumWidth with arg `50`
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'>
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (1, 0)
called HBox.__init__
called CheckBox.__init__
called CheckBox.setChecked with arg True
called CheckBox.setEnabled with arg False
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called CheckBox.__init__
called CheckBox.setChecked with arg True
called CheckBox.setEnabled with arg False
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (1, 1)
called HBox.__init__
called LineEdit.__init__
called LineEdit.setMinimumWidth with arg `250`
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'>
called LineEdit.__init__
called LineEdit.setMinimumWidth with arg `50`
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'>
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (1, 2)
called HBox.__init__
called CheckBox.__init__
called CheckBox.setEnabled with arg False
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called CheckBox.__init__
called CheckBox.setEnabled with arg False
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (1, 3)
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockGridLayout'>
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Controleren', {testobj}) {{}}
called Signal.connect with args ({testobj.check},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Vervangen', {testobj}) {{}}
called Signal.connect with args ({testobj.confirm},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Afbreken', {testobj}) {{}}
called Signal.connect with args ({testobj.close},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called QWidget.setLayout()
"""
show_screen = """\
called QApplication.__init__()
called QWidget.__init__()
called ShowFiles.setup_screen()
called Action.__init__ with args ('Done', {testobj})
called Signal.connect with args ({testobj.confirm},)
called Action.setShortcut with arg `Ctrl+Enter`
called QWidget.addAction()
called Action.__init__ with args ('Cancel', {testobj})
called Signal.connect with args ({testobj.close},)
called Action.setShortcut with arg `Escape`
called QWidget.addAction()
called QWidget.show()
called QApplication.exec()
"""

@pytest.fixture
def expected_output():
    return {'showfiles': show_files, 'showscreen': show_screen}
