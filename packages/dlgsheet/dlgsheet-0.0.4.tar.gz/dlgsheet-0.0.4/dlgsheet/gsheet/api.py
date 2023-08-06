from dlgsheet import config
from googleapiclient.discovery import build
from google.oauth2 import service_account
from pathlib import Path

if(Path(config.google["credentialsfile"]).exists()):
    globalcredentials = service_account.Credentials.from_service_account_file(
        config.google["credentialsfile"], scopes=config.google["scopes"])


def set_credentials(filename):
    credentials = service_account.Credentials.from_service_account_file(
        filename, scopes=config.google["scopes"])
    return credentials


def get_spreadsheet_service(spreadsheetid=None,
                          credentials=None):

    if(credentials is None):
        credentials = globalcredentials

    if(spreadsheetid is None):
        spreadsheetid = config.google["spreadsheetid"]

    service = build('sheets', 'v4', credentials=credentials)

    sheet = service.spreadsheets()
    return sheet, spreadsheetid


def get_tables(spreadsheetid=None,
              credentials=None):

    sheet, spreadsheetid = get_spreadsheet_service(spreadsheetid=spreadsheetid,
                                                 credentials=credentials)

    result = sheet.get(spreadsheetId=spreadsheetid).execute()
    sheetnames = [sheet["properties"]["title"] for sheet in result["sheets"]]
    return sheetnames


def get_table_values(sheetname, spreadsheetid=None,
                credentials=None):

    sheet, spreadsheetid = get_spreadsheet_service(spreadsheetid=spreadsheetid,
                                                 credentials=credentials)

    result = sheet.values().get(spreadsheetId=spreadsheetid,
                              valueRenderOption="UNFORMATTED_VALUE",
                              dateTimeRenderOption="FORMATTED_STRING",
                              range=f"{sheetname}").execute()

    return result


if __name__ == '__main__':

    result = get_tables()
    print(result)
    values = get_table_values("skills")
    print(values)
