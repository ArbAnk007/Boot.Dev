import re
from htmlnode import ParentNode
import textnode

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        filtered_blocks.append(block.strip())
    return filtered_blocks

markdown = "This is a single markdown \nWith a line break\n actually two linebreak"

def block_to_block_type(markdown):
    lines = markdown.split("\n")
    if (
        markdown.startswith("# ") or
        markdown.startswith("## ") or
        markdown.startswith("### ") or
        markdown.startswith("#### ") or
        markdown.startswith("##### ") or
        markdown.startswith("###### ")
    ):
        return "heading"
    
    if markdown.startswith("```") and markdown.endswith("```"):
        return "code"
    
    if markdown.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return "paragraph"
        return "unordered_list"
    
    if markdown.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return "paragraph"
        return "unordered_list"
    
    if markdown.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return "paragraph"
            i += 1
        return "ordered_list"
    
    if markdown.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return "paragraph"
        return "quote"
    return "paragraph"

def text_to_children(text):
    text_nodes = textnode.text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = textnode.text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    html = ""
    for block in blocks:
        match block_to_block_type(block):
            case "heading":
                html_nodes.append(heading_to_html_node(block))
                continue
            case "code":
                html_nodes.append(code_to_html_node(block))
                continue
            case "unordered_list":
                html_nodes.append(ulist_to_html_node(block))
                continue
            case "ordered_list":
                html_nodes.append(olist_to_html_node(block))
                continue
            case "quote":
                html_nodes.append(quote_to_html_node(block))
                continue
            case "paragraph":
                html_nodes.append(paragraph_to_html_node(block))
            case _:
                raise ValueError("Invalid markdown type")
            
    for html_node in html_nodes:
        html = html + html_node.to_html()
    return html