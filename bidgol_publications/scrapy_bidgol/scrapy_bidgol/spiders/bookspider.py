import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookspiderSpider(CrawlSpider):
    name = "bookspider"
    allowed_domains = ["www.bidgolpublishing.com"]
    start_urls = ["http://www.bidgolpublishing.com/Books.aspx?t=0&c=0&p=1"]

    rules = {
        Rule(LinkExtractor(restrict_css=".pages a"),
            callback="parse", follow=True)
    }

    custom_settings = {
        "DOWNLOAD_DELAY" : 1,
        "RANDOMIZE_DOWNLOAD_DELAY": True
    }

    def parse(self, response):
        BOOK_SELECTOR = ".row .img-row a"
        TITLE_SELECTOR = ".head::text"
        URL_SELECTOR = "::attr(href)"

        for book in response.css(BOOK_SELECTOR):
            yield {
                "title": book.css(TITLE_SELECTOR).extract_first(),
                "url": "http://www.bidgolpublishing.com/" + book.css(URL_SELECTOR).extract_first()
            }
