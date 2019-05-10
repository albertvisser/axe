# -*- coding: utf-8 -*-
"""
XMLEdit GUI-onafhankelijke code
"""

import os
import pathlib
## import sys
# import shutil
## import copy
import xml.etree.ElementTree as et
import logging

# from axe.gui import Gui

ELSTART = '<>'
TITEL = "Albert's (Simple) XML editor"
APATH = pathlib.Path(__file__).parent
axe_iconame = str(APATH / "axe.ico")
# always log in program directory
LOGFILE = APATH.parent / 'logs' / 'axe_qt.log'
LOGPLEASE = 'DEBUG' in os.environ and os.environ["DEBUG"] != "0"
if LOGPLEASE:
    if not LOGFILE.parent.exists():
        LOGFILE.parent.mkdir()
    if not LOGFILE.exists():
        LOGFILE.touch()
    logging.basicConfig(filename=str(LOGFILE),
                        level=logging.DEBUG, format='%(asctime)s %(message)s')


def log(message):
    """if enabled, write a line to the log"""
    if LOGPLEASE:
        logging.info(message)


def getshortname(x, attr=False):
    """build and return a name for this node
    """
    x, ns_prefixes, ns_uris = x
    t = ''
    if attr:
        t = x[1]
        if t[-1] == "\n":
            t = t[:-1]
    elif x[1]:
        t = x[1].split("\n", 1)[0]
    w = 60
    if len(t) > w:
        t = t[:w].lstrip() + '...'
    fullname = x[0]
    if fullname.startswith('{'):
        uri, localname = fullname[1:].split('}')
        for i, x in enumerate(ns_uris):
            if x == uri:
                prefix = ns_prefixes[i]
                break
        fullname = ':'.join((prefix, localname))
    strt = ' '.join((ELSTART, fullname))
    if attr:
        return " = ".join((fullname, t))
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


# def parse_nsmap(file):
#     """analyze namespaces
#     """
#     root = None
#     ns_prefixes = []
#     ns_uris = []
#
#     for event, elem in et.iterparse(file, ("start-ns", "start")):
#         if event == "start-ns":
#             ns_prefixes.append(elem[0])
#             ns_uris.append(elem[1])
#         elif event == "start":
#             if root is None:
#                 root = elem
#
#     return et.ElementTree(root), ns_prefixes, ns_uris


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
