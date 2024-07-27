# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class ScrapyBidgolPipeline:
    def process_item(self, item, spider):
        item["title"] = " ".join(item["title"].split())
        return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.url_seen = set()

    def process_item(self, item, spider):
        if item["url"] in self.url_seen:
            raise DropItem("Repeated item found: %s" % item)
        else:
            self.url_seen.add(item["url"])
            return item
