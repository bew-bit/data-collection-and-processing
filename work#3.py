# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные
# вакансии в созданную БД.
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
#from pymongo import MongoClient
import pymongo

#функция единовременной записи в бд 'vacancies' всех вакансий 'системный аналитик' на hh.ru на данный момеент:
def ones_hh_vacancies():
    client = MongoClient('127.0.0.1',27017)
    db = client['vacancies']
    hh = db.hh

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

            hh.insert_one({'vacancy_name': vacancy_name,
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

#проверка наличия записей в схеме hh:
"""
ones_hh_vacancies()
for item in hh.find({}):
    pprint(item)
"""

#2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.
# Запрос должен анализировать одновременно минимальную и максимальную зарплату.

def print_salary(salary):
    salaries = hh.find({'$or':[{'vacancy_compensation_min': {'$gte': salary}},
                                       {'vacancy_compensation_max': {'$gte': salary}}]
    })
    for sal in salaries:
        pprint(sal)

