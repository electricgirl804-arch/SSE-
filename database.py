import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_sheet():
    scope = ["https://spreadsheets.google.com/feeds"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("sse-credentials.json", scope)
    client = gspread.authorize(creds)
    return client.open("SSE_Customers").sheet1
