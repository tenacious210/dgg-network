from src.chat_log_reader import read_chat_logs
from src.network_analyzer import analyze_chat_connections
from src.visualization import create_interactive_network_graph
from src.filters import filter_chat_logs
from src.export import export_data

import os
import glob
import pandas as pd
from bokeh.io import output_file, save
from datetime import datetime


def main(input_path, filters=None, export_format=None, export_path=None):
    # Check if the input path is a file or a directory
    if os.path.isfile(input_path):
        log_files = [input_path]
    elif os.path.isdir(input_path):
        log_files = glob.glob(os.path.join(input_path, "*.txt"))
    else:
        raise ValueError("Invalid input path")

    # Read and process chat logs from each file
    chat_logs = pd.concat(
        [read_chat_logs(file) for file in log_files], ignore_index=True
    )

    # Apply filters if any
    if filters:
        chat_logs = filter_chat_logs(chat_logs, **filters)

    # Analyze connections between users
    graph = analyze_chat_connections(chat_logs)

    # Create an interactive network graph
    plot = create_interactive_network_graph(graph)
    output_file(f"dgg_network_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
    save(plot)

    # Export the network graph and related data if needed
    if export_format and export_path:
        export_data(graph, file_format=export_format, file_path=export_path)


if __name__ == "__main__":
    input_path = "logs"
    filters = {"time_period": ("2023-04-01", "2023-04-02")}
    main(
        input_path,
        filters=filters,
        export_format="json",
        export_path="output/network_data",
    )
