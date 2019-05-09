# -*- coding: utf-8 -*-
"""wxPython versie van een op een treeview gebaseerde XML-editor
moet nog verder gestript net zoals dat bij de qt versie gedaan is
"""
## import logging
## logging.basicConfig(filename='axe_wx.log', level=logging.DEBUG,
    ## format='%(asctime)s %(message)s')
import os
import sys
import wx
from .axe_base import getshortname, XMLTree, AxeMixin
from .axe_base import ELSTART, TITEL, axe_iconame
TITEL = TITEL.replace('editor', 'viewer')
if os.name == "nt":
    HMASK = "XML files (*.xml)|*.xml|All files (*.*)|*.*"
elif os.name == "posix":
    HMASK = "XML files (*.xml, *.XML)|*.xml;*.XML|All files (*.*)|*.*"
IMASK = "All files|*.*"


def calculate_location(win, node):              # FIXME: qt -> wx
    """attempt to calculate some kind of identification for a tree node

    this function returns a tuple of subsequent indices of a child under its parent.
    possibly this can be used in the replacements dictionary
    """
    id_ = []
    while node != win.top:
        idx = node.parent().indexOfChild(node)
        id_.insert(0, idx)
        node = node.parent()
    return tuple(id_)


def flatten_tree(element):                      # FIXME: qt -> wx
    """return the tree's structure as a flat list
    probably nicer as a generator function
    """
    itemdict = element.data(0, core.Qt.UserRole)
    if itemdict:
        elem_list = [(element, itemdict['tag'], itemdict['text'] or '', itemdict['attrs'])]
    else:
        elem_list = [(element, '', '', [])]
    subel_list = []
    for seq in range(element.childCount()):
        subitem = element.child(seq)
        subel_list = flatten_tree(subitem)
        elem_list.extend(subel_list)
    return elem_list


class SearchDialog(wx.Dialog):
    """Dialog to get search arguments
    """
    def __init__(self, parent, title=""):
        super().__init__(parent, title=title)
        self._parent = parent

        self.cb_element = wx.StaticText(self, 'Element')
        lbl_element = wx.StaticText(self, "name:")
        self.txt_element = wx.TextEdit(self)
        self.txt_element.Bind(wx.EVT_TEXT, self.set_search)

        self.cb_attr = wx.StaticText(self, 'Attribute')
        lbl_attr_name = wx.StaticText(self, "name:")
        self.txt_attr_name = wx.TextEdit(self)
        self.txt_attr_name.Bind(wx.EVT_TEXT, self.set_search)
        lbl_attr_val = wx.StaticText(self, "value:")
        self.txt_attr_val = wx.TextEdit(self)
        self.txt_attr_val.Bind(wx.EVT_TEXT, self.set_search)

        self.cb_text = wx.StaticText(self, 'Text')
        lbl_text = wx.StaticText(self, "value:")
        self.txt_text = wx.TextEdit(self)
        self.txt_text.Bind(wx.EVT_TEXT, self.set_search)

        self.lbl_search = qtw.QLabel('')

        self.btn_ok = wx.Button(self, id=wx.ID_OK)
        # self.btn_ok.clicked.connect(self.accept)
        # self.btn_ok.setDefault(True)
        self.btn_cancel = qtw.QPushButton(self, id=wx.ID_CANCEL)
        # self.btn_cancel.clicked.connect(self.reject)

        # sizer0 = wx.BoxSizer(wx.VERTICAL)
        # sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        # sizer1.Add(self.tree, 1, wx.EXPAND)
        # sizer0.Add(sizer1, 1, wx.EXPAND)
        sizer = wx.BoxSizer(wx.VERTICAL)

        gsizer = wx.GridBagSizer(4, 4)

        gsizer.Add(self.cb_element, (0, 0))
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(lbl_element)
        hsizer.Add(self.txt_element)
        vsizer.Add(hsizer)
        gsizer.Add(vsizer, (0, 1))

        vsizer = wx.BoxSizer(wx.VERTICAL)
        # vsizer.addSpacing(5)
        vsizer.Add(self.cb_attr)
        # vsizer.addStretch()
        gsizer.Add(vsizer, (1, 0))
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(lbl_attr_name)
        hsizer.Add(self.txt_attr_name)
        vsizer.Add(hsizer)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(lbl_attr_val)
        hsizer.Add(self.txt_attr_val)
        vsizer.Add(hsizer)
        gsizer.Add(vsizer, (1, 1))

        gsizer.Add(self.cb_text, (2, 0))
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(lbl_text)
        hsizer.Add(self.txt_text)
        gsizer.Add(hsizer, (2, 1))
        sizer.Add(gsizer)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.lbl_search)
        sizer.Add(hsizer)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        # hsizer.addStretch()
        hsizer.Add(self.btn_ok)
        hsizer.Add(self.btn_cancel)
        # hsizer.addStretch()
        sizer.Add(hsizer)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self.pnl)
        sizer.SetSizeHints(self.pnl)
        self.Layout()
        self.Show(True)

    def set_search(self):
        """build text describing search action"""
        out = ''
        ele = self.txt_element.GetValue()
        attr_name = self.txt_attr_name.GetValue()
        attr_val = self.txt_attr_val.GetValue()
        GetValue = self.txt_text.text()
        attr = ''
        if ele:
            ele = ' an element named `{}`'.format(ele)
        if attr_name or attr_val:
            attr = ' an attribute'
            if attr_name:
                attr += ' named `{}`'.format(attr_name)
            if attr_val:
                attr += ' that has value `{}`'.format(attr_val)
            if ele:
                attr = ' with' + attr
        if text:
            out = 'search for text'
            if ele:
                out += ' under' + ele
            elif attr:
                out += ' under an element with'
            if attr:
                out += attr
        elif ele:
            out = 'search for' + ele
            if attr:
                out += attr
        elif attr:
            out = 'search for' + attr
        self.lbl_search.SetValue(out)

    def accept(self):
        """confirm dialog and pass changed data to parent"""
        ele = str(self.txt_element.text())
        attr_name = str(self.txt_attr_name.text())
        attr_val = str(self.txt_attr_val.text())
        text = str(self.txt_text.text())
        if not any((ele, attr_name, attr_val, text)):
            self._parent._meldfout('Please enter search criteria or press cancel')
            self.txt_element.setFocus()
            return

        self._parent.search_args = (ele, attr_name, attr_val, text)
        super().accept()


class MainFrame(wx.Frame, AxeMixin):
    "Main application window"
    def __init__(self, parent, id, fn=''):
        self.parent = parent
        self.id = id
        self.fn = fn
        AxeMixin.__init__(self)

    # event handlers
    def on_doubleclick(self, ev=None):
        "event handler for doubleclick on tree item"
        pt = ev.GetPosition()
        item, flags = self.tree.HitTest(pt)
        if item:
            if item == self.top:
                edit = False
            else:
                data = self.tree.GetItemText(item)
                edit = True
                if data.startswith(ELSTART):
                    if self.tree.GetChildrenCount(item):
                        edit = False
        if edit:
            self.edit()
        ev.Skip()

    def on_rightdown(self, ev=None):
        "event handler for right click on tree item"
        pt = ev.GetPosition()
        item, flags = self.tree.HitTest(pt)
        if item and item != self.top:
            self.tree.SelectItem(item)
            menu = self._init_menus(popup=True)
            self.PopupMenu(menu)
            ## print "klaar met menu"
            menu.Destroy()
        ## pass

    def on_keyup(self, ev=None):
        "event handler for keyboard"
        ky = ev.GetKeyCode()
        if ev.GetModifiers() == wx.MOD_CONTROL:
            if ky == ord('O'):
                self.openxml()
            elif ky == ord('Q'):
                self.quit()
        item = self.tree.Selection
        # if ky == ord('F'):
        # elif ky == wx.WXK_F3:
        ev.Skip()

    def afsl(self, ev=None):
        """handle CLOSE event"""
        ev.Skip()

    # reimplemented methods from Mixin
    # mostly because of including the gui event in the signature
    def openxml(self, ev=None):
        AxeMixin.openxml(self, skip_check=True)

    def init_tree(self, root, prefixes=None, uris=None, name=''):
        "set up display tree"
        def add_to_tree(el, rt):
            "recursively add elements"
            h = (el.tag, el.text)
            rr = self.tree.AppendItem(rt, getshortname((h, prefixes, uris)))
            self.tree.SetItemData(rr, h)
            for attr in el.keys():
                h = el.get(attr)
                if not h:
                    h = '""'
                h = (attr, h)
                rrr = self.tree.AppendItem(rr, getshortname((h, prefixes, uris), attr=True))
                self.tree.SetItemData(rrr, h)
            for subel in list(el):
                add_to_tree(subel, rr)

        self.tree.DeleteAllItems()
        titel = AxeMixin.init_tree(self, root, prefixes, uris, name)
        self.top = self.tree.AddRoot(titel)
        self.SetTitle(" - ".join((os.path.basename(titel), TITEL)))

        h = (self.rt.tag, self.rt.text)
        rt = self.tree.AppendItem(self.top, getshortname((h, prefixes, uris)))
        self.tree.SetItemData(rt, h)
        for el in list(self.rt):
            add_to_tree(el, rt)
        # self.tree.selection = self.top
        # set_selection()

    # internals
    def _init_gui(self):
        """Deze methode wordt aangeroepen door de __init__ van de mixin class
        """
        wx.Frame.__init__(self, self.parent, self.id, pos=(2, 2), size=(620, 900))
        self.SetIcon(wx.Icon(axe_iconame, wx.BITMAP_TYPE_ICO))
        self.Bind(wx.EVT_CLOSE, self.afsl)

        self._init_menus()
        menuBar = wx.MenuBar()
        filemenu, viewmenu, editmenu = self._init_menus()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(viewmenu, "&View")
        menuBar.Append(editmenu, "&Edit")
        self.SetMenuBar(menuBar)

        self.pnl = wx.Panel(self, -1)
        self.tree = wx.TreeCtrl(self.pnl, -1)
        self.tree.Bind(wx.EVT_LEFT_DCLICK, self.on_doubleclick)
        self.tree.Bind(wx.EVT_RIGHT_DOWN, self.on_rightdown)
        self.tree.Bind(wx.EVT_KEY_UP, self.on_keyup)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.tree, 1, wx.EXPAND)
        sizer0.Add(sizer1, 1, wx.EXPAND)
        self.pnl.SetSizer(sizer0)
        self.pnl.SetAutoLayout(True)
        sizer0.Fit(self.pnl)
        sizer0.SetSizeHints(self.pnl)
        self.pnl.Layout()
        self.Show(True)
        self.tree.SetFocus()

    def _init_menus(self, popup=False):
        """setup application menu"""
        # accels = []
        if popup:
            viewmenu = wx.Menu()
        else:
            filemenu = wx.Menu()
            mitem = wx.MenuItem(filemenu, -1, "&Open")
            self.Bind(wx.EVT_MENU, self.openxml, mitem)
            filemenu.Append(mitem)
            mitem = wx.MenuItem(filemenu, -1, 'E&xit')
            self.Bind(wx.EVT_MENU, self.quit, mitem)
            filemenu.Append(mitem)
            # accels.append(wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('Q'), 0, mitem))
            viewmenu = wx.Menu()

        mitem = wx.MenuItem(viewmenu, -1, "&Expand All (sub)Levels")
        self.Bind(wx.EVT_MENU, self.expand, mitem)
        viewmenu.Append(mitem)
        mitem = wx.MenuItem(viewmenu, -1, "&Collapse All (sub)Levels")
        self.Bind(wx.EVT_MENU, self.collapse, mitem)
        viewmenu.Append(mitem)

        if popup:
            searchmenu = viewmenu
            searchmenu.AppendSeparator()
        else:
            searchmenu = wx.Menu()

        mitem = wx.MenuItem(searchmenu, -1, "&Find")
        self.Bind(wx.EVT_MENU, self.search, mitem)
        searchmenu.Append(mitem)
        mitem = wx.MenuItem(searchmenu, -1, "Find &Last")
        self.Bind(wx.EVT_MENU, self.search_last, mitem)
        searchmenu.Append(mitem)
        mitem = wx.MenuItem(searchmenu, -1, "Find &Next")
        self.Bind(wx.EVT_MENU, self.search_next, mitem)
        searchmenu.Append(mitem)
        mitem = wx.MenuItem(searchmenu, -1, "Find &Previous")
        self.Bind(wx.EVT_MENU, self.search_prev, mitem)
        searchmenu.Append(mitem)
        # accel = wx.AcceleratorTable(accels)
        # self.SetAcceleratorTable(accel)
        if popup:
            return searchmenu
        return filemenu, viewmenu, searchmenu

    def _meldinfo(self, text):
        """notify about some information"""
        wx.MessageBox(text, self.title, wx.OK | wx.ICON_INFORMATION)

    def _meldfout(self, text, abort=False):
        """notify about an error"""
        wx.MessageBox(text, self.title, wx.OK | wx.ICON_ERROR)
        if abort:
            self.quit()

    def _ask_yesnocancel(self, prompt):
        """stelt een vraag en retourneert het antwoord
        1 = Yes, 0 = No, -1 = Cancel
        """
        # retval = dict(zip((wx.YES, wx.NO, wx.CANCEL), (1, 0, -1)))
        h = wx.MessageBox(prompt, self.title, style=wx.YES_NO | wx.CANCEL)
        return h

    def _ask_for_text(self, prompt):
        """vraagt om tekst en retourneert het antwoord"""
        return wx.GetTextFromUser(prompt, self.title)

    def _file_to_read(self):
        """ask for file to load"""
        dlg = wx.FileDialog(self, message="Choose a file",
                            defaultDir=os.getcwd(), wildcard=HMASK, style=wx.FD_OPEN)
        ret = dlg.ShowModal()
        ok = (ret == wx.ID_OK)
        fnaam = dlg.GetPath() if ok else ''
        dlg.Destroy()
        return ok, fnaam

    def _checkselection(self):
        """get the currently selected item

        if there is no selection or the file title is selected, display a message
        (if requested). Also return False in that case
        """
        sel = True
        self.item = self.tree.Selection
        if self.item is None or self.item == self.top:
            wx.MessageBox('You need to select an element or attribute first',
                          self.title, wx.OK | wx.ICON_INFORMATION)
            sel = False
        return sel

    # exposed menu handlers
    def quit(self, ev=None):
        "close the application"
        self.Close()

    def expand(self, ev=None):
        "expand a tree item"
        item = self.tree.Selection
        if item:
            self.tree.ExpandAllChildren(item)

    def collapse(self, ev=None):
        "collapse tree item"
        item = self.tree.Selection
        if item:
            self.tree.CollapseAllChildren(item)

    def search(self, reverse=False):
        "start search after asking for options"
        self._search_pos = None
        with SearchDialog(self, title='Search options') as edt:
            if edt == wx.ID_OK:
                self.search_next(reverse)
                ## found, is_attr = find_next(flatten_tree(self.top), self.search_args,
                    ## reversed) # self.tree.top.child(0)
                ## if found:
                    ## self.tree.setCurrentItem(found)
                    ## self._search_pos = (found, is_attr)

    def search_last(self):
        "start backwards search"
        self.search(reverse=True)

    def search_next(self, reverse=False):
        "find (default is forward)"
        found, is_attr = find_next(flatten_tree(self.top), self.search_args,
                                   reverse, self._search_pos)  # self.tree.top.child(0)
        if found:
            # self.tree.setCurrentItem(found)
            self._search_pos = (found, is_attr)
        else:
            self._meldinfo('Niks (meer) gevonden')

    def search_prev(self):
        "find backwards"
        self.search_next(reverse=True)



def axe_gui(args):
    "start up the editor"
    app = wx.App(redirect=False)  # True, filename="/home/albert/xmledit/axe/axe_wx.log")
    print("----")
    if len(args) > 1:
        frm = MainFrame(None, -1, fn=" ".join(args[1:]))
    else:
        frm = MainFrame(None, -1)
    app.MainLoop()


if __name__ == "__main__":
    axe_gui(sys.argv)
