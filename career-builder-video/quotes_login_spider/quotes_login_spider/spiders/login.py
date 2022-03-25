import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self, response):
        # <input type="hidden" name="csrf_token" value=[some_token]>
        csrf_token = response.xpath('//*[@name="csrf_token"]/@value').extract_first()

        # Params from the Network tab:
        #   request URL
        #   csrf_token
        yield FormRequest(url='http://quotes.toscrape.com/login',
                          formdata={'csrf_token': csrf_token,
                                    'username': 'foobar',
                                    'password': 'testing'},
                          callback=self.parse_after_login)

    def parse_after_login(self, response):
        open_in_browser(response)
        # if response.xpath('//a[text()="Logout"]'):
        #     self.log('You logged in')
        # else:
        #     self.log('Failed to login')
