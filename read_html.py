import parsel
from scrapy import Selector
import re
import requests
import csv

# with open('上海二手房房源_上海二手房出售_买卖_交易信息(上海链家).html','r',encoding='utf-8') as f:
#     res = f.read()
# select = Selector(text=res)
#
# # title = select.xpath('//title/text()').extract_first()
# # print(title)
#
# li_select = select.xpath('.//ul[@class="sellListContent"]/li')
# for one_selector in li_select:
#     name = one_selector.xpath('.//div[@class="info clear"]/div[@class="title"]/a/text()').extract_first()
#     block = one_selector.xpath('.//div[@class="info clear"]/div[@class="flood"]/div/a[1]/text()').extract_first()
#     district = one_selector.xpath('.//div[@class="info clear"]/div[@class="flood"]/div/a[2]/text()').extract_first()
#     houseMessage = one_selector.xpath('.//div[@class="info clear"]/div[@class="address"]/div/text()').extract_first()
#     release_date = one_selector.xpath('.//div[@class="info clear"]/div[@class="followInfo"]/text()').extract_first()
#     totalPrice = one_selector.xpath('.//div[@class="info clear"]/div[@class="priceInfo"]/div[@class="totalPrice"]/span/text()').extract_first()
#     unitPrice = one_selector.xpath('.//div[@class="info clear"]/div[@class="priceInfo"]/div[@class="unitPrice"]/span/text()').extract_first()
#     print('-'*20)
#     print(name,block,district,houseMessage,release_date,totalPrice,unitPrice)
url = 'https://sh.lianjia.com/ershoufang/'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
response = requests.get(url=url, headers=headers)
html = response.text

selector = parsel.Selector(html)
lis = selector.css('.clear.LOGCLICKDATA')
for li in lis:
    item = {}
    item['title'] = li.css('.title a::text').get()
    item['block'] = li.css('.positionInfo a::text').getall()[0]
    item['district'] = li.css('.positionInfo a::text').getall()[1]
    item['houseMessage'] = li.css('.houseInfo::text').get()
    item['releaseDate'] = li.css('.followInfo::text').get()
    item['totalPrice'] = li.css('.totalPrice span::text').get()
    item['unitPrice'] = li.css('.unitPrice span::text').get()
    try:
        tag = []
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
    try:
        item['tag'] = '|'.join(tag)
    except:
        item['tag'] = ''
    item['title_url'] = li.css('.title a::attr(href)').get()

    # with open("ershouhouse.csv", mode='a', encoding="utf_8_sig", newline="") as f:
    #     csv_write = csv.writer(f)
    #     csv_write.writerow([item['title'], item['block'], item['district'], item['houseMessage'], item['releaseDate'],
    #                         item['totalPrice'], item['unitPrice'], item['tag'], item['title_url']])

    # file = open("ershouhouse.csv", "a", encoding="utf_8_sig")
    # print('enter process')
    # csvreader = csv.reader(file)
    # for row in csvreader:
    #     print(row)


    with open("ershouhouse.csv", "r", encoding="utf_8_sig") as f:
        reader = csv.reader(f)
        print(list(reader)[0][0])

    # print(item)