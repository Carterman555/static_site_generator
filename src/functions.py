from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from blocktype import BlockType
import re
import os
import shutil

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

    for node in nodes:
        node.text = node.text.replace("\n", " ")

    return nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    new_blocks = []
    for block in blocks:
        new_block = block.strip()
        if new_block != "":
            new_blocks.append(new_block)

    return new_blocks


def block_to_block_type(block):
    headings = ["# ", "## ", "### ", "#### ", "##### ", "###### "]
    for heading in headings:
        if block.startswith(heading):
            return BlockType.HEADING
    
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    lines = block.splitlines()

    lines_with_carrot = list(filter(lambda line: line.startswith(">"), lines))
    all_lines_have_carrot = len(lines) == len(lines_with_carrot)
    if all_lines_have_carrot:
        return BlockType.QUOTE

    lines_with_dash = list(filter(lambda line: line.startswith("- "), lines))
    all_lines_have_dash = len(lines) == len(lines_with_dash)
    if all_lines_have_dash:
        return BlockType.UNORDERED_LIST

    is_ordered_list = True
    for index, line in enumerate(lines):
        line_num = index + 1
        if not line.startswith(f"{line_num}."):
            is_ordered_list = False

    if is_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown, debug=False):

    def dprint(s):
        if debug:
            print(s)

    div_node = ParentNode("div", [])

    blocks = markdown_to_blocks(markdown)
    for block in blocks:

        block_type = block_to_block_type(block)
        parent_node = None

        match block_type:
            case BlockType.PARAGRAPH:
                parent_node = ParentNode("p", [])

                textnodes = text_to_textnodes(block)
                for node in textnodes:
                    leaf_node = text_node_to_html_node(node)
                    parent_node.children.append(leaf_node)

            case BlockType.HEADING:
                # Count number of '#' for heading level
                level = len(block.split(" ")[0])
                parent_node = ParentNode(f"h{level}", [])

                title_text = block.split(" ", 1)[1] # what comes after the '# '
                textnodes = text_to_textnodes(title_text)
                for node in textnodes:
                    leaf_node = text_node_to_html_node(node)
                    parent_node.children.append(leaf_node)

            case BlockType.CODE:
                code_node = LeafNode("code", block.strip("```").strip("\n"))
                parent_node = ParentNode("pre", [code_node])

            case BlockType.QUOTE:
                parent_node = ParentNode("blockquote", [])

                quote_text = block.replace("\n>", " ").lstrip(">") # what comes after the '>'
                textnodes = text_to_textnodes(quote_text)
                for node in textnodes:
                    leaf_node = text_node_to_html_node(node)
                    parent_node.children.append(leaf_node)

            case BlockType.UNORDERED_LIST:
                parent_node = ParentNode("ul", [])

                lines = block.splitlines()

                for line in lines:
                    textnodes = text_to_textnodes(line)
                    list_item_parent = ParentNode("li", [])

                    for i, node in enumerate(textnodes):
                        leaf_node = text_node_to_html_node(node)

                        if i == 0:
                            leaf_node.value = leaf_node.value[2:]

                        list_item_parent.children.append(leaf_node)
                        
                
                    parent_node.children.append(list_item_parent)

            case BlockType.ORDERED_LIST:
                parent_node = ParentNode("ol", [])

                lines = block.splitlines()

                for line in lines:
                    textnodes = text_to_textnodes(line)
                    list_item_parent = ParentNode("li", [])

                    for i, node in enumerate(textnodes):
                        leaf_node = text_node_to_html_node(node)

                        if i == 0:
                            leaf_node.value = leaf_node.value[3:]

                        list_item_parent.children.append(leaf_node)
                        
                
                    parent_node.children.append(list_item_parent)
            case _:
                raise Exception(f"Error: cannot handle block type {block_type} for {block}")

        

        div_node.children.append(parent_node)

    return div_node


def extract_title(markdown):
    if markdown.startswith("# "):
        start_index = 2
    else:
        start_index = markdown.find("\n# ") + 3

        no_heading = start_index == 2
        if no_heading:
            raise Exception(f"Error: Cannot find heading in markdown {markdown}")
    
    
    
    end_index = start_index
    while end_index < len(markdown) and markdown[end_index] != "\n":
        end_index += 1

    return markdown[start_index:end_index]


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path}")

    with open(from_path) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    md_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", md_html)
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

    dest_only_path, file = os.path.split(dest_path)

    if not os.path.exists(dest_only_path):
        os.makedirs(dest_only_path)

    with open(dest_path, "w") as f:
        f.write(full_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):

    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isdir(item_path):
            new_dest_dir_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(item_path, template_path, new_dest_dir_path, basepath)
        elif item.endswith(".md"):
            html_item = f"{item[:-3]}.html"
            dest_path = os.path.join(dest_dir_path, html_item)
            generate_page(item_path, template_path, dest_path, basepath)
        else:
            raise Exception(f"Error: item is not dir or markdown file: {item_path}")
