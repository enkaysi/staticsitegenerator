import re

from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # takes a list of old_nodes, a delimiter and a text_type (which should probably match the delimiter)
    # and returns a new list of nodes text nodes with wrapping text around the delimiter will need to be 
    # split and wrapped around the delimiter
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter in node.text:
            split = node.text.split(delimiter)   
            if len(split) % 2 == 0:
                raise Exception("helpful message: delimiter does not have a closing tag")
            for i in range(len(split)):
                if split[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(split[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split[i], text_type))       
        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text):
    # I take some text and check it for markdown images. 
    # I spit out a list of tuples starting with the image![alt text](the URL)
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)                       

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            original_text = node.text
            images = extract_markdown_images(node.text) # a list of image text and url tuples
            if len(images) > 0:
                for image in images:
                    split = original_text.split(f'![{image[0]}]({image[1]})', 1)
                    if len(split) != 2:
                        raise ValueError("invalid markdown, image section not closed")
                    if split[0] != "":
                        new_nodes.append(TextNode(split[0], TextType.TEXT))
                    new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    original_text = split[1]
                if original_text != "":
                    new_nodes.append(TextNode(original_text, TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            original_text = node.text
            links = extract_markdown_links(node.text) # a list of link text and url tuples
            if len(links) > 0:
                for link in links:
                    split = original_text.split(f'[{link[0]}]({link[1]})', 1)
                    if len(split) != 2:
                        raise ValueError("invalid markdown, image section not closed")
                    if split[0] != "":
                        new_nodes.append(TextNode(split[0], TextType.TEXT))
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    original_text = split[1]
                if original_text != "":
                    new_nodes.append(TextNode(original_text, TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes


def text_to_textnodes(text):
    start_node = [TextNode(text, TextType.TEXT)]
    bold_nodes = split_nodes_delimiter(start_node, "**", TextType.BOLD)
    italic_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
    code_nodes = split_nodes_delimiter(italic_nodes, "`", TextType.CODE)
    image_nodes = split_nodes_image(code_nodes)
    link_nodes = split_nodes_link(image_nodes)
    return link_nodes
