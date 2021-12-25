import json
import requests
import sys
import importlib
importlib.reload(sys)

def searchLatitudeLongitude(block,city='上海'):
    # 根据地址获取对应经纬度，通过高德地图的api接口来进行
    cityLocation = city + block
    # print(cityLocation)
    base = 'https://restapi.amap.com/v3/geocode/geo?key=5613dda51e29e4bcb84bddfd7d032325&address=' + cityLocation
    response = requests.get(base)
    result = json.loads(response.text)
    info = result['geocodes'][0]['location']

    return info
    # with open('G:/新建文件夹/pc/image/a.csv', 'a', encoding='utf-8')as data:
    #     print(str(info), file=data)
if __name__ == '__main__':
    block = '金海岸花园'
    info = searchLatitudeLongitude(block)
    print(info)
