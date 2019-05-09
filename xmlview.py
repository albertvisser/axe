#! /usr/bin/env python3
"""Startup script for XML viewer - intermediary for choosing a GUI toolkit
"""
import sys
# from axe.xmlviewer_qt import axe_gui
from axe.xmlviewer_wx import axe_gui


def main(args):
    "start GUI with passed arguments"
    axe_gui(args)

if __name__ == '__main__':
    main(sys.argv)
