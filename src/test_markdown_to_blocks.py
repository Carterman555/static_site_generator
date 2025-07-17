import unittest
from functions import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):

    def test1(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test2(self):
        md = """
This is **bolded** paragraph




"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
            ],
        )


    def test3(self):
        md = """
This is **bolded** paragraph





- hello

- hello     
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "- hello",
                "- hello",
            ],
        )