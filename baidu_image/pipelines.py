# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BaiduImagePipeline(object):
    def process_item(self, item, spider):
        filename = r'../images/'+item['kind']+'/'+str(item['name'])+'.'+item['type']
        with open(filename,'wb') as f:
            f.write(item['img'])
        print('成功保存第%s个%s文件' % (item['name'],item['kind']))

