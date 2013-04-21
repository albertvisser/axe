import os,sys,shutil
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
import tkinter.filedialog
import tkinter.simpledialog
from tkinter.ttk import Treeview as Tree
from xml.etree.ElementTree import Element, ElementTree, SubElement
cut_obj=None
cut_el = None
cut_att = None

if os.name == 'ce':
    DESKTOP = False
else:
    DESKTOP = True

## def hello():
    ## print "hello!"

def getshortname(x,attr=False):
    if attr:
        t = x[1]
        if t[-1] == "\n": t = t[:-1]
    else:
        t = x.text.split("\n",1)[0]
    ## print t
    w = 8
    if DESKTOP:
        w = 20
    if len(t) > w: t = t[:w].lstrip() + '...'
    if attr:
        return " = ".join((x[0],t))
    else:
        return ": ".join((x.tag,t))

def init_tree(master,root,name):
    master.tree.root.collapse()
    master.tree.data = root
    master.tree.root.set_label(root.tag)
    master.name = name
    master.tree.root.expand()
    master.tree.setmodified(False)

def bepaal_xmlnode(x): # bepaal de xml node bij een widget node
    name = x.get_label()
    h = x.widget.data
    ## print name,x.full_id(),h
    if len(x.full_id()) == 1:
        h = None
        ix = None
    else:
        for i in x.full_id()[1:-1]:
            h = list(h)[int(i)]
            ## print i,h
        ix = int(x.full_id()[-1]) - len(list(h.items()))
        ## if "=" in name: # attribuut: nog 1 nivo dieper
            ## h = list(h)[int(x.full_id()[-1])]
            ## ix = None
    return h,ix

class ElementDialog(tkinter.simpledialog.Dialog):
    def body(self,master):
        tag = ''
        txt = ''
        self.c1 = IntVar()
        self.c1.set(0)
        if self.parent.e12[0] is not None:
            tag = self.parent.e12[0]
        ## if len(self.parent.e12) > 1:
        if self.parent.e12[1] is not None:
            self.c1.set(1)
            txt = self.parent.e12[1]
        w2 = 25
        h2 = 4
        hfr = master
        if DESKTOP:
            w2 = 80
            h2 = 8
            hfr = Frame(master)
            hfr.pack()
        lb = Label(hfr, text="element name:")
        self.e1 = Entry(hfr,width=20)
        self.e1.insert(END,tag)
        if self.parent.e12[0] is not None:
            self.e1.config(state=DISABLED)
        self.cb = Checkbutton(hfr,text='Bevat data',variable = self.c1)
        if DESKTOP:
            lb.pack(side=LEFT)
            self.e1.pack(side=LEFT)
            self.cb.pack(side=LEFT)
        else:
            lb.pack()
            self.e1.pack()
            self.cb.pack()

        Label(master, text="text data:").pack()
        self.e2 = Text(master,width=w2,height=h2,wrap=WORD)
        self.e2.insert(END,txt)
        self.e2.pack()

        if self.parent.e12[0] is None:
            return self.e1
        else:
            return self.cb

    def apply(self):
        e1 = self.e1.get()
        e2 = self.e2.get(1.0,END)
        if self.c1.get():
            self.result = e1, e2[:-1]
        else:
            self.result = e1

class AttributeDialog(tkinter.simpledialog.Dialog):
    def body(self,master):
        nam,val = self.parent.e12
        w2 = 25
        h2 = 4
        hfr = master
        if DESKTOP:
            w2 = 80
            h2 = 8
            hfr = Frame(master)
            hfr.pack()
        lb = Label(hfr, text="attribute name:")
        self.e1 = Entry(hfr,width=20)
        if self.parent.e12[0] is not None:
            self.e1.insert(END,nam)
            self.e1.config(state=DISABLED)
        if DESKTOP:
            lb.pack(side=LEFT)
            self.e1.pack(side=LEFT)
        else:
            lb.pack()
            self.e1.pack()

        Label(master, text="attribute value:").pack()
        self.e2 = Text(master,width=w2,height=h2,wrap=WORD)
        if self.parent.e12[1] is not None:
            self.e2.insert(END,val)
        self.e2.pack()

        if self.parent.e12[0] is None:
            return self.e1
        else:
            return self.e2

    def apply(self):
        e1 = self.e1.get()
        e2 = self.e2.get(1.0,END)
        self.result = e1, e2[:-1]

class MyNodes(Tree.Node):
    def __init__(self, *args, **kw_args):
        # self.isElement = eljanee
        # call superclass
        Tree.Node.__init__(*(self,)+args, **kw_args)
        # bind right-click
        if DESKTOP:
            self.widget.tag_bind(self.symbol, '<3>', self.popup_menu)
            self.widget.tag_bind(self.label, '<Button-3>', self.popup_menu)
        else:
            self.widget.tag_bind(self.symbol, '<1>', self.popup_menu)
            self.widget.tag_bind(self.label, '<Button-1>', self.popup_menu)
        self.widget.tag_bind(self.label, '<Double-Button-1>', self.edit)

    # pop up menu on right click
    def popup_menu(self, event):
        menu = Menu(self.widget, tearoff=0)
        menu.add_command(label='Edit', command=self.edit)
        menu.add_command(label='Cut', command=self.cut)
        if cut_obj:
            if DESKTOP:
                pastemenu = Menu(self.widget,tearoff=False)
                menu.add_cascade(label="Paste",menu=pastemenu)
                pastemenu.add_command(label='Before', command=self.paste)
                pastemenu.add_command(label='After', command=self.paste_aft)
            else:
                menu.add_command(label='Paste Before', command=self.paste)
                menu.add_command(label='Paste After', command=self.paste_aft)
        else:
            menu.add_command(label='Paste', command=self.paste,
                             state='disabled')
        if DESKTOP:
            insertmenu = Menu(self.widget,tearoff=False)
            menu.add_cascade(label="Insert",menu=insertmenu)
            elmenu = Menu(self.widget,tearoff=False)
            insertmenu.add_cascade(label="Element",menu=elmenu)
            insertmenu.add_command(label="Attribute",command=self.add_attr)
            elmenu.add_command(label='Before', command=self.ins_bef)
            elmenu.add_command(label='After', command=self.ins_aft)
            elmenu.add_command(label='Under', command=self.ins_chld)
        else:
            menu.add_command(label="Insert Attribute",command=self.add_attr)
            menu.add_command(label='Insert Element Before', command=self.ins_bef)
            menu.add_command(label='Insert Element After', command=self.ins_aft)
            menu.add_command(label='Insert Element Under', command=self.ins_chld)
        menu.tk_popup(event.x_root, event.y_root)

    def edit(self,evt=None):
        # afhankelijk van item: element of attribute dialoog
        name = self.get_label()
        if len(self.full_id()) == 1:
            tkinter.messagebox.showwarning('Helaas...','root element kan niet aangepast worden')
            return
        if "=" in name:
            a = name.split(" = ",1)
            self.widget.e12 = (a[0],h.get(a[0]))
            d = AttributeDialog(self.widget)
            if d.result is not None:
                self.set_label(getshortname(d.result,attr=True))
                h,ix = bepaal_xmlnode(self)
                h.set(a[0],d.result[1])
                self.widget.data.parent.setmodified(True)
        else:
            h,ix = bepaal_xmlnode(self)
            h = list(h)[ix]
            self.widget.e12 = (h.tag,h.text)
            d = ElementDialog(self.widget)
            if d.result is not None:
                h.text = d.result[1]
                self.set_label(getshortname(h))
                self.widget.data.parent.setmodified(True)

    # cut'n'paste
    def cut(self):
        global cut_id, cut_name, cut_label, cut_expanded_icon, \
               cut_collapsed_icon, cut_expandable_flag, cut_obj, \
               cut_el, cut_att

        cut_obj=1
        cut_id=self.id
        cut_expanded_icon=self.expanded_icon
        cut_collapsed_icon=self.collapsed_icon
        cut_expandable_flag=self.expandable_flag
        cut_name=self.get_label()
        h,ix = bepaal_xmlnode(self) # zoek de node,
        ## print h,ix
        name = self.get_label()
        if " = " in name:
            cut_att = name.split(" = ",1)
            h.attrib.pop(cut_att[0])
        else:
            cut_el = list(h)[ix] # zet hem in een buffer en
            h.remove(cut_el)
        self.delete()
        self.widget.data.parent.setmodified(True)

    def paste_aft(self):
        self.paste(before=False)

    def paste(self,evt=None,before=True):
        global cut_el,cut_att
        if self == self.widget.root:
            self.insert_children(
                self.widget.add_list(name=cut_name,
                                     id=cut_id,
                                     flag=cut_expandable_flag,
                                     expanded_icon=cut_expanded_icon,
                                     collapsed_icon=cut_collapsed_icon))
            h = self.widget.data #           zoek de root en
            if cut_att is not None:
                h.set(cutt_att[0],cut_att[1])
            elif cut_el is not None:
                h.insert(0,cut_el) # doe een insert(0,buffer) zeg maar
            self.widget.data.parent.setmodified(True)
        elif before:
            self.insert_before(
                self.widget.add_list(name=cut_name,
                                     id=cut_id,
                                     flag=cut_expandable_flag,
                                     expanded_icon=cut_expanded_icon,
                                     collapsed_icon=cut_collapsed_icon))
            h,ix = bepaal_xmlnode(self) #     zoek de node index en
            if cut_att is not None:
                h.set(cut_att[0],cut_att[1])
            elif cut_el is not None:
                h.insert(ix - 1,cut_el)
            self.widget.data.parent.setmodified(True)
        else:
            self.insert_after(
                self.widget.add_list(name=cut_name,
                                     id=cut_id,
                                     flag=cut_expandable_flag,
                                     expanded_icon=cut_expanded_icon,
                                     collapsed_icon=cut_collapsed_icon))
            h,ix = bepaal_xmlnode(self) #     zoek de node index en
            if cut_att is not None:
                h.set(cut_att[0],cut_att[1])
            elif cut_el is not None:
                h.insert(ix,cut_el)
            self.widget.data.parent.setmodified(True)
        cut_att = None
        cut_el = None
        cut_obj=None

    def add_attr(self):
        self.widget.e12 = (None,None)
        d = AttributeDialog(self.widget)
        if d.result is not None:
            n=self.widget.add_list(name=' = '.join(d.result),
                                         id=99,
                                         flag=0,
                                         expanded_icon=self.expanded_icon,
                                         collapsed_icon=self.widget.regular_icon)
            if not self.expandable():
                self.expandable_flag = True
            self.insert_children(n) # ,d.result,elem=False)
            h,ix = bepaal_xmlnode(self) # zoek de node,
            h = list(h)[ix]
            h.set(d.result[0],d.result[1])
            self.widget.data.parent.setmodified(True)

    def ins_bef(self):
        self.widget.e12 = (None,None)
        d = ElementDialog(self.widget)
        if d.result is not None:
            n=self.widget.add_list(name=': '.join(d.result),
                                         id=99,
                                         flag=0,
                                         expanded_icon=self.expanded_icon,
                                         collapsed_icon=self.collapsed_icon)
            self.insert_before(n) # ,d.result)
            h,ix = bepaal_xmlnode(self) # zoek de node,
            e = Element(d.result[0])
            if len(d.result) > 1:
                e.text = d.result[1]
            h.insert(ix - 1,e)
            self.widget.data.parent.setmodified(True)

    def ins_aft(self):
        self.widget.e12 = (None,None)
        d = ElementDialog(self.widget)
        if d.result is not None:
            n=self.widget.add_list(name=': '.join(d.result),
                                         id=99,
                                         flag=0,
                                         expanded_icon=self.expanded_icon,
                                         collapsed_icon=self.collapsed_icon)
            self.insert_after(n) # ,d.result)
            h,ix = bepaal_xmlnode(self) # zoek de node,
            e = Element(d.result[0])
            if len(d.result) > 1:
                e.text = d.result[1]
            h.insert(ix,e)
            self.widget.data.parent.setmodified(True)

    def ins_chld(self):
        self.widget.e12 = (None,None)
        d = ElementDialog(self.widget)
        if d.result is not None:
            n=self.widget.add_list(name=': '.join(d.result),
                                         id=99,
                                         flag=0,
                                         expanded_icon=self.expanded_icon,
                                         collapsed_icon=self.collapsed_icon)
            if not self.expandable():
                self.expandable_flag = True
            self.insert_children(n) # ,d.result,elem=True)
            h,ix = bepaal_xmlnode(self) # zoek de node,
            h = list(h)[ix]
            e = Element(d.result[0])
            if len(d.result) > 1:
                e.text = d.result[1]
            h.insert(0,e)
            self.widget.data.parent.master.setmodified(True)

class XMLTree:
    def __init__(self, master, name, data):
        h0 = 202
        w0 = 218
        if DESKTOP:
            h0 = 600
            w0 = 500
        self.master = master
        frm = Frame(master,borderwidth=5,relief=RIDGE)
        frm.pack(fill=BOTH,expand=True)
        sby=Scrollbar(frm,orient=VERTICAL)
        sby.pack(side=RIGHT,fill=Y)
        sbx=Scrollbar(frm, orient=HORIZONTAL)
        sbx.pack(side=BOTTOM,fill=X)
        self.tree=Tree.Tree(frm,
                            height=h0,
                            width=w0,
                            background="white",
                            highlightthickness=0,
                            root_id="root",
                            root_label=data.tag,
                            node_class=MyNodes,
                            ## drop_callback=dnd_update,
                            get_contents_callback=self.getelems)
        self.tree.data = data
        self.tree.data.parent = self
        ## print self.tree.data
        self.tree.pack(expand=True,fill=BOTH)
        self.tree.name = name
        self.tree.configure(yscrollcommand=sby.set)
        sby.configure(command=self.tree.yview)
        self.tree.configure(xscrollcommand=sbx.set)
        sbx.configure(command=self.tree.xview)
        self.tree.root.expand()
        self.frm = frm

    def getelems(self,node):
        h = node.full_id()
        # zoek de huidige plek in de tree
        ## print h
        for x in h:
            if x == 'root':
                hier = self.tree.data
            else:
                i = int(x)
                hier = list(hier)[i]
        self.master.parent.currentitem = ("element",hier.tag, hier.text)
        ## self.master.parent.editmenu.entryconfig(self.master.parent.miEditElement,state=ACTIVE)
        ## self.master.parent.editmenu.entryconfig(self.master.parent.miEditAttribute,state=DISABLED)
        for x in enumerate(list(hier.keys())):
            naam = getshortname((x[1],hier.get(x[1])),attr=True)
            idee = str(x[0])
            node.widget.add_node(name=naam,id=idee,flag=0)
        for x in enumerate(list(hier)):
            if x[1].text is None:
                naam = x[1].tag
            else:
                naam = getshortname(x[1])
            idee = str(x[0] + len(list(hier.keys())))
            if len(list(x[1])) > 0 or len(list(x[1].keys())) > 0:
                node.widget.add_node(name=naam,id=idee,flag=1)
            else:
                node.widget.add_node(name=naam,id=idee,flag=0,
                collapsed_icon=node.widget.collapsed_icon)

    def setmodified(self,value):
        self.ismodified = value
        if value:
            self.master.parent.filemenu.entryconfig(self.master.parent.miSave,state=ACTIVE)
        else:
            self.master.parent.filemenu.entryconfig(self.master.parent.miSave,state=DISABLED)

class MainFrame:
    def __init__(self, master,fn):
        self.master = master
        self.xmlfn = fn
        self.frame = Frame(master) # , width=224, height=208, bd=1
        self.frame.parent = self
        self.frame.pack(expand=True,fill=BOTH)
        self.mbar = Frame(self.frame)
        self.mbar.pack(fill=X)

        # Create File menu
        self.filebutton = Menubutton(self.mbar, text = 'File', padx=3, pady=2)
        self.filebutton.pack(side = LEFT)
        self.filemenu = Menu(self.filebutton, tearoff=0)
        self.filebutton['menu'] = self.filemenu
        # Populate File menu
        self.filemenu.add('command', label = 'New', command = self.newxml)
        self.filemenu.add('command', label = 'Open', command = self.openxml)
        # deze optie uitgrijzen als er geen file geladen of opgebouwd  is of het is niet gewijzigd:
        self.miSave = 2
        self.filemenu.add('command', label = 'Save', command = self.savexml)
        self.filemenu.entryconfig(self.miSave,state=DISABLED)
        # deze optie uitgrijzen als er geen file geladen of opgebouwd is
        self.miSaveAs = 3
        self.filemenu.add('command', label = 'Save As', command = self.savexmlas)
        self.filemenu.entryconfig(self.miSaveAs,state=DISABLED)
        # deze optie actief maken als er een dtd gemaakt of gewijzigd is
        ## self.miSaveDTD = 4
        ## self.filemenu.add('command', label = 'Save DTD', command = self.stub)
        ## self.filemenu.entryconfig(self.miSaveDTD,state=DISABLED)
        self.filemenu.add('command', label = 'Exit', command = self.quit)

        # Create  help menu
        self.helpbutton = Menubutton(self.mbar, text = 'Help',padx=2,pady=2)
        self.helpbutton.pack(side = RIGHT)
        self.helpmenu = Menu(self.helpbutton, tearoff=0)
        self.helpbutton['menu'] = self.helpmenu
        # Populate help menu
        self.helpmenu.add('command', label = 'About', command = self.stub)

        if self.xmlfn == '':
            rt = Element('New')
            h = tkinter.filedialog.askopenfilename(filetypes=[("XML files","*.xml")])
            if h != "": # is not None:
                try:
                    rt = ElementTree(file=h).getroot()
                except:
                    h = tkinter.messagebox.showwarning('eh...','geen well-formed xml')
                    rt = Element('New')
                else:
                    self.xmlfn = h
            ## self.openxml()
        else:
            rt = ElementTree(file=self.xmlfn).getroot()
        self.t1 = XMLTree(self.frame, self.xmlfn, rt)
        self.filemenu.entryconfig(self.miSaveAs,state=ACTIVE)

    def quit(self):
        self.master.destroy()

    def stub(self):
        pass

    def newxml(self):
        # vraag naar naam voor root element
        h = tkinter.simpledialog.askstring("AXE", "Geef naam (tag) voor het root element op")
        if h is not None:
            init_tree(self.t1,Element(h),"(untitled)")
            self.master.filemenu.entryconfig(self.miSaveAs,state=ACTIVE)

    def openxml(self):
        h = tkinter.filedialog.askopenfilename(filetypes=[("XML files","*.xml")])
        if h is not None:
            ## print h
            try:
                rt = ElementTree(file=h).getroot()
            except:
                h = tkinter.messagebox('eh...','parsing ging fout')
            else:
                init_tree(self.t1,rt,h)
                self.xmlfn = h
                self.master.filemenu.entryconfig(self.miSaveAs,state=ACTIVE)

    def savexmlfile(self):
        print(self.xmlfn)
        try:
            shutil.copyfile(self.xmlfn,self.xmlfn + '.bak')
        except IOError as mld:
            print(mld)
        h = ElementTree(self.t1.tree.data).write(self.xmlfn,encoding="iso-8859-1")

    def savexml(self):
        if self.xmlfn == '':
            self.savexmlas()
        else:
            self.savexmlfile()

    def savexmlas(self):
        h = tkinter.filedialog.asksaveasfilename(filetypes=[("XML files","*.xml")],
            defaultextension=".xml")
        if h is not None:
            self.xmlfn = h
            self.savexmlfile()

    def editelement(self):
        self.master.eltag = self.currentitem[1] # 'root'
        ## self.master.currentitem[1] = ("element",hier.tag, hier.text)
        self.master.eltxt = ''
        if  self.currentitem[2] is not None:
            self.master.eltxt = self.currentitem[2] # ''
        d1 = ElementDialog(self.master)

    def editattribute(self):
        self.master.attnam = 'id'
        self.master.attval = '446852'
        d2 = AttributeDialog(self.master)

def main(inv):
    root = Tk()
    fn = ''
    if len(inv) > 1:
        fn = inv[1]
    h = MainFrame(root,fn)
    root.title("Albert's XML-editor")
    root.mainloop()

if __name__ == "__main__":
    ## print sys.argv
    main(sys.argv)
