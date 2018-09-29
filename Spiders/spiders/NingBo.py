# -*- coding: utf-8 -*-
from scrapy import Spider, Selector
from scrapy_redis.spiders import RedisSpider

from Spiders.items import SpidersItem, ElevatorLoader, OthersItem
from scrapy.http import Request

from Spiders.query import exist_num


class NingboSpider(RedisSpider):
    name = 'NingBo'
    allowed_domains = ['115.238.160.42:8077']
    start_urls = ['http://115.238.160.42:8077/scdeap/BQ/SB/{}']

    def parse(self, response):
        for url in range(1, 295639):
            if str(url) not in exist_num:
                if len(str(url)) < 6:
                    url = "0" * (6 - len(str(url))) + str(url)
                url = self.start_urls[0].format(url)
                yield Request(url, dont_filter=True, callback=self.parse_detail, meta={"num": int(url.split("/")[-1])})

    def parse_detail(self, response):
        identify_code = Selector(text=response.text)
        if '系统忙'not in response.text:
            identify_code = identify_code.xpath('//*[@id="main_basicid"]/div[1]/text()').extract_first()
            if identify_code != '识别码：':
                if "使用证编号" in response.text:
                    items = ElevatorLoader(item=SpidersItem(), response=response)
                    try:
                        items.add_css('identity_code', '#main_basicid > div:nth-child(1)::text')
                        items.add_css('reg_code', '#main_basicid > div:nth-child(2)::text')
                        items.add_css('equipment_name_num', '#main_basicid > div:nth-child(3)::text')
                        items.add_css('customer_addr', '#main_basicid > div:nth-child(4)::text')
                        items.add_css('customer_name', '#main_basicid > div:nth-child(5)::text')
                        items.add_css('expired_date', '#main_basicid > div:nth-child(6)::text')
                        items.add_css('manufacture_unit', '#main_basicid > div:nth-child(7)::text')
                        items.add_css('manufacture_name', '#main_basicid > div:nth-child(8)::text')
                        items.add_css('manufacture_product_id', '#main_basicid > div:nth-child(9)::text')
                        items.add_css('use_id', '#main_basicid > div:nth-child(10)::text')
                        result = items.load_item()
                        return result
                    except Exception as e:
                        print(e)
                elif "维保热线" in response.text:
                    items = ElevatorLoader(item=OthersItem(), response=response)
                    try:
                        items.add_css('identity_code', '#main_basicid > div:nth-child(1)::text')
                        items.add_css('reg_code', '#main_basicid > div:nth-child(2)::text')
                        items.add_css('equipment_name_num', '#main_basicid > div:nth-child(3)::text')
                        items.add_css('customer_addr', '#main_basicid > div:nth-child(4)::text')
                        items.add_css('customer_name', '#main_basicid > div:nth-child(5)::text')
                        items.add_css('equipment_parameter', '#main_basicid > div:nth-child(6)::text')
                        items.add_css('expired_date', '#main_basicid > div:nth-child(7)::text')
                        items.add_css('manufacture_unit', '#main_basicid > div:nth-child(8)::text')
                        items.add_css('maintain_unit', '#main_basicid > div:nth-child(9)::text')
                        items.add_xpath('phone', '//*[@id="main_basicid"]/div[10]/a/@href')
                        result = items.load_item()
                        return result
                    except Exception as e:
                        print(e)
            elif identify_code == '识别码：':
                print(response.meta['num'])
        else:
            print(response.text)
