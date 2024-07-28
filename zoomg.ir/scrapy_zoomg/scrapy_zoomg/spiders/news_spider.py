import scrapy
from scrapy.spiders import CrawlSpider,Rule

class NewsSpiderSpider(scrapy.Spider):
    name = "news_spider"
    allowed_domains = ["zoomg.ir"]
    start_urls = ["https://www.zoomg.ir/page/1/"]
    
    

    def parse(self, response):
        NEWS_SELECTOR = ".imgContainer"
        TITLE_SELECTOR = ".Contents h3 a::text"
        URL_SELECTOR = ".Contents h3 a::attr(href)"
        TAG_SELECTOR = ".topicCategories a label::text"
        AUTHOR_SELECTOR = "ul li:nth-child(1) a::text"
        DATE_SELECTOR = "ul li:nth-child(2)::text"
        COMMENTS_SELECTOR = ".inline-block .pull-left::text"
        SUMMARY_SELECTOR = ".Contents p::text"

        for news in response.css(NEWS_SELECTOR):
            yield {
                "title": news.css(TITLE_SELECTOR).extract_first(),
                "url": news.css(URL_SELECTOR).extract_first(),
                "tag": news.css(TAG_SELECTOR).extract(),
                "author": news.css(AUTHOR_SELECTOR).extract_first(),
                "date": news.css(DATE_SELECTOR).extract_first(),
                "comments": news.css(COMMENTS_SELECTOR).extract_first(),
                "summary": news.css(SUMMARY_SELECTOR).extract_first()
            }
            
        current_page = int(response.url.split('/')[-2])
        next_page = current_page + 1

        if next_page > 10:
            return
        else:
            yield scrapy.Request(f'https://www.zoomg.ir/page/{next_page}/')
