import json
import networkx as nx
from networkx.readwrite import json_graph
from typing import Union


def export_data(
    graph: nx.Graph, file_format: str = "json", file_path: str = "output"
) -> Union[None, str]:
    """
    Exports the network graph and related data to the specified format.
    """
    if file_format == "json":
        data = json_graph.node_link_data(graph)
        with open(file_path + ".json", "w") as outfile:
            json.dump(data, outfile)
    elif file_format == "png" or file_format == "pdf":
        # Your logic to export the graph as PNG or PDF using Matplotlib or another library
        return "PNG and PDF export functionality is not implemented yet."
    else:
        raise ValueError(
            f"Invalid file format '{file_format}'. Supported formats are 'json', 'png', and 'pdf'."
        )
