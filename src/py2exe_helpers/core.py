# See: http://www.py2exe.org/index.cgi/win32com.shell?action=show&redirect=WinShell
# ModuleFinder can't handle runtime changes to __path__, but win32com uses them
try:
    # py2exe 0.6.4 introduced a replacement modulefinder.
    # This means we have to add package paths there, not to the built-in
    # one.  If this new modulefinder gets integrated into Python, then
    # we might be able to revert this some day.
    # if this doesn't work, try import modulefinder
    try:
        import py2exe.mf as modulefinder
    except ImportError:
        import modulefinder
    import win32com, sys
    for p in win32com.__path__[1:]:
        modulefinder.AddPackagePath('win32com', p)
    for extra in ['win32com.shell']: #,'win32com.mapi'
        __import__(extra)
        m = sys.modules[extra]
        for p in m.__path__[1:]:
            modulefinder.AddPackagePath(extra, p)
except ImportError:
    # no build path setup, no worries.
    pass

try:
    # Prevent `_tkinter.TclError: Can't find a usable init.tcl in the following
    # directories` error.  This error seems to occur if `_tkinter` is imported
    # before importing `Tkinter`.  To prevent this from happening, explicitly
    # import `Tkinter` here.
    import Tkinter
except ImportError:
    pass

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

__all__ = ['__version__']
