"""unittests for ./axe/gui_wx.py
"""
from axe import wxgui as testee
from mockgui import mockwxwidgets as mockwx
import types


class TestGui:
    """unittest for gui_wx.Gui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.Gui object

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

    def test_init(self, monkeypatch, capsys):
        """unittest for Gui.__init__
        """
        monkeypatch.setattr(testee.wx, 'App', mockwx.MockApp)
        monkeypatch.setattr(testee.wx.Frame, '__init__', mockwx.MockFrame.__init__)
        monkeypatch.setattr(testee.wx.Frame, 'Show', mockwx.MockFrame.Show)
        testobj = testee.Gui()
        assert testobj.editor is None
        assert testobj.fn == ''
        assert testobj.editable
        assert capsys.readouterr().out == (
                "called app.__init__ with args ()\n"
                "called frame.__init__ with args () {'parent': None, 'pos': (2, 2)}\n"
                "called frame.Show\n")
        testobj = testee.Gui(parent='editor', fn='xxxx', readonly=True)
        assert testobj.editor == 'editor'
        assert testobj.fn == 'xxxx'
        assert not testobj.editable
        assert capsys.readouterr().out == (
                "called app.__init__ with args ()\n"
                "called frame.__init__ with args () {'parent': None, 'pos': (2, 2)}\n"
                "called frame.Show\n")

    def test_go(self, monkeypatch, capsys):
        """unittest for Gui.go
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.app = mockwx.MockApp()
        assert capsys.readouterr().out == "called app.__init__ with args ()\n"
        testobj.go()
        assert capsys.readouterr().out == "called app.MainLoop\n"

    def test_on_doubleclick(self, monkeypatch, capsys):
        """unittest for Gui.on_doubleclick
        """
        def mock_edit():
            print('called Gui.edit')
        def mock_hittest(*args):
            print('called tree.HitTest with args', args)
            return 'topitem', 0
        def mock_hittest_2(*args):
            print('called tree.HitTest with args', args)
            return 'item', 0
        def mock_get(*args):
            print('called tree.GetItemText with args', args)
            return '<> itemtext'
        def mock_count(*args):
            print('called tree.GetChildrenCount with args', args)
            return 1
        event = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(elstart='<>')
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.top = 'topitem'
        testobj.edit = mock_edit
        testobj.on_doubleclick(event)
        assert capsys.readouterr().out == (
                "called event.GetPosition\n"
                "called tree.HitTest with args ('position',)\n"
                "called event.Skip\n")
        testobj.tree.HitTest = mock_hittest
        testobj.on_doubleclick(event)
        assert capsys.readouterr().out == (
                "called event.GetPosition\n"
                "called tree.HitTest with args ('position',)\n"
                "called event.Skip\n")
        testobj.tree.HitTest = mock_hittest_2
        testobj.on_doubleclick(event)
        assert capsys.readouterr().out == (
                "called event.GetPosition\n"
                "called tree.HitTest with args ('position',)\n"
                "called tree.GetItemText with args ('item',)\n"
                "called Gui.edit\n"
                "called event.Skip\n")
        testobj.tree.GetItemText = mock_get
        testobj.on_doubleclick(event)
        assert capsys.readouterr().out == (
                "called event.GetPosition\n"
                "called tree.HitTest with args ('position',)\n"
                "called tree.GetItemText with args ('item',)\n"
                "called Tree.GetChildrenCount with args ('item',)\n"
                "called Gui.edit\n"
                "called event.Skip\n")
        testobj.tree.GetChildrenCount = mock_count
        testobj.on_doubleclick(event)
        assert capsys.readouterr().out == (
                "called event.GetPosition\n"
                "called tree.HitTest with args ('position',)\n"
                "called tree.GetItemText with args ('item',)\n"
                "called tree.GetChildrenCount with args ('item',)\n"
                "called event.Skip\n")

    def test_on_rightdown(self, monkeypatch, capsys):
        """unittest for Gui.on_rightdownlication
        """
        def mock_hittest(*args):
            print('called tree.HitTest with args', args)
            return 'topitem', 0
        def mock_hittest_2(*args):
            print('called tree.HitTest with args', args)
            return 'item', 0
        def mock_init(**kwargs):
            print('called Gui.init_menus with args', kwargs)
            return menu
        def mock_popup(arg):
            print(f'called Gui.PopupMenu with arg {arg}')
        event = mockwx.MockEvent()
        menu = mockwx.MockMenu()
        assert capsys.readouterr().out == ("called event.__init__ with args ()\n"
                                           "called Menu.__init__ with args ()\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.top = 'topitem'
        testobj.init_menus = mock_init
        testobj.PopupMenu = mock_popup
        testobj.on_rightdown(event)
        assert capsys.readouterr().out == (
                "called event.GetPosition\n"
                "called tree.HitTest with args ('position',)\n")
        testobj.tree.HitTest = mock_hittest
        testobj.on_rightdown(event)
        assert capsys.readouterr().out == (
                "called event.GetPosition\n"
                "called tree.HitTest with args ('position',)\n")
        testobj.tree.HitTest = mock_hittest_2
        testobj.on_rightdown(event)
        assert capsys.readouterr().out == (
                "called event.GetPosition\n"
                "called tree.HitTest with args ('position',)\n"
                "called tree.SelectItem with args ('item',)\n"
                "called Gui.init_menus with args {'popup': True}\n"
                "called Gui.PopupMenu with arg A Menu\n"
                "called menu.Destroy\n")

    def test_afsl(self, monkeypatch, capsys):
        """unittest for Gui.afsl
        """
        def mock_check():
            print("called Editor.check_tree")
            return False
        def mock_check_2():
            print("called Editor.check_tree")
            return True
        event = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor = types.SimpleNamespace(check_tree=mock_check)
        testobj.afsl(event)
        assert capsys.readouterr().out == ("called Editor.check_tree\n"
                                           "called event.Veto\n"
                                           "called event.Skip\n")
        testobj.editor.check_tree = mock_check_2
        testobj.afsl(event)
        assert capsys.readouterr().out == ("called Editor.check_tree\n"
                                           "called event.Skip\n")

    def test_get_node_children(self, monkeypatch, capsys):
        """unittest for Gui.get_node_children
        """
        def mock_GetFirstChild(self, *args):
            print('called tree.GetFirstChild with args', args)
            return first, 0
        def mock_GetNextChild(self, *args):
            cookie = args[1]
            print('called tree.GetNextChild with args', args)
            if cookie == 0:
                return item, 1
            return last, -1
        monkeypatch.setattr(mockwx.MockTree, 'GetFirstChild', mock_GetFirstChild)
        monkeypatch.setattr(mockwx.MockTree, 'GetNextChild', mock_GetNextChild)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        first = mockwx.MockTreeItem('first')
        last = mockwx.MockTreeItem('not ok')
        item = mockwx.MockTreeItem('next')
        assert capsys.readouterr().out == ("called Tree.__init__ with args () {}\n"
                                           "called TreeItem.__init__ with args ('first',)\n"
                                           "called TreeItem.__init__ with args ('not ok',)\n"
                                           "called TreeItem.__init__ with args ('next',)\n")
        assert testobj.get_node_children('node') == [first, item]
        assert capsys.readouterr().out == ("called tree.GetFirstChild with args ('node',)\n"
                                           "called TreeItem.IsOk\n"
                                           "called tree.GetNextChild with args ('node', 0)\n"
                                           "called TreeItem.IsOk\n"
                                           "called tree.GetNextChild with args ('node', 1)\n"
                                           "called TreeItem.IsOk\n")

    def test_get_node_title(self, monkeypatch, capsys):
        """unittest for Gui.get_node_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        assert testobj.get_node_title('node') == "itemtext"
        assert capsys.readouterr().out == "called tree.GetItemText with args ('node',)\n"

    def test_get_node_data(self, monkeypatch, capsys):
        """unittest for Gui.get_node_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        assert testobj.get_node_data('node') == 'itemdata'
        assert capsys.readouterr().out == "called tree.GetItemData with args ('node',)\n"

    def test_get_treetop(self, monkeypatch, capsys):
        """unittest for Gui.get_treetop
        """
        def mock_get(*args):
            print('called tree.GetLastChild with args', args)
            return last
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        last = mockwx.MockTreeItem('last')
        assert capsys.readouterr().out == ("called Tree.__init__ with args () {}\n"
                                           "called TreeItem.__init__ with args ('last',)\n")
        testobj.tree.GetLastChild = mock_get
        assert testobj.get_treetop() == last
        assert capsys.readouterr().out == ("called tree.getRootItem\n"
                                           "called tree.GetLastChild with args ('rootitem',)\n")

    def test_setup_new_tree(self, monkeypatch, capsys):
        """unittest for Gui.setup_new_tree
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        assert testobj.setup_new_tree('title') == "The Root"
        assert capsys.readouterr().out == ("called tree.DeleteAllItems\n"
                                           "called tree.AddRoot with args ('title',)\n")

    def test_add_node_to_parent(self, monkeypatch, capsys):
        """unittest for Gui.add_node_to_parent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        assert testobj.add_node_to_parent('parent') == "appended item"
        assert capsys.readouterr().out == ("called tree.AppendItem with args ('parent', '')\n")
        assert testobj.add_node_to_parent('parent', pos=1) == "inserted item"
        assert capsys.readouterr().out == ("called tree.InsertItem with args ('parent', 1, '')\n")

    def test_set_node_title(self, monkeypatch, capsys):
        """unittest for Gui.set_node_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.set_node_title('node', 'title')
        assert capsys.readouterr().out == ("called tree.SetItemText with args ('node', 'title')\n")

    def test_get_node_parentpos(self, monkeypatch, capsys):
        """unittest for Gui.get_node_parentpos
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        assert testobj.get_node_parentpos('node') == ('parent', 2)
        assert capsys.readouterr().out == ("called tree.GetItemParent with args ('node',)\n"
                                           "called tree.GetFirstChild with args ('node',)\n"
                                           "called TreeItem.__init__ with args ('first',)\n"
                                           "called TreeItem.IsOk\n"
                                           "called tree.GetNextChild with args ('node', 0)\n"
                                           "called TreeItem.__init__ with args ('next',)\n"
                                           "called TreeItem.IsOk\n"
                                           "called tree.GetNextChild with args ('node', 1)\n"
                                           "called TreeItem.__init__ with args ('not ok',)\n"
                                           "called TreeItem.IsOk\n")

    def test_set_node_data(self, monkeypatch, capsys):
        """unittest for Gui.set_node_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.set_node_data('node', 'name', 'value')
        assert capsys.readouterr().out == (
                "called tree.SetItemData() with args ('node', ('name', 'value'))\n")

    def test_get_selected_item(self, monkeypatch, capsys):
        """unittest for Gui.get_selected_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        assert testobj.get_selected_item() == "selection"
        assert capsys.readouterr().out == "called tree.GetSelection\n"

    def test_set_selected_item(self, monkeypatch, capsys):
        """unittest for Gui.set_selected_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.set_selected_item('item')
        assert capsys.readouterr().out == "called tree.SelectItem with args ('item',)\n"

    def test_is_node_root(self, monkeypatch, capsys):
        """unittest for Gui.is_node_root
        """
        def mock_get(*args):
            print('called tree.GetItemData with args', args)
            return tag, text
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.item = 'an item'
        testobj.tree.GetItemData = mock_get
        testobj.editor = types.SimpleNamespace(rt=types.SimpleNamespace(tag='tag', text='text'))
        tag, text = '', ''
        assert not testobj.is_node_root()
        assert capsys.readouterr().out == ("called tree.GetItemData with args ('an item',)\n")
        tag, text = 'xxx', 'yyy'
        assert not testobj.is_node_root('item')
        assert capsys.readouterr().out == ("called tree.GetItemData with args ('item',)\n")
        tag, text = 'tag', 'yyy'
        assert not testobj.is_node_root('item')
        assert capsys.readouterr().out == ("called tree.GetItemData with args ('item',)\n")
        tag, text = 'tag', ''
        assert not testobj.is_node_root('item')
        assert capsys.readouterr().out == ("called tree.GetItemData with args ('item',)\n")
        tag, text = 'xxx', 'text'
        assert not testobj.is_node_root('item')
        assert capsys.readouterr().out == ("called tree.GetItemData with args ('item',)\n")
        tag, text = 'tag', 'text'
        assert testobj.is_node_root('item')
        assert capsys.readouterr().out == ("called tree.GetItemData with args ('item',)\n")

    def test_expand_item(self, monkeypatch, capsys):
        """unittest for Gui.expand_item
        """
        def mock_get():
            print('called tree.GetSelection')
            return ''
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.expand_item('item')
        assert capsys.readouterr().out == "called tree.ExpandAllChildren with args ('item',)\n"
        testobj.expand_item()
        assert capsys.readouterr().out == (
                "called tree.GetSelection\n"
                "called tree.ExpandAllChildren with args ('selection',)\n")
        testobj.tree.GetSelection = mock_get
        testobj.expand_item()
        assert capsys.readouterr().out == "called tree.GetSelection\n"

    def test_collapse_item(self, monkeypatch, capsys):
        """unittest for Gui.collapse_item
        """
        def mock_get():
            print('called tree.GetSelection')
            return ''
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.collapse_item('item')
        assert capsys.readouterr().out == "called tree.CollapseAllChildren with args ('item',)\n"
        testobj.collapse_item()
        assert capsys.readouterr().out == (
                "called tree.GetSelection\n"
                "called tree.CollapseAllChildren with args ('selection',)\n")
        testobj.tree.GetSelection = mock_get
        testobj.collapse_item()
        assert capsys.readouterr().out == "called tree.GetSelection\n"

    def test_edit_item(self, monkeypatch, capsys):
        """unittest for Gui.edit_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.edit_item('item', 'oldstate', ('title', 'tag', 'text'), 'edit')
        assert capsys.readouterr().out == (
                "called tree.SetItemText with args ('item', 'title')\n"
                "called tree.SetItemData() with args ('item', ('tag', 'text'))\n")

    def _test_copy(self, monkeypatch, capsys):
        """unittest for Gui.copy
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.copy('item')
        assert capsys.readouterr().out == ("")
        testobj.copy('item', cut=True, retain=False)
        assert capsys.readouterr().out == ("")

    def _test_paste(self, monkeypatch, capsys):
        """unittest for Gui.paste
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.paste('item')
        assert capsys.readouterr().out == ("")
        testobj.paste('item', before=False, below=True)
        assert capsys.readouterr().out == ("")

    def test_add_attribute(self, monkeypatch, capsys):
        """unittest for Gui.add_attribute
        """
        def mock_add(*args, **kwargs):
            print('called Editor.add_item with args', args, kwargs)
            return 'node'
        def mock_is(*args):
            print('called tree.IsExpanded with args', args)
            return True
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.editor = types.SimpleNamespace(add_item=mock_add)
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.add_attribute('item', 'name', 'value', 'text')
        assert capsys.readouterr().out == (
                "called Editor.add_item with args ('item', 'name', 'value') {'attr': True}\n"
                "called tree.GetItemParent with args ('node',)\n"
                "called tree.IsExpanded with args ('parent',)\n"
                "called tree.Expand with args ('parent',)\n")
        testobj.tree.IsExpanded = mock_is
        testobj.add_attribute('item', 'name', 'value', 'text')
        assert capsys.readouterr().out == (
                "called Editor.add_item with args ('item', 'name', 'value') {'attr': True}\n"
                "called tree.GetItemParent with args ('node',)\n"
                "called tree.IsExpanded with args ('parent',)\n")

    def test_insert(self, monkeypatch, capsys):
        """unittest for Gui.insert
        """
        def mock_add(*args, **kwargs):
            print('called Editor.add_item with args', args, kwargs)
            return 'node'
        def mock_is(*args):
            print('called tree.IsExpanded with args', args)
            return True
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.editor = types.SimpleNamespace(add_item=mock_add)
        testobj.insert('item', 'tag', 'text', 'commandtext')
        assert capsys.readouterr().out == (
                "called Editor.add_item with args"
                " ('item', 'tag', 'text') {'before': True, 'below': False}\n"
                "called tree.GetItemParent with args ('node',)\n"
                "called tree.IsExpanded with args ('parent',)\n"
                "called tree.Expand with args ('parent',)\n")
        testobj.tree.IsExpanded = mock_is
        testobj.insert('item', 'tag', 'text', 'commandtext', before=False, below=True)
        assert capsys.readouterr().out == (
                "called Editor.add_item with args"
                " ('item', 'tag', 'text') {'before': False, 'below': True}\n"
                "called tree.GetItemParent with args ('node',)\n"
                "called tree.IsExpanded with args ('parent',)\n")

    def _test_init_gui(self, monkeypatch, capsys):
        """unittest for Gui.init_gui
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.init_gui() == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_set_windowtitle(self, monkeypatch, capsys):
        """unittest for Gui.set_windowtitle
        """
        monkeypatch.setattr(testee.wx.Frame, 'SetTitle', mockwx.MockFrame.SetTitle)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_windowtitle('text')
        assert capsys.readouterr().out == "called Frame.SetTitle with args ('text',)\n"

    def test_get_windowtitle(self, monkeypatch, capsys):
        """unittest for Gui.get_windowtitle
        """
        monkeypatch.setattr(testee.wx.Frame, 'GetTitle', mockwx.MockFrame.GetTitle)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_windowtitle() == "frame title"
        assert capsys.readouterr().out == "called Frame.GetTitle with args ()\n"

    def _test_init_menus(self, monkeypatch, capsys):
        """unittest for Gui.init_menus
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.init_menus(popup=False) == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_meldinfo(self, monkeypatch, capsys):
        """unittest for Gui.meldinfo
        """
        monkeypatch.setattr(testee.wx, 'MessageBox', mockwx.mock_messagebox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor = types.SimpleNamespace(title='title')
        testobj.meldinfo('text')
        assert capsys.readouterr().out == (
                "called wx.MessageBox with args ('text', 'title', 2052) {}\n")

    def test_meldfout(self, monkeypatch, capsys):
        """unittest for Gui.meldfout
        """
        def mock_quit():
            print('called Gui.quit')
        monkeypatch.setattr(testee.wx, 'MessageBox', mockwx.mock_messagebox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor = types.SimpleNamespace(title='title')
        testobj.quit = mock_quit
        testobj.meldfout('text')
        assert capsys.readouterr().out == (
                "called wx.MessageBox with args ('text', 'title', 516) {}\n")
        testobj.meldfout('text', abort=True)
        assert capsys.readouterr().out == (
                "called wx.MessageBox with args ('text', 'title', 516) {}\n"
                "called Gui.quit\n")

    def test_ask_yesnocancel(self, monkeypatch, capsys):
        """unittest for Gui.ask_yesnocancel
        """
        def mock_messagebox(*args, **kwargs):
            print('called wx.MessageBox with args', args, kwargs)
            return testee.wx.YES
        def mock_messagebox_2(*args, **kwargs):
            print('called wx.MessageBox with args', args, kwargs)
            return testee.wx.NO
        def mock_messagebox_3(*args, **kwargs):
            print('called wx.MessageBox with args', args, kwargs)
            return testee.wx.CANCEL
        monkeypatch.setattr(testee.wx, 'MessageBox', mock_messagebox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor = types.SimpleNamespace(title='title')
        assert testobj.ask_yesnocancel('prompt') == 1
        assert capsys.readouterr().out == (
                "called wx.MessageBox with args ('prompt', 'title') {'style': 26}\n")
        monkeypatch.setattr(testee.wx, 'MessageBox', mock_messagebox_2)
        testobj.editor = types.SimpleNamespace(title='title')
        assert testobj.ask_yesnocancel('prompt') == 0
        assert capsys.readouterr().out == (
                "called wx.MessageBox with args ('prompt', 'title') {'style': 26}\n")
        monkeypatch.setattr(testee.wx, 'MessageBox', mock_messagebox_3)
        testobj.editor = types.SimpleNamespace(title='title')
        assert testobj.ask_yesnocancel('prompt') == -1
        assert capsys.readouterr().out == (
                "called wx.MessageBox with args ('prompt', 'title') {'style': 26}\n")

    def test_ask_for_text(self, monkeypatch, capsys):
        """unittest for Gui.ask_for_text
        """
        monkeypatch.setattr(testee.wx, 'GetTextFromUser', mockwx.mock_get_text_from_user)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor = types.SimpleNamespace(title='title')
        assert testobj.ask_for_text('prompt') == ""
        assert capsys.readouterr().out == (
                "called wx.GetTextFromUser with args ('prompt', 'title', '') {}\n")
        monkeypatch.setattr(testee.wx, 'GetTextFromUser', mockwx.mock_get_text_from_user_2)
        testobj.editor = types.SimpleNamespace(title='title')
        assert testobj.ask_for_text('prompt', value='xxx') == "text from user"
        assert capsys.readouterr().out == (
                "called wx.GetTextFromUser with args ('prompt', 'title', 'xxx') {}\n")

    def test_file_to_read(self, monkeypatch, capsys):
        """unittest for Gui.file_to_read
        """
        def mock_show(self):
            print('called FileDialog.ShowModal')
            return testee.wx.ID_CANCEL
        monkeypatch.setattr(testee.wx, 'FileDialog', mockwx.MockFileDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.file_to_read() == (True, 'dirname/filename')
        assert capsys.readouterr().out == (
            "called FileDialog.__init__ with args"
            " () {'message': 'Choose a file', 'defaultDir': '/home/albert/projects/xmledit',"
            " 'wildcard': 'XML files (*.xml, *.XML)|*.xml;*.XML|All files (*.*)|*.*',"
            " 'style': 1}\n"
            "called FileDialog.ShowModal\n"
            "called FileDialog.GetPath\n")
        monkeypatch.setattr(testee.wx.FileDialog, 'ShowModal', mock_show)
        assert testobj.file_to_read() == (False, '')
        assert capsys.readouterr().out == (
            "called FileDialog.__init__ with args"
            " () {'message': 'Choose a file', 'defaultDir': '/home/albert/projects/xmledit',"
            " 'wildcard': 'XML files (*.xml, *.XML)|*.xml;*.XML|All files (*.*)|*.*',"
            " 'style': 1}\n"
            "called FileDialog.ShowModal\n")

    def test_file_to_save(self, monkeypatch, capsys):
        """unittest for Gui.file_to_save
        """
        def mock_show(self):
            print('called FileDialog.ShowModal')
            return testee.wx.ID_CANCEL
        monkeypatch.setattr(testee.wx, 'FileDialog', mockwx.MockFileDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor = types.SimpleNamespace(xmlfn='path/to/xyz')
        assert testobj.file_to_save() == (True, 'dirname/filename')
        assert capsys.readouterr().out == (
            "called FileDialog.__init__ with args"
            " () {'message': 'Save file as ...', 'defaultDir': 'path/to', 'defaultFile': 'xyz',"
            " 'wildcard': 'XML files (*.xml, *.XML)|*.xml;*.XML|All files (*.*)|*.*',"
            " 'style': 2}\n"
            "called FileDialog.ShowModal\n"
            "called FileDialog.GetPath\n")
        monkeypatch.setattr(testee.wx.FileDialog, 'ShowModal', mock_show)
        assert testobj.file_to_save() == (False, '')
        assert capsys.readouterr().out == (
            "called FileDialog.__init__ with args"
            " () {'message': 'Save file as ...', 'defaultDir': 'path/to', 'defaultFile': 'xyz',"
            " 'wildcard': 'XML files (*.xml, *.XML)|*.xml;*.XML|All files (*.*)|*.*',"
            " 'style': 2}\n"
            "called FileDialog.ShowModal\n")

    def test_enable_pasteitems(self, monkeypatch, capsys):
        """unittest for Gui.enable_pasteitems
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pastebefore_text = 'xxx'
        testobj.pastebefore_item = mockwx.MockMenuItem()
        testobj.pasteafter_item = mockwx.MockMenuItem()
        testobj.pasteunder_item = mockwx.MockMenuItem()
        assert capsys.readouterr().out == ("called MenuItem.__init__ with args () {}\n"
                                           "called MenuItem.__init__ with args () {}\n"
                                           "called MenuItem.__init__ with args () {}\n")
        testobj.enable_pasteitems()
        assert capsys.readouterr().out == (
                "called menuitem.SetItemLabel with arg 'Nothing to Paste'\n"
                "called menuitem.Enable with arg False\n"
                "called menuitem.Enable with arg False\n"
                "called menuitem.Enable with arg False\n")
        testobj.enable_pasteitems(active=True)
        assert capsys.readouterr().out == (
                "called menuitem.SetItemLabel with arg 'xxx'\n"
                "called menuitem.Enable with arg True\n"
                "called menuitem.Enable with arg True\n"
                "called menuitem.Enable with arg True\n")

    def _test_popupmenu(self, monkeypatch, capsys):
        """unittest for Gui.popupmenu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.popupmenu('item') == "expected_result"
        assert capsys.readouterr().out == ("")
        # niet geimplementeerd

    def test_quit(self, monkeypatch, capsys):
        """unittest for Gui.quit
        """
        monkeypatch.setattr(testee.wx.Frame, 'Close', mockwx.MockFrame.Close)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.quit('event')
        assert capsys.readouterr().out == "called Frame.Close with arg False\n"

    def test_on_keyup(self, monkeypatch, capsys):
        """unittest for Gui.on_keyup
        """
        def mock_getkey():
            print("called event.GetKeyCode")
            return ''
        def mock_get():
            print('called tree.GetSelection')
            return item
        event = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        event.GetKeyCode = mock_getkey
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.top = 'top'
        testobj.tree.GetSelection = mock_get
        item = ''
        testobj.on_keyup(event)
        assert capsys.readouterr().out == ("called event.GetKeyCode\n"
                                           "called tree.GetSelection\n"
                                           "called event.Skip\n")
        item = 'top'
        testobj.on_keyup(event)
        assert capsys.readouterr().out == ("called event.GetKeyCode\n"
                                           "called tree.GetSelection\n"
                                           "called event.Skip\n")
        item = 'item'
        testobj.on_keyup(event)
        assert capsys.readouterr().out == ("called event.GetKeyCode\n"
                                           "called tree.GetSelection\n"
                                           "called event.Skip\n")

    def test_on_keyup_2(self, monkeypatch, capsys):
        """unittest for Gui.on_keyup
        """
        def mock_getkey():
            print("called event.GetKeyCode")
            return testee.wx.WXK_RETURN
        def mock_has(*args):
            print('called tree.ItemHasChildren with args', args)
            return True
        def mock_is(*args):
            print('called tree.IsExpanded with args', args)
            return True
        def mock_edit():
            print('called Editor.edit')
        event = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        event.GetKeyCode = mock_getkey
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.editor = types.SimpleNamespace(edit=mock_edit)
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.top = 'top'
        testobj.on_keyup(event)
        assert capsys.readouterr().out == ("called event.GetKeyCode\n"
                                           "called tree.GetSelection\n"
                                           "called tree.ItemHasChildren with args ('selection',)\n"
                                           "called Editor.edit\n"
                                           "called event.Skip\n")
        testobj.tree.ItemHasChildren = mock_has
        testobj.on_keyup(event)
        assert capsys.readouterr().out == ("called event.GetKeyCode\n"
                                           "called tree.GetSelection\n"
                                           "called tree.ItemHasChildren with args ('selection',)\n"
                                           "called tree.IsExpanded with args ('selection',)\n"
                                           "called tree.Expand with args ('selection',)\n"
                                           "called tree.GetFirstChild with args ('selection',)\n"
                                           "called TreeItem.__init__ with args ('first',)\n"
                                           "called tree.SelectItem with args (first,)\n"
                                           "called event.Skip\n")
        testobj.tree.IsExpanded = mock_is
        testobj.on_keyup(event)
        assert capsys.readouterr().out == ("called event.GetKeyCode\n"
                                           "called tree.GetSelection\n"
                                           "called tree.ItemHasChildren with args ('selection',)\n"
                                           "called tree.IsExpanded with args ('selection',)\n"
                                           "called tree.Collapse with args ('selection',)\n"
                                           "called event.Skip\n")

    def test_on_keyup_3(self, monkeypatch, capsys):
        """unittest for Gui.on_keyup
        """
        def mock_getkey():
            print("called event.GetKeyCode")
            return testee.wx.WXK_BACK
        def mock_is(*args):
            print('called tree.IsExpanded with args', args)
            return True
        event = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        event.GetKeyCode = mock_getkey
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == "called Tree.__init__ with args () {}\n"
        testobj.top = 'top'
        testobj.on_keyup(event)
        assert capsys.readouterr().out == ("called event.GetKeyCode\n"
                                           "called tree.GetSelection\n"
                                           "called tree.IsExpanded with args ('selection',)\n"
                                           "called tree.GetItemParent with args ('selection',)\n"
                                           "called tree.SelectItem with args ('parent',)\n"
                                           "called event.Skip\n")
        testobj.tree.IsExpanded = mock_is
        testobj.on_keyup(event)
        assert capsys.readouterr().out == ("called event.GetKeyCode\n"
                                           "called tree.GetSelection\n"
                                           "called tree.IsExpanded with args ('selection',)\n"
                                           "called tree.Collapse with args ('selection',)\n"
                                           "called tree.GetItemParent with args ('selection',)\n"
                                           "called tree.SelectItem with args ('parent',)\n"
                                           "called event.Skip\n")

    # def _test_ask_for_search_args(self, monkeypatch, capsys):
    #     """unittest for Gui.ask_for_search_args
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.ask_for_search_args() == "expected_result"
    #     assert capsys.readouterr().out == ("")

    def _test_do_undo(self, monkeypatch, capsys):
        """unittest for Gui.do_undo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.do_undo() == "expected_result"
        assert capsys.readouterr().out == ("")
        # (nog) niet geïmplementeerd

    def _test_do_redo(self, monkeypatch, capsys):
        """unittest for Gui.do_redo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.do_redo() == "expected_result"
        assert capsys.readouterr().out == ("")
        # (nog) niet geïmplementeerd


def test_show_dialog(capsys):
    "unittest for wxgui.show_dialog"
    def mock_show():
        print('called Dialog.ShowModal')
        return testee.wx.ID_CANCEL
    def mock_show_2():
        print('called Dialog.ShowModal')
        return testee.wx.ID_OK
    def mock_accept():
        nonlocal counter
        print('called Dialog.accept')
        counter += 1
        return counter > 1
    dialog = mockwx.MockDialog('')
    assert capsys.readouterr().out == "called Dialog.__init__ with args () {}\n"
    dialog.accept = mock_accept
    dialog.ShowModal = mock_show
    assert not testee.show_dialog(dialog)
    assert capsys.readouterr().out == "called Dialog.ShowModal\n"
    counter = 0
    dialog.ShowModal = mock_show_2
    assert testee.show_dialog(dialog)
    assert capsys.readouterr().out == ("called Dialog.ShowModal\n"
                                       "called Dialog.accept\n"
                                       "called Dialog.ShowModal\n"
                                       "called Dialog.accept\n")


class TestDialogGui:
    """unittests for wxgui.DialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.DialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called DialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.DialogGui, '__init__', mock_init)
        testobj = testee.DialogGui()
        assert capsys.readouterr().out == 'called DialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for DialogGui.__init__
        """
        monkeypatch.setattr(testee.wx.Dialog, 'SetIcon', mockwx.MockDialog.SetIcon)
        monkeypatch.setattr(testee.wx, 'Dialog', mockwx.MockDialog)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'GridBagSizer', mockwx.MockGridSizer)
        parent = types.SimpleNamespace(icon='icon')
        testobj = testee.DialogGui('master', parent, 'title')
        assert testobj.master == 'master'
        assert isinstance(testobj.sizer, testee.wx.BoxSizer)
        assert isinstance(testobj.gsizer, testee.wx.GridBagSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {'title': 'title', 'style': 536877120}\n"
                "called Dialog.SetIcon with args ('icon',)\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called GridSizer.__init__ with args (2, 2) {}\n")

    def test_add_label(self, monkeypatch, capsys):
        """unittest for DialogGui.add_label
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        result = testobj.add_label('text', 'row', 'col')
        assert isinstance(result, testee.wx.StaticText)
        assert capsys.readouterr().out == (
                "called StaticText.__init__ with args"
                f" ({testobj},) {{'label': 'element name:  '}}\n"
                "called GridSizer.Add with args"
                " MockStaticText (('row', 'col'),) {'flag': 48, 'border': 5}\n")
        result = testobj.add_label('text', 'row', 'col', fullwidth=True)
        assert isinstance(result, testee.wx.StaticText)
        assert capsys.readouterr().out == (
                "called StaticText.__init__ with args"
                f" ({testobj},) {{'label': 'element name:  '}}\n"
                "called GridSizer.Cols\n"
                "called GridSizer.Add with args"
                " MockStaticText (('row', 'col'), (1, 'cols'), 48, 5)\n")

    def test_add_lineinput(self, monkeypatch, capsys):
        """unittest for DialogGui.add_lineinput
        """
        monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        result = testobj.add_lineinput('row', 'col')
        assert isinstance(result, testee.wx.TextCtrl)
        assert capsys.readouterr().out == (
                f"called TextCtrl.__init__ with args ({testobj},) {{'size': (200, -1)}}\n"
                "called GridSizer.Add with args"
                " MockTextCtrl (('row', 'col'),) {'flag': 2080, 'border': 5}\n")
        result = testobj.add_lineinput('row', 'col', 'text', 'callback')
        assert isinstance(result, testee.wx.TextCtrl)
        assert capsys.readouterr().out == (
                f"called TextCtrl.__init__ with args ({testobj},) {{'size': (200, -1)}}\n"
                "called GridSizer.Add with args"
                " MockTextCtrl (('row', 'col'),) {'flag': 2080, 'border': 5}\n"
                "called text.SetValue with args ('text',)\n"
                f"called TextCtrl.Bind with args ({testee.wx.EVT_TEXT}, 'callback')\n")

    def test_add_checkbox(self, monkeypatch, capsys):
        """unittest for DialogGui.add_checkbox
        """
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        result = testobj.add_checkbox('text', 'row', 'col')
        assert isinstance(result, testee.wx.CheckBox)
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called GridSizer.Add with args MockCheckBox (('row', 'col'),) {'flag': 2048}\n")
        result = testobj.add_checkbox('text', 'row', 'col', readonly=True)
        assert isinstance(result, testee.wx.CheckBox)
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called GridSizer.Add with args MockCheckBox (('row', 'col'),) {'flag': 2048}\n"
                "called CheckBox.Enable with arg False\n")

    def test_add_combobox(self, monkeypatch, capsys):
        """unittest for DialogGui.add_combobox
        """
        monkeypatch.setattr(testee.wx, 'ComboBox', mockwx.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        result = testobj.add_combobox(['items'], 'row', 'col')
        assert isinstance(result, testee.wx.ComboBox)
        assert capsys.readouterr().out == (
                f"called ComboBox.__init__ with args ({testobj},) {{'size': (120, -1)}}\n"
                "called combobox.AppendItems with args (['items'],)\n"
                "called GridSizer.Add with args MockComboBox (('row', 'col'),)\n")

    def test_add_textinput(self, monkeypatch, capsys):
        """unittest for DialogGui.add_textinput
        """
        monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        result = testobj.add_textinput('row', 'col')
        assert isinstance(result, testee.wx.TextCtrl)
        assert capsys.readouterr().out == (
                "called TextCtrl.__init__ with args"
                f" ({testobj},) {{'size': (300, 140), 'style': 32}}\n"
                "called GridSizer.Add with args MockTextCtrl (('row', 'col'), (1, 2), 496)\n")

    def test_add_buttons(self, monkeypatch, capsys):
        """unittest for DialogGui.add_buttons
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAffirmativeId',
                            mockwx.MockDialog.SetAffirmativeId)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_buttons([(), (), ('text', 'callback')])
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5003}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, {testobj.accept}) {{}}\n"
                "called hori sizer.Add with args MockButton (0, 8432, 2)\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5101}}\n"
                "called hori sizer.Add with args MockButton (0, 8432, 2)\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, 'callback') {{}}\n"
                "called hori sizer.Add with args MockButton (0, 8432, 2)\n"
                "called  sizer.Add with args MockBoxSizer (0, 2544, 2)\n"
                "called dialog.SetAffirmativeId with args (5003,)\n")

    def test_finish_display(self, monkeypatch, capsys):
        """unittest for DialogGui.finish_display
        """
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        monkeypatch.setattr(testee.wx.Dialog, 'Layout', mockwx.MockDialog.Layout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.finish_display()
        assert capsys.readouterr().out == ("called dialog.SetSizer with args ( sizer,)\n"
                                           "called dialog.SetAutoLayout with args (True,)\n"
                                           f"called  sizer.Fit with args ({testobj},)\n"
                                           f"called  sizer.SetSizeHints with args ({testobj},)\n"
                                           "called dialog.Layout with args ()\n")

    def test_set_lineinput_text(self, monkeypatch, capsys):
        """unittest for DialogGui.set_lineinput_text
        """
        tb = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_lineinput_text(tb, 'text')
        assert capsys.readouterr().out == "called text.SetValue with args ('text',)\n"

    def test_set_checkbox_state(self, monkeypatch, capsys):
        """unittest for DialogGui.set_checkbox_state
        """
        cb = mockwx.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_checkbox_state(cb, 'value')
        assert capsys.readouterr().out == "called checkbox.SetValue with args ('value',)\n"

    def test_set_combobox_index(self, monkeypatch, capsys):
        """unittest for DialogGui.set_combobox_index
        """
        cmb = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_combobox_index(cmb, 'value')
        assert capsys.readouterr().out == "called combobox.SetSelection with args ('value',)\n"

    def test_set_textinput_text(self, monkeypatch, capsys):
        """unittest for DialogGui.set_textinput_text
        """
        tb = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_textinput_text(tb, 'text')
        assert capsys.readouterr().out == "called text.SetValue with args ('text',)\n"

    def test_get_lineinput_text(self, monkeypatch, capsys):
        """unittest for DialogGui.get_lineinput_text
        """
        tb = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_lineinput_text(tb) == "value from textctrl"
        assert capsys.readouterr().out == "called text.GetValue\n"

    def test_get_checkbox_state(self, monkeypatch, capsys):
        """unittest for DialogGui.get_checkbox_state
        """
        cb = mockwx.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_checkbox_state(cb) == "value from checkbox"
        assert capsys.readouterr().out == "called checkbox.GetValue\n"

    def test_get_combobox_index(self, monkeypatch, capsys):
        """unittest for DialogGui.get_combobox_index
        """
        cmb = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_combobox_index(cmb) == "selection"
        assert capsys.readouterr().out == "called combobox.GetSelection\n"

    def test_get_combobox_itemtext(self, monkeypatch, capsys):
        """unittest for DialogGui.get_combobox_itemtext
        """
        cmb = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_combobox_itemtext(cmb, 'indx') == "strindx"
        assert capsys.readouterr().out == "called combobox.GetString with args ('indx',)\n"

    def test_get_textinput_text(self, monkeypatch, capsys):
        """unittest for DialogGui.get_textinput_text
        """
        tb = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textinput_text(tb) == "value from textctrl"
        assert capsys.readouterr().out == "called text.GetValue\n"

    def test_set_focus_to(self, monkeypatch, capsys):
        """unittest for DialogGui.set_focus_to
        """
        field = mockwx.MockControl()
        assert capsys.readouterr().out == "called Control.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_focus_to(field)
        assert capsys.readouterr().out == ("called Control.SetFocus\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for DialogGui.on_ok
        """
        def mock_confirm():
            print('called DialogParent.confirm')
            return False
        def mock_confirm_2():
            print('called DialogParent.confirm')
            return True
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        assert not testobj.accept('event')
        assert capsys.readouterr().out == "called DialogParent.confirm\n"
        testobj.master = types.SimpleNamespace(confirm=mock_confirm_2)
        assert testobj.accept('event')
        assert capsys.readouterr().out == "called DialogParent.confirm\n"

    def test_refresh(self, monkeypatch, capsys):
        """unittest for DialogGui.refresh
        """
        def mock_fit():
            print('called Dialog.Fit')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.Fit = mock_fit
        testobj.refresh()
        assert capsys.readouterr().out == "called Dialog.Fit\n"
