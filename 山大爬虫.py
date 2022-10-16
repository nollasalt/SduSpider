import requests
import re
import datetime
import openpyxl
import os

url = 'https://www.bkjx.sdu.edu.cn/sanji_list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1010'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
page_data = requests.get(url=url, headers=headers).text

links='div style="float:left"><a href="(.*?)"'
titles='target=_blank title="(.*?)" style=""'
links_data=re.findall(links,page_data,re.S)
titles_data=re.findall(titles,page_data,re.S)

for i in range(len(links_data)):
    if re.findall('(.*?)content',links_data[i],re.S)==['']:
        links_data[i]='https://www.bkjx.sdu.edu.cn/'+links_data[i]

#for link in titles_data:
#    print(link)
print(len(links_data))
print(len(titles_data))

