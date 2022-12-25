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
        hbox.addWidget(qtw.QLabel('\n'.join((
            'Hieronder worden de namen getoond behorende bij de gebruikte samples en soundfonts.',
            'Ook wordt aangegeven of de bestanden werkelijk bestaan.',
            'Zo niet, dan kun je de naam wijzigen naar wat het wel moet zijn.',
            'Tijdens/na het invullen kun je controleren of de nieuwe namen wel bestaan',
            'Tenslotte kun je het hele proces afbreken of de nieuwe namen laten vervangen'
            ' in de xml')), self))
        vbox.addLayout(hbox)
        self.file_lines = []
        # self.column_widths = (100, 20, 100)
        gbox = qtw.QGridLayout()
        line = 0
        gbox.addWidget(qtw.QLabel('Old filename', self), line, 0)
        gbox.addWidget(qtw.QLabel('Exists', self), line, 1)
        gbox.addWidget(qtw.QLabel('New filename', self), line, 2)
        gbox.addWidget(qtw.QLabel('Exists', self), line, 3)
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
        btn = qtw.QPushButton('&Klaar', self)
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
        widget = qtw.QLineEdit(self)
        widget.insert(old_filename)
        widget.setReadOnly(True)
        layout.addWidget(widget, lineno, 0)
        line.append(widget)
        widget = qtw.QCheckBox('', self)
        widget.setChecked(os.path.exists(old_filename))
        widget.setEnabled(False)  # ReadOnly(True)
        line.append(widget)
        layout.addWidget(widget, lineno, 1)
        widget = qtw.QLineEdit(self)
        line.append(widget)
        layout.addWidget(widget, lineno, 2)
        widget = qtw.QCheckBox('', self)
        self.file_lines.append(line)
        widget.setEnabled(False)  # ReadOnly(True)
        line.append(widget)
        layout.addWidget(widget, lineno, 3)

    def check(self):
        """check for existence of newly added filenames
        """
        for line in self.file_lines:
            new_filename = line[2].text()
            if new_filename:
                line[3].setChecked(os.path.exists(new_filename))

    def confirm(self):
        """pass the changed data back to the caller
        """
        for line in self.file_lines:
            old_filename = line[0].text()
            new_filename = line[2].text()
            if new_filename:
                self.master.filedata.append((old_filename, new_filename))
        self.close()
