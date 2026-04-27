"""unittests for ./axe/base.py
"""
import os.path
import types
import textwrap
import axe.main as testee
import pytest


class MockGui:
    """testdouble object for axe.gui.Gui
    """
    def __init__(self, master, *args, **kwargs):
        self.master = master
        print('called Gui.__init__')
        self.top = 'treetop'
    def go(self):
        """stub
        """
        print('called Gui.go')
    def meldinfo(self, *args, **kwargs):
        """stub
        """
        print('called Gui.meldinfo with args', args, kwargs)
    def meldfout(self, *args, **kwargs):
        """stub
        """
        print('called Gui.meldfout with args', args, kwargs)
    def setup_display(self, *args):
        """stub
        """
        print('called Gui.setup_display with args', args)
    def init_tree(self, *args):
        """stub
        """
        print('called Gui.init_tree with args', args)
    def setup_new_tree(self, *args):
        """stub
        """
        print('called Gui.setup_new_tree with args', args)
    def set_windowtitle(self, title):
        """stub
        """
        print(f'called Gui.set_windowtitle with arg `{title}`')
    def get_windowtitle(self):
        """stub
        """
    def ask_yesnocancel(self):
        """stub
        """
    def get_selected_item(self):
        """stub
        """
        print('called Gui.get_selected_item')
        return 'selected'
    def set_selected_item(self, item):
        """stub
        """
        print(f'called Gui.set_selected_item with arg `{item}`')
    def get_treetop(self):
        """stub
        """
        return self.top
    def get_node_children(self, node):
        """stub
        """
        print(f'called Gui.get_node_children with arg `{node}`')
        return 'child1', 'child2'
    def get_node_title(self, node):
        """stub
        """
        print(f'called Gui.get_node_title with arg `{node}`')
        return 'title'
    def get_node_data(self, node):
        """stub
        """
        print(f'called Gui.get_node_data with arg `{node}`')
        return 'node', 'data'
    def get_node_parentpos(self, node):
        """stub
        """
        print(f'called Gui.get_node_parentpos with arg `{node}`')
        return 'parent', 'pos'
    def add_node_to_parent(self, node):
        """stub
        """
        print(f'called Gui.add_node_to_parent with arg `{node}`')
    def set_node_title(self, node, title):
        """stub
        """
        print(f'called Gui.set_node_title with args `{node}` `{title}`')
    def expand_item(self, node=None):
        """stub
        """
        print(f'called Gui.expand_item with arg `{node}`')
    def collapse_item(self):
        """stub
        """
        print('called Gui.collapse_item')
    def do_undo(self, node=None):
        """stub
        """
        print('called Gui.do_undo')
    def do_redo(self, node=None):
        """stub
        """
        print('called Gui.do_redo')
    def edit_item(self, *args):
        """stub
        """
        print('called Gui.edit_item with args', args)
    def copy(self, *args, **kwargs):
        """stub
        """
        print('called Gui.copy with args', args, kwargs)
    def paste(self, *args, **kwargs):
        """stub
        """
        print('called Gui.paste with args', args, kwargs)
    def add_attribute(self, *args):
        """stub
        """
        print('called Gui.add_attribute with args', args)
    def insert(self, *args, **kwargs):
        """stub
        """
        print('called Gui.insert with args', args, kwargs)
    def file_to_save(self):
        """stub
        """
        print('called Gui.file_to_save')
        return False, ''
    def file_to_read(self):
        """stub
        """
        print('called Gui.file_to_read')
        return False, ''
    def ask_for_text(self, *args):
        """stub
        """
        print('called Gui.ask_for_text with args', args)
        return ''
    def ask_for_search_args(self):
        """stub
        """
        print('called Gui.ask_for_search_args')
        return False


class MockDialogGui:
    """testdouble object for axe.gui.DialogGui
    """
    def __init__(self, *args, **kwargs):
        print('called DialogGui.__init__ with args', args, kwargs)
    def add_label(self, *args, **kwargs):
        print('called DialogGui.add_label with args', args, kwargs)
    def add_lineinput(self, *args, **kwargs):
        print('called DialogGui.add_lineinput with args', args, kwargs)
        return 'lineinput'
    def add_checkbox(self, *args, **kwargs):
        print('called DialogGui.add_checkbox with args', args, kwargs)
        return 'checkbox'
    def add_combobox(self, *args):
        print('called DialogGui.add_combobox with args', args)
        return 'combobox'
    def add_textinput(self, *args):
        print('called DialogGui.add_textinput with args', args)
        return 'textinput'
    def add_buttons(self, *args):
        print('called DialogGui.add_buttons with args', args)
    def finish_display(self):
        print('called DialogGui.finish_display')
    def set_label_text(self, *args):
        print('called DialogGui.set_label_text with args', args)
    def set_lineinput_text(self, *args):
        print('called DialogGui.set_lineinput_text with args', args)
    def set_checkbox_state(self, *args):
        print('called DialogGui.set_checkbox_state with args', args)
    def set_combobox_index(self, *args):
        print('called DialogGui.set_combobox_index with args', args)
    def set_textinput_text(self, *args):
        print('called DialogGui.set_textinput_text with args', args)
    def get_lineinput_text(self, *args):
        print('called DialogGui.get_lineinput_text with args', args)
        return 'lineinput text'
    def get_checkbox_state(self, *args):
        print('called DialogGui.get_checkbox_state with args', args)
        return 'checkbox state'
    def get_combobox_index(self, *args):
        print('called DialogGui.get_combobox_index with args', args)
        return 'combobox index'
    def get_combobox_itemtext(self, *args):
        print('called DialogGui.get_combobox_itemtext with args', args)
        return 'combobox text'
    def get_textinput_text(self, *args):
        print('called DialogGui.get_textinput_text with args', args)
        return 'textinput text'
    def set_focus_to(self, *args):
        print('called DialogGui.set_focus_to with args', args)
    def accept(self):
        print('called DialogGui.accept')
    def reject(self):
        print('called DialogGui.reject')
    def keyPressEvent(self, *args):
        print('called DialogGui.keyPressEvent with args', args)
    def refresh(self):
        print('called DialogGui.refresh')


class TestEditor:
    """unittests for main.Editor
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.Editor object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called Editor.__init__ with args', args)
        monkeypatch.setattr(testee.Editor, '__init__', mock_init)
        testobj = testee.Editor()
        testobj.gui = MockGui(testobj)
        assert capsys.readouterr().out == ('called Editor.__init__ with args ()\n'
                                           "called Gui.__init__\n")
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for Editor.__init__
        """
        def mock_getroot(*args):
            """stub
            """
            return 'got root from tree'
        def mock_parse_nsmap(arg):
            """stub
            """
            print(f'called parse_nsmap with arg {arg}')
            return types.SimpleNamespace(getroot=mock_getroot), ['ns_prefix'], ['ns_uri']
        def mock_parse_nsmap_2(arg):
            """stub
            """
            print(f'called parse_nsmap with arg {arg}')
            raise OSError('got an OSError')
        def mock_parse_nsmap_3(arg):
            """stub
            """
            print(f'called parse_nsmap with arg {arg}')
            # raise testee.et.ParseError('got a ParseError')  # ElementTree
            raise testee.et.ParseError('got a ParseError', 0, 0, 0)  # lxml
        def mock_init_tree(self, *args):
            """stub
            """
            print('called Editor.init_tree with args', args)
        monkeypatch.setattr(testee, 'Gui', MockGui)
        monkeypatch.setattr(testee, 'parse_nsmap', mock_parse_nsmap)
        monkeypatch.setattr(testee.et, 'Element', lambda x: x)
        monkeypatch.setattr(testee.Editor, 'init_tree', mock_init_tree)
        testobj = testee.Editor('')
        assert testobj.title == f'{testee.TITLESTART} Editor'
        assert testobj.xmlfn == ''
        assert not testobj.tree_dirty
        assert not testobj.readonly
        assert isinstance(testobj.gui, testee.Gui)
        assert (testobj.ns_prefixes, testobj.ns_uris) == ([], [])
        assert (testobj.gui.cut_att, testobj.gui.cut_el) == (None, None)
        assert (testobj.search_args, testobj._search_pos) == ([], None)
        assert capsys.readouterr().out == ("called Gui.__init__\n"
                                           "called Gui.setup_display with args ()\n"
                                           "called Editor.init_tree with args ('new_root',)\n"
                                           "called Gui.go\n")
        testobj = testee.Editor('', readonly=True)
        assert testobj.title == f'{testee.TITLESTART} Viewer'
        assert testobj.xmlfn == ''
        assert not testobj.tree_dirty
        assert testobj.readonly
        assert isinstance(testobj.gui, testee.Gui)
        assert (testobj.ns_prefixes, testobj.ns_uris) == ([], [])
        assert not hasattr(testobj.gui, 'cut_att')
        assert not hasattr(testobj.gui, 'cut_el')
        assert (testobj.search_args, testobj._search_pos) == ([], None)
        assert capsys.readouterr().out == ("called Gui.__init__\n"
                                           "called Gui.setup_display with args ()\n"
                                           "called Gui.go\n")
        testobj = testee.Editor('testfile.xml', readonly=True)
        assert testobj.title == f'{testee.TITLESTART} Viewer'
        assert testobj.xmlfn == os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                             'testfile.xml')
        assert not testobj.tree_dirty
        assert testobj.readonly
        assert isinstance(testobj.gui, testee.Gui)
        assert (testobj.ns_prefixes, testobj.ns_uris) == (['ns_prefix'], ['ns_uri'])
        assert not hasattr(testobj.gui, 'cut_att')
        assert not hasattr(testobj.gui, 'cut_el')
        assert (testobj.search_args, testobj._search_pos) == ([], None)
        assert capsys.readouterr().out == (
                "called Gui.__init__\n"
                "called Gui.setup_display with args ()\n"
                f"called parse_nsmap with arg {testobj.xmlfn}\n"
                "called Editor.init_tree with args ('got root from tree',)\n"
                "called Gui.go\n")
        testobj = testee.Editor('testfile.xml')
        assert testobj.title == f'{testee.TITLESTART} Editor'
        assert testobj.xmlfn == os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                             'testfile.xml')
        assert not testobj.tree_dirty
        assert not testobj.readonly
        assert isinstance(testobj.gui, testee.Gui)
        assert (testobj.ns_prefixes, testobj.ns_uris) == (['ns_prefix'], ['ns_uri'])
        assert (testobj.gui.cut_att, testobj.gui.cut_el) == (None, None)
        assert (testobj.search_args, testobj._search_pos) == ([], None)
        assert capsys.readouterr().out == (
                "called Gui.__init__\n"
                "called Gui.setup_display with args ()\n"
                f"called parse_nsmap with arg {testobj.xmlfn}\n"
                "called Editor.init_tree with args ('got root from tree',)\n"
                "called Gui.go\n")
        monkeypatch.setattr(testee, 'parse_nsmap', mock_parse_nsmap_2)
        testobj = testee.Editor('testfile.xml')
        assert (testobj.ns_prefixes, testobj.ns_uris) == ([], [])
        assert capsys.readouterr().out == (
                "called Gui.__init__\n"
                "called Gui.setup_display with args ()\n"
                f"called parse_nsmap with arg {testobj.xmlfn}\n"
                "called Gui.meldfout with args ('got an OSError',) {'abort': True}\n"
                "called Gui.init_tree with args (None,)\n")
        monkeypatch.setattr(testee, 'parse_nsmap', mock_parse_nsmap_3)
        # breakpoint()
        testobj = testee.Editor('testfile.xml')
        assert (testobj.ns_prefixes, testobj.ns_uris) == ([], [])
        assert capsys.readouterr().out == (
                "called Gui.__init__\n"
                "called Gui.setup_display with args ()\n"
                f"called parse_nsmap with arg {testobj.xmlfn}\n"
                "called Gui.meldfout with args ('got a ParseError (line 0)',) {'abort': True}\n"
                "called Gui.init_tree with args (None,)\n")

    def test_mark_dirty(self, monkeypatch, capsys):
        """unittest for Editor.mark_dirty
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.readonly = True
        testobj.mark_dirty(True)
        assert testobj.tree_dirty
        assert capsys.readouterr().out == ''

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.readonly = False
        testobj.title = 'appname'
        monkeypatch.setattr(testobj.gui, 'get_windowtitle', lambda *x: '')
        testobj.mark_dirty(True)
        assert testobj.tree_dirty
        assert capsys.readouterr().out == ''

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.readonly = False
        testobj.title = 'appname'
        monkeypatch.setattr(testobj.gui, 'get_windowtitle', lambda *x: ' - ' + testobj.title)
        testobj.mark_dirty(True)
        assert testobj.tree_dirty
        assert capsys.readouterr().out == 'called Gui.set_windowtitle with arg `* - appname`\n'

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.readonly = False
        testobj.title = 'appname'
        monkeypatch.setattr(testobj.gui, 'get_windowtitle', lambda *x: '* - ' + testobj.title)
        testobj.mark_dirty(True)
        assert testobj.tree_dirty
        assert capsys.readouterr().out == 'called Gui.set_windowtitle with arg ` - appname`\n'

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.readonly = False
        testobj.title = 'appname'
        monkeypatch.setattr(testobj.gui, 'get_windowtitle', lambda *x: ' - ' + testobj.title)
        testobj.mark_dirty(False)
        assert not testobj.tree_dirty
        assert capsys.readouterr().out == 'called Gui.set_windowtitle with arg ` - appname`\n'

    def test_check_tree(self, monkeypatch, capsys):
        """unittest for Editor.check_tree
        """
        def mock_savexml():
            """stub
            """
            print('called Editor.savexml')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.savexml = mock_savexml
        testobj.tree_dirty = False
        assert testobj.check_tree()
        assert capsys.readouterr().out == ''

        testobj.tree_dirty = True
        monkeypatch.setattr(testobj.gui, 'ask_yesnocancel', lambda *x: 1)
        assert testobj.check_tree()
        assert capsys.readouterr().out == 'called Editor.savexml\n'

        monkeypatch.setattr(testobj.gui, 'ask_yesnocancel', lambda *x: -1)
        assert not testobj.check_tree()
        assert capsys.readouterr().out == ''

        monkeypatch.setattr(testobj.gui, 'ask_yesnocancel', lambda *x: 0)
        assert testobj.check_tree()
        assert capsys.readouterr().out == ''

    def test_checkselection(self, monkeypatch, capsys):
        """unittest for Editor.checkselection
        """
        def mock_get():
            """stub
            """
            print('called Gui.get_selected_item')
            return None
        def mock_get2():
            """stub
            """
            print('called Gui.get_selected_item')
            return 'top'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.readonly = True
        testobj.top = 'top'
        assert testobj.checkselection()
        assert testobj.item == 'selected'
        assert capsys.readouterr().out == 'called Gui.get_selected_item\n'

        testobj.readonly = False
        assert testobj.checkselection()
        assert testobj.item == 'selected'
        assert capsys.readouterr().out == 'called Gui.get_selected_item\n'

        testobj.gui.get_selected_item = mock_get
        assert not testobj.checkselection()
        assert testobj.item is None
        assert capsys.readouterr().out == ("called Gui.get_selected_item\n"
                                           "called Gui.meldinfo with args ('You need"
                                           " to select an element or attribute first',) {}\n")

        testobj.gui.get_selected_item = mock_get2
        assert not testobj.checkselection()
        assert testobj.item == 'top'
        assert capsys.readouterr().out == ("called Gui.get_selected_item\n"
                                           "called Gui.meldinfo with args ('You need"
                                           " to select an element or attribute first',) {}\n")

        assert not testobj.checkselection(False)
        assert testobj.item == 'top'
        assert capsys.readouterr().out == "called Gui.get_selected_item\n"

    def test_writexml(self, monkeypatch, capsys):
        """unittest for Editor.writexml
        """
        def mock_copyfile(*args):
            """stub
            """
            print('called shutil.copyfile with args', args)
        class MockTree:
            """stub
            """
            def __init__(self, arg):
                print(f'called XMLTree.__init__ with arg `{arg}`')
                self.root = 'data_root'
            def write(self, *args):
                """stub
                """
                print('called XMLTree.write with args', args)
        def mock_expandnode(x, y, z):
            """stub
            """
            print(f'called Editor.expandnode with args `{x}` `{y}` `data of type {type(z)}`')
        def mock_mark_dirty(arg):
            """stub
            """
            print(f'called Editor.mark_dirty with arg `{arg}`')
        monkeypatch.setattr(testee.shutil, 'copyfile', mock_copyfile)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.xmlfn = 'testfile'
        testobj.expandnode = mock_expandnode
        testobj.mark_dirty = mock_mark_dirty
        monkeypatch.setattr(testee, 'XMLTree', MockTree)
        testobj.ns_prefixes = ()
        monkeypatch.setattr(testee.os.path, 'exists', lambda *x: False)
        testobj.writexml()
        assert capsys.readouterr().out == (
                "called Gui.get_node_data with arg `treetop`\n"
                "called XMLTree.__init__ with arg `node`\n"
                "called Editor.expandnode with args `treetop` `data_root`"
                f" `data of type {testee.XMLTree}`\n"
                "called XMLTree.write with args ('testfile', None)\n"
                "called Editor.mark_dirty with arg `False`\n")
        monkeypatch.setattr(testee.os.path, 'exists', lambda *x: True)
        testobj.writexml()
        assert capsys.readouterr().out == (
                "called shutil.copyfile with args ('testfile',"
                " 'testfile.bak')\n"
                "called Gui.get_node_data with arg `treetop`\n"
                "called XMLTree.__init__ with arg `node`\n"
                "called Editor.expandnode with args `treetop` `data_root`"
                f" `data of type {testee.XMLTree}`\n"
                "called XMLTree.write with args ('testfile', None)\n"
                "called Editor.mark_dirty with arg `False`\n")
        testobj.ns_prefixes = 'prefixes'
        testobj.ns_uris = 'uris'
        testobj.writexml('newfile')
        assert capsys.readouterr().out == (
                "called shutil.copyfile with args ('testfile', 'newfile')\n"
                "called Gui.get_node_data with arg `treetop`\n"
                "called XMLTree.__init__ with arg `node`\n"
                "called Editor.expandnode with args `treetop` `data_root`"
                f" `data of type {testee.XMLTree}`\n"
                "called XMLTree.write with args ('testfile', ('prefixes',"
                " 'uris'))\n"
                "called Editor.mark_dirty with arg `False`\n")

    def test_expandnode(self, monkeypatch, capsys):
        """unittest for Editor.expandnode
        """
        def mock_expand(*args):
            """stub
            """
            nonlocal counter
            print('called Element.expand with args', args)
            counter += 1
            if counter == 1:
                return 'subnode'
            return None
        testobj = self.setup_testobj(monkeypatch, capsys)
        tree = types.SimpleNamespace(expand=mock_expand)
        counter = 0
        testobj.expandnode('app_root', 'data_root', tree)
        assert capsys.readouterr().out == (
                "called Gui.get_node_children with arg `app_root`\n"
                "called Gui.get_node_title with arg `child1`\n"
                "called Gui.get_node_data with arg `child1`\n"
                "called Element.expand with args ('data_root', 'title', ('node', 'data'))\n"
                "called Gui.get_node_children with arg `child1`\n"
                "called Gui.get_node_title with arg `child1`\n"
                "called Gui.get_node_data with arg `child1`\n"
                "called Element.expand with args ('subnode', 'title', ('node', 'data'))\n"
                "called Gui.get_node_title with arg `child2`\n"
                "called Gui.get_node_data with arg `child2`\n"
                "called Element.expand with args ('subnode', 'title', ('node', 'data'))\n"
                "called Gui.get_node_title with arg `child2`\n"
                "called Gui.get_node_data with arg `child2`\n"
                "called Element.expand with args ('data_root', 'title', ('node', 'data'))\n")

    def test_init_tree(self, monkeypatch, capsys):
        """unittest for Editor.init_tree
        """
        class MockElement:
            """stub
            """
            def __init__(self):
                self.tag = 'mytag'
                self.text = 'some text'
                self.attrs = {'x': 'a', 'y': None}
                self.subel = []
            def keys(self):
                """stub
                """
                return self.attrs.keys()
            def get(self, attr):
                """stub
                """
                return self.attrs[attr]
            def __iter__(self):
                """stub
                """
                return (x for x in self.subel)
        class MockElement2:
            """stub
            """
            def __init__(self):
                self.tag = 'mytag'
                self.text = 'some text'
                self.attrs = {'x': 'a', 'y': None}
                self.subel = ['qqq', 'rrr']
            def keys(self):
                """stub
                """
                return self.attrs.keys()
            def get(self, attr):
                """stub
                """
                return self.attrs[attr]
            def __iter__(self):
                """stub
                """
                return (x for x in self.subel)
        def mock_add():
            print("called editor.add_nodes_for_namespaces_if_any")
        def mock_add_item(*args, **kwargs):
            print("called editor.testobj.add_item with args", args, kwargs)
        def mock_add_to_tree(*args):
            print("called editor.testobj.add_to_tree", args)
        def mock_mark_dirty(value):
            print(f"called editor.testobj.mark_dirty with arg {value}")
        def mock_expand(item):
            print("called Gui.expand_item with arg '{item}'")
        def mock_setup(title):
            print(f"called Gui.setup_new_tree with arg '{title}'")
        def mock_set_title(title):
            print(f"called Gui.set_windowtitle with arg '{title}'")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.xmlfn = 'testfile'
        testobj.gui.setup_new_tree = mock_setup
        testobj.gui.set_windowtitle = mock_set_title
        testobj.add_nodes_for_namespaces_if_any = mock_add
        testobj.add_item = mock_add_item
        testobj.add_to_tree = mock_add_to_tree
        testobj.gui.expand_item = mock_expand
        testobj.mark_dirty = mock_mark_dirty
        testobj.title = 'title'
        testobj.top = 'top'
        testobj.ns_prefixes = []
        testobj.ns_uris = []
        testobj.init_tree(None)
        assert capsys.readouterr().out == (
                "called Gui.setup_new_tree with arg 'testfile'\n"
                "called Gui.set_windowtitle with arg 'testfile - title'\n")
        testobj.init_tree(MockElement())
        assert capsys.readouterr().out == (
                "called Gui.setup_new_tree with arg 'testfile'\n"
                "called Gui.set_windowtitle with arg 'testfile - title'\n"
                "called editor.add_nodes_for_namespaces_if_any\n"
                "called editor.testobj.add_item with args (None, 'mytag', 'some text') {}\n"
                "called editor.testobj.add_item with args (None, 'x', 'a') {'attr': True}\n"
                "called editor.testobj.add_item with args (None, 'y', '\"\"') {'attr': True}\n"
                "called Gui.expand_item with arg '{item}'\n"
                "called editor.testobj.mark_dirty with arg False\n")
        testobj.xmlfn = ''
        testobj.init_tree(MockElement2())
        assert capsys.readouterr().out == (
                "called Gui.setup_new_tree with arg '[unsaved file]'\n"
                "called Gui.set_windowtitle with arg '[unsaved file] - title'\n"
                "called editor.add_nodes_for_namespaces_if_any\n"
                "called editor.testobj.add_item with args (None, 'mytag', 'some text') {}\n"
                "called editor.testobj.add_item with args (None, 'x', 'a') {'attr': True}\n"
                "called editor.testobj.add_item with args (None, 'y', '\"\"') {'attr': True}\n"
                "called editor.testobj.add_to_tree ('qqq', None)\n"
                "called editor.testobj.add_to_tree ('rrr', None)\n"
                "called Gui.expand_item with arg '{item}'\n"
                "called editor.testobj.mark_dirty with arg False\n")
        testobj.init_tree(MockElement(), 'some_name')
        assert capsys.readouterr().out == (
                "called Gui.setup_new_tree with arg 'some_name'\n"
                "called Gui.set_windowtitle with arg 'some_name - title'\n"
                "called editor.add_nodes_for_namespaces_if_any\n"
                "called editor.testobj.add_item with args (None, 'mytag', 'some text') {}\n"
                "called editor.testobj.add_item with args (None, 'x', 'a') {'attr': True}\n"
                "called editor.testobj.add_item with args (None, 'y', '\"\"') {'attr': True}\n"
                "called Gui.expand_item with arg '{item}'\n"
                "called editor.testobj.mark_dirty with arg False\n")

    def test_add_nodes_for_namespaces_if_any(self, monkeypatch, capsys):
        """unittest for Editor.add_nodes_for_namespaces_if_any
        """
        def mock_add(arg):
            print(f"called Gui.add_node_to_parent with arg '{arg}'")
            return arg
        def mock_set(*args):
            print("called Gui.set_node_title with args", args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ns_prefixes = ()
        testobj.top = 'top'
        testobj.gui.add_node_to_parent = mock_add
        testobj.gui.set_node_title = mock_set
        testobj.add_nodes_for_namespaces_if_any()
        assert capsys.readouterr().out == ""
        testobj.ns_prefixes = ('a', 'b')
        testobj.ns_uris = ('xxx', 'yyy')
        testobj.gui.add_node_to_parent = mock_add
        testobj.gui.set_node_title = mock_set
        testobj.add_nodes_for_namespaces_if_any()
        assert capsys.readouterr().out == ("called Gui.add_node_to_parent with arg 'top'\n"
                                           "called Gui.set_node_title with args ('top', 'namespaces')\n"
                                           "called Gui.add_node_to_parent with arg 'top'\n"
                                           "called Gui.set_node_title with args ('top', 'a: xxx')\n"
                                           "called Gui.add_node_to_parent with arg 'top'\n"
                                           "called Gui.set_node_title with args ('top', 'b: yyy')\n")

    def test_add_to_tree(self, monkeypatch, capsys):
        """unittest for Editor.add_to_tree
        """
        class MockElement:
            """stub
            """
            def __init__(self):
                self.tag = 'mytag'
                self.text = 'some text'
                self.attrs = {'x': 'a', 'y': None}
                self.subel = []
            def keys(self):
                """stub
                """
                return self.attrs.keys()
            def get(self, attr):
                """stub
                """
                return self.attrs[attr]
            def __iter__(self):
                """stub
                """
                return (x for x in self.subel)
        def mock_add_item(*args, **kwargs):
            """stub
            """
            print('called Editor.add_item with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_item = mock_add_item
        testele = MockElement()
        testele.subel = [MockElement()]
        testobj.add_to_tree(testele, 'root')
        assert capsys.readouterr().out == textwrap.dedent("""\
                called Editor.add_item with args ('root', 'mytag', 'some text') {}
                called Editor.add_item with args (None, 'x', 'a') {'attr': True}
                called Editor.add_item with args (None, 'y', '""') {'attr': True}
                called Editor.add_item with args (None, 'mytag', 'some text') {}
                called Editor.add_item with args (None, 'x', 'a') {'attr': True}
                called Editor.add_item with args (None, 'y', '""') {'attr': True}\n""")

    def test_getshortname(self, monkeypatch, capsys):
        """unittest for Editor.getshortname
        """
        def mock_apply(name):
            print(f"called editor.apply_namespace_mapping with arg '{name}'")
            return name
        def mock_apply_2(name):
            print(f"called editor.apply_namespace_mapping with arg '{name}'")
            raise AttributeError
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.apply_namespace_mapping = mock_apply
        assert testobj.getshortname(('xxx', '')) == '<> xxx'
        assert capsys.readouterr().out == "called editor.apply_namespace_mapping with arg 'xxx'\n"
        assert testobj.getshortname(('xxx', 'yyy')) == '<> xxx: yyy'
        assert capsys.readouterr().out == "called editor.apply_namespace_mapping with arg 'xxx'\n"
        assert testobj.getshortname(('xxx', 'yyy'), True) == 'xxx = yyy'
        assert capsys.readouterr().out == "called editor.apply_namespace_mapping with arg 'xxx'\n"
        assert testobj.getshortname(('xxx', 80 * 'y')) == f"<> xxx: {60 * 'y'}..."
        assert capsys.readouterr().out == "called editor.apply_namespace_mapping with arg 'xxx'\n"
        testobj.apply_namespace_mapping = mock_apply_2
        assert testobj.getshortname(('xxx', '')) == '<!>'
        assert capsys.readouterr().out == "called editor.apply_namespace_mapping with arg 'xxx'\n"

    def test_apply_namespace_mapping(self, monkeypatch, capsys):
        """unittest for Editor.apply_namespace_mapping
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ns_uris = ()
        testobj.ns_prefixes = ('a', 'b')
        assert testobj.apply_namespace_mapping('xxx') == 'xxx'
        assert testobj.apply_namespace_mapping('{xxx}yyy') == 'xxx:yyy'

        testobj.ns_uris = ('xxx', 'zzz')
        assert testobj.apply_namespace_mapping('xxx') == 'xxx'
        assert testobj.apply_namespace_mapping('{xxx}yyy') == 'a:yyy'
        with pytest.raises(ValueError):  # Not enough values to unpack
            assert testobj.apply_namespace_mapping('{xxx') == ''

        testobj.ns_uris = ('xxx', 'zzz')
        assert testobj.apply_namespace_mapping('qqq') == 'qqq'
        assert testobj.apply_namespace_mapping('{qqq}yyy') == 'qqq:yyy'

    def test_add_item(self, monkeypatch, capsys):
        """unittest for Editor.add_item
        """
        def mock_get(*args):
            print("called Editor.getshortname with args", args)
            return f'{testee.ELSTART} xxx'
        def mock_get_2(*args):
            print("called Editor.getshortname with args", args)
            return 'xxx'
        def mock_get_children(node):
            print(f"called Gui.get_node_children with arg {node}")
            return []
        def mock_get_children_2(node):
            print(f"called Gui.get_node_children with arg {node}")
            return ['ppp', '<> qqq', 'rrr']
        def mock_get_title(node):
            print(f"called Gui.get_node_title with arg {node}")
            return node
        def mock_get_pos(*args):
            print("called Gui.get_item_parentpos with args", args)
            return 'parent', 2
        def mock_add(*args):
            print("called Gui.add_node_to_parent with args", args)
            return 'new item'
        def mock_set_title(*args):
            print("called Gui.set_node_title with args", args)
        def mock_set_data(*args):
            print("called Gui.set_node_data with args", args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.getshortname = mock_get
        testobj.gui.get_node_children = mock_get_children
        testobj.gui.get_node_title = mock_get_title
        testobj.gui.get_node_parentpos = mock_get_pos
        testobj.gui.add_node_to_parent = mock_add
        testobj.gui.set_node_title = mock_set_title
        testobj.gui.set_node_data = mock_set_data
        assert testobj.add_item('destitem', 'xxx', None) == 'new item'
        assert capsys.readouterr().out == (
                "called Editor.getshortname with args (('xxx', ''), False)\n"
                "called Gui.add_node_to_parent with args ('destitem', -1)\n"
                "called Gui.set_node_title with args ('new item', '<> xxx')\n"
                "called Gui.set_node_data with args ('new item', 'xxx', '')\n")
        testobj.getshortname = mock_get_2
        assert testobj.add_item('destitem', 'xxx', 'yyy', attr=True) == 'new item'
        assert capsys.readouterr().out == (
                "called Editor.getshortname with args (('xxx', 'yyy'), True)\n"
                "called Gui.get_node_children with arg destitem\n"
                "called Gui.add_node_to_parent with args ('destitem', -1)\n"
                "called Gui.set_node_title with args ('new item', 'xxx')\n"
                "called Gui.set_node_data with args ('new item', 'xxx', 'yyy')\n")
        testobj.gui.get_node_children = mock_get_children_2
        assert testobj.add_item('destitem', 'xxx', 'yyy') == 'new item'
        assert capsys.readouterr().out == (
                "called Editor.getshortname with args (('xxx', 'yyy'), False)\n"
                "called Gui.get_node_children with arg destitem\n"
                "called Gui.get_node_title with arg ppp\n"
                "called Gui.get_node_title with arg <> qqq\n"
                "called Gui.add_node_to_parent with args ('destitem', 1)\n"
                "called Gui.set_node_title with args ('new item', 'xxx')\n"
                "called Gui.set_node_data with args ('new item', 'xxx', 'yyy')\n")
        assert testobj.add_item('destitem', 'xxx', 'yyy', before=True, below=False) == 'new item'
        assert capsys.readouterr().out == (
                "called Editor.getshortname with args (('xxx', 'yyy'), False)\n"
                "called Gui.get_item_parentpos with args ('destitem',)\n"
                "called Gui.add_node_to_parent with args ('parent', 2)\n"
                "called Gui.set_node_title with args ('new item', 'xxx')\n"
                "called Gui.set_node_data with args ('new item', 'xxx', 'yyy')\n")
        assert testobj.add_item('destitem', 'xxx', 'yyy', below=False) == 'new item'
        assert capsys.readouterr().out == (
                "called Editor.getshortname with args (('xxx', 'yyy'), False)\n"
                "called Gui.get_item_parentpos with args ('destitem',)\n"
                "called Gui.add_node_to_parent with args ('parent', 3)\n"
                "called Gui.set_node_title with args ('new item', 'xxx')\n"
                "called Gui.set_node_data with args ('new item', 'xxx', 'yyy')\n")

    def test_get_menu_data(self, monkeypatch, capsys):
        """unittest for Editor.get_menu_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.quit = lambda x: x
        testobj.readonly = False
        result = testobj.get_menu_data()
        assert len(result) == len(['File', 'View', 'Edit', 'Search'])
        assert [x[0] for x in result[0]] == ['&New', '&Open', '&Save', 'Save &As', 'E&xit']
        assert [x[0] for x in result[1]] == ["&Expand All (sub)Levels", "&Collapse All (sub)Levels"]
        assert [x[0] for x in result[2]] == ["Nothing to &Undo", "Nothing to &Redo", "&Edit",
                                             "&Delete", "C&ut", "&Copy", "Paste Before", "Paste After",
                                             "Paste Under", "Insert Attribute", 'Insert Element Before',
                                             'Insert Element After', 'Insert Element Under']
        assert [x[0] for x in result[3]] == ["&Find", "Find from &Here", "Find &Next", "Find &Last",
                                             "Find &Backwards from here", "Find &Previous"]
        testobj.readonly = True
        result = testobj.get_menu_data()
        assert len(result) == len(['File', 'View', 'Search'])
        assert [x[0] for x in result[0]] == ['&Open', 'E&xit']
        assert [x[0] for x in result[1]] == ["&Expand All (sub)Levels", "&Collapse All (sub)Levels"]
        assert [x[0] for x in result[2]] == ["&Find", "Find from &Here", "Find &Next", "Find &Last",
                                             "Find &Backwards from here", "Find &Previous"]

    def test_flatten_tree(self, monkeypatch, capsys):
        """unittest for Editor.flatten_tree
        """
        def mock_get_data(node):
            print(f"called Gui.get_node_data with arg {node}")
            return ('xx', 'yy')
        def mock_get_data_2(node):
            print(f"called Gui.get_node_data with arg {node}")
            raise TypeError
        counter = 0
        def mock_get_children(node):
            nonlocal counter
            print(f"called Gui.get_node_children with arg {node}")
            counter += 1
            if counter == 1:
                return ['ppp', '<> qqq', 'rrr']
            return []
        def mock_get_children_2(node):
            print(f"called Gui.get_node_children with arg {node}")
            return []
        def mock_get_title(node):
            print(f"called Gui.get_node_title with arg {node}")
            return node
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.get_node_children = mock_get_children
        testobj.gui.get_node_title = mock_get_title
        testobj.gui.get_node_data = mock_get_data
        assert testobj.flatten_tree('element') == [('element', 'xx', 'yy', [('ppp', 'xx', 'yy'),
                                                                            ('rrr', 'xx', 'yy')]),
                                                   ('<> qqq', 'xx', 'yy', [])]
        assert capsys.readouterr().out == ("called Gui.get_node_data with arg element\n"
                                           "called Gui.get_node_children with arg element\n"
                                           "called Gui.get_node_title with arg ppp\n"
                                           "called Gui.get_node_data with arg ppp\n"
                                           "called Gui.get_node_title with arg <> qqq\n"
                                           "called Gui.get_node_data with arg <> qqq\n"
                                           "called Gui.get_node_children with arg <> qqq\n"
                                           "called Gui.get_node_title with arg rrr\n"
                                           "called Gui.get_node_data with arg rrr\n")
        testobj.gui.get_node_children = mock_get_children_2
        testobj.gui.get_node_data = mock_get_data_2
        assert testobj.flatten_tree('element') == [('element', '', ('', ''), [])]
        assert capsys.readouterr().out == ("called Gui.get_node_data with arg element\n"
                                           "called Gui.get_node_children with arg element\n")

    def test_find_first(self, monkeypatch, capsys):
        """unittest for Editor.find_first
        """
        def mock_show(*args):
            print('called show_dialog with args', args)
            return False
        def mock_show_2(*args):
            print('called show_dialog with args', args)
            return True
        def mock_check(self, **kwargs):
            print('called Editor.checkselection with args', kwargs)
            self.item = 'item'
            return True
        def mock_check_2(self, **kwargs):
            print('called Editor.checkselection with args', kwargs)
            self.item = None
            return False
        def mock_get(node):
            """stub
            """
            print(f'called Gui.get_node_title with arg `{node}`')
            return '<> title'
        def mock_find_next(*args):
            """stub
            """
            print('called Editor.find_next with args', args)
        class MockDialog:
            "stub"
            def __init__(self, *args, **kwargs):
                print('called SearchDialog.__init__ with args', args, kwargs)
                self.gui = 'SearchDialogGui'
        monkeypatch.setattr(testee, 'SearchDialog', MockDialog)
        monkeypatch.setattr(testee, 'show_dialog', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.Editor, 'checkselection', mock_check)
        # testobj.search_args = {}
        testobj.find_next = mock_find_next
        testobj.find_first()
        assert capsys.readouterr().out == (
            f"called SearchDialog.__init__ with args ({testobj},) {{'title': 'Search options'}}\n"
            "called show_dialog with args ('SearchDialogGui',)\n")
        monkeypatch.setattr(testee, 'show_dialog', mock_show_2)
        testobj.find_first()
        assert testobj._search_pos == ('item', True)
        assert capsys.readouterr().out == (
            f"called SearchDialog.__init__ with args ({testobj},) {{'title': 'Search options'}}\n"
            "called show_dialog with args ('SearchDialogGui',)\n"
            "called Editor.checkselection with args {'message': False}\n"
            'called Gui.get_selected_item\n'
            'called Gui.get_node_title with arg `selected`\n'
            'called Editor.find_next with args (False, False)\n')
        testobj.gui.get_node_title = mock_get
        testobj.find_first()
        assert testobj._search_pos == ('item', False)
        assert capsys.readouterr().out == (
            f"called SearchDialog.__init__ with args ({testobj},) {{'title': 'Search options'}}\n"
            "called show_dialog with args ('SearchDialogGui',)\n"
            "called Editor.checkselection with args {'message': False}\n"
            'called Gui.get_selected_item\n'
            'called Gui.get_node_title with arg `selected`\n'
            'called Editor.find_next with args (False, False)\n')
        monkeypatch.setattr(testee.Editor, 'checkselection', mock_check_2)
        testobj.find_first()
        assert testobj._search_pos == (None, None)  # was ('child1', None)
        assert capsys.readouterr().out == (
            f"called SearchDialog.__init__ with args ({testobj},) {{'title': 'Search options'}}\n"
            "called show_dialog with args ('SearchDialogGui',)\n"
            "called Editor.checkselection with args {'message': False}\n"
            'called Editor.find_next with args (True, False)\n')
        testobj.find_first(reverse=True)
        assert testobj._search_pos == (None, None)  # was ('child2', None)
        assert capsys.readouterr().out == (
            f"called SearchDialog.__init__ with args ({testobj},) {{'title': 'Search options'}}\n"
            "called show_dialog with args ('SearchDialogGui',)\n"
            "called Editor.checkselection with args {'message': False}\n"
            'called Editor.find_next with args (True, True)\n')

    def test_find_next(self, monkeypatch, capsys):
        """unittest for Editor.find_next
        """
        def mock_flatten_tree(node):
            """stub
            """
            print(f'called Editor.flatten_tree with arg `{node}`')
        def mock_find_in_flattened_tree(*args):
            """stub
            """
            print('called find_in_flattened_tree with args', args)
            return 'itemfound', False
        monkeypatch.setattr(testee, 'find_in_flattened_tree', mock_find_in_flattened_tree)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._search_pos = None
        testobj.flatten_tree = mock_flatten_tree
        testobj.find_next(True)
        assert capsys.readouterr().out == ('called Gui.meldinfo with args'
                                           ' (\'You need to "Find" something first\',) {}\n')
        testobj.top = 'top'
        testobj.search_args = 'search_args'
        testobj._search_pos = ('node', True)
        testobj.find_next(True)
        assert capsys.readouterr().out == (
                "called Editor.flatten_tree with arg `top`\n"
                "called find_in_flattened_tree with args"
                " (None, 'search_args', True, False, ('node', True))\n"
                "called Gui.set_selected_item with arg `itemfound`\n")
        testobj._search_pos = ('node', True)
        testobj.find_next(True, reverse=True)
        assert capsys.readouterr().out == (
                "called Editor.flatten_tree with arg `top`\n"
                "called find_in_flattened_tree with args"
                " (None, 'search_args', True, True, ('node', True))\n"
                "called Gui.set_selected_item with arg `itemfound`\n")
        monkeypatch.setattr(testee, 'find_in_flattened_tree', lambda *x: (None, None))
        testobj._search_pos = ('node', True)
        testobj.find_next(True)
        assert capsys.readouterr().out == (
                "called Editor.flatten_tree with arg `top`\n"
                "called Gui.meldinfo with args ('Niks (meer) gevonden',) {}\n")

    def test_newxml(self, monkeypatch, capsys):
        """unittest for Editor.newxml
        """
        def mock_init_tree(arg):
            """stub
            """
            print(f'called Editor.init_tree with arg `{arg}`')
        def mock_element(name):
            """stub
            """
            print(f'created etree.Element for name `{name}`')
            return name
        monkeypatch.setattr(testee.et, 'Element', mock_element)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.init_tree = mock_init_tree
        monkeypatch.setattr(testobj, 'check_tree', lambda *x: False)
        testobj.newxml()
        assert capsys.readouterr().out == ''
        monkeypatch.setattr(testobj, 'check_tree', lambda *x: True)
        testobj.newxml()
        assert testobj.xmlfn == ''
        assert capsys.readouterr().out == (
                "called Gui.ask_for_text with args ('Enter a name (tag) for the root element',"
                " 'new_root')\n"
                "created etree.Element for name `new_root`\n"
                "called Editor.init_tree with arg `new_root`\n")
        monkeypatch.setattr(testobj.gui, 'ask_for_text', lambda *x: 'element')
        testobj.newxml()
        assert testobj.xmlfn == ''
        assert capsys.readouterr().out == ('created etree.Element for name `element`\n'
                                           'called Editor.init_tree with arg `element`\n')

    def test_openxml(self, monkeypatch, capsys):
        """unittest for Editor.openxml
        """
        class MockElement:
            """stub
            """
            def getroot(self):
                """stub
                """
                return 'element_root'
        def mock_init_tree(*args):
            """stub
            """
            print('called Editor.init_tree with args', args)
        def mock_parse_nsmap(fname):
            """stub
            """
            print(f'called parse_nsmap with arg `{fname}`')
            # raise testee.et.ParseError('got a ParseError')  # ElementTree
            raise testee.et.ParseError('got a ParseError', 0, 0, 0)  # lxml
        def mock_parse_nsmap_ok(fname):
            """stub
            """
            return (MockElement(), 'prefixes', 'uris')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.init_tree = mock_init_tree
        testobj.check_tree = lambda *x: False
        testobj.openxml()
        assert capsys.readouterr().out == ''
        testobj.openxml(skip_check=True)
        assert capsys.readouterr().out == 'called Gui.file_to_read\n'
        monkeypatch.setattr(testobj, 'check_tree', lambda *x: True)
        monkeypatch.setattr(testobj.gui, 'file_to_read', lambda *x: (True, 'fname'))
        monkeypatch.setattr(testee, 'parse_nsmap', mock_parse_nsmap)
        testobj.openxml()
        assert capsys.readouterr().out == (
                "called parse_nsmap with arg `fname`\n"
                "called Gui.meldfout with args ('got a ParseError (line 0)',) {}\n")
        monkeypatch.setattr(testee, 'parse_nsmap', mock_parse_nsmap_ok)
        testobj.openxml()
        assert capsys.readouterr().out == (
                "called Editor.init_tree with args ('element_root',)\n")

    def test_savexml(self, monkeypatch, capsys):
        """unittest for Editor.savexml
        """
        def mock_savexmlas():
            """stub
            """
            print('called Editor.savexmlas')
        def mock_writexml():
            """stub
            """
            print('called Editor.writexml')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.savexmlas = mock_savexmlas
        testobj.writexml = mock_writexml
        testobj.xmlfn = ''
        testobj.savexml()
        assert capsys.readouterr().out == 'called Editor.savexmlas\n'
        testobj.xmlfn = 'x'
        testobj.savexml()
        assert capsys.readouterr().out == 'called Editor.writexml\n'

    def test_savexmlas(self, monkeypatch, capsys):
        """unittest for Editor.savexmlas
        """
        def mock_writexml():
            """stub
            """
            print('called Editor.writexml')
        def mock_mark_dirty(value):
            """stub
            """
            print(f'called Editor.mark_dirty with arg `{value}`')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.writexml = mock_writexml
        testobj.mark_dirty = mock_mark_dirty
        testobj.savexmlas()
        assert capsys.readouterr().out == 'called Gui.file_to_save\n'
        monkeypatch.setattr(testobj.gui, 'file_to_save', lambda *x: (True, 'filename'))
        testobj.savexmlas()
        assert capsys.readouterr().out == ('called Editor.writexml\n'
                                           'called Gui.set_node_title with args `treetop` `filename`\n'
                                           'called Editor.mark_dirty with arg `False`\n')

    def test_expand(self, monkeypatch, capsys):
        """unittest for Editor.expand
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.expand()
        assert capsys.readouterr().out == 'called Gui.expand_item with arg `None`\n'

    def test_collapse(self, monkeypatch, capsys):
        """unittest for Editor.collapse
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.collapse()
        assert capsys.readouterr().out == 'called Gui.collapse_item\n'

    def test_undo(self, monkeypatch, capsys):
        """unittest for Editor.undo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.undo()
        assert capsys.readouterr().out == 'called Gui.do_undo\n'

    def test_redo(self, monkeypatch, capsys):
        """unittest for Editor.redo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.redo()
        assert capsys.readouterr().out == 'called Gui.do_redo\n'

    def test_edit_ele(self, monkeypatch, capsys):
        """unittest for Editor.edit
        """
        def mock_check(self, **kwargs):
            print('called Editor.checkselection with args', kwargs)
            self.item = None
            return False
        def mock_check_2(self, **kwargs):
            print('called Editor.checkselection with args', kwargs)
            self.item = 'item'
            return True
        def mock_get(node):
            print(f'called Gui.get_node_title with arg `{node}`')
            return '<> title'
        def mock_get_data(node):
            print(f'called Gui.get_node_data with arg `{node}`')
            return 'node', ''
        def mock_show(*args):
            print('called show_dialog with args', args)
            return False
        def mock_show_2(*args):
            print('called show_dialog with args', args)
            return True
        def mock_getshortname(*args):
            print('called Editor.getshortname with args', args)
            return '-'.join(args[0])
        def mock_mark(*args):
            print('called Editor.mark_dirty with args', args)
        class MockDialog:
            "stub"
            def __init__(self, *args, **kwargs):
                print('called ElementDialog.__init__ with args', args, kwargs)
                self.gui = 'ElementDialogGui'
                args[0].data = {'tag': 'x', 'text': 'y'}
        monkeypatch.setattr(testee, 'ElementDialog', MockDialog)
        monkeypatch.setattr(testee.Editor, 'checkselection', mock_check)
        monkeypatch.setattr(testee, 'show_dialog', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.get_node_title = mock_get
        testobj.getshortname = mock_getshortname
        testobj.mark_dirty = mock_mark
        testobj.edit()
        assert capsys.readouterr().out == 'called Editor.checkselection with args {}\n'
        monkeypatch.setattr(testee.Editor, 'checkselection', mock_check_2)
        testobj.edit()
        assert capsys.readouterr().out == (
            "called Editor.checkselection with args {}\n"
            "called Gui.get_node_title with arg `item`\n"
            "called Gui.get_node_data with arg `item`\n"
            "called ElementDialog.__init__ with args"
            f" ({testobj},) {{'title': 'Edit an element',"
            " 'item': {'item': 'item', 'tag': 'node', 'data': True, 'text': 'data'}}\n"
            "called show_dialog with args ('ElementDialogGui',)\n")
        monkeypatch.setattr(testee, 'show_dialog', mock_show_2)
        testobj.edit()
        assert capsys.readouterr().out == (
            "called Editor.checkselection with args {}\n"
            "called Gui.get_node_title with arg `item`\n"
            "called Gui.get_node_data with arg `item`\n"
            "called ElementDialog.__init__ with args"
            f" ({testobj},) {{'title': 'Edit an element',"
            " 'item': {'item': 'item', 'tag': 'node', 'data': True, 'text': 'data'}}\n"
            "called show_dialog with args ('ElementDialogGui',)\n"
            "called Editor.getshortname with args (('x', 'y'),)\n"
            "called Gui.edit_item with args"
            " ('item', ('<> title', 'node', 'data'), ('x-y', 'x', 'y'), 'Edit Element')\n"
            "called Editor.mark_dirty with args (True,)\n")
        testobj.gui.get_node_data = mock_get_data
        testobj.edit()
        assert capsys.readouterr().out == (
            "called Editor.checkselection with args {}\n"
            "called Gui.get_node_title with arg `item`\n"
            "called Gui.get_node_data with arg `item`\n"
            "called ElementDialog.__init__ with args"
            f" ({testobj},) {{'title': 'Edit an element',"
            " 'item': {'item': 'item', 'tag': 'node'}}\n"
            "called show_dialog with args ('ElementDialogGui',)\n"
            "called Editor.getshortname with args (('x', 'y'),)\n"
            "called Gui.edit_item with args"
            " ('item', ('<> title', 'node', ''), ('x-y', 'x', 'y'), 'Edit Element')\n"
            "called Editor.mark_dirty with args (True,)\n")

    def test_edit_attr(self, monkeypatch, capsys):
        """unittest for Editor.edit
        """
        def mock_check(self, **kwargs):
            print('called Editor.checkselection with args', kwargs)
            self.item = None
            return False
        def mock_check_2(self, **kwargs):
            print('called Editor.checkselection with args', kwargs)
            self.item = 'item'
            return True
        def mock_get(node):
            print(f'called Gui.get_node_title with arg `{node}`')
            return 'title'
        def mock_get_data(node):
            print(f'called Gui.get_node_data with arg `{node}`')
            return 'node', ''
        def mock_show(*args):
            print('called show_dialog with args', args)
            return False
        def mock_show_2(*args):
            print('called show_dialog with args', args)
            return True
        def mock_getshortname(*args, **kwargs):
            print('called Editor.getshortname with args', args, kwargs)
            return '-'.join(args[0])
        def mock_mark(*args):
            print('called Editor.mark_dirty with args', args)
        class MockDialog:
            "stub"
            def __init__(self, *args, **kwargs):
                print('called AttributeDialog.__init__ with args', args, kwargs)
                self.gui = 'AttributeDialogGui'
                args[0].data = {'name': 'q', 'value': 'r'}
        monkeypatch.setattr(testee, 'AttributeDialog', MockDialog)
        monkeypatch.setattr(testee.Editor, 'checkselection', mock_check)
        monkeypatch.setattr(testee, 'show_dialog', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.get_node_title = mock_get
        testobj.getshortname = mock_getshortname
        testobj.mark_dirty = mock_mark
        testobj.edit()
        assert capsys.readouterr().out == 'called Editor.checkselection with args {}\n'
        monkeypatch.setattr(testee.Editor, 'checkselection', mock_check_2)
        testobj.edit()
        assert capsys.readouterr().out == (
            "called Editor.checkselection with args {}\n"
            "called Gui.get_node_title with arg `item`\n"
            "called Gui.get_node_data with arg `item`\n"
            "called AttributeDialog.__init__ with args"
            f" ({testobj},) {{'title': 'Edit an attribute',"
            " 'item': {'item': 'item', 'name': 'node', 'value': 'data'}}\n"
            "called show_dialog with args ('AttributeDialogGui',)\n")
        monkeypatch.setattr(testee, 'show_dialog', mock_show_2)
        testobj.edit()
        assert capsys.readouterr().out == (
            "called Editor.checkselection with args {}\n"
            "called Gui.get_node_title with arg `item`\n"
            "called Gui.get_node_data with arg `item`\n"
            "called AttributeDialog.__init__ with args"
            f" ({testobj},) {{'title': 'Edit an attribute',"
            " 'item': {'item': 'item', 'name': 'node', 'value': 'data'}}\n"
            "called show_dialog with args ('AttributeDialogGui',)\n"
            "called Editor.getshortname with args (('q', 'r'),) {'is_attr': True}\n"
            "called Gui.edit_item with args"
            " ('item', ('title', 'node', 'data'), ('q-r', 'q', 'r'), 'Edit Attribute')\n"
            "called Editor.mark_dirty with args (True,)\n")
        testobj.gui.get_node_data = mock_get_data
        testobj.edit()
        assert capsys.readouterr().out == (
            "called Editor.checkselection with args {}\n"
            "called Gui.get_node_title with arg `item`\n"
            "called Gui.get_node_data with arg `item`\n"
            "called AttributeDialog.__init__ with args"
            f" ({testobj},) {{'title': 'Edit an attribute',"
            " 'item': {'item': 'item', 'name': 'node', 'value': ''}}\n"
            "called show_dialog with args ('AttributeDialogGui',)\n"
            "called Editor.getshortname with args (('q', 'r'),) {'is_attr': True}\n"
            "called Gui.edit_item with args"
            " ('item', ('title', 'node', ''), ('q-r', 'q', 'r'), 'Edit Attribute')\n"
            "called Editor.mark_dirty with args (True,)\n")

    def test_cut(self, monkeypatch, capsys):
        """unittest for Editor.cut
        """
        def mock_editor_copy(*args, **kwargs):
            """stub
            """
            print('called Editor.copy with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.copy = mock_editor_copy
        testobj.cut()
        assert capsys.readouterr().out == "called Editor.copy with args () {'cut': True}\n"

    def test_delete(self, monkeypatch, capsys):
        """unittest for Editor.delete
        """
        def mock_editor_copy(*args, **kwargs):
            """stub
            """
            print('called Editor.copy with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.copy = mock_editor_copy
        testobj.delete()
        assert capsys.readouterr().out == ("called Editor.copy with args () {'cut': True,"
                                           " 'retain': False}\n")

    def test_get_copy_text(self, monkeypatch, capsys):
        """unittest for Editor.get_copy_text
        """
        # wordt in hierna volgende routine meegetest bij het opbouwen van de foutmelding
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_copy_text(False, False) == "copy"  # eigenlijk onjuist maar komt niet voor
        assert testobj.get_copy_text(False, True) == "copy"
        assert testobj.get_copy_text(True, False) == "delete"
        assert testobj.get_copy_text(True, True) == "cut"

    def test_copy(self, monkeypatch, capsys):
        """unittest for Editor.copy
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.checkselection = lambda *x: False
        testobj.copy()
        assert capsys.readouterr().out == ''
        testobj.checkselection = lambda *x: True
        testobj.item = 'item'
        testobj.copy()
        assert capsys.readouterr().out == (
                "called Gui.get_node_parentpos with arg `item`\n"
                "called Gui.copy with args ('item',) {'cut': False, 'retain': True}\n")
        monkeypatch.setattr(testobj.gui, 'get_node_parentpos', lambda *x: ('treetop', 0))
        testobj.copy()
        assert capsys.readouterr().out == (
                'called Gui.meldfout with args ("Can\'t copy the root",) {}\n')
        testobj.copy(cut=True)
        assert capsys.readouterr().out == (
                'called Gui.meldfout with args ("Can\'t cut the root",) {}\n')
        testobj.copy(cut=True, retain=False)
        assert capsys.readouterr().out == (
                'called Gui.meldfout with args ("Can\'t delete the root",) {}\n')

    def test_paste_after(self, monkeypatch, capsys):
        """unittest for Editor.paste_after
        """
        def mock_editor_paste(*args, **kwargs):
            """stub
            """
            print('called Editor.paste with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.paste = mock_editor_paste
        testobj.paste_after()
        assert capsys.readouterr().out == ("called Editor.paste with args () {'before': False}\n")

    def test_paste_under(self, monkeypatch, capsys):
        """unittest for Editor.paste_under
        """
        def mock_editor_paste(*args, **kwargs):
            """stub
            """
            print('called Editor.paste with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.paste = mock_editor_paste
        testobj.paste_under()
        assert capsys.readouterr().out == "called Editor.paste with args () {'below': True}\n"

    def test_paste(self, monkeypatch, capsys):
        """unittest for Editor.paste
        """
        def mock_get_title(node):
            """stub
            """
            return f'{testee.ELSTART} element'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.checkselection = lambda *x: False
        testobj.paste()
        assert capsys.readouterr().out == ''
        testobj.checkselection = lambda *x: True
        testobj.item = 'item'
        testobj.paste()
        assert capsys.readouterr().out == (
                "called Gui.get_node_parentpos with arg `item`\n"
                "called Gui.paste with args ('item',) {'before': True, 'below': False}\n")
        testobj.gui.get_node_parentpos = lambda *x: ('treetop', 0)
        testobj.paste()
        assert capsys.readouterr().out == (
                'called Gui.meldfout with args ("Can\'t paste before the root",) {}\n')
        testobj.paste(below=True)
        assert capsys.readouterr().out == (
                "called Gui.get_node_title with arg `item`\n"
                'called Gui.meldfout with args ("Can\'t paste below an attribute",) {}\n')
        testobj.gui.get_node_title = mock_get_title
        testobj.paste(before=False)
        assert capsys.readouterr().out == (
                "called Gui.meldinfo with args ('Pasting as first element below root',) {}\n"
                # 'called Gui.get_node_title with arg `item`\n'
                "called Gui.paste with args ('item',) {'before': False, 'below': True}\n")
        testobj.paste(below=True)
        assert capsys.readouterr().out == (
                # "called Gui.get_node_title with arg `item`\n"
                "called Gui.paste with args ('item',) {'before': True, 'below': True}\n")

    def test_add_attr(self, monkeypatch, capsys):
        """unittest for Editor.add_attr
        """
        def mock_get_title(node):
            """stub
            """
            print(f'called Gui.get_node_title with arg `{node}`')
            return f'{testee.ELSTART} element'
        def mock_show(*args):
            print('called show_dialog with args', args)
            return False
        def mock_show_2(*args):
            print('called show_dialog with args', args)
            return True
        def mock_mark(*args):
            print('called Editor.mark_dirty with args', args)
        class MockDialog:
            "stub"
            def __init__(self, *args, **kwargs):
                print('called AttributeDialog.__init__ with args', args, kwargs)
                self.gui = 'AttributeDialogGui'
                args[0].data = {'name': 'q', 'value': 'r'}
        monkeypatch.setattr(testee, 'show_dialog', mock_show)
        monkeypatch.setattr(testee, 'AttributeDialog', MockDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        # testobj.gui = MockGui()
        testobj.mark_dirty = mock_mark
        testobj.checkselection = lambda *x: False
        testobj.add_attr()
        assert capsys.readouterr().out == ''
        testobj.checkselection = lambda *x: True
        testobj.item = 'item'
        testobj.add_attr()
        assert capsys.readouterr().out == (
                'called Gui.get_node_title with arg `item`\n'
                'called Gui.meldfout with args ("Can\'t add attribute to attribute",) {}\n')
        testobj.gui.get_node_title = mock_get_title
        testobj.add_attr()
        assert capsys.readouterr().out == (
                'called Gui.get_node_title with arg `item`\n'
                f"called AttributeDialog.__init__ with args ({testobj},)"
                " {'title': 'New attribute', 'item': {'item': 'item', 'name': '', 'value': ''}}\n"
                "called show_dialog with args ('AttributeDialogGui',)\n")
        monkeypatch.setattr(testee, 'show_dialog', mock_show_2)
        testobj.add_attr()
        assert capsys.readouterr().out == (
                'called Gui.get_node_title with arg `item`\n'
                f"called AttributeDialog.__init__ with args ({testobj},)"
                " {'title': 'New attribute', 'item': {'item': 'item', 'name': '', 'value': ''}}\n"
                "called show_dialog with args ('AttributeDialogGui',)\n"
                "called Gui.add_attribute with args ('item', 'q', 'r', 'Insert Attribute')\n"
                "called Editor.mark_dirty with args (True,)\n")

    def test_insert_after(self, monkeypatch, capsys):
        """unittest for Editor.insert_after
        """
        def mock_insert(*args, **kwargs):
            """stub
            """
            print('called Editor.insert with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.insert = mock_insert
        testobj.insert_after()
        assert capsys.readouterr().out == "called Editor.insert with args () {'before': False}\n"

    def test_insert_child(self, monkeypatch, capsys):
        """unittest for Editor.insert_child
        """
        def mock_insert(*args, **kwargs):
            """stub
            """
            print('called Editor.insert with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.insert = mock_insert
        testobj.insert_child()
        assert capsys.readouterr().out == "called Editor.insert with args () {'below': True}\n"

    def test_insert(self, monkeypatch, capsys):
        """unittest for Editor.insert
        """
        def mock_get_title(node):
            """stub
            """
            return f'{testee.ELSTART} element'
        def mock_show(*args):
            print('called show_dialog with args', args)
            return False
        def mock_show_2(*args):
            print('called show_dialog with args', args)
            return True
        def mock_mark(*args):
            print('called Editor.mark_dirty with args', args)
        class MockDialog:
            "stub"
            def __init__(self, *args, **kwargs):
                print('called ElementDialog.__init__ with args', args, kwargs)
                self.gui = 'ElementDialogGui'
                args[0].data = {'tag': 'x', 'text': 'y'}
        monkeypatch.setattr(testee, 'show_dialog', mock_show)
        monkeypatch.setattr(testee, 'ElementDialog', MockDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mark_dirty = mock_mark
        testobj.checkselection = lambda *x: False
        testobj.insert()
        assert capsys.readouterr().out == ''
        testobj.checkselection = lambda *x: True
        testobj.item = 'item'
        testobj.insert()
        assert capsys.readouterr().out == (
                "called Gui.get_node_parentpos with arg `item`\n"
                f"called ElementDialog.__init__ with args ({testobj},)"
                " {'title': 'New element', 'item': {'item': 'item', 'tag': '', 'text': ''}}\n"
                "called show_dialog with args ('ElementDialogGui',)\n")
        testobj.gui.get_node_parentpos = lambda *x: ('treetop', 0)
        testobj.insert()
        assert capsys.readouterr().out == (
                'called Gui.meldinfo with args ("Can\'t insert before or after the root",) {}\n')
        testobj.insert(below=True)
        assert capsys.readouterr().out == (
                'called Gui.get_node_title with arg `item`\n'
                'called Gui.meldfout with args ("Can\'t insert below an attribute",) {}\n')
        monkeypatch.setattr(testobj.gui, 'get_node_title', mock_get_title)
        testobj.insert(below=True)
        assert capsys.readouterr().out == (
                f"called ElementDialog.__init__ with args ({testobj},)"
                " {'title': 'New element', 'item': {'item': 'item', 'tag': '', 'text': ''}}\n"
                "called show_dialog with args ('ElementDialogGui',)\n")
        monkeypatch.setattr(testee, 'show_dialog', mock_show_2)
        testobj.insert(below=True)
        assert capsys.readouterr().out == (
                f"called ElementDialog.__init__ with args ({testobj},)"
                " {'title': 'New element', 'item': {'item': 'item', 'tag': '', 'text': ''}}\n"
                "called show_dialog with args ('ElementDialogGui',)\n"
                "called Gui.insert with args ('item', 'x', 'y', 'Insert Element')"
                " {'before': True, 'below': True}\n"
                "called Editor.mark_dirty with args (True,)\n")

    def test_search(self, monkeypatch, capsys):
        """unittest for Editor.search
        """
        def mock_set(arg):
            print(f"called EditorGui,set_selected_item with arg '{arg}'")
        def mock_find_first(*args, **kwargs):
            """stub        """
            print('called Editor.find_first with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.top = 'top item'
        testobj.gui.set_selected_item = mock_set
        testobj.find_first = mock_find_first
        testobj.search()
        assert capsys.readouterr().out == ("called EditorGui,set_selected_item with arg 'top item'\n"
                                           "called Editor.find_first with args () {}\n")

    def test_search_from_here(self, monkeypatch, capsys):
        """unittest for Editor.search_from_here
        """
        def mock_find_first(*args, **kwargs):
            """stub        """
            print('called Editor.find_first with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.find_first = mock_find_first
        testobj.search_from_here()
        assert capsys.readouterr().out == "called Editor.find_first with args () {}\n"

    def test_search_last(self, monkeypatch, capsys):
        """unittest for Editor.search_last
        """
        def mock_set(arg):
            print(f"called EditorGui,set_selected_item with arg '{arg}'")
        def mock_find_first(*args, **kwargs):
            """stub
            """
            print('called Editor.find_first with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.top = 'top item'
        testobj.gui.set_selected_item = mock_set
        testobj.find_first = mock_find_first
        testobj.search_last()
        assert capsys.readouterr().out == ("called EditorGui,set_selected_item with arg 'top item'\n"
                                           "called Editor.find_first with args () {'reverse': True}\n")

    def test_search_backwards_from_here(self, monkeypatch, capsys):
        """unittest for Editor.search_backwards_from_here
        """
        def mock_find_first(*args, **kwargs):
            """stub
            """
            print('called Editor.find_first with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.find_first = mock_find_first
        testobj.search_backwards_from_here()
        assert capsys.readouterr().out == "called Editor.find_first with args () {'reverse': True}\n"

    def test_search_next(self, monkeypatch, capsys):
        """unittest for Editor.search_next
        """
        def mock_find_next(*args, **kwargs):
            """stub
            """
            print('called Editor.find_next with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.find_next = mock_find_next
        testobj.search_next()
        assert capsys.readouterr().out == (
                "called Editor.find_next with args () {'from_the_top': False}\n")

    def test_search_prev(self, monkeypatch, capsys):
        """unittest for Editor.search_prev
        """
        def mock_find_next(*args, **kwargs):
            """stub
            """
            print('called Editor.find_next with args', args, kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.find_next = mock_find_next
        testobj.search_prev()
        assert capsys.readouterr().out == (
                "called Editor.find_next with args () {'from_the_top': False, 'reverse': True}\n")

    def test_build_search_description(self, monkeypatch, capsys):
        """unittest for Editor.build_search_description
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.build_search_description("", '', '', '') == ['']
        assert testobj.build_search_description("xxxx", '', '', '') == ['search for',
                                                                        ' an element that has a name',
                                                                        '   containing `xxxx`']
        assert testobj.build_search_description("", 'yyyy', '', '') == [
                'search for an attribute that has a name',
                '   containing `yyyy`']
        assert testobj.build_search_description("", '', 'zzzz', '') == [
                'search for an attribute that has a value',
                '   containing `zzzz`']
        assert testobj.build_search_description("", '', '', 'qqqq') == ['search for text',
                                                                        '   `qqqq`']
        assert testobj.build_search_description("xxxx", 'yyyy', '', '') == [
                'search for',
                ' an element that has a name',
                '   containing `xxxx`',
                ' with an attribute that has a name',
                '   containing `yyyy`']
        assert testobj.build_search_description("xxxx", '', 'zzzz', '') == [
                'search for',
                ' an element that has a name',
                '   containing `xxxx`',
                ' with an attribute that has a value',
                '   containing `zzzz`']
        assert testobj.build_search_description("xxxx", '', '', 'qqqq') == [
                'search for text',
                '   `qqqq`',
                ' under an element that has a name',
                '   containing `xxxx`']
        assert testobj.build_search_description("", 'yyyy', 'zzzz', '') == [
                'search for an attribute that has a name',
                '   containing `yyyy`',
                ' and a value',
                '   containing `zzzz`']
        assert testobj.build_search_description("", 'yyyy', '', 'qqqq') == [
                'search for text',
                '   `qqqq`',
                ' under an element with',
                ' an attribute that has a name',
                '   containing `yyyy`']
        assert testobj.build_search_description("", '', 'zzzz', 'qqqq') == [
                'search for text',
                '   `qqqq`',
                ' under an element with',
                ' an attribute that has a value',
                '   containing `zzzz`']
        assert testobj.build_search_description("xxxx", 'yyyy', 'zzzz', '') == [
               'search for',
               ' an element that has a name',
               '   containing `xxxx`',
               ' with an attribute that has a name',
               '   containing `yyyy`',
               ' and a value',
               '   containing `zzzz`']
        assert testobj.build_search_description("xxxx", 'yyyy', '', 'qqqq') == [
               'search for text',
               '   `qqqq`',
               ' under an element that has a name',
               '   containing `xxxx`',
               ' with an attribute that has a name',
               '   containing `yyyy`']
        assert testobj.build_search_description("xxxx", '', 'zzzz', 'qqqq') == [
                'search for text',
                '   `qqqq`',
                ' under an element that has a name',
                '   containing `xxxx`',
                ' with an attribute that has a value',
                '   containing `zzzz`']
        assert testobj.build_search_description("", 'yyyy', 'zzzz', 'qqqq') == [
               'search for text',
               '   `qqqq`',
               ' under an element with',
               ' an attribute that has a name',
               '   containing `yyyy`',
               ' and a value',
               '   containing `zzzz`']
        assert testobj.build_search_description("xxxx", 'yyyy', 'zzzz', 'qqqq') == [
               'search for text',
               '   `qqqq`',
               ' under an element that has a name',
               '   containing `xxxx`',
               ' with an attribute that has a name',
               '   containing `yyyy`',
               ' and a value',
               '   containing `zzzz`']

    def test_replace(self, monkeypatch, capsys):
        """unittest for Editor.replace
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.replace()
        assert capsys.readouterr().out == ("called Gui.meldinfo with args"
                                           " ('Replace: not sure if I wanna implement this',) {}\n")


class TestXMLTree:
    """unittests for main.XMLTree
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.XMLTree object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called XMLTree.__init__ with args', args)
        monkeypatch.setattr(testee.XMLTree, '__init__', mock_init)
        testobj = testee.XMLTree()
        assert capsys.readouterr().out == 'called XMLTree.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for XMLTree.__init__
        """
        monkeypatch.setattr(testee.et, 'Element', lambda x: f'Element({x})')
        testobj = testee.XMLTree('data')
        assert testobj.root == 'Element(data)'

    def test_expand(self, monkeypatch, capsys):
        """unittest for XMLTree.expand
        """
        # testobj = self.setup_testobj(monkeypatch, capsys)
        def mock_init(self):
            """stub
            """
        class MockElement:
            """stub
            """
            def set(self, *args):
                """stub
                """
                print("called Element.set with args", args)
        class MockSubel:
            """stub
            """
            def __init__(self, *args):
                print("called SubElement.__init__ with args", args)
        monkeypatch.setattr(testee.et, 'Element', MockElement)
        monkeypatch.setattr(testee.et, 'SubElement', MockSubel)  # lambda x: f'SubElement({x})')
        monkeypatch.setattr(testee.XMLTree, '__init__', mock_init)
        testobj = testee.XMLTree()
        mock_root = MockElement()
        assert testobj.expand(mock_root, 'text', ('da', 'ta')) is None
        assert capsys.readouterr().out == "called Element.set with args ('da', 'ta')\n"
        result = testobj.expand(mock_root, '<> text', ('data', ''))
        assert isinstance(result, testee.et.SubElement)
        assert capsys.readouterr().out == f"called SubElement.__init__ with args ({mock_root}, 'data')\n"
        node = testobj.expand(mock_root, '<> text', ('da', 'ta'))
        assert isinstance(node, testee.et.SubElement)
        assert node.text == 'ta'
        assert capsys.readouterr().out == f"called SubElement.__init__ with args ({mock_root}, 'da')\n"

    def test_write(self, monkeypatch, capsys):
        """unittest for XMLTree.write
        """
        # testobj = self.setup_testobj(monkeypatch, capsys)
        def mock_init(self):
            """stub
            """
        def mock_register(*args):
            """stub
            """
            print('called register_namespace with args', args)
        class MockEtree:
            """stub
            """
            def __init__(self, arg):
                print(f'called ElementTree.__init__ with arg `{arg}`')
            def write(self, *args, **kwargs):
                """stub
                """
                print('called ElementTree.write with args', args, kwargs)
        monkeypatch.setattr(testee.et, 'ElementTree', MockEtree)
        monkeypatch.setattr(testee.et, 'register_namespace', mock_register)
        monkeypatch.setattr(testee.XMLTree, '__init__', mock_init)
        testobj = testee.XMLTree()
        testobj.root = 'myroot'
        testobj.write('to_file')
        assert capsys.readouterr().out == ('called ElementTree.__init__ with arg `myroot`\n'
                                           "called ElementTree.write with args ('to_file',)"
                                           " {'encoding': 'utf-8', 'xml_declaration': True}\n")
        testobj.write('to_file', (['x', 'y'], ['a', 'b']))
        assert capsys.readouterr().out == ('called ElementTree.__init__ with arg `myroot`\n'
                                           "called register_namespace with args ('x', 'a')\n"
                                           "called register_namespace with args ('y', 'b')\n"
                                           "called ElementTree.write with args ('to_file',)"
                                           " {'encoding': 'utf-8', 'xml_declaration': True}\n")


def test_find_in_flattened_tree(monkeypatch, capsys):
    """unittest for base.find_in_flattened_tree
    """
    def mock_get(*args):
        print('called Editor.get_remaining_data_to_search with args', args)
        return []
    def mock_get_2(*args):
        print('called Editor.get_remaining_data_to_search with args', args)
        return args[1]  # [args[0]:]
    def mock_apply_ele(*args):
        print('called apply_search_criteria_for_element with args', args)
        return False
    def mock_apply_ele_2(*args):
        print('called apply_search_criteria_for_element with args', args)
        return True
    def mock_apply_att(*args):
        print('called apply_search_criteria_for_attrs with args', args)
        return False, None
    def mock_apply_att_2(*args):
        print('called apply_search_criteria_for_attrs with args', args)
        return True, 'node'
    def mock_apply_att_3(*args):
        print('called apply_search_criteria_for_attrs with args', args)
        return True, None
    def mock_apply_txt(*args):
        print('called apply_search_criteria_for_text with args', args)
        return False
    def mock_apply_txt_2(*args):
        print('called apply_search_criteria_for_text with args', args)
        return True
    monkeypatch.setattr(testee, 'get_remaining_data_to_search', mock_get)
    monkeypatch.setattr(testee, 'apply_search_criteria_for_element', mock_apply_ele)
    monkeypatch.setattr(testee, 'apply_search_criteria_for_attrs', mock_apply_att)
    monkeypatch.setattr(testee, 'apply_search_criteria_for_text', mock_apply_txt)
    data = []
    search_args = ['xx', 'yy', 'zz', 'qq']
    assert testee.find_in_flattened_tree(data, search_args, True) == (None, False)
    assert capsys.readouterr().out == ("")
    assert testee.find_in_flattened_tree(data, search_args, True, pos=3) == (None, False)
    assert capsys.readouterr().out == ""
    assert testee.find_in_flattened_tree(data, search_args, False, pos=3) == (None, False)
    assert capsys.readouterr().out == ("called Editor.get_remaining_data_to_search with args"
                                       " (3, [], ['xx', 'yy', 'zz', 'qq'])\n")
    data = [('item', 'a name', 'a text', 'a list')]
    assert testee.find_in_flattened_tree(data, search_args, True) == (None, False)
    assert capsys.readouterr().out == (
            "called apply_search_criteria_for_element with args ('xx', 'a name')\n"
            "called apply_search_criteria_for_attrs with args"
            " (['xx', 'yy', 'zz', 'qq'], 'a list', False)\n"
            "called apply_search_criteria_for_text with args ('qq', 'a text')\n")
    monkeypatch.setattr(testee, 'apply_search_criteria_for_element', mock_apply_ele_2)
    assert testee.find_in_flattened_tree(data, search_args, True) == (None, False)
    assert capsys.readouterr().out == (
            "called apply_search_criteria_for_element with args ('xx', 'a name')\n"
            "called apply_search_criteria_for_attrs with args"
            " (['xx', 'yy', 'zz', 'qq'], 'a list', False)\n"
            "called apply_search_criteria_for_text with args ('qq', 'a text')\n")
    monkeypatch.setattr(testee, 'apply_search_criteria_for_attrs', mock_apply_att_2)
    assert testee.find_in_flattened_tree(data, search_args, True) == (None, False)
    assert capsys.readouterr().out == (
            "called apply_search_criteria_for_element with args ('xx', 'a name')\n"
            "called apply_search_criteria_for_attrs with args"
            " (['xx', 'yy', 'zz', 'qq'], 'a list', False)\n"
            "called apply_search_criteria_for_text with args ('qq', 'a text')\n")
    monkeypatch.setattr(testee, 'apply_search_criteria_for_text', mock_apply_txt_2)
    assert testee.find_in_flattened_tree(data, search_args, True) == ('node', True)
    assert capsys.readouterr().out == (
            "called apply_search_criteria_for_element with args ('xx', 'a name')\n"
            "called apply_search_criteria_for_attrs with args"
            " (['xx', 'yy', 'zz', 'qq'], 'a list', False)\n"
            "called apply_search_criteria_for_text with args ('qq', 'a text')\n")
    monkeypatch.setattr(testee, 'apply_search_criteria_for_attrs', mock_apply_att_3)
    assert testee.find_in_flattened_tree(data, search_args, True) == ('item', False)
    assert capsys.readouterr().out == (
            "called apply_search_criteria_for_element with args ('xx', 'a name')\n"
            "called apply_search_criteria_for_attrs with args"
            " (['xx', 'yy', 'zz', 'qq'], 'a list', False)\n"
            "called apply_search_criteria_for_text with args ('qq', 'a text')\n")
    data = [('item', 'a name', 'a text', 'a list'), ('item 2', 'name 2', 'text 2', 'list 2')]
    assert testee.find_in_flattened_tree(data, search_args, True) == ('item', False)
    assert capsys.readouterr().out == (
            "called apply_search_criteria_for_element with args ('xx', 'a name')\n"
            "called apply_search_criteria_for_attrs with args"
            " (['xx', 'yy', 'zz', 'qq'], 'a list', False)\n"
            "called apply_search_criteria_for_text with args ('qq', 'a text')\n")
    assert testee.find_in_flattened_tree(data, search_args, True, True) == ('item 2', False)
    assert capsys.readouterr().out == (
            "called apply_search_criteria_for_element with args ('xx', 'name 2')\n"
            "called apply_search_criteria_for_attrs with args"
            " (['xx', 'yy', 'zz', 'qq'], 'list 2', True)\n"
            "called apply_search_criteria_for_text with args ('qq', 'text 2')\n")
    monkeypatch.setattr(testee, 'get_remaining_data_to_search', mock_get_2)
    assert testee.find_in_flattened_tree(data, search_args, True, pos=3) == ('item 2', False)
    assert capsys.readouterr().out == (
            "called apply_search_criteria_for_element with args ('xx', 'name 2')\n"
            "called apply_search_criteria_for_attrs with args"
            " (['xx', 'yy', 'zz', 'qq'], 'list 2', False)\n"
            "called apply_search_criteria_for_text with args ('qq', 'text 2')\n")
    assert testee.find_in_flattened_tree(data, search_args, False, pos=3) == ('item 2', False)
    assert capsys.readouterr().out == (
            "called Editor.get_remaining_data_to_search with args"
            f" (3, {data}, ['xx', 'yy', 'zz', 'qq'])\n"
            "called apply_search_criteria_for_element with args ('xx', 'name 2')\n"
            "called apply_search_criteria_for_attrs with args"
            " (['xx', 'yy', 'zz', 'qq'], 'list 2', False)\n"
            "called apply_search_criteria_for_text with args ('qq', 'text 2')\n")


def test_get_remaining_data_to_search():
    """unittest for base.get_remaining_data_to_search
    """
    data = [(0, 'x'), (1, 'y'), (2, 'z')]
    sargs = ['xx', 'yy', 'zz', 'qq']
    assert testee.get_remaining_data_to_search((0, False), data, sargs) == [(1, 'y'), (2, 'z')]
    assert testee.get_remaining_data_to_search((1, False), data, sargs) == [(2, 'z')]
    assert testee.get_remaining_data_to_search((2, False), data, sargs) == []
    assert testee.get_remaining_data_to_search((3, False), data, sargs) == []
    data = [(0, 'x', 'xx', [(1, 'a'), (2, 'b')]), (3, 'y', 'yy', [(4, 'c'), (5, 'd')]),
            (6, 'z', 'zz', [(7, 'e'), (8, 'f')])]
    assert testee.get_remaining_data_to_search((0, False), data, sargs) == [
           (3, 'y', 'yy', [(4, 'c'), (5, 'd')]), (6, 'z', 'zz', [(7, 'e'), (8, 'f')])]
    sargs = ['', 'yy', 'zz', 'qq']
    assert testee.get_remaining_data_to_search((0, False), data, sargs) == [
           (3, 'y', 'yy', [(4, 'c'), (5, 'd')]), (6, 'z', 'zz', [(7, 'e'), (8, 'f')])]
    sargs = ['xx', 'yy', 'zz', '']
    assert testee.get_remaining_data_to_search((0, False), data, sargs) == [
           (3, 'y', 'yy', [(4, 'c'), (5, 'd')]), (6, 'z', 'zz', [(7, 'e'), (8, 'f')])]
    sargs = ['', 'yy', 'zz', '']
    assert testee.get_remaining_data_to_search((0, False), data, sargs) == [
           (0, 'x', 'xx', [(1, 'a'), (2, 'b')]), (3, 'y', 'yy', [(4, 'c'), (5, 'd')]),
           (6, 'z', 'zz', [(7, 'e'), (8, 'f')])]
    sargs = ['xx', 'yy', 'zz', 'qq']
    assert testee.get_remaining_data_to_search((0, True), data, sargs) == [(6, 'z', 'zz', [])]
    assert testee.get_remaining_data_to_search((1, False), data, sargs) == []
    assert testee.get_remaining_data_to_search((1, True), data, sargs) == [
           (0, 'x', 'xx', [(2, 'b')]), (3, 'y', 'yy', [(4, 'c'), (5, 'd')]),
           (6, 'z', 'zz', [(7, 'e'), (8, 'f')])]

    assert testee.get_remaining_data_to_search((2, False), data, sargs) == []
    assert testee.get_remaining_data_to_search((2, True), data, sargs) == [
            (0, 'x', 'xx', []), (3, 'y', 'yy', [(4, 'c'), (5, 'd')]),
            (6, 'z', 'zz', [(7, 'e'), (8, 'f')])]
    assert testee.get_remaining_data_to_search((3, False), data, sargs) == [
            (6, 'z', 'zz', [(7, 'e'), (8, 'f')])]
    assert testee.get_remaining_data_to_search((3, True), data, sargs) == [(6, 'z', 'zz', [])]
    assert testee.get_remaining_data_to_search((4, False), data, sargs) == []
    assert testee.get_remaining_data_to_search((4, True), data, sargs) == [
           (3, 'y', 'yy', [(5, 'd')]), (6, 'z', 'zz', [(7, 'e'), (8, 'f')])]
    assert testee.get_remaining_data_to_search((5, False), data, sargs) == []
    assert testee.get_remaining_data_to_search((5, True), data, sargs) == [
           (3, 'y', 'yy', []), (6, 'z', 'zz', [(7, 'e'), (8, 'f')])]
    assert testee.get_remaining_data_to_search((6, False), data, sargs) == []
    assert testee.get_remaining_data_to_search((6, True), data, sargs) == [(6, 'z', 'zz', [])]
    assert testee.get_remaining_data_to_search((7, False), data, sargs) == []
    assert testee.get_remaining_data_to_search((7, True), data, sargs) == [
            (6, 'z', 'zz', [(8, 'f')])]
    assert testee.get_remaining_data_to_search((8, False), data, sargs) == []
    assert testee.get_remaining_data_to_search((8, True), data, sargs) == [(6, 'z', 'zz', [])]
    assert testee.get_remaining_data_to_search((9, False), data, sargs) == []
    # dit lijkt me ook niet goed:
    assert testee.get_remaining_data_to_search((9, True), data, sargs) == [(6, 'z', 'zz', [])]
    assert testee.get_remaining_data_to_search((10, True), data, sargs) == [(6, 'z', 'zz', [])]
    assert testee.get_remaining_data_to_search((11, True), data, sargs) == [(6, 'z', 'zz', [])]


def test_apply_search_criteria_for_element():
    """unittest for base.apply_search_criteria_for_element
    """
    assert testee.apply_search_criteria_for_element('', 'element_name')
    assert testee.apply_search_criteria_for_element('men', 'element_name')
    assert not testee.apply_search_criteria_for_element('met', 'element_name')


def test_apply_search_criteria_for_text():
    """unittest for base.apply_search_criteria_for_text
    """
    assert testee.apply_search_criteria_for_text('', 'element text')
    assert testee.apply_search_criteria_for_text('ment tex', 'element text')
    assert not testee.apply_search_criteria_for_text('me tex', 'element text')


def test_apply_search_criteria_for_attrs():
    """unittest for base.apply_search_criteria_for_attrs
    """
    attrlist = [('node0', 'xxx', 'yyy'), ('node1', 'name1', 'value1'), ('node2', 'name2', 'value2')]
    criteria = ('', '', '', '')
    assert testee.apply_search_criteria_for_attrs(criteria, attrlist, False) == (True, None)
    criteria = ('', 'nam', '', '')
    assert testee.apply_search_criteria_for_attrs(criteria, attrlist, False) == (True, 'node1')
    criteria = ('', 'nam', '', '')
    assert testee.apply_search_criteria_for_attrs(criteria, attrlist, True) == (True, 'node2')
    attrlist = [('node0', 'xxx', 'yyy'), ('node1', 'name1', 'value1'), ('node2', 'name2', 'value2')]
    criteria = ('', '', 'val', '')
    assert testee.apply_search_criteria_for_attrs(criteria, attrlist, False) == (True, 'node1')
    criteria = ('', 'nam', 'value2', '')
    assert testee.apply_search_criteria_for_attrs(criteria, attrlist, False) == (True, 'node2')
    criteria = ('', 'name1', 'value2', '')
    assert testee.apply_search_criteria_for_attrs(criteria, attrlist, False) == (False, None)
    criteria = ('x', 'nam', '', '')
    assert testee.apply_search_criteria_for_attrs(criteria, attrlist, False) == (True, None)
    criteria = ('', 'nam', '', 'y')
    assert testee.apply_search_criteria_for_attrs(criteria, attrlist, False) == (True, None)
    criteria = ('xxx', '', '', 'yyy')
    assert testee.apply_search_criteria_for_attrs(criteria, [], False) == (True, None)
    assert testee.apply_search_criteria_for_attrs(criteria, [], True) == (True, None)
    criteria = ('xxx', 'yyy', '', 'zzz')
    assert testee.apply_search_criteria_for_attrs(criteria, [], False) == (False, None)
    assert testee.apply_search_criteria_for_attrs(criteria, [], True) == (False, None)
    criteria = ('xxx', '', 'yyy', 'zzz')
    assert testee.apply_search_criteria_for_attrs(criteria, [], False) == (False, None)
    assert testee.apply_search_criteria_for_attrs(criteria, [], True) == (False, None)


def test_parse_nsmap(monkeypatch, capsys):
    """unittest for base.parse_nsmap
    """
    def mock_iterparse(*args):
        """stub
        """
        print('called ElementTree.iterparse with args', args)
        return (('start-ns', ('ns-prefix', 'ns-uri')), ('start', 'newroot'), ('start', 'nextroot'),
                ('end-ns', ''))
    monkeypatch.setattr(testee.et, 'ElementTree', lambda x: f'ElementTree({x})')
    monkeypatch.setattr(testee.et, 'iterparse', mock_iterparse)
    assert testee.parse_nsmap('input') == ('ElementTree(newroot)', ['ns-prefix'], ['ns-uri'])
    assert capsys.readouterr().out == ("called ElementTree.iterparse with args ('input',"
                                       " ('start-ns', 'start'))\n")


class TestElementDialog:
    """unittests for main.ElementDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.ElementDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called ElementDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ElementDialog, '__init__', mock_init)
        testobj = testee.ElementDialog()
        assert capsys.readouterr().out == 'called ElementDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for ElementDialog.__init__
        """
        parent = types.SimpleNamespace(gui='MainGui', icon='XmlIcon', ns_uris=['aaa', 'yyy', 'bbb'])
        item = {'tag': 'xxx', 'text': 'qqqqq'}
        monkeypatch.setattr(testee, 'DialogGui', MockDialogGui)
        testobj = testee.ElementDialog(parent, title="", item=None)
        assert testobj.parent == parent
        assert capsys.readouterr().out == (
            f"called DialogGui.__init__ with args ({testobj}, 'MainGui', '') {{}}\n"
            "called DialogGui.add_label with args ('element name:  ', 0, 0) {}\n"
            "called DialogGui.add_lineinput with args (0, 1) {}\n"
            "called DialogGui.add_checkbox with args ('Namespace:', 1, 0) {}\n"
            "called DialogGui.add_combobox with args"
            " (['-- none --', 'aaa', 'yyy', 'bbb'], 1, 1)\n"
            "called DialogGui.add_checkbox with args ('Bevat data:', 2, 0) {'readonly': True}\n"
            "called DialogGui.add_textinput with args (3, 0)\n"
            "called DialogGui.add_buttons with args"
            f" ([('&Save', {testobj.gui.accept}, True),"
            f" ('&Cancel', {testobj.gui.reject}, False)],)\n"
            "called DialogGui.finish_display\n"
            "called DialogGui.set_focus_to with args ('lineinput',)\n")
        testobj = testee.ElementDialog(parent, title="title", item=item)
        assert testobj.parent == parent
        assert capsys.readouterr().out == (
            f"called DialogGui.__init__ with args ({testobj}, 'MainGui', 'title') {{}}\n"
            "called DialogGui.add_label with args ('element name:  ', 0, 0) {}\n"
            "called DialogGui.add_lineinput with args (0, 1) {}\n"
            "called DialogGui.add_checkbox with args ('Namespace:', 1, 0) {}\n"
            "called DialogGui.add_combobox with args"
            " (['-- none --', 'aaa', 'yyy', 'bbb'], 1, 1)\n"
            "called DialogGui.add_checkbox with args ('Bevat data:', 2, 0) {'readonly': True}\n"
            "called DialogGui.add_textinput with args (3, 0)\n"
            "called DialogGui.add_buttons with args"
            f" ([('&Save', {testobj.gui.accept}, True),"
            f" ('&Cancel', {testobj.gui.reject}, False)],)\n"
            "called DialogGui.finish_display\n"
            "called DialogGui.set_lineinput_text with args ('lineinput', 'xxx')\n"
            "called DialogGui.set_checkbox_state with args ('checkbox', True)\n"
            "called DialogGui.set_textinput_text with args ('textinput', 'qqqqq')\n"
            "called DialogGui.set_focus_to with args ('lineinput',)\n")
        item = {'tag': '{yyy}xxx'}
        testobj = testee.ElementDialog(parent, title="title", item=item)
        assert testobj.parent == parent
        assert capsys.readouterr().out == (
            f"called DialogGui.__init__ with args ({testobj}, 'MainGui', 'title') {{}}\n"
            "called DialogGui.add_label with args ('element name:  ', 0, 0) {}\n"
            "called DialogGui.add_lineinput with args (0, 1) {}\n"
            "called DialogGui.add_checkbox with args ('Namespace:', 1, 0) {}\n"
            "called DialogGui.add_combobox with args"
            " (['-- none --', 'aaa', 'yyy', 'bbb'], 1, 1)\n"
            "called DialogGui.add_checkbox with args ('Bevat data:', 2, 0) {'readonly': True}\n"
            "called DialogGui.add_textinput with args (3, 0)\n"
            "called DialogGui.add_buttons with args"
            f" ([('&Save', {testobj.gui.accept}, True),"
            f" ('&Cancel', {testobj.gui.reject}, False)],)\n"
            "called DialogGui.finish_display\n"
            "called DialogGui.set_lineinput_text with args ('lineinput', 'xxx')\n"
            "called DialogGui.set_checkbox_state with args ('checkbox', True)\n"
            "called DialogGui.set_combobox_index with args ('combobox', 2)\n"
            "called DialogGui.set_focus_to with args ('lineinput',)\n")
        # onbestaanbaar (?): namespace bij element komt niet voor in lijst met namespaces
        item = {'tag': '{zzz}xxx'}
        testobj = testee.ElementDialog(parent, title="title", item=item)
        assert testobj.parent == parent
        assert capsys.readouterr().out == (
            f"called DialogGui.__init__ with args ({testobj}, 'MainGui', 'title') {{}}\n"
            "called DialogGui.add_label with args ('element name:  ', 0, 0) {}\n"
            "called DialogGui.add_lineinput with args (0, 1) {}\n"
            "called DialogGui.add_checkbox with args ('Namespace:', 1, 0) {}\n"
            "called DialogGui.add_combobox with args"
            " (['-- none --', 'aaa', 'yyy', 'bbb'], 1, 1)\n"
            "called DialogGui.add_checkbox with args ('Bevat data:', 2, 0) {'readonly': True}\n"
            "called DialogGui.add_textinput with args (3, 0)\n"
            "called DialogGui.add_buttons with args"
            f" ([('&Save', {testobj.gui.accept}, True),"
            f" ('&Cancel', {testobj.gui.reject}, False)],)\n"
            "called DialogGui.finish_display\n"
            "called DialogGui.set_lineinput_text with args ('lineinput', 'xxx')\n"
            "called DialogGui.set_checkbox_state with args ('checkbox', True)\n"
            "called DialogGui.set_focus_to with args ('lineinput',)\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for ElementDialog.confirm
        """
        class MockGui:
            "stub"
            def get_lineinput_text(self, *args):
                print("called ElementDialogGui.get_lineinput_text with args", args)
                return tag_text
            def get_combobox_index(self, *args):
                print("called ElementDialogGui.get_combobox_index with args", args)
                return 0
            def get_combobox_itemtext(self, *args):
                print("called ElementDialogGui.get_combobox_itemtext with args", args)
                return 'combobox text'
            def get_checkbox_state(self, *args):
                print("called ElementDialogGui.get_checkbox_value with args", args)
                return False
            def get_textinput_text(self, *args):
                print("called ElementDialogGui.get_textinput_text with args", args)
                return 'text input'
            def set_focus_to(self, *args):
                print("called ElementDialogGui.set_focus_to with args", args)
        def mock_meld(*args):
            print('called MainGui.meldfout with args', args)
        def mock_get(*args):
            print("called ElementDialogGui.get_checkbox_value with args", args)
            return True
        def mock_get_index(*args):
            print("called ElementDialogGui.get_combobox_index with args", args)
            return 1
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(gui=types.SimpleNamespace(meldfout=mock_meld))
        testobj.gui = MockGui()
        testobj.txt_tag = 'txt_tag'
        testobj.cb_ns = 'cb_ns'
        testobj.cmb_ns = 'cmb_ns'
        testobj.cb_data = 'cb_data'
        testobj.txt_data = 'txt_data'
        tag_text = ''
        assert not testobj.confirm()
        assert capsys.readouterr().out == (
                "called ElementDialogGui.get_lineinput_text with args ('txt_tag',)\n"
                "called MainGui.meldfout with args ('Element name must not be empty',)\n"
                "called ElementDialogGui.set_focus_to with args ('txt_tag',)\n")
        tag_text = 'two words'
        assert not testobj.confirm()
        assert capsys.readouterr().out == (
                "called ElementDialogGui.get_lineinput_text with args ('txt_tag',)\n"
                "called MainGui.meldfout with args ('Element name must not contain spaces',)\n"
                "called ElementDialogGui.set_focus_to with args ('txt_tag',)\n")
        tag_text = '0-at-start'
        assert not testobj.confirm()
        assert capsys.readouterr().out == (
                "called ElementDialogGui.get_lineinput_text with args ('txt_tag',)\n"
                "called MainGui.meldfout with args ('Element name must not start with a digit',)\n"
                "called ElementDialogGui.set_focus_to with args ('txt_tag',)\n")
        tag_text = 'inputvalue'
        assert testobj.confirm()
        assert testobj.parent.data == {'data': False, 'tag': 'inputvalue', 'text': ''}
        assert capsys.readouterr().out == (
                "called ElementDialogGui.get_lineinput_text with args ('txt_tag',)\n"
                "called ElementDialogGui.get_checkbox_value with args ('cb_ns',)\n"
                "called ElementDialogGui.get_checkbox_value with args ('cb_data',)\n")
        testobj.gui.get_checkbox_state = mock_get
        assert not testobj.confirm()
        assert capsys.readouterr().out == (
                "called ElementDialogGui.get_lineinput_text with args ('txt_tag',)\n"
                "called ElementDialogGui.get_checkbox_value with args ('cb_ns',)\n"
                "called ElementDialogGui.get_combobox_index with args ('cmb_ns',)\n"
                "called MainGui.meldfout with args ('Namespace must be selected if checked',)\n"
                "called ElementDialogGui.set_focus_to with args ('cb_ns',)\n")
        testobj.gui.get_combobox_index = mock_get_index
        assert testobj.confirm()
        assert testobj.parent.data == {'data': True, 'tag': '{combobox text}inputvalue',
                                       'text': 'text input'}
        assert capsys.readouterr().out == (
                "called ElementDialogGui.get_lineinput_text with args ('txt_tag',)\n"
                "called ElementDialogGui.get_checkbox_value with args ('cb_ns',)\n"
                "called ElementDialogGui.get_combobox_index with args ('cmb_ns',)\n"
                "called ElementDialogGui.get_combobox_itemtext with args ('cmb_ns', 1)\n"
                "called ElementDialogGui.get_checkbox_value with args ('cb_data',)\n"
                "called ElementDialogGui.get_textinput_text with args ('txt_data',)\n")


class TestAttributeDialog:
    """unittests for main.AttributeDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.AttributeDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called AttributeDialog.__init__ with args', args)
        monkeypatch.setattr(testee.AttributeDialog, '__init__', mock_init)
        testobj = testee.AttributeDialog()
        assert capsys.readouterr().out == 'called AttributeDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for AttributeDialog.__init__
        """
        parent = types.SimpleNamespace(gui='MainGui', icon='XmlIcon', ns_uris=['aaa', 'yyy', 'bbb'])
        item = {'name': 'xxx', 'value': 'qqqqq'}
        monkeypatch.setattr(testee, 'DialogGui', MockDialogGui)
        testobj = testee.AttributeDialog(parent)
        assert testobj.parent == parent
        assert capsys.readouterr().out == (
            f"called DialogGui.__init__ with args ({testobj}, 'MainGui', '') {{}}\n"
            "called DialogGui.add_label with args ('Attribute name:', 0, 0) {}\n"
            "called DialogGui.add_lineinput with args (0, 1) {}\n"
            "called DialogGui.add_checkbox with args ('Namespace:', 1, 0) {}\n"
            "called DialogGui.add_combobox with args (['-- none --', 'aaa', 'yyy', 'bbb'], 1, 1)\n"
            "called DialogGui.add_label with args ('Attribute value:', 2, 0) {}\n"
            "called DialogGui.add_lineinput with args (2, 1) {}\n"
            "called DialogGui.add_buttons with args"
            f" ([('&Save', {testobj.gui.accept}, True),"
            f" ('&Cancel', {testobj.gui.reject}, False)],)\n"
            "called DialogGui.finish_display\n"
            "called DialogGui.set_focus_to with args ('lineinput',)\n")
        testobj = testee.AttributeDialog(parent, title="title", item=item)
        assert testobj.parent == parent
        assert capsys.readouterr().out == (
            f"called DialogGui.__init__ with args ({testobj}, 'MainGui', 'title') {{}}\n"
            "called DialogGui.add_label with args ('Attribute name:', 0, 0) {}\n"
            "called DialogGui.add_lineinput with args (0, 1) {}\n"
            "called DialogGui.add_checkbox with args ('Namespace:', 1, 0) {}\n"
            "called DialogGui.add_combobox with args (['-- none --', 'aaa', 'yyy', 'bbb'], 1, 1)\n"
            "called DialogGui.add_label with args ('Attribute value:', 2, 0) {}\n"
            "called DialogGui.add_lineinput with args (2, 1) {}\n"
            "called DialogGui.add_buttons with args"
            f" ([('&Save', {testobj.gui.accept}, True),"
            f" ('&Cancel', {testobj.gui.reject}, False)],)\n"
            "called DialogGui.finish_display\n"
            "called DialogGui.set_lineinput_text with args ('lineinput', 'xxx')\n"
            "called DialogGui.set_lineinput_text with args ('lineinput', 'qqqqq')\n"
            "called DialogGui.set_focus_to with args ('lineinput',)\n")
        item = {'name': '{yyy}xxx'}
        testobj = testee.AttributeDialog(parent, title="title", item=item)
        assert testobj.parent == parent
        assert capsys.readouterr().out == (
            f"called DialogGui.__init__ with args ({testobj}, 'MainGui', 'title') {{}}\n"
            "called DialogGui.add_label with args ('Attribute name:', 0, 0) {}\n"
            "called DialogGui.add_lineinput with args (0, 1) {}\n"
            "called DialogGui.add_checkbox with args ('Namespace:', 1, 0) {}\n"
            "called DialogGui.add_combobox with args (['-- none --', 'aaa', 'yyy', 'bbb'], 1, 1)\n"
            "called DialogGui.add_label with args ('Attribute value:', 2, 0) {}\n"
            "called DialogGui.add_lineinput with args (2, 1) {}\n"
            "called DialogGui.add_buttons with args"
            f" ([('&Save', {testobj.gui.accept}, True),"
            f" ('&Cancel', {testobj.gui.reject}, False)],)\n"
            "called DialogGui.finish_display\n"
            "called DialogGui.set_lineinput_text with args ('lineinput', 'xxx')\n"
            "called DialogGui.set_checkbox_state with args ('checkbox', True)\n"
            "called DialogGui.set_combobox_index with args ('combobox', 2)\n"
            "called DialogGui.set_lineinput_text with args ('lineinput', '')\n"
            "called DialogGui.set_focus_to with args ('lineinput',)\n")
        # onbestaanbaar (?): namespace bij element komt niet voor in lijst met namespaces
        item = {'name': '{zzz}xxx'}
        testobj = testee.AttributeDialog(parent, title="title", item=item)
        assert testobj.parent == parent
        assert capsys.readouterr().out == (
            f"called DialogGui.__init__ with args ({testobj}, 'MainGui', 'title') {{}}\n"
            "called DialogGui.add_label with args ('Attribute name:', 0, 0) {}\n"
            "called DialogGui.add_lineinput with args (0, 1) {}\n"
            "called DialogGui.add_checkbox with args ('Namespace:', 1, 0) {}\n"
            "called DialogGui.add_combobox with args (['-- none --', 'aaa', 'yyy', 'bbb'], 1, 1)\n"
            "called DialogGui.add_label with args ('Attribute value:', 2, 0) {}\n"
            "called DialogGui.add_lineinput with args (2, 1) {}\n"
            "called DialogGui.add_buttons with args"
            f" ([('&Save', {testobj.gui.accept}, True),"
            f" ('&Cancel', {testobj.gui.reject}, False)],)\n"
            "called DialogGui.finish_display\n"
            "called DialogGui.set_lineinput_text with args ('lineinput', 'xxx')\n"
            "called DialogGui.set_checkbox_state with args ('checkbox', True)\n"
            "called DialogGui.set_lineinput_text with args ('lineinput', '')\n"
            "called DialogGui.set_focus_to with args ('lineinput',)\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for AttributeDialog.confirm
        """
        class MockGui:
            "stub"
            def get_lineinput_text(self, *args):
                print("called ElementDialogGui.get_lineinput_text with args", args)
                return attr_text
            def get_combobox_index(self, *args):
                print("called ElementDialogGui.get_combobox_index with args", args)
                return 0
            def get_combobox_itemtext(self, *args):
                print("called ElementDialogGui.get_combobox_itemtext with args", args)
                return 'combobox text'
            def get_checkbox_value(self, *args):
                print("called ElementDialogGui.get_checkbox_value with args", args)
                return False
            def get_textinput_text(self, *args):
                print("called ElementDialogGui.get_textinput_text with args", args)
                return 'text input'
            def set_focus_to(self, *args):
                print("called ElementDialogGui.set_focus_to with args", args)
        def mock_meld(*args):
            print('called MainGui.meldfout with args', args)
        def mock_get(*args):
            print("called ElementDialogGui.get_checkbox_value with args", args)
            return True
        def mock_get_index(*args):
            print("called ElementDialogGui.get_combobox_index with args", args)
            return 1
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(gui=types.SimpleNamespace(meldfout=mock_meld))
        testobj.gui = MockGui()
        testobj.txt_name = 'txt_name'
        testobj.cb_ns = 'cb_ns'
        testobj.cmb_ns = 'cmb_ns'
        testobj.cb_data = 'cb_data'
        testobj.txt_value = 'txt_value'
        attr_text = ''
        assert not testobj.confirm()
        assert capsys.readouterr().out == (
                "called ElementDialogGui.get_lineinput_text with args ('txt_name',)\n"
                "called MainGui.meldfout with args ('Attribute name must not be empty',)\n"
                "called ElementDialogGui.set_focus_to with args ('txt_name',)\n")
        attr_text = 'two words'
        assert not testobj.confirm()
        assert capsys.readouterr().out == (
                "called ElementDialogGui.get_lineinput_text with args ('txt_name',)\n"
                "called MainGui.meldfout with args ('Attribute name must not contain spaces',)\n"
                "called ElementDialogGui.set_focus_to with args ('txt_name',)\n")
        attr_text = '0-at-begin'
        assert not testobj.confirm()
        assert capsys.readouterr().out == (
                "called ElementDialogGui.get_lineinput_text with args ('txt_name',)\n"
                "called MainGui.meldfout with args ('Attribute name must not start with a digit',)\n"
                "called ElementDialogGui.set_focus_to with args ('txt_name',)\n")
        attr_text = 'text'
        assert testobj.confirm()
        assert testobj.parent.data == {'name': 'text', 'value': 'text'}
        assert capsys.readouterr().out == (
                "called ElementDialogGui.get_lineinput_text with args ('txt_name',)\n"
                "called ElementDialogGui.get_checkbox_value with args ('cb_ns',)\n"
                "called ElementDialogGui.get_lineinput_text with args ('txt_value',)\n")
        testobj.gui.get_checkbox_value = mock_get
        assert not testobj.confirm()
        assert capsys.readouterr().out == (
                "called ElementDialogGui.get_lineinput_text with args ('txt_name',)\n"
                "called ElementDialogGui.get_checkbox_value with args ('cb_ns',)\n"
                "called ElementDialogGui.get_combobox_index with args ('cmb_ns',)\n"
                "called MainGui.meldfout with args ('Namespace must be selected if checked',)\n"
                "called ElementDialogGui.set_focus_to with args ('cb_ns',)\n")
        testobj.gui.get_combobox_index = mock_get_index
        assert testobj.confirm()
        assert testobj.parent.data == {'name': '{combobox text}text', 'value': 'text'}
        assert capsys.readouterr().out == (
                "called ElementDialogGui.get_lineinput_text with args ('txt_name',)\n"
                "called ElementDialogGui.get_checkbox_value with args ('cb_ns',)\n"
                "called ElementDialogGui.get_combobox_index with args ('cmb_ns',)\n"
                "called ElementDialogGui.get_combobox_itemtext with args ('cmb_ns', 1)\n"
                "called ElementDialogGui.get_lineinput_text with args ('txt_value',)\n")


class TestSearchDialog:
    """unittests for main.SearchDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.SearchDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called SearchDialog.__init__ with args', args)
        monkeypatch.setattr(testee.SearchDialog, '__init__', mock_init)
        testobj = testee.SearchDialog()
        assert capsys.readouterr().out == 'called SearchDialog.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SearchDialog.__init__
        """
        monkeypatch.setattr(testee, 'DialogGui', MockDialogGui)
        parent = types.SimpleNamespace(search_args=(), gui='MainGui')
        testobj = testee.SearchDialog(parent)
        assert testobj.parent == parent
        assert capsys.readouterr().out == (
            f"called DialogGui.__init__ with args ({testobj}, 'MainGui', '') {{}}\n"
            "called DialogGui.add_label with args ('Element name:', 0, 0) {}\n"
            "called DialogGui.add_label with args ('name:', 0, 1) {}\n"
            f"called DialogGui.add_lineinput with args (0, 2, '', {testobj.set_search}) {{}}\n"
            "called DialogGui.add_label with args ('Attribute name:', 1, 0) {}\n"
            "called DialogGui.add_label with args ('name:', 1, 1) {}\n"
            f"called DialogGui.add_lineinput with args (1, 2, '', {testobj.set_search}) {{}}\n"
            "called DialogGui.add_label with args ('', 2, 0) {}\n"
            "called DialogGui.add_label with args ('value:', 2, 1) {}\n"
            f"called DialogGui.add_lineinput with args (2, 2, '', {testobj.set_search}) {{}}\n"
            "called DialogGui.add_label with args ('Text:', 3, 0) {}\n"
            "called DialogGui.add_label with args ('value:', 3, 1) {}\n"
            f"called DialogGui.add_lineinput with args (3, 2, '', {testobj.set_search}) {{}}\n"
            "called DialogGui.add_label with args ('', 4, 0) {'fullwidth': True}\n"
            "called DialogGui.add_buttons with args"
            f" ([('&Save', {testobj.gui.accept}, True), ('&Cancel', {testobj.gui.reject}, False),"
            f" ('C&lear Values', {testobj.clear_values}, False)],)\n"
            "called DialogGui.finish_display\n"
            "called DialogGui.set_focus_to with args ('lineinput',)\n")
        parent.search_args = ('xxx', 'yyy', 'zzz', 'qqq')
        testobj = testee.SearchDialog(parent, title="xxxx")
        assert testobj.parent == parent
        assert capsys.readouterr().out == (
            f"called DialogGui.__init__ with args ({testobj}, 'MainGui', 'xxxx') {{}}\n"
            "called DialogGui.add_label with args ('Element name:', 0, 0) {}\n"
            "called DialogGui.add_label with args ('name:', 0, 1) {}\n"
            f"called DialogGui.add_lineinput with args (0, 2, 'xxx', {testobj.set_search}) {{}}\n"
            "called DialogGui.add_label with args ('Attribute name:', 1, 0) {}\n"
            "called DialogGui.add_label with args ('name:', 1, 1) {}\n"
            f"called DialogGui.add_lineinput with args (1, 2, 'yyy', {testobj.set_search}) {{}}\n"
            "called DialogGui.add_label with args ('', 2, 0) {}\n"
            "called DialogGui.add_label with args ('value:', 2, 1) {}\n"
            f"called DialogGui.add_lineinput with args (2, 2, 'zzz', {testobj.set_search}) {{}}\n"
            "called DialogGui.add_label with args ('Text:', 3, 0) {}\n"
            "called DialogGui.add_label with args ('value:', 3, 1) {}\n"
            f"called DialogGui.add_lineinput with args (3, 2, 'qqq', {testobj.set_search}) {{}}\n"
            "called DialogGui.add_label with args ('', 4, 0) {'fullwidth': True}\n"
            "called DialogGui.add_buttons with args"
            f" ([('&Save', {testobj.gui.accept}, True), ('&Cancel', {testobj.gui.reject}, False),"
            f" ('C&lear Values', {testobj.clear_values}, False)],)\n"
            "called DialogGui.finish_display\n"
            "called DialogGui.set_focus_to with args ('lineinput',)\n")

    def test_set_search(self, monkeypatch, capsys):
        """unittest for SearchDialog.set_search
        """
        def mock_build(*args):
            print('called Editor.build_search_description with args', args)
            return args
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(build_search_description=mock_build)
        testobj.gui = MockDialogGui()
        assert capsys.readouterr().out == "called DialogGui.__init__ with args () {}\n"
        testobj.txt_element = 'txt_element'
        testobj.txt_attr_name = 'txt_attr_name'
        testobj.txt_attr_val = 'txt_attr_val'
        testobj.txt_text = 'txt_text'
        testobj.lbl_search = 'lbl.search'
        testobj.set_search()
        assert capsys.readouterr().out == (
            "called DialogGui.get_lineinput_text with args ('txt_element',)\n"
            "called DialogGui.get_lineinput_text with args ('txt_attr_name',)\n"
            "called DialogGui.get_lineinput_text with args ('txt_attr_val',)\n"
            "called DialogGui.get_lineinput_text with args ('txt_text',)\n"
            "called Editor.build_search_description with args"
            " ('lineinput text', 'lineinput text', 'lineinput text', 'lineinput text')\n"
            "called DialogGui.set_label_text with args"
            " ('lbl.search', 'lineinput text\\nlineinput text\\nlineinput text\\nlineinput text')\n")

    def test_clear_values(self, monkeypatch, capsys):
        """unittest for SearchDialog.clear_values
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = MockDialogGui()
        assert capsys.readouterr().out == "called DialogGui.__init__ with args () {}\n"
        testobj.txt_element = 'txt_element'
        testobj.txt_attr_name = 'txt_attr_name'
        testobj.txt_attr_val = 'txt_attr_val'
        testobj.txt_text = 'txt_text'
        testobj.lbl_search = 'lbl.search'
        testobj.clear_values()
        assert capsys.readouterr().out == (
                "called DialogGui.set_lineinput_text with args ('txt_element', '')\n"
                "called DialogGui.set_lineinput_text with args ('txt_attr_name', '')\n"
                "called DialogGui.set_lineinput_text with args ('txt_attr_val', '')\n"
                "called DialogGui.set_lineinput_text with args ('txt_text', '')\n"
                "called DialogGui.set_label_text with args ('lbl.search', '')\n"
                "called DialogGui.refresh\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for SearchDialog.confirm
        """
        def mock_get(*args):
            print('called DialogGui.get_lineinput_text with args', args)
            return ''
        def mock_get_2(*args):
            print('called DialogGui.get_lineinput_text with args', args)
            return args[0]
        def mock_meld(*args):
            print('called MainGui.meldfout with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(gui=types.SimpleNamespace(meldfout=mock_meld))
        testobj.gui = MockDialogGui()
        assert capsys.readouterr().out == "called DialogGui.__init__ with args () {}\n"
        testobj.txt_element = 'txt_element'
        testobj.txt_attr_name = 'txt_attr_name'
        testobj.txt_attr_val = 'txt_attr_val'
        testobj.txt_text = 'txt_text'
        testobj.gui.get_lineinput_text = mock_get
        assert not testobj.confirm()
        assert capsys.readouterr().out == (
                "called DialogGui.get_lineinput_text with args ('txt_element',)\n"
                "called DialogGui.get_lineinput_text with args ('txt_attr_name',)\n"
                "called DialogGui.get_lineinput_text with args ('txt_attr_val',)\n"
                "called DialogGui.get_lineinput_text with args ('txt_text',)\n"
                "called MainGui.meldfout with args"
                " ('Please enter search criteria or press cancel',)\n"
                "called DialogGui.set_focus_to with args ('txt_element',)\n")
        testobj.gui.get_lineinput_text = mock_get_2
        assert testobj.confirm()
        assert testobj.parent.in_dialog
        assert testobj.parent.search_args == ('txt_element', 'txt_attr_name',
                                              'txt_attr_val', 'txt_text')
        assert capsys.readouterr().out == (
                "called DialogGui.get_lineinput_text with args ('txt_element',)\n"
                "called DialogGui.get_lineinput_text with args ('txt_attr_name',)\n"
                "called DialogGui.get_lineinput_text with args ('txt_attr_val',)\n"
                "called DialogGui.get_lineinput_text with args ('txt_text',)\n")
