import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node4 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")

        self.assertEqual(node, node2)
        self.assertEqual(node3, node4)

    def test_not_eq(self):
        
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("I'm different", TextType.BOLD)
        node3 = TextNode("I'm different", TextType.ITALIC)
        node4 = TextNode("Yah, well I'm more different", TextType.ITALIC)
        node5 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")

        self.assertNotEqual(node, node2)
        self.assertNotEqual(node2, node3)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node, node5)