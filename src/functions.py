from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
import re

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text) 
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"Error: Cannot handle text type {text_node.text_type} of {text_node}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []
    for node in old_nodes:

        # skip all the nodes were the text type was already found
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        current_text = ""
        current_type = TextType.TEXT

        text_index = 0

        while text_index < len(node.text):

            if text_index + len(delimiter) < len(node.text):
                hit_delimiter = node.text[text_index:text_index+len(delimiter)] == delimiter
            else:
                hit_delimiter = False

            if hit_delimiter:
                if len(current_text) > 0:
                    new_node = TextNode(current_text, current_type)
                    new_nodes.append(new_node)
                    current_text = ""

                if current_type == TextType.TEXT:
                    current_type = text_type
                elif current_type == text_type:
                    current_type = TextType.TEXT

                text_index += len(delimiter)

            current_text += node.text[text_index]
            text_index += 1

        if len(current_text) > 0:
            new_node = TextNode(current_text.rstrip(delimiter), current_type)
            new_nodes.append(new_node)

    return new_nodes
                

def extract_markdown_images(text):
    markdown_images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return markdown_images
    
def extract_markdown_links(text):
    markdown_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return markdown_links


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        markdown_images = extract_markdown_images(node.text)
        if len(markdown_images) == 0:
            new_nodes.append(node)
            continue

        text_index = 0
        image_index = 0
        current_text = ""

        while text_index < len(node.text):
            
            image = markdown_images[image_index]
            alt_text = image[0]
            url = image[1]
            image_str = f"![{alt_text}]({url})"
            found_image_in_text = node.text[text_index:text_index + len(image_str)] == image_str
            
            if not found_image_in_text:
                current_text += node.text[text_index]
                text_index += 1
            elif found_image_in_text:
                if current_text != "":
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
                current_text = ""

                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                image_index += 1
                text_index += len(image_str)

                if image_index >= len(markdown_images) and node.text[text_index:] != "":
                    new_nodes.append(TextNode(node.text[text_index:], TextType.TEXT))
                    break

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        markdown_links = extract_markdown_links(node.text)
        if len(markdown_links) == 0:
            new_nodes.append(node)
            continue

        text_index = 0
        link_index = 0
        current_text = ""

        while text_index < len(node.text):
            
            link = markdown_links[link_index]
            alt_text = link[0]
            url = link[1]
            link_str = f"[{alt_text}]({url})"
            found_link_in_text = node.text[text_index:text_index + len(link_str)] == link_str
            
            if not found_link_in_text:
                current_text += node.text[text_index]
                text_index += 1
            elif found_link_in_text:
                if current_text != "":
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
                current_text = ""

                new_nodes.append(TextNode(alt_text, TextType.LINK, url))
                link_index += 1
                text_index += len(link_str)

                if link_index >= len(markdown_links) and node.text[text_index:] != "":
                    new_nodes.append(TextNode(node.text[text_index:], TextType.TEXT))
                    break

    return new_nodes


def text_to_textnodes(text):
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
