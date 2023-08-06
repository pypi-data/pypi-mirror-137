import re
import requests
import time

class GetStockInfo():
    def __init__(self,API = 'tencent'):
        self.api = API
        
    def getHtmlText(self,url):
   
        try:
            r = requests.get(url, timeout = 30)
            r.raise_for_status()
        #r.encoding = r.apparent_encoding

            return r.text
        except:
            return ""

    def getStockInfo(self,code):									#修改为用腾讯API, 2022/1/21

        if self.api == 'tencent':
           
            url = "http://qt.gtimg.cn/q=" + code					# 腾讯URL
            stock = self.getHtmlText(url)
            time.sleep(1)
            return stock.split('~') 
        elif self.api == 'sina':                                    # 新浪待修复
            url = "http://hq.sinajs.cn/list=" + code
            stock = self.getHtmlText(url)
            time.sleep(1)
            stockInfo =  re.findall(r'"(.+?)"', stock)	
            return stockInfo[0].split(',')

    def getStockClosePrice(self,code):

        si = self.getStockInfo(code)
    
        return si[3]	

