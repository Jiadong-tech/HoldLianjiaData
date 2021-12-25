import scrapy
import parsel
import time
import random
import LatitudeLongitude
from scrapy import Selector
from HoldLianjia.items import HoldlianjiaItem

class MyhoneySpider(scrapy.Spider):
    name = 'MyHoney'
    # allowed_domains = ['https://sh.lianjia.com']
    # start_urls = ['http://sh.lianjia.com/']
    # start_urls = ['https://sh.lianjia.com/ershoufang/rs/']
    #
    # def parse(self, response):
    #     print(response.xpath('//ul[@class="sellListContent"]//li[@class="clear LOGCLICKDATA"]//div[@class="info clear"]//div[@class="title"]//a//text()'))
    current_page = 1 # from github

    # def start_requests(self):
    #     yield scrapy.Request(
    #         url='https://sh.lianjia.com/ershoufang/rs/',
    #         callback=self.parse2
    #     )

    def start_requests(self):
        yield scrapy.Request(
            # url='https://sh.lianjia.com/ershoufang/jingan',
            url='https://sh.lianjia.com/ershoufang/l2a2p2/',
            callback=self.parse2
        )
        # pass

    # def parse2(self,response):
    #     # data = response.xpath('//ul[@class="sellListContent"]//li[@class="clear LOGCLICKDATA"]//div[@class="info clear"]//div[@class="title"]//a//text()').extract()
    #     item = {}
    #     item['data'] = data
    #     print(data)
    #     # yield item
    def parse2(self, response):
        timeSleep = random.randint(0,6)
        time.sleep(timeSleep)
        print('-' * 10, 'timeSleep', timeSleep + 3)
        print('正在爬取第',self.current_page,'页')
        html = response.text
        # li_select = response.xpath('.//ul[@class="sellListContent"]/li')
        # for one_selector in li_select:
        #     item = HoldlianjiaItem()  # 生成对象
        #     item['name'] = one_selector.xpath(
        #         './/div[@class="info clear"]/div[@class="title"]/a/text()').extract_first()
        #     item['block'] = one_selector.xpath(
        #         './/div[@class="info clear"]/div[@class="flood"]/div/a[1]/text()').extract_first()
        #     item['district'] = one_selector.xpath(
        #         './/div[@class="info clear"]/div[@class="flood"]/div/a[2]/text()').extract_first()
        #     item['houseMessage'] = one_selector.xpath(
        #         './/div[@class="info clear"]/div[@class="address"]/div/text()').extract_first()
        #     item['release_date'] = one_selector.xpath(
        #         './/div[@class="info clear"]/div[@class="followInfo"]/text()').extract_first()
        #     item['totalPrice'] = one_selector.xpath(
        #         './/div[@class="info clear"]/div[@class="priceInfo"]/div[@class="totalPrice"]/span/text()').extract_first()
        #     item['unitPrice'] = one_selector.xpath(
        #         './/div[@class="info clear"]/div[@class="priceInfo"]/div[@class="unitPrice"]/span/text()').extract_first()
        selector = parsel.Selector(html)
        lis = selector.css('.clear.LOGCLICKDATA')
        for li in lis:
            item = {}
            item['title'] = li.css('.title a::text').get()
            item['block'] = li.css('.positionInfo a::text').getall()[0]
            item['district'] = li.css('.positionInfo a::text').getall()[1]
            print(item['district'])

            houseMessage = li.css('.houseInfo::text').get()
            print(houseMessage)

            item['houseType'] = houseMessage.split('|')[0].strip()
            item['houseArea'] = houseMessage.split('|')[1].strip()
            item['houseOrientation'] = houseMessage.split('|')[2].strip()
            item['houseCover'] = houseMessage.split('|')[3].strip()
            item['houseFloor'] = houseMessage.split('|')[4].strip()

            houseHistory = houseMessage.split('|')[5].strip()
            print(houseHistory)

            item['houseHistory'] = houseHistory if (('19' in houseHistory) or ('20' in houseHistory)) else ''
            item['houseStructure'] = houseMessage.split('|')[-1].strip()
            print(item['houseHistory'],'--',item['houseStructure'])

            releaseDate = li.css('.followInfo::text').get()
            print('releaseDate',releaseDate )
            item['houseFollowing'] = releaseDate.split('/')[0].strip()
            item['houseRelease'] = releaseDate.split('/')[1].strip()
            print(item['houseRelease'])
            item['totalPrice'] = li.css('.totalPrice span::text').get()
            print('totalPrice',item['totalPrice'])

            unitPrice = li.css('.unitPrice span::text').get()
            print('unitPrice1',unitPrice)
            # item['unitPrice'] = unitPrice.split('价')[1].split('元')[0].strip()
            item['unitPrice'] = unitPrice.split('元')[0].strip()
            print('unitPrice',item['unitPrice'])

            item['longitudeLatitude'] = LatitudeLongitude.searchLatitudeLongitude(item['block'])
            print(item['longitudeLatitude'] )
            item['"longitudeLatitude"'] = '"'+item['longitudeLatitude'] +'"'
            print('item',item)

            tag = []
            try:
                tag1 = li.css('.tag span::text').getall()[0]
                tag.append(tag1)
                tag2 = li.css('.tag span::text').getall()[1]
                tag.append(tag2)
                tag3 = li.css('.tag span::text').getall()[2]
                tag.append(tag3)
                tag4 = li.css('.tag span::text').getall()[3]
                tag.append(tag4)
                tag5 = li.css('.tag span::text').getall()[4]
                tag.append(tag5)
            except:
                pass
            print(tag)
            item['houseVR'] = self.findTag(tag, 'VR')
            item['houseAge'] = self.findTag(tag, '房本')
            item['anytime'] = self.findTag(tag, '随时')
            item['subway'] = self.findTag(tag, '地铁')

            item['title_url'] = li.css('.title a::attr(href)').get()
            print(item)
            # #生成详情页面请求对象
            # yield scrapy.Request(url, meta={"item": item}, callback=self.property_parse)
            yield item

        if (int(self.current_page)<101):
            self.current_page = int(self.current_page)+1
            # next_urls = f"https://sh.lianjia.com/ershoufang/jingan/pg{self.current_page}/"
            next_urls = f"https://sh.lianjia.com/ershoufang/pg{self.current_page}l2a2p2/"
            yield scrapy.Request(
                next_urls,
                callback=self.parse2, dont_filter=True
            )
        pass

    def findTag(self,tagList, flag):
        for tag in tagList:
            if flag in tag:
                return tag
        return ''