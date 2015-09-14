import scrapy
import urlparse
import re
import csv
from collections import defaultdict
from scrapy.contrib.spiders import BaseSpider,Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
#from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector  #Imports the html xpath selector
from userdetails.items import UserdetailsItem #Imports the processing items class that was created
import time

#This spider obtains user details from profile on the OpenProcessing website
class UserdetailsSpider(scrapy.Spider):
    name = "userdetailsspider"  #The name that you call the spider from the command line
    allowed_domains = ["openprocessing.org"]
    start_urls=['http://www.openprocessing.org/user/1/'] #The starting URL

    def __init__(self):
        self.page_number=1 #not used in this spider
        
    def start_requests(self):
      #Reads in a set of userids and then loops through them
      ifile  = open('filepath', "rb")
      reader =  csv.DictReader(ifile)
      names=defaultdict(list)
      for row in reader: #Loops through the user ids
         i=row['user_id']
         time.sleep(5)  #Adds in a 5 second delay
         URL='http://www.openprocessing.org/user/'+str(i)+'/'  #Creates the corresponding personal web page url
         print URL
         yield scrapy.Request(url=URL , callback= self.parse) #Calls the parsing function


    def parse(self, response):
            hxs = HtmlXPathSelector(response)
            items=[]
            item=UserdetailsItem()
            idd=response.url
            #Gets the user id info#######################################################################################
            idd=idd.replace("http://www.openprocessing.org/user/","").replace("/","") #strips away info to get the userid  
            item["ids"]=idd
            #Gets the website info#######################################################################################
            webs=hxs.xpath('//div[@id="userDetails"]/a/strong/text()').extract()
            item["website"]=webs
            #Gets the location information##################################################################################
            loc=hxs.xpath('//div[@id="userDetails"]/strong/text()').extract()
            item["location"]=loc
            #Gets the date joined info####################################################################################
            #What we are looking for in the joining data
            #<div id="userDetails"><blah blah>what we want </div>
            joined=hxs.xpath('//div[@id="userDetails"]/text()').extract()
            item["joined"]=joined
            #Gets the name of the person whose page it is which is in the title tag#######################################
            gd1=hxs.xpath('//title/text()').extract()  #Gets the title information for the page
            item["name"]=gd1
            #Gets the membership status data that we are looking for######################################################
            # Example <a href="/membership/" class="hangingBox" style="position:absolute; left: 10px;width: 72px; color:#ff9900; text-align:center; ">Professor+</a>
            gd2=hxs.xpath('//a[@href="/membership/"]/text()').extract()  
            gd2=str(gd2).replace(",","").replace("go","") #Cleans things up
            item["membership"]=gd2
            items.append(item)
            return items # returns the list

#This leaves some commas and extra text in the output, be good to rewrite to resolve the issue.

#################################################################################################################################################
######## Example of some of the data that we are looking for ####################################################################################
#################################################################################################################################################
#
#
#		<div id="userDetails" class="floatRight" style="width:260px; position:absolute; bottom:5px; right:0px; padding:5px 0;">#
#						&nbsp;<span class="iconicSprite iconic-map_pin_stroke_8x12"></span>
#                                            <strong>Brooklyn, NY</strong><br/>
#		    <span class="iconicSprite iconic-link_10x10"></span> <a href="http://wiredpieces.com" rel="nofollow" target="_blank">
#                                              <strong> http://wiredpieces.com</strong></a><br/>
#						<span class="iconicSprite iconic-user_9x12"></span>
#                                                 member since February 6, 2008</div>


