import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

#вопрос, подскажите, пожалуйста, почему у меня не работают пути, хотя leroy_merlin - является пакетом. не работает никакой из вариантов ниже.
#from leroy_merlin.items import LeroyMerlinItem
from ..items import LeroyMerlinItem


from itemloaders.processors import MapCompose, TakeFirst

def process_price(value):
    value = value.replace(' ', '')
    return value

class LeroyMerlinItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field()
    characteristics = scrapy.Field()
    characteristics_keys = scrapy.Field()
    characteristics_values = scrapy.Field(output_processor=MapCompose(str.strip))
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(process_price, float), output_processor=TakeFirst())


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/elektroinstrumenty/']


    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@aria-label, 'Следующая страница:')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, self.parse)

        urls = response.xpath("//div[@data-qa-product]/a/@href").extract()
        for url in urls:
            yield response.follow(url, self.product_parse)


    def product_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyMerlinItem(), response=response)
        loader.add_xpath("name", "//h1/text()")
        loader.add_xpath("images", "//picture[@slot='pictures']/source[contains(@data-origin, '2000')]/@data-origin")
        loader.add_xpath("characteristics_keys", "//dl/div/dt/text()")
        loader.add_xpath("characteristics_values", "//dl/div/dd/text()")
        loader.add_value("url", response.url)
        loader.add_xpath("price", "//span[@slot='price']/text()")

        yield loader.load_item()