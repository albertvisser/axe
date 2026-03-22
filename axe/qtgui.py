"""PyQT5 versie van een op een treeview gebaseerde XML-editor
"""
import os
import sys
## import functools
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as gui
import PyQt6.QtCore as core
# from .shared import ELSTART, axe_iconame, log
HMASK = {"nt": "XML files (*.xml);;All files (*.*)",
         "posix": "XML files (*.xml *.XML);;All files (*.*)"}
IMASK = "All files (*.*)"


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

    def __init__(self, parent=None, fn='', readonly=False):
        self.editor = parent
        self.app = qtw.QApplication(sys.argv)
        self.fn = fn
        self.editable = not readonly
        super().__init__()
        self.show()

    def go(self):
        "start application event loop"
        sys.exit(self.app.exec())

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
        "return the visual tree's root element (below the filename)"
        top = self.tree.topLevelItem(0)
        rt = top.child(0)
        if rt.text(0) == 'namespaces':
            rt = top.child(1)
        return rt

    def setup_new_tree(self, title):
        "build new visual tree and return its root element"
        self.tree.clear()  # DeleteAllItems()
        if self.editable:
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

    # def edit_item(self, item):
    def edit_item(self, item, oldstate, newstate, command_text):
        "edit an element or attribute"
        self.item = item
        # data = str(self.item.text(0))  # self.item.get_text()
        # if data.startswith(self.editor.elstart):
        #     tag, text = str(self.item.text(1)), str(self.item.text(2))
        #     state = data, tag, text   # current values to be passed to UndoAction
        #     data = {'item': self.item, 'tag': tag}
        #     if text:
        #         data['data'] = True
        #         data['text'] = text
        #     edt = ElementDialog(self, title='Edit an element', item=data).exec()
        #     if edt == qtw.QDialog.DialogCode.Accepted:
        #         name = self.editor.getshortname((self.data["tag"], self.data["text"]))
        #         new_state = name, self.data["tag"], self.data["text"]
        #         # print('calling editcommand for element')
        #         command = EditCommand(self, state, new_state, "Edit Element")
        #         self.undo_stack.push(command)
        #         self.editor.mark_dirty(True)
        # else:
        #     nam, val = str(self.item.text(1)), str(self.item.text(2))
        #     state = data, nam, val   # current values to be passed to UndoAction
        #     data = {'item': self.item, 'name': nam, 'value': val}
        #     edt = AttributeDialog(self, title='Edit an attribute', item=data).exec()
        #     if edt == qtw.QDialog.DialogCode.Accepted:
        #         name = self.editor.getshortname((self.data["name"], self.data["value"]), attr=True)
        #         new_state = name, self.data["name"], self.data["value"]
        #         # print('calling editcommand for attribute')
        #         command = EditCommand(self, state, new_state, "Edit Attribute")
        #         self.undo_stack.push(command)
        #         self.editor.mark_dirty(True)
        command = EditCommand(self, oldstate, newstate, command_text)
        self.undo_stack.push(command)

    def copy(self, item, cut=False, retain=True):
        """execute cut/delete/copy action"""
        self.item = item
        txt = self.editor.get_copy_text(cut, retain)
        if self.item.text(0).startswith(self.editor.elstart):
            command = CopyElementCommand(self, self.item, cut, retain, f"{txt} Element")
        else:
            command = CopyAttributeCommand(self, self.item, cut, retain, f"{txt} Attribute")
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
        else:  # if self.cut_el:  als paste wordt gestart heeft een van beide een waiarde
            tag, text = self.cut_el[0][1]
            command = PasteElementCommand(self, tag, text, self.item, before=before, below=below,
                                          description="Paste Element", data=self.cut_el)
            self.undo_stack.push(command)
        self.editor.mark_dirty(True)

    def add_attribute(self, item, name, value, command_text):
        "ask for attibute, then start add action"
        # self.item = item
        # edt = AttributeDialog(self, title="New attribute").exec()
        # if edt == qtw.QDialog.DialogCode.Accepted:
        #     command = PasteAttributeCommand(self, self.data["name"], self.data["value"],
        #                                     self.item, "Insert Attribute")
        #     self.undo_stack.push(command)
        #     self.editor.mark_dirty(True)
        command = PasteAttributeCommand(self, name, value, item, command_text)
        self.undo_stack.push(command)

    def insert(self, item, tag, text, command_text, before=True, below=False):
        """execute insert action"""
        # self.item = item
        # edt = ElementDialog(self, title="New element").exec()
        # if edt == qtw.QDialog.DialogCode.Accepted:
        #     command = PasteElementCommand(self, self.data['tag'], self.data['text'],
        #                                   before=before, below=below, where=self.item,
        #                                   description="Insert Element")
        #     self.undo_stack.push(command)
        #     self.editor.mark_dirty(True)
        command = PasteElementCommand(self, tag, text, item, before=before, below=below,
                                      description=command_text)
        self.undo_stack.push(command)

    # internals
    def init_gui(self):
        """Deze methode wordt aangeroepen door de __init__ van de mixin class
        """
        self.icon = gui.QIcon(self.editor.iconame)
        self.resize(620, 900)
        self.setWindowIcon(self.icon)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        self.init_menus()

        self.tree = VisualTree(self)
        self.tree.headerItem().setHidden(True)
        self.setCentralWidget(self.tree)
        if self.editable:
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
        filemenu = viewmenu = editmenu = None
        if popup:
            viewmenu = qtw.QMenu("&View")
            menubar = None
        else:
            self.setup_menuactions()
            menubar = self.menuBar()
            filemenu = menubar.addMenu("&File")
            for act in self.filemenu_actions[:4]:
                filemenu.addAction(act)
            if self.editable:
                filemenu.addSeparator()
                filemenu.addAction(self.setundo_action)
                filemenu.addSeparator()
                filemenu.addAction(self.filemenu_actions[-1])
            viewmenu = menubar.addMenu("&View")
        for act in self.viewmenu_actions:
            viewmenu.addAction(act)

        if self.editable:
            editmenu = self.add_editactions_to_menu(popup, menubar, viewmenu)

        if popup:
            # searchmenu = editmenu if build_editmenu else viewmenu
            # searchmenu = editmenu if self.editable else viewmenu
            searchmenu = viewmenu
            searchmenu.addSeparator()
        else:
            searchmenu = menubar.addMenu("&Search")

        for act in self.searchmenu_actions:
            searchmenu.addAction(act)

        if popup:
            return searchmenu
        return filemenu, viewmenu, editmenu

    def setup_menuactions(self):
        """build lists with actions for the various submenus from the editor's menudata
        """
        self.filemenu_actions, self.viewmenu_actions = [], []
        self.editmenu_actions, self.searchmenu_actions = [], []
        for ix, menudata in enumerate(self.editor.get_menu_data()):
            for text, callback, shortcuts in menudata:
                act = gui.QAction(text, self)
                act.triggered.connect(callback)
                if shortcuts:
                    act.setShortcuts(list(shortcuts.split(',')))
                if ix == 0:
                    actions = self.filemenu_actions
                elif ix == 1:
                    actions = self.viewmenu_actions
                elif ix == 2:
                    actions = self.editmenu_actions if self.editable else self.searchmenu_actions
                else:  # if ix == 3:  momenteel zijn er maar 4 menu's gedefinieerd
                    actions = self.searchmenu_actions
                actions.append(act)
        if self.editable:
            act = gui.QAction('&Unlimited Undo', self)
            act.triggered.connect(self.limit_undo)
            self.filemenu_actions.insert(-1, act)
            self.undo_item, self.redo_item = self.editmenu_actions[0:2]
            self.pastebefore_item, self.pasteafter_item = self.editmenu_actions[6:8]
            self.pasteunder_item = self.editmenu_actions[8]
            self.setundo_action = self.filemenu_actions[-2]
            self.setundo_action.setCheckable(True)
            self.setundo_action.setChecked(False)

    def add_editactions_to_menu(self, popup, menubar, viewmenu):
        """update the menu in editable mode
        """
        if popup:
            editmenu = viewmenu
            editmenu.setTitle("View/Edit")
            editmenu.addSeparator()
            # build_editmenu = True
        else:
            editmenu = menubar.addMenu("&Edit")

        for ix, act in enumerate(self.editmenu_actions[:6]):
            editmenu.addAction(act)
            if ix == 2:
                editmenu.addSeparator()

        disable_menuitems = not (self.cut_el or self.cut_att)
        # add_menuitem = not popup or not disable_menuitems
        if disable_menuitems:
            self.pastebefore_item.setText("Nothing to Paste")
            self.pastebefore_item.setEnabled(False)
            self.pasteafter_item.setEnabled(False)
            self.pasteunder_item.setEnabled(False)
        # if add_menuitem:
        editmenu.addAction(self.pastebefore_item)
        editmenu.addAction(self.pasteafter_item)
        editmenu.addAction(self.pasteunder_item)

        editmenu.addSeparator()
        for act in self.editmenu_actions[9:]:
            editmenu.addAction(act)
        return editmenu

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
        retval = dict(zip((qtw.QMessageBox.StandardButton.Yes, qtw.QMessageBox.StandardButton.No,
                           qtw.QMessageBox.StandardButton.Cancel), (1, 0, -1)))
        self.in_dialog = True
        h = qtw.QMessageBox.question(
            self, self.editor.title, prompt,
            qtw.QMessageBox.StandardButton.Yes | qtw.QMessageBox.StandardButton.No
            | qtw.QMessageBox.StandardButton.Cancel,
            defaultButton=qtw.QMessageBox.StandardButton.Yes)
        return retval[h]

    def ask_for_text(self, prompt, value=''):
        """vraagt om tekst en retourneert het antwoord"""
        self.in_dialog = True
        data, *_ = qtw.QInputDialog.getText(self, self.editor.title, prompt, text=value)
        return data

    def file_to_read(self):
        """ask for file to load"""
        fnaam, *_ = qtw.QFileDialog.getOpenFileName(self, "Choose a file", os.getcwd(),
                                                    HMASK[os.name])
        ok = bool(fnaam)
        return ok, str(fnaam)

    def file_to_save(self):
        """ask for file to save"""
        name, *_ = qtw.QFileDialog.getSaveFileName(self, "Save file as ...", self.editor.xmlfn,
                                                   HMASK[os.name])
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
        menu = self.init_menus(popup=True)
        menu.exec(self.tree.mapToGlobal(self.tree.visualItemRect(item).bottomRight()))

    def quit(self):
        "close the application"
        self.close()

    def on_keyup(self, event):
        "handle keyboard event"
        ky = event.key()
        item = self.tree.currentItem()
        skip = False
        if item and item != self.top:
            if ky == core.Qt.Key.Key_Return:
                if self.in_dialog:
                    self.in_dialog = False
                elif item.childCount() > 0:
                    if item.isExpanded():
                        self.tree.collapseItem(item)
                        self.tree.setCurrentItem(item.parent())
                    else:
                        self.tree.expandItem(item)
                        self.tree.setCurrentItem(item.child(0))
                skip = True
            elif ky == core.Qt.Key.Key_Backspace:
                if item.isExpanded():
                    self.tree.collapseItem(item)
                    self.tree.setCurrentItem(item.parent())
                skip = True
            elif ky == core.Qt.Key.Key_Menu:
                self.popupmenu(item)
                skip = True
        return skip

    # def ask_for_search_args(self):
    #     """send dialog to get search argument(s)
    #     """
    #     # self.search_args = []
    #     edt = SearchDialog(self, title='Search options').exec()
    #     if edt == qtw.QDialog.DialogCode.Accepted:
    #         # self.editor.search_args = self.search_args
    #         return True
    #     return False

    def do_undo(self):
        "undo action"
        self.undo_stack.undo()

    def do_redo(self):
        "(re)do action"
        self.undo_stack.redo()


class VisualTree(qtw.QTreeWidget):
    """Tree widget subclass overriding some event handlers
    """
    def __init__(self, parent):
        self.parent = parent
        super().__init__()

    def mouseDoubleClickEvent(self, event):
        "reimplemented to reject when on root element"
        pos = event.position()
        # item = self.itemAt(int(pos.x()), int(pos.y()))
        item = self.itemAt(pos.toPoint())
        edit = False
        if item:
            edit = item != self.parent.top
        if edit:
            # self.parent.edit_item(item)
            self.parent.editor.edit(item)
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        "reimplemented to show popup menu when applicable"
        # xc, yc = event.x(), event.y()
        # item = self.itemAt(xc, yc)
        item = self.itemAt(event.pos())
        if event.button() == core.Qt.MouseButton.RightButton:
            if item and item != self.parent.top:
                # self.parent.setCurrentItem(item)
                menu = self.parent.init_menus(popup=True)
                # menu.exec(core.QPoint(xc, yc))
                menu.exec(self.mapToGlobal(event.pos()))
        else:  # left click
            self.parent.set_selected_item(item)
        event.ignore()


def calculate_location(win, node):
    """attempt to calculate some kind of identification for a tree node

    this function returns a tuple of subsequent indices of a child under its
    parent.
    possibly this can be used in the replacements dictionary
    """
    id_ = []
    while node != win.top:
        newnode = node.parent()
        idx = newnode.indexOfChild(node)
        id_.insert(0, idx)
        node = newnode
    return tuple(id_)


class UndoRedoStack(gui.QUndoStack):
    """Undo stack subclass overriding some event handlers
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.cleanChanged.connect(self.clean_changed)
        self.indexChanged.connect(self.index_changed)
        self.maxundo = self.undoLimit()
        self.setUndoLimit(1)  # self.unset_undo_limit(False)
        # print('Undo limit {}'.format(self.undoLimit()))
        # win = parent  # self.parent()
        parent.undo_item.setText('Nothing to undo')
        parent.redo_item.setText('Nothing to redo')
        parent.undo_item.setDisabled(True)
        parent.redo_item.setDisabled(True)

    def unset_undo_limit(self, state):
        """change undo limit"""
        # print(f'state is {state}')
        if state:
            self.setUndoLimit(self.maxundo)
            nolim, yeslim = 'un', ''
        else:
            self.setUndoLimit(1)
            nolim, yeslim = '', ' to one'
        ## self.parent().setundo_action.setChecked(state)
        self.parent().statusbar.showMessage(f'Undo level is now {nolim}limited{yeslim}')

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
class PasteElementCommand(gui.QUndoCommand):
    """subclass to make Undo/Redo possible"""
    def __init__(self, win, tag, text, where, before, below, description="", data=None):
        """
        "where we are" is optional because it can be determined from the current
        position but it should also be possible to provide it
        """
        self.win = win          # main gui
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
        # print(f"init {description} {self.tag} {self.data}")  # , self.item)
        self.first_edit = not self.win.editor.tree_dirty
        super().__init__(description)

    def redo(self):
        "((Re)Do add element"
        def zetzeronder(node, data, before=False, below=True):
            "add elements recursively"
            # print(f'zetzeronder voor node {node} met data {data}')
            text, data, children = data
            tag, value = data
            # tag, value, children = data
            is_attr = not text.startswith(self.win.editor.elstart)
            # is_attr = not tag.startswith(self.win.editor.elstart)
            add_under = self.win.editor.add_item(node, tag, value, before=before, below=below,
                                                 attr=is_attr)
            below = True
            for item in children:
                zetzeronder(add_under, item)
            return add_under
        # print('redo of add')
        # print('    tag is', self.tag)
        # print('    data is', self.data)
        # print('    before is', self.before)
        # print('    below is', self.below)
        # print('    where is', self.where)
        # print(f'In paste element redo for tag {self.tag} data {self.data}')
        self.added = self.win.editor.add_item(self.where, self.tag, self.data, before=self.before,
                                              below=self.below)
        # print(f'newly added {self.added} with children {self.children}')
        if self.children is not None:
            for item in self.children[0][2]:   # begin je zo niet met de grandchildren?
            # for item in self.children:
                zetzeronder(self.added, item)
        ## if self.replaced:
            ## self.win.replaced[calculate_location(add_under)] = self.added
        self.win.tree.expandItem(self.added)
        # print(f"self.added after adding children: {self.added}")

    def undo(self):
        "Undo add element"
        # essentially 'cut' Command
        # print(f'In paste element undo for added: {self.added}')
        self.replaced = self.added   # remember original item in case redo replaces it
        item = CopyElementCommand(self.win, self.added, cut=True, retain=False,
                                  description=__doc__)
        item.redo()
        if self.first_edit:
            self.win.editor.mark_dirty(False)
        self.win.statusbar.showMessage(f'{self.text()} undone')


class PasteAttributeCommand(gui.QUndoCommand):
    """subclass to make Undo/Redo possible"""
    def __init__(self, win, name, value, item, description=""):
        super().__init__(description)
        self.win = win          # main gui
        self.item = item        # where we are now
        self.name = name        # attribute name
        self.value = value      # attribute value
        # print(f"init {description} {self.name} {self.value} {self.item}")
        self.first_edit = not self.win.editor.tree_dirty

    def redo(self):
        "(Re)Do add attribute"
        # print(f'(redo) add attr {self.name} {self.value} {self.item}')
        self.added = self.win.editor.add_item(self.item, self.name, self.value, attr=True)
        self.win.tree.expandItem(self.added.parent())
        # print(f'Added {self.added}')

    def undo(self):
        "Undo add attribute"
        # essentially 'cut' Command
        item = CopyAttributeCommand(self.win, self.added, cut=True, retain=False,
                                    description=__doc__)
        item.redo()
        if self.first_edit:
            self.win.editor.mark_dirty(False)
        self.win.statusbar.showMessage(f'{self.text()} undone')


class EditCommand(gui.QUndoCommand):
    """subclass to make Undo/Redo possible"""
    def __init__(self, win, old_state, new_state, description=""):
        # print(f"building editcommand for {description}")
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
        self.win.statusbar.showMessage(f'{self.text()} undone')


class CopyElementCommand(gui.QUndoCommand):
    """subclass to make Undo/Redo possible"""
    def __init__(self, win, item, cut, retain, description=""):
        super().__init__(description)
        self.undodata = None
        self.win = win      # main gui
        self.item = item    # where we are now
        self.tag = str(self.item.text(1))
        self.data = str(self.item.text(2))  # name and text
        # print(f"init {description} {self.tag} {self.data} {self.item}")
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
        if self.undodata is None:
            self.parent = self.item.parent()
            self.loc = self.parent.indexOfChild(self.item)
            self.undodata = push_el(self.item, [])
            if self.loc > 0:
                self.prev = self.parent.child(self.loc - 1)
            else:
                self.prev = self.parent
                if self.prev == self.win.editor.rt:
                    self.prev = self.parent.child(self.loc + 1)
        if self.retain:
            self.win.cut_el = self.undodata
            self.win.cut_att = None
            self.win.enable_pasteitems(True)
        if self.cut:
            self.parent.removeChild(self.item)
            self.item = self.prev
            self.win.tree.setCurrentItem(self.prev)

    def undo(self):
        "Undo Copy Element"
        # print(f'In copy element undo for tag {self.tag} data {self.data} item {self.item}')
        # self.cut_el = None
        if self.cut:
            # print('undo of', self.item)
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
        self.win.statusbar.showMessage(f'{self.text()} undone')
        ## self.win.tree.setCurrentItem(self.item)


class CopyAttributeCommand(gui.QUndoCommand):
    """subclass to make Undo/Redo possible"""
    def __init__(self, win, item, cut, retain, description):
        super().__init__(description)
        self.win = win      # main gui
        self.item = item    # where we are now
        self.name = str(self.item.text(1))
        self.value = str(self.item.text(2))  # name and text
        # print(f"init {description} {self.name} {self.value} {self.item}")
        self.cut = cut
        self.retain = retain
        self.first_edit = not self.win.editor.tree_dirty

    def redo(self):
        "(re)do copy attribute"
        # print(f'copying item {self.item} with text {self.value}')
        self.parent = self.item.parent()
        self.loc = self.parent.indexOfChild(self.item)
        if self.retain:
            # print('Retaining attribute')
            self.win.cut_el = None
            self.win.cut_att = (self.name, self.value)
            self.win.enable_pasteitems(True)
        if self.cut:
            # print('cutting attribute')
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
        # print(f'{__doc__} for {self.name} {self.value} {self.item}')
        # self.win.cut_att = None
        if self.cut:
            item = PasteAttributeCommand(self.win, self.name, self.value, self.parent,
                                         description=__doc__)
            item.redo()
            self.item = item.added
        if self.first_edit:
            self.win.editor.mark_dirty(False)
        self.win.statusbar.showMessage(f'{self.text()} undone')


def show_dialog(dlg):
    "show a dialog and return confirmation"
    ok = dlg.exec()
    return ok == qtw.QDialog.DialogCode.Accepted


class DialogGui(qtw.QDialog):
    """General purpose interface to dialog implementation
    """
    def __init__(self, master, parent, title):
        self.master = master
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(parent.icon)
        self.sizer = qtw.QVBoxLayout()
        hsizer = qtw.QHBoxLayout()
        self.gsizer = qtw.QGridLayout()
        hsizer.addLayout(self.gsizer)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

    def add_label(self, text, row, col, fullwidth=False):
        "add fixed text to grid"
        lbl_name = qtw.QLabel(text, self)
        if fullwidth:
            # self.gsizer.addWidget(lbl_name, row, col, 1, self.gsizer.columnCount())
            self.gsizer.addWidget(lbl_name, row, col, 1, 2)
        else:
            self.gsizer.addWidget(lbl_name, row, col)
        return lbl_name

    def add_lineinput(self, row, col, text=None, callback=None):
        "add single line text input widget to grid"
        hsizer = qtw.QHBoxLayout()
        txt = qtw.QLineEdit(self)
        if text:
            txt.setText(text)
        if callback:
            txt.textChanged.connect(callback)
        hsizer.addWidget(txt)
        hsizer.addStretch()
        self.gsizer.addLayout(hsizer, row, col)
        return txt

    def add_checkbox(self, text, row, col, readonly=False):
        "add checkbox to grid"
        cb = qtw.QCheckBox(text, self)
        if readonly:
            cb.setCheckable(False)
        self.gsizer.addWidget(cb, row, col)
        return cb

    def add_combobox(self, items, row, col):
        "add combobox to grid"
        cmb = qtw.QComboBox(self)
        cmb.setEditable(False)
        cmb.addItems(items)
        self.gsizer.addWidget(cmb, row, col)
        return cmb

    def add_textinput(self, row, col):
        "add multiline text input widget to grid (over full line)"
        txt = qtw.QTextEdit(self)
        txt.setTabChangesFocus(True)
        self.gsizer.addWidget(txt, row, col, 1, 2)
        return txt

    def add_buttons(self, buttondefs):
        "create action buttons"
        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        for text, callback, is_default in buttondefs:
            btn = qtw.QPushButton(text, self)
            btn.clicked.connect(callback)
            if is_default:
                btn.setDefault(True)
            hsizer.addWidget(btn)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

    def finish_display(self):
        "finalize the layout"
        self.setLayout(self.sizer)

    def set_label_text(self, lbl, text):
        "set value for label"
        lbl.setText(text)

    def set_lineinput_text(self, tb, text):
        "set value for input box"
        tb.setText(text)

    def set_checkbox_state(self, cb, value):
        "set value for checkbox"
        cb.setChecked(value)

    def set_combobox_index(self, cmb, value):
        "set choice for combobox"
        cmb.setCurrentIndex(value)

    def set_textinput_text(self, tb, text):
        "set value for textbox"
        tb.setText(text)

    def get_lineinput_text(self, tb):
        "transmit text input"
        return tb.text()

    def get_checkbox_state(self, cb):
        "transmit state of checkbox"
        return cb.isChecked()

    def get_combobox_index(self, cmb):
        "transmit index of combobox choice"
        return cmb.currentIndex()

    def get_combobox_itemtext(self, cmb, indx):
        "transmit text of combobox choice"
        return cmb.itemText(indx)

    def get_textinput_text(self, tb):
        "transmit textbox input"
        return tb.toPlainText()

    def set_focus_to(self, field):
        "redirect input to error field"
        field.setFocus()

    def accept(self):
        """overridden"""
        ok = self.master.confirm()
        if ok:
            super().accept()

    def keyPressEvent(self, event):
        """reimplemented event handler voor toetsaanslagen"""
        if event.key() == core.Qt.Key.Key_Escape:
            super().done(qtw.QDialog.DialogCode.Rejected)

    def refresh(self):
        "adjust window size after clearing label text (hopefully)"
        self.sizer.update()
        self.update()
