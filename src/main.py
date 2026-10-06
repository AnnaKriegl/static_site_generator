import os
import sys
import shutil
from generator import copy_folder_contents_recursive, generate_pages_recursive

dir_path_static = "./static"
dir_path_content = "./content"
dir_path_public = "./docs"
basepath = "/"


def main():
    if sys.argv:
        basepath = sys.argv[1]

    print( "Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print ("Copying static files to public directory...")
    copy_folder_contents_recursive(dir_path_static, dir_path_public)

    print ("Generating pages...")
    generate_pages_recursive(dir_path_content, "./template.html", dir_path_public, basepath)
main()