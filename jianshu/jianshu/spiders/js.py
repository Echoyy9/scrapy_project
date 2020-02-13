# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu.items import ArticleItem

class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        #获取文章内容
        title = response.xpath("//h1[@class='_1RuRku']/text()").get()
        author = response.xpath("//span[@class='FxYr8x']/a/text()").get()
        img = response.xpath("//a[@class='_1OhGeD']/img/@src").get()
        pub_time = response.xpath("//div[@class='s-dsoj']/time/text()").get()
        origin_url = response.url
        article_id = response.url.split("/")[-1]
        content = response.xpath("//article[@class='_2rhmJa']").get()

        items = ArticleItem(
            title = title,
            author=author,
            img=img,
            pub_time=pub_time,
            article_id = article_id,
            content = content,
            origin_url =origin_url
        )

        yield items

