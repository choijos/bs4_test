import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # h1_tag = response.xpath('//h1/a/text()').extract_first()
        # tags = response.xpath('//*[@class="tag-item"]/a/text()').extract()

        # yield {
        #     'H1 Tag': h1_tag,
        #     'Tags': tags
        # }
        quotes = response.xpath('//*[@class="quote"]')
        for quote in quotes:
            text = quote.xpath('.//*[@class="text"]/text()').extract_first()
            author = quote.xpath('.//*[@class="author"]/text()').extract_first()
            # instead, to get a list of the tags, we can do
            #   quote.xpath('.//*[@class="tag"]/text()').extract()
            tags = quote.xpath('.//*[@class="keywords"]/@content').extract_first()

            yield {
                'Text': text,
                'Author': author,
                'Tags': tags
            }

            # print('\n')
            # print(text)
            # print(author)
            # print(tags)
            # print('\n')
        # scrapy crawl <spider_name>

        next_page_url = response.xpath('//*[@class="next"]/a/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(absolute_next_page_url)
        # if this request was outside of the prase function, the request would also need a callback arg
        #   callback=self.parse_page or something like that


# misc command line work
#
# scrapy crawl quotes -o items.csv
#                        items.json
#                        items.xml
