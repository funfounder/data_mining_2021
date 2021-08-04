from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
from pprint import pprint
import requests
import re
import json

client = MongoClient('127.0.0.1', 27017)
db = client['hh']
vacancies_db = db['results']

url = 'https://hh.ru'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}

params = {'page': 0, 'text': input('Insert job title: ')}

salary_find = int(input('Insert expected amount: '))

available_vacancies = []

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}
params = {'page': 0, 'text': ''}

def get_vacancies():
    page_vacancies = []
    for vacancy in vacancies_block:
        vacancy_data = {}
        vacancy_data['name'] = vacancy.find('a', attrs={'class': 'bloko-link'}).getText()
        money = vacancy.find('div', attrs={'class': 'vacancy-serp-item__sidebar'})
        if money:
            money = money.getText()
            if " – " in money:
                money = money.split(" – ")
                vacancy_data['salary_min'] = int("".join(money[0].split("\u202f")))
                salary_max = money[1].split('\u202f')
                vacancy_data['salary_max'] = int(f"{salary_max[0]}{salary_max[1].split(' ')[0]}")
                vacancy_data['salary_currency'] = salary_max[1].split(' ')[1]
            elif " – " not in money:
                salary = money.split(' ')
                if salary[0] == "от":
                    vacancy_data['salary_min'] = int("".join(salary[1].split("\u202f")))
                    vacancy_data['salary_max'] = None
                    vacancy_data['salary_currency'] = salary[2]
                elif salary[0] == "до":
                    vacancy_data['salary_min'] = None
                    vacancy_data['salary_max'] = int("".join(salary[1].split("\u202f")))
                    vacancy_data['salary_currency'] = salary[2]
                else:
                    vacancy_data['salary_min'] = None
                    try:
                        vacancy_data['salary_max'] = int("".join(salary[0].split("\u202f")))
                        vacancy_data['salary_currency'] = salary[1]
                    except ValueError:
                        vacancy_data['salary_max'] = None
                        vacancy_data['salary_currency'] = None
        vacancy_data['company'] = vacancy.find('a', attrs={'class': 'bloko-link bloko-link_secondary'}).getText().replace('\xa0', '')
        vacancy_data['link'] = vacancy.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).get('href').split('?')[0]
        region = vacancy.find('span', attrs={'class': 'vacancy-serp-item__meta-info'})
        if region:
            vacancy_data['region'] = region.getText()
        page_vacancies.append(vacancy_data)
    return available_vacancies.extend(page_vacancies)

while True:
    response = None
    if params['page'] == 0:
        response = requests.get(url + '/search/vacancy', params={'text': params['text']}, headers=headers)
    elif params['page'] > 0:
        response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    vacancies_block = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
    get_vacancies()
    #get_vacancies(vacancies_block)
    if soup.find('span', attrs={'class': 'bloko-form-spacer'}):
        params['page'] +=1
        continue
    else:
        break

for vacancy in available_vacancies:
    vacancies_db.update_one(
                #{'name':vacancy['name'], 'company':vacancy['company']},
                {'link':vacancy['link']},
                {'$set':vacancy},
                upsert=True)

min_max = vacancies_db.find(
    {'$or': [
        {'salary_min': {'$gt': salary_find}},
        {'salary_max': {'$gt': salary_find}},
    ]})