# -*- coding: utf-8 -*-
import scrapy
from seiya.spider.items import HouseItem
import re

class HousesSpider(scrapy.Spider):
	name = 'houses'
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
		'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'zh-CN',
		'Cache-Control':' max-age=0',
		'cookie' : '_jzqc=1; sajssdk_2015_cross_new_user=1; _smt_uid=5f09c00f.9ae9a73; lianjia_ssid=90a36952-6ea5-42c8-9741-1cfec0311c46; _jzqb=1.1.10.1594474512.1; _jzqckmp=1; UM_distinctid=1733e163f21115-0a8c1cea987f3d-784a5935-1fa400-1733e163f22e3; lianjia_uuid=782f7148-db9e-48fb-b26c-18b706db3dd2; _jzqa=1.2353636321855826000.1594474512.1594474512.1594474512.1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221733e16437a243-0edf2407f56f2a-784a5935-2073600-1733e16437b3f6%22%2C%22%24device_id%22%3A%221733e16437a243-0edf2407f56f2a-784a5935-2073600-1733e16437b3f6%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _gid=GA1.2.933260852.1594474515; _ga=GA1.2.1742153482.1594474515; select_city=350200; _qzjc=1; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiNDcxZTFiNTJmZWM0NjY3YWUwNDY2OGNhNTZkODM5YmNmMTQxNjJmZjUzYjRmOGUxYTIyN2UwNDBjZmU2YWQ5ZWVlNzM5ZTAzMWE1ZDk3NGEyNWUwYjYyOGU1NmMwNDM5ODlkNTlmZjM3NWUwZTU4YjM1NDRmODkyNWQyMzFmYjMxOTZmOTQyNWYyYTE1ZGU0MzhkZjJmZmQ0YmFiNDM5M2QyZmRiZTI4NjA2MGFiZDk4Yzc2Zjc3MDhkZDQwNmM2M2QxNmFhOWI3MDE3NGFmYWQxM2FlOGQyMjgyNmIyZmVmOThjZWJjZmM3MWU4OWYzMDI3ZWE3OWIxZTcxZWZkZjhhNGM0YWMzZjJkMThkNDczYzQwMTRiZTg0OGNiYmE0ZTM3OWMxOTc3MzRiMTE0OWY0MGNkNjUzMjc4ODU5YjRcIixcImtleV9pZFwiOlwiMVwiLFwic2lnblwiOlwiNDczZTc2ZGVcIn0iLCJyIjoiaHR0cHM6Ly94bS5saWFuamlhLmNvbS96dWZhbmcvIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0=; _qzjb=1.1594474512249.1.0.0.0; _qzjto=1.1.0; CNZZDATA1254525948=971081285-1594471717-%7C1594471717; CNZZDATA1255604082=797618328-1594473282-%7C1594473282; _qzja=1.1312602960.1594474512249.1594474512249.1594474512249.1594474512249.1594474512249.0.0.0.1.1; CNZZDATA1255633284=1570167590-1594470492-%7C1594470492; CNZZDATA1255847100=475982576-1594474199-%7C1594474199'
		}

	def start_requests(self):
		# 自动翻30页
		urls = [
		'https://xm.lianjia.com/zufang/pg{}/'.format(i) for i in range(1, 100)]   # 自动翻100页

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

	def parse(self, response):
		for house in response.css('div.content__list--item'):
			zz = house.css('div.content__list--item--main a::text').extract_first().split('·')[0].strip()
			if zz != '整租':     # 判断是否为整租，如果不是就跳过
				continue
			else:
				house_name = house.css('p.content__list--item--des a::text').extract()[2]   # 这里是个列表，小区名在第三个a标签里
				house_type = house.css('p.content__list--item--des::text').extract()[6].strip()
				#print('-------type-------')
				#print(house_type)
				min_area = house.css('p.content__list--item--des::text').extract()[4].strip().strip('㎡')
				#print('-------area-------')
				#print(min_area)
				# 有两种类型，1：55－77；2：55； 利用split('-')分割后取列表第 一个值，无论哪种情况都能取到最前面的值，即最小面积
				house_area = min_area.split('-')[0]
				
				rent = house.css('span.content__list--item-price em::text').extract_first()

				yield HouseItem(
					house_name = house_name.strip(),
					house_type = house_type,
					house_area = int(house_area),
					rent = int(rent)
					)
			





