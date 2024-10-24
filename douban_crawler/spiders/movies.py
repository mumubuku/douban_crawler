# douban_crawler/douban_crawler/spiders/movies.py
import scrapy
from douban_crawler.items import DoubanCrawlerItem

class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['douban.com']
    start_urls = ['http://movie.douban.com/top250']  # 根据实际需求调整 URL

    def parse(self, response):
        # 打印当前处理的页面 URL
        self.logger.info(f'Processing URL: {response.url}')
        movies = response.xpath('//ol[@class="grid_view"]/li')
        self.logger.info(f'Found {len(movies)} movies on the page')

        for movie in movies:
            item = DoubanCrawlerItem()
            title = movie.xpath('.//div[@class="info"]/div[@class="hd"]/a/span[@class="title"][1]/text()').extract_first()
            item['title'] = title
            item['detail_url'] = movie.xpath('.//div[@class="info"]/div[@class="hd"]/a/@href').extract_first()
            item['director'] = movie.xpath('.//div[@class="info"]/div[@class="bd"]/p[1]/text()').re_first(r'导演: ([^主演]+)')
            item['rating'] = movie.xpath('.//div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract_first()
            item['num_reviews'] = movie.xpath('.//div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[last()]/text()').extract_first()

            # 打印每部电影的信息以确认是否正确抓取
            self.logger.debug(f'Scraping movie: {item["title"]} with rating {item["rating"]} and URL {item["detail_url"]}')
            yield item

        # 翻页逻辑，如果有下一页则继续爬取
        next_page = response.xpath('//span[@class="next"]/a/@href').extract_first()
        if next_page:
            next_page_url = response.urljoin(next_page)
            self.logger.info(f'Following next page: {next_page_url}')
            yield scrapy.Request(next_page_url, callback=self.parse)
        else:
            self.logger.info('No more pages to follow.')