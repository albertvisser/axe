#! /usr/bin/env python3
"""Startup script for XML Viewer
"""
import sys
from axe.base import Editor

if len(sys.argv) > 1:
    Editor(sys.argv[1], readonly=True)
else:
    Editor('', readonly=True)
