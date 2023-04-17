import networkx as nx
import re
from tqdm import tqdm
import pandas as pd


def tokenize_message(message) -> list[str]:
    """
    Tokenizes a message into words using regex.
    """
    words = re.findall(r"\b\w+\b", message)
    return words


def analyze_chat_connections(chat_logs: pd.DataFrame) -> nx.Graph:
    """
    Analyzes connections between users in the chat.
    """
    # Create an empty graph
    graph = nx.Graph()

    # Add users as nodes in the graph
    for user in chat_logs["username"].unique():
        graph.add_node(user)

    # Analyze connections between users
    unique_usernames = chat_logs["username"].unique()
    for index, row in tqdm(
        chat_logs.iterrows(), total=len(chat_logs), desc="Analyzing connections"
    ):
        user = row["username"]
        message = row["message"]

        # Check if any of the unique usernames appear in the message
        for mentioned_user in unique_usernames:
            if mentioned_user in message and mentioned_user != user:
                # If a connection exists between the users, increment the weight by 1
                if graph.has_edge(user, mentioned_user):
                    graph[user][mentioned_user]["weight"] += 1
                else:
                    # Otherwise, add a new edge with a weight of 1
                    graph.add_edge(user, mentioned_user, weight=1)

    return graph
