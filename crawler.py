import requests
from bs4 import BeautifulSoup

base_url = 'https://m.lianjia.com/bj/ershoufang'
host = 'https://m.lianjia.com'
list_url = "{}/pg1/?_t=1".format(base_url)
res = requests.get(base_url, headers={'X-Requested-With': 'XMLHttpRequest'}).json()
#print (res['args'])
soup = BeautifulSoup(res['body'],"html.parser")
pictexts = soup.find_all('li',class_="pictext")
for li in pictexts:
    detail_url = "{}{}".format(host, li.a['href'])
    detail = requests.get(detail_url).text
    s = BeautifulSoup(detail,"html.parser")
    divs = s.find_all('div',class_="similar_data_detail")
    _li = []
    for div in divs:
        _li.append(div.find('p',class_='red big').get_text())
    _ul = s.find('ul', class_='house_description big lightblack')
    short_lis = _ul.find_all('li',class_='short')
    # print(_ul)
    for short_li in short_lis:
        _li.append(short_li.get_text().split('：')[1])
    layer_div = s.find('div', class_='info_layer')
    for ul_ in layer_div.find_all('li',class_='info_li'):
        _li.append(ul_.find('p', class_='info_content deep_gray').get_text())
        #'assafd'.split('s')
    print (_li)
    break