# coding:utf-8

import Image
import ImageEnhance
import ImageFilter
import sys
import subprocess
import os

# ��ֵ��  
threshold = 140 
table = []  
for i in range(256):  
    if i < threshold:  
        table.append(0)  
    else:  
        table.append(1)  
   
#����ʶ�����ĸ�� ���øñ��������  
rep={'O':'0',  
    'I':'1','L':'1',  
    'Z':'2',  
    'S':'8'
    };  
   
def getverify1(name,bz):
    #��ͼƬ  
    im = Image.open(name)  
    #ת�����Ҷ�ͼ
    imgry = im.convert('L')
    name1 = name.split('/')[-1]
    #����ͼ��
    imgry.save('g'+name1)  
    #��ֵ����������ֵ�ָ��thresholdΪ�ָ�� 
    out = imgry.point(table,'1')  
    out.save('b'+name1)  
    outName = 'b'+name1
    
    #ʶ��  
    if bz == 'Y':
        #ʶ������
        proc = subprocess.Popen('tesseract '+outName+' 11 -psm 7 nobatch digits')
    elif bz == 'N':
        #ʶ������
        proc = subprocess.Popen('tesseract '+outName+' 11 -l chi_sim -psm 7')
        
    retcode = proc.wait()
            
    file = open('11.txt','r')
    text = file.read()
    #ʶ�����
    for r in rep:
        text = text.replace(r,rep[r])
    text = text.replace(' ','').replace('733','')
    
    file1 = open('11.txt','w')
    file1.write(text)
    
    os.remove(outName)
    os.remove('g'+name1)
    yield text
