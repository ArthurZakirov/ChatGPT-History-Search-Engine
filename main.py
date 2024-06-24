import pandas as pd
import os
import matplotlib.pyplot as plt
import argparse
from src.data.data_utils import search_dataframe
from src.data.data_processing import (
    load_gpt_conversation_data,
    extract_total_message_history,
)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--search_term",
    type=str,
    help="The keyword to search for in the data",
    default="Food",
)
parser.add_argument(
    "--raw_data_dir",
    type=str,
    help="The path to the dir containing the raw data",
    default="data/raw/b317249d9bfd293ab8aeec43fb616fa6792bbaa639f574d45e0fe65fa89eb9d7-2024-06-24-10-46-26",
)
parser.add_argument(
    "--output_path",
    type=str,
    help="The path to the dir containing the output data",
    default="outputs/search_results.csv",
)
args = parser.parse_args()


def main():
    raw_data_path = os.path.join(args.raw_data_dir, "conversations.json")
    conversations = load_gpt_conversation_data(raw_data_path)
    total_message_history = extract_total_message_history(conversations)
    search_df = search_dataframe(total_message_history, args.search_term)
    search_df.to_csv(args.output_path, index=False)

    print(f"Search results saved to {args.output_path}")
    print(search_df)


if __name__ == "__main__":
    main()
