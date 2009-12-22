import os,sys,shutil,copy
from xml.etree.ElementTree import Element, ElementTree, SubElement
import parseDTD as pd
ELTYPES = ('pcdata','one','opt','mul','mulopt')
ATTTYPES = ('cdata','enum','id')
VALTYPES = ('opt','req','fix','dflt')
ENTTYPES = ('ent', 'ext')
SYMBOLS = {
    'elsrt': {
        'pcdata': ('<#PCDATA>', 'parsed character data'),
        'one': ('<1>', 'single'),
        'opt': ('<?>', 'single optional'),
        'mul': ('<+>', 'multiple'),
        'mulopt': ('<*>', 'multiple optional'),
        },
    'elopt': ('<|>', 'either/or'),
    'attsrt': {
        'cdata': ('[CDATA]', 'character data'),
        'enum': ('[enum]', 'enumerated values'),
        'id': ('[ID]', 'id'),
        ## 'IDREF': ('[=>]', 'related id'),
        ## 'IDREFS': ('[=>>]', 'list of related ids')
        },
    'attwrd': {
        'fix': ('[#FIXED]', 'fixed value'),
        'dflt': ('[:]', 'default value'),
        'req': ('[#REQUIRED]', 'required'),
        'opt': ('[#IMPLIED]', 'optional'),
        },
    'entsrt': {
        'ent': ('{&}', 'internal (value)'),
        'ext': ('{&url}','external (url)  ')}
        }
TITEL = "Albert's (Simple) DTD-editor"
HMASK = "DTD files (*.dtd)|*.dtd|All files (*.*)|*.*"
IMASK = "All files|*.*"

import wx
if os.name == 'ce':
    DESKTOP = False
else:
    DESKTOP = True

def getshortname(x,attr=False,ent=False):
    if attr:
        name,srt,opt,val = x
        strt = ' '.join((SYMBOLS['attsrt'][srt][0],name,
                        SYMBOLS['attwrd'][opt][0],val))
        t = ''.join(('[',']'))
    elif ent:
        name,srt,val = x
        strt = ' '.join((SYMBOLS['entsrt'][srt][0],name,":",val))
    else:
        tag,type,opt = x
        strt = ' '.join((SYMBOLS['elsrt'][type][0],tag))
        if opt:
            strt = SYMBOLS['elopt'][0] + strt
    return strt

def is_element(data):
    test = data.split()[0]
    if test in [x[0] for x in SYMBOLS['elsrt'].values()]:
        return True
    else:
        return False

def is_pcdata(data):
    test = data.split()[0]
    if test == SYMBOLS['elsrt']['pcdata'][0]:
        return True
    else:
        return False

def is_attribute(data):
    test = data.split()[0]
    if test in [x[0] for x in SYMBOLS['attsrt'].values()]:
        return True
    else:
        return False

def is_entitydef(data):
    test = data.split()[0]
    if test in [x[0] for x in SYMBOLS['entsrt'].values()]:
        return True
    else:
        return False

#~ def ParseDTD(data=None,file=None):
    #~ root = Element('Root_Element')
    #~ return ElementTree(root)


class ElementDialog(wx.Dialog):
    def __init__(self,parent,title='',size=wx.DefaultSize,
            pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, item=None,
            not_root=True):
        self.not_root = not_root
        size = (320,200) if not_root else (320,100)
        wx.Dialog.__init__(self,parent,-1,title=title,size=size) #, pos, size, style)
        self._parent = parent
        self.pnl = wx.Panel(self,-1)
        lblName = wx.StaticText(self.pnl, -1,"element name:  ")
        self.txtTag = wx.TextCtrl(self.pnl,-1, size=(200,-1))
        self.txtTag.Bind(wx.EVT_KEY_UP,self.OnKeyUp)
        if not_root:
            lblType = wx.StaticText(self.pnl, -1,"choose one:  ")
            self.rbTypes = [wx.RadioButton(self.pnl,-1,label=SYMBOLS['elsrt'][name][1])
                    for name in ELTYPES]
            self.cbOpt = wx.CheckBox(self.pnl,-1,label=SYMBOLS['elopt'][1])
        self.bOk = wx.Button(self.pnl,id=wx.ID_SAVE)
        self.bOk.Bind(wx.EVT_BUTTON,self.on_ok)
        self.bCancel = wx.Button(self.pnl,id=wx.ID_CANCEL)
        ## self.bCancel.Bind(wx.EVENT_BUTTON,self.on_cancel)
        self.SetAffirmativeId(wx.ID_SAVE)

        tag = ''
        type = ''
        opt = False
        if item:
            tag = item["tag"]
            opt = item['opt']
            type = item["type"]
        self.txtTag.SetValue(tag)
        if not_root:
            if type:
                for ix,name in enumerate(ELTYPES):
                    if name == type:
                        self.rbTypes[ix].SetValue(True)
            ## else:
                ## self.rbTypes[2].SetValue(True)
            self.cbOpt.Value = opt
        sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(lblName,0,wx.ALIGN_CENTER_VERTICAL)
        hsizer.Add(self.txtTag,0,wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(hsizer,0, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.ALL,5)
        if not_root:
            hsizer = wx.BoxSizer(wx.HORIZONTAL)
            hsizer.Add(lblType,0)
            vsizer = wx.BoxSizer(wx.VERTICAL)
            for rb in self.rbTypes:
                vsizer.Add(rb)
            hsizer.Add(vsizer,0,wx.TOP,3)
            sizer.Add(hsizer,0, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.ALL,5)
            hsizer = wx.BoxSizer(wx.HORIZONTAL)
            hsizer.Add(self.cbOpt)
            sizer.Add(hsizer,0, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.ALL,5)
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
        tag = self.txtTag.GetValue()
        if self.not_root and self.rbTypes[0].Value:
            if tag:
                self.txtTag.SetFocus()
                wx.MessageBox('Element name must be empty for PCDATA',
                    self._parent.title, wx.OK|wx.ICON_ERROR)
                return
        else:
            if tag == '' or len(tag.split()) > 1:
                self.txtTag.SetFocus()
                wx.MessageBox('Element name cannot be empty or contain spaces',
                    self._parent.title, wx.OK|wx.ICON_ERROR)
                return
        self._parent.data["tag"] = tag
        if self.not_root:
            typed = False
            for ix,rb in enumerate(self.rbTypes):
                if rb.Value:
                    self._parent.data["type"] = ELTYPES[ix] #rb.LabelText
                    typed = True
            if not typed:
                ## self.rbTypes[0].SetFocus()
                wx.MessageBox('You MUST choose a type for this element',
                    self._parent.title, wx.OK|wx.ICON_ERROR)
                return
            self._parent.data['opt'] = self.cbOpt.Value
        else:
            self._parent.data["type"] = 'one'
            self._parent.data['opt'] = False
        print self._parent.data
        ev.Skip()
        ## self.end('ok')
    def OnKeyUp(self,ev):
        ky = ev.GetKeyCode()
        mod = ev.GetModifiers()
        if ky == 65 and mod == wx.MOD_CONTROL:
            win = ev.GetEventObject()
            if win in (self.txtTag):
                win.SelectAll()

class AttributeDialog(wx.Dialog):
    def __init__(self,parent,title='',size=wx.DefaultSize,
            pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE,item=None):
        wx.Dialog.__init__(self,parent,-1,title=title,size=(320,225)) #,pos.size,style)
        self._parent = parent
        self.pnl = wx.Panel(self,-1)
        lblName = wx.StaticText(self.pnl,-1, "Attribute name:")
        self.txtName = wx.TextCtrl(self.pnl,-1, size=(200,-1))
        self.txtName.Bind(wx.EVT_KEY_UP,self.OnKeyUp)
        lblType = wx.StaticText(self.pnl, -1,"Attribute type:  ")
        self.cmbType = wx.ComboBox(self.pnl, -1, style=wx.CB_READONLY,
            choices=[SYMBOLS['attsrt'][name][1] for name in ATTTYPES])
        lblWrd = wx.StaticText(self.pnl, -1,"choose one:  ")
        self.rbWrds = [wx.RadioButton(self.pnl,-1,label=SYMBOLS['attwrd'][name][1])
                for name in VALTYPES]
        lblValue = wx.StaticText(self.pnl, -1,"Fixed/default value:")
        self.txtValue = wx.TextCtrl(self.pnl,-1, size=(100,-1))
        # self.bList = wx.Button(self.pnl,-1,'Edit List',action=self.EditList)
        self.bOk = wx.Button(self.pnl,id=wx.ID_SAVE)
        self.bOk.Bind(wx.EVT_BUTTON,self.on_ok)
        self.bCancel = wx.Button(self.pnl,id=wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_SAVE)

        nam = val = srt = opt = ''
        if item:
            nam = item["name"]
            srt = item['srt']
            opt = item['opt']
            val = item.get('val','')
        self.txtName.SetValue(nam)
        if srt:
            for name in ATTTYPES:
                if name == srt:
                    self.cmbType.Value = SYMBOLS['attsrt'][name][1]
        else:
            self.cmbType.Value = SYMBOLS['attsrt'][ATTTYPES[0]][1]
        if opt:
            for ix,name in enumerate(VALTYPES):
                if name == opt:
                    self.rbWrds[ix].Value = True
        else:
            self.rbWrds[0].Value = True
        self.txtValue.SetValue(val)

        sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(lblName,0,wx.ALIGN_CENTER_VERTICAL | wx.LEFT|wx.RIGHT,5)
        hsizer.Add(self.txtName,1,wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(hsizer,0, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.ALL,5)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(lblType,0,wx.ALIGN_CENTER_VERTICAL | wx.LEFT|wx.RIGHT,5)
        hsizer.Add(self.cmbType,0,wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(hsizer,0, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.ALL,5)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(lblWrd,0, wx.LEFT|wx.RIGHT,5)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        ## print self.rbTypes
        for rb in self.rbWrds:
            vsizer.Add(rb)
        hsizer.Add(vsizer,0,wx.TOP,3)
        sizer.Add(hsizer,0, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.ALL,5)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(lblValue,0,wx.ALIGN_CENTER_VERTICAL | wx.LEFT|wx.RIGHT,5)
        hsizer.Add(self.txtValue,0,wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        #hsizer.Add(self.bList,0,wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(hsizer,0, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.ALL,5)
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
        typ = self.cmbType.GetValue()
        val = self.txtValue.GetValue()
        print nam
        if nam == '' or len(nam.split()) > 1:
            self.txtName.SetFocus()
            wx.MessageBox('Attribute name cannot be empty or contain spaces',
                self._parent.title,wx.OK|wx.ICON_ERROR)
            return
        if self.rbWrds[2].Value and val == '':
            self.txtValue.SetFocus()
            wx.MessageBox('Vaste waarde opgeven',
                self._parent.title,wx.OK|wx.ICON_ERROR)
            return
        if self.rbWrds[3].Value and val == '':
            self.txtValue.SetFocus()
            wx.MessageBox('Default waarde opgeven',
                self._parent.title,wx.OK|wx.ICON_ERROR)
            return
        self._parent.data["name"] = nam
        for key,wrd in SYMBOLS['attsrt'].items():
            if typ == wrd[1]:
                self._parent.data["srt"] = key
        for ix,rb in enumerate(self.rbWrds):
            if rb.Value:
                self._parent.data["opt"] = VALTYPES[ix]
        self._parent.data["val"] = val
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

    def EditList(self,ev):
            data = {'item': self.item, 'tag': tag, 'type': type, 'opt': opt}
            edt = ListDialog(self,title='Edit enumerated list',item=data)
            if edt.ShowModal() == wx.ID_SAVE:
                h = (self.data["tag"],self.data['type'],self.data['opt'])
                self.tree.SetItemText(self.item,getshortname(h))
                self.tree.SetItemPyData(self.item,h)

class EntityDialog(wx.Dialog):
    def __init__(self,parent,title='',size=wx.DefaultSize,
            pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE,item=None):
        wx.Dialog.__init__(self,parent,-1,title=title,size=(320,160)) #,pos.size,style)
        self._parent = parent
        self.pnl = wx.Panel(self,-1)
        lblName = wx.StaticText(self.pnl,-1, "Entity name:")
        self.txtName = wx.TextCtrl(self.pnl,-1, size=(200,-1))
        self.txtName.Bind(wx.EVT_KEY_UP,self.OnKeyUp)
        #lblValue = wx.StaticText(self.pnl,-1, "Attribute value:")
        #self.txtValue = wx.TextCtrl(self.pnl,-1, size=(200,-1))
        #self.txtValue.Bind(wx.EVT_KEY_UP,self.OnKeyUp)
        lblType = wx.StaticText(self.pnl, -1,"Definition:  ")
        self.rbTypes = [wx.RadioButton(self.pnl,-1,
            label=SYMBOLS['entsrt'][name][1] + ": ")
                for name in ENTTYPES]
        self.txtVal = wx.TextCtrl(self.pnl,-1, size=(100,-1))
        self.txtUrl = wx.TextCtrl(self.pnl,-1, size=(100,-1))
        self.bOk = wx.Button(self.pnl,id=wx.ID_SAVE)
        self.bOk.Bind(wx.EVT_BUTTON,self.on_ok)
        self.bCancel = wx.Button(self.pnl,id=wx.ID_CANCEL)
        ## self.bCancel.Bind(wx.EVT_BUTTON,self.on_cancel)
        self.SetAffirmativeId(wx.ID_SAVE)

        nam = val = srt = url = ''
        if item:
            nam = item["name"]
            #val = item["value"]
            srt = item['srt']
            val = item.get('val','')
        self.txtName.SetValue(nam)
        #self.txtValue.SetValue(val)
        if srt == ENTTYPES[0]:
            self.rbTypes[0].SetValue(True)
            self.txtVal.SetValue(val)
        elif srt == ENTTYPES[1]:
            self.rbTypes[1].SetValue(True)
            self.txtUrl.SetValue(val)
        else:
            self.rbTypes[0].SetValue(True)

        sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(lblName,0,wx.ALIGN_CENTER_VERTICAL | wx.LEFT|wx.RIGHT,5)
        hsizer.Add(self.txtName,1,wx.EXPAND)
        sizer.Add(hsizer,1, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.ALL,5)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(lblType,0,wx.TOP|wx.LEFT|wx.RIGHT,5)
        #hsizer.Add(lblValue,0,wx.ALIGN_CENTER_VERTICAL | wx.LEFT|wx.RIGHT,5)
        #hsizer.Add(self.txtValue,1,wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        #sizer.Add(hsizer,1, wx.EXPAND | wx.ALL,5)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        for ix,rb in enumerate(self.rbTypes):
            hhsizer = wx.BoxSizer(wx.HORIZONTAL)
            hhsizer.Add(rb,0,wx.ALIGN_CENTER_VERTICAL | wx.ALL,1)
            if ix == 0:
                hhsizer.Add(self.txtVal,0,wx.ALIGN_CENTER_VERTICAL | wx.ALL,1)
            elif ix == 1:
                hhsizer.Add(self.txtUrl,0,wx.ALIGN_CENTER_VERTICAL | wx.ALL,1)
            vsizer.Add(hhsizer)
        hsizer.Add(vsizer,0)
        sizer.Add(hsizer,0, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.ALL,5)
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
        ent = self.rbTypes[0].Value
        val = self.txtVal.GetValue()
        url = self.txtUrl.GetValue()
        ext = self.rbTypes[1].Value
        print nam
        if nam == '' or len(nam.split()) > 1:
            self.txtName.SetFocus()
            wx.MessageBox('Entity name cannot be empty or contain spaces',
                self._parent.title,wx.OK|wx.ICON_ERROR)
            return
        if ent and val == '':
            self.txtVal.SetFocus()
            wx.MessageBox('Waarde opgeven',
                self._parent.title,wx.OK|wx.ICON_ERROR)
            return
        if ext and url == '':
            self.txtUrl.SetFocus()
            wx.MessageBox('Url opgeven',
                self._parent.title,wx.OK|wx.ICON_ERROR)
            return
        self._parent.data["name"] = nam
        #self._parent.data["value"] = self.txtValue.GetValue()
        if ent:
            self._parent.data["srt"] = 'ent'
            self._parent.data["val"] = val
        elif ext:
            self._parent.data["srt"] = 'ext'
            self._parent.data["val"] = url
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
            size=(320,450)
            )
        self.SetIcon(wx.Icon("axe.ico",wx.BITMAP_TYPE_ICO))

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
        self.cut_ent = None
        self.cut_el = None
        if self.xmlfn == '':
            self.rt = Element('New_Root')
            self.openxml()
        else:
            self.rt = parse_dtd(file=self.xmlfn).getroot()
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
            if not self.cut_el and not self.cut_att and not self.cut_ent:
                mitem.SetItemLabel("Nothing to Paste")
                mitem.Enable(False)
        else:
            self.pastebefore_item = mitem
        editmenu.AppendItem(mitem)
        mitem = wx.MenuItem(editmenu, -1, "Paste After")
        self.Bind(wx.EVT_MENU,self.paste_aft,mitem)
        if popup:
            if not self.cut_el and not self.cut_att and not self.cut_ent:
                ## mitem.SetItemLabel(" ")
                mitem.Enable(False)
        else:
            self.pasteafter_item = mitem
        editmenu.AppendItem(mitem)
        mitem = wx.MenuItem(editmenu, -1, "Paste Under")
        self.Bind(wx.EVT_MENU,self.paste_und,mitem)
        if popup:
            if not self.cut_el and not self.cut_att and not self.cut_ent:
                ## mitem.SetItemLabel(" ")
                mitem.Enable(False)
        else:
            self.pasteunder_item = mitem
        editmenu.AppendItem(mitem)
        editmenu.AppendSeparator()
        mitem = wx.MenuItem(editmenu, -1, 'Insert Element Before')
        self.Bind(wx.EVT_MENU,self.insert,mitem)
        editmenu.AppendItem(mitem)
        mitem = wx.MenuItem(editmenu, -1, 'Insert Element After')
        self.Bind(wx.EVT_MENU,self.ins_aft,mitem)
        editmenu.AppendItem(mitem)
        mitem = wx.MenuItem(editmenu, -1, 'Insert Element Under')
        self.Bind(wx.EVT_MENU,self.ins_chld,mitem)
        editmenu.AppendItem(mitem)
        mitem = wx.MenuItem(editmenu, -1, "Add Attribute")
        self.Bind(wx.EVT_MENU,self.add_attr,mitem)
        editmenu.AppendItem(mitem)
        mitem = wx.MenuItem(editmenu, -1, "Add Entity")
        self.Bind(wx.EVT_MENU,self.add_ent,mitem)
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

    def newxml(self,ev=None):
        h = wx.Dialog.askstring("AXE", "Enter a name (tag) for the root element")
        if h is not None:
            self.init_tree("(untitled)")

    def openxml(self,ev=None):
        ## self.openfile()
        try:
            email = pd.DTDParser(fromstring="""\
<!ELEMENT note (to,from,heading,body)>
<!ELEMENT to (#PCDATA)>
<!ELEMENT from (#PCDATA)>
<!ELEMENT heading (#PCDATA)>
<!ELEMENT body (#PCDATA)>
<!ATTLIST body NAME CDATA #IMPLIED CATEGORY (HandTool|Table|Shop-Professional) "HandTool" PARTNUM CDATA #IMPLIED PLANT (Pittsburgh|Milwaukee|Chicago) "Chicago" INVENTORY (InStock|Backordered|Discontinued) "InStock">
<!ENTITY writer "Donald Duck.">
<!ENTITY copyright SYSTEM "http://www.w3schools.com/entities.dtd">
    """)
        except pd.DTDParsingError,msg:
            print msg
            return
        self.rt = email
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
        if dlg.ShowModal() == wx.ID_OK:
            h = dlg.GetPath()
            if not self._openfile(h):
                dlg = wx.MessageBox('dtd parsing error',
                               self.title, wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
        dlg.Destroy()

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
        wx.MessageBox("Made in 2009 by Albert Visser\nWritten in (wx)Python",
            self.title,wx.OK|wx.ICON_INFORMATION
            )

    def quit(self,ev=None):
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
            titel = '[untitled]'
        self.top = self.tree.AddRoot(titel)
        self.SetTitle(" - ".join((os.path.split(titel)[-1],TITEL)))

        h = (self.rt.tag,'one',False)
        rt = self.tree.AppendItem(self.top,getshortname(h))
        self.tree.SetItemPyData(rt,h)
        for el in list(self.rt):
            add_to_tree(el,rt)
        #self.tree.selection = self.top
        # set_selection()

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
                ## if data.startswith(ELSTART):
                    ## if self.tree.GetChildrenCount(item):
                        ## edit = False
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
        pt = ev.GetPosition()
        ky = ev.GetKeyCode()
        item, flags = self.tree.HitTest(pt)
        if item and item != self.top:
            if ky == wx.WXK_DELETE:
                self.delete()
            elif ky == wx.WXK_F2:
                self.edit()
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
        test = self.tree.GetItemText(self.item) # self.item.get_text()
        if is_element(test):
            tag,type,opt = self.tree.GetItemPyData(self.item) # self.item.get_data()
            data = {'item': self.item, 'tag': tag, 'type': type, 'opt': opt}
            if tag == self.rt.tag:
                edt = ElementDialog(self,title='Edit root element',item=data,not_root=False)
            else:
                edt = ElementDialog(self,title='Edit an element',item=data)
            if edt.ShowModal() == wx.ID_SAVE:
                h = (self.data["tag"],self.data['type'],self.data['opt'])
                self.tree.SetItemText(self.item,getshortname(h))
                self.tree.SetItemPyData(self.item,h)
        elif is_attribute(test):
            nam,srt,opt,val = self.tree.GetItemPyData(self.item) # self.item.get_data()
            data = {'item': self.item, 'name': nam, 'srt': srt, 'opt': opt, 'val': val}
            edt = AttributeDialog(self,title='Edit an attribute',item=data)
            if edt.ShowModal() == wx.ID_SAVE:
                h = (self.data["name"],self.data["srt"],
                 self.data["opt"],self.data["val"])
                self.tree.SetItemText(self.item,getshortname(h,attr=True))
                self.tree.SetItemPyData(self.item,h)
        elif is_entitydef(test):
            nam,srt,val = self.tree.GetItemPyData(self.item) # self.item.get_data()
            data = {'item': self.item, 'name': nam, 'srt': srt, 'val': val}
            edt = EntityDialog(self,title='Edit an attribute',item=data)
            if edt.ShowModal() == wx.ID_SAVE:
                h = (self.data["name"],self.data["srt"],self.data["val"])
                self.tree.SetItemText(self.item,getshortname(h,attr=True))
                self.tree.SetItemPyData(self.item,h)
        else:
            return
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
            if is_element(text):
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
        txt = 'cut' if cut else 'copy'
        txt = txt if retain else 'delete'
        if data == (self.rt.tag,'one',False):
            wx.MessageBox("Can't %s the root" % txt,
                self.title,wx.OK | wx.ICON_ERROR)
            return
        ## print "copy(): print text,data"
        ## print text,data
        if retain:
            self.cut_el = None
            self.cut_att = None
            self.cut_ent = None
            if is_element(text):
                ## self.cut_el = self.item # hmmm... hier moet de aanroep van push_el komen
                self.cut_el = []
                self.cut_el = push_el(self.item,self.cut_el)
            elif is_attribute(text):
                self.cut_att = data
            elif is_entitydef(text):
                self.cut_ent = data
        if cut:
            self.tree.Delete(self.item)
        self.enable_pasteitems(True)
        print "copy(): print self.cut_el, _att, _ent"
        print self.cut_el, self.cut_att, self.cut_ent

    def paste(self, ev=None,before=True,pastebelow=False):
        if DESKTOP and not self.checkselection():
            return
        data = self.tree.GetItemPyData(self.item)
        if pastebelow:
            text = self.tree.GetItemText(self.item)
            if not is_element(text):
                wx.MessageBox("Can't paste under a non-element",self.title,
                wx.OK | wx.ICON_ERROR)
                return
            if is_pcdata(text):
                wx.MessageBox("Can't paste under PCDATA",self.title,
                wx.OK | wx.ICON_ERROR)
                return
        if data == self.rt:
            if before:
                wx.MessageBox("Can't paste before the root",
                    self.title,wx.OK | wx.ICON_ERROR)
                return
            else:
                wx.MessageBox("Pasting as first element under root",
                    self.title,wx.OK | wx.ICON_INFORMATION)
                pastebelow = True
        if self.cut:
            self.enable_pasteitems(False)
        print "paste(): print self.cut_el, _att, _ent"
        print self.cut_el, self.cut_att, self.cut_ent
        if self.cut_el:
            def zetzeronder(node,el,pos=-1):
                ## print "zetzeronder()"
                ## print "node: ",node
                ## print "el:", el
                ## item = self.tree.GetItemText(el)
                ## data = self.tree.GetItemPyData(el)
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
        else:
            if self.cut_att:
                item = getshortname(self.cut_att,attr=True)
                data = self.cut_att
            else:
                item = getshortname(self.cut_ent,ent=True)
                data = self.cut_ent
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

    def paste_aft(self, ev=None):
        self.paste(before=False)

    def paste_und(self, ev=None):
        self.paste(pastebelow=True)

    def add_attr(self, ev=None):
        if DESKTOP and not self.checkselection():
            return
        text = self.tree.GetItemText(self.item)
        if not is_element(text):
            wx.MessageBox("Can't insert under a non-element",self.title,
                wx.OK | wx.ICON_ERROR)
            return
        if is_pcdata(text):
            wx.MessageBox("Can't insert under PCDATA",
                self.title,wx.OK | wx.ICON_ERROR)
            return
        edt = AttributeDialog(self,title="New attribute")
        if edt.ShowModal() == wx.ID_SAVE:
            h = (self.data["name"],self.data["srt"],
                 self.data["opt"],self.data["val"])
            rt = self.tree.AppendItem(self.item,getshortname(h,attr=True))
            self.tree.SetItemPyData(rt,h)
        edt.Destroy()

    def add_ent(self, ev=None):
        if DESKTOP and not self.checkselection():
            return
        text = self.tree.GetItemText(self.item)
        if not is_element(text):
            wx.MessageBox("Can't insert under a non-element",self.title,
                wx.OK | wx.ICON_ERROR)
            return
        if is_pcdata(text):
            wx.MessageBox("Can't insert under PCDATA",
                self.title,wx.OK | wx.ICON_ERROR)
            return
        edt = EntityDialog(self,title="New entity")
        if edt.ShowModal() == wx.ID_SAVE:
            h = (self.data["name"],self.data["srt"],self.data["val"])
            rt = self.tree.AppendItem(self.item,getshortname(h,ent=True))
            self.tree.SetItemPyData(rt,h)
        edt.Destroy()

    def insert(self, ev=None,before=True,below=False):
        if DESKTOP and not self.checkselection():
            return
        if below:
            text = self.tree.GetItemText(self.item)
            if not is_element(text):
                wx.MessageBox("Can't insert under a non-element",self.title,
                    wx.OK | wx.ICON_ERROR)
                return
            if is_pcdata(text):
                wx.MessageBox("Can't insert under PCDATA",
                    self.title,wx.OK | wx.ICON_ERROR)
                return
        if self.tree.GetItemPyData(self.item) == (self.rt.tag,'one',False) and not below:
            wx.MessageBox("Can't insert before/after the root",
                self.title,wx.OK | wx.ICON_ERROR)
            return
        edt = ElementDialog(self,title="New element")
        if edt.ShowModal() == wx.ID_SAVE:
            data = (self.data['tag'],self.data['type'],self.data['opt'])
            text = getshortname(data)
            if below:
                rt = self.tree.AppendItem(self.item,text)
                self.tree.SetItemPyData(rt,data)
            else:
                parent = self.tree.GetItemParent(self.item)
                item = self.item if not before else self.tree.GetPrevSibling(self.item)
                node = self.tree.InsertItem(parent,item,text)
                self.tree.SetPyData(node,data)
        edt.Destroy()

    def ins_aft(self, ev=None):
        self.insert(before=False)

    def ins_chld(self, ev=None):
        self.insert(below=True)

    def on_click(self, event):
       self.close()

class MainGui(object):
    def __init__(self,args):
        app = wx.App(redirect=False) # True,filename="axe.log")
        if len(args) > 1:
            frm = MainFrame(None, -1, fn=args[1])
        else:
            frm = MainFrame(None, -1)
        app.MainLoop()


def test_is_element():
    for test in [x[0] for x in SYMBOLS['elsrt'].values()]:
        assert is_element(" ".join((test,"testdata")))," ".join((test,'wordt niet herkend als element'))
    for test in ('<15> hallo','','xxxxx',"hallo daar vrienden"):
        assert not is_element(" ".join((test,"testdata")))," ".join((test,'wordt herkend als element'))

def test_is_attribute():
    for test in [x[0] for x in SYMBOLS['attsrt'].values()]:
        assert is_attribute(" ".join((test,"testdata")))," ".join((test,'wordt niet herkend als attribuut'))
    for test in ('<15> hallo','','xxxxx',"hallo daar vrienden"):
        assert not is_attribute(" ".join((test,"testdata")))," ".join((test,'wordt herkend als attribuut'))

def test_is_entitydef():
    for test in [x[0] for x in SYMBOLS['entsrt'].values()]:
        assert is_entitydef(" ".join((test,"testdata")))," ".join((test,'wordt niet herkend als entiteit'))
    for test in ('<15> hallo','','xxxxx',"hallo daar vrienden"):
        assert not is_entitydef(" ".join((test,"testdata")))," ".join((test,'wordt herkend als entiteit'))

if __name__ == "__main__":
    ## print sys.argv
    ## test_is_element()
    ## test_is_attribute()
    ## test_is_entitydef()
    MainGui(sys.argv)
