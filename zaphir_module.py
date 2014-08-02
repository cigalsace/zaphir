#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Name:        TkPyms Modules
# Purpose:     Convert Excel file to XML ISO 19139/Inspire file using Python and XLRD and XLWT
#
# Author:      Guillaume Ryckelynck
#
# Created:     25/07/2011
# Modified:    25/01/2012
# Version:     0.3
# Copyright:   (c) Guillaume Ryckelynck / CIGAL 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------


"""
Programme python de conversion de fichiers de métadonnées du format MS Excel vers le format XML ISO 19139 / Inspire.
"""

__author__ = "Guillaume Ryckelynck"
__copyright__ = "Copyright 2011, Guillaume Ryckelynck"
__credits__ = ["Guillaume Ryckelynck"]
__license__ = "GPL"
__version__ = "0.3"
__maintainer__ = "Guillaume Ryckelynck"
__email__ = "guillaume@ryckelynck.info"
__status__ = "Developement"

import os
import sys
import glob
import uuid
import datetime
import time
import ConfigParser
import urlparse

# from htmlentitydefs import codepoint2name as entities
# import config.cellname as cellname
# import config.codelists as codelists
import json


try:
    import xlrd
    import xlwt
except ImportError, e:
    print "Import error! Application cannot start:", e
    sys.exit(1)


### Initialisation des variables ###
APP_NAME = "TkPyms Module"
APP_VERSION = "0.3"
PATH_SCRIPT = os.path.dirname(sys.argv [0])

# Indique s'il faut utiliser la référence xy
XY = None

codelists_js = open('config/codelists.cfg')
codelists = json.load(codelists_js)
cellname_js = open('config/cellname.cfg')
cellname = json.load(cellname_js)


# ------------------------------------------------------------------------------
# CONVERT_XLS2XML
#
# Fonction de conversion d'un fichier MS Excel vers XML
# ------------------------------------------------------------------------------
def convert_xls2xml(xls_file, xml_dir):

        # Geston des erreurs
        Error = u''
        Error_CreateFile = u''

        wb = xlrd.open_workbook(xls_file, encoding_override="utf-8")
        
        # Liste des feuilles déclarées dans le fichier de configuration
        sh = {}
        for s in cellname['sheets']:
            try:
                sh[s] = wb.sheet_by_name(s)
            except:
                print "La Feuille " + str(s) + " n'existe pas."

        # Liste des cellules nommées dans le fichier MS Excel
        lst_name = wb.name_map
        # print len(lst_name), u'cellules nommées dans le fichier Excel.'

        str19139 = u'<?xml version="1.0" encoding="UTF-8"?>\n'
        str19139 += u'<gmd:MD_Metadata xsi:schemaLocation="http://www.isotc211.org/2005/gmd http://schemas.opengis.net/iso/19139/20060504/gmd/gmd.xsd" xmlns:gmx="http://www.isotc211.org/2005/gmx" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gml="http://www.opengis.net/gml" xmlns:xlink="http://www.w3.org/1999/xlink">\n'


        # MD_FileIdentifier
        e, MD_FileIdentifier = _get_xls_value('md_fileidentifier', lst_name, sh, 'string')
        # e, MD_FileIdentifier = _get_xls_value2(sh, cellname.md_fileidentifier, 'string')
        MD_FileIdentifier = _encodexml(MD_FileIdentifier)
        if not MD_FileIdentifier:
            Error += u"MD_FileIdentifier: aucun UUID renseignée. Utilisation du nom de fichier XLS comme UUID... "
            MD_FileIdentifier, ext =  os.path.splitext(os.path.basename(xls_file))
            Error += u"MD_FileIdentifier = " + MD_FileIdentifier + "\n"
        else:
            str19139 += u'<gmd:fileIdentifier><gco:CharacterString>' + MD_FileIdentifier + u'</gco:CharacterString></gmd:fileIdentifier>\n'

        # MD_Language
        MD_Language = u'1' # Valeur par défaut : "Français"
        e, MD_Language = _get_xls_value('md_language', lst_name, sh, 'string')
        if MD_Language: MD_Language = MD_Language.split()[0]
        
        if MD_Language in codelists['LanguageCode']:
            str19139 += u'<gmd:language><gmd:LanguageCode codeList="http://www.loc.gov/standards/iso639-2/" codeListValue="' + codelists['LanguageCode'][MD_Language] + u'">' + codelists['LanguageCode'][MD_Language] + u'</gmd:LanguageCode></gmd:language>\n'
        else:
            Error += u'MD_Language: erreure de lecture. Une langue pour les métadonnées doit être renseignée.\n'

        # MD_CharacterSet
        e, MD_CharacterSet = _get_xls_value('md_characterset', lst_name, sh, 'string')
        if MD_CharacterSet: MD_CharacterSet = MD_CharacterSet.split()[0]
        if MD_CharacterSet not in codelists['CharacterSetCode']:
            MD_CharacterSet = '4' # Valeur par defaut : "utf8"

        str19139 += u'<gmd:characterSet><gmd:MD_CharacterSetCode codeList="http://www.isotc211.org/2005/resources/codeList.xml#MD_CharacterSetCode" codeListValue="' + codelists['CharacterSetCode'][MD_CharacterSet] + u'">' + codelists['CharacterSetCode'][MD_CharacterSet] + u'</gmd:MD_CharacterSetCode></gmd:characterSet>\n'

        # MD_HierarchyLevel
        MD_HierarchyLevel = u'6' # Valeur par defaut : "dataset"
        e, MD_HierarchyLevel = _get_xls_value('md_hierarchylevel', lst_name, sh, 'string')
        if MD_HierarchyLevel: MD_HierarchyLevel = MD_HierarchyLevel.split()[0]
        
        if not MD_HierarchyLevel:
            Error += u'MD_HierarchyLevel: un niveau de description pour les métadonnées doit être renseignée.\n'
        else:
            str19139 += u'<gmd:hierarchyLevel><gmd:MD_ScopeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_ScopeCode" codeListValue="' + codelists['ScopeCode'][MD_HierarchyLevel] + u'">' +  codelists['ScopeCode'][MD_HierarchyLevel] + u'</gmd:MD_ScopeCode></gmd:hierarchyLevel>\n'

        # MD_Contacts
        Error_MdContacts = 1
        #MD_CntRole = u'11' # Valeur par defaut: "pointofContact"
        for i in range(1, 20):
            e, MD_CntName = _get_xls_value('md_cnt'+str(i)+'_name', lst_name, sh, 'string')
            MD_CntName = _encodexml(MD_CntName)
            e, MD_CntFunction = _get_xls_value('md_cnt'+str(i)+'_fct', lst_name, sh, 'string')
            MD_CntFunction = _encodexml(MD_CntFunction)
            e, MD_CntOrganism = _get_xls_value('md_cnt'+str(i)+'_org', lst_name, sh, 'string')
            MD_CntOrganism = _encodexml(MD_CntOrganism)
            e, MD_CntAddress = _get_xls_value('md_cnt'+str(i)+'_address', lst_name, sh, 'string')
            MD_CntAddress = _encodexml(MD_CntAddress)
            e, MD_CntPostalCode = _get_xls_value('md_cnt'+str(i)+'_cp', lst_name, sh, 'integer')
            e, MD_CntCity = _get_xls_value('md_cnt'+str(i)+'_city', lst_name, sh, 'string')
            e, MD_CntPhone = _get_xls_value('md_cnt'+str(i)+'_tel', lst_name, sh, 'string')
            e, MD_CntEmail = _get_xls_value('md_cnt'+str(i)+'_email', lst_name, sh, 'string')
            MD_CntEmail = _encodexml(MD_CntEmail)
            e, MD_CntRole = _get_xls_value('md_cnt'+str(i)+'_role', lst_name, sh, 'string')
            if MD_CntRole: MD_CntRole = MD_CntRole.split()[0]

            if MD_CntOrganism and MD_CntEmail and MD_CntRole in codelists['RoleCode']:
                Error_MdContacts = 0
            if MD_CntOrganism and MD_CntRole in codelists['RoleCode']:
                str19139 += u'<gmd:contact>\n'
                str19139 += u'<gmd:CI_ResponsibleParty>\n'
                if MD_CntName:
                    str19139 += u'<gmd:individualName><gco:CharacterString>' + MD_CntName + '</gco:CharacterString></gmd:individualName>\n'
                if MD_CntOrganism:
                    str19139 += u'<gmd:organisationName><gco:CharacterString>' + MD_CntOrganism + '</gco:CharacterString></gmd:organisationName>\n'
                if MD_CntFunction:
                    str19139 += u'<gmd:positionName><gco:CharacterString>' + MD_CntFunction + '</gco:CharacterString></gmd:positionName>\n'
                if MD_CntPhone or MD_CntAddress or MD_CntCity or MD_CntPostalCode or MD_CntEmail:
                    str19139 += u'<gmd:contactInfo><gmd:CI_Contact>\n'
                    if MD_CntPhone:
                        str19139 += u'<gmd:phone><gmd:CI_Telephone><gmd:voice><gco:CharacterString>' + MD_CntPhone + '</gco:CharacterString></gmd:voice></gmd:CI_Telephone></gmd:phone>\n'
                    if MD_CntAddress or MD_CntCity or MD_CntPostalCode or MD_CntEmail:
                        str19139 += u'<gmd:address><gmd:CI_Address>\n'
                        if MD_CntAddress:
                            str19139 += u'<gmd:deliveryPoint><gco:CharacterString>' + MD_CntAddress + '</gco:CharacterString></gmd:deliveryPoint>\n'
                        if MD_CntCity:
                            str19139 += u'<gmd:city><gco:CharacterString>' + MD_CntCity + '</gco:CharacterString></gmd:city>\n'
                        if MD_CntPostalCode:
                            str19139 += u'<gmd:postalCode><gco:CharacterString>' + MD_CntPostalCode + '</gco:CharacterString></gmd:postalCode>\n'
                        if MD_CntEmail:
                            str19139 += u'<gmd:electronicMailAddress><gco:CharacterString>' + MD_CntEmail + '</gco:CharacterString></gmd:electronicMailAddress>\n'
                        str19139 += u'</gmd:CI_Address></gmd:address>\n'
                    str19139 += u'</gmd:CI_Contact></gmd:contactInfo>\n'
                str19139 += u'<gmd:role><gmd:CI_RoleCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_RoleCode" codeListValue="' + codelists['RoleCode'][MD_CntRole] + '">' + codelists['RoleCode'][MD_CntRole] + '</gmd:CI_RoleCode></gmd:role>\n'
                str19139 += u'</gmd:CI_ResponsibleParty>\n'
                str19139 += u'</gmd:contact>\n'

        if Error_MdContacts :
            Error += u'MD_Contact: au moins 1 contact pour les métadonnées doit être renseigné (un organisme et une adresse email minimum).\n'

        # MD_DateStamp
        e, MD_DateStamp = _get_xls_value('md_datestamp', lst_name, sh, 'date')
        if MD_DateStamp:
            str19139 += u'<gmd:dateStamp><gco:Date>' + MD_DateStamp + u'</gco:Date></gmd:dateStamp>\n'
        else:
            str19139 += u'<gmd:dateStamp><gco:Date>' + time.strftime('%Y-%m-%d',time.localtime()) + u'</gco:Date></gmd:dateStamp>\n'
            Error += u'MD_DateStamp: erreur de lecture de la date. Une date pour les métadonnées doit être renseignée. La date du jour a été utilisée à la place.\n'
            
        # MD_StandardName
        e, MD_StandardName = _get_xls_value('md_standardname', lst_name, sh, 'string')
        MD_StandardName = _encodexml(MD_StandardName)
        if MD_StandardName :
            str19139 += u'<gmd:metadataStandardName><gco:CharacterString>' + MD_StandardName + '</gco:CharacterString></gmd:metadataStandardName>\n'

        # MD_StandardVersion
        e, MD_StandardVersion = _get_xls_value('md_standardversion', lst_name, sh, 'string')
        MD_StandardVersion = _encodexml(MD_StandardVersion)
        if MD_StandardVersion :
            str19139 += u'<gmd:metadataStandardVersion><gco:CharacterString>' + MD_StandardVersion + '</gco:CharacterString></gmd:metadataStandardVersion>\n'

        # Data_ReferenceSystem
        Error_DataReferenceSystem = 1
        for i in range(1, 20):
            e, Data_ReferenceSystem = _get_xls_value('data_referencesystem'+str(i), lst_name, sh, 'string')
            Data_ReferenceSystem = _encodexml(Data_ReferenceSystem)
            if Data_ReferenceSystem :
                Error_DataReferenceSystem = 0
                str19139 += u'<gmd:referenceSystemInfo><gmd:MD_ReferenceSystem>\n'
                str19139 += u'<gmd:referenceSystemIdentifier><gmd:RS_Identifier>\n'
                str19139 += u'<gmd:code><gco:CharacterString>' + Data_ReferenceSystem + '</gco:CharacterString></gmd:code>\n'
                str19139 += u'</gmd:RS_Identifier></gmd:referenceSystemIdentifier>\n'
                str19139 += u'</gmd:MD_ReferenceSystem></gmd:referenceSystemInfo>\n'

        if Error_DataReferenceSystem :
            Error += u'Data_ReferenceSystem: un systeme de projection pour les données doit être renseignée.\n'

        # IDENTIFICATION INFO
        str19139 += u'<gmd:identificationInfo><gmd:MD_DataIdentification>\n'
        str19139 += u'<gmd:citation><gmd:CI_Citation>\n'
        
        # Data_Title
        e, Data_Title = _get_xls_value('data_title', lst_name, sh, 'string')
        Data_Title = _encodexml(Data_Title)
        if Data_Title:
            str19139 = str19139 + u'<gmd:title><gco:CharacterString>' + Data_Title + u'</gco:CharacterString></gmd:title>\n'
        else:
            Error += u'Data_Title: un titre pour les données doit être renseignée.\n'

        # Data_DateCreation / Data_DateRevision / Data_DatePublication
        Error_date = 1
        DateType = (u'creation', u'revision', u'publication')
        for type in DateType:
            e, Data_Date = _get_xls_value('data_date'+type, lst_name, sh, 'date')
            
            if Data_Date:
                Error_date = 0
                str19139 += u'<gmd:date><gmd:CI_Date>\n'
                str19139 += u'<gmd:date><gco:Date>' + Data_Date + '</gco:Date></gmd:date>\n'
                str19139 += u'<gmd:dateType><gmd:CI_DateTypeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode" codeListValue="' + type + '">' + type + '</gmd:CI_DateTypeCode></gmd:dateType>\n'
                str19139 += u'</gmd:CI_Date></gmd:date>\n'

        if Error_date: Error += u'Data_Date: une date pour les données doit être renseignée.\n'

        # Data_presentationForm
        # Utilisé pour les cartes (valeur = mapDigital)
        e, Data_PresentationForm = _get_xls_value('data_presentationform', lst_name, sh, 'string')
        Data_PresentationForm = _encodexml(Data_PresentationForm)
        if Data_PresentationForm:
            str19139 = str19139 + u'<gmd:presentationForm>\n'
            str19139 = str19139 + u'<gmd:CI_PresentationFormCode codeListValue="' + Data_PresentationForm + u'" codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_PresentationFormCode" />\n'
            str19139 = str19139 + u'</gmd:presentationForm>\n'
        
        # Data_Identifier
        # Renseigner MD_FileIdentifier comme Data_Identifier par défaut
        if MD_FileIdentifier != '':
            Data_Code0 = MD_FileIdentifier
            Data_CodeSpace0 = 'MD_URI'
            str19139 += u'<gmd:identifier><gmd:RS_Identifier>\n'
            str19139 += u'<gmd:code><gco:CharacterString>' + Data_Code0 + '</gco:CharacterString></gmd:code>\n'
            str19139 += u'<gmd:codeSpace><gco:CharacterString>' + Data_CodeSpace0 + '</gco:CharacterString></gmd:codeSpace>\n'
            str19139 += u'</gmd:RS_Identifier></gmd:identifier>\n'
        
        for i in range(1, 20):
            e, Data_Code = _get_xls_value('data_code'+str(i), lst_name, sh, 'string')
            Data_Code = _encodexml(Data_Code)
            e, Data_CodeSpace = _get_xls_value('data_codespace'+str(i), lst_name, sh, 'string')
            Data_CodeSpace = _encodexml(Data_CodeSpace)
            
            if (Data_Code and (Data_CodeSpace != 'MD_URI')) :
                str19139 += u'<gmd:identifier><gmd:RS_Identifier>\n'
                str19139 += u'<gmd:code><gco:CharacterString>' + Data_Code + '</gco:CharacterString></gmd:code>\n'
                str19139 += u'<gmd:codeSpace><gco:CharacterString>' + Data_CodeSpace + '</gco:CharacterString></gmd:codeSpace>\n'
                str19139 += u'</gmd:RS_Identifier></gmd:identifier>\n'

        str19139 += u'</gmd:CI_Citation></gmd:citation>\n'

        # Data_Abstract
        e, Data_Abstract = _get_xls_value('data_abstract', lst_name, sh, 'string')
        Data_Abstract = _encodexml(Data_Abstract)
        if Data_Abstract:
            str19139 += u'<gmd:abstract><gco:CharacterString>' + Data_Abstract + '</gco:CharacterString></gmd:abstract>\n'
        else:
            Error += u'Data_Abstract: un résumé pour les données doit être renseignée.\n'

        # Data_PointOfContact
        Error_DataPointOfContacts = 1
        #Data_CntRole = u'11' # Valeur par defaut: "pointofContact"
        for i in range(1, 20):
            e, Data_CntName = _get_xls_value('data_cnt'+str(i)+'_name', lst_name, sh, 'string')
            Data_CntName = _encodexml(Data_CntName)
            e, Data_CntFunction = _get_xls_value('data_cnt'+str(i)+'_fct', lst_name, sh, 'string')
            Data_CntFunction = _encodexml(Data_CntFunction)
            e, Data_CntOrganism = _get_xls_value('data_cnt'+str(i)+'_org', lst_name, sh, 'string')
            Data_CntOrganism = _encodexml(Data_CntOrganism)
            e, Data_CntLogo = _get_xls_value('data_cnt'+str(i)+'_logo', lst_name, sh, 'string')
            Data_CntLogo = _encodexml(Data_CntLogo)
            e, Data_CntAddress = _get_xls_value('data_cnt'+str(i)+'_address', lst_name, sh, 'string')
            Data_CntAddress = _encodexml(Data_CntAddress)
            e, Data_CntPostalCode = _get_xls_value('data_cnt'+str(i)+'_cp', lst_name, sh, 'integer')
            e, Data_CntCity = _get_xls_value('data_cnt'+str(i)+'_city', lst_name, sh, 'string')
            e, Data_CntPhone = _get_xls_value('data_cnt'+str(i)+'_tel', lst_name, sh, 'string')
            e, Data_CntEmail = _get_xls_value('data_cnt'+str(i)+'_email', lst_name, sh, 'string')
            Data_CntEmail = _encodexml(Data_CntEmail)
            e, Data_CntRole = _get_xls_value('data_cnt'+str(i)+'_role', lst_name, sh, 'string')
            if Data_CntRole: Data_CntRole = Data_CntRole.split()[0]

            if Data_CntOrganism and Data_CntEmail and Data_CntRole in codelists['RoleCode']:
                Error_DataPointOfContacts = 0
            if Data_CntOrganism and Data_CntRole in codelists['RoleCode']:
                str19139 += u'<gmd:pointOfContact>\n'
                str19139 += u'<gmd:CI_ResponsibleParty>\n'
                if Data_CntName:
                    str19139 += u'<gmd:individualName><gco:CharacterString>' + Data_CntName + '</gco:CharacterString></gmd:individualName>\n'
                if Data_CntOrganism:
                    str19139 += u'<gmd:organisationName><gco:CharacterString>' + Data_CntOrganism + '</gco:CharacterString></gmd:organisationName>\n'
                if Data_CntFunction:
                    str19139 += u'<gmd:positionName><gco:CharacterString>' + Data_CntFunction + '</gco:CharacterString></gmd:positionName>\n'
                if Data_CntPhone or Data_CntAddress or Data_CntCity or Data_CntPostalCode or Data_CntEmail or Data_CntLogo:
                    str19139 += u'<gmd:contactInfo><gmd:CI_Contact>\n'
                    if Data_CntPhone:
                        str19139 += u'<gmd:phone><gmd:CI_Telephone><gmd:voice><gco:CharacterString>' + Data_CntPhone + '</gco:CharacterString></gmd:voice></gmd:CI_Telephone></gmd:phone>\n'
                    if Data_CntAddress or Data_CntCity or Data_CntPostalCode or Data_CntEmail:
                        str19139 += u'<gmd:address><gmd:CI_Address>\n'
                        if Data_CntAddress:
                            str19139 += u'<gmd:deliveryPoint><gco:CharacterString>' + Data_CntAddress + '</gco:CharacterString></gmd:deliveryPoint>\n'
                        if Data_CntCity:
                            str19139 += u'<gmd:city><gco:CharacterString>' + Data_CntCity + '</gco:CharacterString></gmd:city>\n'
                        if Data_CntPostalCode:
                            str19139 += u'<gmd:postalCode><gco:CharacterString>' + Data_CntPostalCode + '</gco:CharacterString></gmd:postalCode>\n'
                        if Data_CntEmail:
                            str19139 += u'<gmd:electronicMailAddress><gco:CharacterString>' + Data_CntEmail + '</gco:CharacterString></gmd:electronicMailAddress>\n'
                        str19139 += u'</gmd:CI_Address></gmd:address>\n'
                    if Data_CntLogo:
                        str19139 += u'<gmd:contactInstructions><gmx:FileName src="' + Data_CntLogo + '">Logo</gmx:FileName></gmd:contactInstructions>\n'
                    str19139 += u'</gmd:CI_Contact></gmd:contactInfo>\n'
                str19139 += u'<gmd:role><gmd:CI_RoleCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_RoleCode" codeListValue="' + codelists['RoleCode'][Data_CntRole] + '">' + codelists['RoleCode'][Data_CntRole] + '</gmd:CI_RoleCode></gmd:role>\n'
                str19139 += u'</gmd:CI_ResponsibleParty>\n'
                str19139 += u'</gmd:pointOfContact>\n'

        if Error_DataPointOfContacts :
            Error += u'Data_PointOfContacts: au moins 1 contact pour les données doit être renseigné (un organisme et une adresse email minimum).\n'

        # Data_MaintenanceFrequency
        Data_MaintenanceFrequency = u'12' # Valeur par defaut: "unknown"
        e, Data_MaintenanceFrequency = _get_xls_value('data_maintenancefrequency', lst_name, sh, 'string')
        if Data_MaintenanceFrequency: Data_MaintenanceFrequency = Data_MaintenanceFrequency.split()[0]
        
        if Data_MaintenanceFrequency and Data_MaintenanceFrequency in codelists['MaintenanceFrequencyCode']:
            str19139 += u'<gmd:resourceMaintenance>\n'
            str19139 += u'<gmd:MD_MaintenanceInformation>\n'
            str19139 += u'<gmd:maintenanceAndUpdateFrequency>\n'
            str19139 += u'<gmd:MD_MaintenanceFrequencyCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_MaintenanceFrequencyCode" codeListValue="' + codelists['MaintenanceFrequencyCode'][Data_MaintenanceFrequency] + '">' + codelists['MaintenanceFrequencyCode'][Data_MaintenanceFrequency] + '</gmd:MD_MaintenanceFrequencyCode>\n'
            str19139 += u'</gmd:maintenanceAndUpdateFrequency>\n'
            str19139 += u'</gmd:MD_MaintenanceInformation>\n'
            str19139 += u'</gmd:resourceMaintenance>\n'

        # Data_BrowseGraphic
        for i in range(1, 20):
            e, Data_BrowseGraphic_Name = _get_xls_value('data_browsegraphic'+str(i)+'_filename', lst_name, sh, 'string')
            Data_BrowseGraphic_Name = _encodexml(Data_BrowseGraphic_Name)
            e, Data_BrowseGraphic_Description = _get_xls_value('data_browsegraphic'+str(i)+'_description', lst_name, sh, 'string')
            Data_BrowseGraphic_Description = _encodexml(Data_BrowseGraphic_Description)
            Data_BrowseGraphic_Type = os.path.splitext(urlparse.urlparse(Data_BrowseGraphic_Name).path)[1]

            if Data_BrowseGraphic_Name:
                str19139 += u'<gmd:graphicOverview>\n'
                str19139 += u'<gmd:MD_BrowseGraphic>\n'
                str19139 += u'<gmd:fileName>\n'
                str19139 += u'<gco:CharacterString>' + Data_BrowseGraphic_Name + '</gco:CharacterString>\n'
                str19139 += u'</gmd:fileName>\n'
                str19139 += u'<gmd:fileDescription>\n'
                str19139 += u'<gco:CharacterString>' + Data_BrowseGraphic_Description + '</gco:CharacterString>\n'
                str19139 += u'</gmd:fileDescription>\n'
                str19139 += u'<gmd:fileType>\n'
                str19139 += u'<gco:CharacterString>'+ Data_BrowseGraphic_Type +'</gco:CharacterString>\n'
                str19139 += u'</gmd:fileType>\n'
                str19139 += u'</gmd:MD_BrowseGraphic>\n'
                str19139 += u'</gmd:graphicOverview>\n'

        
        # Data_Keywords
        Error_DataKeywords = 1
        
        for i in range(1, 20):
            e, Data_Keyword = _get_xls_value('data_keyword'+str(i), lst_name, sh, 'string')
            Data_Keyword = _encodexml(Data_Keyword)
            e, Data_KeywordType = _get_xls_value('data_keyword'+str(i)+'_type', lst_name, sh, 'string')
            if Data_KeywordType: Data_KeywordType = Data_KeywordType.split()[0]
            e, Data_ThesaurusName = _get_xls_value('data_keyword'+str(i)+'_thesaurusname', lst_name, sh, 'string')
            Data_ThesaurusName = _encodexml(Data_ThesaurusName)
            e, Data_ThesaurusDateCreation = _get_xls_value('data_keyword'+str(i)+'_thesaurusdatecreation', lst_name, sh, 'date')
            e, Data_ThesaurusDatePublication = _get_xls_value('data_keyword'+str(i)+'_thesaurusdatepublication', lst_name, sh, 'date')
            e, Data_ThesaurusDateRevision = _get_xls_value('data_keyword'+str(i)+'_thesaurusdaterevision', lst_name, sh, 'date')

            if Data_Keyword :
                Error_DataKeywords = 0
                str19139 += u'<gmd:descriptiveKeywords><gmd:MD_Keywords>\n'
                str19139 += u'<gmd:keyword><gco:CharacterString>' + Data_Keyword + '</gco:CharacterString></gmd:keyword>\n'
                if Data_KeywordType :
                    str19139 += u'<gmd:type><gmd:MD_KeywordTypeCode codeListValue="' + codelists['KeywordTypeCode'][Data_KeywordType] + '" codeList="http://www.isotc211.org/2005/resources/codeList.xml#MD_KeywordTypeCode" /></gmd:type>\n'
                if Data_ThesaurusName :
                    str19139 += u'<gmd:thesaurusName><gmd:CI_Citation>\n'
                    str19139 += u'<gmd:title><gco:CharacterString>' + Data_ThesaurusName + '</gco:CharacterString></gmd:title>\n'
                    if Data_ThesaurusDateCreation:
                        str19139 += u'<gmd:date><gmd:CI_Date>\n'
                        str19139 += u'<gmd:date><gco:Date>' + Data_ThesaurusDateCreation + '</gco:Date></gmd:date>\n'
                        str19139 += u'<gmd:dateType><gmd:CI_DateTypeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode" codeListValue="creation">creation</gmd:CI_DateTypeCode></gmd:dateType>\n'
                        str19139 += u'</gmd:CI_Date></gmd:date>\n'
                    if Data_ThesaurusDateRevision:
                        str19139 += u'<gmd:date><gmd:CI_Date>\n'
                        str19139 += u'<gmd:date><gco:Date>' + Data_ThesaurusDateRevision + '</gco:Date></gmd:date>\n'
                        str19139 += u'<gmd:dateType><gmd:CI_DateTypeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode" codeListValue="revision">revision</gmd:CI_DateTypeCode></gmd:dateType>\n'
                        str19139 += u'</gmd:CI_Date></gmd:date>\n'
                    if Data_ThesaurusDatePublication:
                        str19139 += u'<gmd:date><gmd:CI_Date>\n'
                        str19139 += u'<gmd:date><gco:Date>' + Data_ThesaurusDatePublication + '</gco:Date></gmd:date>\n'
                        str19139 += u'<gmd:dateType><gmd:CI_DateTypeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode" codeListValue="publication">publication</gmd:CI_DateTypeCode></gmd:dateType>\n'
                        str19139 += u'</gmd:CI_Date></gmd:date>\n'
                    str19139 += u'</gmd:CI_Citation></gmd:thesaurusName>\n'
                str19139 += u'</gmd:MD_Keywords></gmd:descriptiveKeywords>\n'

        # INSPIRE Keywords
        Error_DataKeyword = 1
        Data_InspireThesaurusName = u"GEMET - INSPIRE themes, version 1.0"
        Data_InspireThesaurusDatePublication = u"2008-06-01"

        for i in range(1, 20):
            e, Data_InspireKeyword = _get_xls_value('data_inspirekeyword'+str(i), lst_name, sh, 'string')
            if Data_InspireKeyword: Data_InspireKeyword = Data_InspireKeyword.split()[0]
            
            if Data_InspireKeyword:
                Error_DataKeyword = 0
                str19139 += u'<gmd:descriptiveKeywords><gmd:MD_Keywords>\n'
                str19139 += u'<gmd:keyword><gco:CharacterString>' + codelists['InspireThemeCode_fr'][Data_InspireKeyword] + '</gco:CharacterString></gmd:keyword>\n'
                str19139 += u'<gmd:thesaurusName><gmd:CI_Citation>\n'
                str19139 += u'<gmd:title><gco:CharacterString>' + Data_InspireThesaurusName + '</gco:CharacterString></gmd:title>\n'
                str19139 += u'<gmd:date><gmd:CI_Date>\n'
                str19139 += u'<gmd:date><gco:Date>' + Data_InspireThesaurusDatePublication + '</gco:Date></gmd:date>\n'
                str19139 += u'<gmd:dateType><gmd:CI_DateTypeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode" codeListValue="publication">publication</gmd:CI_DateTypeCode></gmd:dateType>\n'
                str19139 += u'</gmd:CI_Date></gmd:date>\n'
                str19139 += u'</gmd:CI_Citation></gmd:thesaurusName>\n'
                str19139 += u'</gmd:MD_Keywords></gmd:descriptiveKeywords>\n'
        if Error_DataKeyword: Error += u'Data_InspireKeyword: au moins 1 mot-clé INSPIRE pour les données doit être renseigné .\n'

        # Data_ResourceConstraints
        # Data_UseLimitation
        Error_DataUseLimitation = 1
        
        for i in range(1, 20):
            e, Data_UseLimitation = _get_xls_value('data_uselimitation'+str(i), lst_name, sh, 'string')
            Data_UseLimitation = _encodexml(Data_UseLimitation)
            if Data_UseLimitation:
                Error_DataUseLimitation = 0
                str19139 += u'<gmd:resourceConstraints><gmd:MD_Constraints>\n'
                str19139 += u'<gmd:useLimitation><gco:CharacterString>' + Data_UseLimitation + '</gco:CharacterString></gmd:useLimitation>\n'
                str19139 += u'</gmd:MD_Constraints></gmd:resourceConstraints>\n'
        if Error_DataUseLimitation: Error += u'Data_UseLimitation: une limite d\'utilisation pour les données doit être renseignée (indiquer: "Aucune limite." le cas échéant).\n'

        str19139 += u'<gmd:resourceConstraints><gmd:MD_LegalConstraints>\n'

        # Data_AccessConstraints
        # Principe d'implémentation retenu: n'est pas obligatoire car par défaut la valeur Data_AccessConstraints = "otherRestrictions" est ajouté et le champ Data_OtherConstraints est lui considéré comme obligatoire
        # Error_DataAccessConstraints = 1
        for i in range(1, 20):
            e, Data_AccessConstraints = _get_xls_value('data_accessconstraints'+str(i), lst_name, sh, 'string')
            if Data_AccessConstraints: Data_AccessConstraints = Data_AccessConstraints.split()[0]
            
            if Data_AccessConstraints and Data_AccessConstraints in codelists['RestrictionCode']:
                str19139 += u'<gmd:accessConstraints>\n'
                str19139 += u'<gmd:MD_RestrictionCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_RestrictionCode" codeListValue="' + codelists['RestrictionCode'][Data_AccessConstraints] + '">' + codelists['RestrictionCode'][Data_AccessConstraints] + '</gmd:MD_RestrictionCode>\n'
                str19139 += u'</gmd:accessConstraints>\n'
        # if Error_DataAccessConstraints: Error += u'Data_AccessConstraints: une contrainte d\'accès doit être précisée pour les données.\n'
        
        # Ajout de Data_AccessConstraints = "otherRestrictions" par défaut
        str19139 += u'<gmd:accessConstraints>\n'
        str19139 += u'<gmd:MD_RestrictionCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_RestrictionCode" codeListValue="otherRestrictions">otherRestrictions</gmd:MD_RestrictionCode>\n'
        str19139 += u'</gmd:accessConstraints>\n'      
        
        # Data_UseConstraints
        # Error_DataUseConstraints = 1
        for i in range(1, 20):
            e, Data_UseConstraints = _get_xls_value('data_useconstraints'+str(i), lst_name, sh, 'string')
            if Data_UseConstraints: Data_UseConstraints = Data_UseConstraints.split()[0]
            
            if Data_UseConstraints and Data_UseConstraints in codelists['RestrictionCode']:
                # Error_DataUseConstraints = 0
                str19139 += u'<gmd:useConstraints>\n'
                str19139 += u'<gmd:MD_RestrictionCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_RestrictionCode" codeListValue="' + codelists['RestrictionCode'][Data_UseConstraints] + '">' + codelists['RestrictionCode'][Data_UseConstraints] + '</gmd:MD_RestrictionCode>\n'
                str19139 += u'</gmd:useConstraints>\n'
        # if Error_DataUseConstraints: Error += u'Data_UseConstraints: une contrainte d\'utilisation doit être précisée pour les données.\n'
                
        # Data_OtherConstraints
        Error_DataOtherConstraints = 1
        for i in range(1, 20):
            e, Data_OtherConstraints = _get_xls_value('data_otherconstraints'+str(i), lst_name, sh, 'string')
            if Data_OtherConstraints: Data_OtherConstraints = Data_OtherConstraints.split()[0]
            
            if Data_OtherConstraints and Data_OtherConstraints in codelists['InspireRestrictionCode']:
                Error_DataOtherConstraints = 0
                str19139 += u'<gmd:otherConstraints><gco:CharacterString>' + codelists['InspireRestrictionCode'][Data_OtherConstraints] + '</gco:CharacterString></gmd:otherConstraints>\n'
        if Error_DataOtherConstraints: Error += u'Data_OtherConstraints: une contrainte d\'accès doit être précisée pour les données (autres contraintes).\n'

        str19139 += u'</gmd:MD_LegalConstraints></gmd:resourceConstraints>\n'

        # Data_Classification
        Data_Classification = u'1' # Valeur par défaut = "Non classifié (unclassified)"
        e, Data_Classification = _get_xls_value('data_classification', lst_name, sh, 'string')
        if Data_Classification: Data_Classification = Data_Classification.split()[0]
        
        if Data_Classification and Data_Classification in codelists['ClassificationCode']:
            str19139 += u'<gmd:resourceConstraints><gmd:MD_SecurityConstraints><gmd:classification>\n'
            str19139 += u'<gmd:MD_ClassificationCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_ClassificationCode" codeListValue="' + codelists['ClassificationCode'][Data_Classification] + '">' + codelists['ClassificationCode'][Data_Classification] + '</gmd:MD_ClassificationCode>\n'
            str19139 += u'</gmd:classification></gmd:MD_SecurityConstraints></gmd:resourceConstraints>\n'
        else:
            Error += u'Data_Classification: le champ "Restriction d\'utilisation" doit être renseigné pour les données.\n'

        # Fin de Data_ResourceConstraints


        # Data_SpatialRepresentationType
        Data_SpatialRepresentationType = u'1' # Valeur par defaut: "vector"
        e, Data_SpatialRepresentationType = _get_xls_value('data_spatialrepresentationtype', lst_name, sh, 'string')
        if Data_SpatialRepresentationType: Data_SpatialRepresentationType = Data_SpatialRepresentationType.split()[0]
        
        if Data_SpatialRepresentationType and Data_SpatialRepresentationType in codelists['SpatialRepresentationTypeCode']:
            str19139 = str19139 + '<gmd:spatialRepresentationType>\n'
            str19139 = str19139 + '<gmd:MD_SpatialRepresentationTypeCode codeList="http://www.isotc211.org/2005/resources/codeList.xml#MD_SpatialRepresentationTypeCode" codeListValue="' + codelists['SpatialRepresentationTypeCode'][Data_SpatialRepresentationType] + '">' + codelists['SpatialRepresentationTypeCode'][Data_SpatialRepresentationType] + '</gmd:MD_SpatialRepresentationTypeCode>\n'
            str19139 = str19139 + '</gmd:spatialRepresentationType>\n'
        else:
            Error += u'Data_SpatialRepresentationType: erreure de lecture du type de représentation spatiale. Un type de représentation spatiale doit être renseignée pour les données.\n'

        # Data_ScaleDenominator / Data_ScaleDistance
        e, Data_ScaleDenominator = _get_xls_value('data_scaledenominator', lst_name, sh, 'integer')
        e, Data_ScaleDistance = _get_xls_value('data_scaledistance', lst_name, sh, 'string')
        if not Data_ScaleDenominator and not Data_ScaleDistance:
            Error += u'Data_ScaleDenominator / Data_ScaleDistance: une échelle ou une résolution doit être renseignée pour les données.\n'
        else:
            str19139 = str19139 + '<gmd:spatialResolution><gmd:MD_Resolution>\n'
            if Data_ScaleDenominator:
                str19139 = str19139 + '<gmd:equivalentScale><gmd:MD_RepresentativeFraction>\n'
                str19139 = str19139 + '<gmd:denominator><gco:Integer>' + Data_ScaleDenominator + '</gco:Integer></gmd:denominator>\n'
                str19139 = str19139 + '</gmd:MD_RepresentativeFraction></gmd:equivalentScale>\n'
            if Data_ScaleDistance:
                str19139 = str19139 + '<gmd:distance><gco:Distance uom="http://standards.iso.org/ittf/PublicityAvailableStandards/ISO_19139_Schemas/resources.uom/ML_gmxUom.xml#m">' + Data_ScaleDistance + '</gco:Distance></gmd:distance>\n'
            str19139 = str19139 + '</gmd:MD_Resolution></gmd:spatialResolution>\n'

        # Data_Language
        Error_DataLanguage = 1
        #Data_Language = u'1' # Valeur par defaut: "français"
        for i in range(1, 20):
            e, Data_Language = _get_xls_value('data_language'+str(i), lst_name, sh, 'string')
            if Data_Language: Data_Language = Data_Language.split()[0]
            if Data_Language and Data_Language in codelists['LanguageCode']:
                Error_DataLanguage = 0
                str19139 += u'<gmd:language>\n'
                str19139 += u'<gmd:LanguageCode codeList="http://www.loc.gov/standards/iso639-2/" codeListValue="' + codelists['LanguageCode'][Data_Language] + '">' + codelists['LanguageCode'][Data_Language] + '</gmd:LanguageCode>\n'
                str19139 += u'</gmd:language>\n'
        if Error_DataLanguage: Error += u'Data_Language: une langue pour les données doit être renseignée.\n'

        # Data_CharacterSet
        e, Data_CharacterSet = _get_xls_value('data_characterset', lst_name, sh, 'string')
        if Data_CharacterSet: Data_CharacterSet = Data_CharacterSet.split()[0]
        if Data_CharacterSet not in codelists['CharacterSetCode']:
            Data_CharacterSet = '4' # Valeur par defaut: "utf8"
        else :
            str19139 += u'<gmd:characterSet><gmd:MD_CharacterSetCode codeList="http://www.isotc211.org/2005/resources/codeList.xml#MD_CharacterSetCode" codeListValue="' + codelists['CharacterSetCode'][Data_CharacterSet] + '">' + codelists['CharacterSetCode'][Data_CharacterSet] + '</gmd:MD_CharacterSetCode></gmd:characterSet>\n'

        # Data_TopicCategory
        Error_TopicCategory = 1
        for i in range(1, 20):
            e, Data_TopicCategory = _get_xls_value('data_topiccategory'+str(i), lst_name, sh, 'string')
            if Data_TopicCategory: Data_TopicCategory = Data_TopicCategory.split()[0]
            if Data_TopicCategory and Data_TopicCategory in codelists['TopicCategoryCode']:
                Error_TopicCategory = 0
                str19139 += u'<gmd:topicCategory><gmd:MD_TopicCategoryCode>' + codelists['TopicCategoryCode'][Data_TopicCategory] + '</gmd:MD_TopicCategoryCode></gmd:topicCategory>\n'
        if Error_TopicCategory: Error += u'Data_TopicCategory: un thème ISO pour les données doit être renseigné.\n'
        
        ### Data_Extent
        # Data_GeographicExtent
        Error_DataGeographicExtent = 1
        for i in range(1, 20):
            e, Data_ExtentName = _get_xls_value('data_ext'+str(i)+'_name', lst_name, sh, 'string')
            Data_ExtentName = _encodexml(Data_ExtentName)
            e, Data_ExtentNorthbound = _get_xls_value('data_ext'+str(i)+'_n', lst_name, sh, 'string')
            e, Data_ExtentSouthbound = _get_xls_value('data_ext'+str(i)+'_s', lst_name, sh, 'string')
            e, Data_ExtentEastbound = _get_xls_value('data_ext'+str(i)+'_e', lst_name, sh, 'string')
            e, Data_ExtentWestbound = _get_xls_value('data_ext'+str(i)+'_w', lst_name, sh, 'string')
            
            if Data_ExtentNorthbound and Data_ExtentSouthbound and Data_ExtentEastbound and Data_ExtentWestbound:
                Error_DataGeographicExtent = 0
                str19139 += u'<gmd:extent><gmd:EX_Extent>\n'
                str19139 += u'<gmd:description><gco:CharacterString>' + Data_ExtentName + '</gco:CharacterString></gmd:description>\n'
                str19139 += u'<gmd:geographicElement><gmd:EX_GeographicBoundingBox>\n'
                str19139 += u'<gmd:westBoundLongitude><gco:Decimal>' + Data_ExtentWestbound + '</gco:Decimal></gmd:westBoundLongitude>\n'
                str19139 += u'<gmd:eastBoundLongitude><gco:Decimal>' + Data_ExtentEastbound + '</gco:Decimal></gmd:eastBoundLongitude>\n'
                str19139 += u'<gmd:southBoundLatitude><gco:Decimal>' + Data_ExtentSouthbound + '</gco:Decimal></gmd:southBoundLatitude>\n'
                str19139 += u'<gmd:northBoundLatitude><gco:Decimal>' + Data_ExtentNorthbound + '</gco:Decimal></gmd:northBoundLatitude>\n'
                str19139 += u'</gmd:EX_GeographicBoundingBox></gmd:geographicElement>\n'
                #str19139 += u'<gmd:geographicElement><gmd:EX_GeographicDescription>\n'
                #str19139 += u'<extentTypeCode><gmd:Boolean>1</gmd:Boolean></extentTypeCode>\n'
                #str19139 += u'<geographicIdentifier><gmd:MD_Identifier>\n'
                #str19139 += u'<code><gco:CharacterString>' + Data_ExtentName + '</gco:CharacterString></code>\n'
                #str19139 += u'</gmd:MD_Identifier></geographicIdentifier>\n'
                #str19139 += u'</gmd:EX_GeographicDescription></gmd:geographicElement>\n'
                str19139 += u'</gmd:EX_Extent></gmd:extent>\n'
        if Error_DataGeographicExtent: Error += u'Data_GeographicExtent: une emprise géographique pour les données doit être renseignée.\n'

        # Data_TemporalExtent
        for i in range(1, 20):
            e, Data_TemporalExtent_Start = _get_xls_value('data_temporalextent'+str(i)+'_start', lst_name, sh, 'date')
            e, Data_TemporalExtent_End = _get_xls_value('data_temporalextent'+str(i)+'_end', lst_name, sh, 'date')
            e, Data_ExtentName = _get_xls_value('data_temporalextent'+str(i)+'_description', lst_name, sh, 'string')
            Data_ExtentName = _encodexml(Data_ExtentName)

            if Data_TemporalExtent_Start and Data_TemporalExtent_End :
                str19139 += u'<gmd:extent><gmd:EX_Extent>\n'
                str19139 += u'<gmd:description><gco:CharacterString>' + Data_ExtentName + '</gco:CharacterString></gmd:description>\n'
                str19139 += u'<gmd:temporalElement><gmd:EX_TemporalExtent>\n'
                str19139 += u'<gmd:extent><gml:TimePeriod xsi:type="gml:TimePeriodType" gml:id="TemporalId_' + str(i) + '">\n'
                str19139 += u'<gml:beginPosition>' + Data_TemporalExtent_Start + '</gml:beginPosition>\n'
                str19139 += u'<gml:endPosition>' + Data_TemporalExtent_End + '</gml:endPosition>\n'
                str19139 += u'</gml:TimePeriod></gmd:extent>\n'
                str19139 += u'</gmd:EX_TemporalExtent></gmd:temporalElement>\n'
                str19139 += u'</gmd:EX_Extent></gmd:extent>\n'

        """
        # Data_VerticalExtent
        for i in range(1, 20):
            e, Data_VerticalExtent_Min = _get_xls_value('data_verticalextent'+str(i)+'_min', lst_name, sh, 'string')
            e, Data_VerticalExtent_Max = _get_xls_value('data_verticalextent'+str(i)+'_max', lst_name, sh, 'string')
            e, Data_VerticalExtent_Unit = _get_xls_value('data_verticalextent'+str(i)+'_unit', lst_name, sh, 'string')
            e, Data_VerticalExtent_Ref = _get_xls_value('data_verticalextent'+str(i)+'_ref', lst_name, sh, 'string')
 
            if Data_VerticalExtent_Min and Data_VerticalExtent_Max and Data_VerticalExtent_Unit and Data_VerticalExtent_Ref:
                str19139 += u'<gmd:extent><gmd:EX_Extent>\n'
                str19139 += u'<gmd:verticalElement><gmd:EX_VerticalExtent>\n'
                str19139 += u'<gmd:minValue><gco:CharacterString>' + Data_VerticalExtent_Min + '</gco:CharacterString></gmd:minValue>\n'
                str19139 += u'<gmd:maxValue><gco:CharacterString>' + Data_VerticalExtent_Max + '</gco:CharacterString></gmd:maxValue>\n'
                str19139 += u'<gmd:uom><gco:CharacterString>' + Data_VerticalExtent_Unit + '</gco:CharacterString></gmd:uom>\n'
                str19139 += u'<gmd:verticalDatum><gco:CharacterString>' + Data_VerticalExtent_Ref + '</gco:CharacterString></gmd:verticalDatum>\n'
                str19139 += u'</gmd:EX_VerticalExtent></gmd:verticalElement>\n'
                str19139 += u'</gmd:EX_Extent></gmd:extent>\n'
        """
        
        str19139 += u'</gmd:MD_DataIdentification></gmd:identificationInfo>\n'

        ### DISTRIBUTION INFO
        str19139 += u'<gmd:distributionInfo><gmd:MD_Distribution>\n'

        # Data_DistFormat
        for i in range(1, 20):
            e, Data_DistFormatName = _get_xls_value('data_distformat'+str(i)+'_name', lst_name, sh, 'string')
            Data_DistFormatName = _encodexml(Data_DistFormatName)
            e, Data_DistFormatVersion = _get_xls_value('data_distformat'+str(i)+'_version', lst_name, sh, 'string')
            Data_DistFormatVersion = _encodexml(Data_DistFormatVersion)
            e, Data_DistFormatSpecification = _get_xls_value('data_distformat'+str(i)+'_specification', lst_name, sh, 'string')
            Data_DistFormatSpecification = _encodexml(Data_DistFormatSpecification)
   
            if Data_DistFormatName:
                str19139 += u'<gmd:distributionFormat><gmd:MD_Format>\n'
                str19139 += u'<gmd:name><gco:CharacterString>' + Data_DistFormatName + '</gco:CharacterString></gmd:name>\n'
                str19139 += u'<gmd:version><gco:CharacterString>' + Data_DistFormatVersion + '</gco:CharacterString></gmd:version>\n'
                str19139 += u'<gmd:specification><gco:CharacterString>' + Data_DistFormatSpecification + '</gco:CharacterString></gmd:specification>\n'
                str19139 += u'</gmd:MD_Format></gmd:distributionFormat>\n'

        str19139 += u'<gmd:transferOptions><gmd:MD_DigitalTransferOptions>\n'
        
        # Data_Linkage (url)
        for i in range(1, 20):
            e, Data_LinkageName = _get_xls_value('data_linkage'+str(i)+'_name', lst_name, sh, 'string')
            Data_LinkageName = _encodexml(Data_LinkageName)
            e, Data_LinkageDescription = _get_xls_value('data_linkage'+str(i)+'_description', lst_name, sh, 'string')
            Data_LinkageDescription = _encodexml(Data_LinkageDescription)
            e, Data_LinkageURL = _get_xls_value('data_linkage'+str(i)+'_url', lst_name, sh, 'string')
            Data_LinkageURL = _encodexml(Data_LinkageURL)
            e, Data_LinkageProtocol = _get_xls_value('data_linkage'+str(i)+'_protocol', lst_name, sh, 'string')
            Data_LinkageProtocol = _encodexml(Data_LinkageProtocol)

            linkageName = '<gco:CharacterString>' + Data_LinkageName + '</gco:CharacterString>'
            if Data_LinkageProtocol in ("MAP:PDF", "MAP:JPEG", "MAP:JPG", "MAP:PNG", "DATA:ZIP"):
                if Data_LinkageProtocol == "MAP:PDF": linkageName = '<gmx:MimeFileType xmlns:gmx="http://www.isotc211.org/2005/gmx"type="application/pdf">'+Data_LinkageName+'</gmx:MimeFileType>'
                if Data_LinkageProtocol == "MAP:JPEG": linkageName = '<gmx:MimeFileType xmlns:gmx="http://www.isotc211.org/2005/gmx" type="image/jpeg">'+Data_LinkageName+'</gmx:MimeFileType>'
                if Data_LinkageProtocol == "MAP:JPG": linkageName = '<gmx:MimeFileType xmlns:gmx="http://www.isotc211.org/2005/gmx" type="image/jpg">'+Data_LinkageName+'</gmx:MimeFileType>'
                if Data_LinkageProtocol == "MAP:PNG": linkageName = '<gmx:MimeFileType xmlns:gmx="http://www.isotc211.org/2005/gmx" type="image/png">'+Data_LinkageName+'</gmx:MimeFileType>'
                if Data_LinkageProtocol == "DATA:ZIP": linkageName = '<gmx:MimeFileType xmlns:gmx="http://www.isotc211.org/2005/gmx" type="application/zip">'+Data_LinkageName+'</gmx:MimeFileType>'
                Data_LinkageProtocol = "WWW:DOWNLOAD-1.0-http--download"
            if Data_LinkageURL:
                str19139 += u'<gmd:onLine><gmd:CI_OnlineResource>\n'
                str19139 += u'<gmd:linkage><gmd:URL>' + Data_LinkageURL + '</gmd:URL></gmd:linkage>\n'
                if Data_LinkageProtocol:
                    str19139 += u'<gmd:protocol><gco:CharacterString>' + Data_LinkageProtocol + '</gco:CharacterString></gmd:protocol>\n'
                # str19139 += u'<gmd:name><gco:CharacterString>' + Data_LinkageName + '</gco:CharacterString></gmd:name>\n'
                str19139 += u'<gmd:name>' + linkageName + '</gmd:name>\n'
                str19139 += u'<gmd:description><gco:CharacterString>' + Data_LinkageDescription + '</gco:CharacterString></gmd:description>\n'
                str19139 += u'</gmd:CI_OnlineResource></gmd:onLine>\n'

        str19139 += u'</gmd:MD_DigitalTransferOptions></gmd:transferOptions>\n'
        str19139 += u'</gmd:MD_Distribution></gmd:distributionInfo>\n'

        ### DATA QUALITY INFO
        str19139 += u'<gmd:dataQualityInfo><gmd:DQ_DataQuality>\n'

        # DQ_Level
        e, Data_DQ_Level = _get_xls_value('data_dq_level', lst_name, sh, 'string')
        if Data_DQ_Level: Data_DQ_Level = Data_DQ_Level.split()[0]
        
        if not Data_DQ_Level:
            Data_DQ_Level = MD_HierarchyLevel
        
        if Data_DQ_Level and Data_DQ_Level in codelists['ScopeCode']:
             str19139 += u'<gmd:scope><gmd:DQ_Scope>\n'
             str19139 += u'<gmd:level><gmd:MD_ScopeCode codeListValue="' + codelists['ScopeCode'][Data_DQ_Level] + '" codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_ScopeCode">' + codelists['ScopeCode'][Data_DQ_Level] + '</gmd:MD_ScopeCode></gmd:level>\n'
             str19139 += u'</gmd:DQ_Scope></gmd:scope>\n'

        # DQ_InspireConformity
        Error_DQInspireConformity = 1
        for i in range(1, 20):
            e, Data_DQ_InspireConformityId = _get_xls_value('data_dq_inspireconformity'+str(i)+'_id', lst_name, sh, 'integer')
            e, Data_DQ_InspireConformityTest = _get_xls_value('data_dq_inspireconformity'+str(i)+'_specification', lst_name, sh, 'string')
            if Data_DQ_InspireConformityTest: Data_DQ_InspireConformityTest = Data_DQ_InspireConformityTest.split()[0]
            e, Data_DQ_InspireConformityDateCreation = _get_xls_value('data_dq_inspireconformity'+str(i)+'_datecreation', lst_name, sh, 'date')
            e, Data_DQ_InspireConformityDatePublication = _get_xls_value('data_dq_inspireconformity'+str(i)+'_datepublication', lst_name, sh, 'date')
            e, Data_DQ_InspireConformityDateRevision = _get_xls_value('data_dq_inspireconformity'+str(i)+'_daterevision', lst_name, sh, 'date')
            e, Data_DQ_InspireConformityResult = _get_xls_value('data_dq_inspireconformity'+str(i)+'_explain', lst_name, sh, 'string')
            Data_DQ_InspireConformityResult = _encodexml(Data_DQ_InspireConformityResult)
            e, Data_DQ_InspireConformityPass = _get_xls_value('data_dq_inspireconformity'+str(i)+'_pass', lst_name, sh, 'string')
            if Data_DQ_InspireConformityPass: Data_DQ_InspireConformityPass = Data_DQ_InspireConformityPass.split()[0]
            
            if Data_DQ_InspireConformityTest and Data_DQ_InspireConformityTest in codelists['InspireSpecificationCode'] and Data_DQ_InspireConformityPass in [1, 2]:
                Error_DQInspireConformity = 0
                str19139 += u'<gmd:report><gmd:DQ_DomainConsistency xsi:type="gmd:DQ_DomainConsistency_Type">\n'
                str19139 += u'<gmd:measureIdentification>\n'
                str19139 += u'<gmd:RS_Identifier>\n'
                str19139 += u'<gmd:code>\n'
                str19139 += u'<gco:CharacterString>InspireConformity_' + str(i) + '</gco:CharacterString>\n'
                str19139 += u'</gmd:code>\n'
                str19139 += u'<gmd:codeSpace>\n'
                str19139 += u'<gco:CharacterString>INSPIRE Conformity</gco:CharacterString>\n'
                str19139 += u'</gmd:codeSpace>\n'
                str19139 += u'</gmd:RS_Identifier>\n'
                str19139 += u'</gmd:measureIdentification>\n'
                str19139 += u'<gmd:result><gmd:DQ_ConformanceResult>\n'
                str19139 += u'<gmd:specification><gmd:CI_Citation>\n'
                str19139 += u'<gmd:title><gco:CharacterString>' + codelists['InspireSpecificationCode'][Data_DQ_InspireConformityTest] + '</gco:CharacterString></gmd:title>\n'
                if Data_DQ_InspireConformityDateCreation or Data_DQ_InspireConformityDatePublication or Data_DQ_InspireConformityDateRevision :
                    if Data_DQ_InspireConformityDateCreation:
                        str19139 += u'<gmd:date><gmd:CI_Date>\n'
                        str19139 += u'<gmd:date><gco:Date>' + Data_DQ_InspireConformityDateCreation + '</gco:Date></gmd:date>\n'
                        str19139 += u'<gmd:dateType><gmd:CI_DateTypeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode" codeListValue="creation">creation</gmd:CI_DateTypeCode></gmd:dateType>\n'
                        str19139 += u'</gmd:CI_Date></gmd:date>\n'
                    if Data_DQ_InspireConformityDatePublication:
                        str19139 += u'<gmd:date><gmd:CI_Date>\n'
                        str19139 += u'<gmd:date><gco:Date>' + Data_DQ_InspireConformityDatePublication + '</gco:Date></gmd:date>\n'
                        str19139 += u'<gmd:dateType><gmd:CI_DateTypeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode" codeListValue="publication">publication</gmd:CI_DateTypeCode></gmd:dateType>\n'
                        str19139 += u'</gmd:CI_Date></gmd:date>\n'
                    if Data_DQ_InspireConformityDateRevision:
                        str19139 += u'<gmd:date><gmd:CI_Date>\n'
                        str19139 += u'<gmd:date><gco:Date>' + Data_DQ_InspireConformityDateRevision + '</gco:Date></gmd:date>\n'
                        str19139 += u'<gmd:dateType><gmd:CI_DateTypeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode" codeListValue="revision">revision</gmd:CI_DateTypeCode></gmd:dateType>\n'
                        str19139 += u'</gmd:CI_Date></gmd:date>\n'
                else:
                    Error += u'DQ_InspireConformity: une date doit être renseigné pour les tests de conformité INSPIRE.\n'

                str19139 += u'</gmd:CI_Citation></gmd:specification>\n'

                if Data_DQ_InspireConformityResult:
                    str19139 += u'<gmd:explanation><gco:CharacterString>' + Data_DQ_InspireConformityResult + '</gco:CharacterString></gmd:explanation>\n'

                if Data_DQ_InspireConformityPass == "1":
                    str19139 += u'<gmd:pass><gco:Boolean>true</gco:Boolean></gmd:pass>\n'
                elif Data_DQ_InspireConformityPass == "2":
                    str19139 += u'<gmd:pass><gco:Boolean>false</gco:Boolean></gmd:pass>\n'

                str19139 += u'</gmd:DQ_ConformanceResult></gmd:result>\n'
                str19139 += u'</gmd:DQ_DomainConsistency></gmd:report>\n'

        # DQ_Conformity
        Error_DQConformity = 1
        for i in range(1, 20):
            e, Data_DQ_ConformityTest = _get_xls_value('data_dq_conformity'+str(i)+'_specification', lst_name, sh, 'string')
            Data_DQ_ConformityTest = _encodexml(Data_DQ_ConformityTest)
            e, Data_DQ_ConformityDateCreation = _get_xls_value('data_dq_conformity'+str(i)+'_datecreation', lst_name, sh, 'date')
            e, Data_DQ_ConformityDatePublication = _get_xls_value('data_dq_conformity'+str(i)+'_datepublication', lst_name, sh, 'date')
            e, Data_DQ_ConformityDateRevision = _get_xls_value('data_dq_conformity'+str(i)+'_daterevision', lst_name, sh, 'date')
            e, Data_DQ_ConformityResult = _get_xls_value('data_dq_conformity'+str(i)+'_explain', lst_name, sh, 'string')
            Data_DQ_ConformityResult = _encodexml(Data_DQ_ConformityResult)
            e, Data_DQ_ConformityPass = _get_xls_value('data_dq_conformity'+str(i)+'_pass', lst_name, sh, 'string')
            
            if Data_DQ_ConformityTest:
                Error_DQInspireConformity = 0
                str19139 += u'<gmd:report><gmd:DQ_DomainConsistency xsi:type="gmd:DQ_DomainConsistency_Type">\n'
                str19139 += u'<gmd:measureIdentification>\n'
                str19139 += u'<gmd:RS_Identifier>\n'
                str19139 += u'<gmd:code>\n'
                str19139 += u'<gco:CharacterString>Conformity_' + str(i) + '</gco:CharacterString>\n'
                str19139 += u'</gmd:code>\n'
                str19139 += u'<gmd:codeSpace>\n'
                str19139 += u'<gco:CharacterString>Other conformity</gco:CharacterString>\n'
                str19139 += u'</gmd:codeSpace>\n'
                str19139 += u'</gmd:RS_Identifier>\n'
                str19139 += u'</gmd:measureIdentification>\n'
                str19139 += u'<gmd:result><gmd:DQ_ConformanceResult>\n'
                str19139 += u'<gmd:specification><gmd:CI_Citation>\n'
                str19139 += u'<gmd:title><gco:CharacterString>' + Data_DQ_ConformityTest + '</gco:CharacterString></gmd:title>\n'
                if Data_DQ_ConformityDateCreation or Data_DQ_ConformityDatePublication or Data_DQ_ConformityDateRevision :
                    if Data_DQ_ConformityDateCreation:
                        str19139 += u'<gmd:date><gmd:CI_Date>\n'
                        str19139 += u'<gmd:date><gco:Date>' + Data_DQ_ConformityDateCreation + '</gco:Date></gmd:date>\n'
                        str19139 += u'<gmd:dateType><gmd:CI_DateTypeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode" codeListValue="creation">creation</gmd:CI_DateTypeCode></gmd:dateType>\n'
                        str19139 += u'</gmd:CI_Date></gmd:date>\n'
                    if Data_DQ_ConformityDatePublication:
                        str19139 += u'<gmd:date><gmd:CI_Date>\n'
                        str19139 += u'<gmd:date><gco:Date>' + Data_DQ_ConformityDatePublication + '</gco:Date></gmd:date>\n'
                        str19139 += u'<gmd:dateType><gmd:CI_DateTypeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode" codeListValue="publication">publication</gmd:CI_DateTypeCode></gmd:dateType>\n'
                        str19139 += u'</gmd:CI_Date></gmd:date>\n'
                    if Data_DQ_ConformityDateRevision:
                        str19139 += u'<gmd:date><gmd:CI_Date>\n'
                        str19139 += u'<gmd:date><gco:Date>' + Data_DQ_ConformityDateRevision + '</gco:Date></gmd:date>\n'
                        str19139 += u'<gmd:dateType><gmd:CI_DateTypeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode" codeListValue="revision">revision</gmd:CI_DateTypeCode></gmd:dateType>\n'
                        str19139 += u'</gmd:CI_Date></gmd:date>\n'
                else:
                    Error += u'DQ_InspireConformity: une date doit être renseigné pour les tests de conformité INSPIRE.\n'

                str19139 += u'</gmd:CI_Citation></gmd:specification>\n'

                if Data_DQ_ConformityResult:
                    str19139 += u'<gmd:explanation><gco:CharacterString>' + Data_DQ_ConformityResult + '</gco:CharacterString></gmd:explanation>\n'
                if Data_DQ_ConformityPass == "Conforme":
                    str19139 += u'<gmd:pass><gco:Boolean>true</gco:Boolean></gmd:pass>\n'
                elif Data_DQ_ConformityPass == "Non conforme":
                    str19139 += u'<gmd:pass><gco:Boolean>false</gco:Boolean></gmd:pass>\n'
                else:
                    str19139 += u'<gmd:pass></gmd:pass>\n'

                str19139 += u'</gmd:DQ_ConformanceResult></gmd:result>\n'
                str19139 += u'</gmd:DQ_DomainConsistency></gmd:report>\n'
        
        ### DQ_Lineage
        str19139 += u'<gmd:lineage><gmd:LI_Lineage>\n'

        # LI_Statement
        e, LI_Statement = _get_xls_value('li_statement', lst_name, sh, 'string')
        LI_Statement = _encodexml(LI_Statement)
        if LI_Statement:
            str19139 += u'<gmd:statement><gco:CharacterString>' + LI_Statement + '</gco:CharacterString></gmd:statement>\n'
        else:
            Error += u'LI_Statement: un texte sur la provenance des données doit être renseigné.\n'

        # LI_ProcessStep
        e, LI_ProcessStep = _get_xls_value('li_processstep', lst_name, sh, 'string')
        LI_ProcessStep = _encodexml(LI_ProcessStep)
        if LI_ProcessStep:
            str19139 += u'<gmd:processStep><gmd:LI_ProcessStep>\n'
            str19139 += u'<gmd:description><gco:CharacterString>' + LI_ProcessStep + '</gco:CharacterString></gmd:description>\n'
            str19139 += u'</gmd:LI_ProcessStep></gmd:processStep>\n'

        # LI_Source
        e, LI_Source = _get_xls_value('li_source', lst_name, sh, 'string')
        LI_Source = _encodexml(LI_Source)
        if LI_Source:
            str19139 += u'<gmd:source><gmd:LI_Source>\n'
            str19139 += u'<gmd:description><gco:CharacterString>' + LI_Source + '</gco:CharacterString></gmd:description>\n'
            str19139 += u'</gmd:LI_Source></gmd:source>\n'

        str19139 += u'</gmd:LI_Lineage></gmd:lineage>\n'
        str19139 += u'</gmd:DQ_DataQuality></gmd:dataQualityInfo>\n'

        # Fin du fichier
        str19139 += u'</gmd:MD_Metadata>\n'

        # Définition du nom de fichier XML
        xml_filename = MD_FileIdentifier + '.xml'
        xml_filename = os.path.join(xml_dir, xml_filename)
        
        if not os.path.isfile(xml_filename):             
            xml_file = open(xml_filename, 'w')
            xml_file.write(str19139.encode('utf-8'))
            xml_file.close()
            #Error += u'Le fichier '+xml_filename+' a ete cree avec succes.\n'
            Error_CreateFile = u'Le fichier '+xml_filename+' a ete cree avec succes.\n'
        else:
            Error += u'Le fichier '+xml_filename+' existe deja et ne peut-etre cree.\n'
        
        
        # Définition du nom de fichier de log
        log_filename = MD_FileIdentifier + '_erreur.txt'
        log_filename = os.path.join(xml_dir, log_filename)
        
        if Error != '':
            if os.path.isfile(log_filename):
                os.remove(log_filename)
            log_file = open(log_filename, 'w')
            log_file.write(Error.encode('utf-8'))
            log_file.close()
            print u'Le fichier '+log_filename+' a ete cree.\n'
        else:
            print u'Aucune erreur identifiée.\n'
        
        return Error.encode('utf-8') + Error_CreateFile.encode('utf-8')


# ------------------------------------------------------------------------------
# _encodexml
# ------------------------------------------------------------------------------
SPECIAL_CHARACTERS = {'"': '&quot;', '&': '&amp;', "'": '&apos;', '<': '&lt;', '>': '&gt;'}
def _encodexml(value):
    # value = value.decode('utf-8')    # ou l'encoding qui va bien
    result = '';
    if value:
        for c in value:
            if c in SPECIAL_CHARACTERS:
                result += SPECIAL_CHARACTERS[c]
            else:
                result += c
    return result

# ------------------------------------------------------------------------------
# _get_value
# ------------------------------------------------------------------------------
def _get_xls_value(cell = '', lst_name = {}, sh = {}, type = 'string'):
    global XY
    error = 1
    clean = ''
    result = ''

    if cell and cell in lst_name:
        try:
            value = lst_name[cell][0].cell().value
        except:
            error = u'Erreur lors de la lecture de la cellule (' + cell + ')'
            value = ''
    elif cell and cell in cellname and XY:
        try:
            value = sh[cellname[cell][0]].cell(cellname[cell][1], cellname[cell][2]).value
        except:
            error = u'Erreur lors de la lecture de la cellule (' + cell + ')'
            value = ''
    else:
        error = u'Erreur lors de la lecture de la cellule (' + cell + ')'
        value = ''

    # Traiter les valeurs nulles
    if value == '':
        error = 0
        result = ''
    else:
        if type == 'string':
            error = 0
            result = unicode(value)
        elif type == 'integer':
            try: 
                error = 0
                result = int(value)
            except: 
                error = u'La valeur transmise n\'est pas un entier'
                result = ''
        elif type == 'date':
            try: 
                error = 0
                result = datetime.datetime(*xlrd.xldate_as_tuple(value, 0))
                result = str(result)[:10]
            except: 
                error = u'La valeur transmise n\'est pas une date'
                result = ''
        else:
            error = u'Le type indiqué n\'existe pas (' + type + ')'
            result = ''

    if result != '' : result = unicode(result)

    # Transmettre le résultat
    return error, result

# ------------------------------------------------------------------------------
# CONVERT_XML2XLS
#
# Fonction de conversion d'un fichier XML vers MS Excel
# ------------------------------------------------------------------------------
def convert_xml2xls(xml_file, xls_dir):       
    print 'convert_xml2xls' 


# Fonction "main"
def main():
    ''' Fonction princpal du programme '''
    xls_file = ''
    xml_dir = ''

    # error = xls_file.xls2xml(XML_DIR)
    try:
        error = xls2xml(xls_file, xml_dir)
    except:
        error = u'Erreur de transformation.'
    
    if error:
        print '\n=> ERREUR pour le fichier :', xls_file
        print error
    else:
        print '\n=> OK pour le fichier', xls_file, 'converti en XML.'


if __name__ == '__main__':
    main()
