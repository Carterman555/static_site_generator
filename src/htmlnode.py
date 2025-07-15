class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html_str = ""
        for prop, prop_value in self.props.items():
            html_str += f' {prop}="{prop_value}"'
        return html_str

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props_to_html()})"

