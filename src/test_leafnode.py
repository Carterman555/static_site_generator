import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_props(self):
        node = LeafNode("p", "Hello, world!", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<p href="https://www.google.com" target="_blank">Hello, world!</p>')

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello")
        self.assertEqual(node.to_html(), "Hello")
