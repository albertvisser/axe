"""wxPython versie van een op een treeview gebaseerde XML-editor
"""
import os
import wx
# from .shared import ELSTART, axe_iconame  # , log
HMASK = {"nt": "XML files (*.xml)|*.xml|All files (*.*)|*.*",
         "posix": "XML files (*.xml, *.XML)|*.xml;*.XML|All files (*.*)|*.*"}
IMASK = "All files|*.*"


class Gui(wx.Frame):
    "Main application window"
    def __init__(self, parent=None, fn='', readonly=False):
        self.editor = parent
        self.app = wx.App()
        self.fn = fn
        self.editable = not readonly
        super().__init__(parent=None, pos=(2, 2))  # , size=(620, 900))
        self.Show()

    def go(self):
        "start application event loop"
        self.app.MainLoop()

    # event handlers
    def on_doubleclick(self, ev):
        "event handler for doubleclick on tree item"
        pt = ev.GetPosition()
        item = self.tree.HitTest(pt)[0]
        edit = False
        if item and item != self.top:
            data = self.tree.GetItemText(item)
            edit = True
            if data.startswith(self.parent.elstart) and self.tree.GetChildrenCount(item):
                # als een element node children heeft kan die niet gewijzigd worden?
                edit = False
        if edit:
            self.edit()
        ev.Skip()

    def on_rightdown(self, ev):
        "event handler for right click on tree item"
        pt = ev.GetPosition()
        item = self.tree.HitTest(pt)[0]
        if item and item != self.top:
            self.tree.SelectItem(item)
            menu = self.init_menus(popup=True)
            self.PopupMenu(menu)
            menu.Destroy()

    def afsl(self, ev):
        """handle CLOSE event"""
        test = self.editor.check_tree()
        if not test:
            ev.Veto()
        ev.Skip()

    # helper methods for getting/setting data in visual tree
    def get_node_children(self, node):
        "return descendants of the given node"
        result = []
        tag, c = self.tree.GetFirstChild(node)
        while tag.IsOk():
            result.append(tag)
            tag, c = self.tree.GetNextChild(node, c)
        return result

    def get_node_title(self, node):
        "return the title of the given node"
        return self.tree.GetItemText(node)

    def get_node_data(self, node):
        "return data (element name and text/CDATA) associated with the given node"
        return self.tree.GetItemData(node)  # assuming this is always a 2-tuple

    def get_treetop(self):
        "return the visual tree's root element"
        top = self.tree.GetRootItem()
        return self.tree.GetLastChild(top)

    def setup_new_tree(self, title):
        "build new visual tree and return its root element"
        self.tree.DeleteAllItems()
        # self.undo_stack.clear()
        self.top = self.tree.AddRoot(title)
        return self.top

    def add_node_to_parent(self, parent, pos=-1):
        "add a new descendant to an element at the given position and return it"
        if pos == -1:
            node = self.tree.AppendItem(parent, '')
        else:
            node = self.tree.InsertItem(parent, pos, '')
        return node

    def set_node_title(self, node, title):
        "set the title for the given node"
        self.tree.SetItemText(node, title)

    def get_node_parentpos(self, node):
        "return the parent of the given node and its position under it"
        parent = self.tree.GetItemParent(node)
        pos = 0
        tag, c = self.tree.GetFirstChild(node)
        while tag.IsOk() and tag != node:
            pos += 1
            tag, c = self.tree.GetNextChild(node, c)
        return parent, pos

    def set_node_data(self, node, name, value):
        "set the data (element name, text/CDATA) associated with the given node"
        self.tree.SetItemData(node, (name, value))

    def get_selected_item(self):
        "return the currently selected item"
        return self.tree.GetSelection()

    def set_selected_item(self, item):
        "set the currently selected item to the given item"
        self.tree.SelectItem(item)

    def is_node_root(self, item=None):
        "check if the given element is the visual tree's root and return the result"
        if not item:
            item = self.item
        if self.tree.GetItemData(item) == (self.editor.rt.tag, self.editor.rt.text or ""):
            return True
        return False

    def expand_item(self, item=None):
        "expand a tree item"
        if not item:
            item = self.tree.GetSelection()
        if item:
            self.tree.ExpandAllChildren(item)

    def collapse_item(self, item=None):
        "collapse tree item"
        if not item:
            item = self.tree.GetSelection()
        if item:
            self.tree.CollapseAllChildren(item)

    def edit_item(self, item, oldstate, newstate, command_text):
        "edit an element or attribute"
        # oldstate, newstate and command_text are meant to be used in an undo/redo mechanism
        self.item = item
        # data = self.tree.GetItemText(self.item)  # self.item.get_text()
        # if data.startswith(self.parent.elstart):
        #     tag, text = self.tree.GetItemData(self.item)  # self.item.get_data()
        #     data = {'item': self.item, 'tag': tag}
        #     if text is not None:
        #         data['data'] = True
        #         data['text'] = text
        #     with ElementDialog(self, title='Edit an element', item=data) as edt:
        #         if edt.ShowModal() == wx.ID_SAVE:
        #             h = (self.data["tag"], self.data["text"])
        #             self.tree.SetItemText(self.item, self.editor.getshortname(h))
        #             self.tree.SetItemData(self.item, h)
        #             self.editor.mark_dirty(True)
        # else:
        #     nam, val = self.tree.GetItemData(self.item)  # self.item.get_data()
        #     data = {'item': self.item, 'name': nam, 'value': val}
        #     with AttributeDialog(self, title='Edit an attribute', item=data) as edt:
        #         if edt.ShowModal() == wx.ID_SAVE:
        #             h = (self.data["name"], self.data["value"])
        #             self.tree.SetItemText(self.item, self.editor.getshortname(h, attr=True))
        #             self.tree.SetItemData(self.item, h)
        #             self.editor.mark_dirty(True)
        self.tree.SetItemText(self.item, newstate[0])
        self.tree.SetItemData(self.item, newstate[1:])

    def copy(self, item, cut=False, retain=True):  # retain is t.b.v. delete functie
        """execute cut/delete/copy action"""
        def push_el(el, result):
            "copy element data recursively"
            # print "start: ",result
            text = self.tree.GetItemText(el)
            data = self.tree.GetItemData(el)
            children = []
            # print "before looping over contents:",text,y
            if text.startswith(self.parent.elstart):
                subel, whereami = self.tree.GetFirstChild(el)
                while subel.IsOk():
                    _ = push_el(subel, children)
                    subel, whereami = self.tree.GetNextChild(el, whereami)
            # print "after  looping over contents: ",text,y
            result.append((text, data, children))
            # print "end:  ",result
            return result
        self.item = item
        text = self.tree.GetItemText(self.item)
        data = self.tree.GetItemData(self.item)
        if retain:
            if text.startswith(self.parent.elstart):
                self.cut_el = []
                self.cut_el = push_el(self.item, self.cut_el)
                self.cut_att = None
            else:
                self.cut_el = None
                self.cut_att = data
            self.enable_pasteitems(True)
        if cut:
            prev = self.tree.GetPrevSibling(self.item)
            if not prev.IsOk():
                prev = self.tree.GetItemParent(self.item)
                if prev == self.editor.rt:
                    prev = self.tree.GetNextSibling(self.item)
            self.tree.Delete(self.item)
            self.editor.mark_dirty(True)
            # self.tree.SelectItem(prev)

    def paste(self, item, before=True, below=False):
        """execute paste action"""
        self.item = item
        if self.cut_att:
            item = self.editor.getshortname(self.cut_att, attr=True)
            data = self.cut_att
            if below:
                node = self.tree.AppendItem(self.item, item)
                self.tree.SetItemData(node, data)
            else:
                add_to = self.tree.GetItemParent(self.item)  # self.item.get_parent()
                added = False
                x, c = self.tree.GetFirstChild(add_to)
                for i in range(self.tree.GetChildrenCount(add_to)):
                    if x == self.item:
                        if not before:
                            i += 1
                        node = self.tree.InsertItem(add_to, i, item)
                        self.tree.SetItemData(node, data)
                        added = True
                        break
                    x, c = self.tree.GetNextChild(add_to, c)
                if not added:
                    node = self.tree.AppendItem(add_to, item)
                    self.tree.SetItemData(node, data)
        else:
            def zetzeronder(node, el, pos=-1):
                "add elements recursively"
                if pos == -1:
                    subnode = self.tree.AppendItem(node, el[0])
                    self.tree.SetItemData(subnode, el[1])
                else:
                    subnode = self.tree.InsertItem(node, i, el[0])
                    self.tree.SetItemData(subnode, el[1])
                for x in el[2]:
                    zetzeronder(subnode, x)
            if below:
                node = self.item
                i = -1
            else:
                node = self.tree.GetItemParent(self.item)  # self.item.get_parent()
                x, c = self.tree.GetFirstChild(node)
                cnt = self.tree.GetChildrenCount(node)
                for i in range(cnt):
                    if x == self.item:
                        if not before:
                            i += 1
                        break
                    x, c = self.tree.GetNextChild(node, c)
                if i == cnt:
                    i = -1
            zetzeronder(node, self.cut_el[0], i)
        self.editor.mark_dirty(True)

    def add_attribute(self, item, name, value, command_text):
        "ask for attibute, then start add action"
        # commandtext is provided for use in and undo-redo mechanism
        # self.item = item
        # with AttributeDialog(self, title="New attribute") as edt:
        #     test = edt.ShowModal()
        #     if test == wx.ID_SAVE:
        node = self.editor.add_item(item, name, value, attr=True)
        item = self.tree.GetItemParent(node)
        if not self.tree.IsExpanded(item):
            self.tree.Expand(item)
        #        self.editor.mark_dirty(True)

    def insert(self, item, tag, text, commandtext, before=True, below=False):
        """execute insert action"""
        # commandtext is provided for use in and undo-redo mechanism
        # self.item = item
        # with ElementDialog(self, title="New element") as edt:
        #     if edt.ShowModal() == wx.ID_SAVE:
        node = self.editor.add_item(item, tag, text, before=before, below=below)
        item = self.tree.GetItemParent(node)
        if not self.tree.IsExpanded(item):
            self.tree.Expand(item)
        #         self.editor.mark_dirty(True)

    # internals
    def init_gui(self):
        """Deze methode wordt aangeroepen door de __init__ van de mixin class
        """
        self.icon = wx.Icon(self.editor.iconame, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        self.Bind(wx.EVT_CLOSE, self.afsl)

        # set up statusbar
        self.SetStatusBar(wx.StatusBar(self))
        self.SetStatusText('Ready.')

        # self.init_menus()
        menu_bar = wx.MenuBar()
        filemenu, viewmenu, editmenu, searchmenu = self.init_menus()
        menu_bar.Append(filemenu, "&File")
        menu_bar.Append(viewmenu, "&View")
        if self.editable:
            menu_bar.Append(editmenu, "&Edit")
        menu_bar.Append(searchmenu, "&Search")
        self.SetMenuBar(menu_bar)

        ## self.helpmenu.append('About', callback = self.about)

        self.tree = wx.TreeCtrl(self, size=(820, 808))  # size=(620, 808))
        self.tree.Bind(wx.EVT_LEFT_DCLICK, self.on_doubleclick)
        self.tree.Bind(wx.EVT_RIGHT_DOWN, self.on_rightdown)
        self.tree.Bind(wx.EVT_KEY_UP, self.on_keyup)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.tree, 1, wx.EXPAND)
        vsizer.Add(hsizer, 1, wx.EXPAND)
        self.SetSizer(vsizer)
        self.SetAutoLayout(True)
        vsizer.SetSizeHints(self)
        vsizer.Fit(self)
        self.Layout()
        # self.Show(True)
        self.tree.SetFocus()

        if self.editable:
            self.enable_pasteitems(False)
            self.editor.mark_dirty(False)

    def set_windowtitle(self, text):
        """set screen title
        """
        self.SetTitle(text)

    def get_windowtitle(self):
        """get screen title
        """
        return self.GetTitle()

    def init_menus(self, popup=False):
        """setup application menu"""
        accels = []
        filemenu = wx.Menu()
        viewmenu = wx.Menu()
        if popup:
            editmenu = viewmenu
            searchmenu = editmenu
        else:
            editmenu = wx.Menu() if self.editable else None
            searchmenu = wx.Menu()
        if self.editable:
            disable_menu = not self.cut_el and not self.cut_att

        for ix, menudata in enumerate(self.editor.get_menu_data()):
            for ix2, data in enumerate(menudata):
                text, callback, shortcuts = data
                if shortcuts:
                    shortcuts = shortcuts.split(',')
                    text = '\t'.join((text, shortcuts[0]))
                    shortcuts = shortcuts[1:]
                if ix == 0:
                    # if text.startswith('&Exit'):
                    #     filemenu.AppendSeparator()
                    #     mitem = filemenu.Append(text='&Unlimited Undo', kind=wx.ITEM_CHECK)
                    #     filemenu.AppendSeparator()
                    #     self.setundo_action = mitem
                    mitem = filemenu.Append(-1, text)
                elif ix == 1:
                    mitem = viewmenu.Append(-1, text)
                elif ix == 2 and self.editable:
                    if ix2 == 0:
                        editmenu.AppendSeparator()
                    mitem = editmenu.Append(-1, text)
                    if ix2 == 0:
                        self.undo_item = mitem
                    elif ix2 == 1:
                        self.redo_item = mitem
                        editmenu.AppendSeparator()
                    elif ix2 == 6:
                        self.pastebefore_item = mitem
                        self.pastebefore_text = text
                    elif ix2 == 7:
                        self.pasteafter_item = mitem
                    elif ix2 == 8:
                        self.pasteunder_item = mitem
                        editmenu.AppendSeparator()
                elif (ix == 2 and not self.editable) or ix == 3:
                    if ix2 == 0:
                        searchmenu.AppendSeparator()
                    mitem = searchmenu.Append(-1, text)
                self.Bind(wx.EVT_MENU, callback, mitem)
                if shortcuts:  # voorlopig alleen voor edit en delete
                    for item in shortcuts:
                        accel = wx.AcceleratorEntry(cmd=mitem.GetId())
                        if accel.FromString(item):
                            accels.append(accel)
                self.SetAcceleratorTable(wx.AcceleratorTable(accels))

        if self.editable and disable_menu:
            self.enable_pasteitems(False)

        if popup:
            return searchmenu
        return filemenu, viewmenu, editmenu, searchmenu

    def meldinfo(self, text):
        """notify about some information"""
        wx.MessageBox(text, self.editor.title, wx.OK | wx.ICON_INFORMATION)

    def meldfout(self, text, abort=False):
        """notify about an error"""
        wx.MessageBox(text, self.editor.title, wx.OK | wx.ICON_ERROR)
        if abort:
            self.quit()

    def ask_yesnocancel(self, prompt):
        """stelt een vraag en retourneert het antwoord
        1 = Yes, 0 = No, -1 = Cancel
        """
        retval = dict(zip((wx.YES, wx.NO, wx.CANCEL), (1, 0, -1)))
        h = wx.MessageBox(prompt, self.editor.title, style=wx.YES_NO | wx.CANCEL)
        return retval[h]

    def ask_for_text(self, prompt, value=''):
        """vraagt om tekst en retourneert het antwoord"""
        return wx.GetTextFromUser(prompt, self.editor.title, value)

    def file_to_read(self):
        """ask for file to load"""
        with wx.FileDialog(self, message="Choose a file", defaultDir=os.getcwd(),
                           wildcard=HMASK[os.name], style=wx.FD_OPEN) as dlg:
            ret = dlg.ShowModal()
            ok = ret == wx.ID_OK
            fnaam = dlg.GetPath() if ok else ''
        return ok, fnaam

    def file_to_save(self):  # afwijkende signature
        """ask for file to save"""
        d, f = os.path.split(self.editor.xmlfn)
        with wx.FileDialog(self, message="Save file as ...", defaultDir=d, defaultFile=f,
                           wildcard=HMASK[os.name], style=wx.FD_SAVE) as dlg:
            ret = dlg.ShowModal()
            ok = ret == wx.ID_OK
            name = dlg.GetPath() if ok else ''
        return ok, name

    def enable_pasteitems(self, active=False):
        """activeert of deactiveert de paste-entries in het menu
        afhankelijk van of er iets te pASTEN VALT
        """
        if active:
            self.pastebefore_item.SetItemLabel(self.pastebefore_text)
        else:
            self.pastebefore_item.SetItemLabel("Nothing to Paste")
        self.pastebefore_item.Enable(active)
        self.pasteafter_item.Enable(active)
        self.pasteunder_item.Enable(active)

    def popupmenu(self, item):
        """call up menu"""

    def quit(self, *args):
        "close the application"
        self.Close()

    def on_keyup(self, ev=None):
        "event handler for keyboard"
        ky = ev.GetKeyCode()
        item = self.tree.GetSelection()
        if item and item != self.top:
            if ky == wx.WXK_RETURN:
                if self.tree.ItemHasChildren(item):
                    if self.tree.IsExpanded(item):
                        self.tree.Collapse(item)
                    else:
                        self.tree.Expand(item)
                        item, dummy = self.tree.GetFirstChild(item)
                        self.tree.SelectItem(item)
                else:
                    self.editor.edit()
            elif ky == wx.WXK_BACK:
                if self.tree.IsExpanded(item):
                    self.tree.Collapse(item)
                self.tree.SelectItem(self.tree.GetItemParent(item))
        ev.Skip()

    # def ask_for_search_args(self):
    #     """end dialog to get search argument(s)
    #     """
    #     # self._search_args = []
    #     with SearchDialog(self, title='Search options') as edt:
    #         send = True
    #         while send:
    #             ok = edt.ShowModal()
    #             if ok == wx.ID_OK:
    #                 if self.editor.search_args:
    #                     break
    #             else:
    #                 send = False
    #     print(send)
    #     return send

    def do_undo(self):
        "undo action"

    def do_redo(self):
        "redo action"


def show_dialog(dlg):
    "show a dialog and return confirmation"
    with dlg:
        send = True
        while send:
            ok = dlg.ShowModal()
            send = False
            if ok == wx.ID_OK and not dlg.accept():
                send = True
    return ok == wx.ID_OK


class DialogGui(wx.Dialog):
    """Dialog for editing an element
    """
    def __init__(self, master, parent, title):
        wx.Dialog.__init__(self, parent, title=title,
                           # size=(400, 270), pos=wx.DefaultPosition,
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.SetIcon(parent.icon)
        self.master = master
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.gsizer = wx.GridBagSizer(2, 2)

    def add_label(self, text, row, col, fullwidth=False):
        "add fixed text to grid"
        lbl_name = wx.StaticText(self, label="element name:  ")
        if fullwidth:
            self.gsizer.Add(lbl_name, (row, col), (1, self.gsizer.GetCols()), wx.LEFT | wx.RIGHT, 5)
        else:
            self.gsizer.Add(lbl_name, (row, col), flag=wx.LEFT | wx.RIGHT, border=5)
        return lbl_name

    def add_lineinput(self, row, col, text=None, callback=None):
        "add single line text input widget to grid (over full line)"
        txt = wx.TextCtrl(self, size=(200, -1))
        self.gsizer.Add(txt, (row, col), flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=5)
        if text:
            txt.SetValue(text)
        if callback:
            txt.Bind(wx.EVT_TEXT, callback)
        return txt

    def add_checkbox(self, text, row, col, readonly=False):
        "add checkbox to grid"
        cb = wx.CheckBox(self, label=text)
        self.gsizer.Add(cb, (row, col), flag=wx.ALIGN_CENTER_VERTICAL)  # | wx.LEFT | wx.RIGHT, 5)
        if readonly:
            cb.Enable(False)
        return cb

    def add_combobox(self, items, row, col):
        "add combobox to grid"
        cmb = wx.ComboBox(self, size=(120, -1))
        cmb.AppendItems(items)
        self.gsizer.Add(cmb, (row, col))  # , wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        return cmb

    def add_textinput(self, row, col):
        "add multiline text input widget to grid (over full line)"
        txt = wx.TextCtrl(self, size=(300, 140), style=wx.TE_MULTILINE)
        self.gsizer.Add(txt, (row, col), (1, 2), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
        return txt

    def add_buttons(self, buttondefs):
        "create action buttons"
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        for ix, bdef in enumerate(buttondefs):
            if ix == 0:
                btn = wx.Button(self, id=wx.ID_SAVE)
                btn.Bind(wx.EVT_BUTTON, self.accept)
            elif ix == 1:
                btn = wx.Button(self, id=wx.ID_CANCEL)
            else:
                btn = wx.Button(self, label=bdef[0])
                btn.Bind(wx.EVT_BUTTON, bdef[1])
            hsizer.Add(btn, 0, wx.EXPAND | wx.ALL, 2)
        self.sizer.Add(hsizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 2)
        self.SetAffirmativeId(wx.ID_SAVE)

    def finish_display(self):
        "finalize the layout"
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        self.sizer.Fit(self)
        self.sizer.SetSizeHints(self)
        self.Layout()

    def set_lineinput_text(self, tb, text):
        "set value for input box"
        tb.SetValue(text)

    def set_checkbox_state(self, cb, value):
        "set value for checkbox"
        cb.SetValue(value)

    def set_combobox_index(self, cmb, value):
        "set choice for combobox"
        cmb.SetSelection(value)

    def set_textinput_text(self, tb, text):
        "set value for textbox"
        tb.SetValue(text)

    def get_lineinput_text(self, tb):
        "transmit text input"
        return tb.GetValue()

    def get_checkbox_state(self, cb):
        "transmit state of checkbox"
        return cb.GetValue()

    def get_combobox_index(self, cmb):
        "transmit index of combobox choice"
        return cmb.GetSelection()

    def get_combobox_itemtext(self, cmb, indx):
        "transmit text of combobox choice"
        return cmb.GetString(indx)

    def get_textinput_text(self, tb):
        "transmit textbox input"
        return tb.GetValue()

    def set_focus_to(self, field):
        "redirect input to error field"
        field.SetFocus()

    def accept(self, *args):
        """final checks, send changed data to parent"""
        return self.master.confirm()

    def reject(self, *args):
        "needed for reference"

    def refresh(self):
        "adjust window size after clearing label text (hopefully)"
        self.Fit()
