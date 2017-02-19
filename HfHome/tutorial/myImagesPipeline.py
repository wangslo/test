# coding:utf-8

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request

class MyImagesPipeline(ImagesPipeline):
    def get_meida_requests(self,item,info):
        for imgurl in item['image_urls']:
            yield imgurl
            
    def item_completed(self,requests,item,info):
        image_path = [x['path'] for ok,x in requests if ok]
        if not image_path:
            raise DropItem("Item not contines images")
        item['image_paths'] = image_path
        return item