import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchild(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])

        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)

        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_child_no_value(self):
        child_node = LeafNode("span", None)
        parent_node = ParentNode("div", [child_node])

        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_child_no_tag(self):
        child_node = LeafNode(None, "child")
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(parent_node.to_html(), "<div>child</div>")

    def test_to_html_complex(self):
        great_grandchild1 = LeafNode(None, "great grand child 1")
        great_grandchild2 = LeafNode("b", "great grand child 2", {"href": "https://www.google.com/"})

        grandchild1 = ParentNode("p", [great_grandchild1, great_grandchild2], {"target": "_blank"})
        grandchild2 = ParentNode("p", [great_grandchild1])

        child = ParentNode("span", [grandchild1, grandchild2], {"href": "https://www.boot.dev/dashboard"})

        parent = ParentNode("div", [child])

        assert_html_str = (
            '<div>'
                '<span href="https://www.boot.dev/dashboard">'
                    '<p target="_blank">'
                        'great grand child 1'
                        '<b href="https://www.google.com/">great grand child 2</b>'
                    '</p>'
                    '<p>great grand child 1</p>'
                '</span>'
            '</div>'
        )

        self.assertEqual(parent.to_html(), assert_html_str)
        