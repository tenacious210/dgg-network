import networkx as nx
from bokeh.io import output_file, save
from bokeh.plotting import from_networkx, figure
from bokeh.models import HoverTool, MultiLine, Circle, LabelSet, ColumnDataSource
from typing import Tuple
from datetime import datetime


def create_interactive_network_graph(
    graph: nx.Graph, plot_dimensions: Tuple[int, int] = (800, 800)
) -> figure:
    """
    Creates an interactive network graph using Bokeh.
    """
    # Set the output file name
    output_file(f"dgg_network_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

    # Create a mapping of the original node names to integer values
    node_mapping = {name: i for i, name in enumerate(graph.nodes)}
    # Create a new graph with integer node names
    int_graph = nx.relabel_nodes(graph, node_mapping)

    # Set up the plot dimensions
    plot_width, plot_height = plot_dimensions

    # Create a Bokeh plot with the specified dimensions
    plot = figure(
        title="DGG Chat Network",
        x_range=(-1.2, 1.2),
        y_range=(-1.2, 1.2),
        width=plot_width,
        height=plot_height,
        tools="pan,box_zoom,reset,save",
    )

    # Create a NetworkX layout for the graph
    pos = nx.spring_layout(int_graph)

    # Use the Bokeh 'from_networkx' function to create a Bokeh graph from the NetworkX graph
    bokeh_graph = from_networkx(int_graph, pos, scale=1, center=(0, 0))

    # Create a ColumnDataSource with the original node names and their connection count (degree)
    node_labels = {i: name for name, i in node_mapping.items()}
    connections = {i: int_graph.degree(i) for i in int_graph.nodes}
    source = ColumnDataSource(
        data=dict(
            index=list(node_labels.keys()),
            names=list(node_labels.values()),
            connections=list(connections.values()),
        )
    )

    # Replace the node renderer data source with the new one
    bokeh_graph.node_renderer.data_source = source

    # Add hover tooltips to display the user and connection count
    tooltips = [
        ("User", "@names"),
        ("Connections", "@connections"),
    ]
    plot.add_tools(HoverTool(tooltips=tooltips, renderers=[bokeh_graph.node_renderer]))

    # Customize the appearance of the nodes and edges
    bokeh_graph.node_renderer.glyph = Circle(size=15, fill_color="skyblue")
    bokeh_graph.edge_renderer.glyph = MultiLine(
        line_color="#CCCCCC", line_alpha=0.8, line_width=1
    )

    # Add the graph to the plot
    plot.renderers.append(bokeh_graph)

    return plot
