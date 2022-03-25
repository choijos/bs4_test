# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor


# class BooksSpider(CrawlSpider):
#     name = 'books'
#     allowed_domains = ['books.toscrape.com']
#     start_urls = ['http://books.toscrape.com/']

#     # LinkExtractor args
#     #
#     # deny_domains=('google.com')
#     # allow=('music') # only scrapes urls with 'music' in them
#     rules = (Rule(LinkExtractor(), callback='parse_page', follow=True),) # this comma afterwards is important, will throw error if not present

#     def parse_page(self, response):
#         yield {
#             'URL': response.url
#         }


from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from time import sleep
from selenium.common.exceptions import NoSuchElementException

class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['http://books.toscrape.com']

    def start_requests(self):
        # return request to url
        self.driver = webdriver.Chrome('/Users/jossiechoi/chromedriver')
        self.driver.get('http://books.toscrape.com')

        while True:
            try:
                next_page = self.driver.find_element_by_xpath('//a[text()="next"]')
                sleep(3)
                self.logger.info('sleeping for 3 secs')
                next_page.click()

                sel = Selector(text=self.driver.page_source)
                books = sel.xpath('//h3/a/@href').extract()

                for book in books:
                    url = 'http://books.toscrape.com/catalogue/' + book
                    yield Request(url, callback=self.parse_book)

            except NoSuchElementException:
                self.logger.info('No more pages to load')
                self.driver.quit()
                break

    def parse_book(self, response):
        pass