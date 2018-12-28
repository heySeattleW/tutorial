import scrapy
from tutorial.items import CourseItem


class MockSpider(scrapy.Spider):
    name = 'MockSpider'
    # 允许访问的域
    allowed_domains = ['imooc.com']
    # 爬取的地址
    start_urls = ['https://www.imooc.com/course/list']
    # 爬取方法

    def parse(self, response):
        # 实例化一个容器，保存爬取内容
        item = CourseItem()
        # 爬取，使用xpath方式选择信息，具体方法根据网页结构而定
        # 先获取每个课程的div
        for box in response.xpath('//div[@class="course-card-container"]'):
            # 获取每个div中课程的路径
            item['url'] = 'http://www.imooc.com' + box.xpath('.//@href').extract()[0]
            # 标题
            item['title'] = box.xpath('.//h3[@class="course-card-name"]/text()').extract()[0].strip()
            # 图片地址
            item['image_url'] = box.xpath('.//@src').extract()[0].strip()
            # 学生人数
            item['student'] = box.xpath('.//span/text()').extract()[1].strip()
            # 课程简介
            item['introduction'] = box.xpath('.//p/text()').extract()[0].strip()
            yield item

            # url跟进开始
            # 获取下一页的url信息
            url = response.xpath("//a[contains(text(),'下一页')]/@href").extract()
            if url:
                # 将信息组合成下一页的url
                page = 'http://www.imooc.com' + url[0]
                # 返回url
                yield scrapy.Request(page, callback=self.parse)
            # url跟进结束

