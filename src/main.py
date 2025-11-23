from sunburst import SunburstBuilder
from utils import dict_to_node_tree, node_tree_to_dict


def main():
    hierarchy = {
        "1": {
            "1.1": {
                "1.1.1": {},
                "1.1.2": {},
            },
            "1.2": {
                "1.2.1": {},
                "1.2.2": {},
                "1.2.3": {},
            }
        },
        "2": {
            "2.1": {},
            "2.2": {
                "2.2.1": {},
            }
        }
    }

    tree = dict_to_node_tree(hierarchy)
    sb = SunburstBuilder(tree)

    # normal diagram
    fig = sb.build_normal_diagram()
    fig.show()

    # diagram for each path
    figs = sb.build_all_single_leaf_diagrams()
    for fig in figs:
        fig.show()


if __name__ == "__main__":
    main()
