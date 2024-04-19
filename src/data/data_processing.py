import pandas as pd
import json

def load_gpt_conversation_data(total_path):
    
    with open(total_path, 'r') as f:
        conversations = pd.DataFrame(json.load(f))

    conversations['create_time'] = pd.to_datetime(conversations["create_time"], unit='s').dt.floor('S')
    conversations['update_time'] = pd.to_datetime(conversations["update_time"], unit='s').dt.floor('S')
    conversations.groupby(conversations["update_time"].dt.date).get_group(pd.to_datetime("2024-03-17").date())
    select_columns = ["title", "create_time", "create_time", "mapping", "conversation_id"]
    conversations = conversations[select_columns]
    return conversations

def extract_message_history(conversations, conversation_id):
    """
    Extracts the message history for a given conversation ID from the conversations DataFrame.

    Args:
        conversations (DataFrame): The DataFrame containing the conversations data.
        conversation_id (str): The ID of the conversation to extract the message history for.

    Returns:
        DataFrame: A DataFrame containing the extracted message history for the specified conversation ID.
    """
    def is_list_with_empty_string(obj):
        # Check if obj is a list, has exactly one element, and that element is an empty string
        return isinstance(obj, list) and len(obj) == 1 and obj[0] == ''

    select = conversations["conversation_id"] == conversation_id
    mapping = conversations[select]["mapping"].values[0]

    messages = []

    for message_ID, message_Data in mapping.items():
        message_data = message_Data.get("message")  # Use .get() to safely access "message"
        if message_data is not None:
            try:
                # Safely access "content" and then "parts" using .get(), defaulting to None if not found
                parts = message_data.get("content", {}).get("parts", None)
                if parts is not None and not is_list_with_empty_string(parts) and isinstance(parts[0], str):
                    message = {
                        "message_id": message_Data.get("id"),  # Assume .get() usage is correct here
                        "author": message_data.get("author", {}).get("role"),  # Safe access
                        "create_time": message_data.get("create_time"),  # Assume this is always present
                        "update_time": message_data.get("update_time"),  # Assume this is always present
                        "content": parts[0]  # Now ensured to be a string
                    }
                    messages.append(message)
            except KeyError:
                continue  # Explicitly skip to the next iteration

    conversation = pd.DataFrame(messages)
    conversation['conversation_id'] = conversation_id
    conversation['title'] = conversations[select]["title"].values[0]
    conversation['create_time'] = pd.to_datetime(conversation["create_time"], unit='s').dt.floor('S')
    conversation['update_time'] = pd.to_datetime(conversation["update_time"], unit='s').dt.floor('S')
    return conversation

def extract_total_message_history(conversations):
    total_message_history = []
    for conversation_id in conversations["conversation_id"].values:
        message_history = extract_message_history(conversations, conversation_id)
        total_message_history.append(message_history)

    total_message_history = pd.concat(total_message_history, axis=0).reset_index(drop=True)
    return total_message_history