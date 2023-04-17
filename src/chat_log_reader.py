import pandas as pd
import re


def read_chat_logs(file_path):
    chat_data = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = re.match(r"\[(.*?) UTC\] (.*?): (.*)", line)
            if match:
                timestamp, username, message = match.groups()
                chat_data.append(
                    {"timestamp": timestamp, "username": username, "message": message}
                )

    # Convert the list of dictionaries into a DataFrame
    chat_logs = pd.DataFrame(chat_data)

    # Convert the timestamp column to a datetime object
    chat_logs["timestamp"] = pd.to_datetime(
        chat_logs["timestamp"], format="%Y-%m-%d %H:%M:%S"
    )

    return chat_logs
