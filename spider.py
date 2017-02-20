# -*- coding:utf-8 -*-
import scrapy
import requests
import re
from lxml import etree
from scratext.items import ScratextItem
class MySpider(scrapy.Spider):
    name='sspider'
    handle_httpstatus_list = [404, 500]
    allowed_domains = ["dress.pclady.com.cn"]
    start_urls = ["http://dress.pclady.com.cn/stature/"]



    def parse(self, response):
        s = requests.session()
        s.keep_alive = False
        if response.status in self.handle_httpstatus_list:
            print 'sorry 404 404 404 404'
        url=response.url

        if 'stature' in url:#home page
            #find all urls
            #yield nextpage
            urls=response.xpath('//i[@class="iPic"]/a/@href').extract()
            for url in urls:
                yield scrapy.Request(url, self.parse)

            next_page = response.xpath('//div[@class="pclady_page"]/a[@class="next"]/@href')
            w=response.xpath('//div[@class="pclady_page"]/span/text()')

            if w <= 2:
                # 爬每一页
                yield scrapy.Request(next_page[0].extract(), self.parse)

        elif 'all' in url:

            item=ScratextItem()
            item['url']=[response.url]
            u=response.xpath('//td')
            s=u.xpath('string(.)').extract()
            print s

            item['text']=s
           # item['img']=response.xpath('//table//td//img/@#src').extract()

            yield item
            #scrapy items
        else:

            curl = response.xpath('//a[@class="viewAll"]/@href')[0].extract()
            yield scrapy.Request(curl, self.parse)

            # find all url
            # scrapy items


    def after_404(self, response):
        print response.url