"""PyQT5 versie van een op een treeview gebaseerde XML-editor
"""
import os
import sys
## import functools
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as gui
import PyQt5.QtCore as core
from .shared import ELSTART, axe_iconame, log
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


# Dialog windows
class ElementDialog(qtw.QDialog):
    """Dialog for editing an element
    """
    def __init__(self, parent, title="", item=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(parent._icon)
        self._parent = parent
        lbl_name = qtw.QLabel("element name:  ", self)
        self.txt_tag = qtw.QLineEdit(self)

        self.cb_ns = qtw.QCheckBox('Namespace:', self)
        self.cmb_ns = qtw.QComboBox(self)
        self.cmb_ns.setEditable(False)
        self.cmb_ns.addItem('-- none --')
        self.cmb_ns.addItems(self._parent.editor.ns_uris)

        self.cb = qtw.QCheckBox('Bevat data:', self)
        self.cb.setCheckable(False)
        self.txt_data = qtw.QTextEdit(self)
        self.txt_data.setTabChangesFocus(True)
        self.btn_ok = qtw.QPushButton('&Save', self)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_ok.setDefault(True)
        self.btn_cancel = qtw.QPushButton('&Cancel', self)
        self.btn_cancel.clicked.connect(self.reject)

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

        sizer = qtw.QVBoxLayout()

        hsizer = qtw.QHBoxLayout()
        gsizer = qtw.QGridLayout()
        gsizer.addWidget(lbl_name, 0, 0)
        hsizer2 = qtw.QHBoxLayout()
        hsizer2.addWidget(self.txt_tag)
        hsizer2.addStretch()
        gsizer.addLayout(hsizer2, 0, 1)
        gsizer.addWidget(self.cb_ns)
        gsizer.addWidget(self.cmb_ns)
        hsizer.addLayout(gsizer)
        hsizer.addStretch()
        sizer.addLayout(hsizer)

        hsizer = qtw.QHBoxLayout()
        vsizer = qtw.QVBoxLayout()
        vsizer.addWidget(self.cb)
        vsizer.addWidget(self.txt_data)
        hsizer.addLayout(vsizer)
        sizer.addLayout(hsizer)

        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(self.btn_ok)
        hsizer.addWidget(self.btn_cancel)
        hsizer.addStretch()
        sizer.addLayout(hsizer)

        self.setLayout(sizer)

    ## def on_cancel(self):
        ## super().done(qtw.QDialog.Rejected)

    def accept(self):
        """final checks, send changed data to parent"""
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
            self._parent.meldfout(fout)
            self.txt_tag.setFocus()
            return
        if self.cb_ns.isChecked():
            seq = self.cmb_ns.currentIndex()
            if seq == 0:
                self._parent.meldfout('Namespace must be selected if checked')
                self.cb_ns.setFocus()
                return
            tag = '{{{}}}{}'.format(self.cmb_ns.itemText(seq), tag)
        self._parent.data["tag"] = tag
        self._parent.data["data"] = self.cb.isChecked()
        self._parent.data["text"] = self.txt_data.toPlainText()
        super().accept()

    def keyPressEvent(self, event):
        """reimplemented event handler voor toetsaanslagen"""
        if event.key() == core.Qt.Key_Escape:
            super().done(qtw.QDialog.Rejected)


class AttributeDialog(qtw.QDialog):
    """Dialog for editing an attribute"""
    def __init__(self, parent, title='', item=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(parent._icon)
        self._parent = parent
        lbl_name = qtw.QLabel("Attribute name:", self)
        self.txt_name = qtw.QLineEdit(self)

        self.cb_ns = qtw.QCheckBox('Namespace:', self)
        self.cmb_ns = qtw.QComboBox(self)
        self.cmb_ns.setEditable(False)
        self.cmb_ns.addItem('-- none --')
        self.cmb_ns.addItems(self._parent.editor.ns_uris)

        lbl_value = qtw.QLabel("Attribute value:", self)
        self.txt_value = qtw.QLineEdit(self)
        self.btn_ok = qtw.QPushButton('&Save', self)
        self.btn_ok.setDefault(True)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel = qtw.QPushButton('&Cancel', self)
        self.btn_cancel.clicked.connect(self.reject)

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

        sizer = qtw.QVBoxLayout()

        hsizer = qtw.QHBoxLayout()
        gsizer = qtw.QGridLayout()
        gsizer.addWidget(lbl_name, 0, 0)
        hsizer2 = qtw.QHBoxLayout()
        hsizer2.addWidget(self.txt_name)
        hsizer2.addStretch()
        gsizer.addLayout(hsizer2, 0, 1)
        gsizer.addWidget(self.cb_ns, 1, 0)
        gsizer.addWidget(self.cmb_ns, 1, 1)
        gsizer.addWidget(lbl_value, 2, 0)
        hsizer2 = qtw.QHBoxLayout()
        hsizer2.addWidget(self.txt_value)
        hsizer2.addStretch()
        gsizer.addLayout(hsizer2, 2, 1)
        hsizer.addLayout(gsizer)
        hsizer.addStretch()
        sizer.addLayout(hsizer)

        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(self.btn_ok)
        hsizer.addWidget(self.btn_cancel)
        hsizer.addStretch()
        sizer.addLayout(hsizer)

        self.setLayout(sizer)
        ## self.resize(320,125)

    def accept(self):
        """final checks, transmit changes to parent"""
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
            self._parent.meldfout(fout)
            self.txt_name.setFocus()
            return
        if self.cb_ns.isChecked():
            seq = self.cmb_ns.currentIndex()
            if seq == 0:
                self._parent.meldfout('Namespace must be selected if checked')
                self.cb_ns.setFocus()
                return
            nam = '{{{}}}{}'.format(self.cmb_ns.itemText(seq), nam)
        self._parent.data["name"] = nam
        self._parent.data["value"] = self.txt_value.text()
        super().accept()

    ## def on_cancel(self):
        ## super().done(qtw.QDialog.Rejected)

    def keyPressEvent(self, event):
        """event handler voor toetsaanslagen"""
        if event.key() == core.Qt.Key_Escape:
            super().done(qtw.QDialog.Rejected)


class SearchDialog(qtw.QDialog):
    """Dialog to get search arguments
    """
    def __init__(self, parent, title=""):
        super().__init__(parent)
        self.setWindowTitle(title)
        self._parent = parent
        if self._parent.editor.search_args:
            ele_name, attr_name, attr_val, text_val = self._parent.editor.search_args
        else:
            ele_name = attr_name = attr_val = text_val = ''

        sizer = qtw.QVBoxLayout()
        gsizer = qtw.QGridLayout()

        self.cb_element = qtw.QLabel('Element', self)
        gsizer.addWidget(self.cb_element, 0, 0)
        vsizer = qtw.QVBoxLayout()
        hsizer = qtw.QHBoxLayout()
        lbl_element = qtw.QLabel("name:", self)
        hsizer.addWidget(lbl_element)
        self.txt_element = qtw.QLineEdit(self)
        hsizer.addWidget(self.txt_element)
        vsizer.addLayout(hsizer)
        gsizer.addLayout(vsizer, 0, 1)

        vsizer = qtw.QVBoxLayout()
        self.cb_attr = qtw.QLabel('Attribute', self)
        vsizer.addWidget(self.cb_attr)
        gsizer.addLayout(vsizer, 1, 0)
        vsizer = qtw.QVBoxLayout()
        hsizer = qtw.QHBoxLayout()
        lbl_attr_name = qtw.QLabel("name:", self)
        hsizer.addWidget(lbl_attr_name)
        self.txt_attr_name = qtw.QLineEdit(self)
        hsizer.addWidget(self.txt_attr_name)
        vsizer.addLayout(hsizer)
        gsizer.addLayout(vsizer, 1, 1)
        vsizer = qtw.QVBoxLayout()
        hsizer = qtw.QHBoxLayout()
        lbl_attr_val = qtw.QLabel("value:", self)
        hsizer.addWidget(lbl_attr_val)
        self.txt_attr_val = qtw.QLineEdit(self)
        hsizer.addWidget(self.txt_attr_val)
        vsizer.addLayout(hsizer)
        gsizer.addLayout(vsizer, 2, 1)

        self.cb_text = qtw.QLabel('Text', self)
        gsizer.addWidget(self.cb_text, 3, 0)
        hsizer = qtw.QHBoxLayout()
        lbl_text = qtw.QLabel("value:", self)
        hsizer.addWidget(lbl_text)
        self.txt_text = qtw.QLineEdit(self)
        hsizer.addWidget(self.txt_text)
        gsizer.addLayout(hsizer, 3, 1)
        sizer.addLayout(gsizer)

        hsizer = qtw.QHBoxLayout()
        self.lbl_search = qtw.QLabel('', self)
        hsizer.addWidget(self.lbl_search)
        sizer.addLayout(hsizer)
        self.lblsizer = hsizer

        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        self.btn_ok = qtw.QPushButton('&Ok', self)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_ok.setDefault(True)
        hsizer.addWidget(self.btn_ok)
        self.btn_cancel = qtw.QPushButton('&Cancel', self)
        self.btn_cancel.clicked.connect(self.reject)
        hsizer.addWidget(self.btn_cancel)
        self.btn_clear = qtw.QPushButton('C&lear Values', self)
        self.btn_clear.clicked.connect(self.clear_values)
        hsizer.addWidget(self.btn_clear)
        hsizer.addStretch()
        sizer.addLayout(hsizer)
        self.sizer = sizer

        self.setLayout(sizer)

        self.txt_element.textChanged.connect(self.set_search)
        self.txt_element.setText(ele_name)
        self.txt_attr_name.textChanged.connect(self.set_search)
        self.txt_attr_name.setText(attr_name)
        self.txt_attr_val.textChanged.connect(self.set_search)
        self.txt_attr_val.setText(attr_val)
        self.txt_text.textChanged.connect(self.set_search)
        self.txt_text.setText(text_val)

    def set_search(self):
        """build text describing search action"""
        out = ''
        ele = self.txt_element.text()
        attr_name = self.txt_attr_name.text()
        attr_val = self.txt_attr_val.text()
        text = self.txt_text.text()
        out = self._parent.editor.get_search_text(ele, attr_name, attr_val, text)
        self.lbl_search.setText('\n'.join(out))
        # self.layout()

    def clear_values(self):
        "set empty search values"
        self.txt_element.clear()
        self.txt_attr_name.clear()
        self.txt_attr_val.clear()
        self.txt_text.clear()
        self.lbl_search.setText('')
        self.lblsizer.update()  # is bedoeld om de dialoog te laten krimpen, maar werkt niet
        self.sizer.update()
        self.update()
        # self.adjustSize()

    def accept(self):
        """confirm dialog and pass changed data to parent"""
        ele = str(self.txt_element.text())
        attr_name = str(self.txt_attr_name.text())
        attr_val = str(self.txt_attr_val.text())
        text = str(self.txt_text.text())
        if not any((ele, attr_name, attr_val, text)):
            self._parent.meldfout('Please enter search criteria or press cancel')
            self.txt_element.setFocus()
            return

        self._parent.in_dialog = True
        self._parent.editor.search_args = (ele, attr_name, attr_val, text)
        super().accept()

    ## def on_cancel(self):
        ## super().done(qtw.QDialog.Rejected)


class VisualTree(qtw.QTreeWidget):
    """Tree widget subclass overriding some event handlers
    """
    def __init__(self, parent):
        self.parent = parent
        super().__init__()

    def mouseDoubleClickEvent(self, event):
        "reimplemented to reject when on root element"
        item = self.itemAt(event.x(), event.y())
        if item:
            if item == self.parent.top:
                edit = False
            else:
                ## data = str(item.text(0))
                edit = True
                ## if data.startswith(ELSTART):
                    ## if item.childCount() > 0:
                        ## edit = False
        if edit:
            self.parent.edit()
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        "reimplemented to show popup menu when applicable"
        xc, yc = event.x(), event.y()
        item = self.itemAt(xc, yc)
        if event.button() == core.Qt.RightButton:
            if item and item != self.parent.top:
                ## self.parent.setCurrentItem(item)
                menu = self.parent.init_menus(popup=True)
                menu.exec_(core.QPoint(xc, yc))
        else: #left click
            self.parent.set_selected_item(item)
        
        event.ignore()


class UndoRedoStack(qtw.QUndoStack):
    """Undo stack subclass overriding some event handlers
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.cleanChanged.connect(self.clean_changed)
        self.indexChanged.connect(self.index_changed)
        self.maxundo = self.undoLimit()
        self.setUndoLimit(1)  # self.unset_undo_limit(False)
        ## log('Undo limit {}'.format(self.undoLimit()))
        win = self.parent()
        win.undo_item.setText('Nothing to undo')
        win.redo_item.setText('Nothing to redo')
        win.undo_item.setDisabled(True)
        win.redo_item.setDisabled(True)

    def unset_undo_limit(self, state):
        """change undo limit"""
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
        """change text of undo/redo menuitems according to stack change"""
        ## print('undo stack status changed:', state)
        win = self.parent()
        if state:
            win.undo_item.setText('Nothing to undo')
        win.undo_item.setDisabled(state)

    def index_changed(self):  # , num): currently only change from 1 to unlimited and back
        """change text of undo/redo menuitems according to stack change"""
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


# UndoCommand subclasses
class PasteElementCommand(qtw.QUndoCommand):
    """subclass to make Undo/Redo possible"""
    def __init__(self, win, tag, text, before, below, description="",
                 data=None, where=None):
        """
        "where we are" is optional because it can be determined from the current
        position but it should also be possible to provide it
        """
        self.win = win          # treewidget
        self.tag = tag          # element name
        self.data = text        # element text
        self.before = before    # switch
        self.below = below      # switch
        self.children = data
        self.where = where
        self.replaced = None    # in case item is replaced while redoing
        if below:
            description += ' Under'
        elif before:
            description += ' Before'
        else:
            description += ' After'
        log("init {} {} {}".format(description, self.tag, self.data))  # , self.item)
        self.first_edit = not self.win.editor.tree_dirty
        super().__init__(description)

    def redo(self):
        "((Re)Do add element"
        def zetzeronder(node, data, before=False, below=True):
            "add elements recursively"
            log('zetzeronder voor node {} met data {}'.format(node, data))
            text, data, children = data
            tag, value = data
            is_attr = False if text.startswith(ELSTART) else True
            add_under = self.win.editor.add_item(node, tag, value, before=before, below=below,
                                                 attr=is_attr)
            below = True
            for item in children:
                zetzeronder(add_under, item)
            return add_under
        print('redo of add')
        print('    tag is', self.tag)
        print('    data is', self.data)
        print('    before is', self.before)
        print('    below is', self.below)
        print('    where is', self.where)
        log('In paste element redo for tag {} data {}'.format(self.tag, self.data))
        self.added = self.win.editor.add_item(self.where, self.tag, self.data, before=self.before,
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
        "Undo add element"
        # essentially 'cut' Command
        log('In paste element undo for added: {}'.format(self.added))
        self.replaced = self.added   # remember original item in case redo replaces it
        item = CopyElementCommand(self.win, self.added, cut=True, retain=False,
                                  description=__doc__)
        item.redo()
        if self.first_edit:
            self.win.editor.mark_dirty(False)
        self.win.statusbar.showMessage('{} undone'.format(self.text()))


class PasteAttributeCommand(qtw.QUndoCommand):
    """subclass to make Undo/Redo possible"""
    def __init__(self, win, name, value, item, description=""):
        super().__init__(description)
        self.win = win          # treewidget
        self.item = item        # where we are now
        self.name = name        # attribute name
        self.value = value      # attribute value
        log("init {} {} {} {}".format(description, self.name, self.value, self.item))
        self.first_edit = not self.win.editor.tree_dirty
        super().__init__(description)

    def redo(self):
        "(Re)Do add attribute"
        log('(redo) add attr {} {} {}'.format(self.name, self.value, self.item))
        self.added = self.win.editor.add_item(self.item, self.name, self.value, attr=True)
        self.win.tree.expandItem(self.added.parent())
        log('Added {}'.format(self.added))

    def undo(self):
        "Undo add attribute"
        # essentially 'cut' Command
        item = CopyElementCommand(self.win, self.added, cut=True, retain=False,
                                  description=__doc__)
        item.redo()
        if self.first_edit:
            self.win.editor.mark_dirty(False)
        self.win.statusbar.showMessage('{} undone'.format(self.text()))


class EditCommand(qtw.QUndoCommand):
    """subclass to make Undo/Redo possible"""
    def __init__(self, win, old_state, new_state, description=""):
        log("building editcommand for {}".format(description))
        super().__init__(description)
        self.win = win
        self.item = self.win.item
        self.old_state = old_state
        self.new_state = new_state
        self.first_edit = not self.win.editor.tree_dirty

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
            self.win.editor.mark_dirty(False)
        self.win.statusbar.showMessage('{} undone'.format(self.text()))


class CopyElementCommand(qtw.QUndoCommand):
    """subclass to make Undo/Redo possible"""
    def __init__(self, win, item, cut, retain, description=""):
        super().__init__(description)
        self.undodata = None
        self.win = win      # treewidget
        self.item = item    # where we are now
        self.tag = str(self.item.text(1))
        self.data = str(self.item.text(2))  # name and text
        log("init {} {} {} {}".format(description, self.tag, self.data, self.item))
        self.cut = cut
        self.retain = retain
        self.first_edit = not self.win.editor.tree_dirty

    def redo(self):
        "(Re)Do Copy Element"
        def push_el(el, result):
            "do this recursively"
            text = str(el.text(0))
            data = (str(el.text(1)), str(el.text(2)))
            children = []
            for ix in range(el.childCount()):
                subel = el.child(ix)
                push_el(subel, children)
            result.append((text, data, children))
            return result
        log('In copy element redo for item {} with data {}'.format(self.item,
                                                                   self.data))
        print("redo of ", self.item)
        if self.undodata is None:
            print('building reference data')
            self.parent = self.item.parent()
            self.loc = self.parent.indexOfChild(self.item)
            self.undodata = push_el(self.item, [])
            if self.loc > 0:
                self.prev = self.parent.child(self.loc - 1)
            else:
                self.prev = self.parent
                if self.prev == self.win.editor.rt:
                    self.prev = self.parent.child(self.loc + 1)
            print('   parent:', self.parent)
            print('   location:', self.loc)
            print('   undodata:', self.undodata)
            print('   pointer fallback:', self.prev)
        if self.retain:
            log('Retaining item')
            self.win.cut_el = self.undodata
            self.win.cut_att = None
            self.win.enable_pasteitems(True)
        if self.cut:
            log('cutting item from parent {}'.format(self.parent))
            self.parent.removeChild(self.item)
            self.item = self.prev
            self.win.tree.setCurrentItem(self.prev)

    def undo(self):
        "Undo Copy Element"
        log('In copy element undo for tag {} data {} item {}'.format(self.tag, self.data,
                                                                     self.item))
        # self.cut_el = None
        if self.cut:
            print('undo of', self.item)
            if self.loc >= self.parent.childCount():
                item = PasteElementCommand(self.win, self.tag, self.data,
                                           before=False, below=True, data=self.undodata,
                                           description=__doc__, where=self.parent)
            else:
                item = PasteElementCommand(self.win, self.tag, self.data,
                                           before=True, below=False, data=self.undodata,
                                           description=__doc__,
                                           where=self.parent.child(self.loc))
            item.redo()  # add_under=add_under, loc=self.loc)
            self.item = item.added
        if self.first_edit:
            self.win.editor.mark_dirty(False)
        self.win.statusbar.showMessage('{} undone'.format(self.text()))
        ## self.win.tree.setCurrentItem(self.item)


class CopyAttributeCommand(qtw.QUndoCommand):
    """subclass to make Undo/Redo possible"""
    def __init__(self, win, item, cut, retain, description):
        super().__init__(description)
        self.win = win      # treewidget
        self.item = item    # where we are now
        self.name = str(self.item.text(1))
        self.value = str(self.item.text(2))  # name and text
        log("init {} {} {} {}".format(description, self.name, self.value, self.item))
        self.cut = cut
        self.retain = retain
        self.first_edit = not self.win.editor.tree_dirty

    def redo(self):
        "(re)do copy attribute"
        log('copying item {} with text {}'.format(self.item, self.value))
        self.parent = self.item.parent()
        self.loc = self.parent.indexOfChild(self.item)
        if self.retain:
            log('Retaining attribute')
            self.win.cut_el = None
            self.win.cut_att = (self.name, self.value)
            self.win.enable_pasteitems(True)
        if self.cut:
            log('cutting attribute')
            ix = self.loc
            if ix > 0:
                prev = self.parent.child(ix - 1)
            else:
                prev = self.parent
                if prev == self.win.editor.rt:
                    prev = self.parent.child(ix + 1)
            self.parent.removeChild(self.item)
            self.item = None
            self.win.tree.setCurrentItem(prev)

    def undo(self):
        "Undo Copy attribute"
        log('{} for {} {} {}'.format(__doc__, self.name, self.value, self.item))
        # self.win.cut_att = None
        if self.cut:
            item = PasteAttributeCommand(self.win, self.name, self.value, self.parent,
                                         description=__doc__)
            item.redo()
            self.item = item.added
        if self.first_edit:
            self.win.editor.mark_dirty(False)
        self.win.statusbar.showMessage('{} undone'.format(self.text()))


## class MainFrame(qtw.QMainWindow, AxeMixin):
class Gui(qtw.QMainWindow):
    "Main application window"
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

    def __init__(self, parent=None, fn=''):
        self.editor = parent
        self.app = qtw.QApplication(sys.argv)
        self.fn = fn
        super().__init__()
        self.show()

    def go(self):
        "start application event loop"
        sys.exit(self.app.exec_())

    # reimplemented methods from QMainWindow
    def keyReleaseEvent(self, event):
        "reimplemented: keyboard event handler"
        skip = self.on_keyup(event)
        if not skip:
            super().keyReleaseEvent(event)

    def closeEvent(self, event):
        """reimplemented close event handler: check if data was modified"""
        test = self.editor.check_tree()
        if test:
            event.accept()
        else:
            event.ignore()

    # helper methods for getting/setting data in visual tree
    # self is passed in for compatibility with similar methods for e.g. wx version
    def get_node_children(self, node):
        "return descendants of the given node"
        return [node.child(i) for i in range(node.childCount())]

    def get_node_title(self, node):
        "return the title of the given node"
        return node.text(0)

    def get_node_data(self, node):
        "return data (element name and text/CDATA) associated with the given node"
        return node.text(1), node.text(2)

    def get_treetop(self):
        "return the visual tree's root element"
        top = self.tree.topLevelItem(0)
        rt = top.child(0)
        if rt.text(0) == 'namespaces':
            rt = top.child(1)
        return rt

    def setup_new_tree(self, title):
        "build new visual tree and return its root element"
        self.tree.clear()  # DeleteAllItems()
        self.undo_stack.clear()
        self.top = qtw.QTreeWidgetItem()
        self.top.setText(0, title)
        self.tree.addTopLevelItem(self.top)  # AddRoot(titel)
        return self.top

    def add_node_to_parent(self, parent, pos=-1):
        "add a new descendant to an element at the given position and return it"
        node = qtw.QTreeWidgetItem()
        if pos == -1:
            parent.addChild(node)
        else:
            parent.insertChild(pos, node)
        return node

    def set_node_title(self, node, title):
        "set the title for the given node"
        node.setText(0, title)

    def get_node_parentpos(self, node):
        "return the parent of the given node and its position under it"
        parent = node.parent()
        pos = parent.indexOfChild(node)
        return parent, pos

    def set_node_data(self, node, name, value):
        "set the data (element name, text/CDATA) associated with the given node"
        node.setText(1, name)
        node.setText(2, value)

    def get_selected_item(self):
        "return the currently selected item"
        return self.tree.currentItem()

    def set_selected_item(self, item):
        "set the currently selected item to the given item"
        self.tree.setCurrentItem(item)

    def is_node_root(self, item=None):
        "check if the given element is the visual tree's root and return the result"
        if not item:
            item = self.item
        if (item.text(1), item.text(2)) == (self.editor.rt.tag, self.editor.rt.text or ""):
            return True
        return False

    def expand_item(self, item=None):
        "expand a tree item"
        def expand_with_children(item):
            "do it recursively"
            self.tree.expandItem(item)
            for ix in range(item.childCount()):
                expand_with_children(item.child(ix))
        if not item:
            item = self.tree.currentItem()
        if item:
            expand_with_children(item)
            self.tree.resizeColumnToContents(0)

    def collapse_item(self, item=None):
        "collapse tree item"
        if not item:
            item = self.tree.currentItem()
        if item:
            self.tree.collapseItem(item)    # mag eventueel recursief in overeenstemming met vorige
            self.tree.resizeColumnToContents(0)

    def edit_item(self, item):
        "edit an element or attribute"
        self.item = item
        data = str(self.item.text(0))  # self.item.get_text()
        if data.startswith(ELSTART):
            tag, text = str(self.item.text(1)), str(self.item.text(2))
            state = data, tag, text   # current values to be passed to UndoAction
            data = {'item': self.item, 'tag': tag}
            if text:
                data['data'] = True
                data['text'] = text
            edt = ElementDialog(self, title='Edit an element', item=data).exec_()
            if edt == qtw.QDialog.Accepted:
                name = self.editor.getshortname((self.data["tag"], self.data["text"]))
                new_state = name, self.data["tag"], self.data["text"]
                log('calling editcommand for element')
                command = EditCommand(self, state, new_state, "Edit Element")
                self.undo_stack.push(command)
                self.editor.mark_dirty(True)
        else:
            nam, val = str(self.item.text(1)), str(self.item.text(2))
            state = data, nam, val   # current values to be passed to UndoAction
            data = {'item': self.item, 'name': nam, 'value': val}
            edt = AttributeDialog(self, title='Edit an attribute', item=data).exec_()
            if edt == qtw.QDialog.Accepted:
                name = self.editor.getshortname((self.data["name"], self.data["value"]), attr=True)
                new_state = name, self.data["name"], self.data["value"]
                log('calling editcommand for attribute')
                command = EditCommand(self, state, new_state, "Edit Attribute")
                self.undo_stack.push(command)
                self.editor.mark_dirty(True)

    def copy(self, item, cut=False, retain=True):
        """execute cut/delete/copy action"""
        self.item = item
        txt = self.editor.get_copy_text(cut, retain)
        if self.item.text(0).startswith(ELSTART):
            command = CopyElementCommand(self, self.item, cut, retain, "{} Element".format(txt))
        else:
            command = CopyAttributeCommand(self, self.item, cut, retain, "{} Attribute".format(txt))
        self.undo_stack.push(command)
        if cut:
            self.editor.mark_dirty(True)
            ## self.tree.setCurrentItem(prev)

    def paste(self, item, before=True, below=False):
        """execute paste action"""
        self.item = item
        if self.cut_att:
            name, value = self.cut_att
            command = PasteAttributeCommand(self, name, value, self.item,
                                            description="Paste Attribute")
            self.undo_stack.push(command)
        elif self.cut_el:
            tag, text = self.cut_el[0][1]
            command = PasteElementCommand(self, tag, text,
                                          before=before, below=below, where=self.item,
                                          description="Paste Element",
                                          data=self.cut_el)
            self.undo_stack.push(command)
        self.editor.mark_dirty(True)

    def add_attribute(self, item):
        "ask for attibute, then start add action"
        self.item = item
        edt = AttributeDialog(self, title="New attribute").exec_()
        if edt == qtw.QDialog.Accepted:
            command = PasteAttributeCommand(self, self.data["name"], self.data["value"],
                                            self.item, "Insert Attribute")
            self.undo_stack.push(command)
            self.editor.mark_dirty(True)

    def insert(self, item, before=True, below=False):
        """execute insert action"""
        self.item = item
        edt = ElementDialog(self, title="New element").exec_()
        if edt == qtw.QDialog.Accepted:
            command = PasteElementCommand(self, self.data['tag'], self.data['text'],
                                          before=before, below=below, where=self.item,
                                          description="Insert Element")
            self.undo_stack.push(command)
            self.editor.mark_dirty(True)

    # internals
    def init_gui(self):
        """Deze methode wordt aangeroepen door de __init__ van de mixin class
        """
        ## self.parent = parent
        ## qtw.QMainWindow.__init__(self, parent) # aparte initialisatie net als voor mixin
        self._icon = gui.QIcon(axe_iconame)
        self.resize(620, 900)
        self.setWindowIcon(self._icon)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        self.init_menus()

        self.tree = VisualTree(self)
        self.tree.headerItem().setHidden(True)
        self.setCentralWidget(self.tree)
        self.enable_pasteitems(False)
        self.undo_stack = UndoRedoStack(self)
        self.editor.mark_dirty(False)
        self.in_dialog = False

    def set_windowtitle(self, text):
        """set screen title
        """
        self.setWindowTitle(text)

    def get_windowtitle(self):
        """get screen title
        """
        return self.windowTitle()

    def init_menus(self, popup=False):
        """setup application menu"""
        if popup:
            viewmenu = qtw.QMenu("&View")
        else:
            self.filemenu_actions, self.viewmenu_actions = [], []
            self.editmenu_actions, self.searchmenu_actions = [], []
            for ix, menudata in enumerate(self.editor.get_menu_data()):
                for text, callback, shortcuts in menudata:
                    act = qtw.QAction(text, self)
                    act.triggered.connect(callback)
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
            act = qtw.QAction('&Unlimited Undo', self)
            act.triggered.connect(self.limit_undo)
            self.filemenu_actions.insert(-1, act)
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
        return filemenu, viewmenu, editmenu

    def meldinfo(self, text):
        """notify about some information"""
        self.in_dialog = True
        qtw.QMessageBox.information(self, self.editor.title, text)

    def meldfout(self, text, abort=False):
        """notify about an error"""
        self.in_dialog = True
        qtw.QMessageBox.critical(self, self.editor.title, text)
        if abort:
            self.quit()

    def ask_yesnocancel(self, prompt):
        """stelt een vraag en retourneert het antwoord
        1 = Yes, 0 = No, -1 = Cancel
        """
        retval = dict(zip((qtw.QMessageBox.Yes, qtw.QMessageBox.No,
                           qtw.QMessageBox.Cancel), (1, 0, -1)))
        self.in_dialog = True
        h = qtw.QMessageBox.question(
            self, self.editor.title, prompt,
            qtw.QMessageBox.Yes | qtw.QMessageBox.No | qtw.QMessageBox.Cancel,
            defaultButton=qtw.QMessageBox.Yes)
        return retval[h]

    def ask_for_text(self, prompt, value=''):
        """vraagt om tekst en retourneert het antwoord"""
        self.in_dialog = True
        data, *_ = qtw.QInputDialog.getText(self, self.editor.title, prompt,
                                            qtw.QLineEdit.Normal, value)
        return data

    def file_to_read(self):
        """ask for file to load"""
        fnaam, *_ = qtw.QFileDialog.getOpenFileName(self, "Choose a file",
                                                    os.getcwd(), HMASK)
        ok = bool(fnaam)
        return ok, str(fnaam)

    def file_to_save(self):
        """ask for file to save"""
        name, *_ = qtw.QFileDialog.getSaveFileName(self, "Save file as ...", self.editor.xmlfn,
                                                   HMASK)
        ok = bool(name)
        return ok, str(name)

    def enable_pasteitems(self, active=False):
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

    def limit_undo(self):
        "set undo limit"
        newstate = self.setundo_action.isChecked()
        self.undo_stack.unset_undo_limit(newstate)
        if newstate:
            self.meldinfo(self.undoredowarning)

    def popupmenu(self, item):
        """call up menu"""
        log('self.popupmenu called')
        menu = self.init_menus(popup=True)
        menu.exec_(self.tree.mapToGlobal(self.tree.visualItemRect(item).bottomRight()))

    def quit(self):
        "close the application"
        self.close()

    def on_keyup(self, ev=None):
        "handle keyboard event"
        ky = ev.key()
        item = self.tree.currentItem()
        skip = False
        if item and item != self.top:
            if ky == core.Qt.Key_Return:
                if self.in_dialog:
                    self.in_dialog = False
                else:
                    if item.childCount() > 0:
                        if item.isExpanded():
                            self.tree.collapseItem(item)
                            self.tree.setCurrentItem(item.parent())
                        else:
                            self.tree.expandItem(item)
                            self.tree.setCurrentItem(item.child(0))
                    ## else:
                        ## self.edit()
                skip = True
            elif ky == core.Qt.Key_Backspace:
                if item.isExpanded():
                    self.tree.collapseItem(item)
                    self.tree.setCurrentItem(item.parent())
                skip = True
            elif ky == core.Qt.Key_Menu:
                self.popupmenu(item)
                skip = True
        return skip

    def get_search_args(self):
        """send dialog to get search argument(s)
        """
        # self.search_args = []
        edt = SearchDialog(self, title='Search options').exec_()
        if edt == qtw.QDialog.Accepted:
            # self.editor.search_args = self.search_args
            return True
        return False

    def do_undo(self):
        "undo action"
        self.undo_stack.undo()

    def do_redo(self):
        "(re)do action"
        self.undo_stack.redo()
