import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from mercado.items import MercadoItem

class MercadoSpider(CrawlSpider):
	name = 'mercado'
	item_count = 0
	allowed_domain = ['www.mercadolibre.com.pe']
	start_urls = ['https://listado.mercadolibre.com.pe/laptops#D[A:laptops]]']

	rules = {
		# Para cada item
		Rule(LinkExtractor(allow = (), restrict_xpaths = ('//li[@class="andes-pagination__button andes-pagination__button--next"]/a'))),
		Rule(LinkExtractor(allow =(), restrict_xpaths = ('//a[@class="ui-search-item__group__element ui-search-link"]')),
							callback = 'parse_item', follow = False)
	}

	def parse_item(self, response):
		ml_item = MercadoItem()
		#info de producto
		ml_item['titulo'] = response.xpath('normalize-space(//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/h1/text())').extract_first()
		ml_item['precio'] = response.xpath('normalize-space(//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[3]/div[1]/div[1]/span[1]/span[3]/text())').extract()
		ml_item['condicion'] = response.xpath('normalize-space(//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/span/text())').extract()
		ml_item['envio'] = response.xpath('normalize-space(//*[@id="buybox-form"]/div[1]/div/div/p[1]/text())').extract()
		ml_item['opiniones'] = response.xpath('normalize-space(//*[@id="reviews_capability_v3"]/div/section/div/div[1]/article/div/div[1]/div[1]/p/text())').extract()
		ml_item['ventas_producto'] = response.xpath('normalize-space(//strong[@class="ui-pdp-seller__sales-description"]/text())').extract()
		#info de la tienda o vendedor
		ml_item['vendedor_url'] = response.xpath('//*[@id="ui-pdp-main-container"]/div[2]/div/div[2]/div[1]/a/@href').extract()

		self.item_count += 1
		if self.item_count > 100:
			raise CloseSpider('item_exceeded')
		yield ml_item
