import unittest
import mock
from wireframe2html import *
from xml.dom.minidom import Element

class TestWireframe2html(unittest.TestCase):

    def setUp(self):
        pass

    def test_attribute2param(self):
        element = Element('cbrun')
        element.setAttribute('href','http://site.free.fr')
        element.setAttribute('style','bien')
        self.assertItemsEqual(attribute2param(element),{'href':'http://site.free.fr', 'style':'bien'})

    def test_get_table_header(self):
        data =  "header1,header2,header3\nvalue1,value2,value3\nautrevalue1,autrevalue2,autrevalue3"
        self.assertItemsEqual(get_table_header(data),['header1','header2','header3'])

    def test_get_table_lignes(self):
        data =  "header1,header2,header3\nvalue1,value2,value3\nautrevalue1,autrevalue2,autrevalue3"
        self.assertItemsEqual(get_table_lignes(data),['value1,value2,value3','autrevalue1,autrevalue2,autrevalue3'])

    def test_get_table_ligne_value(self):
        data="value1,value2,value3"
        self.assertItemsEqual(get_table_ligne_value(data),['value1','value2','value3'])
