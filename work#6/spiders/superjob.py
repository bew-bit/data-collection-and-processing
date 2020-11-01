import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['spb.superjob.ru']
    start_urls = ['https://www.superjob.ru/vakansii/analitik-sistemnyj.html?geo%5Bt%5D%5B0%5D=4&click_from=facet']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[contains (@class, "_6AfZ9")]/@href').extract()
        next_page = response.xpath('//span[@class="_3IDf-"]/@href').extract_first()
        for link in links:
            yield response.follow(vac_link, callback=self.vacancy_parse)
        if next_page:
            yield response.follow(next_page_link, callback=self.parse)
        print()

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath('//h1/text()').extract_first()
        salary = response.xpath('//span[@class="_1OuF_ ZON4b"]//text()').extract()
        url = response.url
        yield JobparserItem(name=name, salary=salary, link=url)
        print()