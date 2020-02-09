# -*- coding: utf-8 -*-
import scrapy
from budejie.items import BudejieItem

class BudejieScrapySpider(scrapy.Spider):
    name = 'budejie_scrapy'
    allowed_domains = ['budejie.com']
    start_urls = ['http://www.budejie.com/pic/1']

    def parse(self, response):
        duanziLis = response.xpath("//div[@class='j-r-list']/ul/li")
        #SelectoeList
        for duanziLi in duanziLis:
            #Selector
            author = duanziLi.xpath(".//a[@class='u-user-name']/text()").get()
            content = duanziLi.xpath(".//div[@class='j-r-list-c-desc']/a/text()").get()
            content = "".join(content)
            item = BudejieItem(author=author, content=content)
            duanzi = {"author":author, "content": content}
            yield item

        next_page = response.xpath("//a[@class='pagenxt']/@href").get()

        if not next_page:
            return
        else:
            next_url = "http://www.budejie.com/pic/" + str(next_page)
            print("next_url:"+next_url)
            yield scrapy.Request(next_url, callback=self.parse)

