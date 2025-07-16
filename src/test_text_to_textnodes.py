import unittest
from functions import text_to_textnodes
from textnode import TextNode
from textnode import TextType

class TestTextToTextnodes(unittest.TestCase):

    def test_just_text(self):
        text = "This is just text :)"
        nodes = text_to_textnodes(text)

        desired_nodes = [TextNode("This is just text :)", TextType.TEXT)]
        self.assertListEqual(nodes, desired_nodes)


    def test_bold(self):
        text = "This is **not** just text :|"
        nodes = text_to_textnodes(text)

        desired_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("not", TextType.BOLD),
            TextNode(" just text :|", TextType.TEXT)
        ]
        self.assertListEqual(nodes, desired_nodes)

    def test_every_type(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)

        desired_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(nodes, desired_nodes)
