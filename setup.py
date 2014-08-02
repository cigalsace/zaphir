from distutils.core import setup
import py2exe
import os

'''
setup(
    zipfile = None,
    name="zaphir.exe",
    version="0.5c",
    windows=['main.py'])
'''

'''
setup(
    name="tkpyms_0.5c.exe",
    version="0.5c",
    windows=['main.py'],
    options = {"py2exe": {"optimize": 2,
                          "bundle_files": 1,
                          "compressed": 1}},
    zipfile = None)
'''

setup(
    version = "1.04",
    description = "Zaphir",
    name = "Zaphir.exe",
    # targets to build
    windows = [ {'script': "zaphir.py",
                'icon_resources': [(1, 'icon.ico')],
                # 'excludes': ["pywin", "pywin.debugger", "pywin.debugger.dbgcon", "pywin.dialogs", "pywin.dialogs.list", "Tkconstants", "Tkinter","tcl"] ,
                'includes': ['tkpyms_module']
                }],
    options = {"py2exe": {"compressed": 1, "optimize": 2, "bundle_files": 3,}},
    zipfile = None,
    data_files = [('config',['config/zaphir.cfg']),
                  ('', ['history.txt', 'icon.ico']),
                  # ('template/xsl',['template/xsl/XSL_CIGAL-ISO19139_view_1.06']), 
                  # ('template/xsl/css',['template/xsl/css/]),
                  # ('modules',['modules/__init__.py', 'modules/xml2xls.py', 'modules/xls2xml.py'])
        ],
    )
    
    # Commande pour executer : python setup.py py2exe
    # Pensez a copier les fichiers necessaires (XSL, etc.) manuellement...