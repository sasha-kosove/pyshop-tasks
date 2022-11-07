BOT_NAME = "scrapy_ozon"

SPIDER_MODULES = ["scrapy_ozon.spiders"]
NEWSPIDER_MODULE = "scrapy_ozon.spiders"


DOWNLOADER_MIDDLEWARES = {"scrapy_ozon.middlewares.SeleniumMiddleWare": 200}

ITEM_PIPELINES = {
    "scrapy_ozon.pipelines.SmartphonePipeline": 100,
    "scrapy_ozon.pipelines.JsonWriterPipeline": 300,
    "scrapy_ozon.pipelines.DistributionWriterPipeline": 500,
}

ROBOTSTXT_OBEY = False
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
