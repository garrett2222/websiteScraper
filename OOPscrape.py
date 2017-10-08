from multiprocessing import Pool
import threading
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import time
import winsound
import webbrowser

class Site:
 #INITIALIZE SELF
     def __init__(self, name, url, viewing_url, tag, number_tag, ticker):
         self.name=name
         self.url=url
         self.viewing_url=viewing_url
         self.tag=tag
         self.number_tag=number_tag
         self.ticker=ticker
         self.fails = 0

 # FINDING TOOL
     def findnth(self, haystack, needle, n):
         parts = haystack.split(needle, n + 1)
         if len(parts) <= n + 1:
             return -1
         return len(haystack) - len(parts[-1]) - len(needle)

 # TICKER FINDING FUNCTIONS
     def citronTicker(self):
         nasdaq = "NASDAQ"
         nyse = "NYSE"

         self.textBody = str(self.soup.find_all(self.tag)[self.number_tag])

         if self.textBody.find(nyse) != -1:
             startIndex = self.textBody.find(nyse) + 5
             endIndex = self.textBody[startIndex:startIndex + 10].find(")")
             self.tickerShort = self.textBody[startIndex: startIndex + endIndex]
             print self.tickerShort
         else:
             startIndex = self.textBody.find(nasdaq) + 7
             endIndex = self.textBody[startIndex:startIndex + 10].find(")")
             self.tickerShort = self.textBody[startIndex: startIndex + endIndex]
             print self.tickerShort

     def prescienceTicker(self):
         nasdaq = "NASDAQ"
         nyse = "NYSE"

         text = str(self.soup)
         textBody = text[self.findnth(str(self.soup), "<content:encoded>", 0):self.findnth(str(self.soup),
                                                                                      "</content:encoded>", 0)]

         if textBody.find(nyse) != -1:
             startIndex = textBody.find(nyse) + 5
             endIndex = textBody[startIndex:startIndex + 10].find(")")
             ticker = textBody[startIndex: startIndex + endIndex]
             print ticker
         else:
             startIndex = textBody.find(nasdaq) + 7
             endIndex = textBody[startIndex:startIndex + 10].find(")")
             ticker = textBody[startIndex: startIndex + endIndex]
             print ticker

     def spruceTicker(self):
         text = str(self.soup)
         textBody = text[
                    self.findnth(str(self.soup), "<content:encoded>", 0):self.findnth(str(self.soup), "</content:encoded>", 0)]
         startIndex = textBody.find("(") + 1
         endIndex = textBody.find(")") - 18
         # endIndex = textBody[startIndex:startIndex + 10].find(" or 'the company'")
         ticker = textBody[startIndex: endIndex]
         print ticker

     def keywordCheck(self):
         keywords = ["activist", "deal", "merger", "shareholder", "takeover", "direct knowledge", "antitrust",
                     "anti-trust", "whistleblower", "ftc", "federal trade commision", "acquire", "acquiring",
                     "acquisition" "in talks", "buyout", "source"]
         matches=0

         for item in keywords:
             if item in self.newHeadline.lower():
                 matches +=1

         if matches>=1:
             return True
         else:
             return False


     # FUNCTION TO CHECK FOR CHANGE
     def check_action(self):
         Freq = 150  # Set Frequency To 2500 Hertz
         Dur = 2000  # Set Duration To 1000 ms == 1 second
         if self.newHeadline not in self.oldArray:
             print self.name
             print self.newHeadline
             print datetime.now()
             if "UPDATE" or "Update" or "update" not in self.newHeadline:
                 winsound.Beep(Freq, Dur)

             webbrowser.open(self.viewing_url, new=0, autoraise=True)

             if self.ticker == True:
                 if self.name=="Citron":
                     self.citronTicker
                 elif self.name=="Prescience":
                     self.prescienceTicker
                 elif self.name=="Sprucepoint":
                     self.spruceTicker

     def getsite(self):
         self.header = {
             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
         self.oldArray=[]
         self.response=requests.get(self.url, headers=self.header)
         self.soup=BeautifulSoup(self.response.content, "html.parser")
         self.oldArray=[self.soup.find_all(self.tag)[self.number_tag].text]
         self.loops=1

         print "\n \n \n \n "


         while True:
             self.loops+=1
             self.response = requests.get(self.url, headers=self.header)
             if str(self.response)!="<Response [200]>":
                 #print "bad response",self.name
                 time.sleep(.20)
                 self.fails+=1
                 #print self.fails
                 if self.fails>1:
                     #print self.fails
                     time.sleep(.20)
                 if self.fails>2:
                     #print self.fails
                     #print self.name
                     time.sleep(.4)
                 if self.fails>6:
                     #print self.fails
                     self.fails=0
                 continue
             #print self.name
             self.soup = BeautifulSoup(self.response.content, "html.parser")
             try:
                 self.newHeadline = self.soup.find_all(self.tag)[self.number_tag].text
             except IndexError:
                 self.newHeadline=self.oldArray[5]

             if self.name=="NYPost":
                 if Site.keywordCheck(self)==True:
                     Site.check_action(self)
             else:
                 Site.check_action(self)

             self.oldArray.append(self.newHeadline)
             if self.loops>6:
                 del self.oldArray[0]

             #print self.newHeadline


citron=Site("Citron","http://citronresearch.com/feed","http://citronresearch.com","title",1,True)
muddywaters=Site("Muddywaters","http://www.muddywatersresearch.com/research/","http://www.muddywatersresearch.com/research/","a",10,False)
prescience=Site("Prescience","http://www.presciencepoint.com/feed/", "http://www.presciencepoint.com/research/","title",2,True)
gotham=Site("Gotham","http://gothamcityresearch.com/research/feed","http://gothamcityresearch.com/research",'title',2,False)
bronte=Site("Bronte","http://brontecapital.blogspot.com/","http://brontecapital.blogspot.com/",'a',1,False)
spruce=Site("Sprucepoint","http://www.sprucepointcap.com/feed/","http://www.sprucepointcap.com/research/",'title', 1, True)
sirf=Site("Sirf","http://sirf-online.org/feed","http://sirf-online.org",'title',1,False)
nypost=Site("NYPost","http://nypost.com/feed/","nypost.com","title",2,False)

All=[citron,muddywaters,prescience,gotham,bronte,spruce, nypost]

threads=[]
for item in All:
    t=threading.Thread(target=item.getsite)
    threads.append(t)
    t.start()
for item in threads:
    item.join()