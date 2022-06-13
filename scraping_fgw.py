# coding: utf-8

# from bs4 import BeautifulSoup
# from urllib2 import urlopen
# import re
import requests
# import webbrowser
import pandas as pd
import json
import jsonpath


# # 发改委

keyword = u"西部大开发"
url_search = "https://so.ndrc.gov.cn/api/query"

param = {
    'qt': '',
    'tab': 'all', 
    'page': 1, 
    'pageSize': 50,
    'siteCode': 'bm04000fgk', 
    'key': 'CAB549A94CF659904A7D6B0E8FC8A7E9', 
#     startDateStr: 
#     endDateStr: 
    'timeOption': 0, 
    'sort': 'dateDesc'
}

param['qt'] = keyword
print(u"搜索关键词：%s" % keyword)

page = 1
all_title = []
all_href = []
all_date = []
mpage = 100

while page:
    param['page'] = page
    r = requests.get(url_search, params=param)
#     print page, r.status_code
    r_json = json.loads(r.content)
    if r.status_code == 200 and r_json['resultList']:
        print(u"正在爬取第 %d 页" % page)
        page += 1
        all_title.extend(jsonpath.jsonpath(r_json,"$..title"))
        all_href.extend(jsonpath.jsonpath(r_json,"$..url"))
        all_date.extend(jsonpath.jsonpath(r_json,"$..publishTime"))
    else:
        print(u"完成！")
        page = -1
        break
    if page == mpage:
        print(u"已达到最大页数 %d！" % mpage)
        page = -1
        break

# print all_date[0]

df = pd.DataFrame({
    u"公文名称": all_title, 
    u"正文链接": all_href, 
    u"发布日期": all_date
})

column = [
    u"公文名称", 
    u"正文链接", 
    u"发布日期"
]

savename = u"信息公开-发改委-"+keyword+".csv"
df.to_csv(savename, index=False, encoding='utf_8_sig', columns=column)
print(u"文件 %s 已保存。" %(savename))