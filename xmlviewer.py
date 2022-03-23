#! /usr/bin/env python3
"""Startup script for XML Editor
"""
import sys
from axe.viewer import Viewer

if len(sys.argv) > 1:
    Viewer(sys.argv[1])
else:
    Viewer('')
