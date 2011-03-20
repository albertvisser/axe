import os,sys,shutil,copy
from xml.etree.ElementTree import Element, ElementTree, SubElement
ELSTART = '<>'
TITEL = "Albert's (Simple) XML-editor"
if os.name == "nt":
    HMASK = "XML files (*.xml)|*.xml|All files (*.*)|*.*"
elif os.name == "posix":
    HMASK = "XML files (*.xml, *.XML)|*.xml;*.XML|All files (*.*)|*.*"
IMASK = "All files|*.*"
PPATH = os.path.split(__file__)[0]
import wx
if os.name == 'ce':
    DESKTOP = False
else:
    DESKTOP = True

def getshortname(x,attr=False):
    t = ''
    if attr:
        t = x[1]
        if t[-1] == "\n": t = t[:-1]
    elif x[1]:
        t = x[1].split("\n",1)[0]
    w = 60
    if len(t) > w: t = t[:w].lstrip() + '...'
    strt = ' '.join((ELSTART,x[0]))
    if attr:
        return " = ".join((x[0],t))
    elif t:
        return ": ".join((strt,t))
    else:
        return strt

class ElementDialog(wx.Dialog):
    def __init__(self,parent,title='',size=wx.DefaultSize,
            pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, item=None):
        wx.Dialog.__init__(self,parent,-1,title=title) #, pos, size, style)
        self._parent = parent
        self.pnl = wx.Panel(self,-1)
        lblName = wx.StaticText(self.pnl, -1,"element name:  ")
        self.txtTag = wx.TextCtrl(self.pnl,-1, size=(200,-1))
        self.txtTag.Bind(wx.EVT_KEY_UP,self.OnKeyUp)
        self.cb = wx.CheckBox(self.pnl,-1,label='Bevat data:')
        ## lblData = wx.StaticText(self.pnl, -1, "text data:")
        self.txtData = wx.TextCtrl(self.pnl,-1, size=(300,140),
            style=wx.TE_MULTILINE )
        self.txtData.Bind(wx.EVT_KEY_UP,self.OnKeyUp)
        self.bOk = wx.Button(self.pnl,id=wx.ID_SAVE)
        self.bOk.Bind(wx.EVT_BUTTON,self.on_ok)
        self.bCancel = wx.Button(self.pnl,id=wx.ID_CANCEL)
        ## self.bCancel.Bind(wx.EVET_BUTTON,self.on_cancel)
        self.SetAffirmativeId(wx.ID_SAVE)

        tag = ''
        txt = ''
        if item:
            tag = item["tag"]
            if "text" in item:
                self.cb.SetValue(True)
                txt = item["text"]
        self.txtTag.SetValue(tag)
        self.txtData.SetValue(txt)

        sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(lblName,0,wx.ALIGN_CENTER_VERTICAL)
        hsizer.Add(self.txtTag,0,wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(hsizer,0, wx.EXPAND | wx.ALL,5)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.cb,0,wx.TOP,3)
        ## hsizer.add(lblData)
        hsizer.Add(self.txtData)
        sizer.Add(hsizer,0, wx.EXPAND | wx.ALL,5)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.bOk,0,wx.EXPAND | wx.ALL, 2)
        hsizer.Add(self.bCancel,0,wx.EXPAND | wx.ALL, 2)
        sizer.Add(hsizer,0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL,2)
        self.pnl.SetSizer(sizer)
        self.pnl.SetAutoLayout(True)
        sizer.Fit(self.pnl)
        sizer.SetSizeHints(self.pnl)
        self.pnl.Layout()

    def on_cancel(self, ev):
        self.end('cancel')

    def on_ok(self, ev):
        self._parent.data = {}
        tag = self.txtTag.GetValue()
        print tag
        if tag == '' or len(tag.split()) > 1:
            wx.MessageBox('Element name cannot be empty or contain spaces',
                self._parent.title, wx.OK|wx.ICON_ERROR)
            return
        self._parent.data["tag"] = tag
        self._parent.data["data"] = self.cb.IsChecked()
        self._parent.data["text"] = self.txtData.GetValue()
        print self._parent.data
        ev.Skip()
        ## self.end('ok')

    def OnKeyUp(self,ev):
        ky = ev.GetKeyCode()
        mod = ev.GetModifiers()
        if ky == 65 and mod == wx.MOD_CONTROL:
            win = ev.GetEventObject()
            if win in (self.txtTag, self.txtData):
                win.SelectAll()

class AttributeDialog(wx.Dialog):
    def __init__(self,parent,title='',size=wx.DefaultSize,
            pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE,item=None):
        wx.Dialog.__init__(self,parent,-1,title=title,size=(320,125)) #,pos.size,style)
        self._parent = parent
        self.pnl = wx.Panel(self,-1)
        lblName = wx.StaticText(self.pnl,-1, "Attribute name:")
        self.txtName = wx.TextCtrl(self.pnl,-1, size=(200,-1))
        self.txtName.Bind(wx.EVT_KEY_UP,self.OnKeyUp)
        lblValue = wx.StaticText(self.pnl,-1, "Attribute value:")
        self.txtValue = wx.TextCtrl(self.pnl,-1, size=(200,-1))
        self.txtValue.Bind(wx.EVT_KEY_UP,self.OnKeyUp)
        self.bOk = wx.Button(self.pnl,id=wx.ID_SAVE)
        self.bOk.Bind(wx.EVT_BUTTON,self.on_ok)
        self.bCancel = wx.Button(self.pnl,id=wx.ID_CANCEL)
        ## self.bCancel.Bind(wx.EVT_BUTTON,self.on_cancel)
        self.SetAffirmativeId(wx.ID_SAVE)

        nam = ''
        val = ''
        if item:
            nam = item["name"]
            val = item["value"]
        self.txtName.SetValue(nam)
        self.txtValue.SetValue(val)

        sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(lblName,0,wx.ALIGN_CENTER_VERTICAL | wx.LEFT|wx.RIGHT,5)
        hsizer.Add(self.txtName,1,wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(hsizer,1, wx.EXPAND | wx.ALL,5)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(lblValue,0,wx.ALIGN_CENTER_VERTICAL | wx.LEFT|wx.RIGHT,5)
        hsizer.Add(self.txtValue,1,wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(hsizer,1, wx.EXPAND | wx.ALL,5)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.bOk,0,wx.EXPAND | wx.ALL, 2)
        hsizer.Add(self.bCancel,0,wx.EXPAND | wx.ALL, 2)
        sizer.Add(hsizer,0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL,2)

        self.pnl.SetSizer(sizer)
        self.pnl.SetAutoLayout(True)
        sizer.Fit(self.pnl)
        sizer.SetSizeHints(self.pnl)
        self.pnl.Layout()

    def on_ok(self, ev):
        self._parent.data = {}
        nam = self.txtName.GetValue()
        print nam
        if nam == '':
            wx.MessageBox('Attribute name cannot be empty or spaces',
                self._parent.title,wx.OK|wx.ICON_ERROR)
            return
        self._parent.data["name"] = nam
        self._parent.data["value"] = self.txtValue.GetValue()
        ## self.end('ok')
        print self._parent.data
        ev.Skip()

    def on_cancel(self, ev):
        self.end('cancel')

    def OnKeyUp(self,ev):
        ky = ev.GetKeyCode()
        mod = ev.GetModifiers()
        if ky == 65 and mod == wx.MOD_CONTROL:
            win = ev.GetEventObject()
            if win in (self.txtName, self.txtValue):
                win.SelectAll()

class MainFrame(wx.Frame):
    def __init__(self,parent,id,fn=''):
        self.parent = parent
        self.title = "Albert's XML Editor"
        self.xmlfn = fn
        wx.Frame.__init__(self,parent,id,
            pos=(2,2),
            size=(620,900)
            )
        self.SetIcon(wx.Icon(os.path.join(PPATH,"axe.ico"),wx.BITMAP_TYPE_ICO))

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
        self.tree = wx.TreeCtrl(self.pnl,-1)        self.tree.Bind(wx.EVT_LEFT_DCLICK, self.onLeftDClick)
        self.tree.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.tree.Bind(wx.EVT_KEY_UP,self.OnKeyUp)
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

        self.cut_att = None
        self.cut_el = None
        self.tree_dirty = False
        if self.xmlfn == '':
            self.rt = Element('New')
            self.openxml()
        else:
            self.rt = ElementTree(file=self.xmlfn).getroot()
            self.init_tree()

    def init_menus(self,popup=False):
        if popup:
            viewmenu = wx.Menu()
        else:
            filemenu = wx.Menu()
            mitem = wx.MenuItem(filemenu, -1, "&New")
            self.Bind(wx.EVT_MENU,self.newxml,mitem)
            filemenu.AppendItem(mitem)
            mitem = wx.MenuItem(filemenu, -1, "&Open")
            self.Bind(wx.EVT_MENU,self.openxml,mitem)
            filemenu.AppendItem(mitem)
            mitem = wx.MenuItem(filemenu, -1, '&Save')
            self.Bind(wx.EVT_MENU,self.savexml,mitem)
            filemenu.AppendItem(mitem)
            mitem = wx.MenuItem(filemenu, -1, 'Save &As')
            self.Bind(wx.EVT_MENU,self.savexmlas,mitem)
            filemenu.AppendItem(mitem)
            filemenu.AppendSeparator()
            mitem = wx.MenuItem(filemenu, -1, 'E&xit')
            self.Bind(wx.EVT_MENU,self.quit,mitem)
            filemenu.AppendItem(mitem)
            viewmenu = wx.Menu()

        mitem = wx.MenuItem(viewmenu, -1, "&Expand All (sub)Levels")
        self.Bind(wx.EVT_MENU,self.expand,mitem)
        viewmenu.AppendItem(mitem)
        mitem = wx.MenuItem(viewmenu, -1, "&Collapse All (sub)Levels")
        self.Bind(wx.EVT_MENU,self.collapse,mitem)
        viewmenu.AppendItem(mitem)

        if popup:
            editmenu = viewmenu
            editmenu.AppendSeparator()
        else:
            editmenu = wx.Menu()

        mitem = wx.MenuItem(editmenu, -1, "&Edit")
        self.Bind(wx.EVT_MENU,self.edit,mitem)
        editmenu.AppendItem(mitem)
        editmenu.AppendSeparator()
        mitem = wx.MenuItem(editmenu, -1, "&Delete")
        self.Bind(wx.EVT_MENU,self.delete,mitem)
        editmenu.AppendItem(mitem)
        mitem = wx.MenuItem(editmenu, -1, "C&ut")
        self.Bind(wx.EVT_MENU,self.cut,mitem)
        editmenu.AppendItem(mitem)
        mitem = wx.MenuItem(editmenu, -1, "&Copy")
        self.Bind(wx.EVT_MENU,self.copy,mitem)
        editmenu.AppendItem(mitem)
        mitem = wx.MenuItem(editmenu, -1, "Paste Before")
        self.Bind(wx.EVT_MENU,self.paste,mitem)
        if popup:
            if not self.cut_el and not self.cut_att:
                mitem.SetItemLabel("Nothing to Paste")
                mitem.Enable(False)
        else:
            self.pastebefore_item = mitem
        editmenu.AppendItem(mitem)
        mitem = wx.MenuItem(editmenu, -1, "Paste After")
        self.Bind(wx.EVT_MENU,self.paste_aft,mitem)
        if popup:
            if not self.cut_el and not self.cut_att:
                ## mitem.SetItemLabel(" ")
                mitem.Enable(False)
        else:
            self.pasteafter_item = mitem
        editmenu.AppendItem(mitem)
        mitem = wx.MenuItem(editmenu, -1, "Paste Under")
        self.Bind(wx.EVT_MENU,self.paste_und,mitem)
        if popup:
            if not self.cut_el and not self.cut_att:
                ## mitem.SetItemLabel(" ")
                mitem.Enable(False)
        else:
            self.pasteunder_item = mitem
        editmenu.AppendItem(mitem)
        editmenu.AppendSeparator()
        mitem = wx.MenuItem(editmenu, -1, "Insert Attribute")
        self.Bind(wx.EVT_MENU,self.add_attr,mitem)
        editmenu.AppendItem(mitem)
        mitem = wx.MenuItem(editmenu, -1, 'Insert Element Before')
        self.Bind(wx.EVT_MENU,self.insert,mitem)
        editmenu.AppendItem(mitem)
        mitem = wx.MenuItem(editmenu, -1, 'Insert Element After')
        self.Bind(wx.EVT_MENU,self.ins_aft,mitem)
        editmenu.AppendItem(mitem)
        mitem = wx.MenuItem(editmenu, -1, 'Insert Element Under')
        self.Bind(wx.EVT_MENU,self.ins_chld,mitem)
        editmenu.AppendItem(mitem)
        if popup:
            return editmenu
        else:
            return filemenu, viewmenu, editmenu

    def enable_pasteitems(self,active=False):
        if active:
            self.pastebefore_item.SetItemLabel("Paste Before")
        else:
            self.pastebefore_item.SetItemLabel("Nothing to Paste")
        self.pastebefore_item.Enable(active)
        self.pasteafter_item.Enable(active)

    def check_tree(self):
        print "check_tree aangeroepen"
        if self.tree_dirty:
            h = wx.MessageBox("XML data has been modified - save before continuing?",
                self.title,
                style = wx.YES_NO)
            if h == wx.YES:
                self.savexml()

    def newxml(self,ev=None):
        self.check_tree()
        h = wx.GetTextFromUser("Enter a name (tag) for the root element",
            self.title)
        if h:
            self.rt = Element(h)
            self.xmlfn = ""
            self.init_tree()

    def openxml(self,ev=None):
        self.check_tree()
        if self.openfile():
            self.init_tree()

    def _openfile(self,h):
        try:
            rt = ElementTree(file=h).getroot()
        except:
            return False
        else:
            self.rt = rt
            self.xmlfn = h
            return True

    def openfile(self,ev=None):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(),
            wildcard=HMASK,
            style=wx.OPEN
            )
        ret = dlg.ShowModal()
        if ret == wx.ID_OK:
            h = dlg.GetPath()
            if not self._openfile(h):
                dlg = wx.MessageBox('parsing error, probably not well-formed xml',
                               self.title, wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
                return False
        dlg.Destroy()
        return (ret == wx.ID_OK)

    def savexmlfile(self,oldfile=''):
        def expandnode(rt,root):
            tag,c = self.tree.GetFirstChild(rt)
            while tag.IsOk():
                text = self.tree.GetItemText(tag)
                data = self.tree.GetItemPyData(tag)
                ## print text,data[0],data[1]
                if text.startswith(ELSTART):
                    node = SubElement(root,data[0])
                    if data[1]:
                        node.text = data[1]
                    expandnode(tag,node)
                else:
                    root.set(data[0],data[1])
                tag,c = self.tree.GetNextChild(rt,c)
        print "savexmlfile():",self.xmlfn
        try:
            shutil.copyfile(self.xmlfn,self.xmlfn + '.bak')
        except IOError as mld:
            ## wx.MessageBox(str(mld),self.title,wx.OK|wx.ICON_ERROR)
            pass
        top = self.tree.GetRootItem()
        rt = self.tree.GetLastChild(top)
        text = self.tree.GetItemText(rt)
        data = self.tree.GetItemPyData(rt)
        root = Element(data[0]) # .split(None,1)
        expandnode(rt,root)
        h = ElementTree(root).write(self.xmlfn,encoding="iso-8859-1")
        self.tree_dirty = False

    def savexml(self,ev=None):
        ## print "savexml(): ", self.xmlfn
        if self.xmlfn == '':
            self.savexmlas()
        else:
            self.savexmlfile()

    def savexmlas(self,ev=None):
        d,f = os.path.split(self.xmlfn)
        ## print "savexmlas(): ", d,f
        dlg = wx.FileDialog(
            self, message="Save file as ...",
            defaultDir=d,
            defaultFile=f,
            wildcard=HMASK,
            style=wx.SAVE
            )
        if dlg.ShowModal() == wx.ID_OK:
            self.xmlfn = dlg.GetPath()
            ## print "savexmlas(): ", self.xmlfn
            self.savexmlfile() # oldfile=os.path.join(d,f))
            self.tree.SetItemText(self.top,self.xmlfn)
            self.SetTitle(" - ".join((os.path.split(self.xmlfn)[-1],TITEL)))
        dlg.Destroy()

    def about(self,ev=None):
        wx.MessageBox("Made in 2008 by Albert Visser\nWritten in (wx)Python",
            self.title,wx.OK|wx.ICON_INFORMATION
            )

    def quit(self,ev=None):
        print "quit aangeroepen, self.dirty is", self.tree_dirty
        self.check_tree()
        self.Close()

    def init_tree(self,name=''):
        def add_to_tree(el,rt):
            h = (el.tag,el.text)
            rr = self.tree.AppendItem(rt,getshortname(h))
            self.tree.SetItemPyData(rr,h)
            for attr in el.keys():
                h = el.get(attr)
                if not h: h = '""'
                h = (attr,h)
                rrr = self.tree.AppendItem(rr,getshortname(h,attr=True))
                self.tree.SetItemPyData(rrr,h)
            for subel in list(el):
                add_to_tree(subel,rr)
        self.tree.DeleteAllItems()

        if name:
            titel = name
        elif self.xmlfn:
            titel = self.xmlfn
        else:
            titel = '[unsaved file]'
        self.top = self.tree.AddRoot(titel)
        self.SetTitle(" - ".join((os.path.split(titel)[-1],TITEL)))

        h = (self.rt.tag,self.rt.text)
        rt = self.tree.AppendItem(self.top,getshortname(h))
        self.tree.SetItemPyData(rt,h)
        for el in list(self.rt):
            add_to_tree(el,rt)
        #self.tree.selection = self.top
        # set_selection()
        self.tree_dirty = False


    def on_bdown(self, ev=None):
        if wx.recon_context(self.tree, ev):
            self.item = self.tree.selection
            if self.item == self.top:
                wx.context_menu(self, ev, self.filemenu)
            elif self.item is not None:
                wx.context_menu(self, ev, self.editmenu)
            else:
                wx.Message.ok(self.title,'You need to select a tree item first')
                #menu.append()
        else:
            ev.skip()

    def onLeftDClick(self,ev=None):
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

    def OnRightDown(self, ev=None):
        pt = ev.GetPosition()
        item, flags = self.tree.HitTest(pt)
        if item and item != self.top:
            self.tree.SelectItem(item)
            menu = self.init_menus(popup=True)
            self.PopupMenu(menu)
            ## print "klaar met menu"
            menu.Destroy()
        ## pass

    def OnKeyUp(self, ev=None):
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
                self.title,wx.OK | wx.ICON_INFORMATION)
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
        if data.startswith('<>'):
            tag,text = self.tree.GetItemPyData(self.item) # self.item.get_data()
            data = {'item': self.item, 'tag': tag}
            if text is not None:
                data['data'] = True
                data['text'] = text
            edt = ElementDialog(self,title='Edit an element',item=data)
            if edt.ShowModal() == wx.ID_SAVE:
                h = (self.data["tag"],self.data["text"])
                self.tree.SetItemText(self.item,getshortname(h))
                self.tree.SetItemPyData(self.item,h)
                self.tree_dirty = True
        else:
            nam,val = self.tree.GetItemPyData(self.item) # self.item.get_data()
            data = {'item': self.item, 'name': nam, 'value': val}
            edt = AttributeDialog(self,title='Edit an attribute',item=data)
            if edt.ShowModal() == wx.ID_SAVE:
                h = (self.data["name"],self.data["value"])
                self.tree.SetItemText(self.item,getshortname(h,attr=True))
                self.tree.SetItemPyData(self.item,h)
                self.tree_dirty = True
        edt.Destroy()

    def cut(self, ev=None):
        self.copy(cut=True)

    def delete(self, ev=None):
        self.copy(cut=True, retain=False)

    def copy(self, ev=None, cut=False, retain=True): # retain is t.b.v. delete functie
        def push_el(el,result):
            # print "start: ",result
            text = self.tree.GetItemText(el)
            data = self.tree.GetItemPyData(el)
            y = []
            # print "before looping over contents:",text,y
            if text.startswith(ELSTART):
                x,c = self.tree.GetFirstChild(el)
                while x.IsOk():
                    z = push_el(x,y)
                    x,c = self.tree.GetNextChild(el,c)
            # print "after  looping over contents: ",text,y
            result.append((text,data,y))
            # print "end:  ",result
            return result
        if DESKTOP and not self.checkselection():
            return
        text = self.tree.GetItemText(self.item)
        data = self.tree.GetItemPyData(self.item)
        if cut:
            if retain:
                txt = 'cut'
            else:
                txt = 'delete'
        else:
            txt = 'copy'

        if data == (self.rt.tag,self.rt.text):
            wx.MessageBox("Can't %s the root" % txt,
                self.title,wx.OK | wx.ICON_ERROR)
            return
        ## print "copy(): print text,data"
        ## print text,data
        if retain:
            if text.startswith(ELSTART):
                ## self.cut_el = self.item # hmmm... hier moet de aanroep van push_el komen
                self.cut_el = []
                self.cut_el = push_el(self.item,self.cut_el)
                self.cut_att = None
            else:
                self.cut_el = None
                self.cut_att = data
        if cut:
            self.tree.Delete(self.item)
            self.tree_dirty = True
        self.enable_pasteitems(True)

    def paste(self, ev=None,before=True,pastebelow=False):
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
        if self.cut:
            self.enable_pasteitems(False)
        print "paste(): print self.cut_el, self.cut_att"
        print self.cut_el, self.cut_att
        if self.cut_att:
            item = getshortname(self.cut_att,attr=True)
            data = self.cut_att
            if pastebelow:
                node = self.tree.AppendItem(self.item,item)
                self.tree.SetItemPyData(node,data)
            else:
                add_to = self.tree.GetItemParent(self.item) # self.item.get_parent()
                added = False
                x,c = self.tree.GetFirstChild(add_to)
                for i in range(self.tree.GetChildrenCount(add_to)):
                    if x == self.item:
                        if not before:
                            i += 1
                        node = self.tree.InsertItemBefore(add_to,i,item)
                        self.tree.SetItemPyData(node,data)
                        added = True
                        break
                    x,c = self.tree.GetNextChild(add_to,c)
                if not added:
                    node = self.tree.AppendItem(add_to,item)
                    self.tree.SetItemPyData(node,data)
        else:
            def zetzeronder(node,el,pos=-1):
                if pos == -1:
                    subnode = self.tree.AppendItem(node,el[0])
                    self.tree.SetItemPyData(subnode,el[1])
                else:
                    subnode = self.tree.InsertItemBefore(node,i,el[0])
                    self.tree.SetItemPyData(subnode,el[1])
                for x in el[2]:
                    zetzeronder(subnode,x)
            if pastebelow:
                node = self.item
                i = -1
            else:
                node = self.tree.GetItemParent(self.item) # self.item.get_parent()
                x,c = self.tree.GetFirstChild(node)
                cnt = self.tree.GetChildrenCount(node)
                for i in range(cnt):
                    if x == self.item:
                        if not before: i += 1
                        break
                    x,c = self.tree.GetNextChild(node,c)
                if i == cnt: i = -1
            zetzeronder(node,self.cut_el[0],i)
        self.tree_dirty = True

    def paste_aft(self, ev=None):
        self.paste(before=False)

    def paste_und(self, ev=None):
        self.paste(pastebelow=True)

    def add_attr(self, ev=None):
        if DESKTOP and not self.checkselection():
            return
        edt = AttributeDialog(self,title="New attribute")
        if edt.ShowModal() == wx.ID_SAVE:
            h = (self.data["name"],self.data["value"])
            rt = self.tree.AppendItem(self.item,getshortname(h,attr=True))
            self.tree.SetItemPyData(rt,h)
            self.tree_dirty = True
        edt.Destroy()

    def insert(self, ev=None,before=True,below=False):
        if DESKTOP and not self.checkselection():
            return
        edt = ElementDialog(self,title="New element")
        if edt.ShowModal() == wx.ID_SAVE:
            data = (self.data['tag'],self.data['text'])
            text = getshortname(data)
            if below:
                rt = self.tree.AppendItem(self.item,text)
                self.tree.SetItemPyData(rt,data)
            else:
                parent = self.tree.GetItemParent(self.item)
                item = self.item if not before else self.tree.GetPrevSibling(self.item)
                node = self.tree.InsertItem(parent,item,text)
                self.tree.SetPyData(node,data)
            self.tree_dirty = True
        edt.Destroy()

    def ins_aft(self, ev=None):
        self.insert(before=False)

    def ins_chld(self, ev=None):
        self.insert(below=True)

    def on_click(self, event):
       self.close()
class MainGui(object):
    def __init__(self,args):
        app = wx.App(redirect=True,filename="axe.log")
        if len(args) > 1:
            frm = MainFrame(None, -1, fn=args[1])
        else:
            frm = MainFrame(None, -1)
        app.MainLoop()

if __name__ == "__main__":
    print sys.argv
    MainGui(sys.argv)
