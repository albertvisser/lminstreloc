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
        print('called VBox.__init__()')
    def addWidget(self, *args):
        print('called VBox.addWidget()')
    def addLayout(self, *args):
        print('called VBox.addLayout()')
    def addStretch(self, *args):
        print('called VBox.addStretch()')
    def addSpacing(self, *args):
        print('called VBox.addSpacing()')


class MockHBoxLayout:
    def __init__(self, *args):
        print('called HBox.__init__()')
    def addWidget(self, *args):
        print('called HBox.addWidget()')
    def addLayout(self, *args):
        print('called HBox.addLayout()')
    def addSpacing(self, *args):
        print('called HBox.addSpacing()')
    def addStretch(self, *args):
        print('called HBox.addStretch()')
    def insertStretch(self, *args):
        print('called HBox.insertStretch()')


class MockGridLayout:
    def __init__(self, *args):
        print('called Grid.__init__()')
    def addWidget(self, *args):
        print('called Grid.addWidget()')
    def addLayout(self, *args):
        print('called Grid.addLayout()')
    def addSpacing(self, *args):
        print('called Grid.addSpacing()')
    def addStretch(self, *args):
        print('called Grid.addStretch()')
    def insertStretch(self, *args):
        print('called Grid.insertStretch()')


class MockLabel:
    def __init__(self, *args):
        print('called Label.__init__()')


class MockCheckBox:
    def __init__(self, *args):
        print('called CheckBox.__init__()')
        self.checked = None
        self.textvalue = args[0]
    def setEnabled(self, value):
        print('called CheckBox.setEnabled({})'.format(value))
    def setChecked(self, value):
        print('called CheckBox.setChecked({})'.format(value))
        self.checked = value
    def isChecked(self):
        print('called CheckBox.isChecked()')
        return self.checked
    def text(self):
        return self.textvalue


class MockPushButton:
    def __init__(self, *args):
        print('called PushButton.__init__()')
        self.clicked = MockSignal()


class MockLineEdit:
    def __init__(self, *args):
        print('called LineEdit.__init__()')
        self.textvalue = ''
    def insert(self, text):
        self.textvalue += text
        print(f'called LineEdit.insert(`{text}`)')
    def setReadOnly(self, value):
        print(f'called LineEdit.setReadOnly(`{value}`)')
