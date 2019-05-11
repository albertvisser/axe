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
