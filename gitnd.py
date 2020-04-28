# -*- coding: utf-8 -*-
import scrapy
from git.items import GitItem

class GitndSpider(scrapy.Spider):
	name = 'gitnd'

	@property
	def start_urls(self):
		url_list = url_list = ['https://github.com/shiyanlou?tab=repositories',
					'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK0MjAxNy0wNi0wN1QwMDozMzozN1rOBZKTIQ%3D%3D&tab=repositories',
					'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK0MjAxNy0wNi0wNlQwNToxNToyMlrOBZI5zw%3D%3D&tab=repositories',
					'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK0MjAxNC0xMi0xNlQwMjo0MTowMlrOAaxFrA%3D%3D&tab=repositories',
					'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK0MjAxNC0xMS0wM1QwMDo1OToxMVrOAY4E1w%3D%3D&tab=repositories'
					]
		return url_list


	def parse(self, response):
		for git in response.css('li.col-12'):
			# 获取h3标签属性为wb-break-all下的a标签的文本
			item = GitItem({
					'name': git.css('h3.wb-break-all a::text').extract_first().strip(),
					'update_time': git.css('relative-time::attr(datetime)').extract_first()
					})
			yield item
					
					
