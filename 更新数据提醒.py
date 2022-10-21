import requests
import re
import openpyxl
import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from tkinter import messagebox

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
url='https://www.bkjx.sdu.edu.cn/sanji_list.jsp?totalpage=154&PAGENUM=1&urltype=tree.TreeTempUrl&wbtreeid=1010'
#初始化，用于获取当前数据数量
def init():
    url='https://www.bkjx.sdu.edu.cn/sanji_list.jsp?totalpage=154&PAGENUM=1&urltype=tree.TreeTempUrl&wbtreeid=1010'
    page_data=requests.get(url=url,headers=headers).text
    times='<div style="float:right;">(.*?)</div>'
    times_data=re.findall(times,page_data,re.S)
    pagemax=int(re.findall('TD nowrap align=left width=1% id=fanye128813>.*?&nbsp;&nbsp;1/(.*?)&nbsp',page_data,re.S)[0])
    for i in range(2,pagemax+1):
        url='https://www.bkjx.sdu.edu.cn/sanji_list.jsp?totalpage=154&PAGENUM='+str(i)+'&urltype=tree.TreeTempUrl&wbtreeid=1010'
        times_data.extend(re.findall(times,page_data,re.S))
    return len(times_data)
init_data=init()
print(init_data)
#自动
def getInfo():
    global init_data
    if init()!=init_data:
        print("数据已更新，正在获取")
        url='https://www.bkjx.sdu.edu.cn/sanji_list.jsp?totalpage=154&PAGENUM=1&urltype=tree.TreeTempUrl&wbtreeid=1010'
        page_data=requests.get(url=url,headers=headers).text
        #获取第一页的title、link、times
        links='div style="float:left"><a href="(.*?)"'
        titles='target=_blank title="(.*?)" style='
        times='<div style="float:right;">(.*?)</div>'
        links_data=re.findall(links,page_data,re.S)
        titles_data=re.findall(titles,page_data,re.S)
        times_data=re.findall(times,page_data,re.S)
        #对不完整的链接进行修正
        for i in range(len(links_data)):
            if re.findall('(.*?)content',links_data[i],re.S)==['']:
                links_data[i]='https://www.bkjx.sdu.edu.cn/'+links_data[i]
        print(titles_data[0])
        print(times_data[0])
        print(links_data[0])
        messagebox.showinfo(title= '山大消息已更新',message=titles_data[0]+'\n'+times_data[0]+'\n'+links_data[0])
        init_data=init()
    else:
        print("数据未更新")

sched = BlockingScheduler()
sched.add_job(getInfo, 'interval', minutes=1)
sched.start()