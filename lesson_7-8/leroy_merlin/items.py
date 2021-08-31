# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
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
