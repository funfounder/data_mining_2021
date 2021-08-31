import scrapy
import re
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

replaces = ('\xa0', '/')


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vakansii/kassir.html?geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("///a[contains(@class, 'f-test-button-dalshe')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath(
            "//div[@class='f-test-search-result-item']//a[contains(@class, 'f-test-link-') and contains(@href, 'vakansii')]/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        job_name = response.xpath("//h1/child::text()").extract_first()
        money = ''.join(response.xpath("//h1/following-sibling::span/descendant::text()").getall())
        # todo проверить что мы получаем в выдаче по этому спану и разобрать его на деньги как было сделано в hh
        if money:
            if "\xa0—\xa0" in money:
                money = money.split("\xa0—\xa0")
                job_salary_min = int(money[0].replace('\xa0', ''))
                money_max = money[1].replace('\xa0', '')
                job_salary_max = int(re.split('(\d+)', money_max)[1])
                job_salary_rate = re.split('(\d+)', money_max)[-1].replace('/', ' ')
            elif "\xa0—\xa0" not in money:
                money = money.split('\xa0')
                if "от" in money:
                    value = [i for i in money if i.isdigit()]
                    job_salary_min = int(''.join(value))
                    job_salary_max = None
                    if money[-1].isdigit() == False:
                        job_salary_rate = money[-1].replace('/', ' ')
                    else:
                        job_salary_rate = None
                elif "до" in money:
                    value = [i for i in money if i.isdigit()]
                    job_salary_min = None
                    job_salary_max = int(''.join(value))
                    if money[-1].isdigit() == False:
                        job_salary_rate = money[-1].replace('/', ' ')
                    else:
                        job_salary_rate = None
                else:
                    job_salary_min = None
                    try:
                        value = [i for i in money if i.isdigit()]
                        job_salary_max = int(''.join(value))
                        if money[-1].isdigit() == False:
                            job_salary_rate = money[-1].replace('/', ' ')
                        else:
                            job_salary_rate = None
                    except ValueError:
                        job_salary_max = None
                        job_salary_rate = None
        # job_salary_min = response.css("p.vacancy-salary span::text").extract_first() salary_min=job_salary_min, salary_max=job_salary_max,
        # job_salary_max = response.css("p.vacancy-salary span::text").extract_first()
        # job_salary_rate = '''salary_rate = job_salary_rate'''
        job_url = response.url
        yield JobparserItem(name=job_name, salary_min=job_salary_min, salary_max=job_salary_max, url=job_url,
                            salary_rate=job_salary_rate, source=self.allowed_domains)
