import random
import re
import requests
import xlwt
from user_agent import get_user_agent
from 代理66 import get_ips
book = xlwt.Workbook(encoding='utf-8')
sheet = book.add_sheet("安居客",cell_overwrite_ok=True)
headers = {
        'user-agent': random.choice(get_user_agent()),
        'Accept-Encoding': 'gzip, deflate',
        'referer': 'https://shanghai.anjuke.com/',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', }
ip_list=get_ips()
##请求网站信息
def req():
    response = requests.get('https://sh.fang.anjuke.com/',headers=headers,proxies=random.choice(ip_list)) ##加请求头，更换ip,
    return response

#解析网站
def crawl():
    res = req()
    print(res.text)
    names = re.findall('<span class="items-name">(.*?)</span>',res.text,re.S)
    places = re.findall('<span class="list-map" target="_blank">\[&nbsp;(.*?)&nbsp;(.*?)&nbsp;\]&nbsp;(.*?)</span>',res.text,re.S)
    huxing_mianji_prices = re.findall('<a class="address"(.*?)<!-- 户型销控信息开关 -->',res.text,re.S)
    return names,places,huxing_mianji_prices

 ##解析户型等信息
def details():
    names,places,huxing_mianji_prices = crawl()
    huxing_list = []
    mianji_list = []
    prices_list = []
    for content in huxing_mianji_prices:
        strings = '户型：'
        strings1 = '建筑面积：'

        if strings in content:  #在每一块里寻找户型
            huxing = re.findall('户型：.*?<span>(.*?) ',content,re.S)[0]
        else:
            huxing = "无户型"
        huxing_list.append(huxing)

        if strings1 in content:   #在每一块里寻找面积
            mianji= re.findall('建筑面积：(.*?)</span>',content,re.S)[0]
        else:
            mianji = "无面积"
        mianji_list.append(mianji)

        price = re.findall('<p class="price(.*?)</p>', content, re.S)[0]
        prices_list.append(price)
    print(len(huxing_list),len(mianji_list),len(prices_list))
    return names,places,huxing_list,mianji_list,prices_list #返回户型,面积,价格

#清洗
def select_datas():
    names,places,huxing_list,mianji_list,prices_list = details()
    final_huxing = []
    final_mianji = mianji_list
    final_prices = []
    for i in range(len(huxing_list)):
        if "span" in huxing_list[i]:
            huxing_list[i]=huxing_list[i].replace('</span>','、').replace('/<span>','')
        else:
            pass
        final_huxing.append(huxing_list[i])

        if '-txt">' in prices_list[i]:
            prices_list[i] = prices_list[i].replace('-txt">','')
        if 'span' in prices_list[i]:
            prices_list[i] = prices_list[i].replace('<span>',':').replace('</span>','')
        if '">' in prices_list[i]:
            prices_list[i] = prices_list[i].replace('">','')
        final_prices.append(prices_list[i])
    return names,places,huxing_list,mianji_list,prices_list
    # print(len(names),len(places),len(huxing_list),len(mianji_list),len(prices_list))

#写入表格
def write_to_excel():
    names,places,huxing_list,mianji_list,prices_list=select_datas()
    sheet.write(0, 0, '小区名')
    sheet.write(0, 1, '地址')
    sheet.write(0, 2, '户型')
    sheet.write(0, 3, '面积')
    sheet.write(0, 4, '价格')
    for i in range(len(names)):
        name = names[i]
        place = places[i]
        huxing = huxing_list[i]
        mianji = mianji_list[i]
        price = prices_list[i]
        sheet.write(i+1 ,0 , name)
        sheet.write(i + 1, 1, place)
        sheet.write(i + 1, 2, huxing)
        sheet.write(i + 1, 3, mianji)
        sheet.write(i + 1, 4, price)
    book.save('上海安居客房价数据' + '.xls')

def main():
    write_to_excel()

if __name__ == "__main__":
    main()
