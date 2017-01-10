#! python3

# -*- coding: utf-8 -*-

"""
pyqt5-dumper

Dumps all PyQt5 classes to a destination JSON file.
The JSON file is to be used with vim-pyqt5-importer VIM plugin.
"""

__author__ = "Robert Basic"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "robertbasic.com@gmail.com"

import sys
import inspect
import pkgutil
import json

def dump_pyqt5(dump_file_name):
    try:
        import PyQt5
    except ImportError:
        print("Can't import PyQt5")
        sys.exit()

    package = PyQt5

    packages = []
    for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__):
        if modname[:2].lower() == "qt":
            pyqt5_package_name = "%s.%s" % (package.__name__, modname)
            packages.append((modname, pyqt5_package_name))

    __import__('PyQt5', globals(), locals(), [p[0] for p in packages], 0)

    pyqt5_packages = {}
    for pyqt5_package in [p[1] for p in packages]:
        for package_name, package_object in inspect.getmembers(sys.modules[pyqt5_package], inspect.isclass):
            pyqt5_packages[package_name] = pyqt5_package.split('.')[1]

    json_dump = json.dumps(pyqt5_packages)

    dump_file = open(dump_file_name, "w")
    dump_file.write(json_dump)
    dump_file.close()

if __name__ == "__main__":
    dump_file_name = sys.argv[1]
    dump_pyqt5(dump_file_name)
