import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from mercado.items import MercadoItem

class MercadoSpider(CrawlSpider):
	name = 'mercado'
	item_count = 0
	allowed_domain = ['www.mercadolibre.com.pe']
	start_urls = ['https://www.mercadolibre.com.pe/ofertas#nav-header']

	rules = {
		# Para cada item
		Rule(LinkExtractor(allow = (), restrict_xpaths = ('//li[@class="andes-pagination__button andes-pagination__button--next"]/a'))),
		Rule(LinkExtractor(allow =(), restrict_xpaths = ('//a[@class="promotion-item__link-container"]')),
							callback = 'parse_item', follow = False)
	}

	def parse_item(self, response):
		ml_item = MercadoItem()
		#INFORMACION DEL PRODUCTO
		ml_item['NP'] = response.xpath('normalize-space(//h1[@class="ui-pdp-title"])').extract()
		ml_item['VP'] = response.xpath('normalize-space(//div[@class="ui-pdp-seller__header__title"])').extract()
		ml_item['EV'] = response.xpath('//a[@class="ui-pdp-media__action ui-box-component__action"]/@href').extract()

		#INFORMACION DE PRECIOS
		ml_item['PA'] = response.xpath('normalize-space(//*[@id="price"]/div/div/s/span[3])').extract()
		ml_item['PD'] = response.xpath('normalize-space(//*[@id="price"]/div/div[1]/div[1]/span[1]/span[3])').extract()
		ml_item['D'] = response.xpath('normalize-space(//span[@class="andes-money-amount__discount"])').extract()

		#OPINIONES DEL PRODUCTO
		ml_item['CC'] = response.xpath('normalize-space(//p[@class="ui-review-capability__rating__label"])').extract()
		ml_item['CL'] = response.xpath('normalize-space(//p[@class="ui-review-capability__rating__average ui-review-capability__rating__average--desktop"])').extract()

		self.item_count += 1
		if self.item_count > 960:
			raise CloseSpider('item_exceeded')
		yield ml_item
