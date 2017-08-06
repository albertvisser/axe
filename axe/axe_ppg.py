"""XMLEdit PocketPyGUI versie - not actively maintained
"""
import os,sys,shutil,copy
from xml.etree.ElementTree import Element, ElementTree, SubElement
ELSTART = '<>'
if os.name == 'ce':
    DESKTOP = False
    import ppygui as gui
else:
    DESKTOP = True
    import ppygui.api as gui

def getshortname(x,attr=False):
    t = ''
    if attr:
        t = x[1]
        if t[-1] == "\n": t = t[:-1]
    elif x[1]:
        t = x[1].split("\n",1)[0]
    w = 8
    if DESKTOP:
        w = 20
    if len(t) > w: t = t[:w].lstrip() + '...'
    strt = ' '.join((ELSTART,x[0]))
    if attr:
        return " = ".join((x[0],t))
    elif t:
        return ": ".join((strt,t))
    else:
        return strt

class ElementDialog(gui.Dialog):
    def __init__(self,title='',item=None):
        gui.Dialog.__init__(self,title,action=("Cancel", self.on_cancel))
        lblName = gui.Label(self, "element name:")
        self.txtTag = gui.Edit(self)
        self.cb = gui.Button(self,title='Bevat data:',style="check")
        lblData = gui.Label(self, "text data:")
        self.txtData = gui.Edit(self,multiline=True,line_wrap=True)
        self.bOk = gui.Button(self,title='Ok',action=self.on_ok)
        self.bCancel = gui.Button(self,title='Cancel',action=self.on_cancel)
        self.sippref = gui.SIPPref(self)

        tag = ''
        txt = ''
        if item:
            tag = item["tag"]
            if "text" in item:
                self.cb.checked = True
                txt = item["text"]
        self.txtTag.append(tag)
        self.txtData.append(txt)

        sizer = gui.VBox((2,2,2,2))
        hsizer = gui.HBox()
        hsizer.add(lblName)
        hsizer.add(self.txtTag)
        sizer.add(hsizer)
        hsizer = gui.HBox()
        hsizer.add(self.cb)
        #hsizer.add(lblData)
        sizer.add(hsizer)
        hsizer = gui.HBox()
        hsizer.add(self.txtData)
        sizer.add(hsizer)
        hsizer = gui.HBox()
        hsizer.add(self.bOk)
        hsizer.add(self.bCancel)
        sizer.add(hsizer)
        self.sizer = sizer

    def on_cancel(self, ev):
        self.end('cancel')

    def on_ok(self, ev):
        self._parent.data = {}
        self.txtTag.select_all()
        tag = self.txtTag.selected_text.strip()
        if tag == '':
            gui.message.ok(self._parent.title,'Element name cannot be empty or spaces')
            return
        self._parent.data["tag"] = tag
        self._parent.data["data"] = self.cb.checked
        self.txtData.select_all()
        self._parent.data["text"] = self.txtData.selected_text
        self.end('ok')

class AttributeDialog(gui.Dialog):
    def __init__(self,title='',item=None):
        gui.Dialog.__init__(self,title,action=("Cancel", self.on_cancel))
        lblName = gui.Label(self, "Attribute name:")
        self.txtName = gui.Edit(self)
        lblValue = gui.Label(self, "Attribute value:")
        self.txtValue = gui.Edit(self)
        self.bOk = gui.Button(self,title='Ok',action=self.on_ok)
        self.bCancel = gui.Button(self,title='Cancel',action=self.on_cancel)
        self.sippref = gui.SIPPref(self)

        nam = ''
        val = ''
        if item:
            nam = item["name"]
            val = item["value"]
        self.txtName.append(nam)
        self.txtValue.append(val)

        sizer = gui.VBox((2,2,2,2))
        hsizer = gui.HBox()
        hsizer.add(lblName)
        sizer.add(hsizer)
        hsizer = gui.HBox()
        hsizer.add(self.txtName)
        sizer.add(hsizer)
        hsizer = gui.HBox()
        hsizer.add(lblValue)
        sizer.add(hsizer)
        hsizer = gui.HBox()
        hsizer.add(self.txtValue)
        sizer.add(hsizer)
        hsizer = gui.HBox()
        hsizer.add(self.bOk)
        hsizer.add(self.bCancel)
        sizer.add(hsizer)
        self.sizer = sizer

    def on_ok(self, ev):
        self._parent.data = {}
        self.txtName.select_all()
        nam = self.txtName.selected_text.strip()
        if nam == '':
            gui.message.ok(self._parent.title,'Attribute name cannot be empty or spaces')
            return
        self._parent.data["name"] = nam
        self.txtValue.select_all()
        self._parent.data["value"] = self.txtValue.selected_text
        self.end('ok')

    def on_cancel(self, ev):
        self.end('cancel')

class MainFrame(gui.CeFrame):
    def __init__(self,fn=''):
        self.title = "Albert's XML Editor"
        gui.CeFrame.__init__(self,
            title=self.title,
            action=("About", self.about),
            menu="Menu"
            )
        self.xmlfn = fn
        self.sipp = gui.SIPPref(self)
        self.tree = gui.Tree(self)
        self.filemenu = gui.PopupMenu()
        self.filemenu.append("New",callback=self.newxml)
        self.filemenu.append("Open",callback=self.openxml)
        self.filemenu.append('Save', callback = self.savexml)
        self.filemenu.append('Save As', callback = self.savexmlas)
        self.filemenu.append_separator()
        self.filemenu.append('Exit', callback = self.quit)
        self.editmenu = gui.PopupMenu()
        self.editmenu.append("Edit", callback = self.edit)
        self.editmenu.append_separator()
        self.editmenu.append("Cut", callback = self.cut)
        self.editmenu.append("Copy", callback = self.copy)
        self.pastebeforeitem = self.editmenu.append("Paste Before", callback = self.paste)
        self.pasteafteritem = self.editmenu.append("Paste After", callback = self.paste_aft)
        self.editmenu.append_separator()
        self.editmenu.append("Insert Attribute",callback=self.add_attr)
        self.editmenu.append('Insert Element Before', callback=self.insert)
        self.editmenu.append('Insert Element After', callback=self.ins_aft)
        self.editmenu.append('Insert Element Under', callback=self.ins_chld)
        self.pastebeforeitem.set_title = "Nothing to Paste"
        self.pastebeforeitem.enable(False)
        self.pasteafteritem.set_title = " "
        self.pasteafteritem.enable(False)
        ## self.helpmenu.append('About', callback = self.about)

        sizer = gui.VBox(border=(2,2,2,2), spacing=2)        sizer.add(self.tree)        self.sizer = sizer
        if self.xmlfn == '':
            self.rt = Element('New')
            if DESKTOP:
                self.openxml()
            else:
                self.init_tree("(untitled)")
        else:
            self.rt = ElementTree(file=self.xmlfn).getroot()
            self.init_tree()

        # context menu doesn't work in PC version, cb_menu doesn't in WM2003
        if DESKTOP:
            self.cb_menu.append_menu("File",self.filemenu)
            self.cb_menu.append_menu("Edit",self.editmenu)
        else:
            self.tree.bind(lbdown=self.on_bdown)

    def newxml(self,ev=None):
        h = gui.Dialog.askstring("AXE", "Enter a name (tag) for the root element")
        if h is not None:
            self.init_tree("(untitled)")

    def openxml(self,ev=None):
        self.openfile()
        self.init_tree()

    def openfile(self,ev=None):
        h = gui.FileDialog.open(wildcards={"XML files": "*.xml"})
        if h:
            try:
                rt = ElementTree(file=h).getroot()
            except:
                h = gui.Message.ok(self.title,'parsing error, probably not well-formed xml')
            else:
                self.rt = rt
                self.xmlfn = h

    def savexmlfile(self,ev=None):
        def expandnode(node,root):
            for el in node:
                name,value = el.data
                # print name, value
                if el.text.startswith(ELSTART):
                    sub = SubElement(root,name)
                    if value:
                        sub.text = value
                    expandnode(el,sub)
                else:
                    root.set(name,value)
        ## print self.xmlfn
        try:
            shutil.copyfile(self.xmlfn,self.xmlfn + '.bak')
        except IOError,mld:
            ## print mld
            pass
        rt = self.tree.roots[1]
        print rt.text, rt.data
        root = Element(rt.data[0]) # .split(None,1)
        expandnode(rt,root)
        h = ElementTree(root).write(self.xmlfn,encoding="iso-8859-1")

    def savexml(self,ev=None):
        if self.xmlfn == '':
            self.savexmlas()
        else:
            self.savexmlfile()

    def savexmlas(self,ev=None):
        h = gui.FileDialog.save(filename=self.xmlfn,wildcards={"XML files": "*.xml"})
        if h is not None:
            self.xmlfn = h
            self.savexmlfile()

    def about(self,ev=None):
        gui.Message.ok(self.title,"Made in 2008 by Albert Visser\nWritten in PythonCE and PocketPyGui")

    def quit(self,ev=None):
        self.destroy()

    def init_tree(self,name=''):
        def add_to_tree(el,rt):
            h = (el.tag,el.text)
            rr = rt.append(getshortname(h),h)
            for attr in el.keys():
                h = el.get(attr)
                if not h: h = '""'
                h = (attr,h)
                rr.append(getshortname(h,attr=True),h)
            for subel in list(el):
                add_to_tree(subel,rr)
        self.tree.delete_all()
        if name:
            self.top = self.tree.add_root(name)
        else:
            self.top = self.tree.add_root(self.xmlfn)
        h = (self.rt.tag,self.rt.text)
        rt = self.tree.add_root(getshortname(h),h)
        for el in list(self.rt):
            add_to_tree(el,rt)
        #self.tree.selection = self.top
        # set_selection()

    def on_bdown(self, ev=None):
        if gui.recon_context(self.tree, ev):
            self.item = self.tree.selection
            if self.item == self.top:
                gui.context_menu(self, ev, self.filemenu)
            elif self.item is not None:
                gui.context_menu(self, ev, self.editmenu)
            else:
                gui.Message.ok(self.title,'You need to select a tree item first')
                #menu.append()
        else:
            ev.skip()

    def checkselection(self):
        sel = True
        self.item = self.tree.selection
        if self.item is None or self.item == self.top:
            gui.Message.ok(self.title,'You need to select an element or attribute first')
        return sel

    def edit(self, ev=None):
        if DESKTOP and not self.checkselection():
            return
        data = self.item.get_text()
        if data.startswith('<>'):
            tag,text = self.item.get_data()
            data = {'item': self.item, 'tag': tag}
            if text is not None:
                data['data'] = True
                data['text'] = text
            edt = ElementDialog(title='Edit an element',item=data)
        else:
            nam,val = self.item.get_data()
            data = {'item': self.item, 'name': nam, 'value': val}
            edt = AttributeDialog(title='Edit an attribute',item=data)
        if edt.popup(self) == 'ok':
            node = self.data['item']
            if 'tag' in self.data:
                h = (self.data["tag"],self.data["text"])
            elif 'name' in self.data:
                h = (self.data["name"],self.data["value"])
            else:
                return
            node.set_text(getshortname(h))
            node.set_data(h)

    def cut(self, ev=None):
        self.copy(cut=True)

    def copy(self, ev=None, cut=False):
        if DESKTOP and not self.checkselection():
            return
        text = self.item.get_text()
        data = self.item.get_data()
        txt = 'cut' if cut else 'copy'
        if data == self.rt:
            gui.Message.ok(self.title,"Can't %s the root" % txt)
            return
        print text,data
        if text.startswith('<>'):
            self.cut_el = self.item
            self.cut_att = None
        else:
            self.cut_el = None
            self.cut_att = data
        if cut:
            self.item.remove()
        self.pastebeforeitem.set_text = "Paste Before"
        self.pastebeforeitem.enable(True)
        self.pasteafteritem.set_text = "Paste After"
        self.pasteafteritem.enable(True)

    def paste(self, ev=None,before=True):
        if DESKTOP and not self.checkselection():
            return
        data = self.item.get_data()
        pastebelow =  False
        if pastebelow and not self.item.get_text().starswith('<>'):
            gui.Message.ok(self.title,"Can't paste below an attribute")
            return
        if data == self.rt:
            if before:
                gui.Message.ok(self.title,"Can't paste before the root")
                return
            else:
                gui.Message.ok(self.title,"Pasting as first element below root")
                pastebelow = True
        if self.cut:
            self.pastebeforeitem.set_text = "Nothing to Paste"
            self.pastebeforeitem.enable(False)
            self.pasteafteritem.set_text = " "
            self.pasteafteritem.enable(False)
        print self.cut_el, self.cut_att
        if self.cut_att:
            item = getshortname(self.cut_att,attr=True)
            data = self.cut_att
            if pastebelow:
                node = self.item.append(item,data)
            else:
                add_to = self.item.get_parent()
                added = False
                for i,x in enumerate(add_to):
                    if x == self.item:
                        if not before:
                            i += 1
                        node = add_to.insert(i,item,data)
                        added = True
                        break
                if not added:
                    node = add_to.append(item,data)
        else:
            # I'd like to manipulate a complete treeitem (with subtree) here but I don't know how
            def zetzeronder(node,el,pos=-1):
                item = el.get_text()
                data = el.get_data()
                if pos == -1:
                    subnode = node.append(item,data)
                else:
                    subnode = node.insert(i,item,data)
                for x in el:
                    zetzeronder(subnode,x)
            if pastebelow:
                node = self.item
            else:
                node = self.item.get_parent()
                for i,x in enumerate(node):
                    if x == self.item:
                        if not before: i += 1
                        break
                if i > len(node): i = -1
            zetzeronder(node,self.cut_el,i)

    def paste_aft(self, ev=None):
        self.paste(before=False)

    def add_attr(self, ev=None):
        if DESKTOP and not self.checkselection():
            return
        edt = AttributeDialog("New attribute")
        if edt.popup(self) == 'ok':
            h = (self.data["name"],self.data["value"])
            self.item.append(getshortname(h,attr=True),h)

    def insert(self, ev=None,before=True,below=False):
        if DESKTOP and not self.checkselection():
            return
        current = self.item
        parent = self.item.get_parent()
        edt = ElementDialog("New element")
        if edt.popup(self) == 'ok':
            data = (self.data['tag'],self.data['text'])
            text = getshortname(data)
            if below:
                current.append(text,data)
            else:
                for i,x in enumerate(parent):
                    print i,x,x.get_text()
                    if x == self.item:
                        i = i if before else i+1
                        print i
                        parent.insert(i,text,data)
                        break

    def ins_aft(self, ev=None):
        self.insert(before=False)

    def ins_chld(self, ev=None):
        self.insert(below=True)

    def on_click(self, event):
       self.close()
if __name__ == '__main__':
    if len(sys.argv) > 1:        app = gui.Application(MainFrame(sys.argv[1]))
    else:        app = gui.Application(MainFrame())
    app.run()