"""unittests for ./axe/gui_wx.py
"""
from axe import gui_wx as testee


class TestElementDialog:
    """unittest for gui_wx.ElementDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.ElementDialog object

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
        assert capsys.readouterr().out == 'called ElementDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for ElementDialog.__init__
        """
        testobj = testee.ElementDialog(parent, title='',
                  style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
                  item=None)
        assert capsys.readouterr().out == ("")

    def _test_on_ok(self, monkeypatch, capsys):
        """unittest for ElementDialog.on_ok
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_ok(ev) == "expected_result"
        assert capsys.readouterr().out == ("")


class TestAttributeDialog:
    """unittest for gui_wx.AttributeDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.AttributeDialog object

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
        assert capsys.readouterr().out == 'called AttributeDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for AttributeDialog.__init__
        """
        testobj = testee.AttributeDialog(parent, title='',
                  style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
                  item=None)
        assert capsys.readouterr().out == ("")

    def _test_on_ok(self, monkeypatch, capsys):
        """unittest for AttributeDialog.on_ok
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_ok(ev) == "expected_result"
        assert capsys.readouterr().out == ("")


class TestSearchDialog:
    """unittest for gui_wx.SearchDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.SearchDialog object

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
        assert capsys.readouterr().out == 'called SearchDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for SearchDialog.__init__
        """
        testobj = testee.SearchDialog(parent, title='',
                  style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        assert capsys.readouterr().out == ("")

    def _test_set_search(self, monkeypatch, capsys):
        """unittest for SearchDialog.set_search
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_search(evt=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_clear_values(self, monkeypatch, capsys):
        """unittest for SearchDialog.clear_values
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.clear_values(evt=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_ok(self, monkeypatch, capsys):
        """unittest for SearchDialog.on_ok
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_ok(evt=None) == "expected_result"
        assert capsys.readouterr().out == ("")


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

    def _test_on_doubleclick(self, monkeypatch, capsys):
        """unittest for Gui.on_doubleclick
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_doubleclick(ev=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_rightdown(self, monkeypatch, capsys):
        """unittest for Gui.on_rightdown
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_rightdown(ev=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_afsl(self, monkeypatch, capsys):
        """unittest for Gui.afsl
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.afsl(ev=None) == "expected_result"
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
        assert testobj.quit(ev=None) == "expected_result"
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
