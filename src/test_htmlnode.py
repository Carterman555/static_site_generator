import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_fields(self):
        htmlnode1 = HTMLNode("a", "Text")
        self.assertEqual("a", htmlnode1.tag)
        self.assertEqual("Text", htmlnode1.value)
        self.assertEqual([], htmlnode1.children)
        self.assertEqual({}, htmlnode1.props)

    def test_props_to_html(self):
        htmlnode1 = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(htmlnode1.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_empty_props(self):
        htmlnode1 = HTMLNode("a", "Text")
        self.assertEqual(htmlnode1.props_to_html(), '')

    def test_repr(self):
        htmlnode1 = HTMLNode(tag="a", value="Text", props={"href": "https://www.google.com", "target": "_blank"})
        representation = 'HTMLNode(tag=a, value=Text, children=[], props= href="https://www.google.com" target="_blank")'
        self.assertEqual(htmlnode1.__repr__(), representation)
