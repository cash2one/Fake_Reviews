#coding=utf-8
'''
Created on 2016年7月19日

@author: hadoop
'''

 

#import util.fileprocessing as fp
import logging
from gensim import corpora, models, similarities
import csv
import jieba
import os


def read_csv_file(filepath):
    f_csv = open(filepath)
    rows  = csv.reader(f_csv)
    rows.next() 
    print "read_csv_file\n"
    #for row in rows:
        #print row[7]
    return rows

def read_csv_file_nonext(filepath):
    f_csv = open(filepath)
    rows  = csv.reader(f_csv)
    print "read_csv_file\n"
    #for row in rows:
        #print row[7]
    return rows

def write_csv_file(filepath,row):
    #coding:utf-8
    f = open(filepath, 'a')
    write = csv.writer(f)
    #row=row.strip('\n')
    seg_result = (row)
    #print type(row) 
    f.write(seg_result+'\n')
    f.close()
#分词
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


def similarity_toMatrix(datapath, querypath, storepath):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    class MyCorpus(object):
        def __iter__(self):
            #载入语料库(评论数据集4k)
            rows = read_csv_file(datapath)
            for line in rows:
                #print line[22]+"line[22]"
                #print line[7].split()
                #print line.split()
                #print str(line[7]).split()
                #print (line[7].decode("utf-8")).split(),"========"
                yield line[22].split()
                
            #for line in open(datapath):
                #yield line.split()
    #将网页文档转化为tf-idf
    #以下是把评论通过gensim 转化为tf-idf 形式，程序具体解释参见52nlp的博客或gensim官方文档
    Corp = MyCorpus()
    print "Corp",Corp,"---------"   
    
    dictionary = corpora.Dictionary(Corp)
    corpus = [dictionary.doc2bow(text) for text in Corp]#把所有评论转化为词包（bag of words）
    #print "corpus",corpus,"---------" 
    
    #print corpus
    tfidf = models.TfidfModel(corpus)#使用tf-idf 模型得出该评论集的tf-idf 模型
    #print "tfidf",tfidf,"---------" 
    corpus_tfidf = tfidf[corpus]#此处已经计算得出所有评论的tf-idf 值
    #print "corpus_tfidf",corpus_tfidf,"---------" 
    
    q_file = read_csv_file(querypath)#open(querypath, 'r')#读取待计算的商品评论
    q_file2 = read_csv_file(querypath)
    #生产评分矩阵
    
    #toMatrix(q_file,q_file2,"../result/data/usermatrix.csv")    
    users_id = []
    matrixfile = open(storepath, 'ab')
 
    for qrow2 in q_file2:#把每条评论当作搜索词
        print " for q_row2 in q_file2:"
        #print "for q_row in q_file"
        userid=  qrow2[15]
        query = qrow2[22]
        #query = "酒水 两百 消费 300 团购 人均 出品 还会 白开水 ~ 不错 豪吃 提供 券 哈哈哈 餐饮 美中不足"
        print userid,"------------"  
        print query,"------------" 
        vec_bow = dictionary.doc2bow(query.split())#把商品描述转为词包
        vec_tfidf = tfidf[vec_bow]#直接使用上面得出的tf-idf 模型即可得出商品描述的tf-idf 值
        
         
        index = similarities.MatrixSimilarity(corpus_tfidf) #把所有评论做成索引
        sims = index[vec_tfidf]#利用索引计算每一条评论和商品描述之间的相似度
        
        similarity = list(sims)#把相似度存储成数组，以便写入txt 文档
        
        #write = csv.writer(matrixfile)
        #row=row.strip('\n')
        #seg_result = (row.encode("utf-8"))
        
        
        ii=0
        point = []
        for sim_point in similarity:
            #print ii,'-',sim_point
            point.append(str(sim_point))
            #sim_file.write(str(sim_point)+'\n')#写入txt 时不要忘了编码
            ii=ii+1
        str_point=",".join(point)
        matrixfile.write(str_point+'\n') 
        print userid+"写成功"+point[0]
        #print str(userid)+','+str_point+'\n'
    print "matrixfile.close()"   
    matrixfile.close()
        #print users_id
     
    
def similarity(datapath, querypath, storepath):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    class MyCorpus(object):
        def __iter__(self):
            rows = read_csv_file(datapath)
            for line in rows:
                #print line[7]+"line[7]"
                #print line[7].split()
                #print line.split()
                #print str(line[7]).split()
                #print (line[7].decode("utf-8")).split(),"========"
                yield line[7].split()
                
            #for line in open(datapath):
                #yield line.split()
    #将网页文档转化为tf-idf
    #以下是把评论通过gensim 转化为tf-idf 形式，程序具体解释参见52nlp的博客或gensim官方文档
    Corp = MyCorpus()
    print "Corp",Corp,"---------"   
    
    dictionary = corpora.Dictionary(Corp)
    corpus = [dictionary.doc2bow(text) for text in Corp]#把所有评论转化为词包（bag of words）
    print "corpus",corpus,"---------" 
    
    #print corpus
    tfidf = models.TfidfModel(corpus)#使用tf-idf 模型得出该评论集的tf-idf 模型
    #print "tfidf",tfidf,"---------" 
    corpus_tfidf = tfidf[corpus]#此处已经计算得出所有评论的tf-idf 值
    #print "corpus_tfidf",corpus_tfidf,"---------" 
    
    q_file = read_csv_file(querypath)#open(querypath, 'r')#读取商品描述的txt 文档
    q_file2 = read_csv_file(querypath)
    #生产评分矩阵
    #toMatrix(q_file,q_file2,"../Statistics/data/usermatrix____100.csv")    
    
    '''
    print "q_file",q_file
    #query = q_file.readline() 
    #求每条评论与其他评论的相似度
    for q_row in q_file:#把每条评论当作搜索词
        #print "for q_row in q_file"
        userid=  q_row[15]
        query = q_row[7]
        #query = "酒水 两百 消费 300 团购 人均 出品 还会 白开水 ~ 不错 豪吃 提供 券 哈哈哈 餐饮 美中不足"
        print userid,"------------"  
        print query,"------------" 
        vec_bow = dictionary.doc2bow(query.split())#把商品描述转为词包
        vec_tfidf = tfidf[vec_bow]#直接使用上面得出的tf-idf 模型即可得出商品描述的tf-idf 值
        
         
        index = similarities.MatrixSimilarity(corpus_tfidf) #把所有评论做成索引
        sims = index[vec_tfidf]#利用索引计算每一条评论和商品描述之间的相似度
        
        similarity = list(sims)#把相似度存储成数组，以便写入txt 文档
        
        sim_file = open(storepath + userid + '.csv', 'w')
        ii=0
             
        for i in similarity:
                #print ii,'-',i
            sim_file.write(str(i)+'\n')#写入txt 时不要忘了编码
            ii=ii+1
        sim_file.close()'''
        
def get_similarity_by_history_reviews(user_id,querypath,query_words):
    #logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    class MyCorpus(object):
        def __iter__(self):
            rows = read_csv_file_nonext("../result/reviewsbypreprocessing/user/"+user_id+'.csv')
            
            for line in rows:
                words=segmentation_with_stop(line[5],"str")
                print line[0]
                print "cut : ",words
                yield words.split()
    #将网页文档转化为tf-idf
    #以下是把评论通过gensim 转化为tf-idf 形式，程序具体解释参见52nlp的博客或gensim官方文档
    
    try:
        Corp = MyCorpus()
        #print "Corp",Corp,"---------\n"   
        
        dictionary = corpora.Dictionary(Corp)
        corpus = [dictionary.doc2bow(text) for text in Corp]#把所有评论转化为词包（bag of words）
        #print "corpus",corpus,"---------\n" 
        
        #print corpus
        tfidf = models.TfidfModel(corpus)#使用tf-idf 模型得出该评论集的tf-idf 模型
        #print "tfidf",tfidf,"---------\n" 
        corpus_tfidf = tfidf[corpus]#此处已经计算得出所有评论的tf-idf 值
        #print "corpus_tfidf",corpus_tfidf,"---------\n" 
         
        #q_file = read_csv_file(querypath)#open(querypath, 'r')#读取商品评论信息作为检索关键字
        #q_file2 = read_csv_file(querypath)
        #生产评分矩阵
        #toMatrix(q_file,q_file2,"../Statistics/data/usermatrix____100.csv")    
        
        
        #print "q_file",q_file
        #query = q_file.readline() 
        #求每条评论与其他评论的相似度
        #for q_row in q_file:#把每条评论当作搜索词
        #print "for q_row in q_file"
        userid =  user_id
         
        #query = "酒水 两百 消费 300 团购 人均 出品 还会 白开水 ~ 不错 豪吃 提供 券 哈哈哈 餐饮 美中不足"
        #print "------------userid[15]:",userid,"------------"  
        #print "------------query_words[22]:",query_words,"------------" 
        vec_bow = dictionary.doc2bow(query_words.split())#把商品描述转为词包
        #print "vec_bow",vec_bow,"---------\n"         
        vec_tfidf = tfidf[vec_bow]#直接使用上面得出的tf-idf 模型即可得出商品描述的tf-idf 值
        #print "vec_tfidf",vec_tfidf,"---------\n" 
         
        #index = similarities.MatrixSimilarity(corpus_tfidf) #把所有评论做成索引
        index = similarities.Similarity('.',tfidf[corpus_tfidf],len(dictionary))        
        #print "index",index,"---------\n" 
        sims = index[vec_tfidf]#利用索引计算每一条评论和商品描述之间的相似度
        #print sims
        #print "sims",sims,"---------\n" 
        similarity = list(sims)#把相似度存储成数组，以便写入txt 文档
        
        
       
        
           
        sim_file = open("../result/reviews_similarity/user_history/" + userid + '.csv', 'w')
        ii=0
             
        for similarity_i in similarity:
            print ii,'-',similarity_i
            #sim_file.write(str(similarity_i)+'\n')#写入txt 时不要忘了编码
            sim_file.write(str(round(similarity_i, 4))+'\n')
                      
            ii=ii+1
        sim_file.close()
    except Exception,e:
        print "yichang:",e
        pass

def similarity_history(reviews_file_path):
    #生成用户历史评论相似文件
    
    rows = read_csv_file(reviews_file_path)  
    ii = 1
    for row in rows:
        user_id = row[15]
        print ii
        if os.path.exists("../result/reviews_similarity/user_history/" + user_id + '.csv'):
            #print "pass:",user_id
            pass
        else:
            print "no pass:",user_id
            
            print "用户：",user_id,"-------------------------"
            #query_words= row[22]
            query_words=  segmentation_with_stop(row[6],"str")
            print "query_words:",query_words,"-------------------------"
            get_similarity_by_history_reviews(user_id,reviews_file_path,query_words)
        ii=ii+1
   
#similarity_toMatrix("../result/reviewsbypreprocessing/reviews_4k_cut.csv","../result/reviewsbypreprocessing/reviews_4k_cut.csv","../result/reviews_similarity/similarity_matrix4.csv")
similarity_history("../data/food_reviews/reviews_4k.csv")
#query_words=  segmentation_with_stop("我发誓这是我吃过最好吃的牛扒！又是吃货好友推荐的！太赞啦！还尝了流奶牛角包和芝士牛角包，流奶的奶香浓郁，特别甜，咬一口都会爆浆！外面脆脆的香香的，横切面的层次也很美！口感好好！芝士的味道也很醇厚~重要的是牛角的酥皮超好吃呀！而且还有一点淡淡的咸味，很喜欢啦！下次再来还要尝试不同味道的！","str")
#print query_words
#get_similarity_by_history_reviews("14294014","../result/reviewsbypreprocessing/reviews_4k_cut.csv",query_words)

#similarity("../Statistics/data/reviews_all_4990.csv","C:/Users/hadoop/Workspaces/MyEclipse Professional 2014/Sentimental_Polarities/Statistics/data/reviews_all_4990.csv","../Statistics/data/reviews_all_4990.csv.txt")
#q_file = fp.read_csv_file("C:/Users/hadoop/Workspaces/MyEclipse Professional 2014/Sentimental_Polarities/Statistics/data/reviews_all_4990.csv")#open(querypath, 'r')#读取商品描述的txt 文档
#for q_row in q_file:
    #print q_row[7]

