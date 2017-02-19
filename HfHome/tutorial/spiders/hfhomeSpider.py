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
    
    #第一层：合肥楼盘信息汇总
    def parse(self,response):
        hxs = HtmlXPathSelector(response)
        
        item = HfHomeItem()
        item['bz'] = 'hfhome'
        #查询class="tabcut"的div数量
        lables = hxs.xpath('count(//div[@id="mainleft"]/div[@class="tabcut"])').extract()
        
        print type(lables[0].encode('gbk'))
        labNum = int(float(lables[0].encode('gbk')))
        for lab in xrange(labNum):
            l = lab + 1
            print l
            #信息分类名称
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
                        #存入item中
                        yield item
                        #获取下一层url请求
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
                        #存入item中
                        yield item
                        #获取下一层url请求
                        url_next = i[1].xpath('@href').extract()
                        
                        next_url = 'http://newhouse.hfhome.cn/' + url_next[0]
                        yield Request(next_url,callback=self.parse_next,meta = {'lf_mc':lfmc[0]})
    
    #第二层：楼盘详细信息
    def parse_next(self,response):
        hxs = HtmlXPathSelector(response)
        
        #获取楼盘详细信息链接
        lp_url = hxs.select('//div[@class="jiaodiantu"]/iframe/@src').extract()
        lfmc = response.meta['lf_mc']
        lpxx_url = 'http://newhouse.hfhome.cn/' + lp_url[0]
        yield Request(lpxx_url,callback=self.parse_lpxx,meta = {'lf_mc':lfmc})
        
        #分幢成交信息汇总
        item = FzcjxxhzItem()
        
        item['bz'] = 'fzcjxxhz'
        item['lf_mc'] = lfmc
        
        #获取分幢成交汇总信息
        #查询tr的数量
        trs = hxs.xpath('count(//table[@id="dlBuildingList"]/tr)').extract()
        labNum = int(float(trs[0].encode('gbk')))
        for trs_i in xrange(labNum):
            m = trs_i + 1
            
            for tds_i in xrange(2):
                n = tds_i + 1
                items_next_1 = hxs.xpath('//table[@id="dlBuildingList"]/tr['+str(m)+']/td['+str(n)+']//div[@class="Itemleft"]')
                items_next_2 = hxs.xpath('//table[@id="dlBuildingList"]/tr['+str(m)+']/td['+str(n)+']//div[@class="Itemright"]')
                urls_next_a = hxs.xpath('//table[@id="dlBuildingList"]/tr['+str(m)+']/td['+str(n)+']/div[@class="Item"]/div[@class="Itemleft"]//li/a/@href').extract()
                
                #栋号
                lf_dh = items_next_1.xpath('.//li[1]/text()').extract()
                #是否列入预售款监管
                sflryskjg = items_next_1.xpath('.//li[2]/text()').extract()
                #许可证号码
                license_num = items_next_1.xpath('.//li[3]/text()').extract()
                #地上楼层数
                overground_count = items_next_1.xpath('.//li[4]/text()').extract()
                #地下楼层数
                underground_count = items_next_1.xpath('.//li[4]/text()').extract()
                #住宅
                house_count = items_next_2.xpath('.//li[1]/text()').extract()
                #商业
                business_count = items_next_2.xpath('.//li[2]/text()').extract()
                #办公
                office_count = items_next_2.xpath('.//li[3]/text()').extract()
                #其他
                other_count = items_next_2.xpath('.//li[4]/text()').extract()
                #详细信息入口url
                detailInfUrl = urls_next_a
                
                #分隔符
                fgf = unicode('：','gbk')
                
                #栋号
                if lf_dh != []:
                    lf_dh = lf_dh[0].split(fgf)
                    item['lf_dh'] = "".join(lf_dh[1])
                else:
                    item['lf_dh'] = ""
                #是否列入预售款监管
                if sflryskjg != []:
                    item['sflryskjg'] = sflryskjg[0]
                else:
                    item['sflryskjg'] = ""
                #许可证号码
                if license_num != []:
                    license_num = license_num[0].split(fgf)
                    item['license_num'] = "".join(license_num[1])
                else:
                    item['license_num'] = ""
                #地上楼层数
                if overground_count != []:
                    fgf1 = unicode('地','gbk')
                    overground_count = overground_count[0].split(fgf)
                    overground_count = overground_count[1].split(fgf1)
                    
                    item['overground_count'] = "".join(overground_count[0])
                else:
                    item['overground_count'] = ""
                #地下楼层数
                if underground_count != []:
                    underground_count = underground_count[0].split(fgf)
                    item['underground_count'] = "".join(underground_count[2])
                else:
                    item['underground_count'] = ""
                #住宅
                if house_count != []:
                    house_count = house_count[0].split(fgf)
                    item['house_count'] = "".join(house_count[1])
                else:
                    item['house_count'] = ""
                #商业
                if business_count != []:
                    business_count = business_count[0].split(fgf)
                    item['business_count'] = "".join(business_count[1])
                else:
                    item['business_count'] = ""
                #办公
                if office_count != []:
                    office_count = office_count[0].split(fgf)
                    item['office_count'] = "".join(office_count[1])
                else:
                    item['office_count'] = ""
                #其他
                if other_count != []:
                    other_count = other_count[0].split(fgf)
                    item['other_count'] = "".join(other_count[1])
                else:
                    item['other_count'] = ""
                #详细信息入口url
                if urls_next_a != []:
                    item['detailInfUrl'] = urls_next_a[0]
                
                    yield item
                    
                    third_url = 'http://newhouse.hfhome.cn/' + urls_next_a[0]
                    #详细信息
                    yield Request(third_url,callback=self.parse_third,meta = {'lf_mc':lfmc,'third_url':third_url})
                    
                else:
                    continue
                    
    #分楼盘详细信息
    def parse_lpxx(self,response):
        hxs = HtmlXPathSelector(response)
        
        #二、分楼盘详细信息
        item = FlpxxxxItem()
        item['bz'] = 'flpxx'
        item['lf_mc'] = response.meta['lf_mc']
        #可售幢数
        item['sellTotal'] = ''.join(hxs.select('//span[@id="lblSellTotal"]/text()').extract()).strip()
        #尾房幢数
        item['wf_num'] = ''.join(hxs.select('//span[@id="lblWF_Num"]/text()').extract()).strip()
        #售完幢数
        item['sell_num'] = ''.join(hxs.select('//span[@id="lblSell_Num"]/text()').extract()).strip()
        #住宅套数
        item['sellHouse_Num'] = ''.join(hxs.select('//span[@id="lblSellHouse_Num"]/text()').extract()).strip()
        #商业套数
        item['sellBiz_num'] = ''.join(hxs.select('//span[@id="lblSellBiz_Num"]/text()').extract()).strip()
        #办公套数
        item['sellOffice_num'] = ''.join(hxs.select('//span[@id="lblSellOffice_Num"]/text()').extract()).strip()
        #其他套数
        item['sellOther_num'] = ''.join(hxs.select('//span[@id="lblSellOther_Num"]/text()').extract()).strip()
        #所在区域
        item['district'] = ''.join(hxs.select('//span[@id="lblDISTRICT"]/text()').extract()).strip()
        #物业类别
        item['servicesType'] = ''.join(hxs.select('//span[@id="lblServicesType"]/text()').extract()).strip()
        #建筑类型
        item['buildingType'] = ''.join(hxs.select('//span[@id="lblBuildingType"]/text()').extract()).strip()
        #售楼电话
        item['sellTele'] = ''.join(hxs.select('//span[@id="lblSellTele"]/text()').extract()).strip()
        #售楼处
        item['sellAddress'] = ''.join(hxs.select('//span[@id="lblSellAddress"]/text()').extract()).strip()
        #项目地址
        item['location'] = ''.join(hxs.select('//span[@id="lblLocation"]/text()').extract()).strip()
        #交通状况
        item['trafficInfo'] = ''.join(hxs.select('//span[@id="lblTrafficInfo"]/text()').extract()).strip()
        #开发商
        item['companyName'] = ''.join(hxs.select('//span[@id="lblCompanyName"]/text()').extract()).strip()
        #交付标准
        buyRules = hxs.select('//span[@id="lblBuyRules"]/text()').extract()
        if buyRules == []:
            item['buyRules'] = ''
        else:
            buyRules_pr = buyRules[0].replace('\n','').replace('\r','').replace(' ','').replace('amp;','')
            
            item['buyRules'] = buyRules_pr
            
        #项目退换房累计换手套数
        item['quit_num'] = ''.join(hxs.select('//span[@id="lblQuit_Num"]/text()').extract()).strip()
        #项目退换房累计换手率
        item['quit_hsl'] = ''.join(hxs.select('//span[@id="lblQuit_Hsl"]/text()').extract()).strip()
        #幢数总计
        item['buildingCount'] = ''.join(hxs.select('//span[@id="lblBulidingCount"]/text()').extract()).strip()
        #建筑面积
        item['buildArea'] = ''.join(hxs.select('//span[@id="lblBuildArea"]/text()').extract()).strip()
        #土地面积
        item['itemGetArea'] = ''.join(hxs.select('//span[@id="lblItemGetArea"]/text()').extract()).strip()
        #容积率
        item['rjl'] = ''.join(hxs.select('//span[@id="lblRJL"]/text()').extract()).strip()
        #建筑设计单位
        item['buildDesign'] = ''.join(hxs.select('//span[@id="lblBuildDesign"]/text()').extract()).strip()
        #环境设计单位
        item['servicesCompany'] = ''.join(hxs.select('//span[@id="lblServicesCompany"]/text()').extract()).strip()
        #物业公司
        item['entironmentDesign'] = ''.join(hxs.select('//span[@id="lblEntironmentDesign"]/text()').extract()).strip()
        #物业电话
        item['prtel'] = ''.join(hxs.select('//span[@id="lblPRTEL"]/text()').extract()).strip()
        #物业费
        item['prcost'] = ''.join(hxs.select('//span[@id="lblPRCOST"]/text()').extract()).strip()
        #车位配比
        item['parking'] = ''.join(hxs.select('//span[@id="lblPARKING"]/text()').extract()).strip()
        #供暖设施
        item['heating'] = ''.join(hxs.select('//span[@id="lblHEATING"]/text()').extract()).strip()
        #周边环境
        entironment = hxs.select('//span[@id="lblEntironment"]/text()').extract()
        if entironment == []:
            item['entironment'] = ''
        else:
            entironment_pr = entironment[0].replace('\n','').replace('\r','').replace(' ','').replace('amp;','')
            item['entironment'] = entironment_pr
            
        return item
    
    #第三层：详细信息
    def parse_third(self,response):
        print "----------333333333333333------------"
        hxs = HtmlXPathSelector(response)
        
        third_url = response.meta['third_url']
        
        #获取楼房名称
        lfmc = response.meta['lf_mc']
        
        #许可证详细信息
        item = XkzxxxxItem()
        
        item['bz'] = 'xkzxxxx'
        item['lf_mc'] = lfmc
        
        #幢号
        lf_dh = ''.join(hxs.select('//span[@id="lbXKZ"]/text()').extract()).strip()
        item['lf_dh'] = lf_dh
        #许可证号
        item['permitNO'] = ''.join(hxs.select('//span[@id="lbPermitNO"]/text()').extract()).strip()
        #地上层数
        item['realFloors'] = ''.join(hxs.select('//span[@id="lbRealFloors"]/text()').extract()).strip()
        #地下层数
        item['minFloors'] = ''.join(hxs.select('//span[@id="lbMinFloors"]/text()').extract()).strip()
        #土地使用权证
        item['landNO'] = ''.join(hxs.select('//span[@id="lbLandNO"]/text()').extract()).strip()
        #套数
        item['sets'] = ''.join(hxs.select('//span[@id="lbSets"]/text()').extract()).strip()
        #规划许可证
        item['scaleNO'] = ''.join(hxs.select('//span[@id="lbScaleNO"]/text()').extract()).strip()
        #预售许可面积
        item['permitArea'] = ''.join(hxs.select('//span[@id="lbPermitArea"]/text()').extract()).strip()
        #建筑结构
        item['buildFramework'] = ''.join(hxs.select('//span[@id="lbBuildFramework"]/text()').extract()).strip()
        #网上销售总面积
        item['selledArea'] = ''.join(hxs.select('//span[@id="lbSelledArea"]/text()').extract()).strip()
        #用途
        item['useFor'] = ''.join(hxs.select('//span[@id="lbUseFor"]/text()').extract()).strip()
        #开盘日期
        item['openDate'] = ''.join(hxs.select('//span[@id="lbOpenDate"]/text()').extract()).strip()
        #设计单位
        item['buildingDesign'] = ''.join(hxs.select('//span[@id="lbBuildingDesign"]/text()').extract()).strip()
        #代理销售企业
        item['seller'] = ''.join(hxs.select('//span[@id="lbSeller"]/text()').extract()).strip()
        #竣工日期
        item['completeDate'] = ''.join(hxs.select('//span[@id="lbCompleteDate"]/text()').extract()).strip()
        #销售电话
        item['sellTele'] = ''.join(hxs.select('//span[@id="lbSellTele"]/text()').extract()).strip()
        #交付日期
        item['acrossDate'] = ''.join(hxs.select('//span[@id="lbAcrossDate"]/text()').extract()).strip()
        
        yield item
        
        #分幢销售汇总信息保存图片   重复URL判断：dont_filter=True,
        yield Request(third_url,callback=self.parse_img,dont_filter=True,meta = {'lf_mc':lfmc,'third_url':third_url})
        
        four_url = 'http://newhouse.hfhome.cn/' + ''.join(hxs.select('//div[@class="detailLp"]/iframe/@src').extract()).strip()
        yield Request(four_url,callback=self.parse_flcxxxx,meta = {'lf_mc':lfmc,'lf_dh':lf_dh})
        
        
    #分幢销售汇总信息保存图片
    def parse_img(self,response):
        print '================33333333333333======================'
        hxs = HtmlXPathSelector(response)
        
        third_url = response.meta['third_url']
        lf_mc = response.meta['lf_mc']
        
        #获取分幢销售汇总信息
        lf_dh = hxs.select('//span[@id="lblDH"]/text()').extract()
        xshzxxUrls = hxs.xpath('//table[@id="dlfdInfo"]//table[@class="unnamed7"]/tr[2]')
        #xshzxxNames = hxs.select('//table[@id="dlfdInfo"]//table[@class="unnamed7"]')

        img_items = ImageItem()
        img_items['bz'] = 'img'
        
        #网上销售总套数URL
        wsxxztsURL = xshzxxUrls.xpath('./td[1]//img/@src').extract()
        #现可售套数URL
        xkstsURL = xshzxxUrls.xpath('./td[2]//img/@src').extract()
        #已签约套数URL
        yqytsURL = xshzxxUrls.xpath('./td[3]//img/@src').extract()
        #已备案套数URL
        ybatsURL = xshzxxUrls.xpath('./td[4]//img/@src').extract()
        #已成交住宅均价URL
        ycjzzjjURL = xshzxxUrls.xpath('./td[5]//img/@src').extract()
        #已成交商业均价URL
        ycjsyjjURL = xshzxxUrls.xpath('./td[6]//img/@src').extract()
        
        #网上销售总套数图片路径
        wsxxztsImgPath = hashlib.sha1('http://newhouse.hfhome.cn/'+wsxxztsURL[0]).hexdigest() + '.jpg'
        #现可售套数图片路径
        xkstsImgPath = hashlib.sha1('http://newhouse.hfhome.cn/'+xkstsURL[0]).hexdigest() + '.jpg'
        #已签约套数图片路径
        yqytsImgPath = hashlib.sha1('http://newhouse.hfhome.cn/'+yqytsURL[0]).hexdigest() + '.jpg'
        #已备案套数图片路径
        ybatsImgPath = hashlib.sha1('http://newhouse.hfhome.cn/'+ybatsURL[0]).hexdigest() + '.jpg'
        #已成交住宅均价图片路径
        ycjzzjjImgPath = hashlib.sha1('http://newhouse.hfhome.cn/'+ycjzzjjURL[0]).hexdigest() + '.jpg'
        #已成交商业均价图片路径
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
        #获取参数
        lf_mc = response.meta['lf_mc']
        lf_dh = response.meta['lf_dh']
        wsxxztsImgPath = response.meta['wsxxztsImgPath']
        xkstsImgPath = response.meta['xkstsImgPath']
        yqytsImgPath = response.meta['yqytsImgPath']
        ybatsImgPath = response.meta['ybatsImgPath']
        ycjzzjjImgPath = response.meta['ycjzzjjImgPath']
        ycjsyjjImgPath = response.meta['ycjsyjjImgPath']
        
        #网上销售总套数
        wsxxzts = imageToText.getverify1('D:/scrapySpace/tutorial/images/full/'+wsxxztsImgPath,'Y')
        #现可售套数
        xksts = imageToText.getverify1('D:/scrapySpace/tutorial/images/full/'+xkstsImgPath,'Y')
        #已签约套数
        yqyts = imageToText.getverify1('D:/scrapySpace/tutorial/images/full/'+yqytsImgPath,'Y')
        #已备案套数
        ybats = imageToText.getverify1('D:/scrapySpace/tutorial/images/full/'+ybatsImgPath,'Y')
        #已成交住宅均价
        ycjzzjj = imageToText.getverify1('D:/scrapySpace/tutorial/images/full/'+ycjzzjjImgPath,'Y')
        #已成交商业均价
        ycjsyjj = imageToText.getverify1('D:/scrapySpace/tutorial/images/full/'+ycjsyjjImgPath,'Y')
        
        items = FzxshzxxItem()
        #标志
        items['bz'] = 'fzxshzxx'
        #楼房名称
        items['lf_mc'] = lf_mc
        #栋号
        items['lf_dh'] = lf_dh[0]
        #网上销售总套数
        items['wsxxzts'] = list(wsxxzts)[0].replace('\n\n','').replace('.','6')
        #现可售套数
        items['xksts'] = list(xksts)[0].replace('\n\n','').replace('.','6')
        #已签约套数
        items['yqyts'] = list(yqyts)[0].replace('\n\n','').replace('.','6')
        #已备案套数
        items['ybats'] = list(ybats)[0].replace('\n\n','').replace('.','6')
        #已成交住宅均价
        items['ycjzzjj'] = list(ycjzzjj)[0].replace('\n\n','').replace('.','6')
        #已成交商业均价
        items['ycjsyjj'] = list(ycjsyjj)[0].replace('\n\n','').replace('.','6')
        #网上销售总套数图片路径
        items['wsxxztsImgPath'] = wsxxztsImgPath
        #现可售套数图片路径
        items['xkstsImgPath'] = xkstsImgPath
        #已签约套数图片路径
        items['yqytsImgPath'] = yqytsImgPath
        #已备案套数图片路径
        items['ybatsImgPath'] = ybatsImgPath
        #已成交住宅均价图片路径
        items['ycjzzjjImgPath'] = ycjzzjjImgPath
        #已成交商业均价图片路径
        items['ycjsyjjImgPath'] = ycjsyjjImgPath
        
        yield items
        
    def parse_flcxxxx(self,response):
        print '>>>>>>>>>>44444444444444>>>>>>>>>>'
        hxs = HtmlXPathSelector(response)
        
        #获取参数
        lf_mc = response.meta['lf_mc']
        lf_dh = response.meta['lf_dh']
        
        #获取分楼层详细信息
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
        
        #获取参数
        lf_mc = response.meta['lf_mc']
        lf_dh = response.meta['lf_dh']
        lc_mc = response.meta['lc_mc']
        lcxx_url = response.meta['lcxx_url']
        #房间号
        partNO = ''.join(hxs.select('//span[@id="lbPartNO"]/text()').extract()).strip()
        #套型
        houseType = ''.join(hxs.select('//span[@id="lbHouseType"]/text()').extract()).strip()
        #建筑面积
        buildAreaUrl = 'http://newhouse.hfhome.cn/Modal/' + ''.join(hxs.select('//span[@id="lbBuildArea"]/img/@src').extract()).strip()
        #套内面积
        insideAreaUrl = 'http://newhouse.hfhome.cn/Modal/' + ''.join(hxs.select('//span[@id="lbInsideArea"]/img/@src').extract()).strip()
        #分摊面积
        joinAreaUrl = 'http://newhouse.hfhome.cn/Modal/' + ''.join(hxs.select('//span[@id="lbJoinArea"]/img/@src').extract()).strip()
        #建筑结构
        structure = ''.join(hxs.select('//span[@id="lbStructure"]/text()').extract()).strip()
        #房屋用途
        houseUseUrl = 'http://newhouse.hfhome.cn/Modal/' + ''.join(hxs.select('//span[@id="lbHouseUsefulness"]/img/@src').extract()).strip()
        #销售状态
        sellFlagUrl = 'http://newhouse.hfhome.cn/Modal/' + ''.join(hxs.select('//span[@id="lbSellFlag"]/img/@src').extract()).strip()
        #坐落地址
        location = ''.join(hxs.select('//span[@id="lbLocation"]/text()').extract()).strip()
        #建筑面积图片名
        buildAreaImg = hashlib.sha1(buildAreaUrl).hexdigest() + '.jpg'
        #套内面积图片名
        insideAreaImg = hashlib.sha1(insideAreaUrl).hexdigest() + '.jpg'
        #分摊面积图片名
        joinAreaImg = hashlib.sha1(joinAreaUrl).hexdigest() + '.jpg'
        #房屋用途图片名
        houseUseImg = hashlib.sha1(houseUseUrl).hexdigest() + '.jpg'
        #销售状态图片名
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
        #获取参数
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
        #标志
        items['bz'] = 'flcxxxx'
        #楼房名称
        items['lf_mc'] = lf_mc
        #栋号
        items['lf_dh'] = lf_dh
        #楼层号
        items['lc_mc'] = lc_mc
        #房间号
        items['partNO'] = partNO
        #套型
        items['houseType'] = houseType
        #建筑面积
        items['buildArea'] = list(buildArea)[0].replace('\n\n','')
        #套内面积
        items['insideArea'] = list(insideArea)[0].replace('\n\n','')
        #分摊面积
        items['joinArea'] = list(joinArea)[0].replace('\n\n','')
        #建筑结构
        items['structure'] = structure
        
        #替换乱码
        zz_lm = unicode('琏膏','gbk')
        zz = unicode('住宅','gbk')
        
        yba_lm = unicode('己蚤票','gbk')
        yba = unicode('已备案','gbk')
        
        cc_lm = unicode('@裤','gbk')
        cc = unicode('仓储','gbk')
        
        bgmc_lm = unicode('灯公','gbk')
        bgmc = unicode('办公','gbk')
        #房屋用途
        items['houseUse'] = list(houseUse)[0].replace('\n\n','').replace(zz_lm,zz).replace(cc_lm,cc).replace(bgmc_lm,bgmc)
        #销售状态
        items['sellFlag'] = list(sellFlag)[0].replace('\n\n','').replace(yba_lm,yba)
        #坐落地址
        items['location'] = location
        #建筑面积图片名
        items['buildAreaImg'] = buildAreaImg
        #套内面积图片名
        items['insideAreaImg'] = insideAreaImg
        #分摊面积图片名
        items['joinAreaImg'] = joinAreaImg
        #房屋用途图片名
        items['houseUseImg'] = houseUseImg
        #销售状态图片名
        items['sellFlagImg'] = sellFlagImg
        
        yield items
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    