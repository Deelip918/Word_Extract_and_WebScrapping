from pathlib import Path

import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime
import os


class QuotesSpider(scrapy.Spider):
    name = "quotes2"
    def start_requests(self):
        yield scrapy.Request('https://quotes.toscrape.com/page/1/')

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get().replace('“', ''),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
            if quote in visited:
                continue
            visited.add(quote)
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


now = datetime.now()
folder_path = 'file://D:/affine/hitachi/crawling/output'
file_date_part = "quotes_" + now.strftime("%Y%m%d_%H%M%S") + ".csv"
file_name = os.path.join(folder_path, file_date_part)

process = CrawlerProcess(settings={
    'ROBOTSTXT_OBEY': True,
    'FEED_URI': file_name,
    'FEED_FORMAT': 'csv',
    "FEED_EXPORT_ENCODING": "utf-8",
    "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"
})
visited=set()
process.crawl(QuotesSpider)
process.start()