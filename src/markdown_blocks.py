from enum import Enum
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(markdown):
    # takes a raw markdown string
    # spits out list of block strings

    blocks = markdown.split("\n\n")
    block_list = []
    for block in blocks:
        if block == "":
            continue
        block_list.append(block.strip())
    return block_list


def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and block.startswith("```\n") and lines[-1] == "```":
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
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_list = []
    for block in blocks:
        lines = block.split("\n")
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            paragraph = " ".join(lines)
            child_list.append(ParentNode("p", text_to_children(paragraph)))
        elif block_type == BlockType.HEADING:
            count = 0
            for char in block:
                if char == "#":
                    count += 1
                else:
                    break
            child_list.append(ParentNode(f"h{count}", text_to_children(block[count + 1:])))
        elif block_type == BlockType.CODE:
            text_node = TextNode(block[4:-3], TextType.CODE)
            child_list.append(ParentNode("pre", [text_node_to_html_node(text_node)]))
        elif block_type == BlockType.QUOTE:
            new_lines = []
            for line in lines:
                line = line.lstrip(">").strip()
                new_lines.append(line)
            paragraph = " ".join(new_lines)
            child_list.append(ParentNode("blockquote", text_to_children(paragraph)))
        elif block_type == BlockType.UNORDERED_LIST:
            new_lines = []
            for line in lines:
                line = line.lstrip("-").strip()
                new_lines.append(f"<li>{line}</li>")
            paragraph = "".join(new_lines)
            child_list.append(ParentNode("ul", text_to_children(paragraph)))
        elif block_type == BlockType.ORDERED_LIST:
            new_lines = []
            i = 1
            for line in lines:
                line = line.lstrip(f"{i}. ").strip()
                new_lines.append(f"<li>{line}</li>")
                i += 1
            paragraph = "".join(new_lines)
            child_list.append(ParentNode("ol", text_to_children(paragraph)))
        else:
            raise Exception("invalid blocktype")
    return ParentNode("div", child_list)
    


