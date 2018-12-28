# -*- coding: utf-8 -*-
"""wxPython versie van een op een treeview gebaseerde XML-editor
"""
## import logging
## logging.basicConfig(filename='axe_wx.log', level=logging.DEBUG,
    ## format='%(asctime)s %(message)s')
import os
import sys
import wx
from .axe_base import getshortname, XMLTree, AxeMixin
from .axe_base import ELSTART, TITEL, axe_iconame
if os.name == "nt":
    HMASK = "XML files (*.xml)|*.xml|All files (*.*)|*.*"
elif os.name == "posix":
    HMASK = "XML files (*.xml, *.XML)|*.xml;*.XML|All files (*.*)|*.*"
IMASK = "All files|*.*"


class ElementDialog(wx.Dialog):
    """Dialog for editing an element
    """
    def __init__(self, parent, title='',  # size=(400, 270), pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
                 item=None):
        # wx.Dialog.__init__(self, parent, -1, title=title, pos=pos, size=size, style=style)
        wx.Dialog.__init__(self, parent, -1, title=title, style=style)
        self._parent = parent
        self.pnl = wx.Panel(self, -1)
        lbl_name = wx.StaticText(self.pnl, -1, "element name:  ")
        self.txt_tag = wx.TextCtrl(self.pnl, -1, size=(200, -1))
        self.txt_tag.Bind(wx.EVT_KEY_UP, self.on_keyup)
        self.cb = wx.CheckBox(self.pnl, -1, label='Bevat data:')
        ## lbl_data = wx.StaticText(self.pnl, -1, "text data:")
        self.txt_data = wx.TextCtrl(self.pnl, -1, size=(300, 140), style=wx.TE_MULTILINE)
        self.txt_data.Bind(wx.EVT_KEY_UP, self.on_keyup)
        self.btn_ok = wx.Button(self.pnl, id=wx.ID_SAVE)
        self.btn_ok.Bind(wx.EVT_BUTTON, self.on_ok)
        self.btn_cancel = wx.Button(self.pnl, id=wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_SAVE)

        tag = txt = ''
        if item:
            tag = item["tag"]
            if "text" in item:
                self.cb.SetValue(True)
                txt = item["text"]
        self.txt_tag.SetValue(tag)
        self.txt_data.SetValue(txt)

        sizer = wx.BoxSizer(wx.VERTICAL)
        ## hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer2.Add(lbl_name, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
        hsizer2.Add(self.txt_tag, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        ## hsizer.Add(hsizer2, 0, wx.EXPAND | wx.ALL, 5)
        ## sizer.Add(hsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP,  5)
        sizer.Add(hsizer2, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 5)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(self.cb, 0, wx.ALIGN_CENTER_HORIZONTAL)  # ,wx.TOP, 3)
        vsizer.Add(self.txt_data, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)
        hsizer.Add(vsizer, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(hsizer, 1, wx.EXPAND | wx.ALL, 5)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.btn_ok, 0, wx.EXPAND | wx.ALL, 2)
        hsizer.Add(self.btn_cancel, 0, wx.EXPAND | wx.ALL, 2)
        sizer.Add(hsizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 2)

        self.pnl.SetSizer(sizer)
        self.pnl.SetAutoLayout(True)
        sizer.Fit(self.pnl)
        sizer.SetSizeHints(self.pnl)
        self.pnl.Layout()
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.pnl, 0, wx.EXPAND | wx.ALL)
        vbox.Add(hbox, 0, wx.EXPAND | wx.ALL)
        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        vbox.Fit(self)
        vbox.SetSizeHints(self)

        self.txt_tag.SetFocus()

    def on_cancel(self, ev):
        "dismiss dialog"
        self.end('cancel')

    def on_ok(self, ev):
        """final checks, send changed data to parent"""
        self._parent.data = {}
        tag = self.txt_tag.GetValue()
        if tag == '' or len(tag.split()) > 1:
            wx.MessageBox('Element name cannot be empty or contain spaces',
                          self._parent.title, wx.OK | wx.ICON_ERROR)
            return
        self._parent.data["tag"] = tag
        self._parent.data["data"] = self.cb.IsChecked()
        self._parent.data["text"] = self.txt_data.GetValue()
        ev.Skip()
        ## self.end('ok')

    def on_keyup(self, ev):
        """event handler to make "select all" possible"""
        ky = ev.GetKeyCode()
        mod = ev.GetModifiers()
        if ky == 65 and mod == wx.MOD_CONTROL:
            win = ev.GetEventObject()
            if win in (self.txt_tag, self.txt_data):
                win.SelectAll()


class AttributeDialog(wx.Dialog):
    """Dialog for editing an attribute"""
    def __init__(self, parent, title='',  # size=(320, 160), pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
                 item=None):
        # wx.Dialog.__init__(self, parent, -1, title=title, pos=pos, size=size, style=style)
        wx.Dialog.__init__(self, parent, -1, title=title, style=style)
        self._parent = parent
        self.pnl = wx.Panel(self, -1)
        lbl_name = wx.StaticText(self.pnl, -1, "Attribute name:")
        self.txt_name = wx.TextCtrl(self.pnl, -1, size=(180, -1))
        self.txt_name.Bind(wx.EVT_KEY_UP, self.on_keyup)
        lbl_value = wx.StaticText(self.pnl, -1, "Attribute value:")
        self.txt_value = wx.TextCtrl(self.pnl, -1, size=(180, -1))
        self.txt_value.Bind(wx.EVT_KEY_UP, self.on_keyup)
        self.btn_ok = wx.Button(self.pnl, id=wx.ID_SAVE)
        self.btn_ok.Bind(wx.EVT_BUTTON, self.on_ok)
        self.btn_cancel = wx.Button(self.pnl, id=wx.ID_CANCEL)
        ## self.btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        self.SetAffirmativeId(wx.ID_SAVE)

        nam = val = ''
        if item:
            nam, val = item["name"], item["value"]
        self.txt_name.SetValue(nam)
        self.txt_value.SetValue(val)

        sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(lbl_name, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
        hsizer.Add(self.txt_name, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        sizer.Add(hsizer, 0, wx.EXPAND | wx.ALL, 5)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(lbl_value, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
        hsizer.Add(self.txt_value, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        sizer.Add(hsizer, 0, wx.EXPAND | wx.ALL, 5)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.btn_ok, 0, wx.EXPAND | wx.ALL, 2)
        hsizer.Add(self.btn_cancel, 0, wx.EXPAND | wx.ALL, 2)
        sizer.Add(hsizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 2)

        self.pnl.SetSizer(sizer)
        self.pnl.SetAutoLayout(True)
        sizer.Fit(self.pnl)
        sizer.SetSizeHints(self.pnl)
        self.pnl.Layout()
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.pnl, 0, wx.EXPAND | wx.ALL)
        vbox.Add(hbox, 0, wx.EXPAND | wx.ALL)
        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        vbox.Fit(self)
        vbox.SetSizeHints(self)
        self.txt_name.SetFocus()

    def on_ok(self, ev):
        """final checks, transmit changes to parent"""
        self._parent.data = {}
        nam = self.txt_name.GetValue()
        if nam == '':
            wx.MessageBox('Attribute name cannot be empty or spaces', self._parent.title,
                          wx.OK | wx.ICON_ERROR)
            return
        self._parent.data["name"] = nam
        self._parent.data["value"] = self.txt_value.GetValue()
        ## self.end('ok')
        ev.Skip()

    def on_cancel(self, ev):
        "dismiss dialog"
        self.end('cancel')

    def on_keyup(self, ev):
        """event handler to make "select all" possible"""
        ky = ev.GetKeyCode()
        mod = ev.GetModifiers()
        if ky == 65 and mod == wx.MOD_CONTROL:
            win = ev.GetEventObject()
            if win in (self.txt_name, self.txt_value):
                win.SelectAll()


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
            if ky == ord('N'):
                self.newxml()
            elif ky == ord('O'):
                self.openxml()
            elif ky == ord('S'):
                self.savexml()
            elif ky == ord('Q'):
                self.quit()
        elif ev.GetModifiers() == wx.MOD_CONTROL | wx.MOD_SHIFT:
            if ky == ord('S'):
                self.savexmlas()
        item = self.tree.Selection
        if item and item != self.top:
            if ky == wx.WXK_DELETE:
                self.delete()
            elif ky == wx.WXK_F2:
                self.edit()
            elif ky == wx.WXK_RETURN:
                if self.tree.ItemHasChildren(item):
                    if self.tree.IsExpanded(item):
                        self.tree.Collapse(item)
                    else:
                        self.tree.Expand(item)
                        item, dummy = self.tree.GetFirstChild(item)
                        self.tree.SelectItem(item)
                else:
                    self.edit()
            elif ky == wx.WXK_BACK:
                if self.tree.IsExpanded(item):
                    self.tree.Collapse(item)
                self.tree.SelectItem(self.tree.GetItemParent(item))
        ev.Skip()

    def afsl(self, ev=None):
        """handle CLOSE event"""
        if self.check_tree():
            ev.Skip()
        ev.Veto()

    # reimplemented methods from Mixin
    def mark_dirty(self, state):
        """past gewijzigd-status aan
        en stelt de overeenkomstig gewijzigde tekst voor de titel in
        """
        data = AxeMixin.mark_dirty(self, state, self.GetTitle())
        if data:
            self.SetTitle(data)

    def newxml(self, ev=None):
        "reimplemented from mixin to swallow menu event"
        AxeMixin.newxml(self)
        print("self.newxml aangeroepen")

    def openxml(self, ev=None):
        "reimplemented from mixin to swallow menu event"
        AxeMixin.openxml(self)

    def savexml(self, ev=None):
        "reimplemented from mixin to swallow menu event"
        AxeMixin.savexml(self)

    def savexmlas(self, ev=None):
        """save as and notify of result"""
        ok = AxeMixin.savexmlas(self)
        if ok:
            self.tree.SetItemText(self.top, self.xmlfn)
            ## self.SetTitle(" - ".join((os.path.basename(self.xmlfn), TITEL)))
            self.mark_dirty(False)

    def savexmlfile(self, oldfile=''):      # writexml
        "(re)write tree to XML file"
        def expandnode(rt, root, tree):
            "recursively expand node"
            tag, c = self.tree.GetFirstChild(rt)
            while tag.IsOk():
                text = self.tree.GetItemText(tag)
                data = self.tree.GetItemData(tag)
                node = tree.expand(root, text, data)
                if node is not None:
                    expandnode(tag, node, tree)
                tag, c = self.tree.GetNextChild(rt, c)
        AxeMixin.savexmlfile(self, oldfile)
        top = self.tree.GetRootItem()
        rt = self.tree.GetLastChild(top)
        text = self.tree.GetItemText(rt)
        data = self.tree.GetItemData(rt)
        tree = XMLTree(data[0])  # .split(None,1)
        root = tree.root
        expandnode(rt, root, tree)
        h = tree.write(self.xmlfn)
        self.mark_dirty(False)

    def about(self, ev=None):
        "reimplemented from mixin to swallow menu event"
        AxeMixin.about(self)

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
        self.mark_dirty(False)

    def cut(self, ev=None):
        "reimplemented from mixin to swallow menu event"
        AxeMixin.cut(self)

    def delete(self, ev=None):
        "reimplemented from mixin to swallow menu event"
        AxeMixin.delete(self)

    def copy(self, ev=None, cut=False, retain=True):  # retain is t.b.v. delete functie
        """execute cut/delete/copy action"""
        def push_el(el, result):
            "copy element data recursively"
            # print "start: ",result
            text = self.tree.GetItemText(el)
            data = self.tree.GetItemData(el)
            children = []
            # print "before looping over contents:",text,y
            if text.startswith(ELSTART):
                subel, whereami = self.tree.GetFirstChild(el)
                while subel.IsOk():
                    temp = push_el(subel, children)
                    subel, whereami = self.tree.GetNextChild(el, whereami)
            # print "after  looping over contents: ",text,y
            result.append((text, data, children))
            # print "end:  ",result
            return result
        if not self._checkselection():
            return
        text = self.tree.GetItemText(self.item)
        data = self.tree.GetItemData(self.item)
        txt = AxeMixin.copy(self, cut, retain)
        if data == (self.rt.tag, self.rt.text):
            wx.MessageBox("Can't %s the root" % txt, self.title, wx.OK | wx.ICON_ERROR)
            return
        ## print "copy(): print text,data"
        ## print text,data
        if retain:
            if text.startswith(ELSTART):
                ## self.cut_el = self.item # hmmm... hier moet de aanroep van push_el komen
                self.cut_el = []
                self.cut_el = push_el(self.item, self.cut_el)
                self.cut_att = None
            else:
                self.cut_el = None
                self.cut_att = data
            self._enable_pasteitems(True)
        if cut:
            prev = self.tree.GetPrevSibling(self.item)
            if not prev.IsOk():
                prev = self.tree.GetItemParent(self.item)
                if prev == self.rt:
                    prev = self.tree.GetNextSibling(self.item)
            self.tree.Delete(self.item)
            self.mark_dirty(True)
            self.tree.SelectItem(prev)

    def paste_after(self, ev=None):
        "reimplemented from mixin to swallow menu event"
        AxeMixin.paste_after(self)

    def paste_under(self, ev=None):
        "reimplemented from mixin to swallow menu event"
        AxeMixin.paste_under(self)

    def paste(self, ev=None, before=True, pastebelow=False):
        """execute paste action"""
        if not self._checkselection():
            return
        data = self.tree.GetItemData(self.item)
        if pastebelow and not self.tree.GetItemText(self.item).startswith(ELSTART):
            wx.MessageBox("Can't paste below an attribute", self.title, wx.OK | wx.ICON_ERROR)
            return
        if data == self.rt:
            if before:
                wx.MessageBox("Can't paste before the root",
                              self.title, wx.OK | wx.ICON_ERROR)
                return
            else:
                wx.MessageBox("Pasting as first element below root",
                              self.title, wx.OK | wx.ICON_INFORMATION)
                pastebelow = True
        ## if self.cut:
            ## self._enable_pasteitems(False)
        print("paste(): print self.cut_el, self.cut_att")
        print(self.cut_el, self.cut_att)
        if self.cut_att:
            item = getshortname(self.cut_att, attr=True)
            data = self.cut_att
            if pastebelow:
                node = self.tree.AppendItem(self.item, item)
                self.tree.SetItemPyData(node, data)
            else:
                add_to = self.tree.GetItemParent(self.item)  # self.item.get_parent()
                added = False
                x, c = self.tree.GetFirstChild(add_to)
                for i in range(self.tree.GetChildrenCount(add_to)):
                    if x == self.item:
                        if not before:
                            i += 1
                        node = self.tree.InsertItemBefore(add_to, i, item)
                        self.tree.SetItemPyData(node, data)
                        added = True
                        break
                    x, c = self.tree.GetNextChild(add_to, c)
                if not added:
                    node = self.tree.AppendItem(add_to, item)
                    self.tree.SetItemPyData(node, data)
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
            if pastebelow:
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
        self.mark_dirty(True)

    def insert_after(self, ev=None):
        "reimplemented from mixin to swallow menu event"
        AxeMixin.insert_after(self)

    def insert_child(self, ev=None):
        "reimplemented from mixin to swallow menu event"
        AxeMixin.insert_child(self)

    def insert(self, ev=None, before=True, below=False):
        """execute insert action"""
        if not self._checkselection():
            return
        edt = ElementDialog(self, title="New element")
        if edt.ShowModal() == wx.ID_SAVE:
            data = self.data['tag'], self.data['text']
            text = getshortname((data, [], []))
            if below:
                rt = self.tree.AppendItem(self.item, text)
                self.tree.SetItemData(rt, data)
            else:
                parent = self.tree.GetItemParent(self.item)
                if before:
                    item = self.tree.GetPrevSibling(self.item)
                else:
                    item = self.item
                node = self.tree.InsertItem(parent, item, text)
                self.tree.SetItemData(node, data)
            self.mark_dirty(True)
        edt.Destroy()

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

        self._enable_pasteitems(False)
        ## self.helpmenu.append('About', callback = self.about)

        self.pnl = wx.Panel(self, -1)
        self.tree = wx.TreeCtrl(self.pnl, -1)        self.tree.Bind(wx.EVT_LEFT_DCLICK, self.on_doubleclick)
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

        self.mark_dirty(False)

    def _init_menus(self, popup=False):
        """setup application menu"""
        # accels = []
        if popup:
            viewmenu = wx.Menu()
        else:
            filemenu = wx.Menu()
            mitem = wx.MenuItem(filemenu, -1, "&New")
            self.Bind(wx.EVT_MENU, self.newxml, mitem)
            filemenu.Append(mitem)
            # accels.append(wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('N'), 0, mitem))
            mitem = wx.MenuItem(filemenu, -1, "&Open")
            self.Bind(wx.EVT_MENU, self.openxml, mitem)
            filemenu.Append(mitem)
            # accels.append(wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('O'), 0, mitem))
            mitem = wx.MenuItem(filemenu, -1, '&Save')
            self.Bind(wx.EVT_MENU, self.savexml, mitem)
            filemenu.Append(mitem)
            # accels.append(wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('S'), 0, mitem))
            mitem = wx.MenuItem(filemenu, -1, 'Save &As')
            self.Bind(wx.EVT_MENU, self.savexmlas, mitem)
            filemenu.Append(mitem)
            # accels.append(wx.AcceleratorEntry(wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord('S'),
            #                                   0, mitem))
            filemenu.AppendSeparator()
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
            editmenu = viewmenu
            editmenu.AppendSeparator()
        else:
            editmenu = wx.Menu()

        mitem = wx.MenuItem(editmenu, -1, "&Edit")
        self.Bind(wx.EVT_MENU, self.edit, mitem)
        editmenu.Append(mitem)
        editmenu.AppendSeparator()
        mitem = wx.MenuItem(editmenu, -1, "&Delete")
        self.Bind(wx.EVT_MENU, self.delete, mitem)
        editmenu.Append(mitem)
        mitem = wx.MenuItem(editmenu, -1, "C&ut")
        self.Bind(wx.EVT_MENU, self.cut, mitem)
        editmenu.Append(mitem)
        mitem = wx.MenuItem(editmenu, -1, "&Copy")
        self.Bind(wx.EVT_MENU, self.copy, mitem)
        editmenu.Append(mitem)
        mitem = wx.MenuItem(editmenu, -1, "Paste Before")
        self.Bind(wx.EVT_MENU, self.paste, mitem)
        disable_menu = True if not self.cut_el and not self.cut_att else False
        ## add_menuitem = True if not popup or not disable_menu else False
        ## if add_menuitem:
            ## editmenu.Append(mitem)
        ## else:
            ## viewmenu.Append(mitem)
        editmenu.Append(mitem)
        if disable_menu:
            mitem.SetItemLabel("Nothing to Paste")
            mitem.Enable(False)
        if not popup:
            self.pastebefore_item = mitem
        mitem = wx.MenuItem(editmenu, -1, "Paste After")
        self.Bind(wx.EVT_MENU, self.paste_after, mitem)
        ## if add_menuitem:
            ## editmenu.Append(mitem)
        ## else:
            ## viewmenu.Append(mitem)
        editmenu.Append(mitem)
        if disable_menu:
            ## mitem.SetItemLabel(" ")
            mitem.Enable(False)
        if not popup:
            self.pasteafter_item = mitem
        mitem = wx.MenuItem(editmenu, -1, "Paste Under")
        self.Bind(wx.EVT_MENU, self.paste_under, mitem)
        ## if add_menuitem:
            ## editmenu.Append(mitem)
        ## else:
            ## viewmenu.Append(mitem)
        editmenu.Append(mitem)
        if disable_menu:
            ## mitem.SetItemLabel(" ")
            mitem.Enable(False)
        if not popup:
            self.pasteunder_item = mitem
        editmenu.AppendSeparator()
        mitem = wx.MenuItem(editmenu, -1, "Insert Attribute")
        self.Bind(wx.EVT_MENU, self.add_attr, mitem)
        editmenu.Append(mitem)
        mitem = wx.MenuItem(editmenu, -1, 'Insert Element Before')
        self.Bind(wx.EVT_MENU, self.insert, mitem)
        editmenu.Append(mitem)
        mitem = wx.MenuItem(editmenu, -1, 'Insert Element After')
        self.Bind(wx.EVT_MENU, self.insert_after, mitem)
        editmenu.Append(mitem)
        mitem = wx.MenuItem(editmenu, -1, 'Insert Element Under')
        self.Bind(wx.EVT_MENU, self.insert_child, mitem)
        editmenu.Append(mitem)
        # accel = wx.AcceleratorTable(accels)
        # self.SetAcceleratorTable(accel)
        if popup:
            return editmenu
        return filemenu, viewmenu, editmenu

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

    def _file_to_save(self):  # afwijkende signature
        """ask for file to save"""
        d, f = os.path.split(self.xmlfn)
        dlg = wx.FileDialog(self, message="Save file as ...",
                            defaultDir=d, defaultFile=f, wildcard=HMASK, style=wx.FD_SAVE)
        ret = dlg.ShowModal()
        ok = (ret == wx.ID_OK)
        name = dlg.GetPath() if ok else ''
        dlg.Destroy()
        return ok, name

    def _enable_pasteitems(self, active=False):
        """activeert of deactiveert de paste-entries in het menu
        afhankelijk van of er iets te pASTEN VALT
        """
        if active:
            self.pastebefore_item.SetItemLabel("Paste Before")
        else:
            self.pastebefore_item.SetItemLabel("Nothing to Paste")
        self.pastebefore_item.Enable(active)
        self.pasteafter_item.Enable(active)
        self.pasteunder_item.Enable(active)

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

    def edit(self, ev=None):
        "edit an element or attribute"
        if not self._checkselection():
            return
        data = self.tree.GetItemText(self.item)  # self.item.get_text()
        if data.startswith(ELSTART):
            tag, text = self.tree.GetItemData(self.item)  # self.item.get_data()
            data = {'item': self.item, 'tag': tag}
            if text is not None:
                data['data'] = True
                data['text'] = text
            edt = ElementDialog(self, title='Edit an element', item=data)
            if edt.ShowModal() == wx.ID_SAVE:
                h = (self.data["tag"], self.data["text"])
                self.tree.SetItemText(self.item, getshortname(h))
                self.tree.SetItemData(self.item, h)
                self.mark_dirty(True)
        else:
            nam, val = self.tree.GetItemData(self.item)  # self.item.get_data()
            data = {'item': self.item, 'name': nam, 'value': val}
            edt = AttributeDialog(self, title='Edit an attribute', item=data)
            if edt.ShowModal() == wx.ID_SAVE:
                h = (self.data["name"], self.data["value"])
                self.tree.SetItemText(self.item, getshortname(h, attr=True))
                self.tree.SetItemData(self.item, h)
                self.mark_dirty(True)
        edt.Destroy()

    def add_attr(self, ev=None):
        "ask for attibute, then start add action"
        if not self._checkselection():
            return
        edt = AttributeDialog(self, title="New attribute")
        test = edt.ShowModal()
        if test == wx.ID_SAVE:
            data = self.tree.GetItemText(self.item)
            if data.startswith(ELSTART):
                h = (self.data["name"], self.data["value"])
                rt = self.tree.AppendItem(self.item, getshortname((h, [], []), attr=True))
                self.tree.SetItemData(rt, h)
                self.mark_dirty(True)
            else:
                self._meldfout("Can't add attribute to attribute")
        edt.Destroy()

    ## def on_click(self, event):      # not used?
        ## self.close()


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
