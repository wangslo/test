# coding:utf-8

import Image
import ImageEnhance
import ImageFilter
import sys
import subprocess
import os

# 二值化  
threshold = 140 
table = []  
for i in range(256):  
    if i < threshold:  
        table.append(0)  
    else:  
        table.append(1)  
   
#对于识别成字母的 采用该表进行修正  
rep={'O':'0',  
    'I':'1','L':'1',  
    'Z':'2',  
    'S':'8'
    };  
   
def getverify1(name,bz):
    #打开图片  
    im = Image.open(name)  
    #转化到灰度图
    imgry = im.convert('L')
    name1 = name.split('/')[-1]
    #保存图像
    imgry.save('g'+name1)  
    #二值化，采用阈值分割法，threshold为分割点 
    out = imgry.point(table,'1')  
    out.save('b'+name1)  
    outName = 'b'+name1
    
    #识别  
    if bz == 'Y':
        #识别数字
        proc = subprocess.Popen('tesseract '+outName+' 11 -psm 7 nobatch digits')
    elif bz == 'N':
        #识别中文
        proc = subprocess.Popen('tesseract '+outName+' 11 -l chi_sim -psm 7')
        
    retcode = proc.wait()
            
    file = open('11.txt','r')
    text = file.read()
    #识别对吗
    for r in rep:
        text = text.replace(r,rep[r])
    text = text.replace(' ','').replace('733','')
    
    file1 = open('11.txt','w')
    file1.write(text)
    
    os.remove(outName)
    os.remove('g'+name1)
    yield text
