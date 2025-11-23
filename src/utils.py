from node import Node


def node_tree_to_dict(node: Node):
    if not node.children:
        return {}

    return {child.name: node_tree_to_dict(child) for child in node.children}


def dict_to_node_tree(tree_dict: dict) -> Node:
    root = Node("ROOT")

    def _dict_to_node_tree(subtree: dict, parent: Node):
        for key, value in subtree.items():
            node = Node(key)
            parent.add(node)

            if isinstance(value, dict) and len(value) > 0:
                _dict_to_node_tree(value, node)

    _dict_to_node_tree(tree_dict, root)
    return root