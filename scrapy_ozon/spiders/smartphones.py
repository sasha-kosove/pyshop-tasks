import scrapy

from scrapy_ozon.items import Smartphone


class SmartphonesSpider(scrapy.Spider):
    name = "smartphones"

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.ozon.ru/category/smartfony-15502/?sorting=rating",
            callback=self.parse_list,
        )
        self.product_links = []

    def parse_list(self, response):
        for link in response.css("a.tile-hover-target.k8n::attr(href)"):
            self.product_links.append(link.get())

        next_page_number = int(response.css("a.ama.aam0::text").get()) + 1

        if len(self.product_links) < 100:
            yield scrapy.Request(
                url=f"https://www.ozon.ru/category/smartfony-15502/?page={next_page_number}&sorting=rating",
                callback=self.parse_list,
            )
        else:
            for link in self.product_links[:100]:
                link = link.split("?")[0]
                yield scrapy.Request(
                    url=f"https://www.ozon.ru{link}",
                    callback=self.parse_detail,
                    dont_filter=True,
                )

    def parse_detail(self, response):
        name = response.xpath("//h1[@class='vn0']/text()").get()
        os = response.xpath(
            "//dl[dt[span[contains(text(), 'Версия')]]]/dd//text()"
        ).get()
        print(self.product_links)
        if not os:
            os = "Not specified"
        yield Smartphone(name=name, os=os)
