import os
import sys
import shutil

from copystatic import copy_static
from gencontent import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    if sys.argv[1]:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    if os.path.exists(dir_path_public):
        print("deleting public folder")
        shutil.rmtree(dir_path_public)
    
    print("transferring static assets")
    copy_static(dir_path_static, dir_path_public)

    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public,
        basepath,
        )



if __name__ == "__main__":
    main()