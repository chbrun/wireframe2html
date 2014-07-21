from xml.dom.minidom import parse
from optparse import OptionParser
from jinja2 import Environment, PackageLoader

def attribute2param(element):
    params={}
    attributes = element.attributes.items()
    for attribute in attributes:
        params[attribute[0]] = attribute[1]
    return params

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="inputfile",
            help="Screen Input File", metavar="FILE")
    parser.add_option("-s", "--screen", dest="inputscreen",
            help="Screen Input", metavar="Name")

    (options, args) = parser.parse_args()

    # Chargement de l'environnement pour les templates
    env = Environment(loader = PackageLoader('screen2html', 'templates'))

    screen_name = options.inputscreen
    screen = parse('%s.screen' % screen_name)
    htmlscreen = open('%s.html' % screen_name, 'w')

    page = env.get_template('page.tpl')

    content = ''
    root = screen.childNodes[0]
    widgets = root.childNodes
    for widget in widgets:
        if widget.nodeName == u'widgets' :
            subcontent=''
            template_path = widget.getAttribute('xsi:type')
            if template_path == 'model:Master':
                screens = widget.childNodes
                for screen in screens:
                    if screen.nodeName == u'screen':
                        subscreen = env.get_template('%s.tpl' % screen.getAttribute('href').replace("#","/"))
                        subcontent = subscreen.render()

            subtemplate = env.get_template('%s.tpl' % template_path.replace(":","/"))
            content += subtemplate.render(
                    attribute2param(widget),
                    content=subcontent
                       )


    htmlscreen.write(page.render(page_title=screen_name, content=content))
