"""dispatcher to import from the right gui toolkit module
"""
from .toolkit import toolkit
if toolkit == 'qt':
    from .qtgui import Gui, DialogGui, show_dialog
elif toolkit == 'wx':
    from .wxgui import Gui, DialogGui, show_dialog
