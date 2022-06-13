# coding: utf-8

from bs4 import BeautifulSoup
# from urllib2 import urlopen
import re
import requests
# import webbrowser
import pandas as pd


# # 林草

keyword = u"退耕还林"
url_base = "http://www.forestry.gov.cn"
url_index = "/sites/main/main/gov/govindex.jsp"

param = {
    'p': '1', 
    'textfield2': '', 
    'startdt': '2002-01-01', 
    'stopdt': '2099-12-30', 
    'govtypeid': '0', 
    'typeid': '0', 
    'page': 1
}

all_title = []
all_href = []
all_date = []
all_number = []

param['textfield2'] = keyword
r = requests.get(url_base+url_index, params=param)
soup = BeautifulSoup(r.text, features='lxml')
all_page = soup.find_all('span', {'style': "border: 1px solid #CCCCCC; font-size: 12px; line-height: 28px; margin: 8px 0; overflow: hidden; padding: 3px 5px; text-decoration:none; color:#000;"})
mpage = int(re.findall(r"\d+", all_page[0].text)[0])
print(u"搜索关键词：%s，共 %d 页" %(keyword, mpage) )


for page in range(1, mpage+1):
    print(u"正在爬取第 %d 页" % page)
    if(page != 1):
        param['page'] = page
        r = requests.get(url_base+url_index, params=param)
        soup = BeautifulSoup(r.text, features='lxml')
    
    all_document_a = soup.find_all('a', {'class': 'tooltip'})
    all_title.extend([d.get_text() for d in all_document_a])
    all_href.extend([d['href'] for d in all_document_a])

    all_date_td = soup.find_all('td', {'class':'border_bottom_c2ceb3', 'width':'100'})
    all_date.extend([d.get_text() for d in all_date_td])

    all_number_td = soup.find_all('td', {'class':'border_bottom_c2ceb3', 'width':'130'})
    all_number.extend([d.get_text() for d in all_number_td])
print(u"完成！")

all_href = [url_base+h for h in all_href]

df = pd.DataFrame({
    u"公文名称": all_title, 
    u"发文日期": all_date, 
    u"文号": all_number, 
    u"正文链接": all_href
})

column = [u"公文名称", u"发文日期", u"文号", u"正文链接"]

savename = u"信息公开-林草-"+keyword+".csv"
df.to_csv(savename, index=False, encoding='utf_8_sig', columns=column)
print(u"文件 %s 已保存。" %(savename))