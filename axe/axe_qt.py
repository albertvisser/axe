# -*- coding: utf-8 -*-

"PyQT versie van een op een treeview gebaseerde XML-editor"
import logging
logging.basicConfig(filename='axe_qt.log', level=logging.DEBUG,
    format='%(asctime)s %(message)s')

import os
import sys
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
from .axe_base import getshortname, XMLTree, AxeMixin
from .axe_base import ELSTART, TITEL, axe_iconame
if os.name == "nt":
    HMASK = "XML files (*.xml);;All files (*.*)"
elif os.name == "posix":
    HMASK = "XML files (*.xml *.XML);;All files (*.*)"
IMASK = "All files (*.*)"

def add_as_child(element, root, attr=False, insert=-1):
    if element[1] is None:
        element = (element[0], "")
    h = (str(element[0]), str(element[1]))
    item = gui.QTreeWidgetItem()
    item.setText(0, getshortname(h, attr))
    item.setText(1, element[0])
    item.setText(2, element[1])
    if insert == -1:
        root.addChild(item)
    else:
        root.insertChild(insert, item)
    return item

class ElementDialog(gui.QDialog):
    def __init__(self, parent, title="", item=None):
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        self.setWindowIcon(parent._icon)
        self._parent = parent
        lbl_name = gui.QLabel("element name:  ", self)
        self.txt_tag = gui.QLineEdit(self)
        self.cb = gui.QCheckBox('Bevat data:', self)
        ## lbl_data = gui.QLabel("text data:", self)
        self.txt_data = gui.QTextEdit(self)
        self.txt_data.setTabChangesFocus(True)
        ## self.txt_data.Bind(wx.EVT_KEY_UP,self.on_keyup)
        self.btn_ok = gui.QPushButton('&Save', self)
        self.connect(self.btn_ok, core.SIGNAL('clicked()'), self.on_ok)
        self.btn_ok.setDefault(True)
        self.btn_cancel = gui.QPushButton('&Cancel', self)
        self.connect(self.btn_cancel, core.SIGNAL('clicked()'), self.on_cancel)

        tag = txt = ''
        if item:
            tag = item["tag"]
            if "text" in item:
                self.cb.toggle()
                txt = item["text"]
        self.txt_tag.setText(tag)
        self.txt_data.setText(txt)

        sizer = gui.QVBoxLayout()
        ## hsizer = gui.QHBoxLayout()
        hsizer2 = gui.QHBoxLayout()
        hsizer2.addWidget(lbl_name)
        hsizer2.addWidget(self.txt_tag)
        ## hsizer.Add(hsizer2, 0, wx.EXPAND | wx.ALL, 5)
        ## sizer.Add(hsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP,  5)
        sizer.addLayout(hsizer2)

        hsizer = gui.QHBoxLayout()
        vsizer = gui.QVBoxLayout()
        vsizer.addWidget(self.cb)
        vsizer.addWidget(self.txt_data)
        hsizer.addLayout(vsizer)
        sizer.addLayout(hsizer)

        hsizer = gui.QHBoxLayout()
        hsizer.addWidget(self.btn_ok)
        hsizer.addWidget(self.btn_cancel)
        sizer.addLayout(hsizer)

        self.setLayout(sizer)
        ## self.resize(400, 270)

    def on_cancel(self):
        gui.QDialog.done(self, gui.QDialog.Rejected)

    def on_ok(self):
        self._parent.data = {}
        tag = str(self.txt_tag.text())
        if tag == '' or len(tag.split()) > 1:
            gui.QMessageBox.critical(self, self._parent.title,
            'Element name cannot be empty or contain spaces')
            return
        self._parent.data["tag"] = tag
        self._parent.data["data"] = self.cb.isChecked()
        self._parent.data["text"] = self.txt_data.toPlainText()
        gui.QDialog.done(self, gui.QDialog.Accepted)

    ## def on_keyup(self,ev):
        ## ky = ev.GetKeyCode()
        ## mod = ev.GetModifiers()
        ## if ky == 65 and mod == wx.MOD_CONTROL:
            ## win = ev.GetEventObject()
            ## if win in (self.txt_tag, self.txt_data):
                ## win.SelectAll()
    def keyPressEvent(self, event):
        """event handler voor toetsaanslagen"""
        if event.key() == core.Qt.Key_Escape:
            gui.QDialog.done(self, gui.QDialog.Rejected)

class AttributeDialog(gui.QDialog):
    def __init__(self, parent, title='', item=None):
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        self.setWindowIcon(parent._icon)
        self._parent = parent
        lbl_name = gui.QLabel("Attribute name:", self)
        self.txt_name = gui.QLineEdit(self)
        lbl_value = gui.QLabel("Attribute value:", self)
        self.txt_value = gui.QLineEdit(self)
        self.btn_ok = gui.QPushButton('&Save', self)
        self.btn_ok.setDefault(True)
        self.connect(self.btn_ok, core.SIGNAL('clicked()'), self.on_ok)
        self.btn_cancel = gui.QPushButton('&Cancel', self)
        self.connect(self.btn_cancel, core.SIGNAL('clicked()'), self.on_cancel)

        nam = val = ''
        if item:
            nam, val = item["name"], item["value"]
        self.txt_name.setText(nam)
        self.txt_value.setText(val)

        sizer = gui.QVBoxLayout()
        hsizer = gui.QHBoxLayout()
        hsizer.addWidget(lbl_name)
        hsizer.addWidget(self.txt_name)
        sizer.addLayout(hsizer)
        hsizer = gui.QHBoxLayout()
        hsizer.addWidget(lbl_value)
        hsizer.addWidget(self.txt_value)
        sizer.addLayout(hsizer)
        hsizer = gui.QHBoxLayout()
        hsizer.addWidget(self.btn_ok)
        hsizer.addWidget(self.btn_cancel)
        sizer.addLayout(hsizer)

        self.setLayout(sizer)
        ## self.resize(320,125)

    def on_ok(self):
        self._parent.data = {}
        nam = self.txt_name.text()
        if nam == '':
            gui.QMessageBox.critical(self, self._parent.title,
                'Attribute name cannot be empty or spaces')
            return
        self._parent.data["name"] = nam
        self._parent.data["value"] = self.txt_value.text()
        gui.QDialog.done(self, gui.QDialog.Accepted)

    def on_cancel(self):
        gui.QDialog.done(self, gui.QDialog.Rejected)

    ## def on_keyup(self,ev):
        ## ky = ev.GetKeyCode()
        ## mod = ev.GetModifiers()
        ## if ky == 65 and mod == wx.MOD_CONTROL:
            ## win = ev.GetEventObject()
            ## if win in (self.txt_name, self.txt_value):
                ## win.SelectAll()
    def keyPressEvent(self, event):
        """event handler voor toetsaanslagen"""
        if event.key() == core.Qt.Key_Escape:
            gui.QDialog.done(self, gui.QDialog.Rejected)

class VisualTree(gui.QTreeWidget):
    def __init__(self, parent):
        self.parent = parent
        gui.QTreeWidget.__init__(self)

    def mouseDoubleClickEvent(self, event):
        item = self.itemAt(event.x(), event.y())
        if item:
            if item == self.parent.top:
                edit = False
            else:
                data = str(item.text(0))
                edit = True
                ## if data.startswith(ELSTART):
                    ## if item.childCount() > 0:
                        ## edit = False
        if edit:
            self.parent.edit()
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        if event.button() == core.Qt.RightButton:
            xc, yc = event.x(), event.y()
            item = self.itemAt(xc, yc)
            if item and item != self.parent.top:
                ## self.parent.setCurrentItem(item)
                menu = self.parent.init_menus(popup=True)
                menu.exec_(core.QPoint(xc, yc))
            else:
                event.ignore()
        else:
            event.ignore()


class MainFrame(gui.QMainWindow, AxeMixin):
    "Main GUI class"
    def __init__(self, parent, id, fn=''):
        AxeMixin.__init__(self, parent, id, fn)
        self.show()

    def _init_gui(self, parent, id):
        self.parent = parent
        gui.QMainWindow.__init__(self) # , parent, id, pos=(2, 2), size=(620, 900))
        self._icon = gui.QIcon(axe_iconame)
        self.resize(620, 900)
        self.setWindowIcon(self._icon)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        ## menubar = self.menuBar()
        ## menu = menubar.addMenu('&File')
        ## act = gui.QAction('E&xit', self)
        ## self.connect(act, core.SIGNAL('triggered()'), self.quit)
        ## menu.addAction(act)

        ## filemenu, viewmenu, editmenu =
        self.init_menus()
        ## x = menubar.addMenu(filemenu)
        ## y = menubar.addMenu(viewmenu)
        ## z = menubar.addMenu(editmenu)
        self.enable_pasteitems(False)
        ## menubar.setVisible(True)

        self.tree = VisualTree(self)
        self.tree.setItemHidden(self.tree.headerItem(), True)
        ## self.connect(self.tree, QtCore.SIGNAL("self.tree.keyReleaseEvent()"), self.on_keyup)
        ## self.tree.mouseReleaseEvent.connect(self.on_rightdown)
        ## self.tree.keyReleaseEvent.connect(self.on_keyup)        self.setCentralWidget(self.tree)

        self.mark_dirty(False)

    def keyReleaseEvent(self, event):
        skip = self.on_keyup(event)
        if not skip:
            gui.QMainWindow.keyPressEvent(self, event)

    def closeEvent(self, event):
        """applicatie afsluiten"""
        self.afsl()

    def init_menus(self, popup=False):
        if not popup:
            self.filemenu_actions, self.viewmenu_actions, self.editmenu_actions = [], [], []
            for ix, menudata in enumerate((
                    (
                        ("&New", self.newxml, 'Ctrl+N'),
                        ("&Open", self.openxml, 'Ctrl+O'),
                        ('&Save', self.savexml, 'Ctrl+S'),
                        ('Save &As', self.savexmlas, 'Shift+Ctrl+S'),
                        ('E&xit', self.quit, 'Ctrl+Q'),
                    ),
                    (
                        ("&Expand All (sub)Levels", self.expand, 'Ctrl++'),
                        ("&Collapse All (sub)Levels", self.collapse, 'Ctrl+-'),
                    ),
                    (
                        ("&Edit", self.edit, 'Ctrl-E,F2'),
                        ("&Delete", self.delete, 'Ctrl-D,Delete'),
                        ("C&ut", self.cut, 'Ctrl+X'),
                        ("&Copy", self.copy, 'Ctrl+C'),
                        ("Paste Before", self.paste, 'Shift+Ctrl+V'),
                        ("Paste After", self.paste_aft, 'Ctrl+V'),
                        ("Paste Under", self.paste_und, 'Alt+Ctrl+V'),
                        ("Insert Attribute", self.add_attr, 'Shift+Insert'),
                        ('Insert Element Before', self.insert, 'Ctrl+Insert'),
                        ('Insert Element After', self.ins_aft, 'Alt+Insert'),
                        ('Insert Element Under', self.ins_chld, 'Insert'),
                    ))):
                for text, callback, shortcuts in menudata:
                    act = gui.QAction(text, self)
                    self.connect(act, core.SIGNAL('triggered()'), callback)
                    act.setShortcuts([x for x in shortcuts.split(',')])
                    if ix == 0:
                        self.filemenu_actions.append(act)
                    elif ix == 1:
                        self.viewmenu_actions.append(act)
                    elif ix == 2:
                        self.editmenu_actions.append(act)
            self.pastebefore_item, self.pasteafter_item, \
                self.pasteunder_item = self.editmenu_actions[4:7]

            menubar = self.menuBar()
            filemenu = menubar.addMenu("&File")
            for act in self.filemenu_actions[:4]:
                filemenu.addAction(act)
            filemenu.addSeparator()
            filemenu.addAction(self.filemenu_actions[-1])
        if popup:
            viewmenu = gui.QMenu("&View")
        else:
            viewmenu = menubar.addMenu("&View")
        for act in self.viewmenu_actions:
            viewmenu.addAction(act)

        if popup:
            editmenu = viewmenu
            editmenu.setTitle("View/Edit")
            editmenu.addSeparator()
        else:
            editmenu = menubar.addMenu("&Edit")

        editmenu.addAction(self.editmenu_actions[0])
        editmenu.addSeparator()
        for act in self.editmenu_actions[1:4]:
            editmenu.addAction(act)

        disable_menu = True if not self.cut_el and not self.cut_att else False
        add_menuitem = True if not popup or not disable_menu else False
        if disable_menu:
            self.pastebefore_item.setText("Nothing to Paste")
            self.pastebefore_item.setEnabled(False)
            self.pasteafter_item.setEnabled(False)
            self.pasteunder_item.setEnabled(False)
        if add_menuitem:
            editmenu.addAction(self.pastebefore_item)
            editmenu.addAction(self.pasteafter_item)
            editmenu.addAction(self.pasteunder_item)

        editmenu.addSeparator()
        for act in self.editmenu_actions[7:]:
            editmenu.addAction(act)

        if popup:
            return editmenu
        ## else:
            ## return filemenu, viewmenu, editmenu

    def enable_pasteitems(self, active=False):
        """activeert of deactiveert de paste-entries in het menu
        afhankelijk van of er iets te pASTEN VALT
        """
        if active:
            self.pastebefore_item.setText("Paste Before")
        else:
            self.pastebefore_item.setText("Nothing to Paste")
        self.pastebefore_item.setEnabled(active)
        self.pasteafter_item.setEnabled(active)
        self.pasteunder_item.setEnabled(active)

    def mark_dirty(self, state):
        data = AxeMixin.mark_dirty(self, state, str(self.windowTitle()))
        if data:
            self.setWindowTitle(data)

    def _ask_yesnocancel(self, prompt):
        """stelt een vraag en retourneert het antwoord
        1 = Yes, 0 = No, -1 = Cancel
        """
        retval = dict(zip((gui.QMessageBox.Yes, gui.QMessageBox.No,
            gui.QMessageBox.Cancel), (1, 0, -1)))
        h = gui.QMessageBox.question(self, self.title, prompt,
            gui.QMessageBox.Yes | gui.QMessageBox.No | gui.QMessageBox.Cancel,
            defaultButton = gui.QMessageBox.Yes)
        return h

    def newxml(self, ev=None):
        AxeMixin.newxml(self)

    def _ask_for_text(self, prompt):
        """vraagt om tekst en retourneert het antwoord"""
        data, ok = gui.QInputDialog.getText(self, self.title, prompt,
            gui.QLineEdit.Normal, "")
        return data

    def openxml(self, ev=None):
        AxeMixin.openxml(self)

    def _file_to_read(self):
        fnaam = gui.QFileDialog.getOpenFileName(self, "Choose a file", os.getcwd(),
            HMASK)
        ok = bool(fnaam)
        return ok, str(fnaam)

    def _meldinfo(self, text):
        gui.QMessageBox.information(self, self.title, text)

    def _meldfout(self, text, abort=False):
        gui.QMessageBox.critical(self, self.title, text)
        if abort:
            self.quit()

    def savexml(self, ev=None):
        AxeMixin.savexml(self)

    def savexmlfile(self, oldfile=''):      # TODO
        def expandnode(rt, root, tree):
            for ix in range(rt.childCount()):
                tag = rt.child(ix)
                text = str(tag.text(0))
                data = (str(tag.text(1)), str(tag.text(2)))
                node = tree.expand(root, text, data)
                if node is not None:
                    expandnode(tag, node, tree)
        AxeMixin.savexmlfile(self, oldfile)
        top = self.tree.topLevelItem(0)
        rt = top.child(0)
        text = str(rt.text(0))
        data = (str(rt.text(1)), str(rt.text(2)))
        tree = XMLTree(data[0]) # .split(None,1)
        root = tree.root
        expandnode(rt, root, tree)
        h = tree.write(self.xmlfn)
        self.mark_dirty(False)

    def savexmlas(self, ev=None):
        ok = AxeMixin.savexmlas(self)
        if ok:
            self.top.SetText(0, self.xmlfn)
            self.setWindowTitle(" - ".join((os.path.basename(self.xmlfn), TITEL)))

    def _file_to_save(self, dirname, filename):
        name = gui.QFileDialog.getSaveFileName(self, "Save file as ...", dirname,
            HMASK)
        ok = bool(name)
        return ok, str(name)

    def about(self, ev=None):
        AxeMixin.about(self)

    def quit(self, ev=None):
        self.close()

    def afsl(self, ev=None):
        if self.check_tree():
            if ev:
                ev.accept()
        else:
            if ev:
                ev.ignore()

    def init_tree(self, name=''):
        def add_to_tree(el, rt):
            rr = add_as_child((el.tag, el.text), rt)
            ## h = (el.tag, el.text)
            ## rr = gui.QTreeWidgetItem()
            ## rr.setText(0, getshortname(h))
            ## rr.setData(0, core.Qt.UserRole, h)
            ## rt.addChild(rr)
            for attr in el.keys():
                h = el.get(attr)
                if not h:
                    h = '""'
                rrr = add_as_child((attr, h), rr, attr=True)
                ## h = (attr, h)
                ## rrr = gui.QTreeWidgetItem()
                ## rrr.setText(0, getshortname(h, attr=True))
                ## rrr.setData(0, core.Qt.UserRole, h)
                ## rr.addChild(rrr)
            for subel in list(el):
                add_to_tree(subel, rr)

        self.tree.clear() # DeleteAllItems()
        titel = AxeMixin.init_tree(self, name)
        self.top = gui.QTreeWidgetItem()
        self.top.setText(0, titel)
        self.tree.addTopLevelItem(self.top) # AddRoot(titel)
        self.setWindowTitle(" - ".join((os.path.split(titel)[-1],TITEL)))
        rt = add_as_child((self.rt.tag, self.rt.text), self.top)
        ## h = (self.rt.tag,self.rt.text)
        ## rt = self.tree.AppendItem(self.top,getshortname(h))
        ## self.tree.SetItemPyData(rt,h)
        for el in list(self.rt):
            add_to_tree(el, rt)
        #self.tree.selection = self.top
        # set_selection()
        self.mark_dirty(False)

    def on_keyup(self, ev=None):
        ky = ev.key()
        item = self.tree.currentItem()
        skip = False
        if item and item != self.top:
            if ky == core.Qt.Key_Return:
                if item.childCount > 0:
                    if self.tree.isItemExpanded(item):
                        self.tree.collapseItem(item)
                        self.tree.setCurrentItem(item.parent())
                    else:
                        self.tree.expandItem(item)
                        self.tree.setCurrentItem(item.child(0))
                else:
                    self.edit()
                skip = True
            elif ky == core.Qt.Key_Backspace:
                if self.tree.isItemExpanded(item):
                    self.tree.collapseItem(item)
                    self.tree.setCurrentItem(item.parent())
                skip = True
        return skip

    def checkselection(self):
        sel = True
        self.item = self.tree.currentItem()
        if self.item is None or self.item == self.top:
            gui.QMessageBox.information(self, self.title,
                'You need to select an element or attribute first')
        return sel

    def expand(self, ev=None):
        def expand_with_children(item):
            self.tree.expandItem(item)
            for ix in range(item.childCount()):
                expand_with_children(item.child(ix))
        item = self.tree.currentItem()
        if item:
            expand_with_children(item)      # TODO: moet recursief

    def collapse(self,ev=None):
        item = self.tree.currentItem()
        if item:
            self.tree.collapseItem(item)    # mag eventueel recursief in overeenstemming met vorige

    def edit(self, ev=None):
        if not self.checkselection():
            return
        data = str(self.item.text(0)) # self.item.get_text()
        if data.startswith(ELSTART):
            tag, text = str(self.item.text(1)), str(self.item.text(2))
            data = {'item': self.item, 'tag': tag}
            if text:
                data['data'] = True
                data['text'] = text
            edt = ElementDialog(self, title='Edit an element', item=data).exec_()
            if edt == gui.QDialog.Accepted:
                h = (self.data["tag"], self.data["text"])
                self.item.setText(0, getshortname(h))
                self.item.setText(1, self.data["tag"])
                self.item.setText(2, self.data["text"])
                self.mark_dirty(True)
        else:
            nam, val = str(self.item.text(1)), str(self.item.text(2))
            data = {'item': self.item, 'name': nam, 'value': val}
            edt = AttributeDialog(self,title='Edit an attribute',item=data).exec_()
            if edt == gui.QDialog.Accepted:
                h = (self.data["name"], self.data["value"])
                self.item.setText(0, getshortname(h, attr=True))
                self.item.setText(1, self.data["name"])
                self.item.setText(2, self.data["value"])
                self.mark_dirty(True)

    def cut(self, ev=None):
        AxeMixin.cut(self)

    def delete(self, ev=None):
        AxeMixin.delete(self)

    def copy(self, ev=None, cut=False, retain=True):
        def push_el(el, result):
            text = str(el.text(0))
            data = (str(el.text(1)), str(el.text(2)))
            children = []
            if str(text).startswith(ELSTART):
                for ix in range(el.childCount()):
                    subel = el.child(ix)
                    temp = push_el(subel, children)
            result.append((text, data, children))
            return result
        if not self.checkselection():
            return
        txt = AxeMixin.copy(self, cut, retain)
        text = str(self.item.text(0))
        data = (str(self.item.text(1)), str(self.item.text(2)))
        if data == (self.rt.tag, self.rt.text or ""):
            self._meldfout("Can't %s the root" % txt)
            return
        if retain:
            if str(text).startswith(ELSTART):
                self.cut_el = []
                self.cut_el = push_el(self.item, self.cut_el)
                self.cut_att = None
            else:
                self.cut_el = None
                self.cut_att = data
            self.enable_pasteitems(True)
        if cut:
            parent = self.item.parent()
            ix = parent.indexOfChild(self.item)
            if ix > 0:
                ix -= 1
                prev = parent.child(ix)
            else:
                prev = parent
                if prev == self.rt:
                    prev = parent.child(ix+1)
            parent.removeChild(self.item)
            self.mark_dirty(True)
            self.tree.setCurrentItem(prev)

    def paste_aft(self, ev=None):
        AxeMixin.paste_aft(self)

    def paste_und(self, ev=None):
        AxeMixin.paste_und(self)

    def paste(self, ev=None, before=True, pastebelow=False):
        if not self.checkselection():
            return
        data = (str(self.item.text(1)), str(self.item.text(2)))
        if pastebelow and not str(self.item.text(0)).startswith(ELSTART):
            gui.QMessageBox.critical("Can't paste below an attribute", self.title)
            return
        if data == (self.rt.tag, self.rt.text or ""):
            if before:
                gui.QMessageBox.critical("Can't paste before the root", self.title)
                return
            else:
                gui.QMessageBox.information("Pasting as first element below root",
                    self.title)
                pastebelow = True
        ## if self.cut:
            ## self.enable_pasteitems(False)
        if self.cut_att:
            item = getshortname(self.cut_att, attr=True)
            node = gui.QTreeWidgetItem()
            node.setText(0, item)
            node.setText(1, self.cut_att[0])
            node.setText(2, self.cut_att[1])
            if pastebelow:
                self.item.addChild(node)
            else:
                add_to = self.item.parent() # self.item.get_parent()
                added = False
                for ix in range(add_to.childCount()):
                    if add_to.child(ix) == self.item:
                        if not before:
                            ix += 1
                        add_to.insertChild(ix, node)
                        added = True
                        break
                if not added:
                    add_to.addChild(item)
        elif self.cut_el:
            def zetzeronder(node, el, pos=-1):
                subnode = gui.QTreeWidgetItem()
                subnode.setText(0, el[0])
                subnode.setText(1, el[1][0])
                subnode.setText(2, el[1][1])
                if pos == -1:
                    node.addChild(subnode)
                else:
                    node.insertChild(pos, subnode)
                for x in el[2]:
                    zetzeronder(subnode, x)
            if pastebelow:
                node = self.item
                ix = -1
            else:
                node = self.item.parent()
                cnt = node.childCount()
                for ix in range(cnt):
                    x = node.child(ix)
                    if x == self.item:
                        if not before:
                            ix += 1
                        break
                if ix == cnt:
                    ix = -1
            zetzeronder(node, self.cut_el[0], ix)
        self.mark_dirty(True)

    def add_attr(self, ev=None):
        if not self.checkselection():
            return
        edt = AttributeDialog(self, title="New attribute").exec_()
        if edt == gui.QDialog.Accepted:
            if str(self.item.text(0)).startswith(ELSTART):
                h = (self.data["name"], self.data["value"])
                rt = add_as_child(h, self.item, attr=True)
                ## rt = gui.QTreeWidgetItem()
                ## rt.setText(0, getshortname(h, attr=True))
                ## rt.setData(0, core.Qt.UserRole, h)
                ## self.item.addChild(rt)
                self.mark_dirty(True)
            else:
                self._meldfout("Can't add attribute to attribute")

    def ins_aft(self, ev=None):
        AxeMixin.ins_aft(self)

    def ins_chld(self, ev=None):
        AxeMixin.ins_chld(self)

    def insert(self, ev=None, before=True, below=False):
        if not self.checkselection():
            return
        edt = ElementDialog(self, title="New element").exec_()
        if edt == gui.QDialog.Accepted:
            data = (self.data['tag'], self.data['text'])
            if below:
                add_under = self.item
                ix = -1
            else:
                add_under = self.item.parent()
                ix = add_under.indexOfChild(self.item)
                if not before:
                    ix += 1
            rt = add_as_child(data, add_under, insert=ix)
            ## rt = gui.QTreeWidgetItem(getshortname(data))
            ## rt.setData(0, data)
            ## if below:
                ## x = self.item.addChild(rt)
            ## else:
                ## parent = self.item.parent()
                ## ix = parent.indexOfChild(self.item)
                ## if not before:
                    ## ix += 1
                ## y = parent.insertChild(ix, rt)
            self.mark_dirty(True)

def axe_gui(args):
    app = gui.QApplication(sys.argv)
    if len(args) > 1:
        frm = MainFrame(None, -1, fn=" ".join(args[1:]))
    else:
        frm = MainFrame(None, -1)
    sys.exit(app.exec_())

if __name__ == "__main__":
    axe_gui(sys.argv)
