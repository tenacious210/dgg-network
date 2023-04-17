def filter_chat_logs(chat_logs, username=None, message_content=None, time_period=None):
    if username:
        chat_logs = chat_logs[chat_logs["username"] == username]
    if message_content:
        chat_logs = chat_logs[chat_logs["message"].str.contains(message_content)]
    if time_period:
        chat_logs = chat_logs[
            (chat_logs["timestamp"] >= time_period[0])
            & (chat_logs["timestamp"] <= time_period[1])
        ]

    return chat_logs
