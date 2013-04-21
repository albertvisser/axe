import sys
## from axe_ppg import MainGui
## from axe_tk import MainGui - NB werkt niet op deze manier
## from axe.axe_wx import axe_gui
from axe.axe_qt import axe_gui

def main(args):
    x = axe_gui(args)

if __name__ == '__main__':
    main(sys.argv)
