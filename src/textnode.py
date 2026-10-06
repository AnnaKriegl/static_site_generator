from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold" # **Bold text**
    ITALIC = "italic" # _Italic text_
    CODE = "code" #`Code text`
    LINK = "link" # Links, in this format: [anchor text](url)
    IMAGE = "image" # Images, in this format: ![alt text](url)

class TextNode:
    def __init__(self, text : str, text_type : TextType, url : str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False
        return( self.text_type == other.text_type
               and self.text == other.text
               and self.url == other.url
               )

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'

def text_node_to_html_node( text_node: TextNode) -> LeafNode:
    if text_node.text_type not in TextType:
        raise Exception("No valid text type.")
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href" : text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", text_node.text, {"src": text_node.url, "alt" : text_node.text})

