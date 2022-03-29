import scrapy
from scrapy_splash import SplashRequest


class BaierlSpider(scrapy.Spider):
    name = 'baierl'
    allowed_domains = ['lithia.com']
    start_urls = ['https://www.lithia.com/new-inventory/']

    def start_requests(self):
        filters_script = """function main(splash)
                                assert(splash:go(splash.args.url))
                                splash:wait(5)
                                
                                local get_element_dim_by_xpath = splash:jsfunc([[
                                    function(xpath) {
                                        var element = document.evaluate(xpath, document, null,
                                            XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                        var element_rect = element.getClientRects()[0];
                                        return {"x": element_rect.left, "y": element_rect.top}
                                    }
                                ]])
                                
                                -- -- find the year drop down
                                local year_drop_dimensions = get_element"""
