# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#一、合肥楼盘信息
class HfHomeItem(scrapy.Item):
    bz = scrapy.Field()
    #所属地区
    lf_dq = scrapy.Field()
    #楼房名称
    lf_mc = scrapy.Field()
    #新上市标志
    lf_new_bz = scrapy.Field()
    #备案名称
    lf_bamc = scrapy.Field()
    #推广名称与备案名称不相符标志
    lf_bxfmc_bz = scrapy.Field()
    
#二、分楼盘详细信息
class FlpxxxxItem(scrapy.Item):
    bz = scrapy.Field()
    #楼盘名称
    lf_mc = scrapy.Field()
    #可售幢数
    sellTotal = scrapy.Field()
    #尾房幢数
    wf_num = scrapy.Field()
    #售完幢数
    sell_num = scrapy.Field()
    #住宅套数
    sellHouse_Num = scrapy.Field()
    #商业套数
    sellBiz_num = scrapy.Field()
    #办公套数
    sellOffice_num = scrapy.Field()
    #其他套数
    sellOther_num = scrapy.Field()
    #所在区域
    district = scrapy.Field()
    #物业类别
    servicesType = scrapy.Field()
    #建筑类型
    buildingType = scrapy.Field()
    #售楼电话
    sellTele = scrapy.Field()
    #售楼处
    sellAddress = scrapy.Field()
    #项目地址
    location = scrapy.Field()
    #交通状况
    trafficInfo = scrapy.Field()
    #开发商
    companyName = scrapy.Field()
    #交付标准
    buyRules = scrapy.Field()
    #项目退换房累计换手套数
    quit_num = scrapy.Field()
    #项目退换房累计换手率
    quit_hsl = scrapy.Field()
    #幢数总计
    buildingCount = scrapy.Field()
    #建筑面积
    buildArea = scrapy.Field()
    #土地面积
    itemGetArea = scrapy.Field()
    #容积率
    rjl = scrapy.Field()
    #建筑设计单位
    buildDesign = scrapy.Field()
    #环境设计单位
    servicesCompany = scrapy.Field()
    #物业公司
    entironmentDesign = scrapy.Field()
    #物业电话
    prtel = scrapy.Field()
    #物业费
    prcost = scrapy.Field()
    #车位配比
    parking = scrapy.Field()
    #供暖设施
    heating = scrapy.Field()
    #周边环境
    entironment = scrapy.Field()
    
#三、分幢成交汇总信息
class FzcjxxhzItem(scrapy.Item):
    #标志
    bz = scrapy.Field()
    #楼房名称
    lf_mc = scrapy.Field()
    #栋号
    lf_dh = scrapy.Field()
    #是否列入预售款监管
    sflryskjg = scrapy.Field()
    #许可证号码
    license_num = scrapy.Field()
    #地上楼层数
    overground_count = scrapy.Field()
    #地下楼层数
    underground_count = scrapy.Field()
    #住宅
    house_count = scrapy.Field()
    #商业
    business_count = scrapy.Field()
    #办公
    office_count = scrapy.Field()
    #其他
    other_count = scrapy.Field()
    #详细信息入口url
    detailInfUrl = scrapy.Field()

#四、许可证详细信息
class XkzxxxxItem(scrapy.Item):
    #标志
    bz = scrapy.Field()
    #楼房名称
    lf_mc = scrapy.Field()
    #幢号
    lf_dh = scrapy.Field()
    #许可证号
    permitNO = scrapy.Field()
    #地上层数
    realFloors = scrapy.Field()
    #地下层数
    minFloors = scrapy.Field()
    #土地使用权证
    landNO = scrapy.Field()
    #套数
    sets = scrapy.Field()
    #规划许可证
    scaleNO = scrapy.Field()
    #预售许可面积
    permitArea = scrapy.Field()
    #建筑结构
    buildFramework = scrapy.Field()
    #网上销售总面积
    selledArea = scrapy.Field()
    #用途
    useFor = scrapy.Field()
    #开盘日期
    openDate = scrapy.Field()
    #设计单位
    buildingDesign = scrapy.Field()
    #代理销售企业
    seller = scrapy.Field()
    #竣工日期
    completeDate = scrapy.Field()
    #销售电话
    sellTele = scrapy.Field()
    #交付日期
    acrossDate = scrapy.Field()
    
#五、分幢销售汇总信息
class FzxshzxxItem(scrapy.Item):
    #标志
    bz = scrapy.Field()
    #楼房名称
    lf_mc = scrapy.Field()
    #栋号
    lf_dh = scrapy.Field()
    #网上销售总套数
    wsxxzts = scrapy.Field()
    #现可售套数
    xksts = scrapy.Field()
    #已签约套数
    yqyts = scrapy.Field()
    #已备案套数
    ybats = scrapy.Field()
    #已成交住宅均价
    ycjzzjj = scrapy.Field()
    #已成交商业均价
    ycjsyjj = scrapy.Field()
    #网上销售总套数图片路径
    wsxxztsImgPath = scrapy.Field()
    #现可售套数图片路径
    xkstsImgPath = scrapy.Field()
    #已签约套数图片路径
    yqytsImgPath = scrapy.Field()
    #已备案套数图片路径
    ybatsImgPath = scrapy.Field()
    #已成交住宅均价图片路径
    ycjzzjjImgPath = scrapy.Field()
    #已成交商业均价图片路径
    ycjsyjjImgPath = scrapy.Field()

#下载图片item
class ImageItem(scrapy.Item):
    bz = scrapy.Field()
    image_urls = scrapy.Field()
    imgName = scrapy.Field()
    image_paths = scrapy.Field()
    
#六、分楼层详细信息
class FlcxxxxItem(scrapy.Item):
    #标志
    bz = scrapy.Field()
    #楼房名称
    lf_mc = scrapy.Field()
    #栋号
    lf_dh = scrapy.Field()
    #楼层号
    lc_mc = scrapy.Field()
    #房间号
    partNO = scrapy.Field()
    #套型
    houseType = scrapy.Field()
    #建筑面积
    buildArea = scrapy.Field()
    #套内面积
    insideArea = scrapy.Field()
    #分摊面积
    joinArea = scrapy.Field()
    #建筑结构
    structure = scrapy.Field()
    #房屋用途
    houseUse = scrapy.Field()
    #销售状态
    sellFlag = scrapy.Field()
    #坐落地址
    location = scrapy.Field()
    #建筑面积图片名
    buildAreaImg = scrapy.Field()
    #套内面积图片名
    insideAreaImg = scrapy.Field()
    #分摊面积图片名
    joinAreaImg = scrapy.Field()
    #房屋用途图片名
    houseUseImg = scrapy.Field()
    #销售状态图片名
    sellFlagImg = scrapy.Field()
    
    
    
    
    
    
    
    
    
    
    
    
    
    