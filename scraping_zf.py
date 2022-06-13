# coding: utf-8

from bs4 import BeautifulSoup
# from urllib2 import urlopen
import re
import requests
import webbrowser
import pandas as pd


# # 政府

keyword = u"西部大开发"
url_search = "http://sousuo.gov.cn/list.htm"

param = {
    'q': '',
    'n': 50, 
    'p': 0, 
    't': 'paper', 
    'sort': 'publishDate', 
    # childtype: 
    # subchildtype: 
    # pcodeJiguan: 
    # pcodeYear: 
    # pcodeNum: 
    # location: 
    'searchfield': 'title:content:pcode:puborg:keyword', 
    # title: 
    # content: 
    # pcode: 
    # puborg: 
    'timetype': 'timeqb'
    # mintime: 
    # maxtime: 
}

all_title = []
all_href = []
all_index = []
all_class = []
all_dept = []
all_date_f = []
all_number = []
all_date_p = []


param['q'] = keyword
r = requests.get(url_search, params=param)
soup = BeautifulSoup(r.text, features='lxml')
all_page = soup.find_all('span', {'class': 'jilu'})
mpage = int(re.findall(r"\d+", all_page[0].text)[0])
print(u"搜索关键词：%s，共 %d 页" %(keyword, mpage) )

for page in range(mpage):
    print(u"正在爬取第 %d 页" %(page+1))
    if(page != 0):
        param['p'] = page
        r = requests.get(url_search, params=param)
        soup = BeautifulSoup(r.content, features='lxml')

    all_document = soup.find_all('td', {'class': 'info'})
    
    for d in all_document:
#         all_title.append(d.a.text)
        all_href.append(d.a['href'])
        all_info = [re.findall(r"</strong>(.*?)</li>", str(i))[0] 
                    for i in BeautifulSoup(str(d), features="lxml").find_all('li')]
#         print type(all_info)
        all_index.append(all_info[0])
        all_class.append(all_info[1])
        all_dept.append(all_info[2])
        all_date_f.append(all_info[3])
        all_title.append(all_info[4])
        all_number.append(all_info[5])
        all_date_p.append(all_info[6])
print(u"完成！")

df = pd.DataFrame({
    u'公文名称': all_title, 
    u'正文链接': all_href, 
    u'主题分类': all_class, 
    u'发文机关': all_dept, 
    u'索引号': all_index, 
    u'发文字号': all_number, 
    u'成文日期': all_date_f, 
    u'发布日期': all_date_p
})

column = [
    u'公文名称', 
    u'正文链接', 
    u'主题分类', 
    u'发文机关', 
    u'索引号', 
    u'发文字号', 
    u'成文日期', 
    u'发布日期'
]

savename = u"信息公开-政府-"+keyword+".csv"
df.to_csv(savename, index=False, encoding='utf_8_sig', columns=column)
print(u"文件 %s 已保存。" %(savename))