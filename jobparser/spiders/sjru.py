import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vakansii/kassir.html?geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("///a[contains(@class, 'f-test-button-dalshe')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//div[@class='f-test-search-result-item']//a[contains(@class, 'f-test-link-') and contains(@href, 'vakansii')]").extract()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response:HtmlResponse):
        job_name = response.xpath("//h1/child::text()").extract_first()
        salary = response.css("//h1/following-sibling::span/text()").extract_first()
        #todo проверить что мы получаем в выдаче по этому спану и разобрать его на деньги как было сделано в hh
        job_salary_min = response.css("p.vacancy-salary span::text").extract_first()
        job_salary_max = response.css("p.vacancy-salary span::text").extract_first()
        #job_salary_rate =
        job_url = response.url
        yield JobparserItem(name=job_name, salary_min=job_salary_min, salary_max=job_salary_max, url=job_url, source = self.allowed_domains)