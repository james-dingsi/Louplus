# -*- coding: utf-8 -*-
import scrapy
from seiya.spider.items import JobItem
import re

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    
    '''
    模仿登录后的cookie信息，直接从网站request中copy
    cookie copy from web->rightclick->network->refresh->position zhaopin->request headers..........

    '''
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding' : 'gzip, deflate, br',
    'accept-language' : 'zh-CN,zh;q=0.9',
    'cache-control' : 'no-cache',
    'cookie' : 'user_trace_token=20200629140130-73221d6a-7923-42be-bc6d-44f85091910a; _ga=GA1.2.1538005364.1593410490; LGUID=20200629140131-a361457d-7d7b-4b1c-832b-c7ef7cb94f7e; LG_HAS_LOGIN=1; hasDeliver=0; privacyPolicyPopup=false; RECOMMEND_TIP=true; index_location_city=%E5%85%A8%E5%9B%BD; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; gate_login_token=3a95f633e37d2826cbceca11e50798ffdea97ee6be8ddc27f463795eaddb837b; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217956372%22%2C%22%24device_id%22%3A%22172feb03044b5e-03e5598cc0c19b-4353760-2073600-172feb03045b50%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2283.0.4103.116%22%7D%2C%22first_id%22%3A%22172feb03044b5e-03e5598cc0c19b-4353760-2073600-172feb03045b50%22%7D; JSESSIONID=ABAAAECAAEBABIIECAB9F59E5CE1B0C66329A2681D7F9CE; WEBTJ-ID=20200702164123-1730eb00545126-05e2e11ef505fa-4353760-2073600-1730eb0054685; _putrc=EABCF29DE93B7811123F89F2B170EADC; _gid=GA1.2.675051096.1593679284; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1593410490,1593411024,1593498311,1593679284; login=true; unick=%E7%94%A8%E6%88%B74700; PRE_UTM=; PRE_HOST=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2F2%2F%3FfilterOption%3D2%26sid%3Ddf51718c3f0147759be67ed7d8788ef6; PRE_SITE=; LGSID=20200702192514-c9ceb638-ea3f-499f-ac0e-79b88ccf45aa; SEARCH_ID=33f013fd7db5447391c4494490102acc; X_HTTP_TOKEN=ccfd0ed94489805651198639516e062729bd93edfd; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1593689115; LGRID=20200702192515-82ed6c01-1fcc-4ec8-9f08-0918809c8cdc'
    }
    
    def start_requests(self):
        # 自动翻30页
        urls = [
        'https://www.lagou.com/zhaopin/{}/'.format(i) for i in range(1, 31)]   # 自动翻30页
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)
        

    def parse(self, response):
        for job in response.css('li.con_list_item'):
            title = job.css('div.p_top h3::text').extract_first()
            city = job.css('div.p_top em::text').extract_first().split('·')[0]

            salary = job.css('div.p_bot span.money::text').re('(\d+)k-(\d+)k')
            salary_list = salary if salary else [0, 0]
            salary_lower = int(salary_list[0])
            salary_upper = int(salary_list[1])
            # 使用extract()提取内容后产生列表,列表包含经验和教育2个内容，分别存储到两个变量中
            experience, education = job.css('div.p_bot div.li_b_l::text').extract()[2].split(' / ')
            # 匹配提取内容中的数字(如:经验1－3年 or 不限) 
            experience = re.findall('\d+', experience)
            # 如果存在,存入列表
            experience_list = experience if experience else [0, 0]
            # 空列表，则存入0～1
            experience_list = experience if len(experience) > 1 else [0, 1]
            # 经验1年以下，仅包含1个数字
            if len(experience) == 1:
                experience_list = [0, 1]
            # 通过列表索引存入对应字段 
            experience_lower = experience_list[0]
            experience_upper = experience_list[1]

            tags = ' '.join(job.css('div.list_item_bot span::text') .extract())   # it's a list
            company = job.css('div.company_name a::text').extract_first()

            yield JobItem(
                title = title,
                city = city,
                salary_lower = int(salary_list[0]),
                salary_upper = int(salary_list[1]),
                experience_lower = int(experience_list[0]),
                experience_upper = int(experience_list[1]),
                education = education.strip(),
                tags = tags,
                company = company
            )


