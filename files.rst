Files in this directory
=======================
AXE stands for "Albert's XML editor"

__init__.py
    (empty) package indicator
axe_ppg.py
    GUI code, PocketPyGui version
    imports shutil, copy, xml.etree.ElementTree, ppygui
axe_tk.py
    GUI code, Tkinter version
    uses Tree widget by Gene Cash
    imports shutil, tkinter, Tree, xml.etree.ElementTree
axe_wx.py
    GUI code, wxPython version
    imports shutil, copy, xml.etree.ElementTree, wx
axedtd_wx.py
    cloned and adapted from axe_wx.py
    standalone dtd editor, intended to be callable from within AXE
    imports shutil, copy, xml.etree.ElementTree, wx
parsedtd.py
    dtd parser, intended to be used by axedtd
xmleditor.py
    Starter program
    imports axe(_wx)

axe.ico
    homemade application icon