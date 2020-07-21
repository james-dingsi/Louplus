# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from flask_doc.items import FlaskDocItem

class FlaskSpider(scrapy.spiders.CrawlSpider):
    name = 'flask'
    allowed_domains = ['flask.palletsprojects.com']
    start_urls = ['https://flask.palletsprojects.com/en/1.0.x/']
    rules = (
        Rule(LinkExtractor(allow='https://flask.palletsprojects.com/en/1.0.x/.*'),
        callback='parse_page', follow=True),
        )
    # ['http://flask.pocoo.org/docs/1.0/']
    def parse_page(self, response):
        item = FlaskDocItem()
        item['url'] = response.url
        item['text'] = ' '.join(response.xpath('//text()').extract())
        yield item
