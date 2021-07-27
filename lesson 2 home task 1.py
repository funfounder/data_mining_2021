from bs4 import BeautifulSoup as bs
import requests
import json

url = 'https://hh.ru'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}

params = {'page':1,
          'text':''}

params['text'] = input('Insert job title: ')

available_vacancies = []

# todo заходим на первую страницу только с job title
response = requests.get(url+'/search/vacancy', params={'text':params['text']}, headers=headers)

soup = bs(response.text, 'html.parser')

vacancies_block = soup.find_all('div',attrs={'class':'vacancy-serp-item'})

for vacancy in vacancies_block:
    vacancy_data = {}
    vacancy_data['name'] = vacancy.find('a', attrs={'class':'bloko-link'}).getText()
    salary = vacancy.find('div', attrs={'class': 'vacancy-serp-item__sidebar'})
    if salary:
        vacancy_data['salary'] = salary.getText()
    vacancy_data['company'] = vacancy.find('a', attrs={'class': 'bloko-link bloko-link_secondary'}).getText()
    vacancy_data['region'] = vacancy.find('span', attrs={'clas':'vacancy-serp-item__meta-info'}).text
    available_vacancies.append(vacancy_data)


# todo заходим в цикл где перебираем страницы пока есть кнопка далее

while True:
    response = requests.get(url + '/search/vacancy', params={params}, headers=headers)
    soup = bs(response.text, 'html.parser')
    vacancies_block = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
    for vacancy in vacancies_block:
        vacancy_data = {}
        vacancy_data['name'] = vacancy.find('a', attrs={'class': 'bloko-link'}).getText()
        salary = vacancy.find('div', attrs={'class': 'vacancy-serp-item__sidebar'})
        if salary:
            vacancy_data['salary'] = salary.getText()
        vacancy_data['company'] = vacancy.find('a', attrs={'class': 'bloko-link bloko-link_secondary'}).getText()
        vacancy_data['region'] = vacancy.find('span', attrs={'clas': 'vacancy-serp-item__meta-info'}).text
        available_vacancies.append(vacancy_data)
    if soup.find('span', attrs={'class':'bloko-form-spacer'}):
        params['page'] +=1
        continue
    else:
        break

# todo сохранить в json
with open(f'vacancies_{params["text"]}.json', 'w', encoding='UTF-8') as file:
    json.dump(available_vacancies, file, ensure_ascii=False)


#response = requests.get(url+'/search/vacancy', params=params, headers=headers)
