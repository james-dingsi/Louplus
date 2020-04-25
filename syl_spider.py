#! use/env/bin python3
# -*- coding:utf-8 -*-
import scrapy

class ShiyanlouCoursesSpider(scrapy.Spider):
        # 爬虫类要继承scrpy.Spider类
        # 在爬虫类中定义要请求的网站和连接以及如何从返回的网业提取数据等
        # name属性用于标识每个爬虫，各个爬虫类的name值不能相同
	name = 'shiyanlou-course'
        # start_requests的方法名字是固定的，不可更改

    '''
	def start_requests(self):
        # scrapy.Request接受一个url参数和一个callback参数
        # url指明要爬取的网页
        # callback是回调函数，用于处理返回的网页，它的值通常是一个提取数据的parse方法
		url_list = ['https://www.shiyanlou.com/courses/',
					'https://www.shiyanlou.com/courses/?page=2',
					'https://www.shiyanlou.com/courses/?page=3']
    	# 返回一个生成器,生成request对象，生成器是可迭代对象
		for url in url_list:
			yield scrapy.Request(url=url, callback=self.parse)
	'''

	def start_urls(self):
        # start_urls 需要返回一个可迭代对象，所以可写成列表、元组或生成器
		url_list = ['https://www.shiyanlou.com/courses/',
					'https://www.shiyanlou.com/courses/?page=2',
					'https://www.shiyanlou.com/courses/?page=3']
		return url_list

	def parse(self, response):
            # parse方法作为scrapy.Request的callback，用于提取数据
            # scrapy中的下载器会下载start_request中定义的每个Request
            # 并将结果封装为一个response对象传入这个方法

            # 遍历每个课程的div.col-md-3
            for course in response.css('div.col-md-3'):
			#使用css语法对每个course提取数据
                yield {
                    # 课程名称，使用strip方法去掉字符串前后的空白字符
					# 下面获取name的写法还可以省略h6的类属性，思考
                    'name': course.css('h6.course-name::text').extract_first().strip(),
					# 课程描述
                    'description': course.css('div.course-description::text').extract_first().strip(),
					# 课程类型
                    'typ':course.css('span.course-type::text').extract_first('免费').strip(),
					# 学生人数
                    'students': course.css('span.students-count span::text').extract_first().strip()
                    }



			
