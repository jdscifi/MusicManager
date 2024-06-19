def delete_key_recursive(d, key):
    if isinstance(d, dict):
        # Check if the key exists in the dictionary and delete it
        if key in d:
            d.pop(key)
        # Recursively call the function for each value in the dictionary
        for k in list(d.keys()):  # use list() to avoid RuntimeError due to dictionary size change
            d[k] = delete_key_recursive(d[k], key)
    elif isinstance(d, list):
        # If the value is a list, recursively call the function for each item in the list
        for i in range(len(d)):
            d[i] = delete_key_recursive(d[i], key)
    return d