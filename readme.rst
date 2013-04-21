XML Editor
==========

At some point I got the idea that the only proper way to edit an xml file
is in a tree based orientation where element and attribute names
are clearly separated from their contents.

From using it I found out that this idea actually works (for me anyway)...

I'm currently working on adding a simple dtd editor but mostly I'm trying to add
features that allow me to work fast, like keyboard-shortcuts for common actions
and to avoid adding things I don't need.

The DTD parser/editor bit is also an experiment in working with a kind of element
factories I think.

There's also a PyQt version that is meant to smooth the transition in making this
application work in Python 3.

Requirements
------------

- Python (with ElementTree)
- wxPython or PyQT4 (for the current versions)
- Tkinter and Gene Cash's Tree module (for an older version)
- PocketPyGUI (for a PocketPC version)

