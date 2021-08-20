"""aangepaste versie van tree-based XML-editor, bedoeld als read-only en een
ietsje verder platgeslagen weergave
"""
import os
import sys
## import functools
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as gui
import PyQt5.QtCore as core
from .axe_base import getshortname, find_next, log, TITEL, axe_iconame, AxeMixin
TITEL = TITEL.replace('editor', 'viewer')
if os.name == "nt":
    HMASK = "XML files (*.xml);;All files (*.*)"
elif os.name == "posix":
    HMASK = "XML files (*.xml *.XML);;All files (*.*)"
IMASK = "All files (*.*)"


def calculate_location(win, node):
    """attempt to calculate some kind of identification for a tree node

    this function returns a tuple of subsequent indices of a child under its parent.
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
    itemdict = element.data(0, core.Qt.UserRole)
    if itemdict:
        elem_list = [(element, itemdict['tag'], itemdict['text'] or '', itemdict['attrs'])]
    else:
        elem_list = [(element, '', '', [])]
    subel_list = []
    for seq in range(element.childCount()):
        subitem = element.child(seq)
        subel_list = flatten_tree(subitem)
        elem_list.extend(subel_list)
    return elem_list


# Dialog windows
class SearchDialog(qtw.QDialog):
    """Dialog to get search arguments
    """
    def __init__(self, parent, title=""):
        super().__init__(parent)
        self.setWindowTitle(title)
        self._parent = parent

        self.cb_element = qtw.QLabel('Element', self)
        lbl_element = qtw.QLabel("name:", self)
        self.txt_element = qtw.QLineEdit(self)
        self.txt_element.textChanged.connect(self.set_search)

        self.cb_attr = qtw.QLabel('Attribute', self)
        lbl_attr_name = qtw.QLabel("name:", self)
        self.txt_attr_name = qtw.QLineEdit(self)
        self.txt_attr_name.textChanged.connect(self.set_search)
        lbl_attr_val = qtw.QLabel("value:", self)
        self.txt_attr_val = qtw.QLineEdit(self)
        self.txt_attr_val.textChanged.connect(self.set_search)

        self.cb_text = qtw.QLabel('Text', self)
        lbl_text = qtw.QLabel("value:", self)
        self.txt_text = qtw.QLineEdit(self)
        self.txt_text.textChanged.connect(self.set_search)

        self.lbl_search = qtw.QLabel('', self)

        self.btn_ok = qtw.QPushButton('&Ok', self)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_ok.setDefault(True)
        self.btn_cancel = qtw.QPushButton('&Cancel', self)
        self.btn_cancel.clicked.connect(self.reject)

        sizer = qtw.QVBoxLayout()

        gsizer = qtw.QGridLayout()

        gsizer.addWidget(self.cb_element, 0, 0)
        vsizer = qtw.QVBoxLayout()
        hsizer = qtw.QHBoxLayout()
        hsizer.addWidget(lbl_element)
        hsizer.addWidget(self.txt_element)
        vsizer.addLayout(hsizer)
        gsizer.addLayout(vsizer, 0, 1)

        vsizer = qtw.QVBoxLayout()
        vsizer.addSpacing(5)
        vsizer.addWidget(self.cb_attr)
        vsizer.addStretch()
        gsizer.addLayout(vsizer, 1, 0)
        vsizer = qtw.QVBoxLayout()
        hsizer = qtw.QHBoxLayout()
        hsizer.addWidget(lbl_attr_name)
        hsizer.addWidget(self.txt_attr_name)
        vsizer.addLayout(hsizer)
        hsizer = qtw.QHBoxLayout()
        hsizer.addWidget(lbl_attr_val)
        hsizer.addWidget(self.txt_attr_val)
        vsizer.addLayout(hsizer)
        gsizer.addLayout(vsizer, 1, 1)

        gsizer.addWidget(self.cb_text, 2, 0)
        hsizer = qtw.QHBoxLayout()
        hsizer.addWidget(lbl_text)
        hsizer.addWidget(self.txt_text)
        gsizer.addLayout(hsizer, 2, 1)
        sizer.addLayout(gsizer)

        hsizer = qtw.QHBoxLayout()
        hsizer.addWidget(self.lbl_search)
        sizer.addLayout(hsizer)

        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(self.btn_ok)
        hsizer.addWidget(self.btn_cancel)
        hsizer.addStretch()
        sizer.addLayout(hsizer)

        self.setLayout(sizer)

    def set_search(self):
        """build text describing search action"""
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

    def accept(self):
        """confirm dialog and pass changed data to parent"""
        ele = str(self.txt_element.text())
        attr_name = str(self.txt_attr_name.text())
        attr_val = str(self.txt_attr_val.text())
        text = str(self.txt_text.text())
        if not any((ele, attr_name, attr_val, text)):
            self._parent._meldfout('Please enter search criteria or press cancel')
            self.txt_element.setFocus()
            return

        self._parent.search_args = (ele, attr_name, attr_val, text)
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


class MainFrame(qtw.QMainWindow, AxeMixin):
    """Main application window
    """
    def __init__(self, fn=''):
        self.fn = fn
        super().__init__()
        self.show()

    # reimplemented methods from Mixin
    # mostly because of including the gui event in the signature
    def openxml(self, ev=None):
        AxeMixin.openxml(self, skip_check=True)

    def init_tree(self, root, prefixes=None, uris=None, name=''):
        "set up display tree"
        def add_to_tree(el, rt):
            "recursively add elements"
            self.item = rt
            rr = self._add_item(el)
            ## log(calculate_location(self, rr))
            # for attr in el.keys():
            #     h = el.get(attr)
            #     if not h:
            #         h = '""'
            #     self.item = rr
            #     self._add_item(attr, h, attr=True)
            for subel in list(el):
                add_to_tree(subel, rr)

        self.tree.clear()  # DeleteAllItems()
        titel = AxeMixin.init_tree(self, root, prefixes, uris, name)
        self.top = qtw.QTreeWidgetItem()
        self.top.setText(0, titel)
        self.tree.addTopLevelItem(self.top)  # AddRoot(titel)
        self.setWindowTitle(" - ".join((os.path.basename(titel), TITEL)))
        if not root:
            return
        # eventuele namespaces toevoegen
        namespaces = False
        for ix, prf in enumerate(self.ns_prefixes):
            if not namespaces:
                ns_root = qtw.QTreeWidgetItem(['namespaces'])
                self.top.addChild(ns_root)
                namespaces = True
            ns_item = qtw.QTreeWidgetItem()
            ns_item.setText(0, '{}: {}'.format(prf, self.ns_uris[ix]))
            ns_root.addChild(ns_item)
        self.item = self.top
        rt = self._add_item(self.rt)
        for el in list(self.rt):
            add_to_tree(el, rt)

    # internals
    def _init_gui(self):
        """Deze methode wordt aangeroepen door de __init__ van de mixin class
        """
        ## self.parent = parent
        ## qtw.QMainWindow.__init__(self, parent) # aparte initialisatie net als voor mixin
        self._icon = gui.QIcon(axe_iconame)
        self.resize(620, 900)
        self.setWindowIcon(self._icon)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        self._init_menus()

        self.tree = VisualTree(self)
        self.tree.headerItem().setHidden(True)
        self.setCentralWidget(self.tree)
        self.in_dialog = False

    def _init_menus(self, popup=False):
        """setup application menu"""
        if popup:
            viewmenu = qtw.QMenu("&View")
        else:
            self.filemenu_actions, self.viewmenu_actions = [], []
            self.editmenu_actions, self.searchmenu_actions = [], []
            for ix, menudata in enumerate((
                    (
                        ("&Open", self.openxml, 'Ctrl+O'),
                        ('E&xit', self.quit, 'Ctrl+Q'),
                    ),
                    (
                        ("&Expand All (sub)Levels", self.expand, 'Ctrl++'),
                        ("&Collapse All (sub)Levels", self.collapse, 'Ctrl+-'),
                    ),
                    (
                        ("&Find", self.search, 'Ctrl+F'),
                        ("Find &Last", self.search_last, 'Shift+Ctrl+F'),
                        ("Find &Next", self.search_next, 'F3'),
                        ("Find &Previous", self.search_prev, 'Shift+F3'),
                    ))):
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
                        self.searchmenu_actions.append(act)

            menubar = self.menuBar()
            filemenu = menubar.addMenu("&File")
            for act in self.filemenu_actions:
                filemenu.addAction(act)
            viewmenu = menubar.addMenu("&View")
        for act in self.viewmenu_actions:
            viewmenu.addAction(act)

        if popup:
            searchmenu = viewmenu
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
        """notify about some information"""
        self.in_dialog = True
        qtw.QMessageBox.information(self, self.title, text)

    def _meldfout(self, text, abort=False):
        """notify about an error"""
        self.in_dialog = True
        qtw.QMessageBox.critical(self, self.title, text)
        if abort:
            self.quit()

    def _ask_yesnocancel(self, prompt):
        """stelt een vraag en retourneert het antwoord
        1 = Yes, 0 = No, -1 = Cancel
        """
        retval = dict(zip((qtw.QMessageBox.Yes, qtw.QMessageBox.No,
                           qtw.QMessageBox.Cancel), (1, 0, -1)))
        self.in_dialog = True
        h = qtw.QMessageBox.question(
            self, self.title, prompt,
            qtw.QMessageBox.Yes | qtw.QMessageBox.No | qtw.QMessageBox.Cancel,
            defaultButton=qtw.QMessageBox.Yes)
        return retval[h]

    def _ask_for_text(self, prompt):
        """vraagt om tekst en retourneert het antwoord"""
        self.in_dialog = True
        data, *_ = qtw.QInputDialog.getText(self, self.title, prompt,
                                            qtw.QLineEdit.Normal, "")
        return data

    def _file_to_read(self):
        """ask for file to load"""
        fnaam, *_ = qtw.QFileDialog.getOpenFileName(self, "Choose a file",
                                                    os.getcwd(), HMASK)
        ok = bool(fnaam)
        return ok, str(fnaam)

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

    def _add_item(self, element):  # , before=False, below=True, attr=False):
        """execute adding of item"""
        name, value, attrs = element.tag, element.text, element.items()
        itemdict = {"tag": name, "text": value, "attrs": attrs}
        log('in _add_item for {} value {} attrs {}'.format(name, value, attrs))
        if value is None:
            value = ""
        itemtext = getshortname(((name, value), self.ns_prefixes, self.ns_uris))
        new = qtw.QTreeWidgetItem()
        new.setText(0, itemtext)
        new.setData(0, core.Qt.UserRole, itemdict)
        tooltiptext = value
        if itemdict['attrs']:
            tooltiptext += '\n--------------------\n' + '\n'.join(
                ["{}: {}".format(x, y) for x, y in sorted(itemdict['attrs'])])
        new.setToolTip(0, tooltiptext)
        log('add under {}'.format(self.item))
        self.item.addChild(new)
        return new

    # exposed
    def popupmenu(self, item):
        """call up menu"""
        log('self.popupmenu called')
        menu = self._init_menus(popup=True)
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

    def expand(self):
        "expand a tree item"
        def expand_with_children(item):
            "do it recursively"
            self.tree.expandItem(item)
            for ix in range(item.childCount()):
                expand_with_children(item.child(ix))
        item = self.tree.currentItem()
        if item:
            expand_with_children(item)
            self.tree.resizeColumnToContents(0)

    def collapse(self):
        "collapse tree item"
        item = self.tree.currentItem()
        if item:
            self.tree.collapseItem(item)    # mag eventueel recursief in overeenstemming met vorige
            self.tree.resizeColumnToContents(0)

    def search(self, reverse=False):
        "start search after asking for options"
        self._search_pos = None
        edt = SearchDialog(self, title='Search options').exec_()
        if edt == qtw.QDialog.Accepted:
            self.search_next(reverse)
            ## found, is_attr = find_next(flatten_tree(self.top), self.search_args,
                ## reversed) # self.tree.top.child(0)
            ## if found:
                ## self.tree.setCurrentItem(found)
                ## self._search_pos = (found, is_attr)

    def search_last(self):
        "start backwards search"
        self.search(reverse=True)

    def search_next(self, reverse=False):
        "find (default is forward)"
        found, is_attr = find_next(flatten_tree(self.top), self.search_args,
                                   reverse, self._search_pos)  # self.tree.top.child(0)
        if found:
            self.tree.setCurrentItem(found)
            self._search_pos = (found, is_attr)
        else:
            self._meldinfo('Niks (meer) gevonden')

    def search_prev(self):
        "find backwards"
        self.search_next(reverse=True)


def axe_gui(args):
    "start up the editor"
    app = qtw.QApplication(sys.argv)
    if len(args) > 1:
        MainFrame(fn=" ".join(args[1:]))
    else:
        MainFrame()
    sys.exit(app.exec_())


if __name__ == "__main__":
    axe_gui(sys.argv)
