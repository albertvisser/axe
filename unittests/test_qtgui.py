"""unittests for ./axe/gui_qt.py
"""
import types
import pytest
from mockgui import mockqtwidgets as mockqtw
from axe import gui_qt as testee

eldialog_start = """\
called Dialog.__init__ with args {testobj.parent} () {{}}
called Dialog.setWindowTitle with args ('{title}',)
called Dialog.setWindowIcon with args ('appicon',)
called Label.__init__ with args ('element name:  ', {testobj})
called LineEdit.__init__
called CheckBox.__init__
called ComboBox.__init__
called ComboBox.setEditable with arg `False`
called ComboBox.addItems with arg `-- none --`
called ComboBox.addItems with arg {{'ns1': 'namespace1', 'ns2': 'namespace'}}
called CheckBox.__init__
called CheckBox.setCheckable with arg False
called Editor.__init__ with args ({testobj},)
called Editor.setTabChangesFocus with arg True
called PushButton.__init__ with args ('&Save', {testobj}) {{}}
called Signal.connect with args ({testobj.accept},)
called PushButton.setDefault with arg `True`
called PushButton.__init__ with args ('&Cancel', {testobj}) {{}}
called Signal.connect with args ({testobj.reject},)
"""
eldialog_middle_1 = """\
called CheckBox.toggle
called CheckBox.toggle
"""
eldialog_middle_2 = """\
called ComboBox.setCurrentIndex with arg `2`
"""
eldialog_end = """\
called LineEdit.setText with arg `{tag}`
called Editor.setText with arg `{text}`
called VBox.__init__
called HBox.__init__
called Grid.__init__
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 0)
called HBox.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'>
called HBox.addStretch
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (0, 1)
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'> at ()
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockComboBox'> at ()
called HBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockGridLayout'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called VBox.__init__
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockEditorWidget'>
called HBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called HBox.addStretch
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
"""
attrdialog_start = """\
called Dialog.__init__ with args {testobj.parent} () {{}}
called Dialog.setWindowTitle with args ('{title}',)
called Dialog.setWindowIcon with args ('appicon',)
called Label.__init__ with args ('Attribute name:', {testobj})
called LineEdit.__init__
called CheckBox.__init__
called ComboBox.__init__
called ComboBox.setEditable with arg `False`
called ComboBox.addItems with arg `-- none --`
called ComboBox.addItems with arg {{'ns1': 'namespace1', 'ns2': 'namespace'}}
called Label.__init__ with args ('Attribute value:', {testobj})
called LineEdit.__init__
called PushButton.__init__ with args ('&Save', {testobj}) {{}}
called PushButton.setDefault with arg `True`
called Signal.connect with args ({testobj.accept},)
called PushButton.__init__ with args ('&Cancel', {testobj}) {{}}
called Signal.connect with args ({testobj.reject},)
"""
attrdialog_middle_1 = """\
called CheckBox.toggle
"""
attrdialog_middle_2 = """\
called ComboBox.setCurrentIndex with arg `2`
"""
attrdialog_end = """\
called LineEdit.setText with arg `{name}`
called LineEdit.setText with arg `{value}`
called VBox.__init__
called HBox.__init__
called Grid.__init__
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 0)
called HBox.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'>
called HBox.addStretch
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (0, 1)
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'> at (1, 0)
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockComboBox'> at (1, 1)
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (2, 0)
called HBox.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'>
called HBox.addStretch
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (2, 1)
called HBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockGridLayout'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called HBox.addStretch
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
"""
search = """\
called Dialog.__init__ with args {testobj.parent} () {{}}
called Dialog.setWindowTitle with args ('{title}',)
called VBox.__init__
called Grid.__init__
called Label.__init__ with args ('Element', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 0)
called VBox.__init__
called HBox.__init__
called Label.__init__ with args ('name:', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called LineEdit.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'> at (0, 1)
called VBox.__init__
called Label.__init__ with args ('Attribute', {testobj})
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'> at (1, 0)
called VBox.__init__
called HBox.__init__
called Label.__init__ with args ('name:', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called LineEdit.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'> at (1, 1)
called VBox.__init__
called HBox.__init__
called Label.__init__ with args ('value:', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called LineEdit.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'> at (2, 1)
called Label.__init__ with args ('Text', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (3, 0)
called HBox.__init__
called Label.__init__ with args ('value:', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called LineEdit.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'>
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (3, 1)
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockGridLayout'>
called HBox.__init__
called Label.__init__ with args ('', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Ok', {testobj}) {{}}
called Signal.connect with args ({testobj.accept},)
called PushButton.setDefault with arg `True`
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Cancel', {testobj}) {{}}
called Signal.connect with args ({testobj.reject},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('C&lear Values', {testobj}) {{}}
called Signal.connect with args (<bound method SearchDialog.clear_values of {testobj}>,)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
called Signal.connect with args ({testobj.set_search},)
called LineEdit.setText with arg `{name}`
called Signal.connect with args ({testobj.set_search},)
called LineEdit.setText with arg `{attr}`
called Signal.connect with args ({testobj.set_search},)
called LineEdit.setText with arg `{attrval}`
called Signal.connect with args ({testobj.set_search},)
called LineEdit.setText with arg `{text}`
"""
undostack = """\
called MainWindow.__init__
called Application.__init__
called Action.__init__ with args ({parent},)
called Action.__init__ with args ({parent},)
called UndoStack.__init__ with args ({parent},)
called Signal.connect with args ({testobj.clean_changed},)
called Signal.connect with args ({testobj.index_changed},)
called UndoRedoStack.undoLimit
called UndoRedoStack.setUndoLimit with arg 1
called Action.setText with arg `Nothing to undo`
called Action.setText with arg `Nothing to redo`
called Action.setDisabled with arg `True`
called Action.setDisabled with arg `True`
"""


@pytest.fixture
def expected_output():
    return {'element': eldialog_start + eldialog_end,
            'element2': eldialog_start + eldialog_middle_1 + eldialog_end,
            'element3': eldialog_start + eldialog_middle_1 + eldialog_middle_2 + eldialog_end,
            'attrib': attrdialog_start + attrdialog_end,
            'attrib2': attrdialog_start + attrdialog_middle_1 + attrdialog_end,
            'attrib3': attrdialog_start + attrdialog_middle_1 + attrdialog_middle_2
            + attrdialog_end,
            'search': search, 'undostack': undostack}


class MockEditor:
    def __init__(self):
        print('called Editor.__init__')
        self.ns_uris = {'ns1': 'namespace1', 'ns2': 'namespace'}


class MockTree:
    def __init__(self):
        print('called Tree.__init__')

class MockGui:
    def __init__(self):
        print('called Gui.__init__')
        self.editor = MockEditor()
        self._icon = 'appicon'
    def meldfout(self, msg):
        print(f"called Gui.meldfout with arg '{msg}'")
    def init_menus(self, **kwargs):
        print('called Gui.init_menus with args', kwargs)
        return mockqtw.MockMenu()
    def set_selected_item(self, item):
        print('called Gui.set_selected_item with arg', item)


# jammergenoeg komt deze maar op 2 uitgecommentaarde locaties voor
def test_calculate_location(monkeypatch, capsys):
    """unittest for gui_qt.calculate_location
    """
    class Node:
        def __init__(self, name, parent=None):
            self.name = name
            self.children = []
            self._parent = parent
            if parent:
                parent.children.append(self)
        def parent(self):
            print(f"called self.parent with arg '{self.name}'")
            return self._parent
        def indexOfChild(self, node):
            return self.children.index(node)
    level0 = Node('level0')
    level1 = Node('level1', level0)
    level1a = Node('level1a', level0)
    level2 = Node('level2', level1a)
    win = types.SimpleNamespace(top=level0)
    assert testee.calculate_location(win, level2) == (1, 0)
    assert capsys.readouterr().out == ("called self.parent with arg 'level2'\n"
                                       "called self.parent with arg 'level1a'\n")


class TestElementDialog:
    """unittest for gui_qt.ElementDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.ElementDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ElementDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ElementDialog, '__init__', mock_init)
        testobj = testee.ElementDialog()
        testobj._parent = MockGui()
        assert capsys.readouterr().out == ('called ElementDialog.__init__ with args ()\n'
                                           'called Gui.__init__\n'
                                           'called Editor.__init__\n')
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for ElementDialog.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QTextEdit', mockqtw.MockEditorWidget)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        parent = MockGui()
        assert capsys.readouterr().out == "called Gui.__init__\ncalled Editor.__init__\n"
        testobj = testee.ElementDialog(parent)
        assert capsys.readouterr().out == expected_output['element'].format(testobj=testobj,
                                                                            tag='',
                                                                            title='',
                                                                            text='')
        mockitem = {'tag': 'simple'}
        testobj = testee.ElementDialog(parent, item=mockitem)
        assert capsys.readouterr().out == expected_output['element'].format(testobj=testobj,
                                                                            tag='simple',
                                                                            title='',
                                                                            text='')
        mockitem = {'tag': '{ns}tag', 'text': 'some text'}
        testobj = testee.ElementDialog(parent, "xxxxx", mockitem)
        assert capsys.readouterr().out == expected_output['element2'].format(testobj=testobj,
                                                                            tag='tag',
                                                                            title='xxxxx',
                                                                            text='some text')
        mockitem = {'tag': '{ns2}tag', 'text': 'some text'}
        testobj = testee.ElementDialog(parent, "xxxxx", mockitem)
        assert capsys.readouterr().out == expected_output['element3'].format(testobj=testobj,
                                                                            tag='tag',
                                                                            title='xxxxx',
                                                                            text='some text')

    def test_accept(self, monkeypatch, capsys):
        """unittest for ElementDialog.accept
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.txt_tag = mockqtw.MockLineEdit()
        testobj.txt_data = mockqtw.MockEditorWidget()
        testobj.cb = mockqtw.MockCheckBox()
        testobj.cb_ns = mockqtw.MockCheckBox()
        testobj.cmb_ns = mockqtw.MockComboBox()
        assert capsys.readouterr().out == ("called LineEdit.__init__\n"
                                           "called Editor.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called ComboBox.__init__\n")
        testobj.accept()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called Gui.meldfout with arg 'Element name must not be empty'\n"
                "called LineEdit.setFocus\n")
        testobj.txt_tag.setText('ele ment')
        assert capsys.readouterr().out == 'called LineEdit.setText with arg `ele ment`\n'
        testobj.accept()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called Gui.meldfout with arg 'Element name must not contain spaces'\n"
                "called LineEdit.setFocus\n")
        testobj.txt_tag.setText('1element')
        assert capsys.readouterr().out == 'called LineEdit.setText with arg `1element`\n'
        testobj.accept()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called Gui.meldfout with arg 'Element name must not start with a digit'\n"
                "called LineEdit.setFocus\n")
        testobj.txt_tag.setText('element')
        assert capsys.readouterr().out == 'called LineEdit.setText with arg `element`\n'
        testobj.accept()
        assert testobj._parent.data['tag'] == "element"
        assert not testobj._parent.data['data']
        assert testobj._parent.data['text'] == "editor text"
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called CheckBox.isChecked\n"
                "called CheckBox.isChecked\n"
                "called Editor.toPlainText\n"
                "called Dialog.accept\n")
        testobj.cb_ns.setChecked(True)
        testobj.cmb_ns.setCurrentIndex(0)
        assert capsys.readouterr().out == ("called CheckBox.setChecked with arg True\n"
                                           "called ComboBox.setCurrentIndex with arg `0`\n")
        testobj.accept()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called CheckBox.isChecked\n"
                "called ComboBox.currentIndex\n"
                "called Gui.meldfout with arg 'Namespace must be selected if checked'\n"
                "called CheckBox.setFocus\n")
        testobj.cmb_ns.setCurrentIndex(1)
        assert capsys.readouterr().out == "called ComboBox.setCurrentIndex with arg `1`\n"
        testobj.accept()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called CheckBox.isChecked\n"
                "called ComboBox.currentIndex\n"
                "called ComboBox.itemText with value `1`\n"
                "called CheckBox.isChecked\n"
                "called Editor.toPlainText\n"
                "called Dialog.accept\n")

    def test_keyPressEvent(self, monkeypatch, capsys):
        """unittest for ElementDialog.keyPressEvent
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'done', mockqtw.MockDialog.done)
        testobj = self.setup_testobj(monkeypatch, capsys)
        event = mockqtw.MockEvent(key=None)
        testobj.keyPressEvent(event)
        assert capsys.readouterr().out == ""
        event = mockqtw.MockEvent(key=testee.core.Qt.Key_Escape)
        testobj.keyPressEvent(event)
        assert capsys.readouterr().out == (
                f"called Dialog.done with arg `{testee.qtw.QDialog.Rejected}`\n")


class TestAttributeDialog:
    """unittest for gui_qt.AttributeDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.AttributeDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called AttributeDialog.__init__ with args', args)
        monkeypatch.setattr(testee.AttributeDialog, '__init__', mock_init)
        testobj = testee.AttributeDialog()
        testobj._parent = MockGui()
        assert capsys.readouterr().out == ('called AttributeDialog.__init__ with args ()\n'
                                           'called Gui.__init__\n'
                                           'called Editor.__init__\n')
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for AttributeDialog.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        parent = MockGui()
        assert capsys.readouterr().out == "called Gui.__init__\ncalled Editor.__init__\n"
        testobj = testee.AttributeDialog(parent)
        assert capsys.readouterr().out == expected_output['attrib'].format(testobj=testobj,
                                                                            name='',
                                                                            title='',
                                                                            value='')
        mockitem = {'name': 'xxx', 'value': 'yyy'}
        testobj = testee.AttributeDialog(parent, item=mockitem)
        assert capsys.readouterr().out == expected_output['attrib'].format(testobj=testobj,
                                                                            name='xxx',
                                                                            title='',
                                                                            value='yyy')
        mockitem = {'name': '{ns}xxx', 'value': 'yyy'}
        testobj = testee.AttributeDialog(parent, 'title', mockitem)
        assert capsys.readouterr().out == expected_output['attrib2'].format(testobj=testobj,
                                                                            name='xxx',
                                                                            title='title',
                                                                            value='yyy')
        mockitem = {'name': '{ns2}xxx', 'value': 'yyy'}
        testobj = testee.AttributeDialog(parent, 'title', mockitem)
        assert capsys.readouterr().out == expected_output['attrib3'].format(testobj=testobj,
                                                                            name='xxx',
                                                                            title='title',
                                                                            value='yyy')

    def test_accept(self, monkeypatch, capsys):
        """unittest for AttributeDialog.accept
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.txt_name = mockqtw.MockLineEdit()
        testobj.txt_value = mockqtw.MockLineEdit()
        testobj.cb_ns = mockqtw.MockCheckBox()
        testobj.cmb_ns = mockqtw.MockComboBox()
        assert capsys.readouterr().out == ("called LineEdit.__init__\n"
                                           "called LineEdit.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called ComboBox.__init__\n")
        testobj.accept()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called Gui.meldfout with arg 'Attribute name must not be empty'\n"
                "called LineEdit.setFocus\n")
        testobj.txt_name.setText('attr ib')
        assert capsys.readouterr().out == 'called LineEdit.setText with arg `attr ib`\n'
        testobj.accept()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called Gui.meldfout with arg 'Attribute name must not contain spaces'\n"
                "called LineEdit.setFocus\n")
        testobj.txt_name.setText('1attrib')
        assert capsys.readouterr().out == 'called LineEdit.setText with arg `1attrib`\n'
        testobj.accept()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called Gui.meldfout with arg 'Attribute name must not start with a digit'\n"
                "called LineEdit.setFocus\n")
        testobj.txt_name.setText('attrib')
        assert capsys.readouterr().out == 'called LineEdit.setText with arg `attrib`\n'
        testobj.accept()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called CheckBox.isChecked\n"
                "called LineEdit.text\n"
                "called Dialog.accept\n")
        testobj.cb_ns.setChecked(True)
        testobj.cmb_ns.setCurrentIndex(0)
        assert capsys.readouterr().out == ("called CheckBox.setChecked with arg True\n"
                                           "called ComboBox.setCurrentIndex with arg `0`\n")
        testobj.accept()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called CheckBox.isChecked\n"
                "called ComboBox.currentIndex\n"
                "called Gui.meldfout with arg 'Namespace must be selected if checked'\n"
                "called CheckBox.setFocus\n")
        testobj.cmb_ns.setCurrentIndex(1)
        assert capsys.readouterr().out == "called ComboBox.setCurrentIndex with arg `1`\n"
        testobj.accept()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called CheckBox.isChecked\n"
                "called ComboBox.currentIndex\n"
                "called ComboBox.itemText with value `1`\n"
                "called LineEdit.text\n"
                "called Dialog.accept\n")

    def test_keyPressEvent(self, monkeypatch, capsys):
        """unittest for AttributeDialog.keyPressEvent
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'done', mockqtw.MockDialog.done)
        testobj = self.setup_testobj(monkeypatch, capsys)
        event = mockqtw.MockEvent(key=None)
        testobj.keyPressEvent(event)
        assert capsys.readouterr().out == ""
        event = mockqtw.MockEvent(key=testee.core.Qt.Key_Escape)
        testobj.keyPressEvent(event)
        assert capsys.readouterr().out == (
                f"called Dialog.done with arg `{testee.qtw.QDialog.Rejected}`\n")


class TestSearchDialog:
    """unittest for gui_qt.SearchDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.SearchDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SearchDialog.__init__ with args', args)
        monkeypatch.setattr(testee.SearchDialog, '__init__', mock_init)
        testobj = testee.SearchDialog()
        testobj._parent = MockGui()
        assert capsys.readouterr().out == ('called SearchDialog.__init__ with args ()\n'
                                           'called Gui.__init__\n'
                                           'called Editor.__init__\n')
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for SearchDialog.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        parent = MockGui()
        parent.editor.search_args = None
        assert capsys.readouterr().out == "called Gui.__init__\ncalled Editor.__init__\n"
        testobj = testee.SearchDialog(parent)
        assert capsys.readouterr().out == expected_output['search'].format(testobj=testobj,
                                                                           title='',
                                                                           name='', attr='',
                                                                           attrval='', text='')
        parent.editor.search_args = ('x', 'y', 'z', 'aa')
        testobj = testee.SearchDialog(parent, title="xxxxx")
        assert capsys.readouterr().out == expected_output['search'].format(testobj=testobj,
                                                                           title='xxxxx',
                                                                           name='x', attr='y',
                                                                           attrval='z', text='aa')

    def test_set_search(self, monkeypatch, capsys):
        """unittest for SearchDialog.set_search
        """
        def mock_get(*args):
            print('called Editor.get_search_text with args', args)
            return args
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.txt_element = mockqtw.MockLineEdit()
        testobj.txt_element.setText('xxx')
        testobj.txt_attr_name = mockqtw.MockLineEdit()
        testobj.txt_attr_name.setText('yyy')
        testobj.txt_attr_val = mockqtw.MockLineEdit()
        testobj.txt_attr_val.setText('zzz')
        testobj.txt_text = mockqtw.MockLineEdit()
        testobj.txt_text.setText('qqq')
        testobj.lbl_search = mockqtw.MockLabel()
        assert capsys.readouterr().out == (
                "called LineEdit.__init__\ncalled LineEdit.setText with arg `xxx`\n"
                "called LineEdit.__init__\ncalled LineEdit.setText with arg `yyy`\n"
                "called LineEdit.__init__\ncalled LineEdit.setText with arg `zzz`\n"
                "called LineEdit.__init__\ncalled LineEdit.setText with arg `qqq`\n"
                "called Label.__init__\n")
        testobj._parent.editor.get_search_text = mock_get
        testobj.set_search()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called Editor.get_search_text with args ('xxx', 'yyy', 'zzz', 'qqq')\n"
                "called Label.setText with arg `xxx\nyyy\nzzz\nqqq`\n")

    def test_clear_values(self, monkeypatch, capsys):
        """unittest for SearchDialog.clear_values
        """
        def mock_update():
            print('called SearchDialog.update')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.update = mock_update
        testobj.txt_element = mockqtw.MockLineEdit()
        testobj.txt_attr_name = mockqtw.MockLineEdit()
        testobj.txt_attr_val = mockqtw.MockLineEdit()
        testobj.txt_text = mockqtw.MockLineEdit()
        testobj.lbl_search = mockqtw.MockLabel()
        testobj.lblsizer = mockqtw.MockHBoxLayout()
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == (
                "called LineEdit.__init__\ncalled LineEdit.__init__\n"
                "called LineEdit.__init__\ncalled LineEdit.__init__\n"
                "called Label.__init__\ncalled HBox.__init__\ncalled VBox.__init__\n")
        testobj.clear_values()
        assert capsys.readouterr().out == ("called LineEdit.clear\n"
                                           "called LineEdit.clear\n"
                                           "called LineEdit.clear\n"
                                           "called LineEdit.clear\n"
                                           "called Label.setText with arg ``\n"
                                           "called HBox.update\n"
                                           "called VBox.update\n"
                                           "called SearchDialog.update\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for SearchDialog.accept
        """
        count = 0
        def mock_text(self):
            nonlocal count
            print("called LineEdit.text")
            count += 1
            if count == 2:
                return 'x'
            return ''
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.txt_element = mockqtw.MockLineEdit()
        testobj.txt_attr_name = mockqtw.MockLineEdit()
        testobj.txt_attr_val = mockqtw.MockLineEdit()
        testobj.txt_text = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == ("called LineEdit.__init__\n"
                                           "called LineEdit.__init__\n"
                                           "called LineEdit.__init__\n"
                                           "called LineEdit.__init__\n")
        testobj.accept()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called Gui.meldfout with arg 'Please enter search criteria or press cancel'\n"
                "called LineEdit.setFocus\n")
        monkeypatch.setattr(mockqtw.MockLineEdit, 'text', mock_text)
        testobj.accept()
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called Dialog.accept\n")


class TestVisualTree:
    """unittest for gui_qt.VisualTree
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.VisualTree object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called VisualTree.__init__ with args', args)
        monkeypatch.setattr(testee.VisualTree, '__init__', mock_init)
        testobj = testee.VisualTree()
        testobj.parent = MockGui()
        assert capsys.readouterr().out == ('called VisualTree.__init__ with args ()\n'
                                           "called Gui.__init__\n"
                                           "called Editor.__init__\n")
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for VisualTree.__init__
        """
        monkeypatch.setattr(testee.qtw.QTreeWidget, '__init__', mockqtw.MockTreeWidget.__init__)
        parent = MockGui()
        testobj = testee.VisualTree(parent)
        assert capsys.readouterr().out == ("called Gui.__init__\n"
                                           "called Editor.__init__\n"
                                           "called Tree.__init__\n")

    def test_mouseDoubleClickEvent(self, monkeypatch, capsys):
        """unittest for VisualTree.mouseDoubleClickEvent
        """
        def mock_itemat(x, y):
            print(f'called VisualTree.itemat with args ({x}, {y})')
            return None
        def mock_itemat_2(x, y):
            print(f'called VisualTree.itemat with args ({x}, {y})')
            return 'an item'
        def mock_edit(arg):
            print(f"called Gui.edit_item with arg '{arg}'")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.itemAt = mock_itemat
        testobj.parent.edit_item = mock_edit
        event = mockqtw.MockEvent()
        testobj.mouseDoubleClickEvent(event)
        assert capsys.readouterr().out == ("called VisualTree.itemat with args (x, y)\n"
                                           "called event.ignore\n")
        testobj.itemAt = mock_itemat_2
        testobj.parent.top = None
        testobj.mouseDoubleClickEvent(event)
        assert capsys.readouterr().out == ("called VisualTree.itemat with args (x, y)\n"
                                           "called Gui.edit_item with arg 'an item'\n")
        testobj.parent.top = 'an item'
        testobj.mouseDoubleClickEvent(event)
        assert capsys.readouterr().out == ("called VisualTree.itemat with args (x, y)\n"
                                           "called event.ignore\n")

    def test_mouseReleaseEvent(self, monkeypatch, capsys):
        """unittest for VisualTree.mouseReleaseEvent
        """
        def mock_itemat(arg):
            print('called VisualTree.itemat with arg', arg)
            return 'an item'
        def mock_map(arg):
            print('called VisualTree.mapToGlobal with arg', arg)
        def mock_button(self):
            print('called event.button')
            return testee.core.Qt.LeftButton
        def mock_button_2(self):
            print('called event.button')
            return testee.core.Qt.RightButton
        monkeypatch.setattr(mockqtw.MockEvent, 'button', mock_button)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.itemAt = mock_itemat
        testobj.mapToGlobal = mock_map
        event = mockqtw.MockEvent()
        testobj.mouseReleaseEvent(event)
        assert capsys.readouterr().out == ("called VisualTree.itemat with arg ('x', 'y')\n"
                                           "called event.button\n"
                                           "called Gui.set_selected_item with arg an item\n"
                                           "called event.ignore\n")
        monkeypatch.setattr(mockqtw.MockEvent, 'button', mock_button_2)
        testobj.parent.top = None
        testobj.mouseReleaseEvent(event)
        assert capsys.readouterr().out == ("called VisualTree.itemat with arg ('x', 'y')\n"
                                           "called event.button\n"
                                           "called Gui.init_menus with args {'popup': True}\n"
                                           "called Menu.__init__ with args ()\n"
                                           "called VisualTree.mapToGlobal with arg ('x', 'y')\n"
                                           "called Menu.exec_ with args (None,) {}\n"
                                           "called event.ignore\n")
        testobj.parent.top = 'an item'
        testobj.mouseReleaseEvent(event)
        assert capsys.readouterr().out == ("called VisualTree.itemat with arg ('x', 'y')\n"
                                           "called event.button\n"
                                           "called event.ignore\n")


class TestUndoRedoStack:
    """unittest for gui_qt.UndoRedoStack
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.UndoRedoStack object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called UndoRedoStack.__init__ with args', args)
        monkeypatch.setattr(testee.UndoRedoStack, '__init__', mock_init)
        monkeypatch.setattr(testee.UndoRedoStack, 'setUndoLimit',
                            mockqtw.MockUndoStack.setUndoLimit)
        parent = MockGui()
        parent.statusbar = mockqtw.MockStatusBar()
        parent.undo_item = mockqtw.MockAction(parent)
        parent.redo_item = mockqtw.MockAction(parent)
        testobj = testee.UndoRedoStack(parent)
        testobj.maxundo = 5
        testobj.parent = lambda: parent
        assert capsys.readouterr().out == ('called Gui.__init__\n'
                                           'called Editor.__init__\n'
                                           'called StatusBar.__init__ with args ()\n'
                                           f'called Action.__init__ with args ({parent},)\n'
                                           f'called Action.__init__ with args ({parent},)\n'
                                           f'called UndoRedoStack.__init__ with args ({parent},)\n')
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for UndoRedoStack.__init__
        """
        monkeypatch.setattr(testee.qtw.QMainWindow, '__init__', mockqtw.MockMainWindow.__init__)
        monkeypatch.setattr(testee.qtw.QUndoStack, '__init__', mockqtw.MockUndoStack.__init__)
        monkeypatch.setattr(testee.qtw.QUndoStack, 'cleanChanged', mockqtw.MockUndoStack.cleanChanged)
        monkeypatch.setattr(testee.qtw.QUndoStack, 'indexChanged', mockqtw.MockUndoStack.indexChanged)
        monkeypatch.setattr(testee.qtw.QUndoStack, 'undoLimit', mockqtw.MockUndoStack.undoLimit)
        monkeypatch.setattr(testee.qtw.QUndoStack, 'setUndoLimit', mockqtw.MockUndoStack.setUndoLimit)
        parent = testee.qtw.QMainWindow()
        parent.undo_item = mockqtw.MockAction(parent)
        parent.redo_item = mockqtw.MockAction(parent)
        # breakpoint()
        testobj = testee.UndoRedoStack(parent)
        # assert testobj.maxundo == mockqtw.MockUndoStack.MAXUNDO
        assert capsys.readouterr().out == expected_output['undostack'].format(testobj=testobj,
                                                                              parent=parent)

    def test_unset_undo_limit(self, monkeypatch, capsys):
        """unittest for UndoRedoStack.unset_undo_limit
        """
        monkeypatch.setattr(testee.qtw.QUndoStack, 'setUndoLimit',
                            mockqtw.MockUndoStack.setUndoLimit)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.unset_undo_limit(True)
        assert capsys.readouterr().out == (
                "called UndoRedoStack.setUndoLimit with arg 5\n"
                "called StatusBar.showMessage with arg `Undo level is now unlimited`\n")
        testobj.unset_undo_limit(False)
        assert capsys.readouterr().out == (
                "called UndoRedoStack.setUndoLimit with arg 1\n"
                "called StatusBar.showMessage with arg `Undo level is now limited to one`\n")

    def test_clean_changed(self, monkeypatch, capsys):
        """unittest for UndoRedoStack.clean_changed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.clean_changed(True)
        assert capsys.readouterr().out == ("called Action.setText with arg `Nothing to undo`\n"
                                           "called Action.setDisabled with arg `True`\n")
        testobj.clean_changed(False)
        assert capsys.readouterr().out == ("called Action.setDisabled with arg `False`\n")

    def test_index_changed(self, monkeypatch, capsys):
        """unittest for UndoRedoStack.index_changed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.undoText = lambda: ''
        testobj.redoText = lambda: ''
        testobj.index_changed()
        assert capsys.readouterr().out == ("called Action.setText with arg `Nothing to undo`\n"
                                           "called Action.setDisabled with arg `True`\n"
                                           "called Action.setText with arg `Nothing to redo`\n"
                                           "called Action.setDisabled with arg `True`\n")
        testobj.undoText = lambda: ''
        testobj.redoText = lambda: 'x'
        testobj.index_changed()
        assert capsys.readouterr().out == ("called Action.setText with arg `Nothing to undo`\n"
                                           "called Action.setDisabled with arg `True`\n"
                                           "called Action.setText with arg `&Redo x`\n"
                                           "called Action.setEnabled with arg `True`\n")
        testobj.undoText = lambda: 'x'
        testobj.redoText = lambda: ''
        testobj.index_changed()
        assert capsys.readouterr().out == ("called Action.setText with arg `&Undo x`\n"
                                           "called Action.setEnabled with arg `True`\n"
                                           "called Action.setText with arg `Nothing to redo`\n"
                                           "called Action.setDisabled with arg `True`\n")
        testobj.undoText = lambda: 'x'
        testobj.redoText = lambda: 'x'
        testobj.index_changed()
        assert capsys.readouterr().out == ("called Action.setText with arg `&Undo x`\n"
                                           "called Action.setEnabled with arg `True`\n"
                                           "called Action.setText with arg `&Redo x`\n"
                                           "called Action.setEnabled with arg `True`\n")


class TestPasteElementCommand:
    """unittest for gui_qt.PasteElementCommand
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.PasteElementCommand object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called PasteElementCommand.__init__ with args', args)
        monkeypatch.setattr(testee.PasteElementCommand, '__init__', mock_init)
        testobj = testee.PasteElementCommand()
        assert capsys.readouterr().out == 'called PasteElementCommand.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for PasteElementCommand.__init__
        """
        win = MockGui()
        win.editor.tree_dirty = False
        assert capsys.readouterr().out == "called Gui.__init__\ncalled Editor.__init__\n"
        monkeypatch.setattr(testee.qtw.QUndoCommand, '__init__', mockqtw.MockUndoCommand)
        testobj = testee.PasteElementCommand(win, 'tag', 'text', True, False, data=['xx'])
        assert testobj.win == win
        assert testobj.tag == 'tag'
        assert testobj.data == 'text'
        assert testobj.before
        assert not testobj.below
        assert testobj.children == ['xx']
        assert testobj.where is None
        assert testobj.replaced is None
        assert testobj.first_edit
        assert capsys.readouterr().out == "called UndoCommand.__init__ with args (' Before',) {}\n"
        win.editor.tree_dirty = True
        testobj = testee.PasteElementCommand(win, 'tag', 'text', False, False, "xx", where= 'yy')
        assert testobj.win == win
        assert testobj.tag == 'tag'
        assert testobj.data == 'text'
        assert not testobj.before
        assert not testobj.below
        assert testobj.children is None
        assert testobj.where == 'yy'
        assert testobj.replaced is None
        assert not testobj.first_edit
        assert capsys.readouterr().out == "called UndoCommand.__init__ with args ('xx After',) {}\n"
        testobj = testee.PasteElementCommand(win, 'tag', 'text', False, True, "xx", ['yy'], 'zz')
        assert testobj.win == win
        assert testobj.tag == 'tag'
        assert testobj.data == 'text'
        assert not testobj.before
        assert testobj.below
        assert testobj.children == ['yy']
        assert testobj.where == 'zz'
        assert testobj.replaced is None
        assert not testobj.first_edit
        assert capsys.readouterr().out == "called UndoCommand.__init__ with args ('xx Under',) {}\n"
        testobj = testee.PasteElementCommand(win, 'tag', 'text', True, True, "xx", ['yy'], 'zz')
        assert testobj.win == win
        assert testobj.tag == 'tag'
        assert testobj.data == 'text'
        assert testobj.before
        assert testobj.below
        assert testobj.children == ['yy']
        assert testobj.where == 'zz'
        assert testobj.replaced is None
        assert not testobj.first_edit
        assert capsys.readouterr().out == "called UndoCommand.__init__ with args ('xx Under',) {}\n"

    def _test_redo(self, monkeypatch, capsys):
        """unittest for PasteElementCommand.redo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.redo() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_undo(self, monkeypatch, capsys):
        """unittest for PasteElementCommand.undo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.undo() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestPasteAttributeCommand:
    """unittest for gui_qt.PasteAttributeCommand
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.PasteAttributeCommand object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called PasteAttributeCommand.__init__ with args', args)
        monkeypatch.setattr(testee.PasteAttributeCommand, '__init__', mock_init)
        testobj = testee.PasteAttributeCommand()
        assert capsys.readouterr().out == 'called PasteAttributeCommand.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for PasteAttributeCommand.__init__
        """
        testobj = testee.PasteAttributeCommand(win, name, value, item, description="")
        assert capsys.readouterr().out == ("")

    def _test_redo(self, monkeypatch, capsys):
        """unittest for PasteAttributeCommand.redo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.redo() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_undo(self, monkeypatch, capsys):
        """unittest for PasteAttributeCommand.undo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.undo() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestEditCommand:
    """unittest for gui_qt.EditCommand
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.EditCommand object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called EditCommand.__init__ with args', args)
        monkeypatch.setattr(testee.EditCommand, '__init__', mock_init)
        testobj = testee.EditCommand()
        assert capsys.readouterr().out == 'called EditCommand.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for EditCommand.__init__
        """
        testobj = testee.EditCommand(win, old_state, new_state, description="")
        assert capsys.readouterr().out == ("")

    def _test_redo(self, monkeypatch, capsys):
        """unittest for EditCommand.redo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.redo() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_undo(self, monkeypatch, capsys):
        """unittest for EditCommand.undo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.undo() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestCopyElementCommand:
    """unittest for gui_qt.CopyElementCommand
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.CopyElementCommand object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called CopyElementCommand.__init__ with args', args)
        monkeypatch.setattr(testee.CopyElementCommand, '__init__', mock_init)
        testobj = testee.CopyElementCommand()
        assert capsys.readouterr().out == 'called CopyElementCommand.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for CopyElementCommand.__init__
        """
        testobj = testee.CopyElementCommand(win, item, cut, retain, description="")
        assert capsys.readouterr().out == ("")

    def _test_redo(self, monkeypatch, capsys):
        """unittest for CopyElementCommand.redo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.redo() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_undo(self, monkeypatch, capsys):
        """unittest for CopyElementCommand.undo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.undo() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestCopyAttributeCommand:
    """unittest for gui_qt.CopyAttributeCommand
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.CopyAttributeCommand object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called CopyAttributeCommand.__init__ with args', args)
        monkeypatch.setattr(testee.CopyAttributeCommand, '__init__', mock_init)
        testobj = testee.CopyAttributeCommand()
        assert capsys.readouterr().out == 'called CopyAttributeCommand.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for CopyAttributeCommand.__init__
        """
        testobj = testee.CopyAttributeCommand(win, item, cut, retain, description)
        assert capsys.readouterr().out == ("")

    def _test_redo(self, monkeypatch, capsys):
        """unittest for CopyAttributeCommand.redo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.redo() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_undo(self, monkeypatch, capsys):
        """unittest for CopyAttributeCommand.undo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.undo() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestGui:
    """unittest for gui_qt.Gui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.Gui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Gui.__init__ with args', args)
        monkeypatch.setattr(testee.Gui, '__init__', mock_init)
        testobj = testee.Gui()
        assert capsys.readouterr().out == 'called Gui.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for Gui.__init__
        """
        testobj = testee.Gui(parent=None, fn='', readonly=False)
        assert capsys.readouterr().out == ("")

    def _test_go(self, monkeypatch, capsys):
        """unittest for Gui.go
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.go() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_keyReleaseEvent(self, monkeypatch, capsys):
        """unittest for Gui.keyReleaseEvent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.keyReleaseEvent(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_closeEvent(self, monkeypatch, capsys):
        """unittest for Gui.closeEvent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.closeEvent(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_node_children(self, monkeypatch, capsys):
        """unittest for Gui.get_node_children
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_node_children(node) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_node_title(self, monkeypatch, capsys):
        """unittest for Gui.get_node_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_node_title(node) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_node_data(self, monkeypatch, capsys):
        """unittest for Gui.get_node_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_node_data(node) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_treetop(self, monkeypatch, capsys):
        """unittest for Gui.get_treetop
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_treetop() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_setup_new_tree(self, monkeypatch, capsys):
        """unittest for Gui.setup_new_tree
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.setup_new_tree(title) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_node_to_parent(self, monkeypatch, capsys):
        """unittest for Gui.add_node_to_parent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_node_to_parent(parent, pos=-1) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_node_title(self, monkeypatch, capsys):
        """unittest for Gui.set_node_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_node_title(node, title) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_node_parentpos(self, monkeypatch, capsys):
        """unittest for Gui.get_node_parentpos
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_node_parentpos(node) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_node_data(self, monkeypatch, capsys):
        """unittest for Gui.set_node_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_node_data(node, name, value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_selected_item(self, monkeypatch, capsys):
        """unittest for Gui.get_selected_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_selected_item() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_selected_item(self, monkeypatch, capsys):
        """unittest for Gui.set_selected_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_selected_item(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_is_node_root(self, monkeypatch, capsys):
        """unittest for Gui.is_node_root
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.is_node_root(item=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_expand_item(self, monkeypatch, capsys):
        """unittest for Gui.expand_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.expand_item(item=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_collapse_item(self, monkeypatch, capsys):
        """unittest for Gui.collapse_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.collapse_item(item=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_edit_item(self, monkeypatch, capsys):
        """unittest for Gui.edit_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.edit_item(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_copy(self, monkeypatch, capsys):
        """unittest for Gui.copy
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.copy(item, cut=False, retain=True) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_paste(self, monkeypatch, capsys):
        """unittest for Gui.paste
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.paste(item, before=True, below=False) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_attribute(self, monkeypatch, capsys):
        """unittest for Gui.add_attribute
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_attribute(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_insert(self, monkeypatch, capsys):
        """unittest for Gui.insert
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.insert(item, before=True, below=False) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_init_gui(self, monkeypatch, capsys):
        """unittest for Gui.init_gui
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.init_gui() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_windowtitle(self, monkeypatch, capsys):
        """unittest for Gui.set_windowtitle
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_windowtitle(text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_windowtitle(self, monkeypatch, capsys):
        """unittest for Gui.get_windowtitle
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_windowtitle() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_init_menus(self, monkeypatch, capsys):
        """unittest for Gui.init_menus
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.init_menus(popup=False) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_meldinfo(self, monkeypatch, capsys):
        """unittest for Gui.meldinfo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.meldinfo(text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_meldfout(self, monkeypatch, capsys):
        """unittest for Gui.meldfout
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.meldfout(text, abort=False) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_ask_yesnocancel(self, monkeypatch, capsys):
        """unittest for Gui.ask_yesnocancel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.ask_yesnocancel(prompt) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_ask_for_text(self, monkeypatch, capsys):
        """unittest for Gui.ask_for_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.ask_for_text(prompt, value='') == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_file_to_read(self, monkeypatch, capsys):
        """unittest for Gui.file_to_read
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.file_to_read() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_file_to_save(self, monkeypatch, capsys):
        """unittest for Gui.file_to_save
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.file_to_save() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_enable_pasteitems(self, monkeypatch, capsys):
        """unittest for Gui.enable_pasteitems
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.enable_pasteitems(active=False) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_limit_undo(self, monkeypatch, capsys):
        """unittest for Gui.limit_undo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.limit_undo() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_popupmenu(self, monkeypatch, capsys):
        """unittest for Gui.popupmenu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.popupmenu(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_quit(self, monkeypatch, capsys):
        """unittest for Gui.quit
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.quit() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_keyup(self, monkeypatch, capsys):
        """unittest for Gui.on_keyup
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_keyup(ev=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_ask_for_search_args(self, monkeypatch, capsys):
        """unittest for Gui.ask_for_search_args
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.ask_for_search_args() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_do_undo(self, monkeypatch, capsys):
        """unittest for Gui.do_undo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.do_undo() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_do_redo(self, monkeypatch, capsys):
        """unittest for Gui.do_redo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.do_redo() == "expected_result"
        assert capsys.readouterr().out == ("")
