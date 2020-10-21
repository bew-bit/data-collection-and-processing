# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайтов
# Superjob и HH. Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# - Наименование вакансии.
# - Предлагаемую зарплату (отдельно минимальную, максимальную и валюту).
# - Ссылку на саму вакансию.
# - Сайт, откуда собрана вакансия.
### По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение). Структура должна быть
# одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas.

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from pprint import pprint
import re

#https://hh.ru/vacancies/sistemnyy_analitik?page=
main_link = 'https://hh.ru'
params = {'page':'0'}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38'}

vacancies_hh = []
while True:
    response = requests.get(main_link+'/vacancies/sistemnyy_analitik',params=params,headers=headers)
    soup = bs(response.text,'html.parser')
    vacancy_list = soup.findAll('div', {'class':'vacancy-serp-item'})

    for vacancy in vacancy_list:
        vacancy_name = vacancy.find('span', {'class': 'resume-search-item__name'}).getText()

        vacancy_compensation = vacancy.find('span',{'data-qa':'vacancy-serp__vacancy-compensation'})
        if not vacancy_compensation:
            vacancy_compensation_min = None
            vacancy_compensation_max = None
            vacancy_compensation_currency = None
        else:
            vacancy_compensation = vacancy_compensation.getText()
            vacancy_compensation = re.split(r'\s|-',vacancy_compensation)
            if vacancy_compensation[0] == "до":
                vacancy_compensation_min = None
                vacancy_compensation_max = int(vacancy_compensation[1]+vacancy_compensation[2])
            elif vacancy_compensation[0] == "от":
                vacancy_compensation_min = int(vacancy_compensation[1]+vacancy_compensation[2])
                vacancy_compensation_max = None
            else:
                vacancy_compensation_min = int(vacancy_compensation[0]+vacancy_compensation[1])
                vacancy_compensation_max = int(vacancy_compensation[2]+vacancy_compensation[3])
                vacancy_compensation_currency = vacancy_compensation[4]

        vacancy_link = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']

        vacancies_hh.append({'vacancy_name': vacancy_name,
                       'vacancy_compensation_min': vacancy_compensation_min,
                       'vacancy_compensation_max': vacancy_compensation_max,
                       'vacancy_compensation_currency': vacancy_compensation_currency,
                       'vacancy_link': vacancy_link,
                       'site': main_link
                       })

    next_page = soup.find('a', {'data-qa': ['pager-next']})
    if next_page:
        params['page'] = str(int(params['page']) + 1)
    else:
        break

hh = pd.DataFrame(vacancies_hh)
pprint(hh)
print(f'кол-во вакансий на hh.ru: {len(vacancies_hh)}')


#https://www.superjob.ru/vakansii/analitik-sistemnyj.html?geo%5Bt%5D%5B0%5D=4&click_from=facet
main_link = 'https://www.superjob.ru'
params = {'geo%5Bt%5D%5B0%5D':'4',
          'click_from':'facet',
          'page':'1'}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38'}

vacancies_sj = []
while True:
    response = requests.get(main_link+'/vakansii/analitik-sistemnyj.html',params=params,headers=headers)
    soup = bs(response.text,'html.parser')
    vacancy_list = soup.findAll('div', {'class':['iJCa5 f-test-vacancy-item _1fma_ undefined _2nteL']})

    for vacancy in vacancy_list:
        vacancy_name = vacancy.find('div', {'class': ['_3mfro PlM3e _2JVkc _3LJqf']})#.getText()

        vacancy_compensation = vacancy.find('span', {'class': 'f-test-text-company-item-salary'}).text.split('\xa0')
        if vacancy_compensation[0] == "По договорённости":
            vacancy_compensation_min = None
            vacancy_compensation_max = None
            vacancy_compensation_currency = None
        else:
            vacancy_compensation_currency = vacancy_compensation[-1]
            if vacancy_compensation[0] == "до" or len(vacancy_compensation) == 2:
                vacancy_compensation_min = None
                vacancy_compensation_max = int(vacancy_compensation[1]+vacancy_compensation[2])
            elif vacancy_compensation[0] == "от":
                vacancy_compensation_min = int(vacancy_compensation[1]+vacancy_compensation[2])
                vacancy_compensation_max = None
            else:
                vacancy_compensation_min = int(vacancy_compensation[0]+vacancy_compensation[1])
                vacancy_compensation_max = int(vacancy_compensation[3]+vacancy_compensation[4])

        vacancy_link = main_link + vacancy_name.next['href'] if vacancy_name else ''
        vacancies_sj.append({'vacancy_name': vacancy_name,
                       'vacancy_compensation_min': vacancy_compensation_min,
                       'vacancy_compensation_max': vacancy_compensation_max,
                       'vacancy_compensation_currency': vacancy_compensation_currency,
                       'vacancy_link': vacancy_link,
                       'site': main_link
                       })

    next_page = soup.find('a', {'class': ['icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']})
    if next_page:
        params['page'] = str(int(params['page']) + 1)
    else:
        break

sj = pd.DataFrame(vacancies_sj)
pprint(sj)
print(f'кол-во вакансий на superjob.ru: {len(vacancies_sj)}')

df = hh.append(sj)