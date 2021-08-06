"""wxPython versie van een op een treeview gebaseerde XML-editor
"""
import os
import wx
from .shared import ELSTART, axe_iconame, log
if os.name == "nt":
    HMASK = "XML files (*.xml)|*.xml|All files (*.*)|*.*"
elif os.name == "posix":
    HMASK = "XML files (*.xml, *.XML)|*.xml;*.XML|All files (*.*)|*.*"
IMASK = "All files|*.*"


class ElementDialog(wx.Dialog):
    """Dialog for editing an element
    """
    def __init__(self, parent, title='',  # size=(400, 270), pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
                 item=None):
        wx.Dialog.__init__(self, parent, title=title, style=style)
        self._parent = parent
        lbl_name = wx.StaticText(self, label="element name:  ")
        self.txt_tag = wx.TextCtrl(self, size=(200, -1))

        self.cb_ns = wx.CheckBox(self, label='Namespace:  ')
        self.cmb_ns = wx.ComboBox(self, size=(120, -1))
        self.cmb_ns.Append('-- none --')
        self.cmb_ns.AppendItems(self._parent.editor.ns_uris)

        self.cb = wx.CheckBox(self, label='Bevat data:')
        self.txt_data = wx.TextCtrl(self, size=(300, 140), style=wx.TE_MULTILINE)
        self.btn_ok = wx.Button(self, id=wx.ID_SAVE)
        self.btn_ok.Bind(wx.EVT_BUTTON, self.on_ok)
        self.btn_cancel = wx.Button(self, id=wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_SAVE)

        ns_tag = tag = ns_uri = txt = ''
        if item:
            ns_tag = item["tag"]
            if ns_tag.startswith('{'):
                ns_uri, tag = ns_tag[1:].split('}')
            else:
                tag = ns_tag
            if "text" in item:
                self.cb.SetValue(True)
                txt = item["text"]
            if ns_uri:
                self.cb_ns.SetValue(True)
                for ix, uri in enumerate(self.parent.ns_uris):
                    if uri == ns_uri:
                        self.cmb_ns.SetSelection(ix + 1)
        self.txt_tag.SetValue(tag)
        self.txt_data.SetValue(txt)

        sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(lbl_name, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
        hsizer.Add(self.txt_tag, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        ## hsizer.Add(hsizer2, 0, wx.EXPAND | wx.ALL, 5)
        ## sizer.Add(hsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP,  5)
        sizer.Add(hsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 5)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.cb_ns, 0, wx.ALIGN_CENTER_VERTICAL)  # | wx.LEFT | wx.RIGHT, 5)
        hsizer.Add(self.cmb_ns, 1)  # , wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        sizer.Add(hsizer, 0, wx.EXPAND | wx.ALL, 5)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(self.cb, 0, wx.ALIGN_CENTER_HORIZONTAL)  # ,wx.TOP, 3)
        vsizer.Add(self.txt_data, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)
        hsizer.Add(vsizer, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(hsizer, 1, wx.EXPAND | wx.ALL, 5)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.btn_ok, 0, wx.EXPAND | wx.ALL, 2)
        hsizer.Add(self.btn_cancel, 0, wx.EXPAND | wx.ALL, 2)
        sizer.Add(hsizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 2)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        sizer.SetSizeHints(self)
        self.Layout()
        # vbox = wx.BoxSizer(wx.VERTICAL)
        # hbox = wx.BoxSizer(wx.HORIZONTAL)
        # hbox.Add(self, 0, wx.EXPAND | wx.ALL)
        # vbox.Add(hbox, 0, wx.EXPAND | wx.ALL)
        # self.SetSizer(vbox)
        # self.SetAutoLayout(True)
        # vbox.Fit(self)
        # vbox.SetSizeHints(self)

        self.txt_tag.SetFocus()

    def on_cancel(self, ev):
        "dismiss dialog"
        # TODO: make sure escape activates this too
        self.end('cancel')

    def on_ok(self, ev):
        """final checks, send changed data to parent"""
        self._parent.data = {}
        tag = self.txt_tag.GetValue()
        fout = ''
        if tag == '':
            fout = 'Element name must not be empty'
        elif len(tag.split()) > 1:
            fout = 'Element name must not contain spaces'
        elif tag[0].isdigit():
            fout = 'Element name must not start with a digity'
        if fout:
            self._parent.meldfout(fout)
            self.txt_tag.SetFocus()
            return
        if self.cb_ns.GetValue():
            seq = self.cmb_ns.getSelection()
            if seq == wx.NOT_FOUND:
                self._parent.meldfout('Namespace must be selected if checked')
                self.cb_ns.SetFocus()
                return
            tag = '{{{}}}{}'.format(self.cmb_ns.GetString(seq), tag)
        self._parent.data["tag"] = tag
        self._parent.data["data"] = self.cb.IsChecked()
        self._parent.data["text"] = self.txt_data.GetValue()
        ev.Skip()


class AttributeDialog(wx.Dialog):
    """Dialog for editing an attribute
    """
    def __init__(self, parent, title='',  # size=(320, 160), pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
                 item=None):
        wx.Dialog.__init__(self, parent, title=title, style=style)
        self._parent = parent
        lbl_name = wx.StaticText(self, label="Attribute name:")
        self.txt_name = wx.TextCtrl(self, size=(180, -1))
        lbl_value = wx.StaticText(self, label="Attribute value:")
        self.txt_value = wx.TextCtrl(self, size=(180, -1))
        self.cb_ns = wx.CheckBox(self, label='Namespace:  ')
        self.cmb_ns = wx.ComboBox(self, size=(120, -1))
        self.cmb_ns.Append('-- none --')
        self.cmb_ns.AppendItems(self._parent.editor.ns_uris)

        self.btn_ok = wx.Button(self, id=wx.ID_SAVE)
        self.btn_ok.Bind(wx.EVT_BUTTON, self.on_ok)
        self.btn_cancel = wx.Button(self, id=wx.ID_CANCEL)
        self.SetAffirmativeId(wx.ID_SAVE)

        nam = val = ns_nam = ns_uri = ''
        if item:
            ns_nam = item["name"]
            if ns_nam.startswith('{'):
                ns_uri, nam = ns_nam[1:].split('}')
            else:
                nam = ns_nam
            if ns_uri:
                self.cb_ns.SetValue(True)
                for ix, uri in enumerate(self.parent.ns_uris):
                    if uri == ns_uri:
                        self.cmb_ns.SetSelection(ix + 1)
            val = item["value"]
        self.txt_name.SetValue(nam)
        self.txt_value.SetValue(val)

        sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(lbl_name, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
        hsizer.Add(self.txt_name, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        sizer.Add(hsizer, 0, wx.EXPAND | wx.ALL, 5)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.cb_ns, 0, wx.ALIGN_CENTER_VERTICAL)  # | wx.LEFT | wx.RIGHT, 5)
        hsizer.Add(self.cmb_ns, 1)  # , wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        sizer.Add(hsizer, 0, wx.EXPAND | wx.ALL, 5)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(lbl_value, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
        hsizer.Add(self.txt_value, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        sizer.Add(hsizer, 0, wx.EXPAND | wx.ALL, 5)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.btn_ok, 0, wx.EXPAND | wx.ALL, 2)
        hsizer.Add(self.btn_cancel, 0, wx.EXPAND | wx.ALL, 2)
        sizer.Add(hsizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 2)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        sizer.SetSizeHints(self)
        self.Layout()
        self.txt_name.SetFocus()

    def on_ok(self, ev):
        """final checks, transmit changes to parent
        """
        self._parent.data = {}
        nam = self.txt_name.GetValue()
        fout = ''
        if nam == '':
            fout = 'Attribute name must not be empty'
        elif len(nam.split()) > 1:
            fout = 'Attribute name must not contain spaces'
        elif nam[0].isdigit():
            fout = 'Attribute name must not start with a digit'
        if fout:
            self._parent.meldfout(fout)
            self.txt_name.SetFocus()
            return
        if self.cb_ns.GetValue():
            seq = self.cmb_ns.getSelection()
            if seq == wx.NOT_FOUND:
                self._parent.meldfout('Namespace must be selected if checked')
                self.cb_ns.SetFocus()
                return
            nam = '{{{}}}{}'.format(self.cmb_ns.GetString(seq), nam)  # tag)
        self._parent.data["name"] = nam
        self._parent.data["value"] = self.txt_value.GetValue()
        ev.Skip()


class SearchDialog(wx.Dialog):
    """Dialog to get search arguments
    """
    def __init__(self, parent, title='',  # size=(320, 160), pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER):
        super().__init__(parent, title=title, style=style)
        self._parent = parent
        if self._parent.editor.search_args:
            ele_name, attr_name, attr_val, text_val = self._parent.editor.search_args
        else:
            ele_name = attr_name = attr_val = text_val = ''
        sizer = wx.BoxSizer(wx.VERTICAL)
        gsizer = wx.GridBagSizer(2, 2)

        self.cb_element = wx.StaticText(self, label='Element')
        gsizer.Add(self.cb_element, (0, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl_element = wx.StaticText(self, label="name: ")
        hsizer.Add(lbl_element, flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_element = wx.TextCtrl(self, size=(128, -1))
        hsizer.Add(self.txt_element)
        vsizer.Add(hsizer)
        gsizer.Add(vsizer, (0, 1))

        self.cb_attr = wx.StaticText(self, label='Attribute ')
        gsizer.Add(self.cb_attr, (1, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl_attr_name = wx.StaticText(self, label="name: ")
        hsizer.Add(lbl_attr_name, flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_attr_name = wx.TextCtrl(self, size=(128, -1))
        hsizer.Add(self.txt_attr_name)
        vsizer.Add(hsizer)
        gsizer.Add(vsizer, (1, 1))
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl_attr_val = wx.StaticText(self, label="value: ")
        hsizer.Add(lbl_attr_val, flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_attr_val = wx.TextCtrl(self, size=(128, -1))
        hsizer.Add(self.txt_attr_val)
        vsizer.Add(hsizer)
        gsizer.Add(vsizer, (2, 1))

        self.cb_text = wx.StaticText(self, label='Text')
        gsizer.Add(self.cb_text, (3, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl_text = wx.StaticText(self, label="value: ")
        hsizer.Add(lbl_text, flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_text = wx.TextCtrl(self, size=(128, -1))
        hsizer.Add(self.txt_text)
        gsizer.Add(hsizer, (3, 1))
        sizer.Add(gsizer, flag=wx.TOP | wx.LEFT, border=15)

        self.sbsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.lbl_search = wx.StaticText(self, label="")  # , size=(-1, 30))
        self.sbsizer.Add(self.lbl_search, 1, wx.LEFT | wx.RIGHT, border=5)
        sizer.Add(self.sbsizer, 1, flag=wx.ALL, border=10)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_ok = wx.Button(self, id=wx.ID_OK)
        self.btn_ok.Bind(wx.EVT_BUTTON, self.on_ok)
        # self.SetAffirmativeId(wx.ID_SAVE)
        hsizer.Add(self.btn_ok)
        self.btn_cancel = wx.Button(self, id=wx.ID_CANCEL)
        hsizer.Add(self.btn_cancel)
        self.btn_clear = wx.Button(self, label='C&lear Values')
        self.btn_clear.Bind(wx.EVT_BUTTON, self.clear_values)
        hsizer.Add(self.btn_clear)
        sizer.Add(hsizer, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=10)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        # sizer.SetSizeHints(self)
        self.Layout()

        self.txt_element.Bind(wx.EVT_TEXT, self.set_search)
        self.txt_element.SetValue(ele_name)
        self.txt_attr_name.Bind(wx.EVT_TEXT, self.set_search)
        self.txt_attr_name.SetValue(attr_name)
        self.txt_attr_val.Bind(wx.EVT_TEXT, self.set_search)
        self.txt_attr_val.SetValue(attr_val)
        self.txt_text.Bind(wx.EVT_TEXT, self.set_search)
        self.txt_text.SetValue(text_val)

    def set_search(self, evt=None):
        """build text describing search action"""
        ele = self.txt_element.GetValue()
        attr_name = self.txt_attr_name.GetValue()
        attr_val = self.txt_attr_val.GetValue()
        text = self.txt_text.GetValue()
        out = self._parent.editor.get_search_text(ele, attr_name, attr_val, text)
        self.lbl_search.SetLabel('\n'.join(out))
        self.Fit()

    def clear_values(self, evt=None):
        "set empty search values"
        self.txt_element.Clear()
        self.txt_attr_name.Clear()
        self.txt_attr_val.Clear()
        self.txt_text.Clear()
        self.lbl_search.SetLabel('')
        self.Fit()

    def on_ok(self, evt=None):
        """confirm dialog and pass changed data to parent"""
        print('confirming dialog')
        ele = str(self.txt_element.GetValue())
        attr_name = str(self.txt_attr_name.GetValue())
        attr_val = str(self.txt_attr_val.GetValue())
        text = str(self.txt_text.GetValue())
        if not any((ele, attr_name, attr_val, text)):
            self._parent.meldfout('Please enter search criteria or press cancel')
            self.txt_element.SetFocus()
            return

        self._parent.editor.search_args = (ele, attr_name, attr_val, text)
        evt.Skip()


class Gui(wx.Frame):
    "Main application window"
    def __init__(self, parent=None, fn=''):
        self.editor = parent
        self.app = wx.App()
        self.fn = fn
        super().__init__(parent=None, pos=(2, 2))  # , size=(620, 900))
        self.Show()

    def go(self):
        "start application event loop"
        self.app.MainLoop()

    # event handlers
    def on_doubleclick(self, ev=None):
        "event handler for doubleclick on tree item"
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

    def on_rightdown(self, ev=None):
        "event handler for right click on tree item"
        pt = ev.GetPosition()
        item, flags = self.tree.HitTest(pt)
        if item and item != self.top:
            self.tree.SelectItem(item)
            menu = self.init_menus(popup=True)
            self.PopupMenu(menu)
            menu.Destroy()

    def afsl(self, ev=None):
        """handle CLOSE event"""
        test = self.editor.check_tree()
        if not test:
            ev.Veto()
        ev.Skip()

    # helper methods for getting/setting data in visual tree
    def get_node_children(self, node):
        "return descendants of the given node"
        result = []
        tag, c = self.tree.GetFirstChild(node)
        while tag.IsOk():
            result.append(tag)
            tag, c = self.tree.GetNextChild(node, c)
        return result

    def get_node_title(self, node):
        "return the title of the given node"
        return self.tree.GetItemText(node)

    def get_node_data(self, node):
        "return data (element name and text/CDATA) associated with the given node"
        return self.tree.GetItemData(node)  # assuming this is a 2-tuple

    def get_treetop(self):
        "return the visual tree's root element"
        top = self.tree.GetRootItem()
        return self.tree.GetLastChild(top)  # last, so no need to check for namespaces

    def setup_new_tree(self, title):
        "build new visual tree and return its root element"
        self.tree.DeleteAllItems()
        # self.undo_stack.clear()
        self.top = self.tree.AddRoot(title)
        return self.top

    def add_node_to_parent(self, parent, pos=-1):
        "add a new descendant to an element at the given position and return it"
        if pos == -1:
            node = self.tree.AppendItem(parent, '')
        else:
            node = self.tree.InsertItem(parent, pos, '')
        return node

    def set_node_title(self, node, title):
        "set the title for the given node"
        self.tree.SetItemText(node, title)

    def get_node_parentpos(self, node):
        "return the parent of the given node and its position under it"
        parent = self.tree.GetItemParent(node)
        pos = 0
        tag, c = self.tree.GetFirstChild(node)
        while tag.IsOk() and tag != node:
            pos += 1
            tag, c = self.tree.GetNextChild(node, c)
        return parent, pos

    def set_node_data(self, node, name, value):
        "set the data (element name, text/CDATA) associated with the given node"
        self.tree.SetItemData(node, (name, value))

    def get_selected_item(self):
        "return the currently selected item"
        return self.tree.Selection

    def set_selected_item(self, item):
        "set the currently selected item to the given item"
        self.tree.SelectItem(item)

    def is_node_root(self, item=None):
        "check if the given element is the visual tree's root and return the result"
        if not item:
            item = self.item
        if self.tree.getItemData(item) == (self.editor.rt.tag, self.editor.rt.text or ""):
            return True
        return False

    def expand_item(self, item=None):
        "expand a tree item"
        if not item:
            item = self.tree.Selection
        if item:
            self.tree.ExpandAllChildren(item)

    def collapse_item(self, item=None):
        "collapse tree item"
        if not item:
            item = self.tree.Selection
        if item:
            self.tree.CollapseAllChildren(item)

    def edit_item(self, item):
        "edit an element or attribute"
        self.item = item
        data = self.tree.GetItemText(self.item)  # self.item.get_text()
        if data.startswith(ELSTART):
            tag, text = self.tree.GetItemData(self.item)  # self.item.get_data()
            data = {'item': self.item, 'tag': tag}
            if text is not None:
                data['data'] = True
                data['text'] = text
            with ElementDialog(self, title='Edit an element', item=data) as edt:
                if edt.ShowModal() == wx.ID_SAVE:
                    h = (self.data["tag"], self.data["text"])
                    self.tree.SetItemText(self.item, self.editor.getshortname(h))
                    self.tree.SetItemData(self.item, h)
                    self.editor.mark_dirty(True)
        else:
            nam, val = self.tree.GetItemData(self.item)  # self.item.get_data()
            data = {'item': self.item, 'name': nam, 'value': val}
            with AttributeDialog(self, title='Edit an attribute', item=data) as edt:
                if edt.ShowModal() == wx.ID_SAVE:
                    h = (self.data["name"], self.data["value"])
                    self.tree.SetItemText(self.item, self.editor.getshortname(h, attr=True))
                    self.tree.SetItemData(self.item, h)
                    self.editor.mark_dirty(True)

    def copy(self, item, cut=False, retain=True):  # retain is t.b.v. delete functie
        """execute cut/delete/copy action"""
        def push_el(el, result):
            "copy element data recursively"
            # print "start: ",result
            text = self.tree.GetItemText(el)
            data = self.tree.GetItemData(el)
            children = []
            # print "before looping over contents:",text,y
            if text.startswith(ELSTART):
                subel, whereami = self.tree.GetFirstChild(el)
                while subel.IsOk():
                    _ = push_el(subel, children)
                    subel, whereami = self.tree.GetNextChild(el, whereami)
            # print "after  looping over contents: ",text,y
            result.append((text, data, children))
            # print "end:  ",result
            return result
        self.item = item
        text = self.tree.GetItemText(self.item)
        data = self.tree.GetItemData(self.item)
        if retain:
            if text.startswith(ELSTART):
                self.cut_el = []
                self.cut_el = push_el(self.item, self.cut_el)
                self.cut_att = None
            else:
                self.cut_el = None
                self.cut_att = data
            self.enable_pasteitems(True)
        if cut:
            prev = self.tree.GetPrevSibling(self.item)
            if not prev.IsOk():
                prev = self.tree.GetItemParent(self.item)
                if prev == self.editor.rt:
                    prev = self.tree.GetNextSibling(self.item)
            self.tree.Delete(self.item)
            self.editor.mark_dirty(True)
            # self.tree.SelectItem(prev)

    def paste(self, item, before=True, below=False):
        """execute paste action"""
        self.item = item
        if self.cut_att:
            item = self.editor.getshortname(self.cut_att, attr=True)
            data = self.cut_att
            if below:
                node = self.tree.AppendItem(self.item, item)
                self.tree.SetItemData(node, data)
            else:
                add_to = self.tree.GetItemParent(self.item)  # self.item.get_parent()
                added = False
                x, c = self.tree.GetFirstChild(add_to)
                for i in range(self.tree.GetChildrenCount(add_to)):
                    if x == self.item:
                        if not before:
                            i += 1
                        node = self.tree.InsertItem(add_to, i, item)
                        self.tree.SetItemData(node, data)
                        added = True
                        break
                    x, c = self.tree.GetNextChild(add_to, c)
                if not added:
                    node = self.tree.AppendItem(add_to, item)
                    self.tree.SetItemData(node, data)
        else:
            def zetzeronder(node, el, pos=-1):
                "add elements recursively"
                if pos == -1:
                    subnode = self.tree.AppendItem(node, el[0])
                    self.tree.SetItemData(subnode, el[1])
                else:
                    subnode = self.tree.InsertItem(node, i, el[0])
                    self.tree.SetItemData(subnode, el[1])
                for x in el[2]:
                    zetzeronder(subnode, x)
            if below:
                node = self.item
                i = -1
            else:
                node = self.tree.GetItemParent(self.item)  # self.item.get_parent()
                x, c = self.tree.GetFirstChild(node)
                cnt = self.tree.GetChildrenCount(node)
                for i in range(cnt):
                    if x == self.item:
                        if not before:
                            i += 1
                        break
                    x, c = self.tree.GetNextChild(node, c)
                if i == cnt:
                    i = -1
            zetzeronder(node, self.cut_el[0], i)
        self.editor.mark_dirty(True)

    def add_attribute(self, item):
        "ask for attibute, then start add action"
        self.item = item
        with AttributeDialog(self, title="New attribute") as edt:
            test = edt.ShowModal()
            if test == wx.ID_SAVE:
                node = self.editor.add_item(self.item, self.data["name"], self.data["value"],
                                            attr=True)
                item = self.tree.GetItemParent(node)
                if not self.tree.IsExpanded(item):
                    self.tree.Expand(item)
                self.editor.mark_dirty(True)

    def insert(self, item, before=True, below=False):
        """execute insert action"""
        self.item = item
        with ElementDialog(self, title="New element") as edt:
            if edt.ShowModal() == wx.ID_SAVE:
                node = self.editor.add_item(self.item, self.data["tag"], self.data["text"],
                                            before=before, below=below)
                item = self.tree.GetItemParent(node)
                if not self.tree.IsExpanded(item):
                    self.tree.Expand(item)
                self.editor.mark_dirty(True)

    # internals
    def init_gui(self):
        """Deze methode wordt aangeroepen door de __init__ van de mixin class
        """
        self.SetIcon(wx.Icon(axe_iconame, wx.BITMAP_TYPE_ICO))
        self.Bind(wx.EVT_CLOSE, self.afsl)

        # set up statusbar
        self.SetStatusBar(wx.StatusBar(self))
        self.SetStatusText('Ready.')

        # self.init_menus()
        menu_bar = wx.MenuBar()
        filemenu, viewmenu, editmenu, searchmenu = self.init_menus()
        menu_bar.Append(filemenu, "&File")
        menu_bar.Append(viewmenu, "&View")
        menu_bar.Append(editmenu, "&Edit")
        menu_bar.Append(searchmenu, "&Search")
        self.SetMenuBar(menu_bar)

        ## self.helpmenu.append('About', callback = self.about)

        self.tree = wx.TreeCtrl(self, size=(820, 808))  # size=(620, 808))
        self.tree.Bind(wx.EVT_LEFT_DCLICK, self.on_doubleclick)
        self.tree.Bind(wx.EVT_RIGHT_DOWN, self.on_rightdown)
        self.tree.Bind(wx.EVT_KEY_UP, self.on_keyup)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.tree, 1, wx.EXPAND)
        vsizer.Add(hsizer, 1, wx.EXPAND)
        self.SetSizer(vsizer)
        self.SetAutoLayout(True)
        vsizer.SetSizeHints(self)
        vsizer.Fit(self)
        self.Layout()
        # self.Show(True)
        self.tree.SetFocus()

        self.enable_pasteitems(False)
        self.editor.mark_dirty(False)

    def set_windowtitle(self, text):
        """set screen title
        """
        self.SetTitle(text)

    def get_windowtitle(self):
        """get screen title
        """
        return self.GetTitle()

    def init_menus(self, popup=False):
        """setup application menu"""
        accels = []
        filemenu = wx.Menu()
        viewmenu = wx.Menu()
        if popup:
            editmenu = viewmenu
            searchmenu = editmenu
        else:
            editmenu = wx.Menu()
            searchmenu = wx.Menu()
        disable_menu = True if not self.cut_el and not self.cut_att else False

        for ix, menudata in enumerate(self.editor.get_menu_data()):
            for ix2, data in enumerate(menudata):
                text, callback, shortcuts = data
                if shortcuts:
                    shortcuts = shortcuts.split(',')
                    text = '\t'.join((text, shortcuts[0]))
                    shortcuts = shortcuts[1:]
                if ix == 0:
                    # if text.startswith('&Exit'):
                    #     filemenu.AppendSeparator()
                    #     mitem = filemenu.Append(text='&Unlimited Undo', kind=wx.ITEM_CHECK)
                    #     filemenu.AppendSeparator()
                    #     self.setundo_action = mitem
                    mitem = filemenu.Append(-1, text)
                elif ix == 1:
                    mitem = viewmenu.Append(-1, text)
                elif ix == 2:
                    if ix2 == 0:
                        editmenu.AppendSeparator()
                    mitem = editmenu.Append(-1, text)
                    if ix2 == 0:
                        self.undo_item = mitem
                    elif ix2 == 1:
                        self.redo_item = mitem
                        editmenu.AppendSeparator()
                    elif ix2 == 6:
                        self.pastebefore_item = mitem
                        self.pastebefore_text = text
                    elif ix2 == 7:
                        self.pasteafter_item = mitem
                    elif ix2 == 8:
                        self.pasteunder_item = mitem
                        editmenu.AppendSeparator()
                elif ix == 3:
                    if ix2 == 0:
                        searchmenu.AppendSeparator()
                    mitem = searchmenu.Append(-1, text)
                self.Bind(wx.EVT_MENU, callback, mitem)
                if shortcuts:  # voorlopig alleen voor edit en delete
                    for item in shortcuts:
                        accel = wx.AcceleratorEntry(cmd=mitem.GetId())
                        if accel.FromString(item):
                            accels.append(accel)
                self.SetAcceleratorTable(wx.AcceleratorTable(accels))

        if disable_menu:
            self.enable_pasteitems(False)

        if popup:
            return searchmenu
        return filemenu, viewmenu, editmenu, searchmenu

    def meldinfo(self, text):
        """notify about some information"""
        wx.MessageBox(text, self.editor.title, wx.OK | wx.ICON_INFORMATION)

    def meldfout(self, text, abort=False):
        """notify about an error"""
        wx.MessageBox(text, self.editor.title, wx.OK | wx.ICON_ERROR)
        if abort:
            self.quit()

    def ask_yesnocancel(self, prompt):
        """stelt een vraag en retourneert het antwoord
        1 = Yes, 0 = No, -1 = Cancel
        """
        retval = dict(zip((wx.YES, wx.NO, wx.CANCEL), (1, 0, -1)))
        h = wx.MessageBox(prompt, self.editor.title, style=wx.YES_NO | wx.CANCEL)
        return retval[h]

    def ask_for_text(self, prompt, value=''):
        """vraagt om tekst en retourneert het antwoord"""
        return wx.GetTextFromUser(prompt, self.editor.title, value)

    def file_to_read(self):
        """ask for file to load"""
        with wx.FileDialog(self, message="Choose a file", defaultDir=os.getcwd(),
                           wildcard=HMASK, style=wx.FD_OPEN) as dlg:
            ret = dlg.ShowModal()
            ok = (ret == wx.ID_OK)
            fnaam = dlg.GetPath() if ok else ''
        return ok, fnaam

    def file_to_save(self):  # afwijkende signature
        """ask for file to save"""
        d, f = os.path.split(self.editor.xmlfn)
        with wx.FileDialog(self, message="Save file as ...", defaultDir=d, defaultFile=f,
                           wildcard=HMASK, style=wx.FD_SAVE) as dlg:
            ret = dlg.ShowModal()
            ok = (ret == wx.ID_OK)
            name = dlg.GetPath() if ok else ''
        return ok, name

    def enable_pasteitems(self, active=False):
        """activeert of deactiveert de paste-entries in het menu
        afhankelijk van of er iets te pASTEN VALT
        """
        if active:
            self.pastebefore_item.SetItemLabel(self.pastebefore_text)
        else:
            self.pastebefore_item.SetItemLabel("Nothing to Paste")
        self.pastebefore_item.Enable(active)
        self.pasteafter_item.Enable(active)
        self.pasteunder_item.Enable(active)

    def popupmenu(self, item):
        """call up menu"""

    def quit(self, ev=None):
        "close the application"
        self.Close()

    def on_keyup(self, ev=None):
        "event handler for keyboard"
        ky = ev.GetKeyCode()
        item = self.tree.Selection
        if item and item != self.top:
            if ky == wx.WXK_RETURN:
                if self.tree.ItemHasChildren(item):
                    if self.tree.IsExpanded(item):
                        self.tree.Collapse(item)
                    else:
                        self.tree.Expand(item)
                        item, dummy = self.tree.GetFirstChild(item)
                        self.tree.SelectItem(item)
                else:
                    self.editor.edit()
            elif ky == wx.WXK_BACK:
                if self.tree.IsExpanded(item):
                    self.tree.Collapse(item)
                self.tree.SelectItem(self.tree.GetItemParent(item))
        ev.Skip()

    def get_search_args(self):
        """end dialog to get search argument(s)
        """
        # self._search_args = []
        with SearchDialog(self, title='Search options') as edt:
            send = True
            while send:
                ok = edt.ShowModal()
                if ok == wx.ID_OK:
                    if self.editor.search_args:
                        break
                else:
                    send = False
        print(send)
        return send

    def do_undo(self):
        "undo action"

    def do_redo(self):
        "redo action"
