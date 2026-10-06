import os
import shutil

from markdown_blocks import markdown_to_html_node
from inline_markdown import extract_title

def copy_folder_contents_recursive(source="./static", destination="./public"):
    """copy all files from source folder to destination folder. 
    destination folder's contents will be overwritten"""

    if not os.path.exists(source):
        raise RuntimeError(f"{source} folder is missing.")
    if not os.path.exists(destination):
        os.mkdir(destination)

    for content in os.listdir(source):
        src_content_path = os.path.join(source, content)
        desti_content_path = os.path.join(destination, content)

        print (f"{src_content_path} --> {desti_content_path}")
        if os.path.isfile(src_content_path):
            shutil.copy(src=src_content_path, dst=desti_content_path)

        elif os.path.isdir(src_content_path):
            copy_folder_contents_recursive(source=src_content_path, destination=desti_content_path)


def generate_page(from_path, template_path, dest_path, basepath):
    print (f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    html_node = markdown_to_html_node(markdown)

    html_string = html_node.to_html()
    title = extract_title(markdown)
    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', html_string)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, "w") as f:
        f.write(template)
    

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(os.path.dirname(dest_dir_path)):
        os.makedirs(os.path.dirname(dest_dir_path))

    for content in os.listdir(dir_path_content):
        src_content_path = os.path.join( dir_path_content, content)
        desti_content_path = os.path.join( dest_dir_path, content.replace(".md", ".html"))

        if os.path.isfile(src_content_path):
            generate_page(from_path=src_content_path, 
                          template_path=template_path, 
                          dest_path=desti_content_path,
                          basepath=basepath)

        elif os.path.isdir(src_content_path):
            generate_pages_recursive(dir_path_content=src_content_path, 
                                    template_path=template_path, 
                                    dest_dir_path=desti_content_path,
                                    basepath=basepath)
