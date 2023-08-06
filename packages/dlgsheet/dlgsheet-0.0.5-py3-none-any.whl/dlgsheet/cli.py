from optparse import OptionParser
import os
from pathlib import Path

from dlgsheet import config
from dlgsheet.logger import logger, levels, setLoggerLevel
from dlgsheet.gsheet.api import set_credentials
from dlgsheet.download_data import download_table_values, download_all_tables


usage = "usage: %prog [options] tablename"
parser = OptionParser(usage=usage, prog="dlgsheet")
parser.add_option("-l", "--log-level", dest="loglevel",
                  help="set log level. Available options: " + ",".join(levels))
parser.add_option("-c", "--credentials-file", dest="credentials",
                  help="set credentials file name", metavar="FILE")
parser.add_option("-o", "--output-file", dest="output",
                  help="save to output file", metavar="FILE")
parser.add_option("-d", "--output-folder", dest="output_folder",
                  help="save to output folder", metavar="FOLDER")
parser.add_option("-s", "--spreadsheet-id", dest="spreadsheetid",
                  help="set google spreadsheet id to write on")
parser.add_option("-t", "--sheetname", dest="sheetname",
                  help="set google sheetname to write on")
parser.add_option("-k", "--key-index", type="int", dest="key_index",
                  help="set key index to generate object related to it")

parser.add_option("-K", "--use-keys-table", action="store_true",
                  dest="use_keys_table",
                  default=False, help="use keys table in spreadsheet")

parser.add_option("-T", "--keys-table",
                  dest="keys_table",
                  help="keys table name in spreadsheet. Default '_keys'")

parser.add_option("-n", "--tablename-column",
                  dest="tablename_column",
                  help="tablename column in keys table. Default 'tablename'")

parser.add_option("-i", "--key-index-column",
                  dest="key_index_column",
                  help="key index column in keys table. Default 'key_index'")


# Reference https://stackoverflow.com/a/29301200/5107192
def get_comma_separated_args(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))


parser.add_option(
    "-B",
    "--blacklist",
    type="string",
    action='callback',
    callback=get_comma_separated_args,
    dest="blacklist",
    help="list of tables that won't be considered, separated by commas. Default '_keys'")


def validate_index(index):

    if index is not None:
        try:
            index = int(index)
        except Exception as e:
            logger.error(f"Entered index '{index}' is not an integer.")
            exit(-1)
    return index


def main():

    (options, _) = parser.parse_args()

    if options.loglevel is not None:
        loglevel = options.loglevel
    else:
        loglevel = "info"

    setLoggerLevel(loglevel)

    logger.debug(options)

    DEFAULT_FOLDER_NAME = "output"

    if(options.spreadsheetid is not None):
        spreadsheetid = options.spreadsheetid
    else:
        spreadsheetid = config.google["spreadsheetid"]

    if(not spreadsheetid):
        logger.error(
            '''No spreadsheetid defined, either via option --spreadsheet-id or
            environment variable GOOGLE_SPREADSHEET_ID.''')
        exit(-1)

    if(options.credentials is not None):
        credentials = options.credentials
        auth = set_credentials(credentials)
    else:
        credentials = config.google["credentialsfile"]
        logger.warning("No credentials file defined, usign default: " +
                       credentials)
        if(not Path(credentials).exists()):
            logger.error(
                "Default credentials file doesn't exist, skipping. "
                "Download the credentials file and save as 'key.json' "
                "or specify the name by the --credentials-file option."
            )
            exit(-1)
        auth = set_credentials(credentials)

    if(options.sheetname is not None):

        sheetname = options.sheetname
        defaultfilename = os.path.join(
            DEFAULT_FOLDER_NAME, sheetname + ".json")

        if(options.output is not None):
            filename = options.output
        else:
            filename = defaultfilename
            logger.warning(
                "Not file name provided via --output-file. Usign default: " +
                filename)

        logger.info("Downloading data from spreadsheet: " +
                    spreadsheetid + " from '" +
                    sheetname + "' to " + filename)

        key_index = validate_index(options.key_index)
        if key_index is not None:
            logger.info(f"Using key index {key_index} for selected table.")

        download_table_values(sheetname, filename=filename,
                              spreadsheetid=spreadsheetid, credentials=auth,
                              key_index=key_index)

        logger.info("Task finished")
        exit(0)

    if(options.output_folder is not None):
        foldername = options.output_folder
    else:
        foldername = DEFAULT_FOLDER_NAME
        logger.warning(
            "Not folder name provided via --output-folder. Usign default: " +
            foldername)

    logger.info("Downloading data from spreadsheet: " +
                spreadsheetid + " to folder " + foldername)

    blacklist = options.blacklist
    if blacklist is not None:
        logger.info(f"Blacklisting sheets: {blacklist}")

    if(options.use_keys_table):

        logger.info("Using keys table in spreadsheet to set keys to tables")

        download_all_tables(foldername=foldername,
                            blacklist=blacklist,
                            spreadsheetid=spreadsheetid,
                            credentials=auth,
                            use_keys_table=options.use_keys_table,
                            keys_table=options.keys_table,
                            tablename_column=options.tablename_column,
                            key_index_column=options.key_index_column)

    else:

        key_index = validate_index(options.key_index)

        if key_index is not None:
            logger.info(f"Using key index {key_index} for all tables.")

        download_all_tables(foldername=foldername,
                            blacklist=blacklist,
                            spreadsheetid=spreadsheetid,
                            credentials=auth,
                            key_index=key_index)

    logger.info("Task finished")
