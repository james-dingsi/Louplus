# -*- coding: utf-8 -*-
import scrapy
from seiya.spider.items import RestItem
import re

class RestaurantsSpider(scrapy.Spider):
	name = 'restaurants'
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.9',
		'Cache-Control': 'no-cache',
		'cookie' : 's_ViewType=10; _lxsdk_cuid=17347a21d28c8-004eaf0e3cb222-4353760-1fa400-17347a21d28c8; _lxsdk=17347a21d28c8-004eaf0e3cb222-4353760-1fa400-17347a21d28c8; _hc.v=950bae06-9eb7-99f8-8334-434694806f65.1594634674; fspop=test; cy=15; cye=xiamen; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1594634674,1594693837; dplet=2749c6aacf020f70b6905f32340cdef1; dper=f18c99d60ac97382782cc064a9a9b13925e68c746ca62044f9519fafd5d179179f24dad0bb205a90f76a51f0d3e33172c97b57eaa1812eceb05cab52683953f24ba69bf753c3681b1992b2c7d3c1ff48369fb0453f83edacc61f33eae7415f3b; ll=7fd06e815b796be3df069dec7836c3df; ua=%E4%B8%81%E5%B7%B3_6042; ctu=679d4e5fd51b7bb5b35fb2edf421e536d2951af7b3ed8c1e46cef3db62080633; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1594712392; _lxsdk_s=1734c6ef7ba-d33-0bf-26f%7C%7C2'}

	def start_requests(self):
		# 自动翻30页
		urls = [
		'https://www.dianping.com/xiamen/ch10/p{}'.format(i) for i in range(1, 2)]   # 自动翻100页

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)
	'''
		这个问题多多，由于值不在一个标签里，所以没办法放到一 个循环里，但是分开for循环提取后，值会出现错乱
		使用xpath一直没有返回
	''' 
	def parse(self, response):
		'''
		for rest in response.xpath('//li[class=""]'):
			name = rest.css('div.tit h4::text').extract_first()
			evaluate_count = rest.css('div.nebula_star div::text').extract()[6]
			#print(name, evaluate_count)
		'''
		for rest in response.css('div.txt'):
			name = rest.css('div.tit h4::text').extract_first()
		for rest in response.css('div.comment'):
			evaluate_count = rest.css('div.nebula_star div::text').extract()[6]

			yield RestItem(
					name = name,
					evaluate_count = evaluate_count
					)


