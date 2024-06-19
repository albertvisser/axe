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
main = """\
called Icon.__init__ with arg `icon-name`
called MainWindow.resize with args (620, 900)
called MainWindow.setWindowIcon
called MainWindow.statusBar
called StatusBar.__init__ with args ()
called StatusBar.showMessage with arg `Ready`
called Gui.init_menus
called Tree.__init__
called TreeItem.__init__ with args ()
called TreeItem.setHidden with arg `True`
called MainWidget.setCentralWindow with arg of type `<class 'axe.gui_qt.VisualTree'>`
"""
main_edit = """\
called Gui.enable_pasteitems with arg False
called UndoredoStack.__init__ with arg {testobj}
called Editor.mark_dirty with arg False
"""

@pytest.fixture
def expected_output():
    """fixture for output predictions
    """
    return {'element': eldialog_start + eldialog_end,
            'element2': eldialog_start + eldialog_middle_1 + eldialog_end,
            'element3': eldialog_start + eldialog_middle_1 + eldialog_middle_2 + eldialog_end,
            'attrib': attrdialog_start + attrdialog_end,
            'attrib2': attrdialog_start + attrdialog_middle_1 + attrdialog_end,
            'attrib3': attrdialog_start + attrdialog_middle_1 + attrdialog_middle_2
            + attrdialog_end,
            'search': search, 'undostack': undostack,
            'maingui': main, 'maingui2': main + main_edit}


class MockEditor:
    """stub for base.Editor
    """
    def __init__(self):
        print('called Editor.__init__')
        self.ns_uris = {'ns1': 'namespace1', 'ns2': 'namespace'}
        self._count = 0
    def add_item(self, *args, **kwargs):
        print('called Editor.add_item with args', args, kwargs)
        self._count += 1
        return f'added item #{self._count}'
    def mark_dirty(self, value):
        print(f'called Editor.mark_dirty with arg {value}')
    def get_copy_text(self, *args):
        print("called Editor.get_copy_text with args", args)
        return 'copy'
    def getshortname(self, *args, **kwargs):
        print('called Editor.getshortname with args', args, kwargs)
        return 'shortname'


class MockTree:  # kan waarschijnlijk vervangen worden door mockqtw versie
    """stub for qtgui.VisualTree
    """
    def __init__(self):
        print('called Tree.__init__')
    def expandItem(self, arg):
        print('called Tree.expandItem with arg', arg)
    def setCurrentItem(self, arg):
        print('called Tree.setCurrentItem with arg', arg)


class MockGui:
    """stub for qtgui.Gui
    """
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
    def enable_pasteitems(self, value):
        print('called Gui.enable_pasteitems with arg', value)


def mock_and_create_nodes(monkeypatch, capsys, count):
    """Helper function to create parent TreeWidgetItem
    """
    monkeypatch.setattr(testee.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
    result = []
    while count > 0:
        node = testee.qtw.QTreeWidgetItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        result.append(node)
        count -= 1
    return result


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
        def mock_build(*args):
            print('called Editor.build_search_description with args', args)
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
        testobj._parent.editor.build_search_description = mock_build
        testobj.set_search()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called Editor.build_search_description with args ('xxx', 'yyy', 'zzz', 'qqq')\n"
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
        testobj.win = MockGui()
        testobj.win.tree = MockTree()
        assert capsys.readouterr().out == ('called PasteElementCommand.__init__ with args ()\n'
                                           "called Gui.__init__\n"
                                           "called Editor.__init__\n"
                                           "called Tree.__init__\n")
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

    def test_redo(self, monkeypatch, capsys):
        """unittest for PasteElementCommand.redo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.win.editor.elstart = '<> '
        testobj.where = 'here'
        testobj.tag = 'xx'
        testobj.data = 'yyy'
        testobj.before = True
        testobj.below = False
        testobj.children = None
        testobj.redo()
        assert testobj.added == 'added item #1'
        assert capsys.readouterr().out == (
                "called Editor.add_item with args ('here', 'xx', 'yyy')"
                " {'before': True, 'below': False}\n"
                "called Tree.expandItem with arg added item #1\n")
        testobj.children = [('xx', 'yyy', [('<> a', 'bb', [('c', 'dd', [])])])]
        # breakpoint()
        testobj.redo()
        assert testobj.added == 'added item #2'
        assert capsys.readouterr().out == (
                "called Editor.add_item with args ('here', 'xx', 'yyy')"
                " {'before': True, 'below': False}\n"
                "called Editor.add_item with args ('added item #2', '<> a', 'bb')"
                " {'before': False, 'below': True, 'attr': False}\n"
                "called Editor.add_item with args ('added item #3', 'c', 'dd')"
                " {'before': False, 'below': True, 'attr': True}\n"
                "called Tree.expandItem with arg added item #2\n")

    def test_undo(self, monkeypatch, capsys):
        """unittest for PasteElementCommand.undo
        """
        class MockCopy:
            def __init__(self, *args, **kwargs):
                print('called CopyElementCommand with args', args, kwargs)
            def redo(self):
                print('called CopyElementCommand.redo')
        monkeypatch.setattr(testee, 'CopyElementCommand', MockCopy)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.added = True
        testobj.first_edit = True
        testobj.text = lambda *x: 'text'
        testobj.win.statusbar = mockqtw.MockStatusBar()
        assert capsys.readouterr().out == "called StatusBar.__init__ with args ()\n"
        testobj.undo()
        assert capsys.readouterr().out == (
                "called CopyElementCommand with args"
                f" ({testobj.win}, True) {{'cut': True, 'retain': False,"
                " 'description': 'PyQT5 versie van een op een treeview gebaseerde XML-editor\\n'}\n"
                "called CopyElementCommand.redo\n"
                "called Editor.mark_dirty with arg False\n"
                "called StatusBar.showMessage with arg `text undone`\n")
        testobj.first_edit = False
        testobj.undo()
        assert capsys.readouterr().out == (
                "called CopyElementCommand with args"
                f" ({testobj.win}, True) {{'cut': True, 'retain': False,"
                " 'description': 'PyQT5 versie van een op een treeview gebaseerde XML-editor\\n'}\n"
                "called CopyElementCommand.redo\n"
                "called StatusBar.showMessage with arg `text undone`\n")


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
        testobj.win = MockGui()
        testobj.win.tree = MockTree()
        assert capsys.readouterr().out == ('called PasteAttributeCommand.__init__ with args ()\n'
                                           "called Gui.__init__\n"
                                           "called Editor.__init__\n"
                                           "called Tree.__init__\n")
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for PasteAttributeCommand.__init__
        """
        win = MockGui()
        win.editor.tree_dirty = False
        assert capsys.readouterr().out == "called Gui.__init__\ncalled Editor.__init__\n"
        monkeypatch.setattr(testee.qtw.QUndoCommand, '__init__', mockqtw.MockUndoCommand)
        testobj = testee.PasteAttributeCommand(win, 'name', 'value', 'item')
        assert testobj.win == win
        assert testobj.item == 'item'
        assert testobj.name == 'name'
        assert testobj.value == 'value'
        assert testobj.first_edit
        assert capsys.readouterr().out == "called UndoCommand.__init__ with args ('',) {}\n"
        win.editor.tree_dirty = True
        testobj = testee.PasteAttributeCommand(win, 'name', 'value', 'item', "xxx")
        assert testobj.win == win
        assert testobj.item == 'item'
        assert testobj.name == 'name'
        assert testobj.value == 'value'
        assert not testobj.first_edit
        assert capsys.readouterr().out == "called UndoCommand.__init__ with args ('xxx',) {}\n"

    def test_redo(self, monkeypatch, capsys):
        """unittest for PasteAttributeCommand.redo
        """
        added_item = types.SimpleNamespace(parent=lambda *x: 'parent of added item')
        def mock_add(*args, **kwargs):
            print('called Editor.add_item with args', args, kwargs)
            return added_item
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.item = 'item'
        testobj.name = 'name'
        testobj.value = 'value'
        testobj.win.editor.add_item = mock_add
        testobj.redo()
        assert testobj.added == added_item
        assert capsys.readouterr().out == (
                "called Editor.add_item with args ('item', 'name', 'value') {'attr': True}\n"
                "called Tree.expandItem with arg parent of added item\n")

    def test_undo(self, monkeypatch, capsys):
        """unittest for PasteAttributeCommand.undo
        """
        class MockCopy:
            def __init__(self, *args, **kwargs):
                print('called CopyAttributeCommand with args', args, kwargs)
            def redo(self):
                print('called CopyAttributeCommand.redo')
        monkeypatch.setattr(testee, 'CopyAttributeCommand', MockCopy)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.added = True
        testobj.first_edit = True
        testobj.text = lambda *x: 'text'
        testobj.win.statusbar = mockqtw.MockStatusBar()
        assert capsys.readouterr().out == "called StatusBar.__init__ with args ()\n"
        testobj.undo()
        assert capsys.readouterr().out == (
                "called CopyAttributeCommand with args"
                f" ({testobj.win}, True) {{'cut': True, 'retain': False,"
                " 'description': 'PyQT5 versie van een op een treeview gebaseerde XML-editor\\n'}\n"
                "called CopyAttributeCommand.redo\n"
                "called Editor.mark_dirty with arg False\n"
                "called StatusBar.showMessage with arg `text undone`\n")
        testobj.first_edit = False
        testobj.undo()
        assert capsys.readouterr().out == (
                "called CopyAttributeCommand with args"
                f" ({testobj.win}, True) {{'cut': True, 'retain': False,"
                " 'description': 'PyQT5 versie van een op een treeview gebaseerde XML-editor\\n'}\n"
                "called CopyAttributeCommand.redo\n"
                "called StatusBar.showMessage with arg `text undone`\n")


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
        testobj.win = MockGui()
        testobj.win.tree = MockTree()
        assert capsys.readouterr().out == ('called EditCommand.__init__ with args ()\n'
                                           "called Gui.__init__\n"
                                           "called Editor.__init__\n"
                                           "called Tree.__init__\n")
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for EditCommand.__init__
        """
        win = MockGui()
        win.editor.tree_dirty = False
        assert capsys.readouterr().out == "called Gui.__init__\ncalled Editor.__init__\n"
        win.item = 'xxx'
        monkeypatch.setattr(testee.qtw.QUndoCommand, '__init__', mockqtw.MockUndoCommand)
        testobj = testee.EditCommand(win, 'old_state', 'new_state')
        assert testobj.win == win
        assert testobj.item == 'xxx'
        assert testobj.old_state == 'old_state'
        assert testobj.new_state == 'new_state'
        assert testobj.first_edit
        assert capsys.readouterr().out == "called UndoCommand.__init__ with args ('',) {}\n"
        win.editor.tree_dirty = True
        testobj = testee.EditCommand(win, 'old_state', 'new_state', 'yyyyy')
        assert testobj.win == win
        assert testobj.item == 'xxx'
        assert testobj.old_state == 'old_state'
        assert testobj.new_state == 'new_state'
        assert not testobj.first_edit
        assert capsys.readouterr().out == "called UndoCommand.__init__ with args ('yyyyy',) {}\n"

    def test_redo(self, monkeypatch, capsys):
        """unittest for EditCommand.redo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.old_state = ('xo', 'yo', 'zo')
        testobj.new_state = ('xn', 'yn', 'zn')
        testobj.redo()
        assert capsys.readouterr().out == ("called TreeItem.setText with arg `xn` for col 0\n"
                                           "called TreeItem.setText with arg `yn` for col 1\n"
                                           "called TreeItem.setText with arg `zn` for col 2\n")

    def test_undo(self, monkeypatch, capsys):
        """unittest for EditCommand.undo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.item = mockqtw.MockTreeItem()
        testobj.win.statusbar = mockqtw.MockStatusBar()
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called StatusBar.__init__ with args ()\n")
        testobj.text = lambda *x: 'text'
        testobj.old_state = ('xo', 'yo', 'zo')
        testobj.new_state = ('xn', 'yn', 'zn')
        testobj.first_edit = True
        testobj.undo()
        assert capsys.readouterr().out == ("called TreeItem.setText with arg `xo` for col 0\n"
                                           "called TreeItem.setText with arg `yo` for col 1\n"
                                           "called TreeItem.setText with arg `zo` for col 2\n"
                                           "called Editor.mark_dirty with arg False\n"
                                           "called StatusBar.showMessage with arg `text undone`\n")

        testobj.first_edit = False
        testobj.undo()
        assert capsys.readouterr().out == ("called TreeItem.setText with arg `xo` for col 0\n"
                                           "called TreeItem.setText with arg `yo` for col 1\n"
                                           "called TreeItem.setText with arg `zo` for col 2\n"
                                           "called StatusBar.showMessage with arg `text undone`\n")


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
        testobj.win = MockGui()
        testobj.win.tree = MockTree()
        assert capsys.readouterr().out == ('called CopyElementCommand.__init__ with args ()\n'
                                           "called Gui.__init__\n"
                                           "called Editor.__init__\n"
                                           "called Tree.__init__\n")
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for CopyElementCommand.__init__
        """
        win = MockGui()
        win.editor.tree_dirty = False
        item = mockqtw.MockTreeItem('xx', 'a tag', 'a text')
        assert capsys.readouterr().out == (
                "called Gui.__init__\ncalled Editor.__init__\n"
                "called TreeItem.__init__ with args ('xx', 'a tag', 'a text')\n")
        monkeypatch.setattr(testee.qtw.QUndoCommand, '__init__', mockqtw.MockUndoCommand)
        testobj = testee.CopyElementCommand(win, item, True, False)
        assert testobj.undodata is None
        assert testobj.win == win
        assert testobj.item == item
        assert testobj.tag == 'a tag'
        assert testobj.data == 'a text'
        assert testobj.cut
        assert not testobj.retain
        assert testobj.first_edit
        assert capsys.readouterr().out == ("called UndoCommand.__init__ with args ('',) {}\n"
                                           "called TreeItem.text for col 1\n"
                                           "called TreeItem.text for col 2\n")
        testobj = testee.CopyElementCommand(win, item, True, False, 'desc')
        assert testobj.undodata is None
        assert testobj.win == win
        assert testobj.item == item
        assert testobj.tag == 'a tag'
        assert testobj.data == 'a text'
        assert testobj.cut
        assert not testobj.retain
        assert testobj.first_edit
        assert capsys.readouterr().out == ("called UndoCommand.__init__ with args ('desc',) {}\n"
                                           "called TreeItem.text for col 1\n"
                                           "called TreeItem.text for col 2\n")

    def test_redo(self, monkeypatch, capsys):
        """unittest for CopyElementCommand.redo
        """
        testitem = mockqtw.MockTreeItem('xxx', 'yyy', 'zzz')
        testchild1 = mockqtw.MockTreeItem('c1', 'child', 'one')
        testitem.addChild(testchild1)
        testchild2 = mockqtw.MockTreeItem('c2', 'child', 'two')
        testitem.addChild(testchild2)
        testparent = mockqtw.MockTreeItem('p0', 'parent', 'zero')
        previtem = mockqtw.MockTreeItem()
        testparent.addChild(previtem)
        testparent.addChild(testitem)
        nextitem = mockqtw.MockTreeItem()
        testparent.addChild(nextitem)
        assert capsys.readouterr().out == (
                "called TreeItem.__init__ with args ('xxx', 'yyy', 'zzz')\n"
                "called TreeItem.__init__ with args ('c1', 'child', 'one')\n"
                "called TreeItem.addChild\n"
                "called TreeItem.__init__ with args ('c2', 'child', 'two')\n"
                "called TreeItem.addChild\n"
                "called TreeItem.__init__ with args ('p0', 'parent', 'zero')\n"
                "called TreeItem.__init__ with args ()\n"
                "called TreeItem.addChild\n"
                "called TreeItem.addChild\n"
                "called TreeItem.__init__ with args ()\n"
                "called TreeItem.addChild\n")

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.item = testitem
        # testobj.prev = ''
        testobj.win.cut_el = None
        testobj.win.cut_att = None
        testobj.undodata = None
        testobj.retain = False
        testobj.cut = False
        testobj.win.editor = types.SimpleNamespace(rt='not testparent')
        testobj.redo()
        assert testobj.parent == testparent
        assert testobj.loc == 1
        assert testobj.undodata == [('xxx', ('yyy', 'zzz'), [('c1', ('child', 'one'), []),
                                                             ('c2', ('child', 'two'), [])])]
        assert testobj.prev == previtem
        assert capsys.readouterr().out == ("called TreeItem.parent\n"
                                           "called TreeItem.text for col 0\n"
                                           "called TreeItem.text for col 1\n"
                                           "called TreeItem.text for col 2\n"
                                           "called TreeItem.child with arg 0\n"
                                           "called TreeItem.text for col 0\n"
                                           "called TreeItem.text for col 1\n"
                                           "called TreeItem.text for col 2\n"
                                           "called TreeItem.child with arg 1\n"
                                           "called TreeItem.text for col 0\n"
                                           "called TreeItem.text for col 1\n"
                                           "called TreeItem.text for col 2\n"
                                           "called TreeItem.child with arg 0\n")
        testparent = mockqtw.MockTreeItem('p0', 'parent', 'zero')
        testparent.addChild(testitem)
        testparent.addChild(nextitem)
        assert capsys.readouterr().out == (
                "called TreeItem.__init__ with args ('p0', 'parent', 'zero')\n"
                "called TreeItem.addChild\n"
                "called TreeItem.addChild\n")
        testobj.parent = None
        testobj.loc = None
        testobj.undodata = None
        testobj.prev = None
        testobj.redo()
        assert testobj.parent == testparent
        assert testobj.loc == 0
        assert testobj.undodata == [('xxx', ('yyy', 'zzz'), [('c1', ('child', 'one'), []),
                                                             ('c2', ('child', 'two'), [])])]
        assert testobj.prev == testparent
        assert capsys.readouterr().out == ("called TreeItem.parent\n"
                                           "called TreeItem.text for col 0\n"
                                           "called TreeItem.text for col 1\n"
                                           "called TreeItem.text for col 2\n"
                                           "called TreeItem.child with arg 0\n"
                                           "called TreeItem.text for col 0\n"
                                           "called TreeItem.text for col 1\n"
                                           "called TreeItem.text for col 2\n"
                                           "called TreeItem.child with arg 1\n"
                                           "called TreeItem.text for col 0\n"
                                           "called TreeItem.text for col 1\n"
                                           "called TreeItem.text for col 2\n")
        testobj.win.editor = types.SimpleNamespace(rt=testparent)
        testobj.parent = None
        testobj.loc = None
        testobj.undodata = None
        testobj.prev = None
        # breakpoint()
        testobj.redo()
        assert testobj.parent == testparent
        assert testobj.loc == 0
        assert testobj.undodata == [('xxx', ('yyy', 'zzz'), [('c1', ('child', 'one'), []),
                                                             ('c2', ('child', 'two'), [])])]
        assert testobj.prev == nextitem
        assert capsys.readouterr().out == ("called TreeItem.parent\n"
                                           "called TreeItem.text for col 0\n"
                                           "called TreeItem.text for col 1\n"
                                           "called TreeItem.text for col 2\n"
                                           "called TreeItem.child with arg 0\n"
                                           "called TreeItem.text for col 0\n"
                                           "called TreeItem.text for col 1\n"
                                           "called TreeItem.text for col 2\n"
                                           "called TreeItem.child with arg 1\n"
                                           "called TreeItem.text for col 0\n"
                                           "called TreeItem.text for col 1\n"
                                           "called TreeItem.text for col 2\n"
                                           "called TreeItem.child with arg 1\n")

        testobj.retain = True
        testobj.redo()
        assert testobj.win.cut_el == [('xxx', ('yyy', 'zzz'), [('c1', ('child', 'one'), []),
                                                               ('c2', ('child', 'two'), [])])]
        assert testobj.win.cut_att is None
        assert capsys.readouterr().out == "called Gui.enable_pasteitems with arg True\n"

        testobj.retain = False
        testobj.cut = True
        testobj.redo()
        assert testobj.item == testobj.prev
        assert capsys.readouterr().out == ("called TreeItem.removeChild\n"
                                           f"called Tree.setCurrentItem with arg {testobj.prev}\n")

    def test_undo(self, monkeypatch, capsys):
        """unittest for CopyElementCommand.undo
        """
        class MockPaste:
            def __init__(self, *args, **kwargs):
                print('called PasteElementCommand with args', args, kwargs)
                self.added = 'added item'
            def redo(self):
                print('called PasteElementCommand.redo')
        monkeypatch.setattr(testee, 'PasteElementCommand', MockPaste)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = mockqtw.MockTreeItem()
        testobj.win.statusbar = mockqtw.MockStatusBar()
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called StatusBar.__init__ with args ()\n")
        testobj.text = lambda *x: 'text'
        testobj.cut = False
        testobj.first_edit = True
        testobj.undo()
        assert capsys.readouterr().out == ("called Editor.mark_dirty with arg False\n"
                                           "called StatusBar.showMessage with arg `text undone`\n")
        testobj.tag = 'tag'
        testobj.data = 'data'
        testobj.undodata = 'undodata'

        testobj.cut = True
        testobj.loc = 2
        testobj.parent.addChild('xx')
        # testobj.parent.childCount = lambda *x: 1
        assert capsys.readouterr().out == "called TreeItem.addChild\n"
        testobj.undo()
        assert testobj.item == 'added item'
        assert capsys.readouterr().out == (
                f"called PasteElementCommand with args ({testobj.win}, 'tag', 'data')"
                " {'before': False, 'below': True, 'data': 'undodata',"
                " 'description': 'PyQT5 versie van een op een treeview gebaseerde XML-editor\\n',"
                f" 'where': {testobj.parent}}}\n"
                "called PasteElementCommand.redo\n"
                "called Editor.mark_dirty with arg False\n"
                "called StatusBar.showMessage with arg `text undone`\n")

        testobj.loc = 1
        # testobj.parent.addChild('xx')
        testobj.parent.addChild('yy')
        # testobj.parent.childCount = lambda *x: 2
        assert capsys.readouterr().out == "called TreeItem.addChild\n"
        testobj.undo()
        assert testobj.item == 'added item'
        assert capsys.readouterr().out == (
                "called TreeItem.child with arg 1\n"
                f"called PasteElementCommand with args ({testobj.win}, 'tag', 'data')"
                " {'before': True, 'below': False, 'data': 'undodata',"
                " 'description': 'PyQT5 versie van een op een treeview gebaseerde XML-editor\\n',"
                " 'where': 'yy'}\n"
                "called PasteElementCommand.redo\n"
                "called Editor.mark_dirty with arg False\n"
                "called StatusBar.showMessage with arg `text undone`\n")


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
        testobj.win = MockGui()
        testobj.win.tree = MockTree()
        assert capsys.readouterr().out == ('called CopyAttributeCommand.__init__ with args ()\n'
                                           "called Gui.__init__\n"
                                           "called Editor.__init__\n"
                                           "called Tree.__init__\n")
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for CopyAttributeCommand.__init__
        """
        win = MockGui()
        win.editor.tree_dirty = False
        item = mockqtw.MockTreeItem('xx', 'a name', 'a value')
        assert capsys.readouterr().out == (
                "called Gui.__init__\ncalled Editor.__init__\n"
                "called TreeItem.__init__ with args ('xx', 'a name', 'a value')\n")
        monkeypatch.setattr(testee.qtw.QUndoCommand, '__init__', mockqtw.MockUndoCommand)
        testobj = testee.CopyAttributeCommand(win, item, True, False, 'desc')
        assert testobj.win == win
        assert testobj.item == item
        assert testobj.name == 'a name'
        assert testobj.value == 'a value'
        assert testobj.cut
        assert not testobj.retain
        assert testobj.first_edit
        assert capsys.readouterr().out == ("called UndoCommand.__init__ with args ('desc',) {}\n"
                                           "called TreeItem.text for col 1\n"
                                           "called TreeItem.text for col 2\n")

    def test_redo(self, monkeypatch, capsys):
        """unittest for CopyAttributeCommand.redo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        root = mockqtw.MockTreeItem()
        parent = mockqtw.MockTreeItem()
        item = mockqtw.MockTreeItem()
        parent.addChild(item)
        item2 = mockqtw.MockTreeItem()
        parent.addChild(item2)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.addChild\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.addChild\n")
        testobj.item = item
        testobj.name = 'a name'
        testobj.value = 'a value'
        testobj.retain = True
        testobj.cut = False
        testobj.redo()
        assert testobj.parent == parent
        assert testobj.loc == 0
        assert capsys.readouterr().out == ("called TreeItem.parent\n"
                                           "called Gui.enable_pasteitems with arg True\n")
        testobj.retain = False
        testobj.cut = True
        testobj.win.editor.rt = root
        testobj.redo()
        assert capsys.readouterr().out == ("called TreeItem.parent\n"
                                           "called TreeItem.removeChild\n"
                                           f"called Tree.setCurrentItem with arg {parent}\n")

        testobj.item = item
        testobj.retain = False
        testobj.cut = True
        testobj.win.editor.rt = parent
        testobj.redo()
        assert capsys.readouterr().out == ("called TreeItem.parent\n"
                                           "called TreeItem.child with arg 1\n"
                                           "called TreeItem.removeChild\n"
                                           f"called Tree.setCurrentItem with arg {item2}\n")
        testobj.item = item2
        testobj.retain = False
        testobj.cut = True
        testobj.win.editor.rt = parent
        testobj.redo()
        assert capsys.readouterr().out == ("called TreeItem.parent\n"
                                           "called TreeItem.child with arg 0\n"
                                           "called TreeItem.removeChild\n"
                                           f"called Tree.setCurrentItem with arg {item}\n")

    def test_undo(self, monkeypatch, capsys):
        """unittest for CopyAttributeCommand.undo
        """
        class MockPaste:
            def __init__(self, *args, **kwargs):
                print('called PasteAttributeCommand with args', args, kwargs)
                self.added = 'added item'
            def redo(self):
                print('called PasteAttributeCommand.redo')
        monkeypatch.setattr(testee, 'PasteAttributeCommand', MockPaste)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.item = mockqtw.MockTreeItem()
        testobj.parent = mockqtw.MockTreeItem()
        testobj.win.statusbar = mockqtw.MockStatusBar()
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called StatusBar.__init__ with args ()\n")
        testobj.text = lambda *x: 'text'
        testobj.cut = False
        testobj.first_edit = True
        testobj.undo()
        assert capsys.readouterr().out == ("called Editor.mark_dirty with arg False\n"
                                           "called StatusBar.showMessage with arg `text undone`\n")
        testobj.name = 'name'
        testobj.value = 'value'
        testobj.undodata = 'undodata'

        testobj.cut = True
        testobj.loc = 2
        testobj.parent.addChild('xx')
        # testobj.parent.childCount = lambda *x: 1
        assert capsys.readouterr().out == "called TreeItem.addChild\n"
        testobj.undo()
        assert testobj.item == 'added item'
        assert capsys.readouterr().out == (
                f"called PasteAttributeCommand with args ({testobj.win}, 'name', 'value',"
                f" {testobj.parent})"
                " {'description': 'PyQT5 versie van een op een treeview gebaseerde XML-editor\\n'}\n"
                "called PasteAttributeCommand.redo\n"
                "called Editor.mark_dirty with arg False\n"
                "called StatusBar.showMessage with arg `text undone`\n")


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
        testobj.app = mockqtw.MockApplication()
        testobj.editor = MockEditor()
        testobj.tree = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == ('called Gui.__init__ with args ()\n'
                                           "called Application.__init__\n"
                                           "called Editor.__init__\n"
                                           "called Tree.__init__\n")
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for Gui.__init__
        """
        def mock_init(self, *args, **kwargs):
            print('called MainWindow.__init__ with args', args, kwargs)
        monkeypatch.setattr(testee.qtw.QApplication, '__init__', mockqtw.MockApplication.__init__)
        monkeypatch.setattr(testee.qtw.QMainWindow, '__init__', mock_init)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'show', mockqtw.MockMainWindow.show)
        testobj = testee.Gui()
        assert testobj.editor is None
        assert isinstance(testobj.app, testee.qtw.QApplication)
        assert testobj.fn == ''
        assert testobj.editable
        assert capsys.readouterr().out == ("called Application.__init__\n"
                                           "called MainWindow.__init__ with args () {}\n"
                                           "called MainWindow.show\n")
        testobj = testee.Gui('parent', 'fname', True)
        assert testobj.editor == 'parent'
        assert isinstance(testobj.app, testee.qtw.QApplication)
        assert testobj.fn == 'fname'
        assert not testobj.editable
        assert capsys.readouterr().out == ("called Application.__init__\n"
                                           "called MainWindow.__init__ with args () {}\n"
                                           "called MainWindow.show\n")

    def test_go(self, monkeypatch, capsys):
        """unittest for Gui.go
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        with pytest.raises(SystemExit):
            testobj.go()
        assert capsys.readouterr().out == ("called Application.exec_\n")

    def test_keyReleaseEvent(self, monkeypatch, capsys):
        """unittest for Gui.keyReleaseEvent
        """
        def mock_event(self, arg):
            print(f'called MainWindow.keyReleaseEvent with arg {arg}')
        def mock_onkey(arg):
            print(f'called Gui.on_keyup with arg {arg}')
            return False
        def mock_onkey_2(arg):
            print(f'called Gui.on_keyup with arg {arg}')
            return True
        monkeypatch.setattr(testee.qtw.QMainWindow, 'keyReleaseEvent', mock_event)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.on_keyup = mock_onkey
        testobj.keyReleaseEvent('event')
        assert capsys.readouterr().out == ("called Gui.on_keyup with arg event\n"
                                           "called MainWindow.keyReleaseEvent with arg event\n")
        testobj.on_keyup = mock_onkey_2
        testobj.keyReleaseEvent('event')
        assert capsys.readouterr().out == "called Gui.on_keyup with arg event\n"

    def test_closeEvent(self, monkeypatch, capsys):
        """unittest for Gui.closeEvent
        """
        def mock_check():
            print('called Gui.check_tree')
            return True
        def mock_check_2():
            print('called Gui.check_tree')
            return False
        testobj = self.setup_testobj(monkeypatch, capsys)
        event = mockqtw.MockEvent()
        testobj.editor.check_tree = mock_check
        testobj.closeEvent(event)
        assert capsys.readouterr().out == "called Gui.check_tree\ncalled event.accept\n"
        testobj.editor.check_tree = mock_check_2
        testobj.closeEvent(event)
        assert capsys.readouterr().out == "called Gui.check_tree\ncalled event.ignore\n"

    def test_get_node_children(self, monkeypatch, capsys):
        """unittest for Gui.get_node_children
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        node = mockqtw.MockTreeItem()
        item1 = mockqtw.MockTreeItem()
        item2 = mockqtw.MockTreeItem()
        node.addChild(item1)
        node.addChild(item2)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.addChild\ncalled TreeItem.addChild\n")
        assert testobj.get_node_children(node) == [item1, item2]

    def test_get_node_title(self, monkeypatch, capsys):
        """unittest for Gui.get_node_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        node = mockqtw.MockTreeItem('title')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('title',)\n"
        assert testobj.get_node_title(node) == "title"
        assert capsys.readouterr().out == "called TreeItem.text for col 0\n"

    def test_get_node_data(self, monkeypatch, capsys):
        """unittest for Gui.get_node_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        node = mockqtw.MockTreeItem('title', 'text', 'data')
        assert capsys.readouterr().out == (
                "called TreeItem.__init__ with args ('title', 'text', 'data')\n")
        assert testobj.get_node_data(node) == ('text', 'data')
        assert capsys.readouterr().out == ("called TreeItem.text for col 1\n"
                                           "called TreeItem.text for col 2\n")

    def test_get_treetop(self, monkeypatch, capsys):
        """unittest for Gui.get_treetop
        """
        item = mockqtw.MockTreeItem()
        item2 = mockqtw.MockTreeItem('x')
        item.addChild(item2)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ('x',)\n"
                                           "called TreeItem.addChild\n")
        def mock_item(arg):
            print(f'called Tree.topLevelItem with arg `{arg}`')
            return item
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree.topLevelItem = mock_item
        assert testobj.get_treetop() == item2
        assert capsys.readouterr().out == ("called Tree.topLevelItem with arg `0`\n"
                                           "called TreeItem.child with arg 0\n"
                                           "called TreeItem.text for col 0\n")

        item.insertChild(0, mockqtw.MockTreeItem('namespaces'))
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ('namespaces',)\n"
                                           "called TreeItem.insertChild at pos 0\n")
        def mock_item(arg):
            print(f'called Tree.topLevelItem with arg `{arg}`')
            return item
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree.topLevelItem = mock_item
        assert testobj.get_treetop() == item2
        assert capsys.readouterr().out == ("called Tree.topLevelItem with arg `0`\n"
                                           "called TreeItem.child with arg 0\n"
                                           "called TreeItem.text for col 0\n"
                                           "called TreeItem.child with arg 1\n")

    def test_setup_new_tree(self, monkeypatch, capsys):
        """unittest for Gui.setup_new_tree
        """
        monkeypatch.setattr(testee.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.undo_stack = mockqtw.MockUndoStack()
        assert capsys.readouterr().out == "called UndoStack.__init__ with args ()\n"
        testobj.editable = False
        assert isinstance(testobj.setup_new_tree('Title'), testee.qtw.QTreeWidgetItem)
        assert capsys.readouterr().out == ("called Tree.clear\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.setText with arg `Title` for col 0\n"
                                           "called Tree.addTopLevelItem\n")
        testobj.editable = True
        assert isinstance(testobj.setup_new_tree('Title'), testee.qtw.QTreeWidgetItem)
        assert capsys.readouterr().out == ("called Tree.clear\n"
                                           "called UndoRedoStack.clear\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.setText with arg `Title` for col 0\n"
                                           "called Tree.addTopLevelItem\n")

    def test_add_node_to_parent(self, monkeypatch, capsys):
        """unittest for Gui.add_node_to_parent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        parent = mock_and_create_nodes(monkeypatch, capsys, 1)[0]
        assert isinstance(testobj.add_node_to_parent(parent), testee.qtw.QTreeWidgetItem)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.addChild\n")
        assert isinstance(testobj.add_node_to_parent(parent, pos=1), testee.qtw.QTreeWidgetItem)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.insertChild at pos 1\n")

    def test_set_node_title(self, monkeypatch, capsys):
        """unittest for Gui.set_node_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        node = mock_and_create_nodes(monkeypatch, capsys, 1)[0]
        testobj.set_node_title(node, 'Title')
        assert capsys.readouterr().out == "called TreeItem.setText with arg `Title` for col 0\n"

    def test_get_node_parentpos(self, monkeypatch, capsys):
        """unittest for Gui.get_node_parentpos
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        parent, node = mock_and_create_nodes(monkeypatch, capsys, 2)
        parent.addChild(node)
        assert capsys.readouterr().out == "called TreeItem.addChild\n"
        assert testobj.get_node_parentpos(node) == (parent, 0)
        assert capsys.readouterr().out == "called TreeItem.parent\n"

    def test_set_node_data(self, monkeypatch, capsys):
        """unittest for Gui.set_node_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        node = mock_and_create_nodes(monkeypatch, capsys, 1)[0]
        testobj.set_node_data(node, 'Name', 'Value')
        assert capsys.readouterr().out == ("called TreeItem.setText with arg `Name` for col 1\n""called TreeItem.setText with arg `Value` for col 2\n")

    def test_get_selected_item(self, monkeypatch, capsys):
        """unittest for Gui.get_selected_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_selected_item() == "called Tree.currentItem"
        assert capsys.readouterr().out == ""

    def test_set_selected_item(self, monkeypatch, capsys):
        """unittest for Gui.set_selected_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        item = mock_and_create_nodes(monkeypatch, capsys, 1)[0]
        testobj.set_selected_item(item)
        assert capsys.readouterr().out == (f"called Tree.setCurrentItem with arg `{item}`\n")

    def test_is_node_root(self, monkeypatch, capsys):
        """unittest for Gui.is_node_root
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        node = mockqtw.MockTreeItem('', 'xxx', 'yyy')
        testobj.item = mockqtw.MockTreeItem('', 'aaa', '')
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ('', 'xxx', 'yyy')\n"
                                           "called TreeItem.__init__ with args ('', 'aaa', '')\n")
        testobj.editor.rt = types.SimpleNamespace(tag='aaa', text=None)
        assert testobj.is_node_root()
        assert capsys.readouterr().out == ("called TreeItem.text for col 1\n"
                                           "called TreeItem.text for col 2\n")
        assert not testobj.is_node_root(node)
        assert capsys.readouterr().out == ("called TreeItem.text for col 1\n"
                                           "called TreeItem.text for col 2\n")

    def test_expand_item(self, monkeypatch, capsys):
        """unittest for Gui.expand_item
        """
        def mock_current():
            print('called Tree.currentItem')
            return None
        def mock_expand(item):
            print(f'called Tree.expandItem with arg {item}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree.currentItem = mock_current
        # testobj.tree.expandItem = mock_expand
        testobj.expand_item()
        assert capsys.readouterr().out == ("called Tree.currentItem\n")

        item = mockqtw.MockTreeItem(['x'])
        item2 = mockqtw.MockTreeItem(['y'])
        item.addChild(item2)
        item3 = mockqtw.MockTreeItem(['z'])
        item.addChild(item3)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args (['x'],)\n"
                                           "called TreeItem.__init__ with args (['y'],)\n"
                                           "called TreeItem.addChild\n"
                                           "called TreeItem.__init__ with args (['z'],)\n"
                                           "called TreeItem.addChild\n")
        testobj.expand_item(item)
        assert capsys.readouterr().out == (f"called Tree.expandItem with arg {item}\n"
                                           "called TreeItem.child with arg 0\n"
                                           f"called Tree.expandItem with arg {item2}\n"
                                           "called TreeItem.child with arg 1\n"
                                           f"called Tree.expandItem with arg {item3}\n"
                                           "called Tree.resizeColumnToContents with arg 0\n")

    def test_collapse_item(self, monkeypatch, capsys):
        """unittest for Gui.collapse_item
        """
        def mock_current():
            print('called Tree.currentItem')
            return None
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree.currentItem = mock_current
        testobj.collapse_item()
        assert capsys.readouterr().out == "called Tree.currentItem\n"
        testobj.collapse_item('yyy')
        assert capsys.readouterr().out == ("called Tree.collapseItem with arg yyy\n"
                                           "called Tree.resizeColumnToContents with arg 0\n")

    def test_edit_item(self, monkeypatch, capsys):
        """unittest for Gui.edit_item
        """
        class MockEleDialog:
            def __init__(self, *args, **kwargs):
                print('called ElementDialog with args', args, kwargs)
            def exec_(self):
                print('called ElementDialog.exec_')
                return testee.qtw.QDialog.Rejected
        class MockEleDialog2:
            def __init__(self, *args, **kwargs):
                print('called ElementDialog with args', args, kwargs)
            def exec_(self):
                print('called ElementDialog.exec_')
                return testee.qtw.QDialog.Accepted
        class MockAttrDialog:
            def __init__(self, *args, **kwargs):
                print('called AttributeDialog with args', args, kwargs)
            def exec_(self):
                print('called AttributeDialog.exec_')
                return testee.qtw.QDialog.Rejected
        class MockAttrDialog2:
            def __init__(self, *args, **kwargs):
                print('called AttributeDialog with args', args, kwargs)
            def exec_(self):
                print('called AttributeDialog.exec_')
                return testee.qtw.QDialog.Accepted
        class MockEditCmd:
            def __init__(self, *args, **kwargs):
                print('called EditCommand.__init__ with args', args, kwargs)
        monkeypatch.setattr(testee, 'ElementDialog', MockEleDialog)
        monkeypatch.setattr(testee, 'AttributeDialog', MockAttrDialog)
        monkeypatch.setattr(testee, 'EditCommand', MockEditCmd)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor.elstart = '<>'
        testelement = mockqtw.MockTreeItem('<> xxx', 'yyy', 'zzz')
        testattribute = mockqtw.MockTreeItem('xxx', 'yyy', 'zzz')
        testobj.undo_stack = mockqtw.MockUndoStack()
        assert capsys.readouterr().out == (
                "called TreeItem.__init__ with args ('<> xxx', 'yyy', 'zzz')\n"
                "called TreeItem.__init__ with args ('xxx', 'yyy', 'zzz')\n"
                "called UndoStack.__init__ with args ()\n")
        testobj.edit_item(testelement)
        assert capsys.readouterr().out == (
                "called TreeItem.text for col 0\n"
                "called TreeItem.text for col 1\n"
                "called TreeItem.text for col 2\n"
                f"called ElementDialog with args ({testobj},) {{'title': 'Edit an element',"
                f" 'item': {{'item': {testelement}, 'tag': 'yyy', 'data': True, 'text': 'zzz'}}}}\n"
                "called ElementDialog.exec_\n")
        monkeypatch.setattr(testee, 'ElementDialog', MockEleDialog2)
        testobj.data = {'tag': 'Tag', 'text': 'Text'}
        testobj.edit_item(testelement)
        assert capsys.readouterr().out == (
                "called TreeItem.text for col 0\n"
                "called TreeItem.text for col 1\n"
                "called TreeItem.text for col 2\n"
                f"called ElementDialog with args ({testobj},) {{'title': 'Edit an element',"
                f" 'item': {{'item': {testelement}, 'tag': 'yyy', 'data': True, 'text': 'zzz'}}}}\n"
                "called ElementDialog.exec_\n"
                "called Editor.getshortname with args (('Tag', 'Text'),) {}\n"
                f"called EditCommand.__init__ with args ({testobj},"
                " ('<> xxx', 'yyy', 'zzz'), ('shortname', 'Tag', 'Text'), 'Edit Element') {}\n"
                "called UndoRedoStack.push\n"
                "called Editor.mark_dirty with arg True\n")
        testobj.edit_item(testattribute)
        assert capsys.readouterr().out == (
                "called TreeItem.text for col 0\n"
                "called TreeItem.text for col 1\n"
                "called TreeItem.text for col 2\n"
                f"called AttributeDialog with args ({testobj},) {{'title': 'Edit an attribute',"
                f" 'item': {{'item': {testattribute}, 'name': 'yyy', 'value': 'zzz'}}}}\n"
                "called AttributeDialog.exec_\n")
        monkeypatch.setattr(testee, 'AttributeDialog', MockAttrDialog2)
        testobj.data = {'name': 'Name', 'value': 'Value'}
        testobj.edit_item(testattribute)
        assert capsys.readouterr().out == (
                "called TreeItem.text for col 0\n"
                "called TreeItem.text for col 1\n"
                "called TreeItem.text for col 2\n"
                f"called AttributeDialog with args ({testobj},) {{'title': 'Edit an attribute',"
                f" 'item': {{'item': {testattribute}, 'name': 'yyy', 'value': 'zzz'}}}}\n"
                "called AttributeDialog.exec_\n"
                "called Editor.getshortname with args (('Name', 'Value'),) {'attr': True}\n"
                f"called EditCommand.__init__ with args ({testobj}, ('xxx', 'yyy', 'zzz'),"
                " ('shortname', 'Name', 'Value'), 'Edit Attribute') {}\n"
                "called UndoRedoStack.push\n"
                "called Editor.mark_dirty with arg True\n")

    def test_copy(self, monkeypatch, capsys):
        """unittest for Gui.copy
        """
        class MockCopyEl:
            def __init__(self, *args):
                print('called CopyElementCommand.__init__ with args', args)
        class MockCopyAtt:
            def __init__(self, *args):
                print('called CopyAttributeCommand.__init__ with args', args)
        monkeypatch.setattr(testee, 'CopyElementCommand', MockCopyEl)
        monkeypatch.setattr(testee, 'CopyAttributeCommand', MockCopyAtt)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.undo_stack = mockqtw.MockUndoStack()
        assert capsys.readouterr().out == "called UndoStack.__init__ with args ()\n"
        testobj.editor.elstart = '<>'
        item = mockqtw.MockTreeItem('<> x')
        testobj.copy(item)
        assert capsys.readouterr().out == (
                "called TreeItem.__init__ with args ('<> x',)\n"
                "called Editor.get_copy_text with args (False, True)\n"
                "called TreeItem.text for col 0\n"
                "called CopyElementCommand.__init__ with args"
                f" ({testobj}, {item}, False, True, 'copy Element')\n"
                "called UndoRedoStack.push\n")
        item = mockqtw.MockTreeItem('x')
        testobj.copy(item, True, False)
        assert capsys.readouterr().out == (
                "called TreeItem.__init__ with args ('x',)\n"
                "called Editor.get_copy_text with args (True, False)\n"
                "called TreeItem.text for col 0\n"
                "called CopyAttributeCommand.__init__ with args"
                f" ({testobj}, {item}, True, False, 'copy Attribute')\n"
                "called UndoRedoStack.push\n"
                "called Editor.mark_dirty with arg True\n")

    def test_paste(self, monkeypatch, capsys):
        """unittest for Gui.paste
        """
        class MockPasteEl:
            def __init__(self, *args, **kwargs):
                print('called PasteElementCommand.__init__ with args', args, kwargs)
        class MockPasteAtt:
            def __init__(self, *args, **kwargs):
                print('called PasteAttributeCommand.__init__ with args', args, kwargs)
        monkeypatch.setattr(testee, 'PasteElementCommand', MockPasteEl)
        monkeypatch.setattr(testee, 'PasteAttributeCommand', MockPasteAtt)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.undo_stack = mockqtw.MockUndoStack()
        assert capsys.readouterr().out == "called UndoStack.__init__ with args ()\n"
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.cut_att = ('Name', 'Value')
        testobj.cut_el = (('', ('Tag', 'Text')),)
        testobj.paste(item)
        assert testobj.item == item
        assert capsys.readouterr().out == (
                f"called PasteAttributeCommand.__init__ with args ({testobj}, 'Name', 'Value',"
                f" {item}) {{'description': 'Paste Attribute'}}\n"
                "called UndoRedoStack.push\n"
                "called Editor.mark_dirty with arg True\n")
        testobj.cut_att = ()
        testobj.paste(item)
        assert testobj.item == item
        assert capsys.readouterr().out == (
                f"called PasteElementCommand.__init__ with args ({testobj}, 'Tag', 'Text')"
                f" {{'before': True, 'below': False, 'where': {item},"
                " 'description': 'Paste Element', 'data': (('', ('Tag', 'Text')),)}\n"
                "called UndoRedoStack.push\n"
                "called Editor.mark_dirty with arg True\n")
        testobj.paste(item, False, True)
        assert testobj.item == item
        assert capsys.readouterr().out == (
                f"called PasteElementCommand.__init__ with args ({testobj}, 'Tag', 'Text')"
                f" {{'before': False, 'below': True, 'where': {item},"
                " 'description': 'Paste Element', 'data': (('', ('Tag', 'Text')),)}\n"
                "called UndoRedoStack.push\n"
                "called Editor.mark_dirty with arg True\n")

    def test_add_attribute(self, monkeypatch, capsys):
        """unittest for Gui.add_attribute
        """
        class MockAttrDialog:
            def __init__(self, *args, **kwargs):
                print('called AttributeDialog with args', args, kwargs)
            def exec_(self):
                print('called AttributeDialog.exec_')
                return testee.qtw.QDialog.Rejected
        class MockAttrDialog2:
            def __init__(self, *args, **kwargs):
                print('called AttributeDialog with args', args, kwargs)
            def exec_(self):
                print('called AttributeDialog.exec_')
                return testee.qtw.QDialog.Accepted
        class MockPasteAtt:
            def __init__(self, *args, **kwargs):
                print('called PasteAttributeCommand.__init__ with args', args, kwargs)
        monkeypatch.setattr(testee, 'AttributeDialog', MockAttrDialog)
        monkeypatch.setattr(testee, 'PasteAttributeCommand', MockPasteAtt)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.undo_stack = mockqtw.MockUndoStack()
        assert capsys.readouterr().out == "called UndoStack.__init__ with args ()\n"
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.add_attribute(item)
        assert capsys.readouterr().out == (
                f"called AttributeDialog with args ({testobj},) {{'title': 'New attribute'}}\n"
                "called AttributeDialog.exec_\n")
        monkeypatch.setattr(testee, 'AttributeDialog', MockAttrDialog2)
        testobj.data = {'name': 'Name', 'value': 'Value'}
        testobj.add_attribute(item)
        assert capsys.readouterr().out == (
                f"called AttributeDialog with args ({testobj},) {{'title': 'New attribute'}}\n"
                "called AttributeDialog.exec_\n"
                f"called PasteAttributeCommand.__init__ with args ({testobj}, 'Name', 'Value',"
                f" {item}, 'Insert Attribute') {{}}\n"
                "called UndoRedoStack.push\ncalled Editor.mark_dirty with arg True\n")

    def test_insert(self, monkeypatch, capsys):
        """unittest for Gui.insert
        """
        class MockEleDialog:
            def __init__(self, *args, **kwargs):
                print('called ElementDialog with args', args, kwargs)
            def exec_(self):
                print('called ElementDialog.exec_')
                return testee.qtw.QDialog.Rejected
        class MockEleDialog2:
            def __init__(self, *args, **kwargs):
                print('called ElementDialog with args', args, kwargs)
            def exec_(self):
                print('called ElementDialog.exec_')
                return testee.qtw.QDialog.Accepted
        class MockPasteEl:
            def __init__(self, *args, **kwargs):
                print('called PasteElementCommand.__init__ with args', args, kwargs)
        monkeypatch.setattr(testee, 'ElementDialog', MockEleDialog)
        monkeypatch.setattr(testee, 'PasteElementCommand', MockPasteEl)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.undo_stack = mockqtw.MockUndoStack()
        assert capsys.readouterr().out == "called UndoStack.__init__ with args ()\n"
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.insert(item, before=True, below=False)
        assert capsys.readouterr().out == (
                f"called ElementDialog with args ({testobj},) {{'title': 'New element'}}\n"
                "called ElementDialog.exec_\n")
        monkeypatch.setattr(testee, 'ElementDialog', MockEleDialog2)
        testobj.data = {'tag': 'Tag', 'text': 'Text'}
        testobj.insert(item, before=True, below=False)
        assert capsys.readouterr().out == (
                f"called ElementDialog with args ({testobj},) {{'title': 'New element'}}\n"
                "called ElementDialog.exec_\n"
                f"called PasteElementCommand.__init__ with args ({testobj}, 'Tag', 'Text')"
                f" {{'before': True, 'below': False, 'where': {item},"
                " 'description': 'Insert Element'}\n"
                "called UndoRedoStack.push\n"
                "called Editor.mark_dirty with arg True\n")

    def test_init_gui(self, monkeypatch, capsys, expected_output):
        """unittest for Gui.init_gui
        """
        def mock_init_menus():
            print('called Gui.init_menus')
        def mock_init_stack(self, parent):
            print(f'called UndoredoStack.__init__ with arg {parent}')
        def mock_enable(value):
            print(f'called Gui.enable_pasteitems with arg {value}')
        monkeypatch.setattr(testee.gui.QIcon, '__init__', mockqtw.MockIcon.__init__)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'resize', mockqtw.MockMainWindow.resize)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setWindowIcon',
                            mockqtw.MockMainWindow.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'statusBar', mockqtw.MockMainWindow.statusBar)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setCentralWidget',
                            mockqtw.MockMainWindow.setCentralWidget)
        # monkeypatch.setattr(testee.qtw, 'QTreeWidget', mockqtw.MockTreeWidget)
        monkeypatch.setattr(testee.qtw.QTreeWidget, '__init__', mockqtw.MockTreeWidget.__init__)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'headerItem', mockqtw.MockTreeWidget.headerItem)
        monkeypatch.setattr(testee.UndoRedoStack, '__init__', mock_init_stack)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor = MockEditor()
        assert capsys.readouterr().out == "called Editor.__init__\n"
        testobj.editor.iconame = 'icon-name'
        testobj.init_menus = mock_init_menus
        testobj.enable_pasteitems = mock_enable
        testobj.editable = False
        testobj.init_gui()
        assert isinstance(testobj.tree, testee.qtw.QTreeWidget)
        assert not testobj.in_dialog
        assert capsys.readouterr().out == expected_output['maingui']

        testobj.editable = True
        testobj.init_gui()
        assert isinstance(testobj.tree, testee.qtw.QTreeWidget)
        assert not testobj.in_dialog
        assert capsys.readouterr().out == expected_output['maingui2'].format(testobj=testobj)

    def test_set_windowtitle(self, monkeypatch, capsys):
        """unittest for Gui.set_windowtitle
        """
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setWindowTitle',
                            mockqtw.MockMainWindow.setWindowTitle)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_windowtitle('text')
        assert capsys.readouterr().out == "called MainWindow.setWindowTitle to `text`\n"

    def test_get_windowtitle(self, monkeypatch, capsys):
        """unittest for Gui.get_windowtitle
        """
        monkeypatch.setattr(testee.qtw.QMainWindow, 'windowTitle',
                            mockqtw.MockMainWindow.windowTitle)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_windowtitle() == "text"
        assert capsys.readouterr().out == "called MainWindow.windowTitle\n"

    def test_init_menus(self, monkeypatch, capsys):
        """unittest for Gui.init_menus
        """
        def mock_setup(self):
            print('called Gui.setup_menuactions')
            self.filemenu_actions = ['fm1', 'fm2', 'fm3', 'fm4', 'fm9']
            self.viewmenu_actions = ['vm1', 'vm2']
            self.editmenu_actions = ['em1', 'em2']
            self.searchmenu_actions = ['sm1', 'sm2']
            self.setundo_action = 'fm5'
        def mock_add(*args):
            print('called Gui.add_editactions')
            editmenu = mockqtw.MockMenu()
            return editmenu
        monkeypatch.setattr(testee.qtw, 'QMenu', mockqtw.MockMenu)

        monkeypatch.setattr(testee.Gui, 'setup_menuactions', mock_setup)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.menuBar = lambda: mockqtw.MockMenuBar()
        testobj.add_editactions = mock_add
        testobj.editable = False
        result = testobj.init_menus()
        assert len(result) == len(['File', 'View', 'Edit'])
        assert isinstance(result[0], testee.qtw.QMenu)
        assert isinstance(result[1], testee.qtw.QMenu)
        assert result[2] is None
        assert capsys.readouterr().out == ("called Gui.setup_menuactions\n"
                                           "called MenuBar.__init__\n"
                                           "called MenuBar.addMenu with arg  &File\n"
                                           "called Menu.__init__ with args ('&File',)\n"
                                           "called Menu.addAction with args `fm1` None\n"
                                           "called Action.__init__ with args ('fm1', None)\n"
                                           "called Menu.addAction with args `fm2` None\n"
                                           "called Action.__init__ with args ('fm2', None)\n"
                                           "called Menu.addAction with args `fm3` None\n"
                                           "called Action.__init__ with args ('fm3', None)\n"
                                           "called Menu.addAction with args `fm4` None\n"
                                           "called Action.__init__ with args ('fm4', None)\n"
                                           "called MenuBar.addMenu with arg  &View\n"
                                           "called Menu.__init__ with args ('&View',)\n"
                                           "called Menu.addAction with args `vm1` None\n"
                                           "called Action.__init__ with args ('vm1', None)\n"
                                           "called Menu.addAction with args `vm2` None\n"
                                           "called Action.__init__ with args ('vm2', None)\n"
                                           "called MenuBar.addMenu with arg  &Search\n"
                                           "called Menu.__init__ with args ('&Search',)\n"
                                           "called Menu.addAction with args `sm1` None\n"
                                           "called Action.__init__ with args ('sm1', None)\n"
                                           "called Menu.addAction with args `sm2` None\n"
                                           "called Action.__init__ with args ('sm2', None)\n")
        result = testobj.init_menus(popup=True)
        assert isinstance(result, testee.qtw.QMenu)
        assert capsys.readouterr().out == ("called Menu.__init__ with args ('&View',)\n"
                                           "called Menu.addAction with args `vm1` None\n"
                                           "called Action.__init__ with args ('vm1', None)\n"
                                           "called Menu.addAction with args `vm2` None\n"
                                           "called Action.__init__ with args ('vm2', None)\n"
                                           "called Menu.addSeparator\n"
                                           "called Action.__init__ with args ('-----', None)\n"
                                           "called Menu.addAction with args `sm1` None\n"
                                           "called Action.__init__ with args ('sm1', None)\n"
                                           "called Menu.addAction with args `sm2` None\n"
                                           "called Action.__init__ with args ('sm2', None)\n")
        testobj.editable = True
        result = testobj.init_menus()
        assert len(result) == len (['File', 'View', 'Edit'])
        assert capsys.readouterr().out == ("called Gui.setup_menuactions\n"
                                           "called MenuBar.__init__\n"
                                           "called MenuBar.addMenu with arg  &File\n"
                                           "called Menu.__init__ with args ('&File',)\n"
                                           "called Menu.addAction with args `fm1` None\n"
                                           "called Action.__init__ with args ('fm1', None)\n"
                                           "called Menu.addAction with args `fm2` None\n"
                                           "called Action.__init__ with args ('fm2', None)\n"
                                           "called Menu.addAction with args `fm3` None\n"
                                           "called Action.__init__ with args ('fm3', None)\n"
                                           "called Menu.addAction with args `fm4` None\n"
                                           "called Action.__init__ with args ('fm4', None)\n"
                                           "called Menu.addSeparator\n"
                                           "called Action.__init__ with args ('-----', None)\n"
                                           "called Menu.addAction with args `fm5` None\n"
                                           "called Action.__init__ with args ('fm5', None)\n"
                                           "called Menu.addSeparator\n"
                                           "called Action.__init__ with args ('-----', None)\n"
                                           "called Menu.addAction with args `fm9` None\n"
                                           "called Action.__init__ with args ('fm9', None)\n"
                                           "called MenuBar.addMenu with arg  &View\n"
                                           "called Menu.__init__ with args ('&View',)\n"
                                           "called Menu.addAction with args `vm1` None\n"
                                           "called Action.__init__ with args ('vm1', None)\n"
                                           "called Menu.addAction with args `vm2` None\n"
                                           "called Action.__init__ with args ('vm2', None)\n"
                                           "called Gui.add_editactions\n"
                                           "called Menu.__init__ with args ()\n"
                                           "called MenuBar.addMenu with arg  &Search\n"
                                           "called Menu.__init__ with args ('&Search',)\n"
                                           "called Menu.addAction with args `sm1` None\n"
                                           "called Action.__init__ with args ('sm1', None)\n"
                                           "called Menu.addAction with args `sm2` None\n"
                                           "called Action.__init__ with args ('sm2', None)\n")
        result = testobj.init_menus(popup=True)
        assert isinstance(result, testee.qtw.QMenu)
        assert capsys.readouterr().out == ("called Menu.__init__ with args ('&View',)\n"
                                           "called Menu.addAction with args `vm1` None\n"
                                           "called Action.__init__ with args ('vm1', None)\n"
                                           "called Menu.addAction with args `vm2` None\n"
                                           "called Action.__init__ with args ('vm2', None)\n"
                                           "called Gui.add_editactions\n"
                                           "called Menu.__init__ with args ()\n"
                                           "called Menu.addSeparator\n"
                                           "called Action.__init__ with args ('-----', None)\n"
                                           "called Menu.addAction with args `sm1` None\n"
                                           "called Action.__init__ with args ('sm1', None)\n"
                                           "called Menu.addAction with args `sm2` None\n"
                                           "called Action.__init__ with args ('sm2', None)\n")

    def test_setup_menuactions(self, monkeypatch, capsys):
        """unittest for Gui.setup_menuactions
        """
        def mock_get():
            print('called Editor.get_menu_data')
            return []
        def mock_get_2():
            print('called Editor.get_menu_data')
            return [(('text1', 'callback1', ''),), (('text2', 'callback2', 'xxx'),),
                    (('text3', 'callback3', 'xxx,yyy'),), (('text4', 'callback4', ''),)]
        def mock_get_3():
            print('called Editor.get_menu_data')
            return [(('tf1', 'cf1', ''), ('tf2', 'cf2', '')),
                    (('tv1', 'cv1', ''),),
                    (('te1', 'ce1', ''), ('te2', 'ce2', ''), ('te3', 'ce3', ''),
                     ('te4', 'ce4', ''), ('te5', 'ce5', ''), ('te6', 'ce6', ''),
                     ('te7', 'ce7', ''), ('te8', 'ce8', ''), ('te9', 'ce9', '')),
                    (('ts1', 'cs1', ''),)]
        monkeypatch.setattr(testee.qtw, 'QAction', mockqtw.MockAction)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor.get_menu_data = mock_get
        testobj.editable = False
        testobj.setup_menuactions()
        assert testobj.filemenu_actions == []
        assert testobj.viewmenu_actions == []
        assert testobj.editmenu_actions == []
        assert testobj.searchmenu_actions == []
        assert capsys.readouterr().out == "called Editor.get_menu_data\n"

        testobj.editor.get_menu_data = mock_get_2
        testobj.setup_menuactions()
        assert len(testobj.filemenu_actions) == 1
        assert isinstance(testobj.filemenu_actions[0], testee.qtw.QAction)
        assert len(testobj.viewmenu_actions) == 1
        assert isinstance(testobj.viewmenu_actions[0], testee.qtw.QAction)
        assert len(testobj.editmenu_actions) == 0
        assert len(testobj.searchmenu_actions) == 2
        assert isinstance(testobj.searchmenu_actions[0], testee.qtw.QAction)
        assert isinstance(testobj.searchmenu_actions[1], testee.qtw.QAction)
        assert capsys.readouterr().out == (
                "called Editor.get_menu_data\n"
                f"called Action.__init__ with args ('text1', {testobj})\n"
                "called Signal.connect with args ('callback1',)\n"
                f"called Action.__init__ with args ('text2', {testobj})\n"
                "called Signal.connect with args ('callback2',)\n"
                "called Action.setShortcuts with arg `['xxx']`\n"
                f"called Action.__init__ with args ('text3', {testobj})\n"
                "called Signal.connect with args ('callback3',)\n"
                "called Action.setShortcuts with arg `['xxx', 'yyy']`\n"
                f"called Action.__init__ with args ('text4', {testobj})\n"
                "called Signal.connect with args ('callback4',)\n")

        testobj.editor.get_menu_data = mock_get_3
        testobj.editable = True
        testobj.setup_menuactions()
        assert len(testobj.filemenu_actions) == 3
        assert len(testobj.viewmenu_actions) == 1
        assert len(testobj.editmenu_actions) == 9
        assert len(testobj.searchmenu_actions) == 1
        assert testobj.undo_item, testobj.redo_item == testobj.editmenu_actions[0:2]
        assert testobj.pastebefore_item, testobj.pasteafter_item == testobj.editmenu_actions[6:8]
        assert testobj.pasteunder_item == testobj.editmenu_actions[8]
        assert testobj.setundo_action == testobj.filemenu_actions[-2]
        assert capsys.readouterr().out == (
                "called Editor.get_menu_data\n"
                f"called Action.__init__ with args ('tf1', {testobj})\n"
                "called Signal.connect with args ('cf1',)\n"
                f"called Action.__init__ with args ('tf2', {testobj})\n"
                "called Signal.connect with args ('cf2',)\n"
                f"called Action.__init__ with args ('tv1', {testobj})\n"
                "called Signal.connect with args ('cv1',)\n"
                f"called Action.__init__ with args ('te1', {testobj})\n"
                "called Signal.connect with args ('ce1',)\n"
                f"called Action.__init__ with args ('te2', {testobj})\n"
                "called Signal.connect with args ('ce2',)\n"
                f"called Action.__init__ with args ('te3', {testobj})\n"
                "called Signal.connect with args ('ce3',)\n"
                f"called Action.__init__ with args ('te4', {testobj})\n"
                "called Signal.connect with args ('ce4',)\n"
                f"called Action.__init__ with args ('te5', {testobj})\n"
                "called Signal.connect with args ('ce5',)\n"
                f"called Action.__init__ with args ('te6', {testobj})\n"
                "called Signal.connect with args ('ce6',)\n"
                f"called Action.__init__ with args ('te7', {testobj})\n"
                "called Signal.connect with args ('ce7',)\n"
                f"called Action.__init__ with args ('te8', {testobj})\n"
                "called Signal.connect with args ('ce8',)\n"
                f"called Action.__init__ with args ('te9', {testobj})\n"
                "called Signal.connect with args ('ce9',)\n"
                f"called Action.__init__ with args ('ts1', {testobj})\n"
                "called Signal.connect with args ('cs1',)\n"
                f"called Action.__init__ with args ('&Unlimited Undo', {testobj})\n"
                f"called Signal.connect with args ({testobj.limit_undo},)\n"
                "called Action.setChecked with arg `False`\n")

    def test_add_editactions_to_menu(self, monkeypatch, capsys):
        """unittest for Gui.add_editactions_to_menu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editmenu_actions = []   # (10+ items?)
        testobj.cut_el = testobj.cut_att = None
        testobj.pastebefore_item = mockqtw.MockAction()
        testobj.pasteafter_item = mockqtw.MockAction()
        testobj.pasteunder_item = mockqtw.MockAction()
        menubar = mockqtw.MockMenuBar()
        viewmenu = mockqtw.MockMenu()
        assert capsys.readouterr().out == ("called Action.__init__ with args ()\n"
                                           "called Action.__init__ with args ()\n"
                                           "called Action.__init__ with args ()\n"
                                           "called MenuBar.__init__\n"
                                           "called Menu.__init__ with args ()\n")
        testobj.add_editactions_to_menu(False, menubar, viewmenu)
        assert capsys.readouterr().out == ("called MenuBar.addMenu with arg  &Edit\n"
                                           "called Menu.__init__ with args ('&Edit',)\n"
                                           "called Action.setText with arg `Nothing to Paste`\n"
                                           "called Action.setEnabled with arg `False`\n"
                                           "called Action.setEnabled with arg `False`\n"
                                           "called Action.setEnabled with arg `False`\n"
                                           "called Menu.addAction\n"
                                           "called Menu.addAction\n"
                                           "called Menu.addAction\n"
                                           "called Menu.addSeparator\n"
                                           "called Action.__init__ with args ('-----', None)\n")

        testobj.editmenu_actions = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        testobj.cut_el = 'x'
        testobj.add_editactions_to_menu(False, menubar, viewmenu)
        assert capsys.readouterr().out == ("called MenuBar.addMenu with arg  &Edit\n"
                                           "called Menu.__init__ with args ('&Edit',)\n"
                                           "called Menu.addAction with args `1` None\n"
                                           "called Action.__init__ with args ('1', None)\n"
                                           "called Menu.addAction with args `2` None\n"
                                           "called Action.__init__ with args ('2', None)\n"
                                           "called Menu.addAction with args `3` None\n"
                                           "called Action.__init__ with args ('3', None)\n"
                                           "called Menu.addSeparator\n"
                                           "called Action.__init__ with args ('-----', None)\n"
                                           "called Menu.addAction with args `4` None\n"
                                           "called Action.__init__ with args ('4', None)\n"
                                           "called Menu.addAction with args `5` None\n"
                                           "called Action.__init__ with args ('5', None)\n"
                                           "called Menu.addAction with args `6` None\n"
                                           "called Action.__init__ with args ('6', None)\n"
                                           "called Menu.addAction\n"
                                           "called Menu.addAction\n"
                                           "called Menu.addAction\n"
                                           "called Menu.addSeparator\n"
                                           "called Action.__init__ with args ('-----', None)\n"
                                           "called Menu.addAction with args `10` None\n"
                                           "called Action.__init__ with args ('10', None)\n")
        testobj.add_editactions_to_menu(True, menubar, viewmenu)
        assert capsys.readouterr().out == ("called Menu.setTitle with arg 'View/Edit'\n"
                                           "called Menu.addSeparator\n"
                                           "called Action.__init__ with args ('-----', None)\n"
                                           "called Menu.addAction with args `1` None\n"
                                           "called Action.__init__ with args ('1', None)\n"
                                           "called Menu.addAction with args `2` None\n"
                                           "called Action.__init__ with args ('2', None)\n"
                                           "called Menu.addAction with args `3` None\n"
                                           "called Action.__init__ with args ('3', None)\n"
                                           "called Menu.addSeparator\n"
                                           "called Action.__init__ with args ('-----', None)\n"
                                           "called Menu.addAction with args `4` None\n"
                                           "called Action.__init__ with args ('4', None)\n"
                                           "called Menu.addAction with args `5` None\n"
                                           "called Action.__init__ with args ('5', None)\n"
                                           "called Menu.addAction with args `6` None\n"
                                           "called Action.__init__ with args ('6', None)\n"
                                           "called Menu.addAction\n"
                                           "called Menu.addAction\n"
                                           "called Menu.addAction\n"
                                           "called Menu.addSeparator\n"
                                           "called Action.__init__ with args ('-----', None)\n"
                                           "called Menu.addAction with args `10` None\n"
                                           "called Action.__init__ with args ('10', None)\n")

    def test_meldinfo(self, monkeypatch, capsys):
        """unittest for Gui.meldinfo
        """
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor.title = 'Title'
        testobj.meldinfo('message')
        assert capsys.readouterr().out == (
                f"called MessageBox.information with args `{testobj}` `Title` `message`\n")

    def test_meldfout(self, monkeypatch, capsys):
        """unittest for Gui.meldfout
        """
        def mock_close():
            print('called Gui.close')
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor.title = 'Title'
        testobj.close = mock_close
        testobj.meldfout('error')
        assert capsys.readouterr().out == (
                f"called MessageBox.critical with args `{testobj}` `Title` `error`\n")
        testobj.meldfout('error', abort=True)
        assert capsys.readouterr().out == (
                f"called MessageBox.critical with args `{testobj}` `Title` `error`\n"
                'called Gui.close\n')

    def test_ask_yesnocancel(self, monkeypatch, capsys):
        """unittest for Gui.ask_yesnocancel
        """
        def mock_ask_no(parent, *args, **kwargs):
            print(f'called MessageBox.question with args {parent}', args, kwargs)
            return mockqtw.MockMessageBox.No
        def mock_ask_yes(parent, *args, **kwargs):
            print(f'called MessageBox.question with args {parent}', args, kwargs)
            return mockqtw.MockMessageBox.Yes
        def mock_ask_cancel(parent, *args, **kwargs):
            print(f'called MessageBox.question with args {parent}', args, kwargs)
            return mockqtw.MockMessageBox.Cancel
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor.title = 'Title'
        monkeypatch.setattr(mockqtw.MockMessageBox, 'question', mock_ask_no)
        assert testobj.ask_yesnocancel('Prompt') == 0
        assert testobj.in_dialog
        assert capsys.readouterr().out == (f"called MessageBox.question with args {testobj}"
                                           " ('Title', 'Prompt', 14) {'defaultButton': 4}\n")
        monkeypatch.setattr(mockqtw.MockMessageBox, 'question', mock_ask_yes)
        testobj.editor.title = 'Title'
        assert testobj.ask_yesnocancel('Prompt') == 1
        assert capsys.readouterr().out == (f"called MessageBox.question with args {testobj}"
                                           " ('Title', 'Prompt', 14) {'defaultButton': 4}\n")
        monkeypatch.setattr(mockqtw.MockMessageBox, 'question', mock_ask_cancel)
        testobj.editor.title = 'Title'
        assert testobj.ask_yesnocancel('Prompt') == -1
        assert capsys.readouterr().out == (f"called MessageBox.question with args {testobj}"
                                           " ('Title', 'Prompt', 14) {'defaultButton': 4}\n")

    def test_ask_for_text(self, monkeypatch, capsys):
        """unittest for Gui.ask_for_text
        """
        monkeypatch.setattr(testee.qtw, 'QInputDialog', mockqtw.MockInputDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor.title = 'Title'
        assert testobj.ask_for_text('Prompt', value='x') == ""
        assert testobj.in_dialog
        assert capsys.readouterr().out == (f"called InputDialog.getText with args {testobj}"
                                           " ('Title', 'Prompt', 0, 'x') {}\n")

    def test_file_to_read(self, monkeypatch, capsys):
        """unittest for Gui.file_to_read
        """
        def mock_open(parent, *args, **kwargs):
            print('called FileDialog.getOpenFileName with args', parent, args, kwargs)
            return 'xxx', True
        monkeypatch.setattr(testee.qtw, 'QFileDialog', mockqtw.MockFileDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.file_to_read() == (False, "")
        assert capsys.readouterr().out == (
                f"called FileDialog.getOpenFileName with args {testobj} ('Choose a file',"
                " '/home/albert/projects/xmledit', 'XML files (*.xml *.XML);;All files (*.*)')"
                " {}\n")
        monkeypatch.setattr(mockqtw.MockFileDialog, 'getOpenFileName', mock_open)
        assert testobj.file_to_read() == (True, "xxx")
        assert capsys.readouterr().out == (
                f"called FileDialog.getOpenFileName with args {testobj} ('Choose a file',"
                " '/home/albert/projects/xmledit', 'XML files (*.xml *.XML);;All files (*.*)')"
                " {}\n")

    def test_file_to_save(self, monkeypatch, capsys):
        """unittest for Gui.file_to_save
        """
        def mock_save(parent, *args, **kwargs):
            print('called FileDialog.getSaveFilename with args', parent, args, kwargs)
            return 'xxx', True
        monkeypatch.setattr(testee.qtw, 'QFileDialog', mockqtw.MockFileDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor.xmlfn = 'qqq'
        assert testobj.file_to_save() == (False, "")
        assert capsys.readouterr().out == (
                f"called FileDialog.getSaveFilename with args {testobj} ('Save file as ...',"
                " 'qqq', 'XML files (*.xml *.XML);;All files (*.*)') {}\n")
        monkeypatch.setattr(mockqtw.MockFileDialog, 'getSaveFileName', mock_save)
        assert testobj.file_to_save() == (True, "xxx")
        assert capsys.readouterr().out == (
                f"called FileDialog.getSaveFilename with args {testobj} ('Save file as ...',"
                " 'qqq', 'XML files (*.xml *.XML);;All files (*.*)') {}\n")

    def test_enable_pasteitems(self, monkeypatch, capsys):
        """unittest for Gui.enable_pasteitems
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pastebefore_item = mockqtw.MockAction()
        testobj.pasteafter_item = mockqtw.MockAction()
        testobj.pasteunder_item = mockqtw.MockAction()
        assert capsys.readouterr().out == ("called Action.__init__ with args ()\n"
                                           "called Action.__init__ with args ()\n"
                                           "called Action.__init__ with args ()\n")
        testobj.enable_pasteitems()
        assert capsys.readouterr().out == ("called Action.setText with arg `Nothing to Paste`\n"
                                           "called Action.setEnabled with arg `False`\n"
                                           "called Action.setEnabled with arg `False`\n"
                                           "called Action.setEnabled with arg `False`\n")
        testobj.enable_pasteitems(active=True)
        assert capsys.readouterr().out == ("called Action.setText with arg `Paste Before`\n"
                                           "called Action.setEnabled with arg `True`\n"
                                           "called Action.setEnabled with arg `True`\n"
                                           "called Action.setEnabled with arg `True`\n")

    def test_limit_undo(self, monkeypatch, capsys):
        """unittest for Gui.limit_undo
        """
        def mock_meldinfo(msg):
            print(f"called Gui.meldinfo with arg '{msg}'")
        def mock_unset(value):
            print(f"called undostack.unset_undo_limit with arg {value}")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.meldinfo = mock_meldinfo
        testobj.undoredowarning = 'undo/redo warning'
        testobj.setundo_action = mockqtw.MockAction()
        testobj.undo_stack = mockqtw.MockUndoStack()
        assert capsys.readouterr().out == ("called Action.__init__ with args ()\n"
                                           "called UndoStack.__init__ with args ()\n")
        testobj.undo_stack.unset_undo_limit = mock_unset
        testobj.limit_undo()
        assert capsys.readouterr().out == ("called Action.isChecked\n"
                                           "called undostack.unset_undo_limit with arg False\n")
        testobj.setundo_action.setChecked(True)
        assert capsys.readouterr().out == "called Action.setChecked with arg `True`\n"
        testobj.limit_undo()
        assert capsys.readouterr().out == ("called Action.isChecked\n"
                                           "called undostack.unset_undo_limit with arg True\n"
                                           "called Gui.meldinfo with arg 'undo/redo warning'\n")

    def test_popupmenu(self, monkeypatch, capsys):
        """unittest for Gui.popupmenu
        """
        def mock_menu(**kwargs):
            print('called Gui.init_menus with args', kwargs)
            result = mockqtw.MockMenu()
            assert capsys.readouterr().out == ("called Gui.init_menus with args {'popup': True}\n"
                                               "called Menu.__init__ with args ()\n")
            return result
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.init_menus = mock_menu
        # breakpoint()
        testobj.popupmenu('item')
        assert capsys.readouterr().out == ("called Tree.visualItemRect with arg item\n"
                                           "called Tree.mapToGlobal with arg bottom-right\n"
                                           "called Menu.exec_ with args ('mapped-to-global',) {}\n")

    def test_quit(self, monkeypatch, capsys):
        """unittest for Gui.quit
        """
        def mock_close():
            print('called Gui.close')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.close = mock_close
        testobj.quit()
        assert capsys.readouterr().out == "called Gui.close\n"

    def test_on_keyup(self, monkeypatch, capsys):
        """unittest for Gui.on_keyup
        """
        def mock_current():
            print('called Tree.currentItem')
            return None
        def mock_current_top():
            print('called Tree.currentItem')
            return 'top'
        item = mockqtw.MockTreeItem()
        parent = mockqtw.MockTreeItem()
        parent.addChild(item)
        child = mockqtw.MockTreeItem()
        item.addChild(child)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.addChild\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.addChild\n")
        def mock_current_other():
            print('called Tree.currentItem')
            return item
        def mock_popup(arg):
            print(f'called Gui.popupmenu with arg {arg}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.top = 'top'
        testobj.popupmenu = mock_popup
        event = mockqtw.MockEvent(key=testee.core.Qt.Key_Return)
        testobj.tree.currentItem = mock_current
        assert not testobj.on_keyup(event)
        assert capsys.readouterr().out == "called Tree.currentItem\n"

        testobj.tree.currentItem = mock_current_top
        assert not testobj.on_keyup(event)
        assert capsys.readouterr().out == "called Tree.currentItem\n"

        testobj.tree.currentItem = mock_current_other
        testobj.in_dialog = True
        assert testobj.on_keyup(event)
        assert not testobj.in_dialog
        assert capsys.readouterr().out == "called Tree.currentItem\n"
        # testobj.in_dialog = False
        monkeypatch.setattr(mockqtw.MockTreeItem, 'childCount', lambda x: 0)
        assert testobj.on_keyup(event)
        assert capsys.readouterr().out == "called Tree.currentItem\n"
        monkeypatch.setattr(mockqtw.MockTreeItem, 'childCount', lambda x: 1)
        monkeypatch.setattr(mockqtw.MockTreeItem, 'isExpanded', lambda x: True)
        assert testobj.on_keyup(event)
        assert capsys.readouterr().out == ("called Tree.currentItem\n"
                                           f"called Tree.collapseItem with arg {item}\n"
                                           "called TreeItem.parent\n"
                                           f"called Tree.setCurrentItem with arg `{parent}`\n")
        monkeypatch.setattr(mockqtw.MockTreeItem, 'isExpanded', lambda x: False)
        assert testobj.on_keyup(event)
        assert capsys.readouterr().out == ("called Tree.currentItem\n"
                                           f"called Tree.expandItem with arg {item}\n"
                                           "called TreeItem.child with arg 0\n"
                                           f"called Tree.setCurrentItem with arg `{child}`\n")

        event = mockqtw.MockEvent(key=testee.core.Qt.Key_Backspace)
        monkeypatch.setattr(mockqtw.MockTreeItem, 'isExpanded', lambda x: False)
        assert testobj.on_keyup(event)
        assert capsys.readouterr().out == "called Tree.currentItem\n"
        monkeypatch.setattr(mockqtw.MockTreeItem, 'isExpanded', lambda x: True)
        assert testobj.on_keyup(event)
        assert capsys.readouterr().out == ("called Tree.currentItem\n"
                                           f"called Tree.collapseItem with arg {item}\n"
                                           "called TreeItem.parent\n"
                                           f"called Tree.setCurrentItem with arg `{parent}`\n")

        event = mockqtw.MockEvent(key=testee.core.Qt.Key_Menu)
        assert testobj.on_keyup(event)
        assert capsys.readouterr().out == ("called Tree.currentItem\n"
                                           f"called Gui.popupmenu with arg {item}\n")

    def test_ask_for_search_args(self, monkeypatch, capsys):
        """unittest for Gui.ask_for_search_args
        """
        class MockSearch:
            def __init__(self, *args, **kwargs):
                print('called SearchDialog.__init__ with args', args, kwargs)
            def exec_(self):
                print('called SearchDialog.exec_')
                return testee.qtw.QDialog.Rejected
        def exec_2(self):
            print('called SearchDialog.exec_')
            return testee.qtw.QDialog.Accepted
        monkeypatch.setattr(testee, 'SearchDialog', MockSearch)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert not testobj.ask_for_search_args()
        assert capsys.readouterr().out == (
                f"called SearchDialog.__init__ with args ({testobj},) {{'title': 'Search options'}}\n"
                "called SearchDialog.exec_\n")
        MockSearch.exec_ = exec_2
        assert testobj.ask_for_search_args()
        assert capsys.readouterr().out == (
                f"called SearchDialog.__init__ with args ({testobj},) {{'title': 'Search options'}}\n"
                "called SearchDialog.exec_\n")

    def test_do_undo(self, monkeypatch, capsys):
        """unittest for Gui.do_undo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.undo_stack = mockqtw.MockUndoStack()
        assert capsys.readouterr().out == "called UndoStack.__init__ with args ()\n"
        testobj.do_undo()
        assert capsys.readouterr().out == "called UndoRedoStack.undo\n"

    def test_do_redo(self, monkeypatch, capsys):
        """unittest for Gui.do_redo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.undo_stack = mockqtw.MockUndoStack()
        assert capsys.readouterr().out == "called UndoStack.__init__ with args ()\n"
        testobj.do_redo()
        assert capsys.readouterr().out == "called UndoRedoStack.redo\n"
