import os
import shutil

from copystatic import copy_static
from gencontent import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    if os.path.exists("public"):
        print("deleting public folder")
        shutil.rmtree("public")
    
    print("transferring static assets")
    copy_static()

    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public,
        )


if __name__ == "__main__":
    main()