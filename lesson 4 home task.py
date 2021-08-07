from lxml import html
from pymongo import MongoClient
import requests
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['lenta_ru']
news_db = db['results']

url = 'https://lenta.ru/'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}

response = requests.get(url, headers = headers)

dom = html.fromstring(response.text)

replaces = ('\u202f', '\xa0')

items = dom.xpath('//time[@class="g-time"]')

articles = []

for item in items:
    article = {}
    article['source'] = 'lenta.ru'
    article['name'] = item.xpath('../text()')[0]
    for rep in replaces:
        name = item.xpath('../text()')[0].replace(rep, ' ')
    article['name'] = name
#    article['name'] = (item.xpath('../text()')[0].replace(rep, ' ') for rep in replaces)
    article['link'] = f'{url}{"/".join(item.xpath("../@href")[0].split("/")[1:])}'
    article['date'] = item.xpath('./@title')[0]
    articles.append(article)


for article in articles:
    news_db.update_one(
                {'link':article['link']},
                {'$set':article},
                upsert=True)
