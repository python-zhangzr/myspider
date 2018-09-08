# -*- coding:utf-8 -*-
import threading
from Queue import Queue
from lxml import etree
import requests
import time
from UserAgentwithProxys import UserAgentwithProxy
import random

class ThreadCrawl1(threading.Thread):
    headers=None
    def __init__(self, threadName, crawlQueue1, crawlQueue2):
        super(ThreadCrawl1, self).__init__()
        self.threadName = threadName
        self.crawlQueue1 = crawlQueue1
        self.crawlQueue2 = crawlQueue2
        #self.headers = {"User-Agent" : "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}

    def run(self):
        print "启动 " + self.threadName
        while not CRAWL_EXIT1:
            try:
                url=self.crawlQueue1.get(False)
                useragent1 = random.choice(UserAgentwithProxy.user_agent_list)
        	headers={"User-Agent":useragent1}
        	#print headers
                content = etree.HTML(requests.get(url, headers = headers).text)
                link_list1 = content.xpath('//div[@id="pagelist"]//a/@href')
                #print link_list1
                for link in link_list1:
                    fulllink1 = "http://www.51voa.com/" + link
                    useragent2 = random.choice(UserAgentwithProxy.user_agent_list)
        	    headers={"User-Agent":useragent2}
        	    #print headers
                    content1 = etree.HTML(requests.get(fulllink1, headers = headers).text)
                    link_list2 = content1.xpath('//div[@id="list"]//ul/li/a/@href')
                    #print link_list2
                    for link in link_list2:
                        fulllink = "http://www.51voa.com" + link
                        self.crawlQueue2.put(fulllink)
                        #print fulllink
                print self.crawlQueue2.qsize()
            except:
                pass
        print "结束 " + self.threadName

class ThreadCrawl2(threading.Thread):
    headers=None
    def __init__(self, threadName, crawlQueue2, dataQueue):
        super(ThreadCrawl2, self).__init__()
        self.threadName = threadName
        self.dataQueue = dataQueue
        self.crawlQueue2 = crawlQueue2
        #self.headers = {"User-Agent" : "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}

    def run(self):
        print "启动 " + self.threadName
        while not CRAWL_EXIT2:
            try:
                url=self.crawlQueue2.get(False)
                useragent = random.choice(UserAgentwithProxy.user_agent_list)
        	headers={"User-Agent":useragent}
        	#print headers
                content = etree.HTML(requests.get(url, headers = headers).text)
                link= content.xpath('//div[@id="menubar"]/a[1]/@href')[0]
                self.dataQueue.put(link)
            except:
                pass
        print "结束 " + self.threadName

class ThreadParse(threading.Thread):
    headers=None
    def __init__(self, threadName, dataQueue):
        super(ThreadParse, self).__init__()
        self.threadName = threadName
        self.dataQueue = dataQueue
        #self.headers = {"User-Agent" : "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}

    def run(self):
        print "启动" + self.threadName
        while not PARSE_EXIT:
            try:
                link = self.dataQueue.get(False)
                self.parse(link)
            except:
                pass
        print "退出" + self.threadName

    def parse(self, url):
    	useragent = random.choice(UserAgentwithProxy.user_agent_list)
        headers={"User-Agent":useragent}
        #print headers
        mp3 = requests.get(url, headers = headers).content
        filename = url[-10:]
        with open('./images/'+filename, "wb") as f:
            f.write(mp3)
        print "已经成功下载 "+ filename
      
        
CRAWL_EXIT1 = False
CRAWL_EXIT2 = False
PARSE_EXIT = False

def main():
    crawlQueue1 = Queue()
    crawlQueue2 = Queue()
    dataQueue = Queue()

    url = "http://www.51voa.com/"
    useragent = random.choice(UserAgentwithProxy.user_agent_list)
    headers={"User-Agent":useragent}
    print headers
    #headers = {"User-Agent" : "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}
    content =etree.HTML(requests.get(url, headers = headers).text)
    link_list = content.xpath('//div[@id="left_nav"]//ul[2]/li/a/@href')
    for link in link_list:
        fulllink = "http://www.51voa.com" + link
        crawlQueue1.put(fulllink)
    print crawlQueue1.qsize()
    
    #crawlList1 = ["01号", "02号", "03号", "04号", "05号", "06号"]
    threadcrawl1 = []
    for Name in range(11):
        threadName="首先采集" + str(Name) + "号"
        thread = ThreadCrawl1(threadName, crawlQueue1, crawlQueue2)
        thread.start()
        threadcrawl1.append(thread)
    while not crawlQueue1.empty():
        pass
    global CRAWL_EXIT1
    CRAWL_EXIT1 = True
    print "crawlQueue1为空"
    for thread in threadcrawl1:
        thread.join()

    #crawlList2 = ["11号", "12号", "13号", "14号", "15号", "16号"]
    threadcrawl2 = []
    for Name in range(41):
        threadName="二次采集" + str(Name) + "号"
        thread = ThreadCrawl2(threadName, crawlQueue2,dataQueue)
        thread.start()
        threadcrawl2.append(thread)
    while not crawlQueue2.empty():
        pass
    global CRAWL_EXIT2
    CRAWL_EXIT2 = True
    print "crawlQueue2为空"
    for thread in threadcrawl2:
        thread.join()


    #parseList = ["01号", "02号", "03号", "04号", "05号", "06号","7号", "8号", 
                #"9号", "10号", "11号", "12号", "13号", "14号", "15号", "16号"]
    threadparse = []
    for Name in range(101):
        threadName="解析" + str(Name) + "号"
        thread = ThreadParse(threadName, dataQueue)
        thread.start()
        threadparse.append(thread)
    while not dataQueue.empty():
        pass
    global PARSE_EXIT
    PARSE_EXIT= True
    for thread in threadparse:
        thread.join()
    print "谢谢使用！"

if __name__ == "__main__":
    main()

