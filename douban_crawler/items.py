# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanCrawlerItem(scrapy.Item):
    title = scrapy.Field()
    detail_url = scrapy.Field()
    director = scrapy.Field()
    cast = scrapy.Field()
    rating = scrapy.Field()
    num_reviews = scrapy.Field()
