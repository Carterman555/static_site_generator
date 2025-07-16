import unittest
from functions import split_nodes_link
from textnode import TextNode
from textnode import TextType

class TestSplitNodeLink(unittest.TestCase):

    def test_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev).", TextType.TEXT)
        new_nodes = split_nodes_link([node])

        self.assertEqual(len(new_nodes), 5)

        self.assertEqual(new_nodes[0].text, "This is text with a link ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[1].text, "to boot dev")
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)

        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[3].text, "to youtube")
        self.assertEqual(new_nodes[3].url, "https://www.youtube.com/@bootdotdev")
        self.assertEqual(new_nodes[3].text_type, TextType.LINK)

        self.assertEqual(new_nodes[4].text, ".")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)

    def test_start_end_links(self):
        node = TextNode("[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])

        self.assertEqual(new_nodes[0].text, "to boot dev")
        self.assertEqual(new_nodes[0].url, "https://www.boot.dev")
        self.assertEqual(new_nodes[0].text_type, TextType.LINK)

        self.assertEqual(new_nodes[1].text, " and ")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[2].text, "to youtube")
        self.assertEqual(new_nodes[2].url, "https://www.youtube.com/@bootdotdev")
        self.assertEqual(new_nodes[2].text_type, TextType.LINK)

    def test_duplicate_links(self):
        node = TextNode("[to boot dev](https://www.boot.dev)[to boot dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])

        self.assertEqual(len(new_nodes), 2)

        self.assertEqual(new_nodes[0].text, "to boot dev")
        self.assertEqual(new_nodes[0].url, "https://www.boot.dev")
        self.assertEqual(new_nodes[0].text_type, TextType.LINK)

        self.assertEqual(new_nodes[1].text, "to boot dev")
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)

    def test_no_links(self):
        node = TextNode("This is a test", TextType.TEXT)
        new_nodes = split_nodes_link([node])

        self.assertEqual(len(new_nodes), 1)

        self.assertEqual(new_nodes[0].text, "This is a test")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_multiple_nodes(self):
        node1 = TextNode("This is a test", TextType.TEXT)
        node2 = TextNode("[to boot dev](https://www.boot.dev)[to boot dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node1, node2])

        self.assertEqual(len(new_nodes), 3)

        self.assertEqual(new_nodes[0].text, "This is a test")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[1].text, "to boot dev")
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)

        self.assertEqual(new_nodes[2].text, "to boot dev")
        self.assertEqual(new_nodes[2].url, "https://www.boot.dev")
        self.assertEqual(new_nodes[2].text_type, TextType.LINK)