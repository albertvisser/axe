"""unittests for ./axe/base.py
"""
import os.path
import types
import textwrap
import axe.base as testee
import pytest

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
    assert testee.find_in_flattened_tree(data, search_args) == (None, False)
    assert capsys.readouterr().out == ("")
    assert testee.find_in_flattened_tree(data, search_args, pos=3) == (None, False)
    assert capsys.readouterr().out == (
            "called Editor.get_remaining_data_to_search with args (3, [])\n")
    data = [('item', 'a name', 'a text', 'a list')]
    assert testee.find_in_flattened_tree(data, search_args) == (None, False)
    assert capsys.readouterr().out == (
            "called apply_search_criteria_for_element with args ('xx', 'a name')\n"
            "called apply_search_criteria_for_attrs with args"
            " (['xx', 'yy', 'zz', 'qq'], 'a list', False)\n"
            "called apply_search_criteria_for_text with args ('qq', 'a text')\n")
    monkeypatch.setattr(testee, 'apply_search_criteria_for_element', mock_apply_ele_2)
    assert testee.find_in_flattened_tree(data, search_args) == (None, False)
    assert capsys.readouterr().out == (
            "called apply_search_criteria_for_element with args ('xx', 'a name')\n"
            "called apply_search_criteria_for_attrs with args"
            " (['xx', 'yy', 'zz', 'qq'], 'a list', False)\n"
            "called apply_search_criteria_for_text with args ('qq', 'a text')\n")
    monkeypatch.setattr(testee, 'apply_search_criteria_for_attrs', mock_apply_att_2)
    assert testee.find_in_flattened_tree(data, search_args) == (None, False)
    assert capsys.readouterr().out == (
            "called apply_search_criteria_for_element with args ('xx', 'a name')\n"
            "called apply_search_criteria_for_attrs with args"
            " (['xx', 'yy', 'zz', 'qq'], 'a list', False)\n"
            "called apply_search_criteria_for_text with args ('qq', 'a text')\n")
    monkeypatch.setattr(testee, 'apply_search_criteria_for_text', mock_apply_txt_2)
    assert testee.find_in_flattened_tree(data, search_args) == ('node', True)
    assert capsys.readouterr().out == (
            "called apply_search_criteria_for_element with args ('xx', 'a name')\n"
            "called apply_search_criteria_for_attrs with args"
            " (['xx', 'yy', 'zz', 'qq'], 'a list', False)\n"
            "called apply_search_criteria_for_text with args ('qq', 'a text')\n")
    monkeypatch.setattr(testee, 'apply_search_criteria_for_attrs', mock_apply_att_3)
    assert testee.find_in_flattened_tree(data, search_args) == ('item', False)
    assert capsys.readouterr().out == (
            "called apply_search_criteria_for_element with args ('xx', 'a name')\n"
            "called apply_search_criteria_for_attrs with args"
            " (['xx', 'yy', 'zz', 'qq'], 'a list', False)\n"
            "called apply_search_criteria_for_text with args ('qq', 'a text')\n")
    data = [('item', 'a name', 'a text', 'a list'), ('item 2', 'name 2', 'text 2', 'list 2')]
    assert testee.find_in_flattened_tree(data, search_args) == ('item', False)
    assert capsys.readouterr().out == (
            "called apply_search_criteria_for_element with args ('xx', 'a name')\n"
            "called apply_search_criteria_for_attrs with args"
            " (['xx', 'yy', 'zz', 'qq'], 'a list', False)\n"
            "called apply_search_criteria_for_text with args ('qq', 'a text')\n")
    assert testee.find_in_flattened_tree(data, search_args, True) == ('item 2', False)
    assert capsys.readouterr().out == (
            "called apply_search_criteria_for_element with args ('xx', 'name 2')\n"
            "called apply_search_criteria_for_attrs with args"
            " (['xx', 'yy', 'zz', 'qq'], 'list 2', True)\n"
            "called apply_search_criteria_for_text with args ('qq', 'text 2')\n")
    monkeypatch.setattr(testee, 'get_remaining_data_to_search', mock_get_2)
    assert testee.find_in_flattened_tree(data, search_args, pos=3) == ('item 2', False)
    assert capsys.readouterr().out == (
            f"called Editor.get_remaining_data_to_search with args (3, {data})\n"
            "called apply_search_criteria_for_element with args ('xx', 'name 2')\n"
            "called apply_search_criteria_for_attrs with args"
            " (['xx', 'yy', 'zz', 'qq'], 'list 2', False)\n"
            "called apply_search_criteria_for_text with args ('qq', 'text 2')\n")


def test_get_remaining_data_to_search():
    """unittest for base.get_remaining_data_to_search
    """
    # 55-76
    data = [(0, 'x'), (1, 'y'), (2, 'z')]
    assert testee.get_remaining_data_to_search((0, False), data) == [(1, 'y'), (2, 'z')]
    assert testee.get_remaining_data_to_search((1, False), data) == [(2, 'z')]
    assert testee.get_remaining_data_to_search((2, False), data) == []
    assert testee.get_remaining_data_to_search((3, False), data) == []
    data = [(0, 'x', 'xx', [(1, 'a'), (2, 'b')]), (3, 'y', 'yy', [(4, 'c'), (5, 'd')]),
            (6, 'z', 'zz', [(7, 'e'), (8, 'f')])]
    assert testee.get_remaining_data_to_search((0, False), data) == [
           (3, 'y', 'yy', [(4, 'c'), (5, 'd')]), (6, 'z', 'zz', [(7, 'e'), (8, 'f')])]
    assert testee.get_remaining_data_to_search((0, True), data) == [(6, 'z', 'zz', [])]
    assert testee.get_remaining_data_to_search((1, False), data) == []
    assert testee.get_remaining_data_to_search((1, True), data) == [
           (0, 'x', 'xx', [(2, 'b')]), (3, 'y', 'yy', [(4, 'c'), (5, 'd')]),
           (6, 'z', 'zz', [(7, 'e'), (8, 'f')])]
    assert testee.get_remaining_data_to_search((2, False), data) == []
    assert testee.get_remaining_data_to_search((2, True), data) == [
            (0, 'x', 'xx', []), (3, 'y', 'yy', [(4, 'c'), (5, 'd')]),
            (6, 'z', 'zz', [(7, 'e'), (8, 'f')])]
    assert testee.get_remaining_data_to_search((3, False), data) == [
            (6, 'z', 'zz', [(7, 'e'), (8, 'f')])]
    assert testee.get_remaining_data_to_search((3, True), data) == [(6, 'z', 'zz', [])]
    assert testee.get_remaining_data_to_search((4, False), data) == []
    assert testee.get_remaining_data_to_search((4, True), data) == [
           (3, 'y', 'yy', [(5, 'd')]), (6, 'z', 'zz', [(7, 'e'), (8, 'f')])]
    assert testee.get_remaining_data_to_search((5, False), data) == []
    assert testee.get_remaining_data_to_search((5, True), data) == [
           (3, 'y', 'yy', []), (6, 'z', 'zz', [(7, 'e'), (8, 'f')])]
    assert testee.get_remaining_data_to_search((6, False), data) == []
    assert testee.get_remaining_data_to_search((6, True), data) == [(6, 'z', 'zz', [])]
    assert testee.get_remaining_data_to_search((7, False), data) == []
    assert testee.get_remaining_data_to_search((7, True), data) == [
            (6, 'z', 'zz', [(8, 'f')])]
    assert testee.get_remaining_data_to_search((8, False), data) == []
    assert testee.get_remaining_data_to_search((8, True), data) == [(6, 'z', 'zz', [])]
    assert testee.get_remaining_data_to_search((9, False), data) == []
    # dit lijkt me ook niet goed:
    assert testee.get_remaining_data_to_search((9, True), data) == [(6, 'z', 'zz', [])]
    assert testee.get_remaining_data_to_search((10, True), data) == [(6, 'z', 'zz', [])]
    assert testee.get_remaining_data_to_search((11, True), data) == [(6, 'z', 'zz', [])]


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


def test_xmltree_init(monkeypatch):
    """unittest for base.xmltree_init
    """
    monkeypatch.setattr(testee.et, 'Element', lambda x: f'Element({x})')
    testobj = testee.XMLTree('data')
    assert testobj.root == 'Element(data)'


def test_xmltree_expand(monkeypatch, capsys):
    """unittest for base.xmltree_expand
    """
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


def test_xmltree_write(monkeypatch, capsys):
    """unittest for base.xmltree_write
    """
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
    def init_gui(self, *args):
        """stub
        """
        print('called Gui.init_gui with args', args)
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
        return 'data'
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
    def edit_item(self, node=None):
        """stub
        """
        print(f'called Gui.edit_item with arg `{node}`')
    def copy(self, *args, **kwargs):
        """stub
        """
        print('called Gui.copy with args', args, kwargs)
    def paste(self, *args, **kwargs):
        """stub
        """
        print('called Gui.paste with args', args, kwargs)
    def add_attribute(self, node):
        """stub
        """
        print(f'called Gui.add_attribute with arg `{node}`')
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


def test_editor_init(monkeypatch, capsys):
    """unittest for base.editor_init
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
        raise OSError('got an OSError')
    def mock_parse_nsmap_3(arg):
        """stub
        """
        raise testee.et.ParseError('got a ParseError')
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
    assert not testobj.readonly
    assert isinstance(testobj.gui, testee.Gui)
    assert (testobj.ns_prefixes, testobj.ns_uris) == ([], [])
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
    assert (testobj.ns_prefixes, testobj.ns_uris) == (['ns_prefix'], ['ns_uri'])
    assert (testobj.gui.cut_att, testobj.gui.cut_el) == (None, None)
    assert (testobj.search_args, testobj._search_pos) == ([], None)
    assert capsys.readouterr().out == ("called Gui.__init__\n"
                                       "called Gui.init_gui with args ()\n"
                                       "called Editor.init_tree with args ('(new root)',)\n"
                                       f"called parse_nsmap with arg {testobj.xmlfn}\n"
                                       "called Editor.init_tree with args ('got root from tree',)\n"
                                       "called Gui.go\n")
    testobj = testee.Editor('testfile.xml', readonly=True)
    assert testobj.title == f'{testee.TITLESTART} Viewer'
    assert testobj.xmlfn == os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testfile.xml')
    assert testobj.readonly
    assert isinstance(testobj.gui, testee.Gui)
    assert (testobj.ns_prefixes, testobj.ns_uris) == (['ns_prefix'], ['ns_uri'])
    assert not hasattr(testobj.gui, 'cut_att')
    assert not hasattr(testobj.gui, 'cut_el')
    assert (testobj.search_args, testobj._search_pos) == ([], None)
    assert capsys.readouterr().out == ("called Gui.__init__\n"
                                       "called Gui.init_gui with args ()\n"
                                       f"called parse_nsmap with arg {testobj.xmlfn}\n"
                                       "called Editor.init_tree with args ('got root from tree',)\n"
                                       "called Gui.go\n")
    monkeypatch.setattr(testee, 'parse_nsmap', mock_parse_nsmap_2)
    testobj = testee.Editor('testfile.xml')
    assert (testobj.ns_prefixes, testobj.ns_uris) == ([], [])
    assert capsys.readouterr().out == ("called Gui.__init__\n"
                                       "called Gui.init_gui with args ()\n"
                                       "called Editor.init_tree with args ('(new root)',)\n"
                                       "called Gui.meldfout with args ('got an OSError',)"
                                       " {'abort': True}\n"
                                       "called Gui.init_tree with args (None,)\n")
    monkeypatch.setattr(testee, 'parse_nsmap', mock_parse_nsmap_3)
    testobj = testee.Editor('testfile.xml')
    assert (testobj.ns_prefixes, testobj.ns_uris) == ([], [])
    assert capsys.readouterr().out == ("called Gui.__init__\n"
                                       "called Gui.init_gui with args ()\n"
                                       "called Editor.init_tree with args ('(new root)',)\n"
                                       "called Gui.meldfout with args ('got a ParseError',)"
                                       " {'abort': True}\n"
                                       "called Gui.init_tree with args (None,)\n")


def mock_init_editor(monkeypatch, capsys):
    """stub for setting up axe.base.Editor object
    """
    def mock_init(self, name):
        print(f"called Editor.__init__ with arg '{name}'")
    monkeypatch.setattr(testee.Editor, '__init__', mock_init)
    name = 'testfile'
    testobj = testee.Editor(name)
    testobj.gui = MockGui(testobj)
    testobj.xmlfn = name
    testobj._search_pos = None
    assert capsys.readouterr().out == (f"called Editor.__init__ with arg '{name}'\n"
                                       "called Gui.__init__\n")
    return testobj


def test_editor_mark_dirty(monkeypatch, capsys):
    """unittest for base.editor_mark_dirty
    """
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.readonly = True
    testobj.mark_dirty(True)
    assert testobj.tree_dirty
    assert capsys.readouterr().out == ''

    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.readonly = False
    testobj.title = 'appname'
    monkeypatch.setattr(testobj.gui, 'get_windowtitle', lambda *x: '')
    testobj.mark_dirty(True)
    assert testobj.tree_dirty
    assert capsys.readouterr().out == ''

    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.readonly = False
    testobj.title = 'appname'
    monkeypatch.setattr(testobj.gui, 'get_windowtitle', lambda *x: ' - ' + testobj.title)
    testobj.mark_dirty(True)
    assert testobj.tree_dirty
    assert capsys.readouterr().out == 'called Gui.set_windowtitle with arg `* - appname`\n'

    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.readonly = False
    testobj.title = 'appname'
    monkeypatch.setattr(testobj.gui, 'get_windowtitle', lambda *x: '* - ' + testobj.title)
    testobj.mark_dirty(True)
    assert testobj.tree_dirty
    assert capsys.readouterr().out == 'called Gui.set_windowtitle with arg ` - appname`\n'

    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.readonly = False
    testobj.title = 'appname'
    monkeypatch.setattr(testobj.gui, 'get_windowtitle', lambda *x: ' - ' + testobj.title)
    testobj.mark_dirty(False)
    assert not testobj.tree_dirty
    assert capsys.readouterr().out == 'called Gui.set_windowtitle with arg ` - appname`\n'


def test_editor_check_tree(monkeypatch, capsys):
    """unittest for base.editor_check_tree
    """
    def mock_savexml():
        """stub
        """
        print('called Editor.savexml')
    testobj = mock_init_editor(monkeypatch, capsys)
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


def test_editor_checkselection(monkeypatch, capsys):
    """unittest for base.editor_checkselection
    """
    testobj = mock_init_editor(monkeypatch, capsys)
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
    """unittest for base.editor_writexml
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
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.expandnode = mock_expandnode
    testobj.mark_dirty = mock_mark_dirty
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
    """unittest for base.editor_expandnode
    """
    counter = 0
    def mock_expand(*args):
        """stub
        """
        nonlocal counter
        print('called Element.expand with args', args)
        counter += 1
        if counter == 1:
            return 'subnode'
        return None
    testobj = mock_init_editor(monkeypatch, capsys)
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


def test_editor_init_tree(monkeypatch, capsys):
    """unittest for base.editor_init_tree
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
    testobj = mock_init_editor(monkeypatch, capsys)
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


def test_editor_add_nodes_for_namespaces_if_any(monkeypatch, capsys):
    """unittest for base.editor_add_nodes_for_namespaces_if_any
    """
    def mock_add(arg):
        print(f"called Gui.add_node_to_parent with arg '{arg}'")
        return arg
    def mock_set(*args):
        print("called Gui.set_node_title with args", args)
    testobj = mock_init_editor(monkeypatch, capsys)
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


def test_editor_add_to_tree(monkeypatch, capsys):
    """unittest for base.editor_add_to_tree
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
    testobj = mock_init_editor(monkeypatch, capsys)
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


def test_editor_getshortname(monkeypatch, capsys):
    """unittest for base.editor_getshortname
    """
    def mock_apply(name):
        print(f"called editor.apply_namespace_mapping with arg '{name}'")
        return name
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.apply_namespace_mapping = mock_apply
    assert testobj.getshortname(('xxx', '')) == '<> xxx'
    assert capsys.readouterr().out == "called editor.apply_namespace_mapping with arg 'xxx'\n"
    assert testobj.getshortname(('xxx', 'yyy')) == '<> xxx: yyy'
    assert capsys.readouterr().out == "called editor.apply_namespace_mapping with arg 'xxx'\n"
    assert testobj.getshortname(('xxx', 'yyy'), True) == 'xxx = yyy'
    assert capsys.readouterr().out == "called editor.apply_namespace_mapping with arg 'xxx'\n"
    assert testobj.getshortname(('xxx', 80 * 'y')) == f"<> xxx: {60 * 'y'}..."
    assert capsys.readouterr().out == "called editor.apply_namespace_mapping with arg 'xxx'\n"


def test_editor_apply_namespace_mapping(monkeypatch, capsys):
    """unittest for base.editor_apply_namespace_mapping
    """
    testobj = mock_init_editor(monkeypatch, capsys)
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


def test_editor_add_item(monkeypatch, capsys):
    """unittest for base.editor_add_item
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
    testobj = mock_init_editor(monkeypatch, capsys)
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


def test_editor_get_menu_data(monkeypatch, capsys):
    """unittest for base.editor_get_menu_data
    """
    testobj = mock_init_editor(monkeypatch, capsys)
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
    assert [x[0] for x in result[3]] == [ "&Find", "Find &Last", "Find &Next", "Find &Previous" ]
    testobj.readonly = True
    result = testobj.get_menu_data()
    assert len(result) == len(['File', 'View', 'Search'])
    assert [x[0] for x in result[0]] == ['&Open', 'E&xit']
    assert [x[0] for x in result[1]] == ["&Expand All (sub)Levels", "&Collapse All (sub)Levels"]
    assert [x[0] for x in result[2]] == [ "&Find", "Find &Last", "Find &Next", "Find &Previous" ]


def test_editor_flatten_tree(monkeypatch, capsys):
    """unittest for base.editor_flatten_tree
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
    testobj = mock_init_editor(monkeypatch, capsys)
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


def test_editor_find_first(monkeypatch, capsys):
    """unittest for base.editor_find_first
    """
    def mock_find_next(value):
        """stub
        """
        print(f'called Editor.find_next with arg `{value}`')
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.find_next = mock_find_next
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
    """unittest for base.editor_find_next
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
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.flatten_tree = mock_flatten_tree
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
    """unittest for base.editor_newxml
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
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.init_tree = mock_init_tree
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
    """unittest for base.editor_openxml
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
        raise testee.et.ParseError('error')
    def mock_parse_nsmap_ok(fname):
        """stub
        """
        return (MockElement(), 'prefixes', 'uris')
    testobj = mock_init_editor(monkeypatch, capsys)
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
    assert capsys.readouterr().out == ("called parse_nsmap with arg `fname`\n"
                                       "called Gui.meldfout with args ('error',) {}\n")
    monkeypatch.setattr(testee, 'parse_nsmap', mock_parse_nsmap_ok)
    testobj.openxml()
    assert capsys.readouterr().out == ("called Editor.init_tree with args ('element_root',"
                                       " 'prefixes', 'uris')\n")


def test_editor_savexml(monkeypatch, capsys):
    """unittest for base.editor_savexml
    """
    def mock_savexmlas():
        """stub
        """
        print('called Editor.savexmlas')
    def mock_writexml():
        """stub
        """
        print('called Editor.writexml')
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.savexmlas = mock_savexmlas
    testobj.writexml = mock_writexml
    testobj.xmlfn = ''
    testobj.savexml()
    assert capsys.readouterr().out == 'called Editor.savexmlas\n'
    testobj.xmlfn = 'x'
    testobj.savexml()
    assert capsys.readouterr().out == 'called Editor.writexml\n'


def test_editor_savexmlas(monkeypatch, capsys):
    """unittest for base.editor_savexmlas
    """
    def mock_writexml():
        """stub
        """
        print('called Editor.writexml')
    def mock_mark_dirty(value):
        """stub
        """
        print(f'called Editor.mark_dirty with arg `{value}`')
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.writexml = mock_writexml
    testobj.mark_dirty = mock_mark_dirty
    testobj.savexmlas()
    assert capsys.readouterr().out == 'called Gui.file_to_save\n'
    monkeypatch.setattr(testobj.gui, 'file_to_save', lambda *x: (True, 'filename'))
    testobj.savexmlas()
    assert capsys.readouterr().out == ('called Editor.writexml\n'
                                       'called Gui.set_node_title with args `treetop` `filename`\n'
                                       'called Editor.mark_dirty with arg `False`\n')


def test_editor_expand(monkeypatch, capsys):
    """unittest for base.editor_expand
    """
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.expand()
    assert capsys.readouterr().out == 'called Gui.expand_item with arg `None`\n'


def test_editor_collapse(monkeypatch, capsys):
    """unittest for base.editor_collapse
    """
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.collapse()
    assert capsys.readouterr().out == 'called Gui.collapse_item\n'


def test_editor_undo(monkeypatch, capsys):
    """unittest for base.editor_undo
    """
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.undo()
    assert capsys.readouterr().out == 'called Gui.do_undo\n'


def test_editor_redo(monkeypatch, capsys):
    """unittest for base.editor_redo
    """
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.redo()
    assert capsys.readouterr().out == 'called Gui.do_redo\n'


def test_editor_edit(monkeypatch, capsys):
    """unittest for base.editor_edit
    """
    testobj = mock_init_editor(monkeypatch, capsys)
    monkeypatch.setattr(testee.Editor, 'checkselection', lambda *x: False)
    testobj.edit()
    assert capsys.readouterr().out == ''
    monkeypatch.setattr(testee.Editor, 'checkselection', lambda *x: True)
    testobj.item = 'item'
    testobj.edit()
    assert capsys.readouterr().out == 'called Gui.edit_item with arg `item`\n'


def test_editor_cut(monkeypatch, capsys):
    """unittest for base.editor_cut
    """
    def mock_editor_copy(*args, **kwargs):
        """stub
        """
        print('called Editor.copy with args', args, kwargs)
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.copy = mock_editor_copy
    testobj.cut()
    assert capsys.readouterr().out == "called Editor.copy with args () {'cut': True}\n"


def test_editor_delete(monkeypatch, capsys):
    """unittest for base.editor_delete
    """
    def mock_editor_copy(*args, **kwargs):
        """stub
        """
        print('called Editor.copy with args', args, kwargs)
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.copy = mock_editor_copy
    testobj.delete()
    assert capsys.readouterr().out == ("called Editor.copy with args () {'cut': True,"
                                       " 'retain': False}\n")


def test_editor_copy(monkeypatch, capsys):
    """unittest for base.editor_copy
    """
    testobj = mock_init_editor(monkeypatch, capsys)
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
    assert capsys.readouterr().out == 'called Gui.meldfout with args ("Can\'t copy the root",) {}\n'
    testobj.copy(cut=True)
    assert capsys.readouterr().out == 'called Gui.meldfout with args ("Can\'t cut the root",) {}\n'
    testobj.copy(cut=True, retain=False)
    assert capsys.readouterr().out == 'called Gui.meldfout with args ("Can\'t delete the root",) {}\n'


def test_editor_paste_after(monkeypatch, capsys):
    """unittest for base.editor_paste_after
    """
    def mock_editor_paste(*args, **kwargs):
        """stub
        """
        print('called Editor.paste with args', args, kwargs)
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.paste = mock_editor_paste
    testobj.paste_after()
    assert capsys.readouterr().out == ("called Editor.paste with args () {'before': False}\n")


def test_editor_paste_under(monkeypatch, capsys):
    """unittest for base.editor_paste_under
    """
    def mock_editor_paste(*args, **kwargs):
        """stub
        """
        print('called Editor.paste with args', args, kwargs)
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.paste = mock_editor_paste
    testobj.paste_under()
    assert capsys.readouterr().out == "called Editor.paste with args () {'below': True}\n"


def test_editor_paste(monkeypatch, capsys):
    """unittest for base.editor_paste
    """
    def mock_get_title(node):
        """stub
        """
        return f'{testee.ELSTART} element'
    testobj = mock_init_editor(monkeypatch, capsys)
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


def test_editor_add_attr(monkeypatch, capsys):
    """unittest for base.editor_add_attr
    """
    def mock_get_title(node):
        """stub
        """
        return f'{testee.ELSTART} element'
    testobj = mock_init_editor(monkeypatch, capsys)
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
    assert capsys.readouterr().out == 'called Gui.add_attribute with arg `item`\n'


def test_editor_insert_after(monkeypatch, capsys):
    """unittest for base.editor_insert_after
    """
    def mock_insert(*args, **kwargs):
        """stub
        """
        print('called Editor.insert with args', args, kwargs)
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.insert = mock_insert
    testobj.insert_after()
    assert capsys.readouterr().out == "called Editor.insert with args () {'before': False}\n"


def test_editor_insert_child(monkeypatch, capsys):
    """unittest for base.editor_insert_child
    """
    def mock_insert(*args, **kwargs):
        """stub
        """
        print('called Editor.insert with args', args, kwargs)
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.insert = mock_insert
    testobj.insert_child()
    assert capsys.readouterr().out == f"called Editor.insert with args () {{'below': True}}\n"


def test_editor_insert(monkeypatch, capsys):
    """unittest for base.editor_insert
    """
    def mock_get_title(node):
        """stub
        """
        return f'{testee.ELSTART} element'
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.checkselection = lambda *x: False
    testobj.insert()
    assert capsys.readouterr().out == ''
    testobj.checkselection = lambda *x: True
    testobj.item = 'item'
    testobj.insert()
    assert capsys.readouterr().out == (
            "called Gui.get_node_parentpos with arg `item`\n"
            "called Gui.insert with args ('item',) {'before': True, 'below': False}\n")
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
            "called Gui.insert with args ('item',) {'before': True, 'below': True}\n")


def test_editor_search(monkeypatch, capsys):
    """unittest for base.editor_search
    """
    def mock_find_first(*args, **kwargs):
        """stub        """
        print('called Editor.find_first with args', args, kwargs)
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.find_first = mock_find_first
    testobj.search()
    assert capsys.readouterr().out == "called Editor.find_first with args () {}\n"


def test_editor_search_last(monkeypatch, capsys):
    """unittest for base.editor_search_last
    """
    def mock_find_first(*args, **kwargs):
        """stub
        """
        print('called Editor.find_first with args', args, kwargs)
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.find_first = mock_find_first
    testobj.search_last()
    assert capsys.readouterr().out == "called Editor.find_first with args () {'reverse': True}\n"


def test_editor_search_next(monkeypatch, capsys):
    """unittest for base.editor_search_next
    """
    def mock_find_next(*args, **kwargs):
        """stub
        """
        print('called Editor.find_next with args', args, kwargs)
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.find_next = mock_find_next
    testobj.search_next()
    assert capsys.readouterr().out == "called Editor.find_next with args () {}\n"


def test_editor_search_prev(monkeypatch, capsys):
    """unittest for base.editor_search_prev
    """
    def mock_find_next(*args, **kwargs):
        """stub
        """
        print('called Editor.find_next with args', args, kwargs)
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.find_next = mock_find_next
    testobj.search_prev()
    assert capsys.readouterr().out == "called Editor.find_next with args () {'reverse': True}\n"


def test_editor_build_search_description(monkeypatch, capsys):
    """unittest for base.editor_get_search_text
    """
    testobj = mock_init_editor(monkeypatch, capsys)
    assert testobj.build_search_description("", '', '', '') == ['' ]
    assert testobj.build_search_description("xxxx", '', '', '') == ['search for',
                                                                    ' an element that has a name',
                                                                    '   containing `xxxx`' ]
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
           '   containing `zzzz`' ]
    assert testobj.build_search_description("xxxx", 'yyyy', '', 'qqqq') == [
           'search for text',
           '   `qqqq`',
           ' under an element that has a name',
           '   containing `xxxx`',
           ' with an attribute that has a name',
           '   containing `yyyy`' ]
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
           '   containing `zzzz`' ]
    assert testobj.build_search_description("xxxx", 'yyyy', 'zzzz', 'qqqq') == [
           'search for text',
           '   `qqqq`',
           ' under an element that has a name',
           '   containing `xxxx`',
           ' with an attribute that has a name',
           '   containing `yyyy`',
           ' and a value',
           '   containing `zzzz`' ]


def test_editor_replace(monkeypatch, capsys):
    """unittest for base.editor_replace
    """
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.replace()
    assert capsys.readouterr().out == ("called Gui.meldinfo with args"
                                       " ('Replace: not sure if I wanna implement this',) {}\n")


def _test_editor_about(monkeypatch, capsys):  # about() wordt niet gebruikt
    """unittest for base.editor_about
    """
    testobj = mock_init_editor(monkeypatch, capsys)
    testobj.about()
    assert capsys.readouterr().out == f"called Gui.meldinfo with args ('{testee.ABOUT}',) {{}}\n"
