import os.path
import types
import textwrap
import axe.base as testee

def _test_find_in_flattened_tree():
    pass


def test_parse_nsmap(monkeypatch, capsys):
    def mock_iterparse(*args):
        print('called ElementTree.iterparse with args', args)
        return (('start-ns', ('ns-prefix', 'ns-uri')), ('start', 'newroot'), ('start', 'nextroot'),
                ('end-ns', ''))
    monkeypatch.setattr(testee.et, 'ElementTree', lambda x: f'ElementTree({x})')
    monkeypatch.setattr(testee.et, 'iterparse', mock_iterparse)
    assert testee.parse_nsmap('input') == ('ElementTree(newroot)', ['ns-prefix'], ['ns-uri'])
    assert capsys.readouterr().out == ("called ElementTree.iterparse with args ('input',"
                                       " ('start-ns', 'start'))\n")


def test_xmltree_init(monkeypatch):
    monkeypatch.setattr(testee.et, 'Element', lambda x: f'Element({x})')
    testobj = testee.XMLTree('data')
    assert testobj.root == 'Element(data)'


def test_xmltree_expand(monkeypatch, capsys):
    def mock_init(self):
        pass
    class MockElement:
        def set(self, *args):
            print("called Element.set with args", args)
    class MockSubel:
        def __init__(self, *args):
            print("called SubElement.__init__ with args", args)
    monkeypatch.setattr(testee.et, 'Element', MockElement)
    monkeypatch.setattr(testee.et, 'SubElement', MockSubel)  # lambda x: f'SubElement({x})')
    monkeypatch.setattr(testee.XMLTree, '__init__', mock_init)
    testobj = testee.XMLTree()
    mock_root = MockElement()
    assert testobj.expand(mock_root, 'text', ('da', 'ta')) is None
    assert capsys.readouterr().out == "called Element.set with args ('da', 'ta')\n"
    node = testobj.expand(mock_root, '<> text', ('da', 'ta'))
    assert isinstance(node, testee.et.SubElement)
    assert node.text == 'ta'
    assert capsys.readouterr().out == f"called SubElement.__init__ with args ({mock_root}, 'da')\n"


def test_xmltree_write(monkeypatch, capsys):
    def mock_init(self):
        pass
    def mock_register(*args):
        print('called register_namespace with args', args)
    class MockEtree:
        def __init__(self, arg):
            print(f'called ElementTree.__init__ with arg `{arg}`')
        def write(self, *args, **kwargs):
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


class MockGui:
    def __init__(self, master, *args, **kwargs):
        self.master = master
        print('called Gui.__init__')
        self.top = 'treetop'
    def go(self):
        print('called Gui.go')
    def meldinfo(self, *args, **kwargs):
        print('called Gui.meldinfo with args', args, kwargs)
    def meldfout(self, *args, **kwargs):
        print('called Gui.meldfout with args', args, kwargs)
    def init_gui(self, *args):
        print('called Gui.init_gui with args', args)
    def init_tree(self, *args):
        print('called Gui.init_tree with args', args)
    def setup_new_tree(self, *args):
        print('called Gui.setup_new_tree with args', args)
    def set_windowtitle(self, title):
        print(f'called Gui.set_windowtitle with arg `{title}`')
    def get_windowtitle(self):
        pass
    def ask_yesnocancel(self):
        pass
    def get_selected_item(self):
        pass
    def set_selected_item(self, item):
        print(f'called Gui.set_selected_item with arg `{item}`')
    def get_treetop(self):
        return self.top
    def get_node_children(self, node):
        print(f'called Gui.get_node_children with arg `{node}`')
        return 'child1', 'child2'
    def get_node_title(self, node):
        print(f'called Gui.get_node_title with arg `{node}`')
        return 'title'
    def get_node_data(self, node):
        print(f'called Gui.get_node_data with arg `{node}`')
        return 'data'
    def get_node_parentpos(self, node):
        print(f'called Gui.get_node_parentpos with arg `{node}`')
        return 'parent', 'pos'
    def add_node_to_parent(self, node):
        print(f'called Gui.add_node_to_parent with arg `{node}`')
    def set_node_title(self, node, title):
        print(f'called Gui.set_node_title with args `{node}` `{title}`')
    def expand_item(self, node=None):
        print(f'called Gui.expand_item with arg `{node}`')
    def collapse_item(self):
        print('called Gui.collapse_item')
    def do_undo(self, node=None):
        print('called Gui.do_undo')
    def do_redo(self, node=None):
        print('called Gui.do_redo')
    def edit_item(self, node=None):
        print(f'called Gui.edit_item with arg `{node}`')
    def copy(self, *args, **kwargs):
        print('called Gui.copy with args', args, kwargs)
    def paste(self, *args, **kwargs):
        print('called Gui.paste with args', args, kwargs)
    def add_attribute(self, node):
        print(f'called Gui.add_attribute with arg `{node}`')
    def insert(self, *args, **kwargs):
        print('called Gui.insert with args', args, kwargs)
    def file_to_save(self):
        print('called Gui.file_to_save')
        return False, ''
    def file_to_read(self):
        print('called Gui.file_to_read')
        return False, ''
    def ask_for_text(self, *args):
        print('called Gui.ask_for_text with args', args)
        return ''
    def ask_for_search_args(self):
        print('called Gui.ask_for_search_args')
        return False


def test_editor_init(monkeypatch, capsys):
    def mock_getroot(*args):
        return 'got root from tree'
    def mock_parse_nsmap(arg):
        print(f'called parse_nsmap with arg {arg}')
        return types.SimpleNamespace(getroot=mock_getroot), ['ns_prefix'], ['ns_uri']
    def mock_parse_nsmap_2(arg):
        raise OSError('got an OSError')
    def mock_parse_nsmap_3(arg):
        raise testee.et.ParseError('got a ParseError')
    def mock_init_tree(self, *args):
        print('called Editor.init_tree with args', args)
    monkeypatch.setattr(testee, 'Gui', MockGui)
    monkeypatch.setattr(testee, 'parse_nsmap', mock_parse_nsmap)
    monkeypatch.setattr(testee.et, 'Element', lambda x: x)
    monkeypatch.setattr(testee.Editor, 'init_tree', mock_init_tree)
    testobj = testee.Editor('')
    assert testobj.title == f'{testee.TITLESTART} Editor'
    assert testobj.xmlfn == ''
    assert not testobj.readonly
    assert isinstance(testobj.gui, testee.Gui)
    assert (testobj.gui.cut_att, testobj.gui.cut_el) == (None, None)
    assert (testobj.search_args, testobj._search_pos) == ([], None)
    assert capsys.readouterr().out == ("called Gui.__init__\n"
                                       "called Gui.init_gui with args ()\n"
                                       "called Editor.init_tree with args ('(new root)',)\n"
                                       "called Gui.go\n")
    testobj = testee.Editor('testfile.xml')
    assert testobj.title == f'{testee.TITLESTART} Editor'
    assert testobj.xmlfn == os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testfile.xml')
    assert not testobj.readonly
    assert isinstance(testobj.gui, testee.Gui)
    assert (testobj.gui.cut_att, testobj.gui.cut_el) == (None, None)
    assert (testobj.search_args, testobj._search_pos) == ([], None)
    assert capsys.readouterr().out == ("called Gui.__init__\n"
                                       "called Gui.init_gui with args ()\n"
                                       "called Editor.init_tree with args ('(new root)',)\n"
                                       f"called parse_nsmap with arg {testobj.xmlfn}\n"
                                       "called Editor.init_tree with args ('got root from tree',"
                                       " ['ns_prefix'], ['ns_uri'])\n"
                                       "called Gui.go\n")
    monkeypatch.setattr(testee, 'parse_nsmap', mock_parse_nsmap_2)
    testobj = testee.Editor('testfile.xml')
    assert capsys.readouterr().out == ("called Gui.__init__\n"
                                       "called Gui.init_gui with args ()\n"
                                       "called Editor.init_tree with args ('(new root)',)\n"
                                       "called Gui.meldfout with args ('got an OSError',)"
                                       " {'abort': True}\n"
                                       "called Gui.init_tree with args (None,)\n")
    monkeypatch.setattr(testee, 'parse_nsmap', mock_parse_nsmap_3)
    testobj = testee.Editor('testfile.xml')
    assert capsys.readouterr().out == ("called Gui.__init__\n"
                                       "called Gui.init_gui with args ()\n"
                                       "called Editor.init_tree with args ('(new root)',)\n"
                                       "called Gui.meldfout with args ('got a ParseError',)"
                                       " {'abort': True}\n"
                                       "called Gui.init_tree with args (None,)\n")


def mock_editor_init(self, name):
    print('called Editor.__init__')
    self.gui = MockGui(self)
    self.xmlfn = name
    self._search_pos = None


def test_editor_mark_dirty(monkeypatch, capsys):
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.readonly = True
    testobj.mark_dirty(True)
    assert testobj.tree_dirty
    assert capsys.readouterr().out == ''

    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.readonly = False
    testobj.title = 'windowtitle'
    monkeypatch.setattr(testobj.gui, 'get_windowtitle', lambda *x: '')
    testobj.mark_dirty(True)
    assert testobj.tree_dirty
    assert capsys.readouterr().out == ''

    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.readonly = False
    testobj.title = 'windowtitle'
    monkeypatch.setattr(testobj.gui, 'get_windowtitle', lambda *x: ' - ' + testobj.title)
    testobj.mark_dirty(True)
    assert testobj.tree_dirty
    assert capsys.readouterr().out == 'called Gui.set_windowtitle with arg `* - windowtitle`\n'

    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.readonly = False
    testobj.title = 'windowtitle'
    monkeypatch.setattr(testobj.gui, 'get_windowtitle', lambda *x: '* - ' + testobj.title)
    testobj.mark_dirty(True)
    assert testobj.tree_dirty
    assert capsys.readouterr().out == 'called Gui.set_windowtitle with arg ` - windowtitle`\n'


def test_editor_check_tree(monkeypatch, capsys):
    def mock_savexml(self):
        print('called Editor.savexml')
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    monkeypatch.setattr(testee.Editor, 'savexml', mock_savexml)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
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


def test_editor_checkselection(monkeypatch, capsys):
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    monkeypatch.setattr(testobj.gui, 'get_selected_item', lambda *x: 'selected')
    testobj.readonly = True
    testobj.top = 'top'
    assert testobj.checkselection()
    assert testobj.item == 'selected'
    assert capsys.readouterr().out == ''

    testobj.readonly = False
    assert testobj.checkselection()
    assert testobj.item == 'selected'
    assert capsys.readouterr().out == ''

    monkeypatch.setattr(testobj.gui, 'get_selected_item', lambda *x: None)
    assert not testobj.checkselection()
    assert testobj.item is None
    assert capsys.readouterr().out == ("called Gui.meldinfo with args ('You need"
                                       " to select an element or attribute first',) {}\n")

    monkeypatch.setattr(testobj.gui, 'get_selected_item', lambda *x: 'top')
    assert not testobj.checkselection()
    assert testobj.item == 'top'
    assert capsys.readouterr().out == ("called Gui.meldinfo with args ('You need"
                                       " to select an element or attribute first',) {}\n")


def test_editor_writexml(monkeypatch, capsys):
    def mock_copyfile(*args):
        print('called shutil.copyfile with args', args)
    class MockTree:
        def __init__(self, arg):
            print(f'called XMLTree.__init__ with arg `{arg}`')
            self.root = 'data_root'
        def write(self, *args):
            print('called XMLTree.write with args', args)
    def mock_expandnode(self, x, y, z):
        print(f'called Editor.expandnode with args `{x}` `{y}` `data of type {type(z)}`')
    def mock_mark_dirty(self, arg):
        print(f'called Editor.mark_dirty with arg `{arg}`')
    monkeypatch.setattr(testee.shutil, 'copyfile', mock_copyfile)
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    monkeypatch.setattr(testee.Editor, 'expandnode', mock_expandnode)
    monkeypatch.setattr(testee.Editor, 'mark_dirty', mock_mark_dirty)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    monkeypatch.setattr(testee, 'XMLTree', MockTree)
    testobj.ns_prefixes = ()
    monkeypatch.setattr(testee.os.path, 'exists', lambda *x: False)
    testobj.writexml()
    assert capsys.readouterr().out == ("called Gui.get_node_data with arg `treetop`\n"
                                       "called XMLTree.__init__ with arg `d`\n"
                                       "called Editor.expandnode with args `treetop` `data_root`"
                                       f" `data of type {testee.XMLTree}`\n"
                                       "called XMLTree.write with args ('testfile', None)\n"
                                       "called Editor.mark_dirty with arg `False`\n")
    monkeypatch.setattr(testee.os.path, 'exists', lambda *x: True)
    testobj.writexml()
    assert capsys.readouterr().out == ("called shutil.copyfile with args ('testfile',"
                                       " 'testfile.bak')\n"
                                       "called Gui.get_node_data with arg `treetop`\n"
                                       "called XMLTree.__init__ with arg `d`\n"
                                       "called Editor.expandnode with args `treetop` `data_root`"
                                       f" `data of type {testee.XMLTree}`\n"
                                       "called XMLTree.write with args ('testfile', None)\n"
                                       "called Editor.mark_dirty with arg `False`\n")
    testobj.ns_prefixes = 'prefixes'
    testobj.ns_uris = 'uris'
    testobj.writexml('newfile')
    assert capsys.readouterr().out == ("called shutil.copyfile with args ('testfile', 'newfile')\n"
                                       "called Gui.get_node_data with arg `treetop`\n"
                                       "called XMLTree.__init__ with arg `d`\n"
                                       "called Editor.expandnode with args `treetop` `data_root`"
                                       f" `data of type {testee.XMLTree}`\n"
                                       "called XMLTree.write with args ('testfile', ('prefixes',"
                                       " 'uris'))\n"
                                       "called Editor.mark_dirty with arg `False`\n")

def test_editor_expandnode(monkeypatch, capsys):
    counter = 0
    def mock_expand(*args):
        nonlocal counter
        print('called Element.expand with args', args)
        counter += 1
        if counter == 1:
            return 'subnode'
        return None
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    tree = types.SimpleNamespace(expand=mock_expand)
    testobj.expandnode('app_root', 'data_root', tree)
    assert capsys.readouterr().out == (
            "called Gui.get_node_children with arg `app_root`\n"
            "called Gui.get_node_title with arg `child1`\n"
            "called Gui.get_node_data with arg `child1`\n"
            "called Element.expand with args ('data_root', 'title', 'data')\n"
            "called Gui.get_node_children with arg `child1`\n"
            "called Gui.get_node_title with arg `child1`\n"
            "called Gui.get_node_data with arg `child1`\n"
            "called Element.expand with args ('subnode', 'title', 'data')\n"
            "called Gui.get_node_title with arg `child2`\n"
            "called Gui.get_node_data with arg `child2`\n"
            "called Element.expand with args ('subnode', 'title', 'data')\n"
            "called Gui.get_node_title with arg `child2`\n"
            "called Gui.get_node_data with arg `child2`\n"
            "called Element.expand with args ('data_root', 'title', 'data')\n")

def _test_editor_init_tree(monkeypatch, capsys):
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'

def test_editor_add_to_tree(monkeypatch, capsys):
    class MockElement:
        def __init__(self):
            self.tag = 'mytag'
            self.text = 'some text'
            self.attrs = {'x': 'a', 'y': None}
            self.subel = []
        def keys(self):
            return self.attrs.keys()
        def get(self, attr):
            return self.attrs[attr]
        def __iter__(self):
            return (x for x in self.subel)
    def mock_add_item(self, *args, **kwargs):
        print('called Editor.add_item with args', args, kwargs)
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    monkeypatch.setattr(testee.Editor, 'add_item', mock_add_item)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
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

def _test_editor_getshortname(monkeypatch, capsys):
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'

def _test_editor_add_item(monkeypatch, capsys):
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'

def _test_editor_get_menu_data(monkeypatch, capsys):
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'

def _test_editor_flatten_tree(monkeypatch, capsys):
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'

def test_editor_find_first(monkeypatch, capsys):
    def mock_find_next(self, value):
        print(f'called Editor.find_next with arg `{value}`')
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    monkeypatch.setattr(testee.Editor, 'find_next', mock_find_next)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.find_first()
    assert capsys.readouterr().out == 'called Gui.ask_for_search_args\n'
    monkeypatch.setattr(testobj.gui, 'ask_for_search_args', lambda *x: True)
    monkeypatch.setattr(testobj, 'checkselection', lambda *x, **y: True)
    testobj.item = 'item'
    testobj.find_first()
    assert testobj._search_pos == ('item', None)
    assert capsys.readouterr().out == 'called Editor.find_next with arg `False`\n'
    monkeypatch.setattr(testobj, 'checkselection', lambda *x, **y: False)
    testobj.find_first()
    assert testobj._search_pos == ('child1', None)
    assert capsys.readouterr().out == ('called Gui.get_node_children with arg `treetop`\n'
                                       'called Editor.find_next with arg `False`\n')
    testobj.find_first(reverse=True)
    assert testobj._search_pos == ('child2', None)
    assert capsys.readouterr().out == ('called Gui.get_node_children with arg `treetop`\n'
                                       'called Editor.find_next with arg `True`\n')

def test_editor_find_next(monkeypatch, capsys):
    def mock_flatten_tree(self, node):
        print(f'called Editor.flatten_tree with arg `{node}`')
    def mock_find_in_flattened_tree(*args):
        print('called find_in_flattened_tree with args', args)
        return 'itemfound', False
    monkeypatch.setattr(testee, 'find_in_flattened_tree', mock_find_in_flattened_tree)
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    monkeypatch.setattr(testee.Editor, 'flatten_tree', mock_flatten_tree)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.find_next()
    assert capsys.readouterr().out == ('called Gui.meldinfo with args'
                                       ' (\'You need to "Find" something first\',) {}\n')
    testobj.top = 'top'
    testobj.search_args = 'search_args'
    testobj._search_pos = ('node', True)
    testobj.find_next()
    assert capsys.readouterr().out == (
            "called Editor.flatten_tree with arg `top`\n"
            "called find_in_flattened_tree with args (None, 'search_args', False, ('node', True))\n"
            "called Gui.set_selected_item with arg `itemfound`\n")
    testobj._search_pos = ('node', True)
    testobj.find_next(reverse=True)
    assert capsys.readouterr().out == (
            "called Editor.flatten_tree with arg `top`\n"
            "called find_in_flattened_tree with args (None, 'search_args', True, ('node', True))\n"
            "called Gui.set_selected_item with arg `itemfound`\n")
    monkeypatch.setattr(testee, 'find_in_flattened_tree', lambda *x: (None, None))
    testobj._search_pos = ('node', True)
    testobj.find_next()
    assert capsys.readouterr().out == (
            "called Editor.flatten_tree with arg `top`\n"
            "called Gui.meldinfo with args ('Niks (meer) gevonden',) {}\n")

def test_editor_newxml(monkeypatch, capsys):
    def mock_init_tree(self, arg):
        print(f'called Editor.init_tree with arg `{arg}`')
    def mock_element(name):
        print(f'created etree.Element for name `{name}`')
        return name
    monkeypatch.setattr(testee.et, 'Element', mock_element)
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    monkeypatch.setattr(testee.Editor, 'init_tree', mock_init_tree)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    monkeypatch.setattr(testobj, 'check_tree', lambda *x: False)
    testobj.newxml()
    assert capsys.readouterr().out == ''
    monkeypatch.setattr(testobj, 'check_tree', lambda *x: True)
    testobj.newxml()
    assert testobj.xmlfn == ''
    assert capsys.readouterr().out == (
            "called Gui.ask_for_text with args ('Enter a name (tag) for the root element',"
            " '(new root)')\n"
            "created etree.Element for name `(new root)`\n"
            "called Editor.init_tree with arg `(new root)`\n")
    monkeypatch.setattr(testobj.gui, 'ask_for_text', lambda *x: 'element')
    testobj.newxml()
    assert testobj.xmlfn == ''
    assert capsys.readouterr().out == ('created etree.Element for name `element`\n'
                                       'called Editor.init_tree with arg `element`\n')


def test_editor_openxml(monkeypatch, capsys):
    class MockElement:
        def getroot(self):
            return 'element_root'
    def mock_init_tree(self, *args):
        print('called Editor.init_tree with args', args)
    def mock_parse_nsmap(fname):
        print(f'called parse_nsmap with arg `{fname}`')
        raise testee.et.ParseError('error')
    def mock_parse_nsmap_ok(fname):
        return (MockElement(), 'prefixes', 'uris')
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    monkeypatch.setattr(testee.Editor, 'init_tree', mock_init_tree)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    monkeypatch.setattr(testobj, 'check_tree', lambda *x: False)
    testobj.openxml()
    assert capsys.readouterr().out == ''
    testobj.openxml(skip_check=True)
    assert capsys.readouterr().out == 'called Gui.file_to_read\n'
    monkeypatch.setattr(testobj, 'check_tree', lambda *x: True)
    monkeypatch.setattr(testobj.gui, 'file_to_read', lambda *x: (True, 'fname'))
    monkeypatch.setattr(testee, 'parse_nsmap', mock_parse_nsmap)
    testobj.openxml()
    assert capsys.readouterr().out == ("called parse_nsmap with arg `fname`\n"
                                       "called Gui.meldfout with args ('error',) {}\n")
    monkeypatch.setattr(testee, 'parse_nsmap', mock_parse_nsmap_ok)
    testobj.openxml()
    assert capsys.readouterr().out == ("called Editor.init_tree with args ('element_root',"
                                       " 'prefixes', 'uris')\n")


def test_editor_savexml(monkeypatch, capsys):
    def mock_savexmlas(self):
        print('called Editor.savexmlas')
    def mock_writexml(self):
        print('called Editor.writexml')
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    monkeypatch.setattr(testee.Editor, 'savexmlas', mock_savexmlas)
    monkeypatch.setattr(testee.Editor, 'writexml', mock_writexml)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.xmlfn = ''
    testobj.savexml()
    assert capsys.readouterr().out == 'called Editor.savexmlas\n'
    testobj.xmlfn = 'x'
    testobj.savexml()
    assert capsys.readouterr().out == 'called Editor.writexml\n'

def test_editor_savexmlas(monkeypatch, capsys):
    def mock_writexml(self):
        print('called Editor.writexml')
    def mock_mark_dirty(self, value):
        print(f'called Editor.mark_dirty with arg `{value}`')
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    monkeypatch.setattr(testee.Editor, 'writexml', mock_writexml)
    monkeypatch.setattr(testee.Editor, 'mark_dirty', mock_mark_dirty)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.savexmlas()
    assert capsys.readouterr().out == 'called Gui.file_to_save\n'
    monkeypatch.setattr(testobj.gui, 'file_to_save', lambda *x: (True, 'filename'))
    testobj.savexmlas()
    assert capsys.readouterr().out == ('called Editor.writexml\n'
                                       'called Gui.set_node_title with args `treetop` `filename`\n'
                                       'called Editor.mark_dirty with arg `False`\n')


def test_editor_expand(monkeypatch, capsys):
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.expand()
    assert capsys.readouterr().out == 'called Gui.expand_item with arg `None`\n'

def test_editor_collapse(monkeypatch, capsys):
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.collapse()
    assert capsys.readouterr().out == 'called Gui.collapse_item\n'

def test_editor_undo(monkeypatch, capsys):
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.undo()
    assert capsys.readouterr().out == 'called Gui.do_undo\n'

def test_editor_redo(monkeypatch, capsys):
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.redo()
    assert capsys.readouterr().out == 'called Gui.do_redo\n'

def test_editor_edit(monkeypatch, capsys):
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    monkeypatch.setattr(testee.Editor, 'checkselection', lambda *x: False)
    testobj.edit()
    assert capsys.readouterr().out == ''
    monkeypatch.setattr(testee.Editor, 'checkselection', lambda *x: True)
    testobj.item = 'item'
    testobj.edit()
    assert capsys.readouterr().out == 'called Gui.edit_item with arg `item`\n'


def test_editor_cut(monkeypatch, capsys):
    def mock_editor_copy(self, *args, **kwargs):
        print('called Editor.copy with args', args, kwargs)
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    monkeypatch.setattr(testee.Editor, 'copy', mock_editor_copy)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.cut()
    assert capsys.readouterr().out == "called Editor.copy with args () {'cut': True}\n"

def test_editor_delete(monkeypatch, capsys):
    def mock_editor_copy(self, *args, **kwargs):
        print('called Editor.copy with args', args, kwargs)
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    monkeypatch.setattr(testee.Editor, 'copy', mock_editor_copy)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.delete()
    assert capsys.readouterr().out == ("called Editor.copy with args () {'cut': True,"
                                       " 'retain': False}\n")

def test_editor_copy(monkeypatch, capsys):
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    monkeypatch.setattr(testobj, 'checkselection', lambda *x: False)
    testobj.copy()
    assert capsys.readouterr().out == ''
    monkeypatch.setattr(testobj, 'checkselection', lambda *x: True)
    testobj.item = 'item'
    testobj.copy()
    assert capsys.readouterr().out == (
            "called Gui.get_node_parentpos with arg `item`\n"
            "called Gui.copy with args ('item',) {'cut': False, 'retain': True}\n")
    monkeypatch.setattr(testobj.gui, 'get_node_parentpos', lambda *x: ('treetop', 0))
    testobj.copy()
    assert capsys.readouterr().out == 'called Gui.meldfout with args ("Can\'t copy the root",) {}\n'
    testobj.copy(cut=True)
    assert capsys.readouterr().out == 'called Gui.meldfout with args ("Can\'t cut the root",) {}\n'
    testobj.copy(cut=True, retain=False)
    assert capsys.readouterr().out == 'called Gui.meldfout with args ("Can\'t delete the root",) {}\n'


def test_editor_paste_after(monkeypatch, capsys):
    def mock_editor_paste(self, *args, **kwargs):
        print('called Editor.paste with args', args, kwargs)
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    monkeypatch.setattr(testee.Editor, 'paste', mock_editor_paste)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.paste_after()
    assert capsys.readouterr().out == ("called Editor.paste with args () {'before': False}\n")

def test_editor_paste_under(monkeypatch, capsys):
    def mock_editor_paste(self, *args, **kwargs):
        print('called Editor.paste with args', args, kwargs)
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    monkeypatch.setattr(testee.Editor, 'paste', mock_editor_paste)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.paste_under()
    assert capsys.readouterr().out == "called Editor.paste with args () {'below': True}\n"

def test_editor_paste(monkeypatch, capsys):
    def mock_get_title(node):
        return f'{testee.ELSTART} element'
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    monkeypatch.setattr(testobj, 'checkselection', lambda *x: False)
    testobj.paste()
    assert capsys.readouterr().out == ''
    monkeypatch.setattr(testobj, 'checkselection', lambda *x: True)
    testobj.item = 'item'
    testobj.paste()
    assert capsys.readouterr().out == (
            "called Gui.get_node_parentpos with arg `item`\n"
            "called Gui.paste with args ('item',) {'before': True, 'below': False}\n")
    monkeypatch.setattr(testobj.gui, 'get_node_parentpos', lambda *x: ('treetop', 0))
    testobj.paste()
    assert capsys.readouterr().out == (
            'called Gui.meldfout with args ("Can\'t paste before the root",) {}\n')
    testobj.paste(below=True)
    assert capsys.readouterr().out == (
            "called Gui.get_node_title with arg `item`\n"
            'called Gui.meldfout with args ("Can\'t paste below an attribute",) {}\n')
    monkeypatch.setattr(testobj.gui, 'get_node_title', mock_get_title)
    testobj.paste(before=False)
    assert capsys.readouterr().out == (
            "called Gui.meldinfo with args ('Pasting as first element below root',) {}\n"
            # 'called Gui.get_node_title with arg `item`\n'
            "called Gui.paste with args ('item',) {'before': False, 'below': True}\n")
    testobj.paste(below=True)
    assert capsys.readouterr().out == (
            # "called Gui.get_node_title with arg `item`\n"
            "called Gui.paste with args ('item',) {'before': True, 'below': True}\n")

def test_editor_add_attr(monkeypatch, capsys):
    def mock_get_title(node):
        return f'{testee.ELSTART} element'
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    monkeypatch.setattr(testobj, 'checkselection', lambda *x: False)
    testobj.add_attr()
    assert capsys.readouterr().out == ''
    monkeypatch.setattr(testobj, 'checkselection', lambda *x: True)
    testobj.item = 'item'
    testobj.add_attr()
    assert capsys.readouterr().out == (
            'called Gui.get_node_title with arg `item`\n'
            'called Gui.meldfout with args ("Can\'t add attribute to attribute",) {}\n')
    monkeypatch.setattr(testobj.gui, 'get_node_title', mock_get_title)
    testobj.add_attr()
    assert capsys.readouterr().out == 'called Gui.add_attribute with arg `item`\n'

def test_editor_insert_after(monkeypatch, capsys):
    def mock_insert(self, *args, **kwargs):
        print('called Editor.insert with args', args, kwargs)
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    monkeypatch.setattr(testee.Editor, 'insert', mock_insert)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.insert_after()
    assert capsys.readouterr().out == "called Editor.insert with args () {'before': False}\n"

def test_editor_insert_child(monkeypatch, capsys):
    def mock_insert(self, *args, **kwargs):
        print('called Editor.insert with args', args, kwargs)
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    monkeypatch.setattr(testee.Editor, 'insert', mock_insert)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.insert_child()
    assert capsys.readouterr().out == "called Editor.insert with args () {'below': True}\n"

def test_editor_insert(monkeypatch, capsys):
    def mock_get_title(node):
        return f'{testee.ELSTART} element'
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    monkeypatch.setattr(testobj, 'checkselection', lambda *x: False)
    testobj.insert()
    assert capsys.readouterr().out == ''
    monkeypatch.setattr(testobj, 'checkselection', lambda *x: True)
    testobj.item = 'item'
    testobj.insert()
    assert capsys.readouterr().out == (
            "called Gui.get_node_parentpos with arg `item`\n"
            "called Gui.insert with args ('item',) {'before': True, 'below': False}\n")
    monkeypatch.setattr(testobj.gui, 'get_node_parentpos', lambda *x: ('treetop', 0))
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
            "called Gui.insert with args ('item',) {'before': True, 'below': True}\n")


def test_editor_search(monkeypatch, capsys):
    def mock_find_first(self, *args, **kwargs):
        print('called Editor.find_first with args', args, kwargs)
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    monkeypatch.setattr(testee.Editor, 'find_first', mock_find_first)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.search()
    assert capsys.readouterr().out == "called Editor.find_first with args () {}\n"

def test_editor_search_last(monkeypatch, capsys):
    def mock_find_first(self, *args, **kwargs):
        print('called Editor.find_first with args', args, kwargs)
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    monkeypatch.setattr(testee.Editor, 'find_first', mock_find_first)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.search_last()
    assert capsys.readouterr().out == "called Editor.find_first with args () {'reverse': True}\n"

def test_editor_search_next(monkeypatch, capsys):
    def mock_find_next(self, *args, **kwargs):
        print('called Editor.find_next with args', args, kwargs)
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    monkeypatch.setattr(testee.Editor, 'find_next', mock_find_next)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.search_next()
    assert capsys.readouterr().out == "called Editor.find_next with args () {}\n"

def test_editor_search_prev(monkeypatch, capsys):
    def mock_find_next(self, *args, **kwargs):
        print('called Editor.find_next with args', args, kwargs)
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    monkeypatch.setattr(testee.Editor, 'find_next', mock_find_next)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.search_prev()
    assert capsys.readouterr().out == "called Editor.find_next with args () {'reverse': True}\n"

def _test_editor_get_search_text(monkeypatch, capsys):
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'

def test_editor_replace(monkeypatch, capsys):
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.replace()
    assert capsys.readouterr().out == ("called Gui.meldinfo with args"
                                       " ('Replace: not sure if I wanna implement this',) {}\n")

def _test_editor_about(monkeypatch, capsys):  # about() wordt niet gebruikt
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'
    testobj.about()
    assert capsys.readouterr().out == f"called Gui.meldinfo with args ('{testee.ABOUT}',) {{}}\n"
