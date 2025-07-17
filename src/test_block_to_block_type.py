import unittest
from functions import markdown_to_blocks
from functions import block_to_block_type
from blocktype import BlockType

class TestBlockToBlockType(unittest.TestCase):

    def test_just_text(self):
        md = "This is a bit of text"
        blocks = markdown_to_blocks(md)

        self.assertEqual(len(blocks), 1)

        blocktype = block_to_block_type(blocks[0])

        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_headings(self):
        md = (
            "# Heading 1\n"
            "\n"
            "## Heading 2\n"
            "\n"
            "### Heading 3\n"
            "\n"
            "#### Heading 4\n"
            "\n"
            "##### Heading 5\n"
            "\n"
            "###### Heading 6"
        )

        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 6)
        expected_types = [
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
        ]
        for block, expected_type in zip(blocks, expected_types):
            self.assertEqual(block_to_block_type(block), expected_type)

    def test_code_block(self):
        md = "```\nprint('Hello, world!')\n```"
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.CODE)

    def test_quote_block(self):
        md = "> This is a quote\n> Another line"
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.QUOTE)

    def test_unordered_list_block(self):
        md = "- Item 1\n- Item 2\n- Item 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        md = "1. First\n2. Second\n3. Third"
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.ORDERED_LIST)

    def test_ordered_list_block_fail(self):
        md = "1. First\n2. Second\n4. Third"
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.PARAGRAPH)
