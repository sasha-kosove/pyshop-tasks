import json

import pandas as pd
from itemadapter import ItemAdapter


class SmartphonePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("os"):
            if adapter["os"].endswith(".x"):
                adapter["os"] = adapter["os"][:-2]
        return item


class JsonWriterPipeline:
    def open_spider(self, spider):
        self.smartphones = []

    def close_spider(self, spider):
        with open("smartphones.json", "w", encoding="utf8") as json_file:
            json.dump(self.smartphones, json_file, ensure_ascii=False)

    def process_item(self, item, spider):
        self.smartphones.append(ItemAdapter(item).asdict())
        return item


class DistributionWriterPipeline:
    def open_spider(self, spider):
        self.list_os = []

    def close_spider(self, spider):
        series = pd.Series(self.list_os)
        distribution = series.value_counts()
        distribution.to_csv("distribution.csv")

    def process_item(self, item, spider):
        self.list_os.append(ItemAdapter(item).asdict()["os"])
        return item
