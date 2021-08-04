import requests
from pprint import pprint
from googleapiclient import discovery

credentials = None

service = discovery.build('sheets', 'v4', credentials=credentials)

spreadsheet_id = '1xqmHsYoSxOw9xMuYNHPssLupW8JxN3VpWv3xYWpwx8w'

data_range = '2021!A1:B100'

#url = 'https://sheets.googleapis.com/v4/spreadsheets/1xqmHsYoSxOw9xMuYNHPssLupW8JxN3VpWv3xYWpwx8w/values/Sheet1!A1:D5'

request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_, valueRenderOption=value_render_option, dateTimeRenderOption=date_time_render_option)
response = request.execute()

#response = requests.get(url)
#db_json = response.json()

pprint(response)