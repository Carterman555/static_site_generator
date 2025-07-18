import unittest
from functions import extract_title

class TestExtractTitle(unittest.TestCase):

    def test1(self):
        md = "# Hello"
        title = extract_title(md)
        self.assertEqual(title, "Hello")


    def test2(self):
        md = (
            "# Hello\n"
            "## hello again"
        )
        title = extract_title(md)
        self.assertEqual(title, "Hello")


    def test3(self):
        md = (
            "## Hello\n"
            "# hello again"
        )
        title = extract_title(md)
        self.assertEqual(title, "hello again")

    def test4(self):
        md = (
            "## Hello\n"
            "### hello again"
        )

        with self.assertRaises(Exception):
            extract_title(md)