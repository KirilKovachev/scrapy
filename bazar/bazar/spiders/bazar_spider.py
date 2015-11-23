from scrapy.spiders import Spider
from scrapy.selector import Selector
from bazar.items import BazarItem 
from scrapy.http import Request

class BazarSpider(Spider):
    name = "bazar"
    allowed_domains = ["bazar.bg"]
    current_page_no = 1
    start_urls = [
        "https://bazar.bg/%D0%BE%D0%B1%D1%8F%D0%B2%D0%B8/%D1%83%D1%81%D0%BB%D1%83%D0%B3%D0%B8/"
    ]


    def get_next_url(self, fired_url):
        if '?page=' in fired_url:
            url, page_no = fired_url.rsplit('?page=', 1)
        else:
            if self.current_page_no != 1:
                #end of scroll
                return 
        self.current_page_no += 1
        return "https://bazar.bg/%%D0%%BE%%D0%%B1%%D1%%8F%%D0%%B2%%D0%%B8/%%D1%%83%%D1%%81%%D0%%BB%%D1%%83%%D0%%B3%%D0%%B8?page=%s" % self.current_page_no


    def parse(self, response):
        fired_url = response.url
        hxs = Selector(response)
        sites = hxs.xpath('//div[@class="abTbl "]')
        sites = hxs.xpath('//*[@id="wrapper"]/div[6]/div[1]/div[1]/div[6]')
        for site in sites:
            item = BazarItem()
            item['Title'] = hxs.xpath('//*[@id="wrapper"]/div[6]/div[1]/div[1]/div[6]/a[1]/div/span[1]')
            item['Category'] = site.select('span[@class="icListBusType"]/text()').extract()
            item['Description'] = site.select('span[last()]/text()').extract()
            item['Number'] = site.select('span[@class="searchInfoLabel"]/span/@id').extract()
            item['Web_url'] = site.select('span[@class="searchInfoLabel"]/a/@href').extract()
            item['adress_name'] = site.select('span[@class="searchInfoLabel"]/span/text()').extract()
            item['Photo_name'] = site.select('img/@alt').extract()
            item['Photo_path'] = site.select('img/@src').extract()
            yield item
        next_url = self.get_next_url(fired_url)
        if next_url:
            yield Request(next_url, self.parse, dont_filter=True)
