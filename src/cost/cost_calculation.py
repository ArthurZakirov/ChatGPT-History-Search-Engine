def calculate_gpt_api_cost(total_message_history):
    """
    Calculates the monthly cost of using the GPT API based on the total message history.

    Args:
        total_message_history (DataFrame): The total message history containing the conversation data.

    Returns:
        float: The monthly cost in euros.

    """
    tokens_per_word = 1000 / 750
    dollar_per_input_token = 10.00 / 10e5
    dollar_per_output_token = 30.00 / 10e5
    euro_per_dollar = 0.93
    days_per_month = 30

    total_user_words = (
        total_message_history.groupby("author")
        .get_group("user")["content"]
        .apply(lambda x: len(x.split(" ")))
        .sum()
    )
    total_assistant_words = (
        total_message_history.groupby("author")
        .get_group("assistant")["content"]
        .apply(lambda x: len(x.split(" ")))
        .sum()
    )

    input_cost = dollar_per_input_token * tokens_per_word * total_user_words
    output_cost = dollar_per_output_token * tokens_per_word * total_assistant_words

    delta_time = (
        total_message_history["create_time"][0]
        - total_message_history["create_time"].loc[len(total_message_history) - 1]
    )

    total_cost = input_cost + output_cost
    cost_per_day = total_cost / delta_time.days

    euro_cost_per_day = euro_per_dollar * cost_per_day
    euro_cost_per_month = days_per_month * euro_cost_per_day
    return euro_cost_per_month
