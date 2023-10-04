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
		ml_item['titulo'] = response.xpath('normalize-space(//h1[@class="ui-pdp-title"])').extract()
		ml_item['precio'] = response.xpath('normalize-space(//div[@class="ui-pdp-price__second-line"]/span[@class="andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact"]/span[@class="andes-money-amount__fraction"])').extract()
		ml_item['condicion'] = response.xpath('normalize-space(//span[@class="ui-pdp-subtitle"])').extract()
		ml_item['envio'] = response.xpath('normalize-space(//span[@class="ui-pdp-color--GREEN ui-pdp-family--SEMIBOLD"])').extract()
		ml_item['opiniones'] = response.xpath('normalize-space(//p[@class="ui-review-capability__rating__average ui-review-capability__rating__average--desktop"])').extract()
		ml_item['ventas_producto'] = response.xpath('normalize-space(//strong[@class="ui-pdp-seller__sales-description"])').extract()
		ml_item['vendedor_url'] = response.xpath('//a[@class="ui-pdp-media__action ui-box-component__action"]/@href').extract()

		self.item_count += 1
		if self.item_count > 10:
			raise CloseSpider('item_exceeded')
		yield ml_item
