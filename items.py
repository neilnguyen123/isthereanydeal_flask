# Define here the models for your scraped items

# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# Temporary container
class IsthereanydealItem(scrapy.Item):
    # define the fields for your item here like:
    game_title = scrapy.Field()
    game_store_name = scrapy.Field()
    game_date = scrapy.Field()
    game_regular_price = scrapy.Field()
    game_actual_price = scrapy.Field()
    sale_duration = scrapy.Field()
    game_release_date = scrapy.Field()
    pass
