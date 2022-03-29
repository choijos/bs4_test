import os
import csv
import glob
import pyodbc

from scrapy import Spider
from scrapy.http import Request

def product_info(response, value):
    return response.xpath('//th[text()="' + value + '"]/following-sibling::td/text()').extract_first()

class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com'] # don't have http in this url
    start_urls = ['http://books.toscrape.com']

    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            absolute_url = response.urljoin(book)
            yield Request(absolute_url, callback=self.parse_book)

        # process next page
        # next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()
        # absolute_next_page_url = response.urljoin(next_page_url)
        # yield Request(absolute_next_page_url)


    def parse_book(self, response):
        title = response.css('h1::text').extract_first()
        price = response.xpath('//*[@class="price_color"]/text()').extract_first()
        image_url = response.xpath('//img/@src').extract_first()
        image_url = image_url.replace('../..', 'http://books.toscrape.com/')
        rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
        rating = rating.replace('star-rating ', '')
        description = response.xpath('//*[@id="product_description"]/following-sibling::p/text()').extract_first()

        # product information data points
        upc = product_info(response, 'UPC')
        product_type = product_info(response, 'Product Type')
        price_without_tax = product_info(response, 'Price (excl. tax)')
        price_with_tax = product_info(response, 'Price (incl. tax)')
        tax = product_info(response, 'Tax')
        availability = product_info(response, 'Availability')
        number_of_reviews = product_info(response, 'Number of reviews')


        yield {
            'title': title,
            # 'price': price,
            # 'image_url': image_url,
            'rating': rating,
            # 'description': description,
            'upc': upc,
            'product_type': product_type
            # 'price_without_tax': price_without_tax,
            # 'price_with_tax': price_with_tax,
            # 'tax': tax,
            # 'availability': availability,
            # 'number_of_reviews': number_of_reviews
        }

    def close(self, reason):
        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)

        server = 'localhost'
        db = 'first_test'
        username = 'sa'
        password = 'testingHuskies.123'

        con_string = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=' + server + ',1433;DATABASE=' + db + ';UID=' + username + ';PWD=' + password +';Encrypt=no;TrustServerCertificate=yes'

        con = pyodbc.connect(con_string)
        # mydb = MySQLdb.connect(host='localhost',user='root',passwd=,db='books_db')
        # cursor = mydb.cursor()
        cursor = con.cursor()

        csv_data = csv.reader(open(csv_file))

        row_count = 0
        for row in csv_data:
            if row_count != 0:
                # for ele in row:
                #     print(ele)
                st = "INSERT INTO books_table (rating, product_type, upc, title) VALUES ({}, {}, {}, {})".format(row[1], row[3], row[2], row[0])
                print(st)
                # cursor.execute("INSERT INTO books_table (rating, product_type, upc, title) VALUES ({}, {}, {}, {})".format(row[1], row[3], row[2], row[0]))
            row_count += 1
        
        con.commit()
        cursor.close()

        # scrapy crawl books -o items.csv