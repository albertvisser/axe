from .toolkit import toolkit
if toolkit == 'qt':
    from .gui_qt import Gui
elif toolkit == 'wx':
    from .gui_wx import Gui
