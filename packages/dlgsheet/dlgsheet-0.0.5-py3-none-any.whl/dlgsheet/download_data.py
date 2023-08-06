from pathlib import Path

from dlgsheet.gsheet.api import get_tables, get_table_values
from dlgsheet.utils.to_object import nested_list_to_object
from dlgsheet.utils.list import find_index
from dlgsheet.logger import logger
from dlgsheet.save_data import save_to_json_file
from dlgsheet import config


def download_table_values(sheetname, filename=None, spreadsheetid=None,
                          credentials=None, key_index=None):

    sheets = get_tables(spreadsheetid=spreadsheetid, credentials=credentials)

    if (sheetname not in sheets):
        logger.error("sheet '" + sheetname +
                     "' not in spreadsheet.")
        return exit(-1)

    data = get_table_values(sheetname, spreadsheetid=spreadsheetid,
                            credentials=credentials)

    l_obj = nested_list_to_object(data["values"], key_index=key_index)

    if(l_obj is None):
        logger.error("Cannot save data of specified table, check your "
                     "configuration.")
    if (filename is None):
        filename = sheetname + ".json"

    save_to_json_file(l_obj, filename)


def get_keys_table_info(sheets, keys_table=None,
                        tablename_column=None,
                        key_index_column=None,
                        spreadsheetid=None,
                        credentials=None):

    keys_table_info = config.keys_table
    if keys_table is not None:
        keys_table_info["name"] = keys_table
    else:
        logger.warning("Not keys table specified, using default "
                       + keys_table_info["name"])

    if keys_table_info["name"] not in sheets:
        logger.error(
            f"Specified keys table '{keys_table_info['name']}' not found in spreadsheet")
        return None
    else:
        tablename_column_info = keys_table_info["columns"]["tablename"]
        key_index_column_info = keys_table_info["columns"]["key_index"]
        if tablename_column is not None:
            tablename_column_info["name"] = tablename_column

        if key_index_column is not None:
            key_index_column_info["name"] = key_index_column

        keys_data = get_table_values(
            keys_table_info["name"],
            spreadsheetid=spreadsheetid,
            credentials=credentials)["values"]

        header = keys_data.pop(0)

        tablename_column_info["index"] = find_index(
            header,
            tablename_column_info["name"],
            tablename_column_info["default_index"])

        key_index_column_info["index"] = find_index(
            header,
            key_index_column_info["name"],
            key_index_column_info["default_index"])

        keys_data = list(zip(*keys_data))

        if tablename_column_info["index"] >= len(keys_data):
            logger.error(f"Index {tablename_column_info['index']} for "
                         "tablename is out of range ")
            return None

        if key_index_column_info["index"] >= len(keys_data):
            logger.error(f"Index {key_index_column_info['index']} for "
                         "key_index is out of range ")
            return None

        tablename_column_info["data"] = keys_data[
            tablename_column_info["index"]]

        key_index_column_info["data"] = keys_data[
            key_index_column_info["index"]]

        keys_table_info["columns"]["tablename"] = tablename_column_info
        keys_table_info["columns"]["key_index"] = key_index_column_info

        logger.debug(f"Keys table info: {keys_table_info}")
        return keys_table_info


def download_all_tables(
        foldername,
        blacklist=None,
        spreadsheetid=None,
        credentials=None,
        key_index=None,
        use_keys_table=False,
        keys_table=None,
        tablename_column=None,
        key_index_column=None):

    folder = Path(foldername)

    if blacklist is None:
        blacklist = config.blacklist

    sheets = get_tables(spreadsheetid=spreadsheetid, credentials=credentials)

    keys_table_info = None
    if use_keys_table:
        keys_table_info = get_keys_table_info(
            sheets,
            keys_table=keys_table,
            tablename_column=tablename_column,
            key_index_column=key_index_column,
            spreadsheetid=spreadsheetid,
            credentials=credentials
        )

        if keys_table_info is None:
            logger.error(f"Cannot use specified table "
                         "as table info, please check the configuration, "
                         "or use the default mode with no keys.")
            exit(-1)

    for sheetname in sheets:

        if sheetname in blacklist:
            continue

        filename = sheetname + ".json"
        save_filename = folder / filename

        logger.info(
            "Downloading table '" +
            sheetname +
            "' to " +
            str(save_filename))

        data = get_table_values(sheetname, spreadsheetid=spreadsheetid,
                                credentials=credentials)

        key_index = None
        if use_keys_table and keys_table_info is not None:
            if sheetname in keys_table_info["columns"]["tablename"]["data"]:
                idx = keys_table_info["columns"]["tablename"]["data"].index(
                    sheetname)
                key_index = keys_table_info["columns"]["key_index"]["data"][idx]
                logger.info(f"Using index {key_index} for table '{sheetname}'")

        l_obj = nested_list_to_object(data["values"], key_index=key_index)

        if(l_obj is None):
            logger.error("Cannot save data of specified table, check your "
                         "configuration.")
            continue

        save_to_json_file(l_obj, save_filename)


if __name__ == "__main__":
    download_all_tables("output")
