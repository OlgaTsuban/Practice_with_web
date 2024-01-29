import json
import os
from django.conf import settings
import scrapy
from scrapy.utils.log import configure_logging

from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerRunner
from scrapy.item import Item, Field
from twisted.internet import reactor


class AuthorItem(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()

class QuoteItem(Item):
    author = Field()
    quote = Field()
    tags = Field()

class Pipeline:

    authors = []
    quotes = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'fullname' in adapter.keys():
            self.authors.append(dict(adapter))
        if 'quote' in adapter.keys():
            self.quotes.append(dict(adapter))

    def close_spider(self, spider):
        with open('quotes.json', 'w', encoding='utf-8') as fd:
            json.dump(self.quotes, fd, ensure_ascii=False, indent=2)
        # with open('authors.json', 'w', encoding='utf-8') as fd:
        #     json.dump(self.authors, fd, ensure_ascii=False, indent=2)


class QuotesSpider(scrapy.Spider):
    name = 'quotes_and_authors'
    custom_settings = {
        "ITEM_PIPELINES": {Pipeline: 300}
    }
    allowed_domains = ['localhost']  # Adjust this according to your Django server's domain
    start_urls = ['http://localhost:8000/quotes/all_quotes/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, response, *args, **kwargs):
        for quote_s in response.xpath("/html//div[@class='quote-box']"):
            author = quote_s.xpath(".//p[@class='author']/a/text()").get().strip()
            quote = quote_s.xpath(".//p[2]/text()").get()
            tags = quote_s.xpath(".//p[@class='tags']/a/text()").getall()
            yield QuoteItem(author=author, quote=quote, tags=tags)

        # Extract the "Next" link from the pagination section
        next_link = response.xpath("//a[@class='btn btn-primary' and contains(text(), 'Next')]/@href").get()
        
        # Check if the "Next" link exists and yield a request for it
        if next_link:
            next_url = response.urljoin(next_link)
            yield scrapy.Request(url=next_url)

    @classmethod
    def get_author(self, response):
        body = response.xpath('/html//div[@class="author-details"]')
        yield AuthorItem(
            fullname=body.xpath('h3[@class="author-title"]/text()').get().strip(),
            born_date=body.xpath('p/span[@class="author-born-date"]/text()').get().strip(),
            born_location=body.xpath('p/span[@class="author-born-location"]/text()').get().strip(),
            description=body.xpath('div[@class="author-description"]/text()').get().strip(),
        )


def scrape_data() -> None:
    """process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()"""
    if not settings.configured:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes.settings')  # Set your Django project's settings module
        # Initialize Django settings
        settings.configure()

    configure_logging()
    runner = CrawlerRunner()

    # 'crawl' method returns a deferred, which will be fired when the crawling is finished
    d = runner.crawl(QuotesSpider)
    d.addBoth(lambda _: reactor.stop())

    # Start the Twisted reactor, the script will block here until the spider is finished
    reactor.run()