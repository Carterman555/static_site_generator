import unittest
from functions import split_nodes_image
from textnode import TextNode
from textnode import TextType

class TestSplitNodesImage(unittest.TestCase):
    
    def test_images(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg).", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        self.assertEqual(len(new_nodes), 5)

        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[1].text, "rick roll")
        self.assertEqual(new_nodes[1].url, "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)

        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[3].text, "obi wan")
        self.assertEqual(new_nodes[3].url, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(new_nodes[3].text_type, TextType.IMAGE)

        self.assertEqual(new_nodes[4].text, ".")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)

    def test_start_end_images(self):
        node = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        self.assertEqual(new_nodes[0].text, "rick roll")
        self.assertEqual(new_nodes[0].url, "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(new_nodes[0].text_type, TextType.IMAGE)

        self.assertEqual(new_nodes[1].text, " and ")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[2].text, "obi wan")
        self.assertEqual(new_nodes[2].url, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(new_nodes[2].text_type, TextType.IMAGE)

    def test_duplicate_images(self):
        node = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif)![rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        self.assertEqual(len(new_nodes), 2)

        self.assertEqual(new_nodes[0].text, "rick roll")
        self.assertEqual(new_nodes[0].url, "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(new_nodes[0].text_type, TextType.IMAGE)

        self.assertEqual(new_nodes[1].text, "rick roll")
        self.assertEqual(new_nodes[1].url, "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)

    def test_no_images(self):
        node = TextNode("This is a test", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        self.assertEqual(len(new_nodes), 1)

        self.assertEqual(new_nodes[0].text, "This is a test")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_multiple_nodes(self):
        node1 = TextNode("This is a test", TextType.TEXT)
        node2 = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif)![rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT)
        new_nodes = split_nodes_image([node1, node2])

        self.assertEqual(len(new_nodes), 3)

        self.assertEqual(new_nodes[0].text, "This is a test")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[1].text, "rick roll")
        self.assertEqual(new_nodes[1].url, "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)

        self.assertEqual(new_nodes[2].text, "rick roll")
        self.assertEqual(new_nodes[2].url, "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(new_nodes[2].text_type, TextType.IMAGE)