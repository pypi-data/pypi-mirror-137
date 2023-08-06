import os
from dotenv import load_dotenv

load_dotenv()

google = {
    "spreadsheetid": os.getenv("GOOGLE_SPREADSHEET_ID"),
    "credentialsfile": os.getenv("GOOGLE_AUTH_FILENAME", "key.json"),
    "scopes": ['https://www.googleapis.com/auth/spreadsheets']
}

blacklist = ["_keys"]

keys_table = {
    "name": "_keys",
    "columns": {
        "tablename": {
            "name": "tablename",
            "default_index": 0
        },
        "key_index": {
            "name": "key_index",
            "default_index": 1
        }
    }
}
