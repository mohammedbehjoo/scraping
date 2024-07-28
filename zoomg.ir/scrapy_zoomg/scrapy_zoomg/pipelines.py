# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class ScrapyZoomgPipeline:
    def process_item(self, item, spider):
        return item


class EmptyNewsZoomgPipeline:
    def __init__(self):
        self.title_seen = ()

    def drop_null_titles(self, item, spider):
        if item["title"] in self.title_seen:
            raise DropItem("Repeated title found: %s" % item)
        elif len(item[0]) < 1:
            raise DropItem("Null title found: %s" % item)
        else:
            self.title_seen.add(item["title"])
            return item
