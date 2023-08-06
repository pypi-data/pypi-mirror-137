try:
    from PySide6 import QtCore
except ImportError:
    print("WARNING: macholib found PySide6, but cannot import")

plugin_dir = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.PluginsPath)

