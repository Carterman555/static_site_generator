from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        eq_text = self.text == other.text
        eq_text_type = self.text_type == other.text_type
        eq_url = self.url == other.url
        return eq_text and eq_text_type and eq_url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"