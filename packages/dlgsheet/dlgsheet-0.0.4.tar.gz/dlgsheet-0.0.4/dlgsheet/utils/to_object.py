from dlgsheet.logger import logger


def list_to_object(list_values, header):

    return dict(zip(header, list_values))


def nested_list_to_object(nested_list, header=None, key_index=None):

    if header is None:
        header = nested_list[0]
        nested_list = nested_list[1:]

    if key_index is None:
        return [list_to_object(list_values, header)
                for list_values in nested_list]

    if(key_index >= len(header)):
        logger.error(f"Key index {key_index} is out of range.")
        return None

    header.pop(key_index)
    result = {}

    for list_values in nested_list:

        key = list_values.pop(key_index)
        result[key] = list_to_object(list_values, header)

    return result
