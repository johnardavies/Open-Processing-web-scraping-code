# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy.item import Item, Field

class RascrapeItem(Item): #Inherits from the item class
  name = Field()
  address = Field()
  status = Field()
  region=Field()
  
