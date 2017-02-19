# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs


class HfHomePipeline(object):
    def __init__(self):
        self.file = codecs.open('hfhome.json','wb',encoding = 'utf-8')
        self.flpxxFile = codecs.open('Flpxx.json','wb',encoding = 'utf-8')
        self.fzcjxxhzFile = codecs.open('fzcjxxhz.json','wb',encoding = 'utf-8')
        self.xkzxxxxFile = codecs.open('xkzxxxx.json','wb',encoding = 'utf-8')
        self.fzxshzxxFile = codecs.open("fzxshzxx.json","wb",encoding = "utf-8")
        self.flcxxxxFile = codecs.open("flcxxxx.json","wb",encoding = "utf-8")
        
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        
        if item['bz'] == 'hfhome':
            self.file.write(line.decode("unicode_escape"))
        elif item['bz'] == 'flpxx':
            self.flpxxFile.write(line.decode("unicode_escape"))
        elif item['bz'] == 'fzcjxxhz':
            self.fzcjxxhzFile.write(line.decode("unicode_escape"))
        elif item['bz'] == 'xkzxxxx':
            self.xkzxxxxFile.write(line.decode("unicode_escape"))
        elif item['bz'] == 'fzxshzxx':
            self.fzxshzxxFile.write(line.decode("unicode_escape"))
        elif item['bz'] == 'flcxxxx':
            self.flcxxxxFile.write(line.decode("unicode_escape"))
        elif item['bz'] == 'img':
            return item
        return item
