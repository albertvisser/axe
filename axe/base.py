# -*- coding: utf-8 -*-
"""
XMLEdit GUI-onafhankelijke code
"""

import os
# import pathlib
## import sys
import shutil
## import copy
import xml.etree.ElementTree as et
# import logging

from .shared import ELSTART, TITEL, log
from .gui import Gui


def find_in_flattened_tree(data, search_args, reverse=False, pos=None):
    """searches the flattened tree from start or the given pos
    to find the next item that fulfills the search criteria
    """
    # print('in find_in_flattened_tree:', search_args)
    wanted_ele, wanted_attr, wanted_value, wanted_text = search_args
    if reverse:
        data.reverse()

    if pos:
        pos, is_attr = pos
        ## found_item = False
        for ix, item in enumerate(data):
            if is_attr:
                found_attr = False
                for ix2, attr in enumerate(item[3]):
                    if attr[0] == pos:
                        found_attr = True
                        break
                if found_attr:
                    break
            else:
                if item[0] == pos:
                    break
        if is_attr:
            data = data[ix:]
            id, name, text, attrs = data[0]
            data[0] = id, name, text, attrs[ix2 + 1:]
        elif ix < len(data) - 1:
            data = data[ix + 1:]
        else:
            return None, False  # no more data to search

    itemfound = False
    for item, element_name, element_text, attr_list in data:
        ele_ok = attr_name_ok = attr_value_ok = attr_ok = text_ok = False
        # print(element_name, element_text, attr_list)
        # ele_ok = text_ok = False
        if not wanted_ele or wanted_ele in element_name:
            ele_ok = True
            # print('ele wanted:', wanted_ele, 'found:', ele_ok)
        if not wanted_text or wanted_text in element_text:
            text_ok = True
            # print('text wanted:', wanted_text, 'found:', text_ok)

        attr_item = None
        if attr_list and (wanted_attr or wanted_value):
            if reverse:
                attr_list.reverse()
            for attr, name, value in attr_list:
                attr_name_ok = attr_value_ok = False
                if not wanted_attr or wanted_attr in name:
                    attr_name_ok = True
                    # print('attr name wanted:', wanted_attr, 'found:', attr_name_ok)
                if not wanted_value or wanted_value in value:
                    attr_value_ok = True
                    # print('attr value wanted:', wanted_value, 'found:', attr_value_ok)
                if attr_name_ok and attr_value_ok:
                    attr_ok = True
                    if not (wanted_ele or wanted_text):
                        attr_item = attr
                    break
        elif not wanted_attr and not wanted_value:
            attr_ok = True

        ok = ele_ok and text_ok and attr_ok
        if ok:
            if attr_item:
                itemfound, is_attr = attr_item, True
            else:
                itemfound, is_attr = item, False
            break
    if itemfound:
        return itemfound, is_attr
    else:
        return None, False


def parse_nsmap(file):
    """analyze namespaces
    """
    root = None
    ns_prefixes = []
    ns_uris = []

    for event, elem in et.iterparse(file, ("start-ns", "start")):
        if event == "start-ns":
            ns_prefixes.append(elem[0])
            ns_uris.append(elem[1])
        elif event == "start":
            if root is None:
                root = elem

    return et.ElementTree(root), ns_prefixes, ns_uris


class XMLTree():
    """class to store XMLdata
    """
    def __init__(self, data):
        self.root = et.Element(data)

    def expand(self, root, text, data):
        "expand node"
        if text.startswith(ELSTART):
            node = et.SubElement(root, data[0])
            if data[1]:
                node.text = data[1]
            return node
        else:
            root.set(data[0], data[1])
            return None

    def write(self, fn, ns_data=None):
        "write XML to tree"
        tree = et.ElementTree(self.root)
        if ns_data:
            prefixes, uris = ns_data
            for idx, prefix in enumerate(prefixes):
                et.register_namespace(prefix, uris[idx])
        tree.write(fn, encoding="utf-8", xml_declaration=True)


## class AxeMixin():
class Editor():
    "Applicatievenster zonder GUI-specifieke methoden"
    def __init__(self, fname):
        self.title = "Albert's XML Editor"
        self.xmlfn = os.path.abspath(fname) if fname else ''
        self.gui = Gui(self, fname)
        self.cut_att = None
        self.cut_el = None
        self.search_args = []
        self.gui.init_gui()
        self.init_tree(et.Element('New'))
        if self.xmlfn:
            try:
                tree, prefixes, uris = parse_nsmap(self.xmlfn)
            except (IOError, et.ParseError) as err:
                self.gui.meldfout(str(err), abort=True)
                self.gui.init_tree(None)
                return None
            else:
                self.init_tree(tree.getroot(), prefixes, uris)
        self.gui.go()

    def mark_dirty(self, state):
        """past gewijzigd-status aan
        en retourneert de overeenkomstig gewijzigde tekst voor de titel
        """
        self.tree_dirty = state
        test = ' - ' + TITEL
        test2 = '*' + test
        title = self.gui.get_windowtitle()
        has_test2 = test2 in title
        if state and not has_test2:
            title = title.replace(test, test2)
        elif has_test2:
            title = title.replace(test2, test)
        if title:
            self.gui.set_windowtitle(title)

    def check_tree(self):
        """vraag of er iets moet gebeuren wanneer de data gewijzigd is
        """
        ok = True
        if self.tree_dirty:
            h = self.gui.ask_yesnocancel("XML data has been modified - "
                                         "save before continuing?")
            if h == 1:
                self.savexml()
            elif h == -1:
                ok = False
        return ok

    def writexml(self, oldfile=''):
        "(re)write tree to XML file; backup first"
        def expandnode(rt, root, tree):
            "recursively expand node"
            for tag in self.gui.get_node_children(rt):
                title = self.gui.get_node_title(tag)
                data = self.gui.get_node_data(tag)
                node = tree.expand(root, title, data)
                if node is not None:
                    expandnode(tag, node, tree)
        if oldfile == '':
            oldfile = self.xmlfn + '.bak'
        if os.path.exists(self.xmlfn):
            shutil.copyfile(self.xmlfn, oldfile)
        rt = self.gui.get_treetop()
        # text = self.gui.get_node_title(rt)
        data = self.gui.get_node_data(rt)
        tree = XMLTree(data[0])  # .split(None,1)
        root = tree.root
        expandnode(rt, root, tree)
        namespace_data = None
        if self.ns_prefixes:
            namespace_data = (self.ns_prefixes, self.ns_uris)
        tree.write(self.xmlfn, namespace_data)
        self.mark_dirty(False)

    def init_tree(self, root, prefixes=None, uris=None, name=''):
        "set up display tree"
        def add_to_tree(el, rt):
            "recursively add elements"
            rr = self.add_item(rt, el.tag, el.text)
            ## log(calculate_location(self, rr))
            for attr in el.keys():
                h = el.get(attr)
                if not h:
                    h = '""'
                self.add_item(rr, attr, h, attr=True)
            for subel in list(el):
                add_to_tree(subel, rr)
        if name:
            titel = name
        elif self.xmlfn:
            titel = self.xmlfn
        else:
            titel = '[unsaved file]'
        self.top = self.gui.setup_new_tree(titel)
        self.rt = root
        self.ns_prefixes = prefixes or []
        self.ns_uris = uris or []
        self.gui.set_windowtitle(" - ".join((os.path.basename(titel), TITEL)))
        if root is None:  # explicit test needed, empty root element is falsey
            return
        # eventuele namespaces toevoegen
        namespaces = False
        for ix, prf in enumerate(self.ns_prefixes):
            if not namespaces:
                ns_root = self.gui.add_node_to_parent(self.top)
                self.gui.set_node_title(ns_root, 'namespaces')
                # ns_root = qtw.QTreeWidgetItem(['namespaces'])
                namespaces = True
            ns_item = self.gui.add_node_to_parent(ns_root)
            self.gui.set_node_title('{}: {}'.format(prf, self.ns_uris[ix]))
        rt = self.add_item(self.top, self.rt.tag, self.rt.text)
        for attr in self.rt.keys():
            h = self.rt.get(attr)
            if not h:
                h = '""'
            self.add_item(rt, attr, h, attr=True)
        for el in list(self.rt):
            add_to_tree(el, rt)
        # self.tree.selection = self.top
        # set_selection()
        self.replaced = {}  # dict of nodes that have been replaced while editing
        self.gui.expand_item(self.top)
        self.mark_dirty(False)

    def getshortname(self, data, attr=False):
        """build and return a name for this node
        """
        fullname, value = data
        text = ''
        if attr:
            text = value.rstrip('\n')
        elif value:
            text = value.split("\n", 1)[0]
        max = 60
        if len(text) > max:
            text = text[:max].lstrip() + '...'
        if fullname.startswith('{'):
            uri, localname = fullname[1:].split('}')
            for i, ns_uri in enumerate(self.ns_uris):
                if ns_uri == uri:
                    prefix = self.ns_prefixes[i]
                    break
            fullname = ':'.join((prefix, localname))
        strt = ' '.join((ELSTART, fullname))
        if attr:
            return " = ".join((fullname, text))
        elif text:
            return ": ".join((strt, text))
        else:
            return strt

    def add_item(self, to_item, name, value, before=False, below=True, attr=False):
        """execute adding of item"""
        log('in add_item for {} value {} to {} before is {} below is {}'.format(
            name, value, to_item, before, below))
        if value is None:
            value = ""
        itemtext = self.getshortname((name, value), attr)
        if below:
            add_under = to_item
            insert = -1
            if not itemtext.startswith(ELSTART):
                itemlist = self.gui.get_node_children(to_item)
                for seq, subitem in enumerate(itemlist):
                    if self.gui.get_node_title(subitem).startswith(ELSTART):
                        break
                if itemlist and seq < len(itemlist):
                    insert = seq
        else:
            add_under, insert = self.gui.get_node_parentpos(to_item)
            if not before:
                insert += 1
        item = self.gui.add_node_to_parent(add_under, insert)
        self.gui.set_node_title(item, itemtext)
        self.gui.set_node_data(item, name, value)
        return item

    def get_menu_data(self):
        """return menu structure for GUI (title, callback, keyboard shortcut(s))
        """
        return ((("&New", self.newxml, 'Ctrl+N'),
                 ("&Open", self.openxml, 'Ctrl+O'),
                 ('&Save', self.savexml, 'Ctrl+S'),
                 ('Save &As', self.savexmlas, 'Shift+Ctrl+S'),
                 ('E&xit', self.gui.quit, 'Ctrl+Q'), ),
                (("&Expand All (sub)Levels", self.expand, 'Ctrl++'),
                 ("&Collapse All (sub)Levels", self.collapse, 'Ctrl+-'), ),
                (("Nothing to &Undo", self.undo, 'Ctrl+Z'),
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
                 ('Insert Element Under', self.insert_child, 'Insert'), ),
                (("&Find", self.search, 'Ctrl+F'),
                 ("Find &Last", self.search_last, 'Shift+Ctrl+F'),
                 ("Find &Next", self.search_next, 'F3'),
                 ("Find &Previous", self.search_prev, 'Shift+F3'),
                 ("&Replace", self.replace, 'Ctrl+H'), ))

    def flatten_tree(self, element):
        """return the tree's structure as a flat list
        probably nicer as a generator function
        """
        attr_list = []
        # print('in flatten tree: node title', self.gui.get_node_title(element))
        # print('in flatten tree: node data', self.gui.get_node_data(element))
        try:
            title, data = self.gui.get_node_data(element)
        except TypeError:
            title = data = ''
        if not data:
            data = ('', '')
        elem_list = [(element, title, data, attr_list)]

        subel_list = []
        for subel in self.gui.get_node_children(element):
            if self.gui.get_node_title(subel).startswith(ELSTART):
                subel_list = self.flatten_tree(subel)
                elem_list.extend(subel_list)
            else:
                # attr_list.append((subel, *self.gui.get_node_data(subel)))
                x, y = self.gui.get_node_data(subel)
                attr_list.append((subel, x, y))
        return elem_list

    def find_first(self, reverse=False):
        "start search after asking for options"
        if self.gui.get_search_args():
            loc = -1 if reverse else 0
            # print('getting tree top:', self.gui.get_treetop(),
            #       self.gui.get_node_title(self.gui.get_treetop()))
            self._search_pos = self.gui.get_node_children(self.gui.get_treetop())[loc], None
            self.find_next(reverse)

    def find_next(self, reverse=False):
        "find (default is forward)"
        found, is_attr = find_in_flattened_tree(self.flatten_tree(self.top), self.search_args,
                                                reverse, self._search_pos)
        if found:
            self.gui.set_selected_item(found)
            self._search_pos = (found, is_attr)
        else:
            self.gui.meldinfo('Niks (meer) gevonden')

    @staticmethod
    def get_copytext(cut, retain):
        "get text with this action"
        if cut:
            if retain:
                txt = 'cut'
            else:
                txt = 'delete'
        else:
            txt = 'copy'
        return txt

    # user actions from application menu
    def newxml(self, event=None):
        """nieuwe xml boom initialiseren

        de underscore methode moet in de gui module zijn gedefinieerd
        """
        if self.check_tree():
            h = self.gui.ask_for_text("Enter a name (tag) for the root element")
            if not h:
                h = "root"
            self.xmlfn = ""
            self.init_tree(et.Element(h))

    def openxml(self, event=None, skip_check=False):
        "load XML file (after checking if current needs to be saved)"
        if skip_check or self.check_tree():
            ok, fname = self.gui.file_to_read()
            if ok:
                try:
                    tree, prefixes, uris = parse_nsmap(fname)
                except et.ParseError as e:
                    self.gui.meldfout(str(e))
                    return False
                self.xmlfn = fname
                self.init_tree(tree.getroot(), prefixes, uris)

    def savexml(self, event=None):
        "(re)save XML; ask for filename if unknown"
        if self.xmlfn == '':
            self.savexmlas()
        else:
            self.writexml()

    def savexmlas(self, event=None):
        "ask for filename, then save"
        ok, name = self.gui.file_to_save()
        if ok:
            self.xmlfn = name
            self.writexml()  # oldfile=os.path.join(d,f))
            self.gui.set_node_title(self.gui.top, self.xmlfn)
            self.mark_dirty(False)
        return ok

    def expand(self, event=None):
        """show all children of the current node
        """
        self.gui.expand_item()

    def collapse(self, event=None):
        """hide all children of the current node
        """
        self.gui.collapse_item()

    def undo(self, event=None):
        "maak laatste actie ongedaan"
        self.gui.do_undo()

    def redo(self, event=None):
        "voer laatste ongedaan gemaakte actie opnieuw uit"
        self.gui.do_redo()

    def edit(self, event=None):
        """start dialog to edit the current element
        """
        self.gui.edit_item()

    def cut(self, event=None):
        "cut is copy with remove and retain"
        self.gui.copy(cut=True)

    def delete(self, event=None):
        "delete is copy with remove and without retain"
        self.gui.copy(cut=True, retain=False)

    def copy(self, event=None):
        "standard copy"
        self.gui.copy()

    def paste_after(self, event=None):
        "paste after instead of before"
        self.gui.paste(before=False)

    def paste_under(self, event=None):
        "paste under instead of after"
        self.gui.paste(pastebelow=True)

    def paste(self, event=None):
        "paste after"
        self.gui.paste()

    def add_attr(self, event=None):
        """start dialog to add a new attribute to the element
        """
        self.gui.add_attribute()

    def insert_after(self, event=None):
        "insert after instead of before"
        self.gui.insert(before=False)

    def insert_child(self, event=None):
        "insert under instead of before"
        self.gui.insert(below=True)

    def insert(self, event=None):
        "placeholder for insert before"
        self.gui.insert()

    def search(self, event=None):
        "start forward search"
        self.find_first()

    def search_last(self, event=None):
        "start backwards search"
        self.find_first(reverse=True)

    def search_next(self, event=None):
        "find forward"
        self.find_next()

    def search_prev(self, event=None):
        "find backwards"
        self.find_next(reverse=True)

    @staticmethod
    def get_search_text(ele, attr_name, attr_val, text):
        "build text describing search arguments"
        attr = attr_name or attr_val
        out = ['search for']
        has_text = ' that has'
        name_text = ' a name'
        value_text = ' a value'
        contain_text = '   containing `{}`'
        if ele:
            ele_out = [' an element' + has_text + name_text, contain_text.format(ele)]
        if attr:
            attr_out = [' an attribute' + has_text]
            if attr_name:
                attr_out[0] += name_text
                attr_out.append(contain_text.format(attr_name))
            if attr_val:
                if not attr_name:
                    attr_out[0] += value_text
                else:
                    attr_out.append(' and' + value_text)
                attr_out.append(contain_text.format(attr_val))
            if ele:
                attr_out[0] = ' with' + attr_out[0]
        if text:
            out[0] += ' text'
            out.append('   `{}`'.format(text))
            if ele:
                ele_out[0] = ' under' + ele_out[0]
                out += ele_out
            elif attr:
                out += [' under an element with']
            if attr:
                out += attr_out
        elif ele:
            out += ele_out
            if attr:
                out += attr_out
        elif attr:
            attr_out[0] = out[0] + attr_out[0]
            out = attr_out
        return out

    def replace(self, event=None):
        "replace an element?"
        self.gui.meldinfo('Replace: not sure if I wanna implement this')

    def about(self, event=None):
        "Credits"
        self.gui.meldinfo("Started in 2008 by Albert Visser\nWritten in Python")
