#coding:utf-8

import sys
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from tutorial.items import HfHomeItem,FlpxxxxItem,FzcjxxhzItem,XkzxxxxItem,FzxshzxxItem,FlcxxxxItem,ImageItem

import imageToText
import hashlib

reload(sys)
sys.setdefaultencoding("utf-8")

class HfHomeSpider(BaseSpider):
    name = "hfHome"
    
    start_urls = ['http://newhouse.hfhome.cn/']
    
    #��һ�㣺�Ϸ�¥����Ϣ����
    def parse(self,response):
        hxs = HtmlXPathSelector(response)
        
        item = HfHomeItem()
        item['bz'] = 'hfhome'
        #��ѯclass="tabcut"��div����
        lables = hxs.xpath('count(//div[@id="mainleft"]/div[@class="tabcut"])').extract()
        
        print type(lables[0].encode('gbk'))
        labNum = int(float(lables[0].encode('gbk')))
        for lab in xrange(labNum):
            l = lab + 1
            print l
            #��Ϣ��������
            lf_new_bz = hxs.xpath('//div[@id="mainleft"]/div[@class="tabcut"]['+str(l)+']/div[1]/div/text()').extract()
            for item_newshou in lf_new_bz:
                
                if l == 2:
                    lfxx = hxs.xpath('//div[@id="mainleft"]/div[@class="tabcut"][2]//ul/li//a[1]')
                    for i in lfxx:
                        lfmc = i.xpath('text()').extract()
                        lf_bamc = i.xpath('@title').extract()
                        
                        item['lf_dq'] = ''
                        item['lf_mc'] = ''.join(lfmc).strip()
                        item['lf_bamc'] = ''.join(lf_bamc).strip()
                        item['lf_bxfmc_bz'] = 'Y'
                        item['lf_new_bz'] = ''.join(lf_new_bz).strip()
                        #����item��
                        yield item
                        #��ȡ��һ��url����
                        url_next = i.xpath('@href').extract()
                        
                        next_url = 'http://newhouse.hfhome.cn/' + url_next[0]
                        yield Request(next_url,callback=self.parse_next,meta = {'lf_mc':lfmc[0]})
                else:
                    lfxx_dq = hxs.xpath('//div[@id="mainleft"]/div[@class="tabcut"]['+str(l)+']//ul/li//a[contains(@href,"district")]')
                    lfxx_mc = hxs.xpath('//div[@id="mainleft"]/div[@class="tabcut"]['+str(l)+']//ul/li//a[@title]')
                    lfxx = zip(lfxx_dq,lfxx_mc)
                    for i in lfxx:
                        lf_dq = i[0].xpath('text()').extract()
                        lfmc = i[1].xpath('@title').extract()
                        
                        item['lf_bxfmc_bz'] = 'N'
                        item['lf_dq'] = ''.join(lf_dq).strip()
                        item['lf_mc'] = ''.join(lfmc).strip()
                        item['lf_bamc'] = ''
                        item['lf_new_bz'] = ''.join(lf_new_bz).strip()
                        #����item��
                        yield item
                        #��ȡ��һ��url����
                        url_next = i[1].xpath('@href').extract()
                        
                        next_url = 'http://newhouse.hfhome.cn/' + url_next[0]
                        yield Request(next_url,callback=self.parse_next,meta = {'lf_mc':lfmc[0]})
    
    #�ڶ��㣺¥����ϸ��Ϣ
    def parse_next(self,response):
        hxs = HtmlXPathSelector(response)
        
        #��ȡ¥����ϸ��Ϣ����
        lp_url = hxs.select('//div[@class="jiaodiantu"]/iframe/@src').extract()
        lfmc = response.meta['lf_mc']
        lpxx_url = 'http://newhouse.hfhome.cn/' + lp_url[0]
        yield Request(lpxx_url,callback=self.parse_lpxx,meta = {'lf_mc':lfmc})
        
        #�ִ��ɽ���Ϣ����
        item = FzcjxxhzItem()
        
        item['bz'] = 'fzcjxxhz'
        item['lf_mc'] = lfmc
        
        #��ȡ�ִ��ɽ�������Ϣ
        #��ѯtr������
        trs = hxs.xpath('count(//table[@id="dlBuildingList"]/tr)').extract()
        labNum = int(float(trs[0].encode('gbk')))
        for trs_i in xrange(labNum):
            m = trs_i + 1
            
            for tds_i in xrange(2):
                n = tds_i + 1
                items_next_1 = hxs.xpath('//table[@id="dlBuildingList"]/tr['+str(m)+']/td['+str(n)+']//div[@class="Itemleft"]')
                items_next_2 = hxs.xpath('//table[@id="dlBuildingList"]/tr['+str(m)+']/td['+str(n)+']//div[@class="Itemright"]')
                urls_next_a = hxs.xpath('//table[@id="dlBuildingList"]/tr['+str(m)+']/td['+str(n)+']/div[@class="Item"]/div[@class="Itemleft"]//li/a/@href').extract()
                
                #����
                lf_dh = items_next_1.xpath('.//li[1]/text()').extract()
                #�Ƿ�����Ԥ�ۿ���
                sflryskjg = items_next_1.xpath('.//li[2]/text()').extract()
                #���֤����
                license_num = items_next_1.xpath('.//li[3]/text()').extract()
                #����¥����
                overground_count = items_next_1.xpath('.//li[4]/text()').extract()
                #����¥����
                underground_count = items_next_1.xpath('.//li[4]/text()').extract()
                #סլ
                house_count = items_next_2.xpath('.//li[1]/text()').extract()
                #��ҵ
                business_count = items_next_2.xpath('.//li[2]/text()').extract()
                #�칫
                office_count = items_next_2.xpath('.//li[3]/text()').extract()
                #����
                other_count = items_next_2.xpath('.//li[4]/text()').extract()
                #��ϸ��Ϣ���url
                detailInfUrl = urls_next_a
                
                #�ָ���
                fgf = unicode('��','gbk')
                
                #����
                if lf_dh != []:
                    lf_dh = lf_dh[0].split(fgf)
                    item['lf_dh'] = "".join(lf_dh[1])
                else:
                    item['lf_dh'] = ""
                #�Ƿ�����Ԥ�ۿ���
                if sflryskjg != []:
                    item['sflryskjg'] = sflryskjg[0]
                else:
                    item['sflryskjg'] = ""
                #���֤����
                if license_num != []:
                    license_num = license_num[0].split(fgf)
                    item['license_num'] = "".join(license_num[1])
                else:
                    item['license_num'] = ""
                #����¥����
                if overground_count != []:
                    fgf1 = unicode('��','gbk')
                    overground_count = overground_count[0].split(fgf)
                    overground_count = overground_count[1].split(fgf1)
                    
                    item['overground_count'] = "".join(overground_count[0])
                else:
                    item['overground_count'] = ""
                #����¥����
                if underground_count != []:
                    underground_count = underground_count[0].split(fgf)
                    item['underground_count'] = "".join(underground_count[2])
                else:
                    item['underground_count'] = ""
                #סլ
                if house_count != []:
                    house_count = house_count[0].split(fgf)
                    item['house_count'] = "".join(house_count[1])
                else:
                    item['house_count'] = ""
                #��ҵ
                if business_count != []:
                    business_count = business_count[0].split(fgf)
                    item['business_count'] = "".join(business_count[1])
                else:
                    item['business_count'] = ""
                #�칫
                if office_count != []:
                    office_count = office_count[0].split(fgf)
                    item['office_count'] = "".join(office_count[1])
                else:
                    item['office_count'] = ""
                #����
                if other_count != []:
                    other_count = other_count[0].split(fgf)
                    item['other_count'] = "".join(other_count[1])
                else:
                    item['other_count'] = ""
                #��ϸ��Ϣ���url
                if urls_next_a != []:
                    item['detailInfUrl'] = urls_next_a[0]
                
                    yield item
                    
                    third_url = 'http://newhouse.hfhome.cn/' + urls_next_a[0]
                    #��ϸ��Ϣ
                    yield Request(third_url,callback=self.parse_third,meta = {'lf_mc':lfmc,'third_url':third_url})
                    
                else:
                    continue
                    
    #��¥����ϸ��Ϣ
    def parse_lpxx(self,response):
        hxs = HtmlXPathSelector(response)
        
        #������¥����ϸ��Ϣ
        item = FlpxxxxItem()
        item['bz'] = 'flpxx'
        item['lf_mc'] = response.meta['lf_mc']
        #���۴���
        item['sellTotal'] = ''.join(hxs.select('//span[@id="lblSellTotal"]/text()').extract()).strip()
        #β������
        item['wf_num'] = ''.join(hxs.select('//span[@id="lblWF_Num"]/text()').extract()).strip()
        #���괱��
        item['sell_num'] = ''.join(hxs.select('//span[@id="lblSell_Num"]/text()').extract()).strip()
        #סլ����
        item['sellHouse_Num'] = ''.join(hxs.select('//span[@id="lblSellHouse_Num"]/text()').extract()).strip()
        #��ҵ����
        item['sellBiz_num'] = ''.join(hxs.select('//span[@id="lblSellBiz_Num"]/text()').extract()).strip()
        #�칫����
        item['sellOffice_num'] = ''.join(hxs.select('//span[@id="lblSellOffice_Num"]/text()').extract()).strip()
        #��������
        item['sellOther_num'] = ''.join(hxs.select('//span[@id="lblSellOther_Num"]/text()').extract()).strip()
        #��������
        item['district'] = ''.join(hxs.select('//span[@id="lblDISTRICT"]/text()').extract()).strip()
        #��ҵ���
        item['servicesType'] = ''.join(hxs.select('//span[@id="lblServicesType"]/text()').extract()).strip()
        #��������
        item['buildingType'] = ''.join(hxs.select('//span[@id="lblBuildingType"]/text()').extract()).strip()
        #��¥�绰
        item['sellTele'] = ''.join(hxs.select('//span[@id="lblSellTele"]/text()').extract()).strip()
        #��¥��
        item['sellAddress'] = ''.join(hxs.select('//span[@id="lblSellAddress"]/text()').extract()).strip()
        #��Ŀ��ַ
        item['location'] = ''.join(hxs.select('//span[@id="lblLocation"]/text()').extract()).strip()
        #��ͨ״��
        item['trafficInfo'] = ''.join(hxs.select('//span[@id="lblTrafficInfo"]/text()').extract()).strip()
        #������
        item['companyName'] = ''.join(hxs.select('//span[@id="lblCompanyName"]/text()').extract()).strip()
        #������׼
        buyRules = hxs.select('//span[@id="lblBuyRules"]/text()').extract()
        if buyRules == []:
            item['buyRules'] = ''
        else:
            buyRules_pr = buyRules[0].replace('\n','').replace('\r','').replace(' ','').replace('amp;','')
            
            item['buyRules'] = buyRules_pr
            
        #��Ŀ�˻����ۼƻ�������
        item['quit_num'] = ''.join(hxs.select('//span[@id="lblQuit_Num"]/text()').extract()).strip()
        #��Ŀ�˻����ۼƻ�����
        item['quit_hsl'] = ''.join(hxs.select('//span[@id="lblQuit_Hsl"]/text()').extract()).strip()
        #�����ܼ�
        item['buildingCount'] = ''.join(hxs.select('//span[@id="lblBulidingCount"]/text()').extract()).strip()
        #�������
        item['buildArea'] = ''.join(hxs.select('//span[@id="lblBuildArea"]/text()').extract()).strip()
        #�������
        item['itemGetArea'] = ''.join(hxs.select('//span[@id="lblItemGetArea"]/text()').extract()).strip()
        #�ݻ���
        item['rjl'] = ''.join(hxs.select('//span[@id="lblRJL"]/text()').extract()).strip()
        #������Ƶ�λ
        item['buildDesign'] = ''.join(hxs.select('//span[@id="lblBuildDesign"]/text()').extract()).strip()
        #������Ƶ�λ
        item['servicesCompany'] = ''.join(hxs.select('//span[@id="lblServicesCompany"]/text()').extract()).strip()
        #��ҵ��˾
        item['entironmentDesign'] = ''.join(hxs.select('//span[@id="lblEntironmentDesign"]/text()').extract()).strip()
        #��ҵ�绰
        item['prtel'] = ''.join(hxs.select('//span[@id="lblPRTEL"]/text()').extract()).strip()
        #��ҵ��
        item['prcost'] = ''.join(hxs.select('//span[@id="lblPRCOST"]/text()').extract()).strip()
        #��λ���
        item['parking'] = ''.join(hxs.select('//span[@id="lblPARKING"]/text()').extract()).strip()
        #��ů��ʩ
        item['heating'] = ''.join(hxs.select('//span[@id="lblHEATING"]/text()').extract()).strip()
        #�ܱ߻���
        entironment = hxs.select('//span[@id="lblEntironment"]/text()').extract()
        if entironment == []:
            item['entironment'] = ''
        else:
            entironment_pr = entironment[0].replace('\n','').replace('\r','').replace(' ','').replace('amp;','')
            item['entironment'] = entironment_pr
            
        return item
    
    #�����㣺��ϸ��Ϣ
    def parse_third(self,response):
        print "----------333333333333333------------"
        hxs = HtmlXPathSelector(response)
        
        third_url = response.meta['third_url']
        
        #��ȡ¥������
        lfmc = response.meta['lf_mc']
        
        #���֤��ϸ��Ϣ
        item = XkzxxxxItem()
        
        item['bz'] = 'xkzxxxx'
        item['lf_mc'] = lfmc
        
        #����
        lf_dh = ''.join(hxs.select('//span[@id="lbXKZ"]/text()').extract()).strip()
        item['lf_dh'] = lf_dh
        #���֤��
        item['permitNO'] = ''.join(hxs.select('//span[@id="lbPermitNO"]/text()').extract()).strip()
        #���ϲ���
        item['realFloors'] = ''.join(hxs.select('//span[@id="lbRealFloors"]/text()').extract()).strip()
        #���²���
        item['minFloors'] = ''.join(hxs.select('//span[@id="lbMinFloors"]/text()').extract()).strip()
        #����ʹ��Ȩ֤
        item['landNO'] = ''.join(hxs.select('//span[@id="lbLandNO"]/text()').extract()).strip()
        #����
        item['sets'] = ''.join(hxs.select('//span[@id="lbSets"]/text()').extract()).strip()
        #�滮���֤
        item['scaleNO'] = ''.join(hxs.select('//span[@id="lbScaleNO"]/text()').extract()).strip()
        #Ԥ��������
        item['permitArea'] = ''.join(hxs.select('//span[@id="lbPermitArea"]/text()').extract()).strip()
        #�����ṹ
        item['buildFramework'] = ''.join(hxs.select('//span[@id="lbBuildFramework"]/text()').extract()).strip()
        #�������������
        item['selledArea'] = ''.join(hxs.select('//span[@id="lbSelledArea"]/text()').extract()).strip()
        #��;
        item['useFor'] = ''.join(hxs.select('//span[@id="lbUseFor"]/text()').extract()).strip()
        #��������
        item['openDate'] = ''.join(hxs.select('//span[@id="lbOpenDate"]/text()').extract()).strip()
        #��Ƶ�λ
        item['buildingDesign'] = ''.join(hxs.select('//span[@id="lbBuildingDesign"]/text()').extract()).strip()
        #����������ҵ
        item['seller'] = ''.join(hxs.select('//span[@id="lbSeller"]/text()').extract()).strip()
        #��������
        item['completeDate'] = ''.join(hxs.select('//span[@id="lbCompleteDate"]/text()').extract()).strip()
        #���۵绰
        item['sellTele'] = ''.join(hxs.select('//span[@id="lbSellTele"]/text()').extract()).strip()
        #��������
        item['acrossDate'] = ''.join(hxs.select('//span[@id="lbAcrossDate"]/text()').extract()).strip()
        
        yield item
        
        #�ִ����ۻ�����Ϣ����ͼƬ   �ظ�URL�жϣ�dont_filter=True,
        yield Request(third_url,callback=self.parse_img,dont_filter=True,meta = {'lf_mc':lfmc,'third_url':third_url})
        
        four_url = 'http://newhouse.hfhome.cn/' + ''.join(hxs.select('//div[@class="detailLp"]/iframe/@src').extract()).strip()
        yield Request(four_url,callback=self.parse_flcxxxx,meta = {'lf_mc':lfmc,'lf_dh':lf_dh})
        
        
    #�ִ����ۻ�����Ϣ����ͼƬ
    def parse_img(self,response):
        print '================33333333333333======================'
        hxs = HtmlXPathSelector(response)
        
        third_url = response.meta['third_url']
        lf_mc = response.meta['lf_mc']
        
        #��ȡ�ִ����ۻ�����Ϣ
        lf_dh = hxs.select('//span[@id="lblDH"]/text()').extract()
        xshzxxUrls = hxs.xpath('//table[@id="dlfdInfo"]//table[@class="unnamed7"]/tr[2]')
        #xshzxxNames = hxs.select('//table[@id="dlfdInfo"]//table[@class="unnamed7"]')

        img_items = ImageItem()
        img_items['bz'] = 'img'
        
        #��������������URL
        wsxxztsURL = xshzxxUrls.xpath('./td[1]//img/@src').extract()
        #�ֿ�������URL
        xkstsURL = xshzxxUrls.xpath('./td[2]//img/@src').extract()
        #��ǩԼ����URL
        yqytsURL = xshzxxUrls.xpath('./td[3]//img/@src').extract()
        #�ѱ�������URL
        ybatsURL = xshzxxUrls.xpath('./td[4]//img/@src').extract()
        #�ѳɽ�סլ����URL
        ycjzzjjURL = xshzxxUrls.xpath('./td[5]//img/@src').extract()
        #�ѳɽ���ҵ����URL
        ycjsyjjURL = xshzxxUrls.xpath('./td[6]//img/@src').extract()
        
        #��������������ͼƬ·��
        wsxxztsImgPath = hashlib.sha1('http://newhouse.hfhome.cn/'+wsxxztsURL[0]).hexdigest() + '.jpg'
        #�ֿ�������ͼƬ·��
        xkstsImgPath = hashlib.sha1('http://newhouse.hfhome.cn/'+xkstsURL[0]).hexdigest() + '.jpg'
        #��ǩԼ����ͼƬ·��
        yqytsImgPath = hashlib.sha1('http://newhouse.hfhome.cn/'+yqytsURL[0]).hexdigest() + '.jpg'
        #�ѱ�������ͼƬ·��
        ybatsImgPath = hashlib.sha1('http://newhouse.hfhome.cn/'+ybatsURL[0]).hexdigest() + '.jpg'
        #�ѳɽ�סլ����ͼƬ·��
        ycjzzjjImgPath = hashlib.sha1('http://newhouse.hfhome.cn/'+ycjzzjjURL[0]).hexdigest() + '.jpg'
        #�ѳɽ���ҵ����ͼƬ·��
        ycjsyjjImgPath = hashlib.sha1('http://newhouse.hfhome.cn/'+ycjsyjjURL[0]).hexdigest() + '.jpg'
        
        image_urls = ['http://newhouse.hfhome.cn/'+wsxxztsURL[0],
                      'http://newhouse.hfhome.cn/'+xkstsURL[0],
                      'http://newhouse.hfhome.cn/'+yqytsURL[0],
                      'http://newhouse.hfhome.cn/'+ybatsURL[0],
                      'http://newhouse.hfhome.cn/'+ycjzzjjURL[0],
                      'http://newhouse.hfhome.cn/'+ycjsyjjURL[0]]
                      
        img_items['image_urls'] = image_urls
        yield img_items
        
        yield Request(third_url,callback=self.parse_fzxshzxx,dont_filter=True,meta = {'lf_mc':lf_mc,'lf_dh':lf_dh,
                                                          'wsxxztsImgPath':wsxxztsImgPath,
                                                          'xkstsImgPath':xkstsImgPath,
                                                          'yqytsImgPath':yqytsImgPath,
                                                          'ybatsImgPath':ybatsImgPath,
                                                          'ycjzzjjImgPath':ycjzzjjImgPath,
                                                          'ycjsyjjImgPath':ycjsyjjImgPath,})
        
        
    def parse_fzxshzxx(self,response):
        print ">>>>>>>>>>33333333333333333>>>>>>>>>>>>>"
        #��ȡ����
        lf_mc = response.meta['lf_mc']
        lf_dh = response.meta['lf_dh']
        wsxxztsImgPath = response.meta['wsxxztsImgPath']
        xkstsImgPath = response.meta['xkstsImgPath']
        yqytsImgPath = response.meta['yqytsImgPath']
        ybatsImgPath = response.meta['ybatsImgPath']
        ycjzzjjImgPath = response.meta['ycjzzjjImgPath']
        ycjsyjjImgPath = response.meta['ycjsyjjImgPath']
        
        #��������������
        wsxxzts = imageToText.getverify1('D:/scrapySpace/tutorial/images/full/'+wsxxztsImgPath,'Y')
        #�ֿ�������
        xksts = imageToText.getverify1('D:/scrapySpace/tutorial/images/full/'+xkstsImgPath,'Y')
        #��ǩԼ����
        yqyts = imageToText.getverify1('D:/scrapySpace/tutorial/images/full/'+yqytsImgPath,'Y')
        #�ѱ�������
        ybats = imageToText.getverify1('D:/scrapySpace/tutorial/images/full/'+ybatsImgPath,'Y')
        #�ѳɽ�סլ����
        ycjzzjj = imageToText.getverify1('D:/scrapySpace/tutorial/images/full/'+ycjzzjjImgPath,'Y')
        #�ѳɽ���ҵ����
        ycjsyjj = imageToText.getverify1('D:/scrapySpace/tutorial/images/full/'+ycjsyjjImgPath,'Y')
        
        items = FzxshzxxItem()
        #��־
        items['bz'] = 'fzxshzxx'
        #¥������
        items['lf_mc'] = lf_mc
        #����
        items['lf_dh'] = lf_dh[0]
        #��������������
        items['wsxxzts'] = list(wsxxzts)[0].replace('\n\n','').replace('.','6')
        #�ֿ�������
        items['xksts'] = list(xksts)[0].replace('\n\n','').replace('.','6')
        #��ǩԼ����
        items['yqyts'] = list(yqyts)[0].replace('\n\n','').replace('.','6')
        #�ѱ�������
        items['ybats'] = list(ybats)[0].replace('\n\n','').replace('.','6')
        #�ѳɽ�סլ����
        items['ycjzzjj'] = list(ycjzzjj)[0].replace('\n\n','').replace('.','6')
        #�ѳɽ���ҵ����
        items['ycjsyjj'] = list(ycjsyjj)[0].replace('\n\n','').replace('.','6')
        #��������������ͼƬ·��
        items['wsxxztsImgPath'] = wsxxztsImgPath
        #�ֿ�������ͼƬ·��
        items['xkstsImgPath'] = xkstsImgPath
        #��ǩԼ����ͼƬ·��
        items['yqytsImgPath'] = yqytsImgPath
        #�ѱ�������ͼƬ·��
        items['ybatsImgPath'] = ybatsImgPath
        #�ѳɽ�סլ����ͼƬ·��
        items['ycjzzjjImgPath'] = ycjzzjjImgPath
        #�ѳɽ���ҵ����ͼƬ·��
        items['ycjsyjjImgPath'] = ycjsyjjImgPath
        
        yield items
        
    def parse_flcxxxx(self,response):
        print '>>>>>>>>>>44444444444444>>>>>>>>>>'
        hxs = HtmlXPathSelector(response)
        
        #��ȡ����
        lf_mc = response.meta['lf_mc']
        lf_dh = response.meta['lf_dh']
        
        #��ȡ��¥����ϸ��Ϣ
        trs = hxs.xpath('count(//table[@id="HouseTable"]/tr)').extract()
        labNum = int(float(trs[0].encode('gbk')))
        for trs_i in xrange(labNum):
            m = trs_i + 2
            lc_mc = hxs.xpath('//table[@id="HouseTable"]/tr['+str(m)+']/td[1]/text()').extract()
            lcxx_jsUrl = hxs.xpath('//table[@id="HouseTable"]/tr['+str(m)+']/td[@class="preview"]/a/@href').extract()
            
            for lcUrl in lcxx_jsUrl:
                lcxx_url = 'http://newhouse.hfhome.cn/Modal/'+lcUrl.split('(\'')[1].split('\'')[0]
                
                yield Request(lcxx_url,callback=self.parse_flcxxImg,meta = {'lf_mc':lf_mc,'lf_dh':lf_dh,'lc_mc':lc_mc,'lcxx_url':lcxx_url})
        
    def parse_flcxxImg(self,response):
        print '============4444444444444========='
        hxs = HtmlXPathSelector(response)
        
        #��ȡ����
        lf_mc = response.meta['lf_mc']
        lf_dh = response.meta['lf_dh']
        lc_mc = response.meta['lc_mc']
        lcxx_url = response.meta['lcxx_url']
        #�����
        partNO = ''.join(hxs.select('//span[@id="lbPartNO"]/text()').extract()).strip()
        #����
        houseType = ''.join(hxs.select('//span[@id="lbHouseType"]/text()').extract()).strip()
        #�������
        buildAreaUrl = 'http://newhouse.hfhome.cn/Modal/' + ''.join(hxs.select('//span[@id="lbBuildArea"]/img/@src').extract()).strip()
        #�������
        insideAreaUrl = 'http://newhouse.hfhome.cn/Modal/' + ''.join(hxs.select('//span[@id="lbInsideArea"]/img/@src').extract()).strip()
        #��̯���
        joinAreaUrl = 'http://newhouse.hfhome.cn/Modal/' + ''.join(hxs.select('//span[@id="lbJoinArea"]/img/@src').extract()).strip()
        #�����ṹ
        structure = ''.join(hxs.select('//span[@id="lbStructure"]/text()').extract()).strip()
        #������;
        houseUseUrl = 'http://newhouse.hfhome.cn/Modal/' + ''.join(hxs.select('//span[@id="lbHouseUsefulness"]/img/@src').extract()).strip()
        #����״̬
        sellFlagUrl = 'http://newhouse.hfhome.cn/Modal/' + ''.join(hxs.select('//span[@id="lbSellFlag"]/img/@src').extract()).strip()
        #�����ַ
        location = ''.join(hxs.select('//span[@id="lbLocation"]/text()').extract()).strip()
        #�������ͼƬ��
        buildAreaImg = hashlib.sha1(buildAreaUrl).hexdigest() + '.jpg'
        #�������ͼƬ��
        insideAreaImg = hashlib.sha1(insideAreaUrl).hexdigest() + '.jpg'
        #��̯���ͼƬ��
        joinAreaImg = hashlib.sha1(joinAreaUrl).hexdigest() + '.jpg'
        #������;ͼƬ��
        houseUseImg = hashlib.sha1(houseUseUrl).hexdigest() + '.jpg'
        #����״̬ͼƬ��
        sellFlagImg = hashlib.sha1(sellFlagUrl).hexdigest() + '.jpg'
        
        img_items = ImageItem()
        img_items['bz'] = 'img'
        
        image_urls = [buildAreaUrl,
                      insideAreaUrl,
                      joinAreaUrl,
                      houseUseUrl,
                      sellFlagUrl]
                      
        img_items['image_urls'] = image_urls
        yield img_items
        
        yield Request(lcxx_url,callback=self.parse_flcxxItem,dont_filter=True,meta = {'lf_mc':lf_mc,
                                                                                    'lf_dh':lf_dh,
                                                                                    'lc_mc':lc_mc,
                                                                                    'partNO':partNO,
                                                                                    'houseType':houseType,
                                                                                    'structure':structure,
                                                                                    'location':location,
                                                                                    'buildAreaImg':buildAreaImg,
                                                                                    'insideAreaImg':insideAreaImg,
                                                                                    'joinAreaImg':joinAreaImg,
                                                                                    'houseUseImg':houseUseImg,
                                                                                    'sellFlagImg':sellFlagImg})
    def parse_flcxxItem(self,response):
        print '~~~~~~~~~~~~~~~~~~44444444444444444~~~~~~~~~~~~~~~~~'
        #��ȡ����
        lf_mc = response.meta['lf_mc']
        lf_dh = response.meta['lf_dh']
        lc_mc = response.meta['lc_mc']
        partNO = response.meta['partNO']
        houseType = response.meta['houseType']
        structure = response.meta['structure']
        location = response.meta['location']
        buildAreaImg = response.meta['buildAreaImg']
        insideAreaImg = response.meta['insideAreaImg']
        joinAreaImg = response.meta['joinAreaImg']
        houseUseImg = response.meta['houseUseImg']
        sellFlagImg = response.meta['sellFlagImg']
        
        buildArea = imageToText.getverify1('D:/scrapySpace/tutorial/images/full/'+buildAreaImg,'Y')
        insideArea = imageToText.getverify1('D:/scrapySpace/tutorial/images/full/'+insideAreaImg,'Y')
        joinArea = imageToText.getverify1('D:/scrapySpace/tutorial/images/full/'+joinAreaImg,'Y')
        houseUse = imageToText.getverify1('D:/scrapySpace/tutorial/images/full/'+houseUseImg,'N')
        sellFlag = imageToText.getverify1('D:/scrapySpace/tutorial/images/full/'+sellFlagImg,'N')
        
        items = FlcxxxxItem()
        #��־
        items['bz'] = 'flcxxxx'
        #¥������
        items['lf_mc'] = lf_mc
        #����
        items['lf_dh'] = lf_dh
        #¥���
        items['lc_mc'] = lc_mc
        #�����
        items['partNO'] = partNO
        #����
        items['houseType'] = houseType
        #�������
        items['buildArea'] = list(buildArea)[0].replace('\n\n','')
        #�������
        items['insideArea'] = list(insideArea)[0].replace('\n\n','')
        #��̯���
        items['joinArea'] = list(joinArea)[0].replace('\n\n','')
        #�����ṹ
        items['structure'] = structure
        
        #�滻����
        zz_lm = unicode('����','gbk')
        zz = unicode('סլ','gbk')
        
        yba_lm = unicode('����Ʊ','gbk')
        yba = unicode('�ѱ���','gbk')
        
        cc_lm = unicode('@��','gbk')
        cc = unicode('�ִ�','gbk')
        
        bgmc_lm = unicode('�ƹ�','gbk')
        bgmc = unicode('�칫','gbk')
        #������;
        items['houseUse'] = list(houseUse)[0].replace('\n\n','').replace(zz_lm,zz).replace(cc_lm,cc).replace(bgmc_lm,bgmc)
        #����״̬
        items['sellFlag'] = list(sellFlag)[0].replace('\n\n','').replace(yba_lm,yba)
        #�����ַ
        items['location'] = location
        #�������ͼƬ��
        items['buildAreaImg'] = buildAreaImg
        #�������ͼƬ��
        items['insideAreaImg'] = insideAreaImg
        #��̯���ͼƬ��
        items['joinAreaImg'] = joinAreaImg
        #������;ͼƬ��
        items['houseUseImg'] = houseUseImg
        #����״̬ͼƬ��
        items['sellFlagImg'] = sellFlagImg
        
        yield items
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    