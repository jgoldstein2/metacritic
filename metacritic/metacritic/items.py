# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MetacriticItem(scrapy.Item):
	Rank = scrapy.Field()
	Name = scrapy.Field()
	CriticR = scrapy.Field()
	CriticNum = scrapy.Field()
	UserR = scrapy.Field()
	UserNum = scrapy.Field()
	Network = scrapy.Field()
	SeasonDate = scrapy.Field()
	SeriesDate = scrapy.Field()
	Length = scrapy.Field()
	Genre = scrapy.Field()
	Seasons = scrapy.Field()