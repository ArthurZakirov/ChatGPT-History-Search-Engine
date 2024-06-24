def search_dataframe(df, keyword):
    # Convert keyword to lowercase to make the search case-insensitive
    keyword_pattern = keyword.lower()
    # Use str.contains with regex to find the keyword or its parts in 'title' and 'content' columns, case insensitive
    mask = df["title"].str.contains(keyword_pattern, case=False, na=False) | df[
        "content"
    ].str.contains(keyword_pattern, case=False, na=False)
    # Return the slice of the dataframe where the condition is True
    return df[mask]
