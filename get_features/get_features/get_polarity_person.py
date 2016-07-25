#coding=utf-8
'''
Created on 2016年7月18日

@author: hadoop
'''
import util.util as fp
import jieba
import util.util as ul
import statistics.sentiment_polarity as sp
import statistics.getperson as sg

def save_polarity_person_cvs():
    # Load dataset
    #review = get_excel_data("./data/reviews.xlsx", "1", "1", "data") 
    savepath="../result/reviews_with_features/reviews_4k_cut_polarity_person.csv"
    
    review = ul.read_csv_file("../result/reviewsbypreprocessing/reviews_4k_cut.csv")
    ul.write_csv_file_w(savepath, ",".join(review.next())+",第一人称,其他人才,人称之差,正向极性,反向极性,正向平均值,反向平均值,正向方差,反向方差,总体极性（正反差）")
    
    ii=1
    for re in review:
        #人称统计
        st_person = sg.statistics_person(re[6])
        print st_person[0],"-",st_person[1],"-",st_person[2]
        str_st_person = str(st_person[0])+","+str(st_person[1])+","+str(st_person[2])
        print str_st_person
        #统计极性
        st_score = sp.single_review_sentiment_score(re[6].decode("utf-8"))
        print st_score[0],"-",st_score[1],"-",st_score[2],"-",st_score[3],"-",st_score[4],"-",st_score[5]
        str_st_score = str(st_score[0])+","+str(st_score[1])+","+str(st_score[2])+","+str(st_score[3])+","+str(st_score[4])+","+str(st_score[5])+","+ str(st_score[0]-st_score[1])
        print str_st_score
        #写到文件中
        newrow = ",".join(re)
        print type(newrow),type(str_st_person),type(str_st_score)
        ul.write_csv_file(savepath,newrow+","+str(str_st_person)+","+str(str_st_score) )
        
        
        #print type(re[6].decode("utf-8")),re[6].decode("utf-8")
        #print '第',ii,'条-',sp.single_review_sentiment_score(re[6].decode("utf-8"))
        #print re[6]
        #print
        
        #f.write(str(single_review_sentiment_score(re)[0])+'\t'+str(single_review_sentiment_score(re)[1])+'\t'+str(single_review_sentiment_score(re)[0]-single_review_sentiment_score(re)[1])+'\t'+str(single_review_sentiment_score(re)[2])+'\t'+str(single_review_sentiment_score(re)[3])+'\t'+str(single_review_sentiment_score(re)[4])+'\t'+str(single_review_sentiment_score(re)[5])+'\t'+'\n')
        ii=ii+1
#save_polarity_person_cvs()
