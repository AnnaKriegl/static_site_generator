import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html1(self):
        node = HTMLNode(props = {"href": "https://www.google.com","target": "_blank",})
        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())

    def test_props_to_html2(self):
        node = HTMLNode(props = {"href": "https://www.google.com","target": "_blank",})
        self.assertNotEqual('href="https://www.google.com" target="_blank"', node.props_to_html())

    def test_repr(self):
        node = HTMLNode(tag="a", value="testing testi" )
        self.assertEqual("HTMLNode(a, testing testi, None, None)", repr(node))

    # LeafNode
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    #ParentNode
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_two_children(self):
        child_node = LeafNode("b", "bold")
        child_node2 = LeafNode(None, "normal text")
        parent_node = ParentNode("p", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<p><b>bold</b>normal text</p>")

    def test_to_html_headings(self):
        child_node = LeafNode("b", "bold")
        child_node2 = LeafNode(None, "normal text")
        parent_node = ParentNode("h2", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<h2><b>bold</b>normal text</h2>")


if __name__ == "__main__":
    unittest.main()
