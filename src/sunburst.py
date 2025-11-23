import pandas as pd
import plotly.express as px
from node import Node


class SunburstBuilder:

    def __init__(self, root: Node):
        self.root = root
        self.df = None

    def create_data_frame(self):
        rows = []

        def _create_data_frame(node: Node, path):
            if node.is_leaf():
                rows.append({"path": path, "value": 1})
                return

            for child in node.children:
                _create_data_frame(child, path + [child.name])

        for child in self.root.children:
            _create_data_frame(child, [child.name])

        self.df = pd.DataFrame(rows)

    def build_normal_diagram(self):
        if self.df is None:
            self.create_data_frame()

        max_depth = self.df["path"].apply(len).max()

        for i in range(max_depth):
            self.df[f"level_{i}"] = self.df["path"].apply(
                lambda p, i=i: p[i] if i < len(p) else None
            )

        fig = px.sunburst(
            self.df,
            path=[f"level_{i}" for i in range(max_depth)],
            values="value"
        )

        fig.update_traces(
            hovertemplate=None,
            textinfo='none'
        )

        return fig

    def build_single_leaf_diagram(self, leaf: Node):
        # TODO
        fig = px.sunburst()
        return fig

    def build_all_single_leaf_diagrams(self):
        all_leaves = self.root.get_all_leaves
        figs = []
        for leaf in all_leaves:
            figs.append(self.build_single_leaf_diagram(leaf))
        return figs