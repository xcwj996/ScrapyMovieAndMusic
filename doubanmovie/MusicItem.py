import scrapy


class Music(scrapy.Item):
    name = scrapy.Field()
    hash = scrapy.Field()
    album_id = scrapy.Field()
