"""GUI for rewrite_lmmsfile: a tool to correct filenames for instruments in LMMS modules
"""
import sys
import os
# import types
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qgui
# import PyQt6.QtCore as qcore


class ShowFiles(qtw.QWidget):
    """Show the filenames and whether they exist on the filesystem si that the right ones ca be
    entered
    """
    def __init__(self, master, filenames):
        "setup the gui"
        self.master = master
        self.master.filedata = []  # used to return data to the caller
        self.filenames = filenames
        self.app = qtw.QApplication(sys.argv)
        super().__init__()
        self.setup_screen()

    def setup_screen(self):
        """define the screen elements
        """
        self.setWindowTitle('Select Filenames to alter')
        # self.setWindowIcon()
        vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel(
            'Hieronder worden de namen getoond behorende bij de gebruikte samples en soundfonts.\n'
            'Ook wordt aangegeven of de bestanden werkelijk bestaan.\n'
            'Zo niet, dan kun je de naam wijzigen naar wat het wel moet zijn '
            '(als je het een invult en het ander niet, dan blijft wat je niet invult ongewijzigd).\n'
            'Tijdens/na het invullen kun je laten controleren of de nieuwe namen wel bestaan\n'
            'Tenslotte kun je het hele proces afbreken of de nieuwe namen laten vervangen'
            ' in de xml', self))
        vbox.addLayout(hbox)
        self.file_lines = []
        # self.column_widths = (100, 20, 100)
        gbox = qtw.QGridLayout()
        line = 0
        gbox.addWidget(qtw.QLabel('Old path / filename', self), line, 0)
        gbox.addWidget(qtw.QLabel('Sys/Usr', self), line, 1)
        gbox.addWidget(qtw.QLabel('New path / filename', self), line, 2)
        gbox.addWidget(qtw.QLabel('Sys/Usr', self), line, 3)
        for name in self.filenames:
            line += 1
            self.add_file_line(gbox, line, name)
        vbox.addLayout(gbox)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        btn = qtw.QPushButton('&Controleren', self)
        btn.clicked.connect(self.check)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('&Vervangen', self)
        btn.clicked.connect(self.confirm)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('&Afbreken', self)
        btn.clicked.connect(self.close)
        hbox.addWidget(btn)
        hbox.addStretch()
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def show_screen(self):
        """finish the gui setup; show it and start the event loop
        """
        do = qgui.QAction('Done', self)
        do.triggered.connect(self.confirm)
        do.setShortcut('Ctrl+Enter')
        self.addAction(do)
        dont = qgui.QAction('Cancel', self)
        dont.triggered.connect(self.close)
        dont.setShortcut('Escape')
        self.addAction(dont)
        self.show()
        return self.app.exec()  # niet via sys.exit() want we zijn nog niet klaar

    def add_file_line(self, layout, lineno, old_filename):
        """add a line with widgets to display file information
        """
        line = []
        path, name = os.path.split(old_filename)
        layout2 = qtw.QHBoxLayout()
        widget = qtw.QLineEdit(self)
        widget.insert(path)
        widget.setReadOnly(True)
        widget.setMinimumWidth(250)
        layout2.addWidget(widget)
        line.append(widget)
        widget = qtw.QLineEdit(self)
        widget.insert(name)
        widget.setReadOnly(True)
        widget.setMinimumWidth(50)
        layout2.addWidget(widget)
        line.append(widget)
        layout.addLayout(layout2, lineno, 0)
        layout2 = qtw.QHBoxLayout()
        widget = qtw.QCheckBox('', self)
        in_sysloc, in_userloc = self.master.whereis(old_filename)
        widget.setChecked(in_sysloc)
        widget.setEnabled(False)  # ReadOnly(True)
        line.append(widget)
        layout2.addWidget(widget)
        widget = qtw.QCheckBox('', self)
        widget.setChecked(in_userloc)
        widget.setEnabled(False)  # ReadOnly(True)
        line.append(widget)
        layout2.addWidget(widget)
        layout.addLayout(layout2, lineno, 1)
        layout2 = qtw.QHBoxLayout()
        widget = qtw.QLineEdit(self)
        widget.setMinimumWidth(250)
        layout2.addWidget(widget)
        line.append(widget)
        widget = qtw.QLineEdit(self)
        widget.setMinimumWidth(50)
        layout2.addWidget(widget)
        line.append(widget)
        layout.addLayout(layout2, lineno, 2)
        layout2 = qtw.QHBoxLayout()
        widget = qtw.QCheckBox('', self)
        widget.setEnabled(False)  # ReadOnly(True)
        line.append(widget)
        layout2.addWidget(widget)
        widget = qtw.QCheckBox('', self)
        widget.setEnabled(False)  # ReadOnly(True)
        line.append(widget)
        layout2.addWidget(widget)
        layout.addLayout(layout2, lineno, 3)
        self.file_lines.append(line)

    def check(self):
        """check for existence of newly added filenames
        """
        for line in self.file_lines:
            oldpath, oldname = line[0].text(), line[1].text()
            newpath, newname = line[4].text(), line[5].text()
            if newpath and not newname:
                newname = oldname
                line[5].setText(newname)
            if newname and not newpath:
                newpath = oldpath
                line[4].setText(newpath)
            new_filename = os.path.join(newpath, newname)
            if new_filename:
                in_sysloc, in_userloc = self.master.whereis(new_filename)
                line[6].setChecked(in_sysloc)
                line[7].setChecked(in_userloc)

    def confirm(self):
        """pass the changed data back to the caller
        """
        for line in self.file_lines:
            oldpath, oldname = line[0].text(), line[1].text()
            newpath, newname = line[4].text(), line[5].text()
            if newpath and not newname:
                newname = oldname
            if newname and not newpath:
                newpath = oldpath
            old_filename = os.path.join(oldpath, oldname)
            new_filename = os.path.join(newpath, newname)
            if new_filename:
                self.master.filedata.append((old_filename, new_filename))
        self.close()
