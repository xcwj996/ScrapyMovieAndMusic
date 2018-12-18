# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    # 电影名字
    name = scrapy.Field()
    # 电影信息
    info = scrapy.Field()
    # 评分
    rating = scrapy.Field()
    # 评论人数
    num = scrapy.Field()
    # 经典语句
    quote = scrapy.Field()
    # 电影图片
    img_url = scrapy.Field()
    #电影跳转链接
    movie_url = scrapy.Field()
