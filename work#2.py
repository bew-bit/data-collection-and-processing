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

#https://hh.ru/vacancies/analyst?page=
main_link = 'https://hh.ru'
params = {'page':''}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38'}
response = requests.get(main_link+'/vacancies/analyst',params=params,headers=headers)
soup = bs(response.text,'html.parser')
vacancy_list = soup.findAll('div', {'class':'vacancy-serp-item'})

vacancies = []
for vacancy in vacancy_list:
    vacancy_date = {}

    vacancy_name = vacancy.find('span', {'class': 'resume-search-item__name'}).getText()
    vacancy_date['vacancy_name'] = vacancy_name

    vacancy_compensation = vacancy.find('span',{'data-qa':'vacancy-serp__vacancy-compensation'}).getText()
    if not vacancy_compensation:
        vacancy_compensation_min = None
        vacancy_compensation_max = None
        vacancy_compensation_currency = None
    else:
        vacancy_compensation = re.split(r'\s|-', vacancy_compensation)

        if vacancy_compensation[0] == 'до':
            vacancy_compensation_min = None
            vacancy_compensation_max = int(vacancy_compensation[1]+vacancy_compensation[2])
        elif vacancy_compensation[0] == 'от':
            vacancy_compensation_min = int(vacancy_compensation[1]+vacancy_compensation[2])
            vacancy_compensation_max = None
        else:
            vacancy_compensation_min = int(vacancy_compensation[0]+vacancy_compensation[1])
            vacancy_compensation_max = int(vacancy_compensation[2]+vacancy_compensation[3])

        vacancy_compensation_currency = vacancy_compensation[4]

    vacancy_date['vacancy_compensation_min'] = vacancy_compensation_min
    vacancy_date['vacancy_compensation_max'] = vacancy_compensation_max
    vacancy_date['vacancy_compensation_currency'] = vacancy_compensation_currency

    vacancy_link = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']
    vacancy_date['vacancy_link'] = vacancy_link
    vacancy_date['site'] = 'hh.ru'

df = pd.DataFrame(vacancy_date)