import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import argparse
from src.data.data_utils import search_dataframe
from src.data.data_processing import load_gpt_conversation_data, extract_total_message_history
from src.cost.cost_calculation import calculate_gpt_api_cost

parser = argparse.ArgumentParser()
parser.add_argument("--raw_data_path", type=str, help="The path to the file containing the raw data", default="data/raw/b317249d9bfd293ab8aeec43fb616fa6792bbaa639f574d45e0fe65fa89eb9d7-2024-03-17-08-56-18/conversations.json")
args = parser.parse_args()

def main():
    conversations = load_gpt_conversation_data(args.raw_data_path)
    total_message_history = extract_total_message_history(conversations)
    search_df = search_dataframe(df=total_message_history, keyword="content_type")
    cost = calculate_gpt_api_cost(total_message_history)

    print(search_df)
    print(cost)

if __name__ == "__main__":
    main()

