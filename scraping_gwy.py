# coding: utf-8

from bs4 import BeautifulSoup
import re
import requests
import pandas as pd


# # 国务院

keyword = u"西部大开发"
url_search = "http://sousuo.gov.cn/s.htm"

param = {
    't': 'zhengcelibrary', 
    'q': '', 
    'sortType': 1, 
    'searchfield': '', 
    'p': 0, 
    'n': 5
}

param['q'] = keyword

r = requests.get(url_search, params=param)
soup = BeautifulSoup(r.content, features='lxml')

all_page = soup.find_all('a', {'class': 'lastPage'})[0]
mpage = int(all_page['page'])+1

print(u"搜索关键词：%s，共 %d 页" %(keyword, mpage) )

all_title = []
all_href = []
all_type = []
all_date = []

# 从网页获取信息
for page in range(mpage):
    print(u"正在爬取第 %d 页" %(page+1))
    if(page != 0):
        param['p'] = page
        r = requests.get(url_search, params=param)
        soup = BeautifulSoup(r.content, features='lxml')

    all_document = soup.find_all('div', {'class': 'dys_middle_result_content_item'})
    for d in all_document:
        all_title.append(d.h5.text)
        all_href.append(d.a['href'])
        info = d.find('p', {'class': "dysMiddleResultConItemRelevant clearfix"}).find_all('span')
        all_type.append(info[0].text)
        all_date.append(info[1].text)
print(u"完成！")

# 保存所有信息
df = pd.DataFrame({
    u"公文名称": all_title, 
    u"正文链接": all_href, 
    u"文件类型": all_type, 
    u"发布日期": all_date
})

column = [
    u"公文名称", 
    u"正文链接", 
    u"文件类型", 
    u"发布日期"
]

savename = u"信息公开-国务院-"+keyword+".csv"
df.to_csv(savename, index=False, encoding='utf_8_sig', columns=column)
print(u"文件 %s 已保存。" %(savename))