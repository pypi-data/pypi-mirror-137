def find_index(list_values, value, default_index):

    if value in list_values:
        return list_values.index(value)

    return default_index
