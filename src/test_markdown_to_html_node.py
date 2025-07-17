import unittest
from functions import markdown_to_html_node

class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_paragraph(self):
        md = (
            "This is a paragraph\n"
            "text in a p\n"
            "tag here"
        )

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><p>This is a paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = (
            "This is **bolded** paragraph\n"
            "text in a p\n"
            "tag here\n"
            "\n"
            "This is another paragraph with _italic_ text and `code` here\n"
        )

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_headings(self):
        md = (
            "# Heading1\n\n"
            "## Heading2\n\n"
            "### He`adin`g3\n\n"
            "#### Heading4\n\n"
            "##### Hea**din**g5\n\n"
            "###### Heading6\n\n"
        )

        node = markdown_to_html_node(md, True)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><h1>Heading1</h1><h2>Heading2</h2><h3>He<code>adin</code>g3</h3><h4>Heading4</h4><h5>Hea<b>din</b>g5</h5><h6>Heading6</h6></div>"
        )


    def test_codeblock(self):
        md = (
            "\n"
            "```\n"
            "This is text that _should_ remain\n"
            "the **same** even with inline stuff\n"
            "```\n"
        )

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    
    def test_quote(self):
        md = (
            ">I love coding\n"
            ">and stuff\n"
            "\n"
            "> Hello\n"
        )

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><blockquote>I love coding and stuff</blockquote><blockquote> Hello</blockquote></div>",
        )


    def test_unordered_list(self):
        md = (
            "- pizza\n"
            "- tacos\n"
            "- I love **burgers**!\n"
            "\n"
            "- shrimp"
        )

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><ul><li>pizza</li><li>tacos</li><li>I love <b>burgers</b>!</li></ul><ul><li>shrimp</li></ul></div>"
        )

    def test_ordered_list(self):
        md = (
            "1. one\n"
            "2. two\n"
            "3. three **yah**!\n"
        )

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><ol><li>one</li><li>two</li><li>three <b>yah</b>!</li></ol></div>"
        )