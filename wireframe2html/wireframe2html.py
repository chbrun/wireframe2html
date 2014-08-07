import re
from xml.dom.minidom import parse
from optparse import OptionParser
from jinja2 import Environment, PackageLoader
from jinja2.exceptions import TemplateNotFound
from types import NoneType


def mreplace(replacements, text):
    regex = re.compile("(%s)" % "|".join(map(re.escape, replacements.keys())))
    return regex.sub(lambda mo: replacements[mo.string[mo.start():mo.end()]], text)


def attribute2param(element):
    params = {}
    attributes = element.attributes.items()
    for attribute in attributes:
        params[attribute[0]] = attribute[1]
    return params

def get_title_data(chaine):
    retour = {}
    if chaine.find('%')>0:
        parts=chaine.split('%')
        retour['text']=parts[0]
        if len(parts)>0:
            small=parts[1].split("~")
            retour['small'] = {
                    'text':small[1],
                    'font':small[0].split(":")[0].replace(')','')
                    }
    else:
        retour=chaine
    return retour



def get_pricing_title(chaine):
    ligne = chaine.split("\n")[0]
    retour = ligne.split('.')[1]
    return retour

def get_pricing_price(chaine):
    ligne = chaine.split("\n")[1]
    value = ligne.split('%')[1]
    retour = value.split(')')[1]
    return retour

def get_pricing_description(chaine):
    ligne = chaine.split("\n")[2]
    value = ligne.split('%')[1]
    retour = value.split(')')[1]
    return retour

def get_pricing_items(chaine):
    retour = chaine.split("\n")[3:-2]
    return retour

def get_table_header(chaine):
    header = chaine.split("\n")[0]
    retour = header.split(',')
    return retour


def get_table_lignes(chaine):
    lignes = chaine.split("\n")[1:]
    return lignes


def get_table_ligne_value(chaine):
    values = chaine.split(',')
    return values


def hasoverride(element):
    childs = element.childNodes
    retour = False
    for child in childs:
        if child.nodeName == u'overrides':
            retour = True
    return retour

def hasattribute(element):
    childs = element.childNodes
    retour = False
    for child in childs:
        if child.nodeName == u'attributes':
            retour = True
    return retour


def handleModelScreen(document, env):
    widgets = document.childNodes
    content = ''
    for widget in widgets:
        if widget.nodeName == u'widgets':
            content += handleWidgets(widget, env)
    return content


def handleWidgets(widget,env):
    content = ''
    if widget.getAttribute('xsi:type') in['model:Master', 'model:Image','model:Label']:
        overrides = []
        if hasoverride(widget):
            overrides = handleOverrides(widget.getElementsByTagName('overrides'))
        subcontent = handleScreen(widget.getElementsByTagName('screen'), env, overrides)
        template_path = widget.getAttribute('xsi:type')
        subtemplate = env.get_template('%s.tpl' % template_path.replace(":", "/"))
        content += subtemplate.render(
                    attribute2param(widget),
                    content=subcontent
                       )
    return content

def handleScreen(screens, env, overrides = []):
    if overrides is None:
        overrides=[]
    subcontent = ''
    for screen in screens:
        if screen.nodeName == u'screen':
            screen_path = mreplace({'#':'/','&':'_'}, screen.getAttribute('href')).replace("%20", "")
            try:
                subscreen = env.get_template('%s.tpl' % screen_path)
                subcontent = subscreen.render(overrides)
                return subcontent
            except TemplateNotFound:
                print "le template %s n'existe pas" % screen_path
                exit
    return False

def handleOverrides(data):
    overrides = {}
    subWidgets = data[0].getElementsByTagName('widgets')
    for subWidget in subWidgets:
        handleWidgetOverrides(subWidget)
        overrides['ref_%s' % subWidget.getAttribute('ref')] = handleWidgetOverrides(subWidget)
        if hasattribute(subWidget):
            attributes = handleAttribute(subWidget.getElementsByTagName('attributes'))
            for key, value in attributes.items():
                overrides[key]=value
    return overrides


def handleAttribute(data):
    overrides = {}
    for subAttribute in data:
        overrides['attr_%s' % subAttribute.getAttribute('key')] = subAttribute.getAttribute('value')
    return overrides

def handleWidgetOverrides(widgetoverride):
    params = attribute2param(widgetoverride)
    params['subitems'] = handleItems(widgetoverride)
    return params

def handleItems(widget):
    subitems = widget.getElementsByTagName('items')
    subelements = {}
    for subitem in subitems:
        subelements[subitem.getAttribute('ref')] = attribute2param(subitem)
    return subelements 

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="inputfile",
            help="Screen Input File", metavar="FILE")
    parser.add_option("-s", "--screen", dest="inputscreen",
            help="Screen Input", metavar="Name")
    parser.add_option("-w", "--workspace", dest="workspace",
            help="Wireframesketcher workspace", metavar="Workspace")
    parser.add_option("-o", "--output", dest="outputDir",
            help="Output Dir", metavar="Directory")

    (options, args) = parser.parse_args()

    # Chargement de l'environnement pour les templates
    env = Environment(loader=PackageLoader('wireframe2html', 'templates'))
    env.filters['get_table_header'] = get_table_header
    env.filters['get_table_lignes'] = get_table_lignes
    env.filters['get_table_ligne_value'] = get_table_ligne_value
    env.filters['get_pricing_title'] = get_pricing_title
    env.filters['get_pricing_price'] = get_pricing_price
    env.filters['get_pricing_description'] = get_pricing_description
    env.filters['get_pricing_items'] = get_pricing_items
    env.filters['get_title_data'] = get_title_data

    screen_name = options.inputscreen
    screen = parse('%s.screen' % screen_name)
    htmlscreen = open('%s.html' % screen_name, 'w')

    page = env.get_template('page.tpl')

    root = screen.childNodes[0]
    content = handleModelScreen(root, env)
    htmlscreen.write(page.render(page_title=screen_name, content=content))
