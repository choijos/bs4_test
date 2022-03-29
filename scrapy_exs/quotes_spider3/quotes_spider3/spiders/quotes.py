from scrapy import Spider
from scrapy.http import Request


class QuotesSpider(Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.xpath('//*[@class="quote"]')
        
        for quote in quotes:
            text = quote.xpath('.//*[@class="text"]/text()').extract_first()
            author = quote.xpath('.//*[@class="author"]/text()').extract_first()

            tags = quote.xpath('.//*[@class="tags"]/text()').extract()

            yield {
                'Text': text,
                'Author': author,
                'Tags': tags
            }

# in terminal
#
# shub login
# shub deploy