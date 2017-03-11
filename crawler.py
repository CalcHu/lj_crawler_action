import requests
from bs4 import BeautifulSoup
import re
import csv
import json
import time

def get_city_info(city_id):
    # url = 'https://m.lianjia.com/mapi/dict/city/Info?city_id={}'.format(city_id)
    # res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36','Upgrade-Insecure-Requests': 1}).json()
    with open('Info.json', 'r') as fi:
        res = json.load(fi)
    return {'subway_line': res['data']['info'][0]['subway_line'], 'district': res['data']['info'][0]['district']}

def get_apartment_list_by_bizcircle(district_info):
    feature_set = set()
    ershoufang_base_url = 'https://m.lianjia.com/bj/ershoufang/'

    for district in district_info:

        for biz_circle in district['bizcircle']:
            result = []
            page = 1
            id_re = '(?P<id>\d+).html'
            price_re = '(?P<num>\d+)'
            while True:
                xhr = get_xhr_info('{}{}/pg{}?_t=1'.format(ershoufang_base_url, biz_circle['bizcircle_quanpin'], page))
                body = BeautifulSoup(xhr['body'], "html.parser")
                apartment_list = body.find_all('li', class_="pictext")
                for apartment in apartment_list:
                    key_list = [re.search(id_re, apartment.a['href']).group('id'), district['district_name'], biz_circle['bizcircle_name']]
                    #key_list.append(re.search(id_re, apartment.a['href']).group('id'))
                    item_list_div = apartment.find('div',class_='item_list')
                    key_list.extend(item_list_div.find('div', class_='item_other text_cut').get_text().split('/'))
                    price_total = item_list_div.find('div', class_='item_minor').find('span',class_='price_total').get_text()
                    match = re.search(price_re, price_total)
                    if match:
                        price_total = match.group('num')
                    unit_price = item_list_div.find('div', class_='item_minor').find('span',class_='unit_price').get_text()
                    match = re.search(price_re, unit_price)
                    if match:
                        unit_price = match.group('num')
                    key_list.extend([price_total,unit_price])
                    tag_spans = item_list_div.find('div', class_="tag_box").find_all('span')
                    tags = []
                    for span in tag_spans:
                        tag_name = span['class'][1]
                        feature_set.add(tag_name)
                        tags.append(tag_name)
                    key_list.append(','.join(tags))
                    result.append(key_list)

                if xhr['no_more_data']:
                    break

                page += 1
            with open('stocks.csv', 'w', encoding='utf8') as f:
                f_csv = csv.writer(f)
                #f_csv.writerow(headers)
                f_csv.writerows(result)
            #break
            time.sleep(10)
        #break
    print(feature_set)
    #headers = ['id', 'district', 'Trading Area', 'shape', 'area', 'orientations', 'community', 'total price', 'unit price', 'features']





def get_xhr_info(url):
    r =  requests.get(url, headers={'X-Requested-With': 'XMLHttpRequest', 'Upgrade-Insecure-Requests': 1})
    # print (url)
    # print (r)
    # exit()
    try:
        return r.json()
    except Exception:
        print (r.text)
        exit()
    # return requests.get(url, headers={'X-Requested-With': 'XMLHttpRequest'}).json()


beijing_city_info = get_city_info('110000')
get_apartment_list_by_bizcircle (beijing_city_info['district'])
# base_url = 'https://m.lianjia.com/bj/ershoufang'
# host = 'https://m.lianjia.com'
# list_url = "{}/pg1/?_t=1".format(base_url)
# res = requests.get(base_url, headers={'X-Requested-With': 'XMLHttpRequest'}).json()
# #print (res['args'])
# soup = BeautifulSoup(res['body'],"html.parser")
# pictexts = soup.find_all('li',class_="pictext")
# for li in pictexts:
#     detail_url = "{}{}".format(host, li.a['href'])
#     detail = requests.get(detail_url).text
#     s = BeautifulSoup(detail,"html.parser")
#     divs = s.find_all('div',class_="similar_data_detail")
#     _li = []
#     for div in divs:
#         _li.append(div.find('p',class_='red big').get_text())
#     _ul = s.find('ul', class_='house_description big lightblack')
#     short_lis = _ul.find_all('li',class_='short')
#     # print(_ul)
#     for short_li in short_lis:
#         _li.append(short_li.get_text().split('：')[1])
#     layer_div = s.find('div', class_='info_layer')
#     for ul_ in layer_div.find_all('li',class_='info_li'):
#         _li.append(ul_.find('p', class_='info_content deep_gray').get_text())
#         #'assafd'.split('s')
#     print (_li)
#     break
