import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node

def generate_page(from_path, template_path, dest_path, basepath):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path, "r") as file:
        markdown = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    final = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    final = final.replace('href="/', f'href="{basepath}')
    final = final.replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(final)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(content_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(content_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(content_path, template_path, dest_path, basepath)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("no title in markdown")