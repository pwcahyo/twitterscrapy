# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TwitterscrapingItem(scrapy.Item):
	index = scrapy.Field()
	userid = scrapy.Field()	
	username = scrapy.Field()	
	fullname = scrapy.Field()
	text_tweet = scrapy.Field()
	original_text_tweet = scrapy.Field()
	max_position = scrapy.Field()
	hash_tags = scrapy.Field()
	time_tweet = scrapy.Field()
	lang = scrapy.Field()
	retweets = scrapy.Field()
	favorite = scrapy.Field()
	place_id = scrapy.Field()
	place = scrapy.Field()