from markdown import markdown_to_html
import os
from pathlib import Path

def extract_title(markdown_content):
    lines = markdown_content.split("\n")
    title = None
    for line in lines:
        if line.startswith("# "):
            title = line[2:]
            break
    if title == None:
        raise Exception("All pages need a single h1 header")
    return title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    file = open(from_path)
    markdown_content = file.read()
    file.close()

    file = open(template_path)
    template_content = file.read()
    file.close()

    title = extract_title(markdown_content)
    html_content = markdown_to_html(markdown_content)

    html = template_content.replace("{{ Content }}", html_content)
    html = html.replace("{{ Title }}", title)
    
    file = open(f"{dest_path}", "w")
    file.write(html)
    file.close()

def generate_pages_recursive(dir_path_content, template_path, dst_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dst_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)