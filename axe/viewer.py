"""
XMLView GUI-onafhankelijke code
"""

import os
# import pathlib
## import sys
# import shutil
import xml.etree.ElementTree as et
# import logging

from .shared import ELSTART, log
from .base import find_in_flattened_tree, parse_nsmap
from .gui import Gui
TITEL = "Albert's (Simple) XML viewer"
# NEW_ROOT = '(new root)'


class Viewer:
    "Applicatievenster zonder GUI-specifieke methoden"
    def __init__(self, fname):
        self.title = "Albert's XML Viewer"
        self.xmlfn = os.path.abspath(fname) if fname else ''
        self.gui = Gui(self, fname, readonly=True)
        self.search_args = []
        self._search_pos = None
        self.gui.init_gui()
        if self.xmlfn:
            try:
                tree, prefixes, uris = parse_nsmap(self.xmlfn)
            except (OSError, et.ParseError) as err:
                self.gui.meldfout(str(err), abort=True)
                self.init_tree(None)
                return  # None
            else:
                self.init_tree(tree.getroot(), prefixes, uris)
        self.gui.go()

    def check_tree(self):
        "nodig omdat de gui module deze aanroept"
        return True

    def get_menu_data(self):
        """return menu structure for GUI (title, callback, keyboard shortcut(s))
        """
        return ((("&Open", self.openxml, 'Ctrl+O'),
                 ('E&xit', self.gui.quit, 'Ctrl+Q'), ),
                (("&Expand All (sub)Levels", self.expand, 'Ctrl++'),
                 ("&Collapse All (sub)Levels", self.collapse, 'Ctrl+-'), ),
                (("&Find", self.search, 'Ctrl+F'),
                 ("Find &Last", self.search_last, 'Shift+Ctrl+F'),
                 ("Find &Next", self.search_next, 'F3'),
                 ("Find &Previous", self.search_prev, 'Shift+F3')))

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
            self.gui.set_node_title(ns_item, f'{prf}: {self.ns_uris[ix]}')
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
            fullname = f'{prefix}:{localname}'
        strt = '{ELSTART} {fullname}'
        if attr:
            return "{fullname} = {text}"
        elif text:
            return "{strt}: {text}"
        return strt

    def add_item(self, to_item, name, value, before=False, below=True, attr=False):
        """execute adding of item"""
        log(f'in add_item for {name=} {value=} {to_item=} {before=} {below=}')
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
            print('in base.add_item (not below), insert is', insert)
            if not before:
                insert += 1
            print('in base.add_item after correction, insert is', insert)
        item = self.gui.add_node_to_parent(add_under, insert)
        self.gui.set_node_title(item, itemtext)
        self.gui.set_node_data(item, name, value)
        return item

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
        # for item in elem_list:
        #     print(item)
        return elem_list

    def find_first(self, reverse=False):
        "start search after asking for options"
        # from_contextmenu = self.checkselection(message=False)
        if self.gui.get_search_args():
            # TODO: bij contextmenu rekening houden met positie huidige item
            # if from_contextmenu:
            self.item = self.gui.get_selected_item()  # self.tree.Selection
            self._search_pos = self.item, None
            self.find_next(reverse)

    def find_next(self, reverse=False):
        "find (default is forward)"
        if self._search_pos is None:
            self.gui.meldinfo('You need to "Find" something first')
            return
        found, is_attr = find_in_flattened_tree(self.flatten_tree(self.top), self.search_args,
                                                reverse, self._search_pos)
        if found:
            self.gui.set_selected_item(found)
            self._search_pos = (found, is_attr)
        else:
            self.gui.meldinfo('Niks (meer) gevonden')

    def openxml(self, event=None):
        "load XML file (after checking if current needs to be saved)"
        ok, fname = self.gui.file_to_read()
        if ok:
            try:
                tree, prefixes, uris = parse_nsmap(fname)
            except et.ParseError as e:
                self.gui.meldfout(str(e))
            else:
                self.xmlfn = fname
                self.init_tree(tree.getroot(), prefixes, uris)

    def expand(self, event=None):
        """show all children of the current node
        """
        self.gui.expand_item()

    def collapse(self, event=None):
        """hide all children of the current node
        """
        self.gui.collapse_item()

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
        out = ['search for'] if any((ele, attr, text)) else ['']
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
            out.append(f'   `{text}`')
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

    def about(self, event=None):
        "Credits"
        self.gui.meldinfo("Started in 2008 by Albert Visser\nWritten in Python")
