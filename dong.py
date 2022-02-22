'''
Descripttion:
version: 0.x
Author: zhai
Date: 2022-02-22 13:10:40
LastEditors: zhai
LastEditTime: 2022-02-22 17:38:04
'''


import requests
import csv

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}

# 车型库


def Dongchedi(offset, limit, csv_writer):
    url = 'https://www.dongchedi.com/motor/brand/m/v6/select/series/?city_name=%E9%9D%92%E5%B2%9B'
    data = {
        'offset': '{}'.format(offset),
        'limit': limit,
        'is_refresh': 1,
        'city_name': '青岛'
    }

    response = requests.post(url, headers=headers, data=data).json()
    all_cak = response['data']['series']

    if len(all_cak) <= 0:
        print('out of range')

    for caks in all_cak:
        try:
            caks_id = caks['concern_id']
            caks_url = 'https://www.dongchedi.com/auto/series/' + \
                '{}'.format(caks_id)
            cak_name = caks['outter_name']
            print(cak_name, caks_url)
            Detail(caks_id, csv_writer)
        except Exception as error:
            print(error)
            continue


# 详情页
def Detail(caks_id, csv_writer):
    datail_url = 'https://www.dongchedi.com/motor/car_page/m/v1/series_all_json/?series_id=' + \
        str(caks_id) + '&city_name=青岛&show_city_price=1&m_station_dealer_price_v=1'
    response = requests.get(datail_url, headers=headers).json()

    series_all = response['data']
    online_name = series_all['online']
    for data_name in online_name:
        name_info = data_name['info']  # 全部车型模块所有数据
        try:
            if name_info['brand_name']:  # 判断是否为总型号
                series_name = name_info['name']  # 所有详细车型名称
                car_name = name_info['series_name']
                name = str(car_name) + '-' + str(series_name)
                # 指导价, 经销商报价 -价格字典
                price_info = name_info['price_info']
                dealer_price = str(price_info['official_price'])  # 指导价
                # official_price1 = name_info['dealer_price']  # 经销商报价
                # official_price = official_price1.replace('万', '')  # 去除 ‘万’
                # # 车主参考价 -价格字典
                # owner_price_summary = name_info['owner_price_summary']
                # naked_price_avg = owner_price_summary['naked_price_avg']  # 车主参考价
                # 保存数据库
                print(name, dealer_price)

                # 4. 写入csv文件内容
                csv_writer.writerow(
                    [name_info['brand_name'], name, dealer_price])

        except Exception as error:
            print('exception:', error)
            pass


def Run():
    pages = 120
    limit = 30

    # 1. 创建文件对象
    f = open('./output/汽车报价.csv', 'w', newline='', encoding='utf-8-sig')

    # 2. 基于文件对象构建 csv写入对象
    csv_writer = csv.writer(f)

    # 3. 构建列表头
    csv_writer.writerow(["品牌", "车型", "报价（万元）"])

    for offset in range(0, pages):
        try:
            Dongchedi(offset, limit, csv_writer)
        except Exception as error:
            print(error)

    # 5. 关闭文件
    f.close()


if __name__ == '__main__':
    try:
        Run()
    except Exception as error:
        print(error)
        pass
