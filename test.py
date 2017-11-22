#! /usr/bin/python3
from bs4 import BeautifulSoup
import requests,re
'''
基于beautifulSoup来爬取网页信息
'''
#图书馆网址
ROOT_URL = 'http://opac.ahau.edu.cn/opac/item.php?marc_no='
#伪造浏览器
def download_html(url):
    #伪造火狐浏览器
    headers = {'User-Agent':'Mozilla/5.0(X11;Ubuntu;Linux x86_64;rv:54.0)Gecko/20100101 Firefox/54.0'}
    return requests.get(url,headers=headers).content

#获取数据
def parse_html(html):
    #构造beautifulSoup对象
    soup = BeautifulSoup(html,'lxml')
    book_list = soup.find('div',attrs={'id':'tab_item'})

    result = []
    for val in book_list.find_all('table',attrs={'id':'item'}):
        tr = val.find_all('tr',attrs={'class':'whitetext'})
        add = {}
        isbn = []
        suoshuhao = val.find('td',attrs={'width':'10%'})
        #print(suoshuhao)
		#！！！要进行判定网页是否有我们想要的内容
        if(suoshuhao):
            suoshu = suoshuhao.getText()
        else :
            suoshu = -1
        add['suoshu'] = suoshu
        for val in tr:
            tiaomahao = val.find('td',attrs={'width':'15%'})
            if (tiaomahao):
                tiaoma = tiaomahao.getText()
                isbn.append(tiaoma)
            #print(tiaoma)
            #add[suoshu] = suoshu
            
        #print(name)
        #add['name'] = name
        add['tiaoma'] = ''.join(isbn)
        result.append(add)
        #print(result)
    return result

if __name__ == '__main__':
    result = []
    with open('lib2.txt','a') as file:
        for start in range(9965,9968):
            if start < 100:
                url = ROOT_URL + '00000000' + str(start)
                print(url)
            else:
                url = ROOT_URL + '000000' + str(start)
                print(url)
            html_data = download_html(url)
            for val in parse_html(html_data):
                #print(result)
                if(val['suoshu'] != -1):
                    string = val['suoshu']+'|'+val['tiaoma']
                    string = ''.join(string.split())
                    file.write(string+'\n')
