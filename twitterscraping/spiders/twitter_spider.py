from scrapy.spiders import Spider
from scrapy.http.request import Request
from scrapy.selector import Selector
from twitterscraping.items import TwitterscrapingItem
from scrapy.http.headers import Headers
from w3lib.html import remove_tags
import json

class TwitterSpider(Spider):
	index = 0
	start = '2016-01-30'
	end = '2016-02-01'
	name = "twitter"
	allowed_domains = ["twitter.com"]
	#=========================== PENTING===========================
	# url yang kedua digunakan untuk pengambilan data json, sesuaikan dengan reload yang dihasilkan url pertama agar mendapatkan id yang sesuai
	# url max 9 hari sebelum hari ini
	#==============================================================

	start_urls = [
		"https://twitter.com/search?f=tweets&vertical=default&q=%22demam%20berdarah%22%20OR%20dbd%20OR%20dhf%20OR%20%22dengue%20fever%22%20OR%20%22dengue%20hemorrhagic%22%20OR%20%22sakit%20db%22%20lang%3Aid%20since%3A"+start+"%20until%3A"+end+"&src=typd",
		"https://twitter.com/i/search/timeline?f=tweets&vertical=default&q=%22demam%20berdarah%22%20OR%20dbd%20OR%20dhf%20OR%20%22dengue%20fever%22%20OR%20%22dengue%20hemorrhagic%22%20OR%20%22sakit%20db%22%20lang%3Aid%20since%3A"+start+"%20until%3A"+end+"&src=typd&include_available_features=1&include_entities=1&max_position=TWEET-693931488786653185-693946387516542976-BD1UO2FFu9QAAAAAAAAETAAAAAcAAAASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA&reset_error_state=false"

    ]

	def parse(self, response):
		max_position = ''
		koma = ','
		headers = response.headers
		itemselector = Selector(response).xpath('//div[@class="content"]')

		if headers['Content-Type'] == 'application/json;charset=utf-8':
			data = json.loads(response.body)
			itemselector = Selector(text=data['items_html']).xpath('//div[@class="content"]')
			max_position = data['min_position']
			yield Request("https://twitter.com/i/search/timeline?f=tweets&vertical=default&q=%22demam%20berdarah%22%20OR%20dbd%20OR%20dhf%20OR%20%22dengue%20fever%22%20OR%20%22dengue%20hemorrhagic%22%20OR%20%22sakit%20db%22%20lang%3Aid%20since%3A"+self.start+"%20until%3A"+self.end+"&src=typd&include_available_features=1&include_entities=1&max_position="+max_position+"&reset_error_state=false", 
					callback=self.parse, 
					method="GET",)
		
		for sel in itemselector:
			self.index += 1
			item = TwitterscrapingItem()
			item['index'] = self.index
			item['userid'] = ''.join(
				map(unicode.strip, sel.xpath('div[@class="stream-item-header"]/a/@data-user-id').extract()))
			item['username'] = ''.join(
				map(unicode.strip, sel.xpath('div[@class="stream-item-header"]/a/span[@class="username js-action-profile-name"]/b/text()').extract()))
			item['fullname'] = ''.join(
				map(unicode.strip, sel.xpath('div[@class="stream-item-header"]/a/strong/text()').extract()))
			text_tweet = ''.join(
				map(unicode.strip, sel.xpath('p[@class="TweetTextSize  js-tweet-text tweet-text"]').extract()))
			item['text_tweet'] = remove_tags(text_tweet).replace('\n',' ').replace('\u',' ')
			item['original_text_tweet'] = text_tweet
			hash_tags = koma.join(
				map(unicode.strip, sel.xpath('p[@class="TweetTextSize  js-tweet-text tweet-text"]'
					'/a[@class="twitter-hashtag pretty-link js-nav"]').extract()))
			item['hash_tags'] = remove_tags(hash_tags)
			item['time_tweet'] = ''.join(
				map(unicode.strip, sel.xpath('div[@class="stream-item-header"]/small[@class="time"]/a/@title').extract()))
			item['lang'] = ''.join(
				map(unicode.strip, sel.xpath('p[@class="TweetTextSize  js-tweet-text tweet-text"]/@lang').extract()))
			retweets = ''.join(
				map(unicode.strip, sel.xpath('div[@class="stream-item-footer"]'
					'/div[@class="ProfileTweet-actionList js-actions"]'
					'/div[@class="ProfileTweet-action ProfileTweet-action--retweet js-toggleState js-toggleRt"]'
					'/button[@class="ProfileTweet-actionButton  js-actionButton js-actionRetweet"]'
					'/div[@class="IconTextContainer"]').extract()))
			item['retweets'] = remove_tags(retweets).strip()
			favorite = ''.join(
				map(unicode.strip, sel.xpath('div[@class="stream-item-footer"]'
					'/div[@class="ProfileTweet-actionList js-actions"]'
					'/div[@class="ProfileTweet-action ProfileTweet-action--favorite js-toggleState"]'
					'/button[@class="ProfileTweet-actionButton js-actionButton js-actionFavorite"]'
					'/div[@class="IconTextContainer"]').extract()))
			item['favorite'] = remove_tags(favorite).strip()
			item['place_id'] = ''.join(
				map(unicode.strip, sel.xpath('div[@class="stream-item-header"]/span[@class="Tweet-geo u-floatRight js-tooltip"]/a/@data-place-id').extract()))	
			item['place'] = ''.join(
				map(unicode.strip, sel.xpath('div[@class="stream-item-header"]/span[@class="Tweet-geo u-floatRight js-tooltip"]/a/span[@class="u-hiddenVisually"]/text()').extract()))	
			item['max_position'] = max_position

			yield item