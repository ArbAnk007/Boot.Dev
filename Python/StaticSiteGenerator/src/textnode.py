from htmlnode import LeafNode
import re

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case "text":
            return LeafNode(None, text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "link":
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case "image":
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Invalid text type")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    match delimiter:
        case "**":
            delimiter_name = "bold"
        case "*":
            delimiter_name = "italic"
        case "`":
            delimiter_name = "code"
    
    new_nodes = []
    for node in old_nodes:
        if text_type != "text":
            continue
        node_text_array = node.text.split(delimiter)
        for i in range(len(node_text_array)):
            if i % 2 != 0:
                new_nodes.append(TextNode(node_text_array[i], delimiter_name))
            else:
                if node_text_array[i] == "":
                    continue
                new_nodes.append(TextNode(node_text_array[i], node.text_type))
    return new_nodes

def extract_markdown_images(text):
    pattern_match = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return pattern_match

def extract_markdown_links(text):
    pattern_match = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return pattern_match

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != "text":
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], "text"))
            new_nodes.append(
                TextNode(
                    image[0],
                    "image",
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, "text"))
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != "text":
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(TextNode(original_text, "text"))
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})")
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], "text"))
            new_nodes.append(TextNode(link[0], "link", link[1]))
            original_text = sections[1]
            if original_text != "":
                new_nodes.append(TextNode(original_text, "text"))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, "text")]
    nodes = split_nodes_delimiter(nodes, "**", "text")
    nodes = split_nodes_delimiter(nodes, "*", "text")
    nodes = split_nodes_delimiter(nodes, "`", "text")
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_links(nodes)
    return nodes