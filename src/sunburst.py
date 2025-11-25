import pandas as pd
import plotly.express as px
from node import Node


BASE_COLOR = (0, 0, 0)
OPACITY_VISIBLE = 1.0
OPACITY_HIDDEN = 0.0


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
        if self.df is None:
            self.create_data_frame()

        max_depth = self.df["path"].apply(len).max()
        for i in range(max_depth):
            col = f"level_{i}"
            if col not in self.df.columns:
                self.df[col] = self.df["path"].apply(lambda p, i=i: p[i] if i < len(p) else None)

        fig = px.sunburst(self.df, path=[f"level_{i}" for i in range(max_depth)], values="value")

        path_names = []
        cur = leaf

        while cur is not None and cur is not self.root:
            path_names.append(cur.name)
            cur = cur.parent
        leaf_path = tuple(reversed(path_names))

        trace_ids = list(fig.data[0].ids)
        trace_paths = [tuple(t.split("/")) for t in trace_ids]

        def is_prefix(prefix, full):
            if len(prefix) > len(full):
                return False
            return prefix == full[: len(prefix)]

        visible_flags = [is_prefix(tp, leaf_path) for tp in trace_paths]

        r, g, b = BASE_COLOR
        colors = [
            f"rgba({r},{g},{b},{OPACITY_VISIBLE if vis else OPACITY_HIDDEN})"
            for vis in visible_flags
        ]

        fig.update_traces(
            marker=dict(
                colors=colors,
                line=dict(width=0, color="rgba(0,0,0,0)")
            ),
            selector=dict(type="sunburst"),
            hovertemplate=None,
            textinfo="none",
            branchvalues="total"
        )

        return fig

    def build_all_single_leaf_diagrams(self):
        all_leaves = self.root.get_all_leaves()
        figs = []
        for leaf in all_leaves:
            figs.append(self.build_single_leaf_diagram(leaf))
        return figs