# -*- coding: utf-8 -*-

"PyQT versie van een op een treeview gebaseerde XML-editor"
import os
import sys
import functools
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
from .axe_base import getshortname, find_next, XMLTree, AxeMixin, log
from .axe_base import ELSTART, TITEL, axe_iconame
if os.name == "nt":
    HMASK = "XML files (*.xml);;All files (*.*)"
elif os.name == "posix":
    HMASK = "XML files (*.xml *.XML);;All files (*.*)"
IMASK = "All files (*.*)"

def calculate_location(win, node):
    """attempt to calculate some kind of identification for a tree node

    this function returns a tuple of subsequent indices of a child under its
    parent.
    possibly this can be used in the replacements dictionary
    """
    id_ = []
    while node != win.top:
        idx = node.parent().indexOfChild(node)
        id_.insert(0, idx)
        node = node.parent()
    return tuple(id_)

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
#
# Dialog windows
#
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
        self.cb.setCheckable(False)
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
        fout = ''
        if tag == '':
            fout = 'Element name must not be empty'
        elif len(tag.split()) > 1:
            fout = 'Element name must not contain spaces'
        elif tag[0].isdigit():
            fout = 'Element name must not start with a digit'
        if fout:
            self._parent._meldfout(fout)
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
        fout = ''
        if nam == '':
            fout = 'Attribute name must not be empty'
        elif len(nam.split()) > 1:
            fout = 'Attribute name must not contain spaces'
        elif nam[0].isdigit():
            fout = 'Attribute name must not start with a digit'
        if fout:
            self._parent._meldfout(fout)
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
#
# Tree widget (subclass overriding some event handlers)
#
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
                menu = self.parent._init_menus(popup=True)
                menu.exec_(core.QPoint(xc, yc))
            else:
                event.ignore()
        else:
            event.ignore()


#
# Undo stack (subclass overriding some event handlers)
#
class UndoRedoStack(gui.QUndoStack):

    def __init__(self, parent):
        ## super().__init__(parent)
        gui.QUndoStack.__init__(self, parent)
        self.cleanChanged.connect(self.clean_changed)
        self.indexChanged.connect(self.index_changed)
        self.maxundo = self.undoLimit()
        self.setUndoLimit(1) # self.unset_undo_limit(False)
        ## log('Undo limit {}'.format(self.undoLimit()))
        win = self.parent()
        win.undo_item.setText('Nothing to undo')
        win.redo_item.setText('Nothing to redo')
        win.undo_item.setDisabled(True)
        win.redo_item.setDisabled(True)

    def unset_undo_limit(self, state):
        log('state is {}'.format(state))
        if state:
            self.setUndoLimit(self.maxundo)
            nolim, yeslim = 'un', ''
        else:
            self.setUndoLimit(1)
            nolim, yeslim = '', ' to one'
        ## self.parent().setundo_action.setChecked(state)
        self.parent().statusbar.showMessage('Undo level is now {}limited{}'.format(
            nolim, yeslim))

    def clean_changed(self, state):
        ## print('undo stack status changed:', state)
        win = self.parent()
        if state:
            win.undo_item.setText('Nothing to undo')
        win.undo_item.setDisabled(state)

    def index_changed(self, num):
        ## """change text of undo/redo menuitems according to stack change"""
        ## print('undo stack index changed:', num)
        win = self.parent()
        test = self.undoText()
        if test:
            win.undo_item.setText('&Undo ' + test)
            win.undo_item.setEnabled(True)
        else:
            win.undo_item.setText('Nothing to undo')
            win.undo_item.setDisabled(True)
        test = self.redoText()
        if test:
            win.redo_item.setText('&Redo ' + test)
            win.redo_item.setEnabled(True)
        else:
            win.redo_item.setText('Nothing to redo')
            win.redo_item.setDisabled(True)
#
# UndoCommand subclasses
#
class PasteElementCommand(gui.QUndoCommand):

    def __init__(self, win, tag, text, item, before, below,
            description="", data=None):
        self.win = win          # treewidget
        ## self.item = item        # where we are now
        ## self.parent = item.parent()
        self.tag = tag          # element name
        self.data = text        # element text
        self.before = before    # switch
        self.below = below      # switch
        self.children = data
        self.replaced = None    # in case item is replaced while redoing
        if below:
            description += ' Under'
        elif before:
            description += ' Before'
        else:
            description += ' After'
        log("init {} {} {}".format(description, self.tag, self.data)) ##, self.item)
        self.first_edit = not self.win.tree_dirty
        super().__init__(description)

    def redo(self):
        def zetzeronder(node, data, before=False, below=True):
            log('zetzeronder voor node {} met data {}'.format(node, data))
            text, data, children = data
            tag, value = data
            self.win.item = node
            is_attr = False if text.startswith(ELSTART) else True
            add_under = self.win._add_item(tag, value, before=before,
                below=below, attr=is_attr)
            below = True
            for item in children:
                zetzeronder(add_under, item)
            return add_under
        ## self.win.item = self.item
        log('In paste element redo for tag {} data {}'.format(self.tag, self.data))
        self.added = self.win._add_item(self.tag, self.data, before=self.before,
            below=self.below)
        log('newly added {} with children {}'.format(self.added, self.children))
        if self.children is not None:
            for item in self.children[0][2]:
                zetzeronder(self.added, item)
        ## if self.replaced:
            ## self.win.replaced[calculate_location(add_under)] = self.added
        self.win.tree.expandItem(self.added)
        log("self.added after adding children: {}".format(self.added))

    def undo(self):
        "essentially 'cut' Command"
        log('In paste element undo for added'.format(self.added))
        self.replaced = self.added   # remember original item in case redo replaces it
        item = CopyElementCommand(self.win, self.added, cut=True, retain=False,
            description="Undo add element")
        item.redo()
        if self.first_edit:
            self.win.mark_dirty(False)
        self.win.statusbar.showMessage('{} undone'.format(self.text()))


class PasteAttributeCommand(gui.QUndoCommand):
    def __init__(self, win, name, value, item, description=""):
        super().__init__(description)
        self.win = win          # treewidget
        self.item = item        # where we are now
        self.name = name        # attribute name
        self.value = value      # attribute value
        log("init {} {} {} {}".format(description, self.name, self.value, self.item))
        self.first_edit = not self.win.tree_dirty
        super().__init__(description)

    def redo(self):
        log('(redo) add attr {} {} {}'.format(self.name, self.value, self.item))
        self.win.item = self.item
        self.added = self.win._add_item(self.name, self.value, attr=True)
        self.win.tree.expandItem(self.added.parent())
        log('Added {}'.format(self.added))

    def undo(self):
        "essentially 'cut' Command"
        item = CopyElementCommand(self.win, self.added, cut=True, retain=False,
            description="Undo add attribute")
        item.redo()
        if self.first_edit:
            self.win.mark_dirty(False)
        self.win.statusbar.showMessage('{} undone'.format(self.text()))


class EditCommand(gui.QUndoCommand):
    def __init__(self, win, old_state, new_state, description=""):
        log("building editcommand for {}".format(description))
        super().__init__(description)
        self.win = win
        self.item = self.win.item
        self.old_state = old_state
        self.new_state = new_state
        self.first_edit = not self.win.tree_dirty

    def redo(self):
        "change node's state to new"
        self.item.setText(0, self.new_state[0])
        self.item.setText(1, self.new_state[1])
        self.item.setText(2, self.new_state[2])

    def undo(self):
        "change node's state back to old"
        self.item.setText(0, self.old_state[0])
        self.item.setText(1, self.old_state[1])
        self.item.setText(2, self.old_state[2])
        if self.first_edit:
            self.win.mark_dirty(False)
        self.win.statusbar.showMessage('{} undone'.format(self.text()))

class CopyElementCommand(gui.QUndoCommand):
    def __init__(self, win, item, cut, retain, description=""):
        super().__init__(description)
        self.undodata = None
        self.win = win      # treewidget
        self.item = item    # where we are now
        self.tag = str(self.item.text(1))
        self.data = str(self.item.text(2)) # name and text
        log("init {} {} {} {}".format(description, self.tag, self.data, self.item))
        self.cut = cut
        self.retain = retain
        self.first_edit = not self.win.tree_dirty

    def redo(self):
        def push_el(el, result):
            text = str(el.text(0))
            data = (str(el.text(1)), str(el.text(2)))
            children = []
            for ix in range(el.childCount()):
                subel = el.child(ix)
                temp = push_el(subel, children)
            result.append((text, data, children))
            return result
        log('In copy element redo for item {} with data {}'.format(self.item,
            self.data))
        if self.undodata is None:
            self.parent = self.item.parent()
            self.loc = self.parent.indexOfChild(self.item)
            self.undodata = push_el(self.item, [])
            if self.loc > 0:
                self.prev = self.parent.child(self.loc - 1)
            else:
                self.prev = self.parent
                if self.prev == self.win.rt:
                    self.prev = self.parent.child(self.loc + 1)
        if self.retain:
            log('Retaining item')
            self.win.cut_el = self.undodata
            self.win.cut_att = None
            self.win._enable_pasteitems(True)
        if self.cut:
            log('cutting item from parent {}'.format(self.parent))
            self.parent.removeChild(self.item)
            self.item = self.prev
            self.win.tree.setCurrentItem(self.prev)

    def undo(self):
        log('In copy element undo for tag {} data {} item {}'.format(self.tag,
            self.data, self.item))
        # self.cut_el = None
        if self.cut:
            item = PasteElementCommand(self.win, self.tag, self.data, self.parent,
                before=False, below=True, data = self.undodata,
                description="Undo Copy Element")
            item.redo() # add_under=add_under, loc=self.loc)
            self.item = item.added
        if self.first_edit:
            self.win.mark_dirty(False)
        self.win.statusbar.showMessage('{} undone'.format(self.text()))
            ## self.win.tree.setCurrentItem(self.item)

class CopyAttributeCommand(gui.QUndoCommand):
    def __init__(self, win, item, cut, retain, description):
        super().__init__(description)
        self.win = win      # treewidget
        self.item = item    # where we are now
        self.name = str(self.item.text(1))
        self.value = str(self.item.text(2)) # name and text
        log("init {} {} {} {}".format(description, self.name, self.value, self.item))
        self.cut = cut
        self.retain = retain
        self.first_edit = not self.win.tree_dirty

    def redo(self):
        log('copying item {} with text {}'.format(self.item, self.value))
        self.parent = self.item.parent()
        self.loc = self.parent.indexOfChild(self.item)
        if self.retain:
            log('Retaining attribute')
            self.win.cut_el = None
            self.win.cut_att = (self.name, self.value)
            self.win._enable_pasteitems(True)
        if self.cut:
            log('cutting attribute')
            ix = self.loc
            if ix > 0:
                prev = self.parent.child(ix - 1)
            else:
                prev = self.parent
                if prev == self.win.rt:
                    prev = self.parent.child(ix + 1)
            self.parent.removeChild(self.item)
            self.item = None
            self.win.tree.setCurrentItem(prev)

    def undo(self):
        log('Undo copy attribute for {} {} {}'.format(self.name, self.value, self.item))
        # self.win.cut_att = None
        if self.cut:
            item = PasteAttributeCommand(self.win, self.name, self.value, self.parent,
                description="Undo Copy Attribute")
            item.redo()
            self.item = item.added
        if self.first_edit:
            self.win.mark_dirty(False)
        self.win.statusbar.showMessage('{} undone'.format(self.text()))
#
# Main Window
#
class MainFrame(gui.QMainWindow, AxeMixin):
    "Main GUI class"

    undoredowarning = """\
    NOTE:

    Limiting undo/redo to one action has a reason.

    This feature may not work as intended when items are removed
    and immediately un-removed or when multiple redo actions are
    executed when the originals were done at different levels
    in the tree.

    So be prepared for surprises, I haven't quite figured this lot
    out yet.
    """

    def __init__(self, parent, id, fn=''):
        AxeMixin.__init__(self, parent, id, fn) # super() werkt niet - teveel argumenten
        self.show()

    #
    # reimplemented methods from QMainWindow
    #
    def keyReleaseEvent(self, event):
        skip = self.on_keyup(event)
        if not skip:
            gui.QMainWindow.keyReleaseEvent(self, event)

    def closeEvent(self, event):
        """applicatie afsluiten"""
        test = self.check_tree()
        if test:
            event.accept()
        else:
            event.ignore()
    # reimplemented methods from Mixin
    # mostly because of including the gui event in the signature
    #
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

    def writexml(self):
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
        namespace_data = None
        if self.ns_prefixes:
            namespace_data = (self.ns_prefixes, self.ns_uris)
        h = tree.write(self.xmlfn, namespace_data)
        self.mark_dirty(False)

    def about(self, ev=None):
        AxeMixin.about(self)

    def init_tree(self, root, prefixes=None, uris=None, name=''):
        def add_to_tree(el, rt):
            self.item = rt
            rr = self._add_item(el.tag, el.text)
            ## log(calculate_location(self, rr))
            for attr in el.keys():
                h = el.get(attr)
                if not h:
                    h = '""'
                self.item = rr
                _ = self._add_item(attr, h, attr=True)
            for subel in list(el):
                add_to_tree(subel, rr)

        self.tree.clear() # DeleteAllItems()
        self.undo_stack.clear()
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
        self.item = self.top
        rt = self._add_item(self.rt.tag, self.rt.text)
        for attr in self.rt.keys():
            h = self.rt.get(attr)
            if not h:
                h = '""'
            self.item = rt
            self._add_item(attr, h, attr=True)
        for el in list(self.rt):
            add_to_tree(el, rt)
        #self.tree.selection = self.top
        # set_selection()
        self.replaced = {} # dict of nodes that have been replaced while editing
        self.mark_dirty(False)

    def cut(self, ev=None):
        AxeMixin.cut(self)

    def delete(self, ev=None):
        AxeMixin.delete(self)

    def copy(self, ev=None, cut=False, retain=True):
        if not self._checkselection():
            return
        txt = AxeMixin.copy(self, cut, retain)
        text = str(self.item.text(0))
        data = (str(self.item.text(1)), str(self.item.text(2)))
        if data == (self.rt.tag, self.rt.text or ""):
            self._meldfout("Can't %s the root" % txt)
            return
        if text.startswith(ELSTART):
            command = CopyElementCommand(self, self.item, cut, retain,
                "{} Element".format(txt))
        else:
            command = CopyAttributeCommand(self, self.item, cut, retain,
                "{} Attribute".format(txt))
        self.undo_stack.push(command)
        if cut:
            self.mark_dirty(True)
            ## self.tree.setCurrentItem(prev)

    def paste_after(self, ev=None):
        AxeMixin.paste_after(self)

    def paste_under(self, ev=None):
        AxeMixin.paste_under(self)

    def paste(self, ev=None, before=True, pastebelow=False):
        if not self._checkselection():
            return
        if self.item.parent() == self.top and not pastebelow:
            self._meldinfo("Can't paste before or after the root")
            return
        data = (str(self.item.text(1)), str(self.item.text(2)))
        log('{} {} {}'.format(pastebelow, str(self.item.text(0)), self.cut_att))
        if not str(self.item.text(0)).startswith(ELSTART) and (pastebelow or
                self.cut_att):
            self._meldinfo("Can't paste below an attribute")
            log(self.in_dialog)
            return
        if self.cut_att:
            name, value = self.cut_att
            command = PasteAttributeCommand(self, name, value, self.item,
                description="Paste Attribute")
            self.undo_stack.push(command)
        elif self.cut_el:
            tag, text = self.cut_el[0][1]
            command = PasteElementCommand(self, tag, text, self.item,
                before=before, below=pastebelow, description="Paste Element",
                data=self.cut_el)
            self.undo_stack.push(command)
        self.mark_dirty(True)

    def insert_after(self, ev=None):
        AxeMixin.insert_after(self)

    def insert_child(self, ev=None):
        AxeMixin.insert_child(self)

    def insert(self, ev=None, before=True, below=False):
        if not self._checkselection():
            return
        if str(self.item.text(0)).startswith(ELSTART) or (not before and not below):
            pass
        else:
            self._meldfout("Can't add element to attribute")
            return
        if self.item.parent() == self.top and not below:
            self._meldinfo("Can't insert before or after the root")
            return
        edt = ElementDialog(self, title="New element").exec_()
        if edt == gui.QDialog.Accepted:
            command = PasteElementCommand(self, self.data['tag'], self.data['text'],
                self.item, before, below, "Insert Element")
            self.undo_stack.push(command)
            self.mark_dirty(True)
    #
    # internals
    #
    def _init_gui(self, parent, id):
        """Deze methode wordt aangeroepen door de __init__ van de mixin class
        """
        self.parent = parent
        gui.QMainWindow.__init__(self) # aparte initialisatie net als voor mixin
        self._icon = gui.QIcon(axe_iconame)
        self.resize(620, 900)
        self.setWindowIcon(self._icon)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        self._init_menus()

        self.tree = VisualTree(self)
        self.tree.setItemHidden(self.tree.headerItem(), True)
        self.setCentralWidget(self.tree)
        self._enable_pasteitems(False)
        self.undo_stack = UndoRedoStack(self)
        self.mark_dirty(False)
        self.in_dialog = False

    def _init_menus(self, popup=False):
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
                        ('&Unlimited Undo', self._limit_undo, ''),
                        ('E&xit', self.quit, 'Ctrl+Q'),
                    ),
                    (
                        ("&Expand All (sub)Levels", self.expand, 'Ctrl++'),
                        ("&Collapse All (sub)Levels", self.collapse, 'Ctrl+-'),
                    ),
                    (
                        ("Nothing to &Undo", self.undo, 'Ctrl+Z'),
                        ("Nothing to &Redo", self.redo, 'Ctrl+Y'),
                        ("&Edit", self.edit, 'Ctrl+E,F2'),
                        ("&Delete", self.delete, 'Ctrl+D,Delete'),
                        ("C&ut", self.cut, 'Ctrl+X'),
                        ("&Copy", self.copy, 'Ctrl+C'),
                        ("Paste Before", self.paste, 'Shift+Ctrl+V'),
                        ("Paste After", self.paste_after, 'Ctrl+V'),
                        ("Paste Under", self.paste_under, 'Alt+Ctrl+V'),
                        ("Insert Attribute", self.add_attr, 'Shift+Insert'),
                        ('Insert Element Before', self.insert, 'Ctrl+Insert'),
                        ('Insert Element After', self.insert_after, 'Alt+Insert'),
                        ('Insert Element Under', self.insert_child, 'Insert'),
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
                    if shortcuts:
                        act.setShortcuts([x for x in shortcuts.split(',')])
                    if ix == 0:
                        self.filemenu_actions.append(act)
                    elif ix == 1:
                        self.viewmenu_actions.append(act)
                    elif ix == 2:
                        self.editmenu_actions.append(act)
                    elif ix == 3:
                        self.searchmenu_actions.append(act)
            self.undo_item, self.redo_item = self.editmenu_actions[0:2]
            self.pastebefore_item, self.pasteafter_item, \
                self.pasteunder_item = self.editmenu_actions[6:9]
            self.setundo_action = self.filemenu_actions[-2]
            self.setundo_action.setCheckable(True)
            self.setundo_action.setChecked(False)

            menubar = self.menuBar()
            filemenu = menubar.addMenu("&File")
            for act in self.filemenu_actions[:4]:
                filemenu.addAction(act)
            filemenu.addSeparator()
            filemenu.addAction(self.setundo_action)
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

        for ix, act in enumerate(self.editmenu_actions[:6]):
            editmenu.addAction(act)
            if ix == 2:
                editmenu.addSeparator()

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
        for act in self.editmenu_actions[9:]:
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

    def _meldinfo(self, text):
        self.in_dialog = True
        gui.QMessageBox.information(self, self.title, text)

    def _meldfout(self, text, abort=False):
        self.in_dialog = True
        gui.QMessageBox.critical(self, self.title, text)
        if abort:
            self.quit()
    def _ask_yesnocancel(self, prompt):
        """stelt een vraag en retourneert het antwoord
        1 = Yes, 0 = No, -1 = Cancel
        """
        retval = dict(zip((gui.QMessageBox.Yes, gui.QMessageBox.No,
            gui.QMessageBox.Cancel), (1, 0, -1)))
        self.in_dialog = True
        h = gui.QMessageBox.question(self, self.title, prompt,
            gui.QMessageBox.Yes | gui.QMessageBox.No | gui.QMessageBox.Cancel,
            defaultButton = gui.QMessageBox.Yes)
        return retval[h]

    def _ask_for_text(self, prompt):
        """vraagt om tekst en retourneert het antwoord"""
        self.in_dialog = True
        data, ok = gui.QInputDialog.getText(self, self.title, prompt,
            gui.QLineEdit.Normal, "")
        return data

    def _file_to_read(self):
        fnaam = gui.QFileDialog.getOpenFileName(self, "Choose a file", os.getcwd(),
            HMASK)
        ok = bool(fnaam)
        return ok, str(fnaam)

    def _file_to_save(self, dirname, filename):
        name = gui.QFileDialog.getSaveFileName(self, "Save file as ...", dirname,
            HMASK)
        ok = bool(name)
        return ok, str(name)

    def _enable_pasteitems(self, active=False):
        """activeert of deactiveert de paste-entries in het menu
        afhankelijk van of er iets te pasten valt
        """
        if active:
            self.pastebefore_item.setText("Paste Before")
        else:
            self.pastebefore_item.setText("Nothing to Paste")
        self.pastebefore_item.setEnabled(active)
        self.pasteafter_item.setEnabled(active)
        self.pasteunder_item.setEnabled(active)

    def _checkselection(self, message=True):
        """get the currently selected item

        if there is no selection or the file title is selected, display a message
        (if requested). Also return False in that case
        """
        sel = True
        self.item = self.tree.currentItem()
        log("in checkselection: self.item {}".format(self.item))
        if message and (self.item is None or self.item == self.top):
            self._meldinfo('You need to select an element or attribute first')
            sel = False
        return sel

    def _add_item(self, name, value, before=False, below=True, attr=False):
        log('in _add_item for {} value {} before is {} below is {}'.format(
            name, value, before, below))
        if value is None:
            value = ""
        h = ((str(name), str(value)), self.ns_prefixes, self.ns_uris)
        itemtext = getshortname(h, attr)
        if below:
            add_under = self.item
            insert = -1
            if not itemtext.startswith(ELSTART):
                cnt = self.item.childCount()
                for seq in range(cnt):
                    subitem = self.item.child(seq)
                    if str(subitem.text(0)).startswith(ELSTART):
                        break
                if cnt and seq < cnt:
                    insert = seq
        else:
            add_under = self.item.parent()
            insert = add_under.indexOfChild(self.item)
            if not before:
                insert += 1
        item = gui.QTreeWidgetItem()
        item.setText(0, itemtext)
        item.setText(1, name)
        item.setText(2, value)
        if insert == -1:
            log('add under {}'.format(add_under))
            add_under.addChild(item)
        else:
            add_under.insertChild(insert, item)
        return item

    def _limit_undo(self, ev=None):
        newstate = self.setundo_action.isChecked()
        self.undo_stack.unset_undo_limit(newstate)
        if newstate:
            self._meldinfo(self.undoredowarning)
    #
    # exposed
    #
    def popupmenu(self, item):
        log('self.popupmenu called')
        menu = self._init_menus(popup=True)
        menu.exec_(self.tree.mapToGlobal(self.tree.visualItemRect(item).bottomRight()))
    def quit(self, ev=None):
        self.close()

    def on_keyup(self, ev=None):
        ky = ev.key()
        item = self.tree.currentItem()
        skip = False
        if item and item != self.top:
            if ky == core.Qt.Key_Return:
                if self.in_dialog:
                    self.in_dialog = False
                else:
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
        if not self._checkselection():
            return
        data = str(self.item.text(0)) # self.item.get_text()
        if data.startswith(ELSTART):
            tag, text = str(self.item.text(1)), str(self.item.text(2))
            state = data, tag, text   # current values to be passed to UndoAction
            data = {'item': self.item, 'tag': tag}
            if text:
                data['data'] = True
                data['text'] = text
            edt = ElementDialog(self, title='Edit an element', item=data).exec_()
            if edt == gui.QDialog.Accepted:
                h = ((self.data["tag"], self.data["text"]), self.ns_prefixes,
                    self.ns_uris)
                new_state = getshortname(h), self.data["tag"], self.data["text"]
                log('calling editcommand for element')
                command = EditCommand(self, state, new_state, "Edit Element")
                self.undo_stack.push(command)
                self.mark_dirty(True)
        else:
            nam, val = str(self.item.text(1)), str(self.item.text(2))
            state = data, nam, val   # current values to be passed to UndoAction
            data = {'item': self.item, 'name': nam, 'value': val}
            edt = AttributeDialog(self,title='Edit an attribute',item=data).exec_()
            if edt == gui.QDialog.Accepted:
                h = ((self.data["name"], self.data["value"]), self.ns_prefixes,
                    self.ns_uris)
                new_state = getshortname(h, attr=True), self.data["name"], self.data["value"]
                log('calling editcommand for attribute')
                command = EditCommand(self, state, new_state, "Edit Attribute")
                self.undo_stack.push(command)
                self.mark_dirty(True)

    def add_attr(self, ev=None):
        if not self._checkselection():
            return
        if not str(self.item.text(0)).startswith(ELSTART):
            self._meldfout("Can't add attribute to attribute")
            return
        edt = AttributeDialog(self, title="New attribute").exec_()
        if edt == gui.QDialog.Accepted:
            command = PasteAttributeCommand(self, self.data["name"],
                self.data["value"], self.item, "Insert Attribute")
            self.undo_stack.push(command)
            self.mark_dirty(True)

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

    def undo(self, event=None):
        self.undo_stack.undo()

    def redo(self, event=None):
        self.undo_stack.redo()


def axe_gui(args):
    app = gui.QApplication(sys.argv)
    if len(args) > 1:
        frm = MainFrame(None, -1, fn=" ".join(args[1:]))
    else:
        frm = MainFrame(None, -1)
    sys.exit(app.exec_())

if __name__ == "__main__":
    axe_gui(sys.argv)
