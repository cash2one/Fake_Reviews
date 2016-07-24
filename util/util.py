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

""" Sentence cutting algorithm without bug, but a little difficult to explain why"""
#评论->句子
def cut_sentence(words):
    print type(words),words
    #words = (words).decode('utf8')
    start = 0
    i = 0 #i is the position of words
    token = 'meaningless'
    sents = []
    punt_list = ',.    !?;~，。 ！？；～… '.decode('utf8')
    for word in words:
        if word not in punt_list:
            i += 1
            token = list(words[start:i+2]).pop()
            #print token
        elif word in punt_list and token in punt_list:
            i += 1
            token = list(words[start:i+2]).pop()
        else:
            sents.append(words[start:i+1])
            start = i+1
            i += 1
    if start < len(words):
        sents.append(words[start:])
    #print "sents",sents[0]
    return sents
 
"""
对句子进行分词
input: 这款手机大小合适。
output:
    parameter_1: 这 款 手机 大小 合适 。(unicode)
    parameter_2: [u'\u8fd9', u'\u6b3e', u'\u624b\u673a', u'\u5927\u5c0f', u'\u5408\u9002', u'\uff0c']
"""
def segmentation(sentence, para):
    if para == 'str':
        seg_list = jieba.cut(sentence)
        seg_result = ' '.join(seg_list)#以' '作为分隔符，将seg_list所有的元素合并成一个新的字符串
        return seg_result
    elif para == 'list': 
        seg_list2 = jieba.cut(sentence)
        
        seg_result2 = []
        for w in seg_list2:
            #print w
            seg_result2.append(w) 
        return seg_result2
"""
对句子进行分词+去停止词
input: 这款手机大小合适。
output:
    parameter_1: 这 款 手机 大小 合适 。(unicode)
    parameter_2: [u'\u8fd9', u'\u6b3e', u'\u624b\u673a', u'\u5927\u5c0f', u'\u5408\u9002', u'\uff0c']
"""
def segmentation_with_stop(sentence, para):
    stop = [line.strip().decode('utf-8') for line in open('../dict/others/stopword.txt').readlines()]
    if para == 'str':
        seg_list = jieba.cut(sentence)
        #seg_result = ' '.join(seg_list)#以' '作为分隔符，将seg_list所有的元素合并成一个新的字符串
        seg_result = ' '.join(list(set(seg_list)-set(stop)-set('\n')-set('\r\n')-set('\r')))#以' '作为分隔符，将seg_list所有的元素合并成一个新的字符串
        return seg_result
    elif para == 'list': 
        seg_list2 = jieba.cut(sentence)
        
        seg_result2 = []
        for w in seg_list2:
            #print w
            seg_result2.append(w) 
        return seg_result2
"""
读取指定路径下的csv文件
input: 文件路径。
output:
    csv文件对象
"""
def read_csv_file(filepath):
    f_csv = open(filepath)
    rows  = csv.reader(f_csv) 
    return rows    
    
"""
读取某用户的历史评论csv文件
input: 用户ID。
output:
        用户历史评论
""" 
def read_csv_file_by_user(userid):
    f_user = open("./data/user/"+userid+".csv")
    rows_user  = csv.reader(f_user) 
    return rows_user  
"""
将行“str”写入csv中 append
input: 保存路径、行数据
output:
        csv文件
""" 
def write_csv_file(filepath,row):
    #coding:utf-8
    f = open(filepath, 'a')
    write = csv.writer(f)
    #row=row.strip('\n')
    seg_result = (row)
    #print type(row) 
    f.write(seg_result+'\n')
    f.close()
    
def write_csv_file_w(filepath,row):
    #coding:utf-8
    f = open(filepath, 'w')
    write = csv.writer(f)
    #row=row.strip('\n')
    seg_result = (row)
    #print type(row) 
    f.write(seg_result+'\n')
    f.close()

"""读取字典
input:
    parameter_1: A txt file with many lines
    parameter_2: A txt file with only one line of data
output:
    parameter_1: Every line is a value of the txt_data list. (unicode)
    parameter_2: Txt data is a string. (str)
"""   
def read_txt_file(filepath, para):
    if para == 'lines':
        txt_file1 = open(filepath, 'r')
        txt_tmp1 = txt_file1.readlines()
        txt_tmp2 = ''.join(txt_tmp1)
        txt_data1 = txt_tmp2.decode('utf8').split('\n')
        txt_file1.close()
        return txt_data1
    elif para == 'line':
        txt_file2 = open(filepath, 'r')
        txt_tmp = txt_file2.readline()
        txt_data2 = txt_tmp.decode('utf8')
        txt_file2.close()
        return txt_data2   
#------------------------------------------------    
    
    

def get_excel_data(filepath, sheetnum, colnum, para):
    table = xlrd.open_workbook(filepath)
    #sheet = table.sheets()[sheetnum-1]
    #data = sheet.col_values(colnum-1)
    sheet = table.sheets()[0]
    data = sheet.col_values(0)
    rownum = sheet.nrows
    if para == 'data':
        return data
    elif para == 'rownum':
        return rownum
 
    
def sava_txt_data(storepath,sentence):
    sava_file = open(storepath, 'a')
    #print sentence,"sava_file"
    sava_file.write(sentence.encode("utf-8")+'\n')#写入txt 时不要忘了编码 str(sentence)+'\n'
    sava_file.close()
    
    
#记录已存在的user_id.csv
user_dictionary = {}



def writeByUserID(user_id,row):
    file_name = "./data/user/"+user_id+".csv"
    f = open(file_name,'ab')
    write = csv.writer(f)
    write.writerow(row)
    f.close()
    #os.chdir("../../preprocess/")
def writeDataCsv(filepath,row):
    #coding:utf-8
    f = open('../results/reviewscut.csv', 'a')
    write = csv.writer(f)
    #row=row.strip('\n')
    seg_result = (row.encode("utf-8"))
    
    f.write(seg_result+'\n')
    f.close()
def splitByUser(filepath):
    f_user = open("./data/all_user_sort.csv")
    rows_user  = csv.reader(f_user)
    #users=[]
    for row_user in rows_user:
        print row_user
        #users.append(row)
        ff = open(filepath)
        rows = csv.reader(ff)
        rows.next()
        flag="wx"
        for row in rows:
            user_id = row[12]
            t3 = time.time() 
            #print user_id,'-and-',row_user[0]
            if user_id == row_user[0]:
                flag="yx"
                print "有-yx"
                #print user_id ,"的记录为",row[0],' ',str(row[1]),' ',str(row[12]),"-",t3-t0
                #print row
                writeByUserID(user_id,row)
            else:
                if flag == "yx":
                    flag=="wx"
                    print "flag-",flag,"-break"
                    break 
                    
                
                #print "wu"
                #writeByUserID(user_id,words)
        #words.extend(row[1:])
        #writeByUserID(user_id,words)



 

def readAllUser():
    
    f_user = open("../Statistics/data/reviews_all_4990.csv")
    rows_user  = csv.reader(f_user)
    rows_user.next()
    return rows_user

'''
userdata = readAllUser()#readByUser("55503779","")
for row_user in userdata:
    print row_user[5]
'''    
    
    
#writeDataCsv("../results/reviewscut2.csv","是奥迪")
#writeByUserID("reviewscut3","是奥迪")
#print userdata
'''split by user  
t0 = time.time() 
splitByUser("./data/review_all_sort.csv")
t1 = time.time()
print "It takes %f s to split by user 'data/date/*.csv'" %(t1-t0)
'''




''' 
def splitByUser_xlsx(filepath):
    table = xlrd.open_workbook(filepath)
    sheet = table.sheets()[0]
    #print sheet
    #data = sheet.col_values(0)
    #print data
    data2 = sheet.row_values(1)[1]
    print data2
    rownum = sheet.nrows
    #print rownum
    #rows = sheet.row_values()
    i=1
    for i in range(rownum):
        userid=sheet.row_values(i)[12]
        print userid
       
            
        
splitByUser_xlsx("./data/reviews0.xlsx")
'''  
