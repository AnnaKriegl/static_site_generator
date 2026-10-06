
class HTMLNode:
    def __init__(self, tag : str | None = None, value : str | None = None, children : list[HTMLNode] | None = None, props : dict[str, str] | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props    
        
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html = ''
        if self.props is None or '':
            return html
        for key, value in self.props.items():
            html += f' {key}="{value}"'
        return html

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'


class LeafNode(HTMLNode):
    def __init__(self, tag : str | None, value : str, props : dict[str, str] | None = None):
        super(LeafNode, self).__init__()
        self.tag = tag
        self.value = value
        self.props = props   

    def to_html(self):
        if not self.value:
            raise ValueError('Input "value" is missing')
        if not self.tag:
            return self.value
        html = ''
        html += f'<{self.tag}{ self.props_to_html()}>'
        html += f'{self.value}</{self.tag}>'
        return html

    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'


class ParentNode(HTMLNode):
    def __init__(self, tag : str | None, children : list[HTMLNode] | None, props : dict[str, str] | None = None):
        self.tag = tag
        self.children = children
        self.props = props  

    def to_html(self):
        if not self.tag:
            raise ValueError('Input "tag" is missing.')
        if not self.children:
            raise ValueError('Input "children" is missing.')
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
    

