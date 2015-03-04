<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
    xmlns:gmd='http://www.isotc211.org/2005/gmd'
	xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
	xmlns:fra='http://www.cnig.gouv.fr/2005/fra'
	xmlns:gco='http://www.isotc211.org/2005/gco'
	xmlns:gts='http://www.isotc211.org/2005/gts'
	xmlns:gml='http://www.opengis.net/gml'
	xmlns:gfc='http://www.isotc211.org/2005/gfc'
	xmlns:gmx='http://www.isotc211.org/2005/gmx'
	xmlns:xlink='http://www.w3.org/1999/xlink'
	xmlns:gmi='http://www.isotc211.org/2005/gmi'
    
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:root='http://cigal.geotask.ch/root'
	xmlns:smXML='http://cigal.geotask.ch/smXML' 
	xmlns:scXML='http://cigal.geotask.ch/scXML' 
	xmlns:iso19110='http://cigal.geotask.ch/iso19110'
    
    xmlns:map="urn:cigal:mapping">
    
    <xsl:output method="html" encoding='utf-8' indent='yes'/>

    <xsl:variable name="fileMapping" select="document('./XSL_CIGAL-ISO19139_view.xsl')"/>
   
    <map:Mapping xmlns:map="urn:cigal:mapping">
        <map:dateTypeCode>
            <map:code iso="creation" code="création" />
            <map:code iso="publication" code="publication" />
            <map:code iso="revision" code="révision" />
        </map:dateTypeCode>
        <map:scopeCode>
            <map:code iso="attribute" code="Attribut" />
            <map:code iso="attributeType" code="Type d’attribut" />
            <map:code iso="collectionHardware" code="Collection matérielle" />
            <map:code iso="collectionSession" code="Collection de session" />
            <map:code iso="dataset" code="Jeu de données" />
            <map:code iso="series" code="Collection de données" />
            <map:code iso="nonGeographicDataset" code="Jeu de données non géographique" />
            <map:code iso="dimensionGroup" code="Dimension d’un groupe" />
            <map:code iso="feature" code="Entité" />
            <map:code iso="featureType" code="Type d’entité" />
            <map:code iso="propertyType" code="Type de propriété" />
            <map:code iso="software" code="Logiciel" />
            <map:code iso="fieldSession" code="Champ de Session" />
            <map:code iso="service" code="Service" />
            <map:code iso="model" code="Modèle" />
            <map:code iso="tile" code="Sous-ensemble de données" />
            <map:code iso="fieldCampaign" code="Campagne de mesures" />
        </map:scopeCode>
        <map:languageCode>
            <map:code iso="fre" code="Français" />
            <map:code iso="fr" code="Français" />
            <map:code iso="fra" code="Français" />
            <map:code iso="en" code="Anglais" />
            <map:code iso="eng" code="Anglais" />
            <map:code iso="de" code="Allemand" />
            <map:code iso="deu" code="Allemand" />
            <map:code iso="it" code="Italien" />
            <map:code iso="ita" code="Italien" />
            <map:code iso="es" code="Espagnole" />
            <map:code iso="esp" code="Espagnole" />
        </map:languageCode>
        <map:topicCategory>
            <map:code iso="biota" code="Biologie" />
            <map:code iso="boundaries" code="Frontières et limites" />
            <map:code iso="climatologyMeteorologyAtmosphere" code="Climatologie et météorologie" />
            <map:code iso="economy" code="Economie" />
            <map:code iso="elevation" code="Elevation et altimetrie" />
            <map:code iso="environnement" code="Environnement" />
            <map:code iso="farming" code="Agriculture" />
            <map:code iso="geoscientificInformation" code="Science de la terre" />
            <map:code iso="health" code="Santé" />
            <map:code iso="imageryBaseMapsEarthCover" code="Cartes et données de référence" />
            <map:code iso="inlandWaters" code="Hydrologie" />
            <map:code iso="intelligenceMilitary" code="Activites militaires" />
            <map:code iso="location" code="Localisants" />
            <map:code iso="oceans" code="Oceanologie et oceanographie" />
            <map:code iso="planningCadastre" code="Cadastre, pannification et amenagement" />
            <map:code iso="society" code="Societé" />
            <map:code iso="structure" code="Contructions et équipements" />
            <map:code iso="transportation" code="Infrastructure de transport" />
            <map:code iso="utilitiesCommunication" code="Réseaux (eau, energie, etc.)" />
        </map:topicCategory>
        <map:restrictionCode>
            <map:code iso="copyright" code="Droit d’auteur / Droit moral (copyright)" />
            <map:code iso="patent" code="Brevet" />
            <map:code iso="patentPending" code="Brevet en instance" />
            <map:code iso="trademark" code="Marque déposée" />
            <map:code iso="license" code="Licence" />
            <map:code iso="intellectualPropertyRights" code="Droit de propriété intellectuelle / Droit patrimonial" />
            <map:code iso="restricted" code="Restreint" />
            <map:code iso="otherRestrictions" code="Autres restrictions" />
        </map:restrictionCode>
        <map:classificationCode>
            <map:code iso="unclassified" code="Non classifié" />
            <map:code iso="restricted" code="Restreint" />
            <map:code iso="confidential" code="Confidentiel" />
            <map:code iso="secret" code="Secret" />
            <map:code iso="topSecret" code="Top secret" />
        </map:classificationCode>
        <map:spatialRepresentationTypeCode>
            <map:code iso="vector" code="Vecteur" />
            <map:code iso="grid" code="Raster" />
            <map:code iso="textTable" code="Table texte" />
            <map:code iso="tin" code="Tin" />
            <map:code iso="stereoModel" code="Vue 3D" />
            <map:code iso="video" code="Vidéo" />
        </map:spatialRepresentationTypeCode>
        <map:roleCode>
            <map:code iso="ressourceProvider" code="Fournisseur" />
            <map:code iso="custodian" code="Gestionnaire" />
            <map:code iso="owner" code="Propriétaire" />
            <map:code iso="user" code="Utilisateur" />
            <map:code iso="distributor" code="Distributeur" />
            <map:code iso="originator" code="Commanditaire" />
            <map:code iso="pointOfContact" code="Point de contact" />
            <map:code iso="principalInvestigator" code="Producteur / Maître d’œuvre principal ou d'ensemble" />
            <map:code iso="processor" code="Intégrateur / Exécutant secondaire" />
            <map:code iso="publisher" code="Editeur" />
            <map:code iso="author" code="Auteur" />
        </map:roleCode>
    </map:Mapping>
   
   
    <xsl:template match='/'>
    
    <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <!-- Encodage du site -->
            <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
            
            <!-- Titre du site -->
            <title>Fiche de métadonnées</title>
            
            <!-- Meta-tags du site -->
            <meta name="keywords" content="" />

            <meta name="description" content="" />
            <meta name="author" content="" />
            
            <!-- Icones du site -->
            <link rel="shortcut icon" href="" />
            <link rel="icon" href="" type="image/x-icon" />
        
            <!-- CSS du site -->
                    <!-- css de jquery-ui -->

            <link type="text/css" href="css/green2/jquery-ui-1.8.4.custom.css" rel="Stylesheet" />
            <link type="text/css" href="css/green2/jquery-datatable.css" rel="Stylesheet" />

            <link type="text/css" href="css/green2/index.css" rel="Stylesheet" />

            <!-- Chargement des fichiers css spécifiques envoyés par le controller -->
            
            <!-- Javascript -->
            <!--
            <script type="text/javascript" src="http://metadata.cigalsace.org/js/jquery-1.4.2.min.js"></script>
            <script type="text/javascript" src="http://metadata.cigalsace.org/js/jquery-ui-1.8.4.custom.min.js"></script>
            -->
                                
            <!-- Définition du domaine (hote) -->

                    
        </head>
        <body>

    
            <style type="text/css" media="all" >
                body {text-align: center}
                #page {width: 780px; text-align: center; margin: auto; font: normal 10px verdana, arial, sans-serif; color:#000; vertical-align: top; clear: both; }
                #page .type {float: right; font: bold 0.9em verdana, arial, sans-serif; margin: 0 0 10px 0; padding: 2px; }
                #page .t {font: bold 2em verdana, arial, sans-serif; text-align:center; line-height:1.8em; border: 1px solid #000000;}
                #page .t1 {font: bold 1.5em verdana, arial, sans-serif; text-align:center; line-height:1.8em; }
                #page .t2, .t2_carte {font: bold 1.3em verdana, arial, sans-serif; text-align:center; line-height:1.5em; margin: 25px 5px 10px 5px; padding:5px; text-transform : uppercase; border: 1px solid #000000;}
                #page .t2_carte {}
                #page table {background:#fff; border: 1px solid #000; font:10px verdana, arial, sans-serif; margin-bottom: 5px; width: 100%;}
                #page td {border: 1px solid #ccc; padding: 5px; text-align: left; color: #000;}
                #page .partie {font-weight: bold; text-transform : uppercase; border: 0px solid #000000; }
                #page .td1 {width: 130px;}
                #page .titre {font-weight: bold; text-align: center;}
                #page .td2 { text-align: justify;}
                #page th { padding: 5px; border: 1px solid #ccc; color: #000; }
                #page .tb_cnt {background:#fff; border: 1px solid #ccc; font:10px verdana, arial, sans-serif; border-collapse:collapse; margin: 5px; width: 98%;}
                #page .td1_cnt {width: 400px; border: 1px solid #ccc; color: #000; }
                #page .td2_cnt {width: 200px;; border: 1px solid #ccc; color: #000; }
                
                #page .note {font-size: 0.7em; font-style: italic; text-align: right; margin-bottom: 30px;}
                
                #page .bt_goback {padding: 2px; margin: 5px; text-align: center; text-decoration: none; width: 100px;font-size: 1.2em; cursor: pointer;}
                
                #page tr:hover, #page td:hover, #page tr, #page td { background-color: #fff; }
                
            </style>
            
            <style type="text/css" media="print" >
                #page {width: 100%; text-align: center; }
                #header, #menu, #footer { display: none; }
                body { overflow: visible; }
            </style>


            <div id="page" class="">
                <xsl:apply-templates/>
            </div>
        
        	</body>
        </html>

    </xsl:template >

    <xsl:template match="/gmd:MD_Metadata" >
        <br />
        <xsl:choose>
            <xsl:when test="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:keyword/gco:CharacterString = 'CARTE'">
                <div class="t2_carte ui-widget-header ui-corner-all"><xsl:value-of select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString"/> </div>
                <div class="type ui-state-default ui-corner-all"> - CARTE - </div> <br />
            </xsl:when>
            <xsl:otherwise>
                <div class="t2 ui-widget-header ui-corner-all"><xsl:value-of select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString"/> </div>
                <div class="type ui-state-default ui-corner-all"> - DONNEES - </div> <br />
            </xsl:otherwise>
        </xsl:choose>

        <table class="ui-state-default ui-corner-all">
            <tr>
                <th colspan="2" class="partie ui-widget-header ui-corner-all">Information sur les métadonnées</th>
            </tr>
            <tr>
                <td class="td1">Identifiant de la fiche:</td>
                <td class="titre td2"> 
                    <xsl:choose>
                        <xsl:when test="gmd:fileIdentifier/gco:CharacterString">
                            <xsl:value-of select="gmd:fileIdentifier/gco:CharacterString"/>
                        </xsl:when>
                        <xsl:otherwise>
                            Non renseigné
                        </xsl:otherwise>
                    </xsl:choose>
                </td>      
            </tr>
            <tr>
                <td class="td1">Langue de la fiche:</td>
                <td class="td2"> 
                    <xsl:choose>
                        <xsl:when test="gmd:language/gmd:languageCode">
                            <xsl:call-template name="languageCode">
                                <xsl:with-param name="val" select="gmd:language/gmd:languageCode/@codeListValue"/>
                            </xsl:call-template>
                        </xsl:when>
                        <xsl:otherwise>
                            Non renseigné
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>
            <tr>
                <td class="td1">Date d'édition de la fiche:</td>
                <td class="td2"> 
                    <xsl:choose>
                        <xsl:when test="gmd:dateStamp/gco:Date">
                            <xsl:value-of select="gmd:dateStamp/gco:Date"/>
                        </xsl:when>
                        <xsl:otherwise>
                            Non renseigné
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>
            <tr>
                <td class="td1">Jeu de charactères:</td>
                <td class="td2"> 
                    <xsl:choose>
                        <xsl:when test="gmd:characterSet/gmd:characterSetCode">
                            <xsl:value-of select="gmd:characterSet/gmd:characterSetCode"/>
                        </xsl:when>
                        <xsl:otherwise>
                            Non renseigné
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>
            <tr>
                <td class="td1">Type de ressource:</td>
                <td class="td2"> 
                    <xsl:choose>
                        <xsl:when test="gmd:hierarchyLevel/gmd:MD_ScopeCode">
                            <xsl:call-template name="scopeCode">
                                <xsl:with-param name="val" select="gmd:hierarchyLevel/gmd:MD_ScopeCode/@codeListValue"/>
                            </xsl:call-template>
                        </xsl:when>
                        <xsl:otherwise>
                            Non renseigné
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>
            <tr>
                <td class="td1">Standard/version des métadonnées:</td>
                <td class="td2"> 
                    <xsl:choose>
                        <xsl:when test="gmd:metadataStandardName/gco:CharacterString">
                            <xsl:value-of select="gmd:metadataStandardName/gco:CharacterString"/> - 
                            <xsl:value-of select="gmd:metadataStandardVersion/gco:CharacterString"/>
                        </xsl:when>
                        <xsl:otherwise>
                            Non renseigné
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>
            <tr>
                <td class="td1">Contact pour les métadonnées:</td>
                <td class="td2">
                    <xsl:if test="gmd:contact">
                        <table class="tb_cnt ui-state-default ui-corner-all">
                            <tr>
                                <th class="titre td1_cnt ui-state-default ui-corner-all">Contact</th>
                                <th class="td2_cnt titre ui-state-default ui-corner-all">Rôle</th>
                            </tr>
                          
                            <xsl:for-each select='gmd:contact'>
                                <tr>
                                    <td class="td1_cnt"> 
                                                
                                        <xsl:if test="gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString">
                                            <xsl:value-of select="gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString"/> <br />
                                        </xsl:if>

                                        <xsl:if test="gmd:CI_ResponsibleParty/gmd:positionName/gco:CharacterString">
                                            <xsl:value-of select="gmd:CI_ResponsibleParty/gmd:positionName/gco:CharacterString"/> <br />
                                        </xsl:if>
                                        
                                        <xsl:if test="gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString">
                                            <xsl:value-of select="gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString"/> <br />
                                        </xsl:if>
                                        
                                        <xsl:if test="gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint">
                                            <xsl:for-each select='gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint'>
                                                <xsl:value-of select="gco:CharacterString"/> <br />
                                            </xsl:for-each>
                                        </xsl:if>
                                        
                                        <xsl:if test="gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString">
                                            <xsl:value-of select="gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString"/>
                                            <xsl:value-of select="gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString"/>
                                            <xsl:value-of select="gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gco:CharacterString"/>
                                            <br />
                                        </xsl:if>
                                
                                        <xsl:if test="gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice">
                                            Tél: 
                                            <xsl:for-each select='gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice'>
                                                <xsl:value-of select="gco:CharacterString"/> -
                                            </xsl:for-each> <br />
                                        </xsl:if>
                                        
                                        <xsl:if test="gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:facsimile">
                                            Fax:
                                            <xsl:for-each select='gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:facsimile'>
                                                <xsl:value-of select="gco:CharacterString"/> -
                                            </xsl:for-each> <br />
                                        </xsl:if>
                                        
                                        <xsl:if test="gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress">
                                            E-mail: 
                                            <xsl:for-each select='gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress'>
                                                <xsl:value-of select="gco:CharacterString"/> -
                                            </xsl:for-each> <br />
                                        </xsl:if>
                                        
                                        <xsl:if test="gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage">
                                            Site Internet: 
                                            <xsl:for-each select='gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage'>
                                                <xsl:value-of select="gmd:URL"/> -
                                            </xsl:for-each> <br />
                                        </xsl:if>
                            
                                    </td>
                            
                                    <td class="td2_cnt">
                                        <xsl:for-each select='gmd:CI_ResponsibleParty/gmd:role'>
                                            <xsl:call-template name="roleCode">
                                                <xsl:with-param name="val" select="gmd:CI_RoleCode/@codeListValue"/>
                                            </xsl:call-template>                       
                                        </xsl:for-each> 
                                    </td>
                                </tr>
                            </xsl:for-each>
                        </table> 
                    </xsl:if>
                </td>
          </tr>

        </table>
        
        <table class="ui-state-default ui-corner-all">
            <tr>
                <th colspan="2" class="partie ui-widget-header ui-corner-all">Identification du lot de données</th>
            </tr>
            <tr>
                <td class="td1">Identifiants de la ressource:</td>
                <td class="td2">
                    <xsl:choose>
                        <xsl:when test="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:identifier/gmd:RS_Identifier/gmd:code/gco:CharacterString">
                            <xsl:for-each select='gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:identifier/gmd:RS_Identifier'>
                                <xsl:value-of select="gmd:code/gco:CharacterString"/> 
                                (<xsl:value-of select="gmd:codeSpace/gco:CharacterString"/>) <br />
                            </xsl:for-each>
                        </xsl:when>
                        <xsl:otherwise>
                            Non renseigné
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>
            <tr>
                <td class="td1">Titre:</td>
                <td class="titre td2"> <xsl:value-of select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString"/> </td>      
            </tr>
            <xsl:for-each select='gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date'>
                <tr>
                    <td class="td1">Dates de 
                        <xsl:call-template name="dateTypeCode">
                            <xsl:with-param name="val" select="gmd:CI_Date/gmd:dateType/gmd:CI_DateTypeCode/@codeListValue"/>
                        </xsl:call-template>:</td>
                    <td class="td2">
                        <xsl:call-template name="date">
                            <xsl:with-param name="ladate" select="gmd:CI_Date/gmd:date/gco:Date"/>
                        </xsl:call-template>
                    </td>
                    <!--<td class="td2"><xsl:value-of select="gmd:CI_Date/date/gco:Date"/></td>-->
                </tr>        
            </xsl:for-each>
            <tr>
                <td class="td1">Résumé:</td>
                <td class="td2"> <xsl:value-of select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString/."/> </td>
            </tr>
            <tr>
                <td class="td1">Thèmes:</td>
                <td class="td2"> 
                    <xsl:for-each select='gmd:identificationInfo/gmd:MD_DataIdentification/gmd:topicCategory'>
                        <xsl:call-template name="topicCategory">
                            <xsl:with-param name="val" select="gmd:MD_TopicCategoryCode"/>
                        </xsl:call-template>
                    </xsl:for-each>
                </td>
            </tr>
            <tr>
                <td class="td1">Mots-clés:</td>
                <td class="td2"> 
                    <xsl:for-each select='gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords'>
                        - <xsl:value-of select="gmd:MD_Keywords/gmd:keyword/gco:CharacterString"/>
                        (<xsl:value-of select="gmd:MD_Keywords/gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString"/>)<br /> 
                    </xsl:for-each>
                </td>
            </tr>
          
            <tr>
                <td class="td1">Contact pour les données:</td>
                <td class="td2">

                    <xsl:if test="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact">
                            
                        <table class="tb_cnt ui-state-default ui-corner-all">
                            <tr>
                                <th class="titre td1_cnt ui-state-default ui-corner-all">Contact</th>
                                <th class="td2_cnt titre ui-state-default ui-corner-all">Rôle</th>
                            </tr>
                        
                            <xsl:for-each select='gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact'>

                                <tr>
                                    <td class="td1_cnt"> 

                                        <xsl:if test="gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString">
                                            <xsl:value-of select="gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString"/> <br />
                                        </xsl:if>

                                        <xsl:if test="gmd:CI_ResponsibleParty/gmd:positionName/gco:CharacterString">
                                            <xsl:value-of select="gmd:CI_ResponsibleParty/gmd:positionName/gco:CharacterString"/> <br />
                                        </xsl:if>
                                        
                                        <xsl:if test="gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString">
                                            <xsl:value-of select="gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString"/> <br />
                                        </xsl:if>
                                        
                                        <xsl:if test="gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint">
                                            <xsl:for-each select='gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint'>
                                                <xsl:value-of select="gco:CharacterString"/> <br />
                                            </xsl:for-each>
                                        </xsl:if>
                                        
                                        <xsl:if test="gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString">
                                            <xsl:value-of select="gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString"/>
                                            <xsl:value-of select="gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString"/>
                                            <xsl:value-of select="gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gco:CharacterString"/>
                                            <br />
                                        </xsl:if>
                            
                                        <xsl:if test="gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice">
                                            Tél: 
                                            <xsl:for-each select='gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice'>
                                                <xsl:value-of select="gco:CharacterString"/> -
                                            </xsl:for-each> <br />
                                        </xsl:if>
                                        
                                        <xsl:if test="gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:facsimile">
                                            Fax:
                                            <xsl:for-each select='gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:facsimile'>
                                                <xsl:value-of select="gco:CharacterString"/> -
                                            </xsl:for-each> <br />
                                        </xsl:if>
                                        
                                        <xsl:if test="gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress">
                                            E-mail: 
                                            <xsl:for-each select='gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress'>
                                                <xsl:value-of select="gco:CharacterString"/> -
                                            </xsl:for-each> <br />
                                        </xsl:if>
                                        
                                        <xsl:if test="gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage">
                                            Site Internet: 
                                            <xsl:for-each select='gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage'>
                                                <xsl:value-of select="gmd:URL"/> -
                                            </xsl:for-each> <br />
                                        </xsl:if>
                                    </td>
                            
                                    <td class="td2_cnt"> 
                                        <xsl:for-each select='gmd:CI_ResponsibleParty/gmd:role'>
                                            <xsl:call-template name="roleCode">
                                                <xsl:with-param name="val" select="gmd:CI_RoleCode/@codeListValue"/>
                                            </xsl:call-template>
                                        </xsl:for-each>
                                    </td>
                                </tr>
                            </xsl:for-each>
                        </table> 
                    </xsl:if>  
                </td>
            </tr>
            <tr>
                <td class="td1">Langues des données:</td>
                <td class="td2"> 
                    <xsl:choose>
                        <xsl:when test="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:language/gmd:LanguageCode">
                            <xsl:for-each select='gmd:identificationInfo/gmd:MD_DataIdentification/gmd:language'>
                                <xsl:call-template name="languageCode">
                                    <xsl:with-param name="val" select="gmd:LanguageCode/@codeListValue"/>
                                </xsl:call-template>
                                <br />
                            </xsl:for-each>
                        </xsl:when>
                        <xsl:otherwise>
                            Non renseigné
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>
            <tr>
                <td class="td1">Jeu de charactères:</td>
                <td class="td2"> 
                    <xsl:choose>
                        <xsl:when test="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:characterSet/gmd:characterSetCode">
                            <xsl:value-of select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:characterSet/gmd:characterSetCode"/> <br />
                        </xsl:when>
                        <xsl:otherwise>
                            Non renseigné
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>
        </table>
        
        <table class="ui-state-default ui-corner-all">
            <tr>
                <th colspan="2" class="partie ui-widget-header ui-corner-all">Références géographiques</th>
            </tr>
            <tr>
                <td class="td1">Emprise:</td>
                <td class="td2">
                    <xsl:for-each select='gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent'>
                        <xsl:if test="gmd:EX_Extent/gmd:geographicElement">
                            <xsl:value-of select="gmd:EX_Extent/gmd:description/gco:CharacterString"/>
                            (W:<xsl:value-of select="gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal" /> - 
                            E:<xsl:value-of select="gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal" /> - 
                            S:<xsl:value-of select="gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal" /> - 
                            N:<xsl:value-of select="gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal" />) <br />
                        </xsl:if>  
                    </xsl:for-each>
                </td>
            </tr>
          
            <tr>
                <td class="td1">Etendue verticale:</td>
                <td class="td2"> 
                    <xsl:choose>
                        <xsl:when test="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent">
                   
                            <table class="tb_cnt ui-state-default ui-corner-all">
                            
                                <tr>
                                    <th class="titre ui-state-default ui-corner-all">Minimum</th>
                                    <th class="titre ui-state-default ui-corner-all">Maximum</th>
                                    <th class="titre ui-state-default ui-corner-all">Unité</th>
                                    <th class="titre ui-state-default ui-corner-all">Système de référence</th>
                                </tr>
                                <xsl:for-each select='gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:verticalElement'>
                                    <tr>
                                        <td><xsl:value-of select="gmd:EX_VerticalExtent/gmd:minValue/gco:CharacterString"/></td>
                                        <td><xsl:value-of select="gmd:EX_VerticalExtent/gmd:maxValue/gco:CharacterString"/></td>
                                        <td>mètre</td>
                                        <td><xsl:value-of select="gmd:EX_VerticalExtent/gmd:verticalDatum/gco:CharacterString"/></td>
                                    </tr>
                                </xsl:for-each>

                            </table>

                        </xsl:when>
                        <xsl:otherwise>
                            Non renseigné
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>
            
            <tr>
                <td class="td1">Etendue temporelle:</td>
                <td class="td2">
                    <xsl:choose>
                        <xsl:when test="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement">
                            <xsl:for-each select='gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement'>
                               <xsl:value-of select="gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:beginPosition"/> /
                               <xsl:value-of select="gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:endPosition"/> <br />
                            </xsl:for-each>
                        </xsl:when>
                    <xsl:otherwise>
                        Non renseigné
                    </xsl:otherwise>
                </xsl:choose>

                </td>
            </tr>

            <tr>
                <td class="td1">Système de projection:</td>
                <td class="td2"> 
                    <xsl:for-each select='gmd:referenceSystemInfo'>
                        <xsl:if test="gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString">
                            <xsl:value-of select="gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString"/> <br />
                        </xsl:if>
                    </xsl:for-each>
                </td>
            </tr>
                <xsl:if test="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:equivalentScale/gmd:MD_RepresentativeFraction/gmd:denominator/gco:Integer">
                    <tr>
                        <td class="td1">Echelle:</td>
                        <td class="td2"> <xsl:value-of select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:equivalentScale/gmd:MD_RepresentativeFraction/gmd:denominator/gco:Integer"/> </td>
                    </tr>
                </xsl:if>
                <xsl:if test="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution/distance/gco:Integer">
                    <tr>
                        <td class="td1">Résolution spatiale:</td>
                        <td class="td2"> <xsl:value-of select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution/distance/gco:Integer"/> </td>
                    </tr>
                </xsl:if>
          
          
            <tr>
                <td class="td1">Type de représentation:</td>
                <td class="td2">
                    <xsl:choose>
                        <xsl:when test="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode/@codeListValue">
                            <xsl:call-template name="spatialRepresentationTypeCode">
                                <xsl:with-param name="val" select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode/@codeListValue"/>
                            </xsl:call-template>
                        </xsl:when>
                        <xsl:otherwise>
                            Non renseigné
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>
          
        </table>
        
        <table class="ui-state-default ui-corner-all">
            <tr>
                <th colspan="2" class="partie ui-widget-header ui-corner-all">Qualité du lot de données</th>
            </tr>
            <tr>
                <td class="td1">Niveau décrit:</td>
                <td class="td2">
                    <xsl:choose>
                        <xsl:when test="gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:scope/gmd:DQ_Scope/gmd:level/gmd:MD_ScopeCode">
                            <xsl:call-template name="scopeCode">
                                <xsl:with-param name="val" select="gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:scope/gmd:DQ_Scope/gmd:level/gmd:MD_ScopeCode/@codeListValue"/>
                            </xsl:call-template>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:call-template name="scopeCode">
                                <xsl:with-param name="val" select="gmd:hierarchyLevel/gmd:MD_ScopeCode/@codeListValue"/>
                            </xsl:call-template>
                            (type de ressource décrite)
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>
          
            <tr>
                <td class="td1">Processus:</td>
                <td class="td2"> 
                    <xsl:choose>
                        <xsl:when test="gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:processStep/gmd:LI_ProcessStep/gmd:description">
                            <xsl:value-of select="gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:processStep/gmd:LI_ProcessStep/gmd:description/gco:CharacterString"/>
                        </xsl:when>
                        <xsl:otherwise>
                            Non renseigné
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>
            <tr>
                <td class="td1">Origine des données:</td>
                <td class="td2"> 
                    <xsl:choose>
                        <xsl:when test="gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:source/gmd:LI_Source/gmd:description">
                            <xsl:value-of select="gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:source/gmd:LI_Source/gmd:description/gco:CharacterString"/> 
                        </xsl:when>
                        <xsl:otherwise>
                            Non renseigné
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>
            <tr>
                <td class="td1">Texte sur la qualité:</td>
                <td class="td2"> 
                    <xsl:choose>
                        <xsl:when test="gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:statement">
                            <xsl:value-of select="gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:statement/gco:CharacterString"/>
                        </xsl:when>
                        <xsl:otherwise>
                            Non renseigné
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>
        </table>
        
        <table class="ui-state-default ui-corner-all">
            <tr>
                <th colspan="2" class="partie ui-widget-header ui-corner-all">Diffusion des données</th>
            </tr>
            <tr>
                <td class="td1">Format(s) de diffusion:</td>
                <td class="td2">
                    <xsl:choose>
                        <xsl:when test="gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat">
                            <xsl:for-each select='gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat'>
                                <xsl:value-of select="gmd:MD_Format/gmd:name/gco:CharacterString"/>
                                <xsl:if test="gmd:MD_Format/gmd:version/gco:CharacterString">
                                    (version: <xsl:value-of select="gmd:MD_Format/gmd:version/gco:CharacterString"/>)<br />
                                </xsl:if>
                            </xsl:for-each>
                        </xsl:when>
                        <xsl:otherwise>
                            Non renseigné
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>
            <tr>
                <td class="td1">Limites d'utilisation:</td>
                <td class="td2">
                    <xsl:choose>
                        <xsl:when test="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_Constraints/gmd:useLimitation">
                            <xsl:for-each select='gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_Constraints/gmd:useLimitation'>
                                <xsl:value-of select="gco:CharacterString/."/><br />
                            </xsl:for-each>
                        </xsl:when>
                        <xsl:otherwise>
                            Non renseigné
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>

            <tr>
                <td class="td1">Contraintes d'accès:</td>
                <td class="td2"> 
                    <xsl:choose>
                        <xsl:when test="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:accessConstraints">
                            <xsl:for-each select='gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:accessConstraints'>
                                <xsl:call-template name="restrictionCode">
                                    <xsl:with-param name="val" select="gmd:MD_RestrictionCode/@codeListValue"/> 
                                </xsl:call-template>
                                <br />
                                <!--<xsl:value-of select="gmd:MD_RestrictionCode/."/><br />-->
                            </xsl:for-each>
                        </xsl:when>
                        <xsl:otherwise>
                            Non renseigné
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>
                    
            <tr>
                <td class="td1">Contraintes d'utilisation:</td>
                <td class="td2"> 
                    <xsl:choose>
                        <xsl:when test="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:useConstraints">
                            <xsl:for-each select='gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:useConstraints'>
                                <xsl:call-template name="restrictionCode">
                                    <xsl:with-param name="val" select="gmd:MD_RestrictionCode/@codeListValue"/>
                                </xsl:call-template>
                                <br />
                            </xsl:for-each>
                        </xsl:when>
                        <xsl:otherwise>
                            Non renseigné
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>
            <tr>
                <td class="td1">Autres contraintes:</td>
                <td class="td2"> 
                    <xsl:choose>
                        <xsl:when test="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:otherConstraints">
                            <xsl:for-each select='gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:otherConstraints'>
                                <xsl:value-of select="gco:CharacterString/."/><br />
                            </xsl:for-each>
                        </xsl:when>
                        <xsl:otherwise>
                            Non renseigné
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>
            <tr>
                <td class="td1">Restrictions d'utilisation:</td>
                <td class="td2"> 
                    <xsl:choose>
                        <xsl:when test="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_SecurityConstraints">
                            <xsl:call-template name="classificationCode">
                                <xsl:with-param name="val" select="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_SecurityConstraints/gmd:MD_ClassificationCode/@codeListValue"/>
                            </xsl:call-template>
                            <br />
                        </xsl:when>
                        <xsl:otherwise>
                            Non renseigné
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>
            <tr>
                <td class="td1">Accès en ligne:</td>
                <td class="td2"> 
                    <xsl:choose>
                        <xsl:when test="gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine">
                            <xsl:for-each select='gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine'>
                                <a href="{gmd:CI_OnlineResource/gmd:linkage/gmd:URL/.}"><xsl:value-of select="gmd:CI_OnlineResource/gmd:linkage/gmd:URL/."/></a><br />
                            </xsl:for-each>
                        </xsl:when>
                        <xsl:otherwise>
                            Non renseigné
                        </xsl:otherwise>
                    </xsl:choose>
                </td>
            </tr>

        </table>
        

        
        <!-- CATALOGUE D'OBJET -->
        
        <!--
        <xsl:if test="contentInfo/gmd:MD_FeatureCatalogueDescription/featureCatalogue/iso19110:FC_FeatureCatalogue/name/gco:CharacterString">
        
        <table class="ui-state-default ui-corner-all">
           <tr>
            <th colspan="2" class="partie ui-widget-header ui-corner-all"> Catalogue(s) d'objet(s) </th>
          </tr>
          <xsl:for-each select='contentInfo/gmd:MD_FeatureCatalogueDescription'>              
          <tr>
            <td class="td1"> Nom :</td>
            <td class="td2"> <xsl:value-of select="featureCatalogue/iso19110:FC_FeatureCatalogue/name/gco:CharacterString"/> </td>
            
          </tr>
          <tr>
            <td class="td1"> Version :</td>
            <td class="td2"> <xsl:value-of select="featureCatalogue/iso19110:FC_FeatureCatalogue/versionNumber/gco:CharacterString"/> </td>
            
          </tr>
          <tr>
            <td class="td1"> Date :</td>
            <td class="td2"> 
                <xsl:call-template name="date">
                    <xsl:with-param name="ladate" select="featureCatalogue/iso19110:FC_FeatureCatalogue/versionDate/gco:Date"/>
                </xsl:call-template>
            </td>
          </tr>
          <tr>
            <td class="td1"> Langue :</td>
            <td class="td2"> <xsl:value-of select="featureCatalogue/iso19110:FC_FeatureCatalogue/functionalLanguage/gco:CharacterString"/> </td>
          </tr>
          <tr>
            <td class="td1"> Producteur :</td>
            <td class="td2">
                <xsl:for-each select='featureCatalogue/iso19110:FC_FeatureCatalogue/producer'>
                    <xsl:call-template name="responsibleParty" />                
                </xsl:for-each> 
            </td>
          </tr>

        <xsl:if test="featureCatalogue/iso19110:FC_FeatureCatalogue/featureType/iso19110:FC_FeatureType/typeName/gco:LocalName">
          <xsl:for-each select='featureCatalogue/iso19110:FC_FeatureCatalogue/featureType'>
          <tr>
            <td colspan="2" class="">
            <table class="ui-state-default ui-corner-all">
                   <tr>
                    <th colspan="2" class="titre titre_obj ui-state-default ui-corner-all"> Objet </th>
                  </tr>
                                
                  <tr>
                    <td class="td1"> Nom :</td>
                    <td class="td2"> <xsl:value-of select="iso19110:FC_FeatureType/typeName/gco:LocalName"/> </td>
                  </tr>
                  <tr>
                    <td class="td1"> Code :</td>
                    <td class="td2"> <xsl:value-of select="iso19110:FC_FeatureType/code"/> </td>
                  </tr>
                  <tr>
                    <td class="td1"> Définition :</td>
                    <td class="td2"> <xsl:value-of select="iso19110:FC_FeatureType/definition/gco:CharacterString"/> </td>
                  </tr>
                  
                  <xsl:if test="iso19110:FC_FeatureType/carrierOfCharacteristics/iso19110:FC_FeatureAttribute/memberName/gco:LocalName">
                  <tr>
                    <td colspan="2" class="titre_obj">
                    <table class="ui-state-default ui-corner-all">
                           <tr>
                            <th colspan="6" class="titre ui-state-default ui-corner-all"> Attributs </th>
                          </tr>
                          
                          <tr>
                            <td class="td1 titre"> Nom (code)</td>
                            <td class="titre"> Définition (type - cardinalité)</td>
                            <td class="titre"> Valeurs prédéfinies (définition)</td>                     
                          </tr>
                          
                          <xsl:for-each select='iso19110:FC_FeatureType/carrierOfCharacteristics'>
                          
                          <tr>
                            <td class="td1"> <xsl:value-of select="iso19110:FC_FeatureAttribute/memberName/gco:LocalName"/>
                            (<xsl:value-of select="iso19110:FC_FeatureAttribute/code/gco:CharacterString"/>)</td>

                            <td class=""> <xsl:value-of select="iso19110:FC_FeatureAttribute/definition/gco:CharacterString"/> 
                            (<xsl:value-of select="iso19110:FC_FeatureAttribute/valueType/gco:TypeName/aName/gco:CharacterString"/> 
                            - <xsl:value-of select="iso19110:FC_FeatureAttribute/cardinality/gco:Multiplicity/range/gco:MultiplicityRange/lower/gco:nonNegativeInteger"/>..<xsl:value-of select="iso19110:FC_FeatureAttribute/cardinality/gco:Multiplicity/range/gco:MultiplicityRange/upper/gco:UnlimitedInteger"/>)</td>
                            <td class="">
                                <xsl:for-each select='iso19110:FC_FeatureAttribute/listedValue'>
                                    - <span style="font-style:italic; font-weight:bold;"><xsl:value-of select="iso19110:FC_ListedValue/code/gco:CharacterString"/></span>" 
                                    (<xsl:value-of select="iso19110:FC_ListedValue/definition/gco:CharacterString"/>) <br />
                                </xsl:for-each>
                            </td>   
                          </tr>
                          
                          </xsl:for-each> 

                    </table>
                    </td>      
                  </tr>
                  </xsl:if>
                  
            </table>
            </td>      
          </tr>
          </xsl:for-each> 
          </xsl:if>
          
          </xsl:for-each> 
        </table>
        </xsl:if>
        
        
        <xsl:if test="contentInfo/gmd:MD_FeatureCatalogueDescription/featureTypes/iso19110:FC_FeatureType/typeName/gco:LocalName">
            <table class="ui-state-default ui-corner-all">
               <tr>
                <th colspan="2" class="partie ui-widget-header ui-corner-all"> Catalogue d'objet </th>
              </tr>
        
        <xsl:for-each select='contentInfo/gmd:MD_FeatureCatalogueDescription'>

        <xsl:if test="featureTypes/iso19110:FC_FeatureType/typeName/gco:LocalName">
          <xsl:for-each select='featureTypes'>
            <tr>
                <td colspan="2" class="">
                <table class="tb_cnt ui-state-default ui-corner-all">
                   <tr>
                    <th colspan="2" class="titre titre_obj ui-state-default ui-corner-all"> Objet </th>
                  </tr>
                                
                  <tr>
                    <td class="td1"> Nom :</td>
                    <td class="td2"> <xsl:value-of select="iso19110:FC_FeatureType/typeName/gco:LocalName"/> </td>
                  </tr>
                  <tr>
                    <td class="td1"> Code :</td>
                    <td class="td2"> <xsl:value-of select="iso19110:FC_FeatureType/code"/> </td>
                  </tr>
                  <tr>
                    <td class="td1"> Définition :</td>
                    <td class="td2"> <xsl:value-of select="iso19110:FC_FeatureType/definition/gco:CharacterString"/> </td>
                  </tr>
                  
                  <xsl:if test="iso19110:FC_FeatureType/carrierOfCharacteristics/iso19110:FC_FeatureAttribute/memberName/gco:LocalName">
                  <tr>
                    <td colspan="2" class="titre_obj">
                    <table class="ui-state-default ui-corner-all">
                           <tr>
                            <th colspan="6" class="titre ui-state-default ui-corner-all"> Attributs </th>
                          </tr>
                          
                          <tr>
                            <td class="td1 titre"> Nom (code)</td>
                            <td class="titre"> Définition (type - cardinalité)</td>
                            <td class="titre"> Valeurs prédéfinies (définition)</td>                     
                          </tr>
                          
                          <xsl:for-each select='iso19110:FC_FeatureType/carrierOfCharacteristics'>
                          
                          <tr>
                            <td class="td1"> <xsl:value-of select="iso19110:FC_FeatureAttribute/memberName/gco:LocalName"/>
                            (<xsl:value-of select="iso19110:FC_FeatureAttribute/code/gco:CharacterString"/>)</td>
                            <td class=""> <xsl:value-of select="iso19110:FC_FeatureAttribute/definition/gco:CharacterString"/> 
                            (<xsl:value-of select="iso19110:FC_FeatureAttribute/valueType/gco:TypeName/aName/gco:CharacterString"/> 
                            - <xsl:value-of select="iso19110:FC_FeatureAttribute/cardinality/gco:Multiplicity/range/gco:MultiplicityRange/lower/gco:nonNegativeInteger"/>..<xsl:value-of select="iso19110:FC_FeatureAttribute/cardinality/gco:Multiplicity/range/gco:MultiplicityRange/upper/gco:UnlimitedInteger"/>)</td>
                            <td class="">
                                <xsl:for-each select='iso19110:FC_FeatureAttribute/listedValue'>
                                    - "<span style="font-style:italic; font-weight:bold;"><xsl:value-of select="iso19110:FC_ListedValue/code/gco:CharacterString"/></span>" 
                                    (<xsl:value-of select="iso19110:FC_ListedValue/definition/gco:CharacterString"/>) <br />
                                </xsl:for-each>
                            </td>   
                          </tr>
                          
                          </xsl:for-each> 

                    </table>
                    </td>      
                  </tr>
                  </xsl:if>
                  
                </table>
                </td>      
               </tr>
            </xsl:for-each> 
        </xsl:if>
        </xsl:for-each>
        </table>
        </xsl:if>
        
        -->
        
        
        <!--<div class="note"> Métdonnées produites et gérées grâce au Serveur Fédérateur de Métadonnées (SFM) du partenariat CIGAL - www.cigalsace.org </div> -->
        
    </xsl:template>

    <!-- Template pour la création d'un responsible Party -->
    <xsl:template name="responsibleParty">
        <xsl:if test="gmd:CI_ResponsibleParty/individualName/gco:CharacterString">
            <xsl:value-of select="featureCatalogue/iso19110:FC_FeatureCatalogue/producer/gmd:CI_ResponsibleParty/individualName/gco:CharacterString"/> <br />
        </xsl:if>

        <xsl:if test="gmd:CI_ResponsibleParty/positionName/gco:CharacterString">
            <xsl:value-of select="gmd:CI_ResponsibleParty/positionName/gco:CharacterString"/> <br />
        </xsl:if>
        
        <xsl:if test="gmd:CI_ResponsibleParty/organisationName/gco:CharacterString">
            <xsl:value-of select="gmd:CI_ResponsibleParty/organisationName/gco:CharacterString"/> <br />
        </xsl:if>
        
        <xsl:if test="gmd:CI_ResponsibleParty/contactInfo/gmd:CI_Contact/address/gmd:CI_Address/deliveryPoint">
            <xsl:for-each select='gmd:CI_ResponsibleParty/contactInfo/gmd:CI_Contact/address/gmd:CI_Address/deliveryPoint'>
                <xsl:value-of select="gco:CharacterString"/> <br />
            </xsl:for-each>
        </xsl:if>
        
        <xsl:if test="gmd:CI_ResponsibleParty/contactInfo/gmd:CI_Contact/address/gmd:CI_Address/city/gco:CharacterString">
            <xsl:value-of select="gmd:CI_ResponsibleParty/contactInfo/gmd:CI_Contact/address/gmd:CI_Address/postalCode/gco:CharacterString"/>
            <xsl:value-of select="gmd:CI_ResponsibleParty/contactInfo/gmd:CI_Contact/address/gmd:CI_Address/city/gco:CharacterString"/>
            <xsl:value-of select="gmd:CI_ResponsibleParty/contactInfo/gmd:CI_Contact/address/gmd:CI_Address/country/gco:CharacterString"/>
            <br />
        </xsl:if>
        
        <xsl:if test="gmd:CI_ResponsibleParty/contactInfo/gmd:CI_Contact/phone/gmd:CI_Telephone/voice">
            Tél : 
            <xsl:for-each select='gmd:CI_ResponsibleParty/contactInfo/gmd:CI_Contact/phone/gmd:CI_Telephone/voice'>
                <xsl:value-of select="gco:CharacterString"/> -
            </xsl:for-each> <br />
        </xsl:if>
        
        <xsl:if test="gmd:CI_ResponsibleParty/contactInfo/gmd:CI_Contact/phone/gmd:CI_Telephone/facsimile">
            Fax :
            <xsl:for-each select='gmd:CI_ResponsibleParty/contactInfo/gmd:CI_Contact/phone/gmd:CI_Telephone/facsimile'>
                <xsl:value-of select="gco:CharacterString"/> -
            </xsl:for-each> <br />
        </xsl:if>
        
        <xsl:if test="gmd:CI_ResponsibleParty/contactInfo/gmd:CI_Contact/address/gmd:CI_Address/electronicMailAddress">
            E-mail : 
            <xsl:for-each select='gmd:CI_ResponsibleParty/contactInfo/gmd:CI_Contact/address/gmd:CI_Address/electronicMailAddress'>
                <xsl:value-of select="gco:CharacterString"/> -
            </xsl:for-each> <br />
        </xsl:if>
        
        <xsl:if test="gmd:CI_ResponsibleParty/contactInfo/gmd:CI_Contact/onlineResource/gmd:CI_OnlineResource/linkage">
            Site Internet : 
            <xsl:for-each select='gmd:CI_ResponsibleParty/contactInfo/gmd:CI_Contact/onlineResource/gmd:CI_OnlineResource/linkage'>
                <xsl:value-of select="gmd:URL"/> -
            </xsl:for-each> <br />
        </xsl:if>
    </xsl:template>

    <!-- Template de formatage de la date -->
    <xsl:template name="date">
        <xsl:param name="ladate"/>
        <xsl:value-of select="substring($ladate,9,2)"/>/<xsl:value-of select="substring($ladate,6,2)"/>/<xsl:value-of select="substring($ladate,1,4)"/>
    </xsl:template>
    
    <!-- Template de traduction des topicCategory -->
    <xsl:template name="topicCategory">
        <xsl:param name="val"/>
        <xsl:value-of select="$fileMapping/xsl:stylesheet/map:Mapping/map:topicCategory/map:code[@iso=$val]/@code"/><br /> 
    </xsl:template>
    
    <!-- Template de traduction des restrictionCode -->
    <xsl:template name="restrictionCode">
        <xsl:param name="val"/>
        <xsl:value-of select="$fileMapping/xsl:stylesheet/map:Mapping/map:restrictionCode/map:code[@iso=$val]/@code"/><br /> 
    </xsl:template>
    
    <!-- Template de traduction des classificationCode -->
    <xsl:template name="classificationCode">
        <xsl:param name="val"/>
        <xsl:value-of select="$fileMapping/xsl:stylesheet/map:Mapping/map:classificationCode/map:code[@iso=$val]/@code"/><br /> 
    </xsl:template>
    
    <!-- Template de traduction des spatialRepresentationTypeCode -->
    <xsl:template name="spatialRepresentationTypeCode">
        <xsl:param name="val"/>
        <xsl:value-of select="$fileMapping/xsl:stylesheet/map:Mapping/map:spatialRepresentationTypeCode/map:code[@iso=$val]/@code"/><br /> 
    </xsl:template>
    
    <!-- Template de traduction des roleCode -->
    <xsl:template name="roleCode">
        <xsl:param name="val"/>
        <xsl:value-of select="$fileMapping/xsl:stylesheet/map:Mapping/map:roleCode/map:code[@iso=$val]/@code"/><br /> 
    </xsl:template>
    
    <!-- Template de traduction des scopeCode -->
    <xsl:template name="scopeCode">
        <xsl:param name="val"/>
        <xsl:value-of select="$fileMapping/xsl:stylesheet/map:Mapping/map:scopeCode/map:code[@iso=$val]/@code"/><br /> 
    </xsl:template>
    
    <!-- Template de traduction des languageCode -->
    <xsl:template name="languageCode">
        <xsl:param name="val"/>
        <xsl:value-of select="$fileMapping/xsl:stylesheet/map:Mapping/map:languageCode/map:code[@iso=$val]/@code"/><br /> 
    </xsl:template>
    
    <!-- Template de traduction des dateTypeCode -->
    <xsl:template name="dateTypeCode">
        <xsl:param name="val"/>
        <xsl:value-of select="$fileMapping/xsl:stylesheet/map:Mapping/map:dateTypeCode/map:code[@iso=$val]/@code"/>
    </xsl:template>
    

</xsl:stylesheet>