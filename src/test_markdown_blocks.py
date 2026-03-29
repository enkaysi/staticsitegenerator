import unittest

from markdown_blocks import markdown_to_html_node, extract_title

class TestBlocks(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_all_elements(self):
        #self.maxDiff = None
        md = """
# this is a heading

## this is also a heading

### me too!

I'm just a regular paragraph with some **bold words in the middle** but _not_ the end
a little bit of _italics_ is alright

>a quote
>about penguins

- a list
- about goats

1. they are pretty cool
2. they make milk and cheese!

```
this is code
```

pretty sweet!

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is a heading</h1><h2>this is also a heading</h2><h3>me too!</h3><p>I'm just a regular paragraph with some <b>bold words in the middle</b> but <i>not</i> the end a little bit of <i>italics</i> is alright</p><blockquote>a quote about penguins</blockquote><ul><li>a list</li><li>about goats</li></ul><ol><li>they are pretty cool</li><li>they make milk and cheese!</li></ol><pre><code>this is code\n</code></pre><p>pretty sweet!</p></div>"
        )

    def test_images(self):
        md = """
this is just a paragraph with an image ![alt text](https://bootsissupercool.dev)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>this is just a paragraph with an image <img src="https://bootsissupercool.dev" alt="alt text"></img></p></div>'
        )

    def test_extract_title(self):
        md = """
# this is a heading test

this is a paragraph and shouldn't be selected
"""
        heading = extract_title(md)
        self.assertEqual(heading, "this is a heading test")

if __name__ == "__main__":
    unittest.main()