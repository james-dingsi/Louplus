# -*- coding: utf-8 -*-
import scrapy
from git.items import GitItem

class NewgitSpider(scrapy.Spider):
    name = 'newgit'
    start_urls = ['http://github.com/shiyanlou?tab=repositories']

    def parse(self, response):
        for git in response.css('li.col-12'):
            item = GitItem({
                'name': git.css('h3.wb-break-all a::text').extract_first().strip(),
                'update_time': git.css('relative-time::attr(datetime)'
                        ).extract_first().strip()
            })
            info_url = git.css('a::attr(href)').extract_first()
            full_url = response.urljoin(info_url)
            request = scrapy.Request(full_url, self.parse_info)
            request.meta['item'] = item
            yield request
        url = response.css('a.btn-outline::attr(href)').extract()[-1]
        yield response.follow(url, callback=self.parse)

    def parse_info(self, response):

        item = response.meta['item']
        # 一次性把所需内容存入列表 
        cbr_list = response.xpath('//span[@class="num text-emphasized"]/text()'
                ).extract()
        # 判断列表是否存在，利用索引找到需要的内容存入item 
        if cbr_list:
            item['commits'] = cbr_list[0].replace(',', '').strip()
            item['branches'] = cbr_list[1].strip()
            item['releases'] = cbr_list[3].strip()
        yield item

