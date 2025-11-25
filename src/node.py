class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = []

    def add(self, child_node):
        self.children.append(child_node)
        child_node.parent = self

    def remove(self, child_node):
        self.children.remove(child_node)
        child_node.parent = None

    def is_leaf(self):
        return len(self.children) == 0

    def get_all_leaves(self):
        leaves = []
        def _get_all_leaves(node):
            if node.is_leaf():
                leaves.append(node)
            else:
                for child in node.children:
                    _get_all_leaves(child)
        _get_all_leaves(self)
        return leaves

    def get_path_to_root(self):
        path = []
        node = self
        while node is not None:
            path.append(node.name)
            node = node.parent
        return list(reversed(path))
