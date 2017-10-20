import scrapy
from .communications import services
from urllib import parse


class ProductsSpider(scrapy.Spider):
    name = "products"
    _baseurl = 'https://egypt.souq.com/eg-en/'

    def start_requests(self):
        yield scrapy.Request(self._get_url(), self.parse)

    def _get_url(self, page=1):
        search_term = getattr(self, 'search_term', None)
        if search_term is not None:
            return self._baseurl + search_term + '/s/?page={}'.format(str(page))
        else:
            return self._baseurl

    def parse(self, response):
        for product in response.css('div.search-results-content div.column.single-item'):
            product_name = product.css('h1.itemTitle::text').extract_first()
            price_raw = product.css('h1.itemPrice::text').extract_first()
            yield {
                'name': product_name,
                'features': product_name.split(','),
                'price': price_raw,
                'price_num': float(services.call('cleansing/clean_price')(price_raw).text),
                'author': product.css('small.author::text').extract_first(),
            }
        if len(response.css('div.warning.callout.zero-results')):
            return
        parsed_url = parse.urlparse(response.url)
        next_page = int(parse.parse_qs(parsed_url)['page'].pop()) + 1

        if next_page is not None:
            next_page_url = self._get_url(page=next())
            yield response.follow(next_page_url, self.parse)

