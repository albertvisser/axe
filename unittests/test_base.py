import os.path
import types
import pytest
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
    def set_windowtitle(self, title):
        print(f'called Gui.set_windowtitle with arg `{title}`')
    def get_windowtitle(self):
        pass
    def ask_yesnocancel(self):
        pass
    def get_selected_item(self):
        pass


def test_editor_init(monkeypatch, capsys):
    def mock_getroot(*args):
        return 'got root from tree'
    def mock_parse_nsmap(arg):
        print(f'called parse_nsmap with arg {arg}')
        return types.SimpleNamespace(getroot=mock_getroot), ['ns_prefix'], ['ns_uri']
    def mock_parse_nsmap_2(arg):
        raise IOError('got an IOError')
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
                                       "called Gui.meldfout with args ('got an IOError',)"
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


def _test_editor_(monkeypatch, capsys):
    monkeypatch.setattr(testee.Editor, '__init__', mock_editor_init)
    testobj = testee.Editor('testfile')
    assert capsys.readouterr().out == 'called Editor.__init__\ncalled Gui.__init__\n'


