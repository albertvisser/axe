# -*- coding: utf-8 -*-
"""
GUI-onafhankelijke code
"""

import os
import sys
import shutil
## import copy
import xml.etree.ElementTree as et

ELSTART = '<>'
TITEL = "Albert's (Simple) XML-editor"
PPATH = os.path.split(__file__)[0]
axe_iconame = os.path.join(PPATH, "axe.ico")

def getshortname(x, attr=False):
    t = ''
    if attr:
        t = x[1]
        if t[-1] == "\n":
            t = t[:-1]
    elif x[1]:
        t = x[1].split("\n",1)[0]
    w = 60
    if len(t) > w:
        t = t[:w].lstrip() + '...'
    strt = ' '.join((ELSTART, x[0]))
    if attr:
        return " = ".join((x[0], t))
    elif t:
        return ": ".join((strt, t))
    else:
        return strt

def find_next(data, search_args, reverse=False, pos=None):
    """searches the flattened tree from start or the given pos
    to find the next item that fulfills the search criteria
    """
    wanted_ele, wanted_attr, wanted_value, wanted_text = search_args
    if reverse:
        data.reverse()

    if pos:
        pos, is_attr = pos
        found_item = False
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
            return None, False # no more data to search

    ele_ok = attr_name_ok = attr_value_ok = attr_ok = text_ok = False
    itemfound = False
    for item, element_name, element_text, attr_list in data:
        if not wanted_ele or wanted_ele in element_name:
            ele_ok = True
        if not wanted_text or wanted_text in element_text:
            text_ok = True

        attr_item = None
        if wanted_attr or wanted_value:
            if reverse:
                attr_list.reverse()
            for attr, name, value in attr_list:
                if not wanted_attr or wanted_attr in name:
                    attr_name_ok = True
                if not wanted_value or wanted_value in value:
                    attr_value_ok = True
                if attr_name_ok and attr_value_ok:
                    attr_ok = True
                    if not (wanted_ele or wanted_text):
                        attr_item = attr
                    break
        else:
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

class XMLTree(object):
    def __init__(self, data):
        self.root = et.Element(data)

    def expand(self, root, text, data):
        if text.startswith(ELSTART):
            node = et.SubElement(root, data[0])
            if data[1]:
                node.text = data[1]
            return node
        else:
            root.set(data[0], data[1])
            return None

    def write(self, fn):
        et.ElementTree(self.root).write(fn, encoding="utf-8")


class AxeMixin(object):
    def __init__(self, parent, id, fn=''):
        self.title = "Albert's XML Editor"
        if fn:
            self.xmlfn = os.path.abspath(fn)
        else:
            self.xmlfn = ''
        self.cut_att = None
        self.cut_el = None
        self._init_gui(parent, id)
        self.rt = et.Element('New')
        self.init_tree()
        if self.xmlfn == '':
            self.openxml()
        else:
            try:
                self.rt = et.ElementTree(file=self.xmlfn).getroot()
            except IOError as err:
                self._meldfout(str(err), abort=True)
            self.init_tree()

    def mark_dirty(self, state, data):
        """past gewijzigd-status aan
        en retourneert de overeenkomstig gewijzigde tekst voor de titel
        """
        self.tree_dirty = state
        if state:
            if not data.endswith(' *'):
                return data + ' *'
        elif data.endswith(' *'):
            return data[:-2]

    def check_tree(self):
        """vraag of er iets moet gebeuren wanneer de data gewijzigd is

        de underscore methode moet in de gui module zijn gedefinieerd
        """
        ok = True
        if self.tree_dirty:
            h = self._ask_yesnocancel("XML data has been modified - "
                "save before continuing?")
            if h == 1:
                self.savexml()
            elif h == -1:
                ok = False
        return ok

    def newxml(self):
        """nieuwe xml boom initialiseren

        de underscore methode moet in de gui module zijn gedefinieerd
        """
        if self.check_tree():
            h = self._ask_for_text("Enter a name (tag) for the root element")
            if not h:
                h = "root"
            self.rt = et.Element(h)
            self.xmlfn = ""
            self.init_tree()

    def openxml(self):
        if self.check_tree():
            ok, fname = self._file_to_read()
            if ok:
                try:
                    rt = et.ElementTree(file=fname).getroot()
                except et.ParseError as e:
                    self._meldfout(str(e))
                    return False
                self.rt = rt
                self.xmlfn = fname
                self.init_tree()

    def savexml(self):
        if self.xmlfn == '':
            self.savexmlas()
        else:
            self.savexmlfile()

    def savexmlas(self):
        d, f = os.path.split(self.xmlfn)
        ok, name = self._file_to_save(d, f)
        if ok:
            self.xmlfn = name
            self.savexmlfile() # oldfile=os.path.join(d,f))
        return ok

    def savexmlfile(self, oldfile=''):
        if oldfile == '':
            oldfile = self.xmlfn + '.bak'
        if os.path.exists(self.xmlfn):
            shutil.copyfile(self.xmlfn, oldfile)
        XMLTree('root').write(self.xmlfn)

    def about(self):
        self.meldinfo("Made in 2008 by Albert Visser\nWritten in (wx)Python")

    def init_tree(self, name=''):
        "stelt titel voor in de visuele tree in en geeft deze terug"
        if name:
            titel = name
        elif self.xmlfn:
            titel = self.xmlfn
        else:
            titel = '[unsaved file]'
        return titel

    def cut(self):
        self.copy(cut=True)

    def delete(self):
        self.copy(cut=True, retain=False)

    def copy(self, cut=False, retain=True): # retain is t.b.v. delete functie
        if cut:
            if retain:
                txt = 'cut'
            else:
                txt = 'delete'
        else:
            txt = 'copy'
        return txt

    def paste_aft(self):
        self.paste(before=False)

    def paste_und(self):
        self.paste(pastebelow=True)

    def paste(self, before=True, pastebelow=False):
        pass

    def ins_aft(self, ev=None):
        self.insert(before=False)

    def ins_chld(self, ev=None):
        self.insert(below=True)

    def insert(self, before=True, below=False):
        pass

