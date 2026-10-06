from enum import Enum
from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"



def block_to_block_type(block : str) -> BlockType:
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks



def block_to_html_node(block : str) -> ParentNode:
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        block = block.replace('\n', ' ')
        htmlnode = text_to_children(block)
        return ParentNode(tag="p", children=htmlnode)
    
    elif block_type == BlockType.QUOTE:
        lines = block.split("\n")
        new_lines = []
        for line in lines:
            new_lines.append(line.lstrip(">").strip())
        content = " ".join(new_lines)
        children = text_to_children(content)
        return ParentNode(tag="blockquote", children=children)
    
    elif block_type == BlockType.ULIST:
        lines = block.split("\n")
        child_nodes = []
        for line in lines:
            children = text_to_children(line.lstrip("- "))
            child_nodes.append(ParentNode(tag="li", children=children))
        return ParentNode(tag="ul", children=child_nodes)
    
    elif block_type == BlockType.OLIST:
        lines = block.split("\n")
        child_nodes = []
        for line in lines:
            children = text_to_children(line.split(". ", 1)[-1])
            child_nodes.append(ParentNode(tag="li", children=children))
        return ParentNode(tag="ol", children=child_nodes)
    
    elif block_type == BlockType.CODE:
        if not block.startswith("```") or not block.endswith("```"):
            raise ValueError("invalid code block")
        text = block[4:-3]
        raw_text_node = TextNode(text, TextType.TEXT)
        child = text_node_to_html_node(raw_text_node)
        code = ParentNode("code", [child])
        return ParentNode("pre", [code])
    
    elif block_type == BlockType.HEADING:
        tag = ''
        if block.startswith('# '):
            tag = "h1"
        elif block.startswith('## '):
            tag = "h2"
        elif block.startswith('### '):
            tag = "h3"
        elif block.startswith('#### '):
            tag = "h4"
        elif block.startswith('##### '):
            tag = "h5"
        elif block.startswith('###### '):
            tag = "h6"
        children = text_to_children(block.split(" ", 1)[-1])
        return ParentNode(tag=tag, children=children)

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def text_to_children(text : str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes