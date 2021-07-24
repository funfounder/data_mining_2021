import requests
from pprint import pprint

user = 'funfounder'
token = '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'

url = f'https://api.github.com/users/{user}/repos'

response = requests.get(url)
db_json = response.json()

repositories_names = []

for i in db_json:
    repositories_names.append(i['name'])

pprint(repositories_names)
