# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from jobparser.items import JobparserItem
from scrapy import Spider


class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy

    def process_item(self, item: JobparserItem, spider: Spider):
        collection = self.mongo_base[spider.name]
        item['min_salary'], item['max_salary'], item['currency'] = self.process_salary(item['salary'])
        collection.insert(item)
        return item


    def cleanup_salary_list(self, salary_list: list):
        result_list = []
        for item in salary_list:
            item = item.strip().replace(u'\xa0', u'').replace(u' ', u'')
            if item:
                result_list.append(item)
        return result_list


    def process_salary(self, salary: list):
        min_salary = None
        max_salary = None
        currency = None

        if salary:
            salary = self.cleanup_salary_list(salary)

            try:
                for i in range(0, len(salary)):
                    if salary[i] == 'от':
                        min_salary = int(''.join([i for i in salary[i+1] if i.isdigit()]))
                        currency = salary[i+2]

                    if salary[i] == '—':
                        min_salary = int(''.join([i for i in salary[i-1] if i.isdigit()]))
                        max_salary = int(''.join([i for i in salary[i+1] if i.isdigit()]))
                        currency = salary[i+2]

                    if salary[i] == 'до':
                        max_salary = int(''.join([i for i in salary[i+1] if i.isdigit()]))
                        currency = salary[i+2]

                    if salary[i] == '/':
                        currency = (''.join([i for i in salary[i-1] if not i.isdigit()]))

            except IndexError:
                pass

        return min_salary, max_salary, currency