import scrapy
import urlparse
import re
from scrapy.contrib.spiders import BaseSpider,Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
#from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector  #Imports the html xpath selector
from prouser.items import ProuserItem #Imports the processing items class that was created
import time

############################What this does##################################################
#Spider that goes through the Openprocessing users one at a time and obtains their followers
############################################################################################

class ProcessingSpider(scrapy.Spider):
    name = "prouserspider"  #The name that you call the spider from the command line
    allowed_domains = ["openprocessing.org"]
    start_urls=['http://www.openprocessing.org/user/1/followedBy'] #The starting URL
    #  The regex below matches the hyperlinks in the dated webpage if we want to crawl through the pages. This spider does not do that, so included for reference only
    # The pages are parsed by going through the galleries and clicking on the names of people
    #rules = (Rule(SgmlLinkExtractor(allow=(r'\d+'), callback="parse_links", follow=True ),)

    def __init__(self):
        self.page_number=1 #initialises the class with a page number of 1
        
    def start_requests(self):
        print 'hello'
        number_of_pages=10000 #This sets the number of pages that are looped through
        for i in range(self.page_number, number_of_pages, 1):  #Loops through the pages between page_number and number_of_pages
         time.sleep(5) #Adds in a 5 second time delay 
         URL='http://www.openprocessing.org/user/'+str(i)+'/followedBy'
         print URL
         yield scrapy.Request(url=URL , callback= self.parse)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        print hxs
        items=[]
        # The html we are looking for. We want the number e.g. 2083 from the below
        # <h3><a href="/user/2083/">Patrick May</a></h3>
        #The xpath expression below extracts the numeric userid of the user
        cities=hxs.xpath('//h3/a/@href').extract()
        for elem in cities: #loops through the returned titles
           item=ProuserItem()
           #This extracts the userid from the hyperlink, probably better with a regex
           name=response.url 
           name=key.replace("http://www.openprocessing.org/user/","") #This and the line below remove the text we don't want
           name=key.replace("/followedBy","")
           item["names"]=name
           elem=elem.replace("/","") #This and the line below remove the text we don't want
           elem=elem.replace("user","")        
           item["follower"]=elem
           items.append(item)#sticks the next returned list into the items list
        return items # returns the list










      
        
    
