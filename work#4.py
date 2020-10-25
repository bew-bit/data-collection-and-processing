# 1.Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex-новости. Для парсинга
# использовать XPath. Структура данных должна содержать:
# - название источника;
# - наименование новости;
# - ссылку на новость;
# - дата публикации.
# 2.Сложить собранные данные в БД

from lxml import html
import requests
from pymongo import MongoClient
from pprint import pprint

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38'}

client = MongoClient('127.0.0.1', 27017)
db = client['news']


def lenta_ru():
    main_link = 'https://lenta.ru'
    response = requests.get(main_link, headers=headers)
    dom = html.fromstring(response.text)
    news_elements = dom.xpath("//section[contains(@class,'js-top-seven')]//div[@class='item']")
    for element in news_elements:
        title = str(element.xpath("./a/text()")[0].replace(u'\xa0', u' '))
        url = main_link + str(element.xpath("./a/@href")[0])
        publication_date = str(element.xpath("./a/time/@datetime")[0])
        db.news.insert_one({
            'title': title,
            'url':  url,
            'source': main_link,
            'publication_date': publication_date
        })


def mail_ru():
    main_link = 'https://news.mail.ru/'
    response = requests.get(main_link, headers=headers)
    dom = html.fromstring(response.text)
    news_elements = dom.xpath("//ul[@data-module='TrackBlocks']/li[@class='list__item']")
    for element in news_elements:
        _response = requests.get(str(element.xpath("./a/@href")[0]), headers=self.headers)
        _dom = html.fromstring(_response.text)
        title = str(element.xpath(".//text()")[0].replace(u'\xa0', u' '))
        url = str(element.xpath("./a/@href")[0])
        source = str(_dom.xpath("//a[contains(@class,'breadcrumbs__link')]//text()")[0])
        publication_date = str(_dom.xpath("//span[@datetime]/@datetime")[0])
        db.news.insert_one({
            'title': title,
            'url': url,
            'source': source,
            'publication_date': publication_date
        })


def yandex_ru():
    main_link = 'https://yandex.ru/news'
    response = requests.get(main_link, headers=headers)
    dom = html.fromstring(response.text)
    news_elements = dom.xpath("//div[contains(@class,'news-top-stories')]/div")
    for element in news_elements:
        title = str(element.xpath(".//h2/text()")[0])
        url = str(element.xpath(".//a[@class='news-card__link']/@href")[0])
        source = str(element.xpath(".//span[@class='mg-card-source__source']/a/text()")[0])
        publication_date = str(element.xpath(".//span[@class='mg-card-source__time']/text()")[0])
        db.news.insert_one({
            'title': title,
            'url':  url,
            'source': source,
            'publication_date': publication_date
        })


lenta_ru()
mail_ru()
yandex_ru()