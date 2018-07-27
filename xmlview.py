#! /usr/bin/env python3
"""Startup script for XML Editor - intermediary for choosing a GUI toolkit
"""
import sys
## from axe_ppg import MainGui
## from axe_tk import MainGui - NB werkt niet op deze manier
## from axe.axe_wx import axe_gui
## from axe.axe_qt4 import axe_gui
from axe.xmlviewer import axe_gui


def main(args):
    "start GUI with passed arguments"
    axe_gui(args)

if __name__ == '__main__':
    main(sys.argv)
