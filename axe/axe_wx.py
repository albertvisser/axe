"wxPython versie van een op een treeview gebaseerde XML-editor"

## import logging
## logging.basicConfig(filename='axe_wx.log', level=logging.DEBUG,
    ## format='%(asctime)s %(message)s')

import os
import sys
if os.name == 'ce':
    DESKTOP = False
else:
    DESKTOP = True
import wx
from axe_base import getshortname, XMLTree, AxeMixin
from axe_base import ELSTART, TITEL, axe_iconame
if os.name == "nt":
    HMASK = "XML files (*.xml)|*.xml|All files (*.*)|*.*"
elif os.name == "posix":
    HMASK = "XML files (*.xml, *.XML)|*.xml;*.XML|All files (*.*)|*.*"
IMASK = "All files|*.*"

class ElementDialog(wx.Dialog):
    def __init__(self, parent, title='', size=(400, 270),
            pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
            item=None):
        wx.Dialog.__init__(self, parent, -1, title=title, pos=pos, size=size,
            style=style)
        self._parent = parent
        self.pnl = wx.Panel(self, -1)
        lbl_name = wx.StaticText(self.pnl, -1, "element name:  ")
        self.txt_tag = wx.TextCtrl(self.pnl, -1, size=(200, -1))
        self.txt_tag.Bind(wx.EVT_KEY_UP, self.on_keyup)
        self.cb = wx.CheckBox(self.pnl, -1, label='Bevat data:')
        ## lbl_data = wx.StaticText(self.pnl, -1, "text data:")
        self.txt_data = wx.TextCtrl(self.pnl, -1, size=(300, 140),
            style=wx.TE_MULTILINE )
        self.txt_data.Bind(wx.EVT_KEY_UP,self.on_keyup)
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
        vsizer.Add(self.cb, 0, wx.ALIGN_CENTER_HORIZONTAL) # ,wx.TOP, 3)
        vsizer.Add(self.txt_data, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)
        hsizer.Add(vsizer, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(hsizer, 1, wx.EXPAND | wx.ALL, 5)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.btn_ok, 0, wx.EXPAND | wx.ALL, 2)
        hsizer.Add(self.btn_cancel, 0, wx.EXPAND | wx.ALL, 2)
        sizer.Add(hsizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL |
            wx.ALIGN_CENTER_VERTICAL, 2)

        self.pnl.SetSizer(sizer)
        self.pnl.SetAutoLayout(True)
        sizer.Fit(self.pnl)
        sizer.SetSizeHints(self.pnl)
        self.pnl.Layout()
        self.txt_tag.SetFocus()

    def on_cancel(self, ev):
        self.end('cancel')

    def on_ok(self, ev):
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

    def on_keyup(self,ev):
        ky = ev.GetKeyCode()
        mod = ev.GetModifiers()
        if ky == 65 and mod == wx.MOD_CONTROL:
            win = ev.GetEventObject()
            if win in (self.txt_tag, self.txt_data):
                win.SelectAll()

class AttributeDialog(wx.Dialog):
    def __init__(self,parent,title='',size=(320,125),
            pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE  | wx.RESIZE_BORDER,
            item=None):
        wx.Dialog.__init__(self, parent, -1, title=title, pos=pos, size=size,
            style=style)
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
        hsizer.Add(lbl_name, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT |wx.RIGHT, 5)
        hsizer.Add(self.txt_name, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        sizer.Add(hsizer, 0, wx.EXPAND | wx.ALL, 5)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(lbl_value, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
        hsizer.Add(self.txt_value, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        sizer.Add(hsizer, 0, wx.EXPAND | wx.ALL, 5)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.btn_ok, 0, wx.EXPAND | wx.ALL, 2)
        hsizer.Add(self.btn_cancel, 0, wx.EXPAND | wx.ALL, 2)
        sizer.Add(hsizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL |
            wx.ALIGN_CENTER_VERTICAL, 2)

        self.pnl.SetSizer(sizer)
        self.pnl.SetAutoLayout(True)
        sizer.Fit(self.pnl)
        sizer.SetSizeHints(self.pnl)
        self.pnl.Layout()
        self.txt_name.SetFocus()

    def on_ok(self, ev):
        self._parent.data = {}
        nam = self.txt_name.GetValue()
        if nam == '':
            wx.MessageBox('Attribute name cannot be empty or spaces',
                self._parent.title,wx.OK | wx.ICON_ERROR)
            return
        self._parent.data["name"] = nam
        self._parent.data["value"] = self.txt_value.GetValue()
        ## self.end('ok')
        ev.Skip()

    def on_cancel(self, ev):
        self.end('cancel')

    def on_keyup(self,ev):
        ky = ev.GetKeyCode()
        mod = ev.GetModifiers()
        if ky == 65 and mod == wx.MOD_CONTROL:
            win = ev.GetEventObject()
            if win in (self.txt_name, self.txt_value):
                win.SelectAll()

class MainFrame(wx.Frame, AxeMixin):
    "Main GUI class"
    def __init__(self, parent, id, fn=''):
        AxeMixin.__init__(self, parent, id, fn)

    def _init_gui(self, parent, id):
        self.parent = parent
        wx.Frame.__init__(self, parent, id, pos=(2, 2), size=(620, 900))
        self.SetIcon(wx.Icon(axe_iconame, wx.BITMAP_TYPE_ICO))
        self.Bind(wx.EVT_CLOSE, self.afsl)

        self.init_menus()
        menuBar = wx.MenuBar()
        filemenu, viewmenu, editmenu = self.init_menus()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(viewmenu, "&View")
        menuBar.Append(editmenu, "&Edit")
        self.SetMenuBar(menuBar)

        self.enable_pasteitems(False)
        ## self.helpmenu.append('About', callback = self.about)

        self.pnl = wx.Panel(self,-1)
        self.tree = wx.TreeCtrl(self.pnl,-1)        self.tree.Bind(wx.EVT_LEFT_DCLICK, self.on_doubleclick)
        self.tree.Bind(wx.EVT_RIGHT_DOWN, self.on_rightdown)
        self.tree.Bind(wx.EVT_KEY_UP,self.on_keyup)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.tree,1,wx.EXPAND)
        sizer0.Add(sizer1,1,wx.EXPAND)
        self.pnl.SetSizer(sizer0)
        self.pnl.SetAutoLayout(True)
        sizer0.Fit(self.pnl)
        sizer0.SetSizeHints(self.pnl)
        self.pnl.Layout()
        self.Show(True)
        self.tree.SetFocus()

        self.mark_dirty(False)

    def init_menus(self, popup=False):
        if popup:
            viewmenu = wx.Menu()
        else:
            filemenu = wx.Menu()
            mitem = wx.MenuItem(filemenu, -1, "&New")
            self.Bind(wx.EVT_MENU, self.newxml, mitem)
            filemenu.AppendItem(mitem)
            mitem = wx.MenuItem(filemenu, -1, "&Open")
            self.Bind(wx.EVT_MENU, self.openxml, mitem)
            filemenu.AppendItem(mitem)
            mitem = wx.MenuItem(filemenu, -1, '&Save')
            self.Bind(wx.EVT_MENU, self.savexml, mitem)
            filemenu.AppendItem(mitem)
            mitem = wx.MenuItem(filemenu, -1, 'Save &As')
            self.Bind(wx.EVT_MENU, self.savexmlas, mitem)
            filemenu.AppendItem(mitem)
            filemenu.AppendSeparator()
            mitem = wx.MenuItem(filemenu, -1, 'E&xit')
            self.Bind(wx.EVT_MENU, self.quit, mitem)
            filemenu.AppendItem(mitem)
            viewmenu = wx.Menu()

        mitem = wx.MenuItem(viewmenu, -1, "&Expand All (sub)Levels")
        self.Bind(wx.EVT_MENU, self.expand, mitem)
        viewmenu.AppendItem(mitem)
        mitem = wx.MenuItem(viewmenu, -1, "&Collapse All (sub)Levels")
        self.Bind(wx.EVT_MENU, self.collapse, mitem)
        viewmenu.AppendItem(mitem)

        if popup:
            editmenu = viewmenu
            editmenu.AppendSeparator()
        else:
            editmenu = wx.Menu()

        mitem = wx.MenuItem(editmenu, -1, "&Edit")
        self.Bind(wx.EVT_MENU, self.edit, mitem)
        editmenu.AppendItem(mitem)
        editmenu.AppendSeparator()
        mitem = wx.MenuItem(editmenu, -1, "&Delete")
        self.Bind(wx.EVT_MENU, self.delete, mitem)
        editmenu.AppendItem(mitem)
        mitem = wx.MenuItem(editmenu, -1, "C&ut")
        self.Bind(wx.EVT_MENU, self.cut, mitem)
        editmenu.AppendItem(mitem)
        mitem = wx.MenuItem(editmenu, -1, "&Copy")
        self.Bind(wx.EVT_MENU, self.copy, mitem)
        editmenu.AppendItem(mitem)
        print("creating paste before menu item")
        mitem = wx.MenuItem(editmenu, -1, "Paste Before")
        self.Bind(wx.EVT_MENU, self.paste, mitem)
        disable_menu = True if not self.cut_el and not self.cut_att else False
        add_menuitem = True if not popup or not disable_menu else False
        if disable_menu:
            print("disabling item")
            mitem.SetItemLabel("Nothing to Paste")
            mitem.Enable(False)
        if not popup:
            print("no popping up today")
            self.pastebefore_item = mitem
        if add_menuitem:
            editmenu.AppendItem(mitem)
        print("creating paste after menu item")
        mitem = wx.MenuItem(editmenu, -1, "Paste After")
        self.Bind(wx.EVT_MENU, self.paste_aft, mitem)
        if disable_menu:
            print("disabling item")
            ## mitem.SetItemLabel(" ")
            mitem.Enable(False)
        if not popup:
            print("no popping up today")
            self.pasteafter_item = mitem
        if add_menuitem:
            editmenu.AppendItem(mitem)
        print("creating paste under menu item")
        mitem = wx.MenuItem(editmenu, -1, "Paste Under")
        self.Bind(wx.EVT_MENU, self.paste_und, mitem)
        if disable_menu:
            print("disabling item")
            ## mitem.SetItemLabel(" ")
            mitem.Enable(False)
        if not popup:
            print("no popup today")
            self.pasteunder_item = mitem
        if add_menuitem:
            editmenu.AppendItem(mitem)
        editmenu.AppendSeparator()
        mitem = wx.MenuItem(editmenu, -1, "Insert Attribute")
        self.Bind(wx.EVT_MENU, self.add_attr, mitem)
        editmenu.AppendItem(mitem)
        mitem = wx.MenuItem(editmenu, -1, 'Insert Element Before')
        self.Bind(wx.EVT_MENU, self.insert, mitem)
        editmenu.AppendItem(mitem)
        mitem = wx.MenuItem(editmenu, -1, 'Insert Element After')
        self.Bind(wx.EVT_MENU, self.ins_aft, mitem)
        editmenu.AppendItem(mitem)
        mitem = wx.MenuItem(editmenu, -1, 'Insert Element Under')
        self.Bind(wx.EVT_MENU, self.ins_chld, mitem)
        editmenu.AppendItem(mitem)
        if popup:
            return editmenu
        else:
            return filemenu, viewmenu, editmenu

    def enable_pasteitems(self, active=False):
        """activeert of deactiveert de paste-entries in het menu
        afhankelijk van of er iets te pASTEN VALT
        """
        print("enable pasteitems called using {}".format(active))
        if active:
            self.pastebefore_item.SetItemLabel("Paste Before")
        else:
            self.pastebefore_item.SetItemLabel("Nothing to Paste")
        self.pastebefore_item.Enable(active)
        self.pasteafter_item.Enable(active)
        self.pasteunder_item.Enable(active)

    def mark_dirty(self, state):
        data = AxeMixin.mark_dirty(self, state, self.GetTitle())
        if data:
            self.SetTitle(data)

    def _ask_yesnocancel(self, prompt):
        """stelt een vraag en retourneert het antwoord
        1 = Yes, 0 = No, -1 = Cancel
        """
        retval = dict(zip((wx.YES, wx.NO, wx.CANCEL), (1, 0, -1)))
        h = wx.MessageBox(prompt, self.title, style = wx.YES_NO | wx.CANCEL)
        return h

    def newxml(self, ev=None):
        AxeMixin.newxml(self)
        print("self.newxml aangeroepen")

    def _ask_for_text(self, prompt):
        """vraagt om tekst en retourneert het antwoord"""
        return wx.GetTextFromUser(prompt, self.title)

    def openxml(self, ev=None):
        AxeMixin.openxml(self)

    def _file_to_read(self):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(),
            wildcard=HMASK,
            style=wx.OPEN
            )
        ret = dlg.ShowModal()
        ok = (ret == wx.ID_OK)
        fnaam = dlg.GetPath() if ok else ''
        dlg.Destroy()
        return ok, fnaam

    def _meldinfo(self, text):
        wx.MessageBox(text, self.title, wx.OK | wx.ICON_INFORMATION)

    def _meldfout(self, text, abort=False):
        wx.MessageBox(text, self.title, wx.OK | wx.ICON_ERROR)
        if abort:
            self.quit()

    def savexml(self, ev=None):
        AxeMixin.savexml(self)

    def savexmlfile(self, oldfile=''):
        def expandnode(rt, root, tree):
            tag, c = self.tree.GetFirstChild(rt)
            while tag.IsOk():
                text = self.tree.GetItemText(tag)
                data = self.tree.GetItemPyData(tag)
                node = tree.expand(root, text, data)
                if node is not None:
                    expandnode(tag, node, tree)
                tag, c = self.tree.GetNextChild(rt, c)
        AxeMixin.savexmlfile(self, oldfile)
        top = self.tree.GetRootItem()
        rt = self.tree.GetLastChild(top)
        text = self.tree.GetItemText(rt)
        data = self.tree.GetItemPyData(rt)
        tree = XMLTree(data[0]) # .split(None,1)
        root = tree.root
        expandnode(rt, root, tree)
        h = tree.write(self.xmlfn)
        self.mark_dirty(False)

    def savexmlas(self, ev=None):
        ok = AxeMixin.savexmlas(self)
        if ok:
            self.tree.SetItemText(self.top, self.xmlfn)
            self.SetTitle(" - ".join((os.path.basename(self.xmlfn), TITEL)))

    def _file_to_save(self, d, f):
        dlg = wx.FileDialog(
            self, message="Save file as ...",
            defaultDir=d,
            defaultFile=f,
            wildcard=HMASK,
            style=wx.SAVE
            )
        ret = dlg.ShowModal()
        ok = (ret == wx.ID_OK)
        name = dlg.GetPath() if ok else ''
        dlg.Destroy()
        return ok, name

    def about(self, ev=None):
        AxeMixin.about(self)

    def quit(self, ev=None):
        self.Close()

    def afsl(self, ev=None):
        print "quit aangeroepen, self.dirty is", self.tree_dirty
        if self.check_tree():
            ev.Skip()
        ev.Veto()

    def init_tree(self, name=''):    # blijft gui methode
        def add_to_tree(el, rt):
            h = (el.tag, el.text)
            rr = self.tree.AppendItem(rt, getshortname(h))
            self.tree.SetItemPyData(rr, h)
            for attr in el.keys():
                h = el.get(attr)
                if not h:
                    h = '""'
                h = (attr, h)
                rrr = self.tree.AppendItem(rr, getshortname(h, attr=True))
                self.tree.SetItemPyData(rrr, h)
            for subel in list(el):
                add_to_tree(subel, rr)

        self.tree.DeleteAllItems()
        titel = AxeMixin.init_tree(self, name)
        self.top = self.tree.AddRoot(titel)
        self.SetTitle(" - ".join((os.path.split(titel)[-1],TITEL)))

        h = (self.rt.tag,self.rt.text)
        rt = self.tree.AppendItem(self.top,getshortname(h))
        self.tree.SetItemPyData(rt,h)
        for el in list(self.rt):
            add_to_tree(el,rt)
        #self.tree.selection = self.top
        # set_selection()
        self.mark_dirty(False)

    def on_doubleclick(self,ev=None):
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
        pt = ev.GetPosition()
        item, flags = self.tree.HitTest(pt)
        if item and item != self.top:
            self.tree.SelectItem(item)
            menu = self.init_menus(popup=True)
            self.PopupMenu(menu)
            ## print "klaar met menu"
            menu.Destroy()
        ## pass

    def on_keyup(self, ev=None):
        ky = ev.GetKeyCode()
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

    def checkselection(self):
        sel = True
        self.item = self.tree.Selection
        if self.item is None or self.item == self.top:
            wx.MessageBox('You need to select an element or attribute first',
                self.title, wx.OK | wx.ICON_INFORMATION)
        return sel

    def expand(self,ev=None):
        item = self.tree.Selection
        if item:
            self.tree.ExpandAllChildren(item)

    def collapse(self,ev=None):
        item = self.tree.Selection
        if item:
            self.tree.CollapseAllChildren(item)

    def edit(self, ev=None):
        if DESKTOP and not self.checkselection():
            return
        data = self.tree.GetItemText(self.item) # self.item.get_text()
        if data.startswith(ELSTART):
            tag,text = self.tree.GetItemPyData(self.item) # self.item.get_data()
            data = {'item': self.item, 'tag': tag}
            if text is not None:
                data['data'] = True
                data['text'] = text
            edt = ElementDialog(self, title='Edit an element', item=data)
            if edt.ShowModal() == wx.ID_SAVE:
                h = (self.data["tag"], self.data["text"])
                self.tree.SetItemText(self.item, getshortname(h))
                self.tree.SetItemPyData(self.item, h)
                self.mark_dirty(True)
        else:
            nam, val = self.tree.GetItemPyData(self.item) # self.item.get_data()
            data = {'item': self.item, 'name': nam, 'value': val}
            edt = AttributeDialog(self,title='Edit an attribute',item=data)
            if edt.ShowModal() == wx.ID_SAVE:
                h = (self.data["name"], self.data["value"])
                self.tree.SetItemText(self.item, getshortname(h, attr=True))
                self.tree.SetItemPyData(self.item, h)
                self.mark_dirty(True)
        edt.Destroy()

    def cut(self, ev=None):
        AxeMixin.cut(self)

    def delete(self, ev=None):
        AxeMixin.delete(self)

    def copy(self, ev=None, cut=False, retain=True): # retain is t.b.v. delete functie
        def push_el(el, result):
            # print "start: ",result
            text = self.tree.GetItemText(el)
            data = self.tree.GetItemPyData(el)
            children = []
            # print "before looping over contents:",text,y
            if text.startswith(ELSTART):
                subel, whereami = self.tree.GetFirstChild(el)
                while x.IsOk():
                    temp = push_el(subel, children)
                    subel, whereami = self.tree.GetNextChild(el, whereami)
            # print "after  looping over contents: ",text,y
            result.append((text, data, children))
            # print "end:  ",result
            return result
        if DESKTOP and not self.checkselection():
            return
        text = self.tree.GetItemText(self.item)
        data = self.tree.GetItemPyData(self.item)
        txt = AxeMixin.copy(self, cut, retain)
        if data == (self.rt.tag, self.rt.text):
            wx.MessageBox("Can't %s the root" % txt,
                self.title, wx.OK | wx.ICON_ERROR)
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
            self.enable_pasteitems(True)
        if cut:
            prev = self.tree.GetPrevSibling(self.item)
            if not prev.IsOk():
                prev = self.tree.GetItemParent(self.item)
                if prev == self.rt:
                    prev = self.tree.GetNextSibling(self.item)
            self.tree.Delete(self.item)
            self.mark_dirty(True)
            self.tree.SelectItem(prev)

    def paste_aft(self, ev=None):
        AxeMixin.paste_aft(self)

    def paste_und(self, ev=None):
        AxeMixin.paste_und(self)

    def paste(self, ev=None, before=True, pastebelow=False):
        if DESKTOP and not self.checkselection():
            return
        data = self.tree.GetItemPyData(self.item)
        if pastebelow and not self.tree.GetItemText(self.item).startswith(ELSTART):
            wx.MessageBox("Can't paste below an attribute",self.title,
                wx.OK | wx.ICON_ERROR)
            return
        if data == self.rt:
            if before:
                wx.MessageBox("Can't paste before the root",
                    self.title,wx.OK | wx.ICON_ERROR)
                return
            else:
                wx.MessageBox("Pasting as first element below root",
                    self.title,wx.OK | wx.ICON_INFORMATION)
                pastebelow = True
        ## if self.cut:
            ## self.enable_pasteitems(False)
        print "paste(): print self.cut_el, self.cut_att"
        print self.cut_el, self.cut_att
        if self.cut_att:
            item = getshortname(self.cut_att, attr=True)
            data = self.cut_att
            if pastebelow:
                node = self.tree.AppendItem(self.item, item)
                self.tree.SetItemPyData(node, data)
            else:
                add_to = self.tree.GetItemParent(self.item) # self.item.get_parent()
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
                if pos == -1:
                    subnode = self.tree.AppendItem(node, el[0])
                    self.tree.SetItemPyData(subnode, el[1])
                else:
                    subnode = self.tree.InsertItemBefore(node, i, el[0])
                    self.tree.SetItemPyData(subnode, el[1])
                for x in el[2]:
                    zetzeronder(subnode, x)
            if pastebelow:
                node = self.item
                i = -1
            else:
                node = self.tree.GetItemParent(self.item) # self.item.get_parent()
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

    def add_attr(self, ev=None):
        if DESKTOP and not self.checkselection():
            return
        edt = AttributeDialog(self, title="New attribute")
        test = edt.ShowModal()
        if test == wx.ID_SAVE:
            data = self.tree.GetItemText(self.item)
            if data.startswith(ELSTART):
                h = (self.data["name"], self.data["value"])
                rt = self.tree.AppendItem(self.item, getshortname(h, attr=True))
                self.tree.SetItemPyData(rt, h)
                self.mark_dirty(True)
            else:
                self._meldfout("Can't add attribute to attribute")
        edt.Destroy()

    def ins_aft(self, ev=None):
        AxeMixin.ins_aft(self)

    def ins_chld(self, ev=None):
        AxeMixin.ins_chld(self)

    def insert(self, ev=None, before=True, below=False):
        if DESKTOP and not self.checkselection():
            return
        edt = ElementDialog(self, title="New element")
        if edt.ShowModal() == wx.ID_SAVE:
            data = (self.data['tag'], self.data['text'])
            text = getshortname(data)
            if below:
                rt = self.tree.AppendItem(self.item, text)
                self.tree.SetItemPyData(rt, data)
            else:
                parent = self.tree.GetItemParent(self.item)
                if before:
                    item = self.tree.GetPrevSibling(self.item)
                else:
                    item = self.item
                node = self.tree.InsertItem(parent, item, text)
                self.tree.SetPyData(node, data)
            self.mark_dirty(True)
        edt.Destroy()

    def on_click(self, event):
       self.close()

def axe_gui(args):
        app = wx.App(redirect=False) # True, filename="/home/albert/xmledit/axe/axe_wx.log")
        print "----"
        if len(args) > 1:
            frm = MainFrame(None, -1, fn=" ".join(args[1:]))
        else:
            frm = MainFrame(None, -1)
        app.MainLoop()

if __name__ == "__main__":
    axe_gui(sys.argv)
