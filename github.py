#! use/env/bin python3
# -*- coding:utf-8 -*-
import scrapy
import json

class Github(scrapy.Spider):
    name = 'github'

    def start_requests(self):
        url_list = ['https://github.com/shiyanlou?tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK0MjAxNy0wNi0wN1QwMDozMzozN1rOBZKTIQ%3D%3D&tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK0MjAxNy0wNi0wNlQwNToxNToyMlrOBZI5zw%3D%3D&tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK0MjAxNC0xMi0xNlQwMjo0MTowMlrOAaxFrA%3D%3D&tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK0MjAxNC0xMS0wM1QwMDo1OToxMVrOAY4E1w%3D%3D&tab=repositories']
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 仓库名称是以Li标签作为节点来区分的，class属性为col-12
        for git in response.css('li.col-12'):
            # 获取h3标签属性为wb-break-all下的a标签的文本
            yield {
                'name': git.css('h3.wb-break-all a::text').extract_first().strip(),
                'update_time': git.css('relative-time::attr(datetime)').extract_first()
                }




            #           'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK0MjAxNy0wNi0wN1QwMDozMzozN1rOBZKTIQ%3D%3D&tab=repositories',
            #           'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK0MjAxNy0wNi0wNlQwNToxNToyMlrOBZI5zw%3D%3D&tab=repositories',
            #            'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK0MjAxNC0xMi0xNlQwMjo0MTowMlrOAaxFrA%3D%3D&tab=repositories',
            #            'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK0MjAxNC0xMS0wM1QwMDo1OToxMVrOAY4E1w%3D%3D&tab=repositories']
			
