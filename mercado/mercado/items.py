# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MercadoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #info de producto
    NP = scrapy.Field()
    VP = scrapy.Field()
    EV = scrapy.Field()

    PA = scrapy.Field()
    PD = scrapy.Field()
    D = scrapy.Field()

    CC = scrapy.Field()
    CL = scrapy.Field()