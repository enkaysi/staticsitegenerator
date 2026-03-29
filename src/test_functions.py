import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from textnode import TextType, TextNode

class TestFunctions(unittest.TestCase):
    def test_split_nodes_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_nodes_bold(self):
        node = TextNode("This is text with a *code block* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(new_nodes, [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_nodes_image(self):
        node = TextNode("This is text with an `image`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.IMAGE)
        self.assertEqual(new_nodes, [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE),
            ]
        )

    def test_split_nodes_raise(self):
        node = TextNode("This is text with an `image", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.IMAGE)

    def test_split_nodes_nontext(self):
        node = TextNode("*what*", TextType.BOLD)
        node2 = TextNode("`code`", TextType.CODE)
        new_nodes = split_nodes_delimiter([node, node2], "*", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("*what*", TextType.BOLD),
            TextNode("`code`", TextType.CODE),
            ]
        )

    def test_split_nodes_multipledelimiters(self):
        node = TextNode("*bold words* for a `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("bold words", TextType.BOLD),
            TextNode(" for a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            ]
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )

    def test_split_link(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
        new_nodes,
    )
        
    def test_split_link2(self):
        node = TextNode(
            "This is text with a [link] and another [second link]",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a [link] and another [second link]", TextType.TEXT),
            ],
        new_nodes,
    )

    def test_text_to_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_markdown_to_blocks(self):
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

    def test_markdown_to_blocks_black_lines(self):
        md = """
This is a



blank line



test

* to see



- line removal
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a",
                "blank line",
                "test",
                "* to see",
                "- line removal"
            ]
        )

    def test_block_to_blocktype(self):
        block = "#### This is a heading!"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
        )
    
    def test_block_to_blocktype_quote(self):
        block = ">This is a quote!\n>this too!\n>so is this"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE
        )
    
    def test_block_to_blocktype_quote_error(self):
        block = ">This is a quote!\n>this too!\n>so is this\nbut not this"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_block_to_blocktype_code(self):
        block = "```\nthis is a code block\nit has multiple lines\nbut it ends properly\n```"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE
        )

    def test_block_to_blocktype_code_err(self):
        block = "```\nthis is a code block\nit has multiple lines\nbut it doesn't ends properly\n``` cause of the trail!"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

if __name__ == "__main__":
    unittest.main()