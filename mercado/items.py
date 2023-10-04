# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MercadoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #info de producto
    titulo = scrapy.Field()
    precio = scrapy.Field()
    condicion = scrapy.Field()
    envio = scrapy.Field()
    opiniones = scrapy.Field()
    ventas_producto = scrapy.Field()
    #info de la tienda o vendedor
    vendedor_url = scrapy.Field()
   