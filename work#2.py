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

#https://hh.ru/search/vacancy?clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&text=системный+аналитик&page=
main_link = 'https://hh.ru'
params = {'clusters':'true',
          'area':'1',
          'enable_snippets':'true',
          'salary':'',
          'st':'searchVacancy',
          'text':'системный+аналитик',
          'page':''}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38'}
response = requests.get(main_link+'/search/vacancy',params=params,headers=headers)
soup = bs(response.text,'html.parser')
vacancy_list = soup.findAll('div',{'class':'vacancy-serp-item__row vacancy-serp-item__row_header'})

vacancies = []
for vacancy in vacancy_list:
    vacancy_date = {}
    vacancy_name = vacancy.find('span', {'class': 'resume-search-item__name'}).text
    vacancy_date['vacancy_name'] = vacancy_name