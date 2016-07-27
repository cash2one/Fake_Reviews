#coding=utf-8
'''
Created on 2016年7月17日

@author: hadoop
'''
import numpy as np
import xlrd
import os
import csv
import time
import jieba
import util.util as ul

"""
根据商品评论，获取用户编号，写如csv中-用于相似矩阵等
input: 商品评论csv文件路径
output:
     用户编号csv
"""
def gen_userid(readfilepath,writefilepath):
    f = open(writefilepath, 'w')
    
    reviews_rows = ul.read_csv_file(readfilepath)
    reviews_rows.next()
    for row in reviews_rows:
        #print row[15]
        #print type(row[15])
        ul.write_csv_file(writefilepath, row[15])
        

"""
对评论进行分词-去停止词，写入csv
input: 商品评论csv文件路径
output:
     多一维分词后的csv
"""
def cut_review_to_csv(readfilepath,writefilepath):
    reviews_rows = ul.read_csv_file(readfilepath)
    ul.write_csv_file_w(writefilepath, ','.join(reviews_rows.next())+",分词")#写表头
 
    for row in reviews_rows:
        words = ul.segmentation_with_stop(row[6], "str")
        print words
        newrow = (','.join(row))+(",")+words.encode("utf-8")#Unicode需要变成str
        print newrow
        #seg_result = ' '.join(seg_list)
        #print (words)
        #print type(','.join(row)),','.join(row)
        
        ul.write_csv_file(writefilepath, newrow)



"""
将某用户的历史评论写入相应的csv中
input: 用户编号、行数据
output:
     某用户的历史评论csv
"""
def write_reviews_by_userid(user_id,row):
    file_name = "../result/reviewsbypreprocessing/user/"+user_id+".csv"
    f = open(file_name,'ab')
    write = csv.writer(f)
    write.writerow(row)
    f.close() 
"""
按用户将历史评论切分
input: 历史评论文件路径
output:
    某用户的历史评论csv
"""
def split_reviews_by_user(filepath,useridfile):
    t0 = time.time() 
    f_user = open(useridfile)
    rows_user  = csv.reader(f_user) 
    for row_user in rows_user:
        print row_user[0] 
        f_reviews = open(filepath)
        rows_review = csv.reader(f_reviews)
        rows_review.next()
        
        #先新建用户空文件
        file_name = "../result/reviewsbypreprocessing/user/"+row_user[0] +".csv"
        f = open(file_name,'w')
        
        
        flag="wx"
        
        for row_review in rows_review:
            user_id = row_review[12]
            
            #print user_id,'-and-',row_user[0]
            if user_id == row_user[0]:
                t3 = time.time()
                flag="yx"
                #print "有-yx"
                print user_id ,"的记录为",row_review[0],' ',str(row_review[1]),' ',str(row_review[12]),"-",t3-t0
                #print row
                write_reviews_by_userid(user_id,row_review)
            else:
                if flag == "yx":
                    flag=="wx"
                    print "flag-",flag,"-break"
                    break 
            

        
#gen_userid("../data/food_reviews/reviews_4k.csv","../data/user_id.csv")
#cut_review_to_csv("../data/food_reviews/reviews_4k.csv","../result/reviewsbypreprocessing/reviews_4k_cut.csv")


split_reviews_by_user("../data/personal_reviews/all_reviews_sort_30w_without4510.csv","../data/userid/userid_sort.csv")