#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# main.py
# (c) 2010 - Guillaume Ryckelynck
#

"""Programme python de manipulation de fichiers de métadonnées au format XML

Ce petit programme en Python, basé sur Tkinter, permet de manipuler simplement
des fichiers au format XML.
"""

__author__ = "Guillaume Ryckelynck"
__copyright__ = "Copyright 2011-2015, Guillaume Ryckelynck"
__credits__ = ["Guillaume Ryckelynck"]
__license__ = "GPL"
__version__ = "1.08"
__maintainer__ = "Guillaume Ryckelynck"
__email__ = "guillaume@ryckelynck.info"
__status__ = "Production"

try:
    import os
    import glob
    from xml.dom import minidom
    from xml.etree import ElementTree
    import string
    import unicodedata
    import re
    import ConfigParser
    import webbrowser
    from Tkinter import *
    import tkFileDialog
    import ScrolledText
    import codecs
    # Import tkpyms_module
    import zaphir_module

except ImportError, e:
    print "Import error! Application cannot start:", e
    sys.exit(1)


### Initialisation des variables ###
APP_NAME = "Zaphir"
APP_VERSION = "1.08"
PATH_SCRIPT = os.getcwd()
FILE_CFG = os.path.join(PATH_SCRIPT, 'config', 'zaphir.cfg')
#FILE_CODES = os.path.join(PATH_SCRIPT, 'config', 'codes.cfg')
XML_TMP_FILE = os.path.join(PATH_SCRIPT, 'template', 'CIGAL-CUS_2011_onglets', 'TMP_viewXMLFile.xml')
XSL_FILE = os.path.join('CIGAL-CUS_2011_onglets.xsl')
# XLS_TEMPLATE_FILE = os.path.join(PATH_SCRIPT, 'template', 'xls', 'Form_SaisieMD_ProfilCIGAL_1.08.xls')

# ConfigParser
config = ConfigParser.ConfigParser()
try:
    config.read(FILE_CFG)
    XML_DIR = config.get('FILES', 'XML_DIR')
    XLS_DIR = config.get('FILES', 'XLS_DIR')
except:
    XML_DIR = ''
    XLS_DIR = ''
    print "Erreur de lecture du fichier de configuration."


# Charger les namespace du fichier XML (format ISO 19139 - SFM)
namespaces = { "http://www.isotc211.org/2005/gmd":"gmd", "http://www.opengis.net/gml/3.2":"gml", "http://www.isotc211.org/2005/gts":"gts", "http://www.isotc211.org/2005/gco":"gco", "http://www.w3.org/2001/XMLSchema-instance":"xsi"}
ElementTree._namespace_map.update(namespaces)

### CLASSE DE L'APPLICATION TKINTER ###
class Zaphir_Window(Frame):
    ''' This is the GUI of zaphir application'''

    def __init__(self, master=None):
        ''' Initialisation de l'application '''

        # Initialise the base class
        Frame.__init__(self, master)

        #Window title
        self.master.title(APP_NAME + " - " + APP_VERSION)
        self.grid(padx=10,pady=10,sticky=N+S+E+W)
        self.CreateWidgets()
        self.txt_messages.insert(END, u"Dossier listé : %s\n" % (XML_DIR,))
        self.txt_messages.insert(END, u"Dossier listé : %s\n" % (XLS_DIR,))
        self.getListFiles()

        # Action à la fermeture de le fenêtre
        self.master.protocol("WM_DELETE_WINDOW", self.quit)

    # WIDGETS
    def CreateWidgets(self):
        ''' Crateate widgets in main window '''

        # Create 5 frames
        self.frame_menu = Frame(self)
        self.frame_menu.grid(row=0, column=0, rowspan=4, sticky=N+S+W+E, padx=10, pady=10)
        self.frame_dirxls = Frame(self)
        self.frame_dirxls.grid(row=0, column=1, sticky=N+S+E+W, padx=5, pady=5)
        self.frame_dirxml = Frame(self)
        self.frame_dirxml.grid(row=1, column=1, sticky=N+S+E+W, padx=5, pady=5)
        self.frame_lst = Frame(self)
        self.frame_lst.grid(row=2, column=1, sticky=N+S+E+W, padx=5, pady=5)
        self.frame_message = Frame(self)
        self.frame_message.grid(row=3, column=1, sticky=N+S+E+W, padx=5, pady=5)
        self.frame_info = Frame(self)
        self.frame_info.grid(row=4, column=1, sticky=E, padx=1, pady=1)

        # Frame 1: create buttons menu in frame colum 1
        self.bt_quit = Button(self.frame_menu, text="Quitter", width=15, command=self.quit)
        self.bt_quit.grid(row=0, column=0, sticky=W+E, padx=2, pady=2)
        #self.lb_menu0 = Label(self.frame_menu, text="XML Files")
        #self.lb_menu0.grid(row=1, column=0, sticky=W+E)
        self.bt_lstFiles = Button(self.frame_menu, text="Actualiser les listes", width=15, command = self.getListFiles)
        self.bt_lstFiles.grid(row=1, column=0, sticky=W+E, padx=2, pady=2)
        # self.bt_lstFiles = Button(self.frame_menu, text="XML vers XLS", width=15, command = self.xml2xls)
        # self.bt_lstFiles.grid(row=2, column=0, sticky=W+E, padx=2, pady=2)
        self.bt_lstFiles = Button(self.frame_menu, text="XLS vers XML", width=15, command = self.xls2xml)
        self.bt_lstFiles.grid(row=3, column=0, sticky=W+E, padx=2, pady=2)
        # self.bt_lstFiles = Button(self.frame_menu, text="Liste des fichiers XML", width=15, command = self.viewXmlListFiles)
        # self.bt_lstFiles.grid(row=4, column=0, sticky=W+E, padx=2, pady=2)
        self.bt_lstFiles = Button(self.frame_menu, text="Voir fiche XML", width=15, command = self.viewXmlFile)
        self.bt_lstFiles.grid(row=5, column=0, sticky=W+E, padx=2, pady=2)
        self.bt_lstFiles = Button(self.frame_menu, text="Aide et infos", width=15, command = self.help)
        self.bt_lstFiles.grid(row=6, column=0, sticky=W+E, padx=2, pady=2)

        # Frame 2: create entry for XML directory
        # getXmlDirectory
        self.lb_destXmlDirectory = Label(self.frame_dirxml, text="Dossier XML:", width=12, anchor=W)
        self.lb_destXmlDirectory.grid(row=0, column=0, sticky=E)
        self.ent_destXmlDirectory = Entry(self.frame_dirxml, width=100)
        self.ent_destXmlDirectory.insert(0, XML_DIR)
        self.ent_destXmlDirectory.grid(row=0, column=1, sticky=W+E)
        self.bt_destXmlDirectory = Button(self.frame_dirxml, text="...", command=self.getXmlDirectory)
        self.bt_destXmlDirectory.grid(row=0, column=2, sticky=E)

        # Frame 3: create entry for XLS directory
        # getXlsDirectory
        self.lb_destXlsDirectory = Label(self.frame_dirxls, text="Dossier XLS:", width=12, anchor=W)
        self.lb_destXlsDirectory.grid(row=0, column=0, sticky=W)
        self.ent_destXlsDirectory = Entry(self.frame_dirxls, width=100)
        self.ent_destXlsDirectory.insert(0, XLS_DIR)
        self.ent_destXlsDirectory.grid(row=0, column=1, sticky=W+E)
        self.bt_destXlsDirectory = Button(self.frame_dirxls, text="...", command=self.getXlsDirectory)
        self.bt_destXlsDirectory.grid(row=0, column=2, sticky=E)

        # Frame 4: create listbox for XML files and XLS files
        self.lb_lstbXmlFiles = Label(self.frame_lst, text="Liste des fichiers XML:")
        self.lb_lstbXmlFiles.grid(row=0, column=3, sticky=W)
        self.sbarx_lstbXmlFiles = Scrollbar(self.frame_lst, orient=HORIZONTAL)
        self.sbary_lstbXmlFiles = Scrollbar(self.frame_lst)
        self.lstb_xmlFiles = Listbox(self.frame_lst, width=50, selectmode=EXTENDED)
        self.lstb_xmlFiles.config(xscrollcommand=self.sbarx_lstbXmlFiles.set)
        self.sbarx_lstbXmlFiles.config(command=self.lstb_xmlFiles.xview)
        self.sbarx_lstbXmlFiles.grid(row=3, column=3, columnspan=2, sticky=E+W)
        self.lstb_xmlFiles.config(yscrollcommand=self.sbary_lstbXmlFiles.set)
        self.sbary_lstbXmlFiles.config(command=self.lstb_xmlFiles.yview)
        self.sbary_lstbXmlFiles.grid(row=1, column=4, sticky=N+S)
        self.lstb_xmlFiles.grid(row=1, column=3, sticky=N+S+W+E)
        self.lstb_xmlFiles.bind("<Double-Button-1>", self.selectXmlFile)

        self.space = Frame(self.frame_lst, width=15)
        self.space.grid(row=0, column=2, sticky=W+E+S+N)

        self.lb_lstbXlsFiles = Label(self.frame_lst, text="Liste des fichiers XLS:")
        self.lb_lstbXlsFiles.grid(row=0, column=0, sticky=W)
        self.sbarx_lstbXlsFiles = Scrollbar(self.frame_lst, orient=HORIZONTAL)
        self.sbary_lstbXlsFiles = Scrollbar(self.frame_lst)
        self.lstb_xlsFiles = Listbox(self.frame_lst, width=50, selectmode=EXTENDED)
        self.lstb_xlsFiles.config(xscrollcommand=self.sbarx_lstbXlsFiles.set)
        self.sbarx_lstbXlsFiles.config(command=self.lstb_xlsFiles.xview)
        self.sbarx_lstbXlsFiles.grid(row=3, column=0, columnspan=2, sticky=E+W)
        self.lstb_xlsFiles.config(yscrollcommand=self.sbary_lstbXlsFiles.set)
        self.sbary_lstbXlsFiles.config(command=self.lstb_xlsFiles.yview)
        self.sbary_lstbXlsFiles.grid(row=1, column=1, sticky=N+S)
        self.lstb_xlsFiles.grid(row=1, column=0, sticky=N+S+W+E)
        self.lstb_xlsFiles.bind("<Double-Button-1>", self.selectXlsFile)

        # Frame 5: create message box
        self.lb_messages = Label(self.frame_message, text="Messages:")
        self.lb_messages.grid(row=0, column=0, sticky=W)
        self.txt_messages = ScrolledText.ScrolledText(self.frame_message, wrap=WORD, font="arial 9", width=90, height=9)
        self.txt_messages.tag_config("title", font="arial 9 bold")
        self.txt_messages.tag_config("b", font="arial 9 bold")
        self.txt_messages.insert("1.0", "# Fenêtre d'information #\n\n", ("title"))
        self.txt_messages.grid(row=1, column=0, sticky=W+E+S+N)

        # Frame 6: info
        self.lb_info = Label(self.frame_info, text="G. Ryckelynck (Partenariat CIGAL - 2011-2015)", fg="#666", font="Helvetica 8 normal italic")
        self.lb_info.grid(row=0, column=0, sticky=E)

        # Configure main window
        self.master.grid_columnconfigure(0,weight=1)
        self.master.resizable(width=False, height=False)

    # QUIT
    def quit(self):
        config.set('FILES', 'XML_DIR', XML_DIR)
        config.set('FILES', 'XLS_DIR', XLS_DIR)
        config.write(open(FILE_CFG,'w'))
        #config.write(sys.stdout)
        self.master.destroy()

    # HELP
    def help(self):
        self.txt_messages.delete(1.0, END)
        self.txt_messages.insert("1.0", "# Fenêtre d'information #\n\n", ("title"))
        self.txt_messages.insert(END, u"Application %s - %s\n\n" % (APP_NAME, APP_VERSION), ('b'))
        self.txt_messages.insert(END, u"Aide\n", ('b'))
        help = """Application permettant de consulter facilement une liste de fichiers de métadonnées géographiques au format MS Ecel (XLS) et XML (norme ISO 19139).\n
        Usage simple:
            1. Sélectionnez un dossier contenant une liste de fichiers au format Excel (XLS) adaptés à la saisie des métadonnées selon la norme ISO 19115.
            2. Sélectionnez un dossier destination et/ou contenant une liste de fichiers au format XML (ISO 19139).
            3. Choisissez l'action à réaliser:
                - Le bouton "Quitter" permet de quitter l'application.
                - Le bouton "Actualiser les listes" permet simplement de relire le contenu du sossier sélectionné et recharger la liste des fichiers.
                - Le bouton "XLS vers XML" permet de convertir un fichier XLS sélectionné au format XML CONFORME iso 19139/iNSPIRE.
                - Le bouton "Voir fiche" permet de consulter la fiche XML sélectionnée avec une mise en page html.
                - Le bouton "Aide et info" affiche les présentes informations.
        """
        self.txt_messages.insert(END, help)
        self.txt_messages.insert(END, u"\nDéveloppement\n", ('b'))
        self.txt_messages.insert(END, u"Application développée par G. Ryckelynck - Partenariat CIGAL 2011-2015 (www.cigalsace.org)\n")
        self.txt_messages.insert(END, u"Pour tout contact: guillaume.ryckelynck(at)region-alsace.eu \n")

    # GET LIST OF XML FILES
    def getXmlListFiles(self):
        ''' List metadata files '''
        # global namespaces
        # Get list of files
        XML_DIR = self.ent_destXmlDirectory.get()
        fichiers=[]
        l = glob.glob(os.path.join(XML_DIR,'*.xml'))
        for i in l:
            if os.path.isfile(i): fichiers.append(i)

        # print message in text box
        self.txt_messages.insert(END, u"%d fichiers XML listé(s)\n" % (len(fichiers)))
        # clear listbox
        self.lstb_xmlFiles.delete(0, END)

        xpath_title = './/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString'
        for key, value in namespaces.items():
            xpath_title = string.replace(xpath_title, value+':', '{'+key+'}')

        for file in sorted(fichiers):
            xml_title = None
            try:
                xml = ElementTree.parse(os.path.join(XML_DIR, file))
                xml_title = xml.find(xpath_title)
                title = xml_title.text
            except:
                title = "Erreur lors de la lecture du fichier XML"

            self.lstb_xmlFiles.insert(END, "%d | %s | %s | %d octets" % (fichiers.index(file), title, os.path.basename(file), os.path.getsize(file)))

    # GET LIST OF XLS FILES
    def getXlsListFiles(self):
        ''' List of XLS metadata files '''
        # Get list of files
        XLS_DIR = self.ent_destXlsDirectory.get()
        ext = ('*.xls', '*.xlsx')
        f = []
        fichiers = []
        for e in ext:
            f.extend(glob.glob(os.path.join(XLS_DIR, e)))
        # f = glob.glob(os.path.join(XLS_DIR,'*.xls*'))
        for i in f:
            if os.path.isfile(i): fichiers.append(i)

        # self.txt_messages.delete(1.0, END)
        # self.txt_messages.insert("1.0", "# Fenêtre d'information #\n\n", ("title"))
        self.txt_messages.insert(END, u"%d fichiers XLS listé(s)\n" % (len(fichiers)))
        # clear listbox
        self.lstb_xlsFiles.delete(0, END)
        for i in fichiers:
            self.lstb_xlsFiles.insert(END, "%d | %s | %d octets" % (fichiers.index(i), os.path.basename(i), os.path.getsize(i)))

    # GET LIST OF XML AND XLS FILES
    def getListFiles(self):
        # self.txt_messages.delete(1.0, END)
        # self.txt_messages.insert("1.0", "# Fenêtre d'information #\n\n", ("title"))
        self.getXmlListFiles()
        self.getXlsListFiles()
        print u"Listes mises à jour."

    # SELECT A XML FILE
    def selectXmlFile(self, event):
        global namespaces
        # Get path of files
        XML_DIR = self.ent_destXmlDirectory.get()
        # Get selected item of files list
        selectedFile = self.lstb_xmlFiles.get(self.lstb_xmlFiles.curselection()[0])
        self.txt_messages.delete(1.0, END)
        self.txt_messages.insert("1.0", "# Fenêtre d'information #\n\n", ("title"))
        self.txt_messages.insert(END, 'Fichier selectionné: ')
        self.txt_messages.insert(END, '%s \n\n' % (selectedFile,))
        fileName = string.split(selectedFile, ' | ')
        fileName = fileName[1]

        # Préparer les xpath
        xpath_uuid = './/gmd:fileIdentifier/gco:CharacterString'
        xpath_title = './/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString'
        xpath_abstract = './/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString'
        for key, value in namespaces.items():
            xpath_uuid = string.replace(xpath_uuid, value+':', '{'+key+'}')
            xpath_title = string.replace(xpath_title, value+':', '{'+key+'}')
            xpath_abstract = string.replace(xpath_abstract, value+':', '{'+key+'}')

        xml = ElementTree.parse(os.path.join(XML_DIR, fileName))
        uuid = xml.find(xpath_uuid)
        title = xml.find(xpath_title)
        abstract = xml.find(xpath_abstract)
        if (uuid is not None) and (title is not None) and (abstract is not None):
            self.txt_messages.insert(END, u'UUID: ')
            self.txt_messages.insert(END, uuid.text + "\n", ("b"))
            self.txt_messages.insert(END, u'Titre: ')
            self.txt_messages.insert(END, title.text + "\n", ("b"))
            self.txt_messages.insert(END, u'Résumé: ' + abstract.text + "\n")
        else:
            self.txt_messages.insert(END, u'Fichier XML illisible.')

    # SELECT A XLS FILE
    def selectXlsFile(self, event):
        pass

    # VIEW LIST OF XML FILES
    def viewXmlListFiles(self):
        ''' List metadata files '''
        # Get list of files
        XML_DIR = self.ent_destXmlDirectory.get()
        fichiers=[]
        l = glob.glob(os.path.join(XML_DIR,'*.xml'))
        for i in l:
            if os.path.isfile(i): fichiers.append(i)

        self.txt_messages.delete(1.0, END)
        self.txt_messages.insert("1.0", "# Fenêtre d'information #\n\n", ("title"))
        self.txt_messages.insert(END, u"Lecteure en cours... \n\n")

        # clear listbox
        #self.lstb_xmlFiles.delete(0, END)
        xpath_title = './/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString'
        for key, value in namespaces.items():
            xpath_title = string.replace(xpath_title, value+':', '{'+key+'}')

        for fichier in sorted(fichiers):
            try:
                xml = ElementTree.parse(os.path.join(XML_DIR, fichier))
                title = xml.find(xpath_title)
                title = title.text
            except:
                title = 'Erreur lors de la lecture du fichier'

            #self.lstb_xmlFiles.insert(END, "%d | %s | %d octets" % (fichiers.index(i), os.path.basename(i), os.path.getsize(i)))
            self.txt_messages.insert(END, u" > ")
            self.txt_messages.insert(END, u"%s" % (title,), ('b'))
            self.txt_messages.insert(END, u" = ")
            self.txt_messages.insert(END, u'"%s" \n' % (os.path.basename(fichier),),)

        self.txt_messages.insert(END, u"\n%d fichiers listé(s)\n" % (len(fichiers)))

    # GET XML DIRECTORY
    def getXmlDirectory(self):
        global XML_DIR
        self.directory = tkFileDialog.askdirectory(initialdir=XML_DIR, title='Choisissez un repertoire')
        if len(self.directory) > 0:
            XML_DIR = self.directory
            self.ent_destXmlDirectory.delete(0, END)
            self.ent_destXmlDirectory.insert(0, XML_DIR)
            self.getXmlListFiles()
            text = u"Vous avez choisi le repertoire %s" % (XML_DIR,)
            print text
            self.txt_messages.insert(END, u'\n')
            self.txt_messages.insert(END, text + u'\n')

    # GET XLS DIRECTORY
    def getXlsDirectory(self):
        global XLS_DIR
        self.directory = tkFileDialog.askdirectory(initialdir=XLS_DIR, title='Choisissez un repertoire')
        if len(self.directory) > 0:
            XLS_DIR = self.directory
            self.ent_destXlsDirectory.delete(0, END)
            self.ent_destXlsDirectory.insert(0, XLS_DIR)
            self.getXlsListFiles()
            text = u"Vous avez choisi le repertoire %s" % (XLS_DIR,)
            print text
            self.txt_messages.insert(END, u'\n')
            self.txt_messages.insert(END, text + u'\n')

    # CONVERT XML TO XLS
    """
    def xml2xls(self):
        ''' xml2xls '''
        XML_DIR = self.ent_destXmlDirectory.get()
        XLS_DIR = self.ent_destXlsDirectory.get()
        global XLS_TEMPLATE_FILE

        # Get selected item of files list
        rows = self.lstb_xmlFiles.curselection()
        if len(rows) != 0:
            self.txt_messages.delete(1.0, END)
            self.txt_messages.insert("1.0", u"# Fenêtre d'information #\n\n", ("title"))
            for row in rows:
                selectedFile = self.lstb_xmlFiles.get(row)
                self.txt_messages.insert(END, u'Fichier XML selectionné: %s \n' % (selectedFile,))
                fileName = string.split(selectedFile, u' | ')
                fileName = fileName[2]
                filePath = os.path.join(XML_DIR, fileName)
                self.txt_messages.insert(END, u"Traitement du fichier: "+fileName+"\n")
                xml_file = modules.xml2xls.XML_File(filePath)
                # error = xml_file.xml2xls(XLS_DIR, XLS_TEMPLATE_FILE)
                try:
                    error = xml_file.xml2xls(XLS_DIR, XLS_TEMPLATE_FILE)
                    # error += '\n=> Le fichier '+fileName+' a tout de même été converti en XML.'
                    # pass
                except:
                    error = u'Erreur de transformation.'
                self.txt_messages.insert(END, error+'\n')
            self.getListFiles()
        else:
            print u"Aucun fichier sélectionné"
            self.txt_messages.delete(1.0, END)
            self.txt_messages.insert("1.0", u"# Fenêtre d'information #\n\n", ("title"))
            self.txt_messages.insert(END, u'Aucun fichier selectionné.')
    """

    # CONVERT XLS TO XML
    def xls2xml(self):
        ''' xls2xml '''
        XML_DIR = self.ent_destXmlDirectory.get()
        XLS_DIR = self.ent_destXlsDirectory.get()

        # Get selected item of files list
        rows = self.lstb_xlsFiles.curselection()
        if len(rows) != 0:
            self.txt_messages.delete(1.0, END)
            self.txt_messages.insert("1.0", "# Fenêtre d'information #\n\n", ("title"))
            for row in rows:
                selectedFile = self.lstb_xlsFiles.get(row)
                self.txt_messages.insert(END, 'Fichier XLS selectionné: %s \n' % (selectedFile,))
                fileName = string.split(selectedFile, ' | ')
                fileName = fileName[1]
                filePath = os.path.join(XLS_DIR, fileName)
                self.txt_messages.insert(END, u"Traitement du fichier: "+fileName+"\n")
                # xls_file = xls2xml.XLS_File(filePath)
                # error = xls_file.xls2xml(XML_DIR)
                error = zaphir_module.convert_xls2xml(filePath, XML_DIR)
                try:
                    # error = zaphir_module.convert_xls2xml(filePath, XML_DIR)
                    pass
                except:
                    error = 'Erreur de transformation.'
                self.txt_messages.insert(END, error+'\n')
            self.getListFiles()
        else:
            print u"Aucun fichier sélectionné"
            self.txt_messages.delete(1.0, END)
            self.txt_messages.insert("1.0", u"# Fenêtre d'information #\n\n", ("title"))
            self.txt_messages.insert(END, u'Aucun fichier selectionné.')

    # VIEW XML FILE
    def viewXmlFile(self):
        if self.lstb_xmlFiles.size() > 0 and self.lstb_xmlFiles.curselection() :
            # Get selected item of files list
            selectedFile = self.lstb_xmlFiles.get(self.lstb_xmlFiles.curselection()[0])
            self.txt_messages.delete(1.0, END)
            self.txt_messages.insert("1.0", "# Fenêtre d'information #\n\n", ("title"))
            self.txt_messages.insert(END, 'Fichier selectionné: ')
            self.txt_messages.insert(END, '%s \n' % (selectedFile,))
            fileName = string.split(selectedFile, ' | ')
            fileName = fileName[2]

            xml = ElementTree.parse(os.path.join(XML_DIR, fileName))
            root = xml.getroot()
            root = ElementTree.tostring(root)

            if os.path.isfile(XML_TMP_FILE):
                os.remove(XML_TMP_FILE)
            # Créer le fichier "xsl/viewXMLFile.xml", l'ouvrir et écrire la liste des contextes
            fichier = open(XML_TMP_FILE,"w")
            fichier.write('<?xml version="1.0" encoding="utf-8"?>\n')
            fichier.write('<?xml-stylesheet href="'+XSL_FILE+'" type="text/xsl"?>\n')
            fichier.write(str(root))
            webbrowser.open(XML_TMP_FILE)
        else :
            print u"Aucun fichier sélectionné"
            self.txt_messages.delete(1.0, END)
            self.txt_messages.insert("1.0", "# Fenêtre d'information #\n\n", ("title"))
            self.txt_messages.insert(END, u'Aucun fichier selectionné.')


### PROGRAMME PRINCIPAL ###
if __name__ == "__main__":
    Zaphir_Window = Zaphir_Window()
    Zaphir_Window.mainloop()
