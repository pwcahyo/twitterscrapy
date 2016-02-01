from scrapy.loader import ItemLoader
from twitterscraping.items import TwitterscrapingItem

class TwitterLoader(ItemLoader):
	default_item_class = TwitterscrapingItem
	input_processor=MapCompose(remove_tags),
	default_output_processor = TakeFirst()