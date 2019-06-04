# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

from scrapy.exporters import JsonLinesItemExporter


class BossPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonExportPipeline(object):
    def __init__(self, settings):
        self.save_file = open(os.path.join(settings.get("RESULT_PATH"), "Boss.json"), "ab")
        self.exporter = JsonLinesItemExporter(self.save_file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings)

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.save_file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
