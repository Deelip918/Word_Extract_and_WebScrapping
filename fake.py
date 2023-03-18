import scrapy


class FakeSpider(scrapy.Spider):
    name = "fake"
    allowed_domains = ["fake-plants.co.uk"]
    start_urls = ["http://fake-plants.co.uk/"]
    global visited

    def parse(self, response):
        for link in response.css('li.product-category a::attr(href)'):
            print(link)
            yield response.follow(link.get(), callback=self.parse_cat)
            if link in visited:
                continue
            visited.add(link)
        print(visited)
    def parse_cat(self,response):
        products = response.css('div.astra-shop-summary-wrap')
        for product in products:
            yield {
                'title': product.css('span.ast-woo-product-category::text').get().strip(),
                'details': product.css('h2.woocommerce-loop-product__title::text').get().strip()
            }
visited=set()

