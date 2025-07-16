import unittest
from functions import split_nodes_delimiter
from textnode import TextNode
from textnode import TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_only_text(self):
        node = TextNode("only text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "only text")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_bold(self):
        node = TextNode("this is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(len(new_nodes), 3)

        self.assertEqual(new_nodes[0].text, "this is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)


    def test_italic_code(self):
        node = TextNode("this is _italic_ and `code` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)

        self.assertEqual(len(new_nodes), 5)

        self.assertEqual(new_nodes[0].text, "this is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)

        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[3].text, "code")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)

        self.assertEqual(new_nodes[4].text, " text")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)


    def test_start_bold(self):
        node = TextNode("**this** is **bold** text", TextType.TEXT)

        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(len(new_nodes), 4)

        self.assertEqual(new_nodes[0].text, "this")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

        self.assertEqual(new_nodes[1].text, " is ")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[2].text, "bold")
        self.assertEqual(new_nodes[2].text_type, TextType.BOLD)

        self.assertEqual(new_nodes[3].text, " text")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)


    def test_start_bold_more_delimiting(self):
        node = TextNode("**this** is **bold** text", TextType.TEXT)

        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)

        self.assertEqual(len(new_nodes), 4)

        self.assertEqual(new_nodes[0].text, "this")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

        self.assertEqual(new_nodes[1].text, " is ")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[2].text, "bold")
        self.assertEqual(new_nodes[2].text_type, TextType.BOLD)

        self.assertEqual(new_nodes[3].text, " text")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)


    def test_end_bold(self):
        node = TextNode("this is **bold** **text**", TextType.TEXT)

        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)

        self.assertEqual(len(new_nodes), 4)

        self.assertEqual(new_nodes[0].text, "this is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

        self.assertEqual(new_nodes[2].text, " ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[3].text, "text")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)


    def test_only_bold(self):
        node = TextNode("**this is bold text**", TextType.TEXT)

        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 1)

        self.assertEqual(new_nodes[0].text, "this is bold text")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)


    # I don't know yet how I want to it handle this, or if it'll need to
    # def test_empty_bold(self):
    #     node = TextNode("****none of this is **** really bold****", TextType.TEXT)

    #     new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    #     new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    #     new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        
    #     print(new_nodes)

    