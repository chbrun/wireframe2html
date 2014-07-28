import unittest
import mock
from wireframe2html import attribute2param
from xml.dom.minidom import Element

class TestWireframe2html(unittest.TestCase):

    def setUp(self):
        pass

    def test_attribute2param(self):
        element = Element('cbrun')
        element.setAttribute('href','http://site.free.fr')
        element.setAttribute('style','bien')
        self.assertItemsEqual(attribute2param(element),{'href':'http://site.free.fr', 'style':'bien'})


