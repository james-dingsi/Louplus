# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from flask_doc.items import FlaskDocItem

class FlaskSpider(scrapy.Spider):
    name = 'flask'
    allowed_domains = ['flask.pocoo.org']
    start_urls = ['http://flask.pocoo.org/docs/1.0/']
    rules = (
        Rule(LinkExtractor(allow='http://flask.pocoo.org/docs/1.0/.*'), callback='parse', follow=True)
        )

    def parse(self, response):
        item = FlaskDocItem()
        item['url'] = response.url
        item['text'] = ' '.json(response.xpath('//text()').extract())
        yield item
