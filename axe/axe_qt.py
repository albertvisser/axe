# -*- coding: utf-8 -*-

"PyQT versie van een op een treeview gebaseerde XML-editor"
import os
import logging
try:
    logging.basicConfig(filename='axe_qt.log', level=logging.DEBUG,
        format='%(asctime)s %(message)s')
except PermissionError:
    logging.basicConfig(filename=os.path.join(os.path.dirname(__file__),
        'axe_qt.log'), level=logging.DEBUG, format='%(asctime)s %(message)s')


import os
import sys
import functools
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
from .axe_base import getshortname, find_next, XMLTree, AxeMixin
from .axe_base import ELSTART, TITEL, axe_iconame
if os.name == "nt":
    HMASK = "XML files (*.xml);;All files (*.*)"
elif os.name == "posix":
    HMASK = "XML files (*.xml *.XML);;All files (*.*)"
IMASK = "All files (*.*)"

def add_as_child(element, root, ns_prefixes, ns_uris, attr=False, insert=-1):
    if element[1] is None:
        element = (element[0], "")
    h = ((str(element[0]), str(element[1])), ns_prefixes, ns_uris)
    item = gui.QTreeWidgetItem()
    item.setText(0, getshortname(h, attr))
    item.setText(1, element[0])
    item.setText(2, element[1])
    if insert == -1:
        root.addChild(item)
    else:
        root.insertChild(insert, item)
    return item

def flatten_tree(element):
    """return the tree's structure as a flat list
    probably nicer as a generator function
    """
    attr_list = []
    elem_list = [(element, str(element.text(1)), str(element.text(2)), attr_list)]

    subel_list = []
    for seq in range(element.childCount()):
        subitem = element.child(seq)
        if str(subitem.text(0)).startswith(ELSTART):
            subel_list = flatten_tree(subitem)
            elem_list.extend(subel_list)
        else:
            attr_list.append((subitem, str(subitem.text(1)), str(subitem.text(2))))
    return elem_list

class ElementDialog(gui.QDialog):
    def __init__(self, parent, title="", item=None):
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        self.setWindowIcon(parent._icon)
        self._parent = parent
        lbl_name = gui.QLabel("element name:  ", self)
        self.txt_tag = gui.QLineEdit(self)

        self.cb_ns = gui.QCheckBox('Namespace:', self)
        self.cmb_ns = gui.QComboBox(self)
        self.cmb_ns.setEditable(False)
        self.cmb_ns.addItem('-- none --')
        self.cmb_ns.addItems(self._parent.ns_uris)

        self.cb = gui.QCheckBox('Bevat data:', self)
        self.txt_data = gui.QTextEdit(self)
        self.txt_data.setTabChangesFocus(True)
        self.btn_ok = gui.QPushButton('&Save', self)
        self.connect(self.btn_ok, core.SIGNAL('clicked()'), self.on_ok)
        self.btn_ok.setDefault(True)
        self.btn_cancel = gui.QPushButton('&Cancel', self)
        self.connect(self.btn_cancel, core.SIGNAL('clicked()'), self.on_cancel)

        ns_tag = tag = ns_uri = txt = ''
        if item:
            ns_tag = item["tag"]
            if ns_tag.startswith('{'):
                ns_uri, tag = ns_tag[1:].split('}')
            else:
                tag = ns_tag
            if "text" in item:
                self.cb.toggle()
                txt = item["text"]
            if ns_uri:
                self.cb_ns.toggle()
                for ix, uri in enumerate(self._parent.ns_uris):
                    if uri == ns_uri:
                        self.cmb_ns.setCurrentIndex(ix + 1)
        self.txt_tag.setText(tag)
        self.txt_data.setText(txt)

        sizer = gui.QVBoxLayout()

        hsizer = gui.QHBoxLayout()
        gsizer = gui.QGridLayout()
        gsizer.addWidget(lbl_name, 0, 0)
        hsizer2 = gui.QHBoxLayout()
        hsizer2.addWidget(self.txt_tag)
        hsizer2.addStretch()
        gsizer.addLayout(hsizer2, 0, 1)
        gsizer.addWidget(self.cb_ns)
        gsizer.addWidget(self.cmb_ns)
        hsizer.addLayout(gsizer)
        hsizer.addStretch()
        sizer.addLayout(hsizer)

        hsizer = gui.QHBoxLayout()
        vsizer = gui.QVBoxLayout()
        vsizer.addWidget(self.cb)
        vsizer.addWidget(self.txt_data)
        hsizer.addLayout(vsizer)
        sizer.addLayout(hsizer)

        hsizer = gui.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(self.btn_ok)
        hsizer.addWidget(self.btn_cancel)
        hsizer.addStretch()
        sizer.addLayout(hsizer)

        self.setLayout(sizer)

    def on_cancel(self):
        gui.QDialog.done(self, gui.QDialog.Rejected)

    def on_ok(self):
        self._parent.data = {}
        tag = str(self.txt_tag.text())
        if tag == '' or len(tag.split()) > 1:
            self._parent._meldfout('Element name must not be empty or contain spaces')
            self.txt_tag.setFocus()
            return
        if self.cb_ns.isChecked():
            seq = self.cmb_ns.currentIndex()
            if seq == 0:
                self._parent._meldfout('Namespace must be selected if checked')
                self.cb_ns.setFocus()
                return
            tag = '{{{}}}{}'.format(self.cmb_ns.itemText(seq), tag)
        self._parent.data["tag"] = tag
        self._parent.data["data"] = self.cb.isChecked()
        self._parent.data["text"] = self.txt_data.toPlainText()
        gui.QDialog.done(self, gui.QDialog.Accepted)

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

        self.cb_ns = gui.QCheckBox('Namespace:', self)
        self.cmb_ns = gui.QComboBox(self)
        self.cmb_ns.setEditable(False)
        self.cmb_ns.addItem('-- none --')
        self.cmb_ns.addItems(self._parent.ns_uris)

        lbl_value = gui.QLabel("Attribute value:", self)
        self.txt_value = gui.QLineEdit(self)
        self.btn_ok = gui.QPushButton('&Save', self)
        self.btn_ok.setDefault(True)
        self.connect(self.btn_ok, core.SIGNAL('clicked()'), self.on_ok)
        self.btn_cancel = gui.QPushButton('&Cancel', self)
        self.connect(self.btn_cancel, core.SIGNAL('clicked()'), self.on_cancel)

        ns_nam = nam = ns_uri = val = ''
        if item:
            ns_nam = item["name"]
            if ns_nam.startswith('{'):
                ns_uri, nam = ns_nam[1:].split('}')
            else:
                nam = ns_nam
            if ns_uri:
                self.cb_ns.toggle()
                for ix, uri in enumerate(self._parent.ns_uris):
                    if uri == ns_uri:
                        self.cmb_ns.setCurrentIndex(ix + 1)
            val = item["value"]
        self.txt_name.setText(nam)
        self.txt_value.setText(val)

        sizer = gui.QVBoxLayout()

        hsizer = gui.QHBoxLayout()
        gsizer = gui.QGridLayout()
        gsizer.addWidget(lbl_name, 0, 0)
        hsizer2 = gui.QHBoxLayout()
        hsizer2.addWidget(self.txt_name)
        hsizer2.addStretch()
        gsizer.addLayout(hsizer2, 0, 1)
        gsizer.addWidget(self.cb_ns, 1, 0)
        gsizer.addWidget(self.cmb_ns, 1, 1)
        gsizer.addWidget(lbl_value, 2, 0)
        hsizer2 = gui.QHBoxLayout()
        hsizer2.addWidget(self.txt_value)
        hsizer2.addStretch()
        gsizer.addLayout(hsizer2, 2, 1)
        hsizer.addLayout(gsizer)
        hsizer.addStretch()
        sizer.addLayout(hsizer)

        hsizer = gui.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(self.btn_ok)
        hsizer.addWidget(self.btn_cancel)
        hsizer.addStretch()
        sizer.addLayout(hsizer)

        self.setLayout(sizer)
        ## self.resize(320,125)

    def on_ok(self):
        self._parent.data = {}
        nam = self.txt_name.text()
        if nam == '':
            self._parent._meldfout('Attribute name must not be empty or contain spaces')
            self.txt_name.setFocus()
            return
        if self.cb_ns.isChecked():
            seq = self.cmb_ns.currentIndex()
            if seq == 0:
                self._parent._meldfout('Namespace must be selected if checked')
                self.cb_ns.setFocus()
                return
            nam = '{{{}}}{}'.format(self.cmb_ns.itemText(seq), nam)
        self._parent.data["name"] = nam
        self._parent.data["value"] = self.txt_value.text()
        gui.QDialog.done(self, gui.QDialog.Accepted)

    def on_cancel(self):
        gui.QDialog.done(self, gui.QDialog.Rejected)

    def keyPressEvent(self, event):
        """event handler voor toetsaanslagen"""
        if event.key() == core.Qt.Key_Escape:
            gui.QDialog.done(self, gui.QDialog.Rejected)

class SearchDialog(gui.QDialog):
    def __init__(self, parent, title="", item=None):
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        self._parent = parent

        self.cb_element = gui.QLabel('Element', self)
        lbl_element = gui.QLabel("name:", self)
        self.txt_element = gui.QLineEdit(self)
        self.txt_element.textChanged.connect(self.set_search)

        self.cb_attr = gui.QLabel('Attribute', self)
        lbl_attr_name = gui.QLabel("name:", self)
        self.txt_attr_name = gui.QLineEdit(self)
        self.txt_attr_name.textChanged.connect(self.set_search)
        lbl_attr_val = gui.QLabel("value:", self)
        self.txt_attr_val = gui.QLineEdit(self)
        self.txt_attr_val.textChanged.connect(self.set_search)

        self.cb_text = gui.QLabel('Text', self)
        lbl_text = gui.QLabel("value:", self)
        self.txt_text = gui.QLineEdit(self)
        self.txt_text.textChanged.connect(self.set_search)

        self.lbl_search = gui.QLabel('', self)

        self.btn_ok = gui.QPushButton('&Ok', self)
        self.btn_ok.clicked.connect(self.on_ok)
        self.btn_ok.setDefault(True)
        self.btn_cancel = gui.QPushButton('&Cancel', self)
        self.btn_cancel.clicked.connect(self.on_cancel)

        sizer = gui.QVBoxLayout()

        gsizer = gui.QGridLayout()

        gsizer.addWidget(self.cb_element, 0, 0)
        vsizer = gui.QVBoxLayout()
        hsizer = gui.QHBoxLayout()
        hsizer.addWidget(lbl_element)
        hsizer.addWidget(self.txt_element)
        vsizer.addLayout(hsizer)
        gsizer.addLayout(vsizer, 0, 1)

        vsizer = gui.QVBoxLayout()
        vsizer.addSpacing(5)
        vsizer.addWidget(self.cb_attr)
        vsizer.addStretch()
        gsizer.addLayout(vsizer, 1, 0)
        vsizer = gui.QVBoxLayout()
        hsizer = gui.QHBoxLayout()
        hsizer.addWidget(lbl_attr_name)
        hsizer.addWidget(self.txt_attr_name)
        vsizer.addLayout(hsizer)
        hsizer = gui.QHBoxLayout()
        hsizer.addWidget(lbl_attr_val)
        hsizer.addWidget(self.txt_attr_val)
        vsizer.addLayout(hsizer)
        gsizer.addLayout(vsizer, 1, 1)

        gsizer.addWidget(self.cb_text, 2, 0)
        hsizer = gui.QHBoxLayout()
        hsizer.addWidget(lbl_text)
        hsizer.addWidget(self.txt_text)
        gsizer.addLayout(hsizer, 2, 1)
        sizer.addLayout(gsizer)

        hsizer = gui.QHBoxLayout()
        hsizer.addWidget(self.lbl_search)
        sizer.addLayout(hsizer)

        hsizer = gui.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(self.btn_ok)
        hsizer.addWidget(self.btn_cancel)
        hsizer.addStretch()
        sizer.addLayout(hsizer)

        self.setLayout(sizer)

    def set_search(self):
        out = ''
        ele = self.txt_element.text()
        attr_name = self.txt_attr_name.text()
        attr_val = self.txt_attr_val.text()
        text = self.txt_text.text()
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
        self.lbl_search.setText(out)

    def on_ok(self):
        ele = str(self.txt_element.text())
        attr_name = str(self.txt_attr_name.text())
        attr_val = str(self.txt_attr_val.text())
        text = str(self.txt_text.text())
        if not any((ele, attr_name, attr_val, text)):
            self._parent._meldfout('Please enter search criteria or press cancel')
            self.txt_element.setFocus()
            return

        self._parent.search_args = (ele, attr_name, attr_val, text)
        gui.QDialog.done(self, gui.QDialog.Accepted)

    def on_cancel(self):
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

    def keyReleaseEvent(self, event):
        skip = self.on_keyup(event)
        if not skip:
            gui.QMainWindow.keyReleaseEvent(self, event)

    def closeEvent(self, event):
        """applicatie afsluiten"""
        test = self.check_tree()
        print(test, event)
        if test:
            event.accept()
        else:
            event.ignore()

    def mark_dirty(self, state):
        data = AxeMixin.mark_dirty(self, state, str(self.windowTitle()))
        if data:
            self.setWindowTitle(data)

    def newxml(self, ev=None):
        AxeMixin.newxml(self)

    def openxml(self, ev=None):
        AxeMixin.openxml(self)

    def savexml(self, ev=None):
        AxeMixin.savexml(self)

    def savexmlas(self, ev=None):
        ok = AxeMixin.savexmlas(self)
        if ok:
            self.top.setText(0, self.xmlfn)
            self.setWindowTitle(" - ".join((os.path.basename(self.xmlfn), TITEL)))

    ## def savexmlfile(self, oldfile=''):
        ## AxeMixin.savexmlfile(self, oldfile)

    def _savexml(self):
        def expandnode(rt, root, tree):
            for ix in range(rt.childCount()):
                tag = rt.child(ix)
                text = str(tag.text(0))
                data = (str(tag.text(1)), str(tag.text(2)))
                node = tree.expand(root, text, data)
                if node is not None:
                    expandnode(tag, node, tree)
        top = self.tree.topLevelItem(0)
        rt = top.child(0)
        text = str(rt.text(0))
        if text == 'namespaces':
            rt = top.child(1)
            text = str(rt.text(0))
        data = (str(rt.text(1)), str(rt.text(2)))
        tree = XMLTree(data[0]) # .split(None,1)
        root = tree.root
        expandnode(rt, root, tree)
        if self.ns_prefixes:
            namespace_data = (self.ns_prefixes, self.ns_uris)
        h = tree.write(self.xmlfn, namespace_data)
        self.mark_dirty(False)

    def about(self, ev=None):
        AxeMixin.about(self)

    def init_tree(self, root, prefixes=None, uris=None, name=''):
        def add_to_tree(el, rt):
            rr = add_as_child((el.tag, el.text), rt, self.ns_prefixes, self.ns_uris)
            for attr in el.keys():
                h = el.get(attr)
                if not h:
                    h = '""'
                rrr = add_as_child((attr, h), rr, self.ns_prefixes, self.ns_uris,
                    attr=True)
            for subel in list(el):
                add_to_tree(subel, rr)

        self.tree.clear() # DeleteAllItems()
        titel = AxeMixin.init_tree(self, root, prefixes, uris, name)
        self.top = gui.QTreeWidgetItem()
        self.top.setText(0, titel)
        self.tree.addTopLevelItem(self.top) # AddRoot(titel)
        self.setWindowTitle(" - ".join((os.path.split(titel)[-1],TITEL)))
        # eventuele namespaces toevoegen
        namespaces = False
        for ix, prf in enumerate(self.ns_prefixes):
            if not namespaces:
                ns_root = gui.QTreeWidgetItem(['namespaces'])
                self.top.addChild(ns_root)
                namespaces = True
            ns_item = gui.QTreeWidgetItem()
            ns_item.setText(0, '{}: {}'.format(prf, self.ns_uris[ix]))
            ns_root.addChild(ns_item)
        rt = add_as_child((self.rt.tag, self.rt.text), self.top, self.ns_prefixes,
            self.ns_uris)
        for el in list(self.rt):
            add_to_tree(el, rt)
        #self.tree.selection = self.top
        # set_selection()
        self.mark_dirty(False)

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
            self._meldfout("Can't paste below an attribute")
            return
        if data == ((self.rt.tag, self.rt.text) or ""):
            if before:
                self._meldfout("Can't paste before the root")
                return
            else:
                self._meldinfo("Pasting as first element below root")
                pastebelow = True
        ## if self.cut:
            ## self.enable_pasteitems(False)
        if self.cut_att:
            item = getshortname(self.cut_att, self.ns_prefixes, self.ns_uris,
                attr=True)
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
            rt = add_as_child(data, add_under, self.ns_prefixes, self.ns_uris,
                insert=ix)
            self.mark_dirty(True)

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
        ## action = gui.QAction('Contextmenu', self)
        ## self.connect(action, core.SIGNAL('triggered()'), self.popupmenu)
        ## action.setShortcut(core.Qt.Key_Menu)
        self.mark_dirty(False)

    def init_menus(self, popup=False):
        if popup:
            viewmenu = gui.QMenu("&View")
        else:
            self.filemenu_actions, self.viewmenu_actions = [], []
            self.editmenu_actions, self.searchmenu_actions = [], []
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
                        ("&Edit", self.edit, 'Ctrl+E,F2'),
                        ("&Delete", self.delete, 'Ctrl+D,Delete'),
                        ("C&ut", self.cut, 'Ctrl+X'),
                        ("&Copy", self.copy, 'Ctrl+C'),
                        ("Paste Before", self.paste, 'Shift+Ctrl+V'),
                        ("Paste After", self.paste_aft, 'Ctrl+V'),
                        ("Paste Under", self.paste_und, 'Alt+Ctrl+V'),
                        ("Insert Attribute", self.add_attr, 'Shift+Insert'),
                        ('Insert Element Before', self.insert, 'Ctrl+Insert'),
                        ('Insert Element After', self.ins_aft, 'Alt+Insert'),
                        ('Insert Element Under', self.ins_chld, 'Insert'),
                    ),
                    (
                        ("&Find", self.search, 'Ctrl+F'),
                        ("Find &Last", self.search_last, 'Shift+Ctrl+F'),
                        ("Find &Next", self.search_next, 'F3'),
                        ("Find &Previous", self.search_prev, 'Shift+F3'),
                        ("&Replace", self.replace, 'Ctrl+H'),
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
                    elif ix == 3:
                        self.searchmenu_actions.append(act)
            self.pastebefore_item, self.pasteafter_item, \
                self.pasteunder_item = self.editmenu_actions[4:7]

            menubar = self.menuBar()
            filemenu = menubar.addMenu("&File")
            for act in self.filemenu_actions[:4]:
                filemenu.addAction(act)
            filemenu.addSeparator()
            filemenu.addAction(self.filemenu_actions[-1])
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
            searchmenu = editmenu
            searchmenu.addSeparator()
        else:
            searchmenu = menubar.addMenu("&Search")

        for act in self.searchmenu_actions:
            searchmenu.addAction(act)

        if popup:
            return searchmenu
        ## else:
            ## return filemenu, viewmenu, editmenu

    def popupmenu(self, item):
        print('self.popupmenu called')
        menu = self.init_menus(popup=True)
        menu.exec_(self.tree.mapToGlobal(self.tree.visualItemRect(item).bottomRight()))

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

    def _ask_yesnocancel(self, prompt):
        """stelt een vraag en retourneert het antwoord
        1 = Yes, 0 = No, -1 = Cancel
        """
        retval = dict(zip((gui.QMessageBox.Yes, gui.QMessageBox.No,
            gui.QMessageBox.Cancel), (1, 0, -1)))
        h = gui.QMessageBox.question(self, self.title, prompt,
            gui.QMessageBox.Yes | gui.QMessageBox.No | gui.QMessageBox.Cancel,
            defaultButton = gui.QMessageBox.Yes)
        return retval[h]

    def _ask_for_text(self, prompt):
        """vraagt om tekst en retourneert het antwoord"""
        data, ok = gui.QInputDialog.getText(self, self.title, prompt,
            gui.QLineEdit.Normal, "")
        return data

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

    def _file_to_save(self, dirname, filename):
        name = gui.QFileDialog.getSaveFileName(self, "Save file as ...", dirname,
            HMASK)
        ok = bool(name)
        return ok, str(name)

    def quit(self, ev=None):
        self.close()

    def on_keyup(self, ev=None):
        ky = ev.key()
        item = self.tree.currentItem()
        skip = False
        if item and item != self.top:
            if ky == core.Qt.Key_Return:
                if item.childCount() > 0:
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
            elif ky == core.Qt.Key_Menu:
                self.popupmenu(item)
                skip = True
        return skip

    def checkselection(self, message=True):
        """get the currently seleted item

        if there is no selection or the file title is selected, display a message
        (if requested). I think originally it returned False in that case
        """
        sel = True
        self.item = self.tree.currentItem()
        if message and (self.item is None or self.item == self.top):
            self._meldinfo('You need to select an element or attribute first')
        return sel

    def expand(self, ev=None):
        def expand_with_children(item):
            self.tree.expandItem(item)
            for ix in range(item.childCount()):
                expand_with_children(item.child(ix))
        item = self.tree.currentItem()
        if item:
            expand_with_children(item)
            self.tree.resizeColumnToContents(0)

    def collapse(self,ev=None):
        item = self.tree.currentItem()
        if item:
            self.tree.collapseItem(item)    # mag eventueel recursief in overeenstemming met vorige
            self.tree.resizeColumnToContents(0)

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
                h = ((self.data["tag"], self.data["text"]), self.ns_prefixes,
                    self.ns_uris)
                self.item.setText(0, getshortname(h))
                self.item.setText(1, self.data["tag"])
                self.item.setText(2, self.data["text"])
                self.mark_dirty(True)
        else:
            nam, val = str(self.item.text(1)), str(self.item.text(2))
            data = {'item': self.item, 'name': nam, 'value': val}
            edt = AttributeDialog(self,title='Edit an attribute',item=data).exec_()
            if edt == gui.QDialog.Accepted:
                h = ((self.data["name"], self.data["value"]), self.ns_prefixes,
                    self.ns_uris)
                self.item.setText(0, getshortname(h, attr=True))
                self.item.setText(1, self.data["name"])
                self.item.setText(2, self.data["value"])
                self.mark_dirty(True)

    def add_attr(self, ev=None):
        if not self.checkselection():
            return
        edt = AttributeDialog(self, title="New attribute").exec_()
        if edt == gui.QDialog.Accepted:
            if str(self.item.text(0)).startswith(ELSTART):
                h = (self.data["name"], self.data["value"])
                rt = add_as_child(h, self.item, self.ns_prefixes, self.ns_uris,
                    attr=True)
                self.mark_dirty(True)
            else:
                self._meldfout("Can't add attribute to attribute")

    def search(self, event=None, reversed=False):
        self._search_pos = None
        edt = SearchDialog(self, title='Search options').exec_()
        if edt == gui.QDialog.Accepted:
            self.search_next(event, reversed)
            ## found, is_attr = find_next(flatten_tree(self.top), self.search_args,
                ## reversed) # self.tree.top.child(0)
            ## if found:
                ## self.tree.setCurrentItem(found)
                ## self._search_pos = (found, is_attr)

    def search_last(self, event=None):
        self.search(event, reversed=True)

    def search_next(self, event=None, reversed=False):
        ## self._meldinfo('Find next: not implemented yet')
        found, is_attr = find_next(flatten_tree(self.top), self.search_args,
            reversed, self._search_pos) # self.tree.top.child(0)
        if found:
            self.tree.setCurrentItem(found)
            self._search_pos = (found, is_attr)
        else:
            self._meldinfo('Niks (meer) gevonden')

    def search_prev(self, event=None):
        self.search_next(event, reversed=True)

    def replace(self, event=None):
        self._meldinfo('Replace: not sure if I wanna implement this')


def axe_gui(args):
    app = gui.QApplication(sys.argv)
    if len(args) > 1:
        frm = MainFrame(None, -1, fn=" ".join(args[1:]))
    else:
        frm = MainFrame(None, -1)
    sys.exit(app.exec_())

if __name__ == "__main__":
    axe_gui(sys.argv)
