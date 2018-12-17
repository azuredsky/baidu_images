import scrapy
from baidu_image.items import BaiduImageItem
import re
import os
from tqdm import tqdm


kindList = ['keyword1','keyword2','keyword3']


class BkSpider(scrapy.Spider):
    name = 'bdimg'
    # allowed_domains = ['image.baidu.com']
    start_urls = ['http://image.baidu.com']
    url_start = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word='
    url_end = '&ct=&ic=0&lm=-1&width=0&height=0'
    pages = 30
    step = 30

    def start_requests(self):
        print(len(kindList))
        for key_word in kindList:
            path = os.path.join(r'../images', key_word)
            if os.path.exists(path):
                pass
            else:
                os.makedirs(path)
            end = self.pages * self.step
            for page in range(0, end, self.step):
                gsm = hex(page)
                url = self.url_start + key_word + '&pn=' + str(page) + '&gsm=' + str(gsm) + self.url_end
                request = scrapy.Request(url,callback=self.get_one_page_urls, dont_filter=False)
                request.meta['kind'] = key_word
                request.meta['page'] = page
                yield request

    def parse(self, response):

        print('>>>>>>>>>>>>>>>>>>>>>>>>')
        item = BaiduImageItem()
        item['img'] = response.body
        item['kind'] = response.meta['kind']
        item['name'] = response.meta['name']
        item['type'] = response.meta['type']
        # print('????????')
        yield item

    def get_one_page_urls(self,response):

        kind = response.meta['kind']
        page = response.meta['page']
        # print(response.body)
        urls = re.findall('"objURL":"(.*?)",', response.body.decode('utf-8'), re.S)
        # print(urls)

        for i in tqdm(range(len(urls))):

            request1 = scrapy.Request(urls[i], callback=self.parse)
            request1.meta['kind'] = kind
            request1.meta['name'] = str(page//self.pages) + '_'+str(i)
            request1.meta['type'] = urls[i].split('.')[-1]

            yield request1