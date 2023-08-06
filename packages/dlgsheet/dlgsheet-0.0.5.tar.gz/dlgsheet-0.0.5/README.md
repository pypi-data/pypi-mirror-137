# Python script for downloading sheets from Google Sheets as JSON files

## Requirements

**NOTE** This information is taken from the google-api documentation for Python
 from: https://github.com/googleapis/google-api-python-client/blob/master/docs/oauth-server.md

### Create a service account

Service accounts allow you to perform server to server, app-level authentication using a robot account. You will create a service account, download a keyfile, and use that to authenticate to Google APIs. To create a service account:

- Go to the [Create Service Account Key page](https://console.cloud.google.com/apis/credentials/serviceaccountkey)
- Click the button `Create new service account` 
- Enter the service account name and the corresponding id.
- Add the additional information regarding users and project permissions
	(optional)
- Create the service account.

Once it is created you should create a keyfile, then follow the next steps:
- Enter to the newly created service account
- Go to the `Keys` tab
- Click the button `Add key` and select `JSON`.

Save the service account credential file somewhere safe, and do not check this file into source control!

### Add permissions to the document

If you want to perform operations in a private file, you should add the service
mail (e.g. service-name@project-name.iam.gserviceaccount.com) to the list of
shared users in your document.

You can read this reference which explains this specific requirement:
https://github.com/juampynr/google-spreadsheet-reader


## Installation

To install this package you must build and install following the procedure
suggested for setuptools https://setuptools.readthedocs.io/en/latest/userguide/quickstart.html.

```
pip install --upgrade setuptools
python -m build .
python install .
```

You can also use the scrip from the current source by:
```
pip install -r requirements.txt
```

## How to use

The script could be used installed in your local environment, or directly from the
location of the package source.

If you have installed it, the command name is `dlgsheet` and admits the next
options:

```
dlgsheet [options]
```

**Options:**

* `-h, --help`

  Show this help message and exit

* `-l LOGLEVEL, --log-level=LOGLEVEL`

  Set log level. Available options: critical, error, warning, info, debug

* `-c FILE, --credentials-file=FILE`

  Set credentials file name

* `-o FILE, --output-file=FILE`

  Save to output file

* `-d FOLDEr, --output-folder=FOLDER`

  Save to output folder

* `-s SPREADSHEETID, --spreadsheet-id=SPREADSHEETID`

  Set google spreadsheet id to write on

* `-t SHEETNAME, --sheetname=SHEETNAME`

  Set google sheetname to write on

* `-k KEY_INDEX, --key-index=KEY_INDEX`

  Set key index to generate object related to it

* `-K, --use-keys-table`

  Use keys table in spreadsheet

* `-T KEYS_TABLE, --keys-table=KEYS_TABLE`

  Keys table name in spreadsheet. Default '_keys'

* `-n TABLENAME_COLUMN, --tablename-column=TABLENAME_COLUMN`

  Tablename column in keys table. Default 'tablename'

* `-i KEY_INDEX_COLUMN, --key-index-column=KEY_INDEX_COLUMN`

  Key index column in keys table. Default 'key_index'

* `-B BLACKLIST, --blacklist=BLACKLIST`

  List of tables that won't be considered, separated by commas. Default '_keys'

From these options, providing the `--spreadsheet-id` is mandatory either via the
command line or via an environmental variable `GOOGLE_SPREADSHEET_ID`.

Then, it is required also that you provide the key file downloaded from the Google
service account, explained above. It should be defined via the option
`--credentials-file`, otherwise it will use the default filename `key.json`,
which should be located in the current path where the script is executed.

There are some environment which may be employed to define some options:

| Variable                | Default          |
| -------------           | ---------------- |
| `GOOGLE_SPREADSHEET_ID` | (none)           |
| `GOOGLE_AUTH_FILENAME`  | key.json         |

You have two options to use this software: 

* **Downloading all the sheets**. When using with no arguments, it employs the
    default folder name `output` and saves the sheets in JSON files under this
    folder with the name `<sheetname>.json`.

* **Downloading single sheet**. When `sheetname` is defined, then uses this
    mode downloading only the specified sheet.

In addition to this, when the output filename is not defined via `--output`, the default filename used is a construction of:
`output/<sheetname>.json`, where `sheetname` is the sheet name in the Google
spreadsheet. Similarly, when the output folder is not defined via
`--output-folder`, the default folder name is `output` under the current
directory where the script is launched.


In case you are using the script from the source folder, you can call it via:
```
python -m dlgsheet [options] 
```

Where `[options]` are the options described above.

In case you have installed, it automatically installs a script to the system
path, so you can call as:
```
dlgsheet [options] 
```

## Use cases

### Single sheet

```
dlgsheet --sheetname SHEETNAME 
```

Using in a spreadsheet which has a  `SHEETNAME` sheet  with the following
values:

| key_1     | key_2     | key_3     |
| --------- | --------- | --------- |
| value_1_1 | value_1_2 | value_1_3 |
| value_2_1 | value_2_2 | value_2_3 |
| value_3_1 | value_3_2 | value_3_3 |

The results will be a file with the name `SHEETNAME.json` in the folder
`output`, with the following info:

```
[
    {
        "key_1": "value_1_1",
        "key_2": "value_1_2",
        "key_3": "value_1_3"
    },
    {
        "key_1": "value_2_1",
        "key_2": "value_2_2",
        "key_3": "value_2_3"
    },
    {
        "key_1": "value_3_1",
        "key_2": "value_3_2",
        "key_3": "value_3_3"
    }
]
```

### Single sheet with key index

```
dlgsheet --sheetname SHEETNAME --key-index 0
```

Using in a spreadsheet which has a  `SHEETNAME` sheet  with the following
values:

| key_1     | key_2     | key_3     |
| --------- | --------- | --------- |
| value_1_1 | value_1_2 | value_1_3 |
| value_2_1 | value_2_2 | value_2_3 |
| value_3_1 | value_3_2 | value_3_3 |

The results will be a file with the name `SHEETNAME.json` in the folder
`output`, with the following info:

```
{
    "value_1_1": {
        "key_2": "value_1_2",
        "key_3": "value_1_3"
    },
    "value_2_1": {
        "key_2": "value_2_2",
        "key_3": "value_2_3"
    },
    "value_3_1": {
        "key_2": "value_3_2",
        "key_3": "value_3_3"
    }
}
```

### All sheets in spreadsheet

```
dlgsheet 
```

It saves all the sheets except those in the blacklist, by default '_keys'. The
data is saved to the folder `output` with one file for each sheet.


### All sheets in spreadsheet with key index

```
dlgsheet  --key-index 0
```

It saves all the sheets except those in the blacklist, by default '_keys'. The
data is saved to the folder `output` with one file for each sheet, but in this
case uses the column index 0 to obtain the object for all the sheets. If the
index is out of the range in a sheet, the generation is skipped in this case.

### All sheets in spreadsheet with a sheet configuration

```
dlgsheet  --use-keys-table
```

In this case, it uses a keys' table (by default with `_keys` name) where it has
the information about the sheets that should be saved related to a specified
key and the key index in the columns for each sheet.

The keys' table must have the following structure:

| tablename   | key_index |
| ----------- | --------- |
| sheet_1     | 0         |
| sheet_3     | 0         |
| sheet_5     | 0         |

Where `sheet_x` represents the sheet name in the spreadsheet that will use a
key index and the values in the `key_index` column is the position of the
column that will be used as keys for the generated object.

If the spreadsheet has other sheets that are not present in the `tablename`
column, then the generation is without considering an index.

## License

Copyright 2021 Luighi Viton-Zorrilla

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
