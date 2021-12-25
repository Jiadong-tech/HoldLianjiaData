# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv

class HoldlianjiaPipeline:
    # index = 0
    # file = None

    def __init__(self):
        pass
        # 打开文件，指定方式为写，利用第三个参数把csv写数据时产生的空行消除
        # self.file = open("house.csv",mode='a',encoding="utf_8_sig",newline="")
        # self.writer = csv.writer(self.f, dialect="excel")
    def open_spider(self, spider):
        # 以追加的方式打开文件
        # self.file = open("house.csv", "a", encoding="utf_8_sig",newline="")
        pass

    def process_item(self, item, spider):
        # 第一行写入列名
        # if (self.index == 0) :
        #     column_name="项目,小区,区县,房屋信息,发布时间,总价,单价,备注,url\n"
        #     # 将字符串写入文件中
        #     self.file.write(column_name)
        #     self.index = 1
        # # 获取item中各个字段，将其连接成一个字符串
        # home_str = item['name']+","+ \
        #            item['type'] + "," + \
        #            item['area'] + "," + \
        #            item['direction'] + "," + \
        #            item['fitment'] + "," + \
        #            item['elevator'] + "," + \
        #            item['total_price'] + "," + \
        #            item['unit_price'] + "," + \
        #            item['property'] + "\n"
        # # 将字符串写入文件中
        # self.file.write(home_str)
        print('pipeline 运行了')
        with open("wanted_ershouhouse.csv",mode='a',encoding="utf-8-sig",newline="") as f:
            csv_write = csv.writer(f)
            # column_name = "项目,小区,区县,房屋信息,发布时间,总价,单价,备注,url\n"
            csv_write.writerow(
                [item['title'], item['block'], item['district'],
                 item['houseType'],item['houseArea'],item['houseOrientation'],item['houseCover'],item['houseFloor'],
                 item['houseHistory'],item['houseStructure'],
                 item['houseFollowing'],item['houseRelease'],
                 item['totalPrice'], item['unitPrice'],item['longitudeLatitude'],item['"longitudeLatitude"'],
                 item['houseVR'], item['houseAge'],item['anytime'],item['subway'],
                 item['title_url']])
        return item

    # def close(self, spider):
    #     # 关闭文件
    #     self.file.close()
    #     pass
