# -*- coding: utf-8 -*-
import scrapy
import sys
sys.path.append('D:\\work\\toscrape_book\\toscrape_book')
from scrapy.linkextractors import LinkExtractor
from items import BookItem
from scrapy_redis.spiders import RedisSpider

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    #start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        le = LinkExtractor(restrict_css = 'article.product_pod h3')
        for link in le.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_book)

        #提取下一页
        le = LinkExtractor(restrict_css = 'ul.pager li.next')
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_book(self, response):
        book = BookItem()
        sel = response.css('div.product_main')
        book['name'] = sel.xpath('./h1/text()').extract_first()
        book['price'] = sel.xpath('(./p)[1]/text()').extract_first()
        book['review_rating'] = sel.css('p.star-rating::attr(class)').re_first('star-rating ([A-Za-z]+)')
                                #sel.css('p.star-rating::attr(class)').re_first('star-rating (A-Za-z]+)')
        sel = response.css('table.table.table-striped')
        book['upc'] = sel.xpath('(.//tr)[1]/td/text()').extract_first()
        book['stock'] = sel.xpath('(.//tr)[6]/td/text()').re_first('\((\d+) available\)$')
        book['review_num'] = sel.xpath('(.//tr)[7]/td/text()').extract_first()

        yield book
 