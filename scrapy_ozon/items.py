import scrapy


class Smartphone(scrapy.Item):
    name = scrapy.Field()
    os = scrapy.Field()
