Files in this directory
=======================
AXE stands for "Albert's XML editor"

xmleditor.py
    Starter program for the stuff in package "axe"
    imports axe(_wx)
readme.rst
    information and usage notes
files.rst
    this file

Files in the package
--------------------

__init__.py
    (empty) package indicator
axe_base.py
    gui-independent code, imported into all versions
    imports os, sys, shutil, xml.etree.ElementTree
axe_qt.py
    GUI code, PyQt version
    imports os, logging, sys, functools, PyQt4, symbols from axe_base.py
axe_ppg.py
    GUI code, PocketPyGui version - not adapted for working with axe_base.py
    imports shutil, copy, xml.etree.ElementTree, ppygui
axe_tk.py - not adapted for working with axe_base.py
    GUI code, Tkinter version
    uses Tree widget by Gene Cash
    imports shutil, tkinter, Tree, xml.etree.ElementTree
    an attempt was made to make this work with Python3 and ttk
axe_wx.py
    GUI code, wxPython version
    imports os, sys, wxpython, symbols from axe_base
axedtd_wx.py
    cloned and adapted from axe_wx.py
    standalone dtd editor, intended to be callable from within AXE
    imports shutil, copy, xml.etree.ElementTree, parsedtd
parsedtd.py
    dtd parser, intended to be used by axedtd (GUI independent code)

axe.ico
    homemade application icon
axe.png
    png version of the icon
