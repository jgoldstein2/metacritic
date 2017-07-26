from metacritic.items import MetacriticItem
from scrapy import Spider, Request

class MetacriticSpider(Spider):
	name = "metacritic_spider"
	allowed_urls = ['http://www.metacritic.com']
	start_urls = ['http://www.metacritic.com/browse/tv/score/metascore/all/filtered?sort=desc&page=%s'% page for page in range(0,21)]

	def parse(self, response):
		# parse each page for 100 shows
		rows = response.xpath("//div[@class='product_row season' or @class='product_row season first' or @class='product_row season last']")

		for row in rows:
			item = MetacriticItem()
			item['Rank'] = row.xpath('.//div[@class="product_item row_num"]/text()').extract_first().strip().strip('.')
			item['Name'] = row.xpath('.//div[@class="product_item product_title"]/a/text()').extract_first().strip()

			url = 'http://www.metacritic.com/' + row.xpath('.//div[@class="product_item product_title"]/a/@href').extract_first()
			
			request = Request(url, callback = self.details_parse)
			request.meta['item'] = item
			yield request 

	def details_parse(self, response):
		item = response.meta['item']
		item["CriticR"] = response.xpath('//span[@itemprop="ratingValue"]/text()').extract_first()
		                       
		item["CriticNum"] = response.xpath('//span[@itemprop="reviewCount"]/text()').extract_first().strip() 
		                                               
		item["UserR"] = response.xpath('//a[@class="metascore_anchor"]/div/text()').extract_first()

		try:
			item["UserNum"] = response.xpath('//div[@class="userscore_wrap feature_userscore"]//span[@class="count"]/a/text()').extract_first().strip(' Ratings')
		except AttributeError:
			item["UserNum"] = "N/A"	

		item["Network"] = response.xpath('//ul[@class="summary_details"]//span[@itemprop="name"]/text()').extract_first().strip() 
		
		item["SeasonDate"] = response.xpath('//li[@class="summary_detail release_data"]//span[@class="data"]/text()').extract_first()

		item["SeriesDate"] = response.xpath('//span[@itemprop="startDate"]/text()').extract_first()

		item["Length"] = response.xpath('//li[@class="summary_detail product_runtime"]//span[@class="data"]/text()').extract_first()

		try:
			item["Genre"] = response.xpath("//li[@class='summary_detail product_genre']/span[@class='data']/text()").extract()
		except AttributeError:
			item["Genre"] = "N/A"

		new_url = 'http://www.metacritic.com/' + response.xpath('//li[@class="summary_detail more"]/a/@href').extract_first()
		
		request2 = Request(new_url, callback = self.season_parse)
		request2.meta['item'] = item
		
		yield request2 

	def season_parse(self, response):
		item = response.meta['item']
		item["Seasons"] = response.xpath('//div[@class="product_details"]//th[@scope="row" and text() = "Seasons:"]/following-sibling::td/text()').extract_first().strip().replace(" ","")

		yield item 





