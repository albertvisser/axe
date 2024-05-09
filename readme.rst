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


Usage
-----

Call ``xmleditor.py`` in the top directory, supply a filename if needed .

Use ``toolkit.py`` in the program directory (``axe``) to define which gui toolkit to use.

I have configured my file manager to call this program on the file selected.


Requirements
------------

- Python (with ElementTree)
- PyQt or wxPhoenix for the current version

