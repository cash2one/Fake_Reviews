#coding=utf-8
'''
Created on 2016年7月18日

@author: hadoop
'''
import util.util as fp
import jieba

#统计人称数据
def statistics_person(reviews):
    #for re in reviews:
    #re_segs = reviews.split()
    rewcut=fp.segmentation(reviews,"list")
    first=0
    other=0
    print rewcut
    for word in rewcut:
        if word in first_persondict:
            print word,":第一人称"
            first=first+1
        elif word in other_persondict:
            print word,":其他人称"
            other=other+1
        #else:
            #print word,":不在词典内"
    return first,other,abs(first-other)#,first/(first+other),other/(first+other)
   
#加载人称词典

first_persondict = fp.read_txt_file('../dict/dictionary_of_person/first_person.txt', 'lines')
other_persondict = fp.read_txt_file('../dict/dictionary_of_person/other_person.txt', 'lines')
 
#统计人称数据
#print statistics_person("你们的同妈妈去，我叫了烧鸡，榴莲披萨，老公 阿姨烧鸡98元一只，朋友比超市19元一只的难吃，骚味，差！披萨可以食！鸡尾酒好饮！今次第二次去，打算带妈妈体验体验，结果这样！下次都不会再去了！")[1] 

#统计转折词

#统计复杂



