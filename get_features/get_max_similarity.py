#coding=utf-8
'''
Created on 2016年7月19日



                   _ooOoo_
                  o8888888o
                  88" . "88
                  (| -_- |)
                  O\  =  /O
               ____/`---'\____
             .'  \\|     |//  `.
            /  \\|||  :  |||//  \
           /  _||||| -:- |||||-  \
           |   | \\\  -  /// |   |
           | \_|  ''\---/''  |   |
           \  .-\__  `-`  ___/-. /
         ___`. .'  /--.--\  `. . __
      ."" '<  `.___\_<|>_/___.'  >'"".
     | | :  `- \`.;`\ _ /`;.`/ - ` : | |
     \  \ `-.   \_ __\ /__ _/   .-` /  /
======`-.____`-.___\_____/___.-`____.-'======
                   `=---='
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                   佛祖保佑       永无BUG
                佛曰:  
                      写字楼里写字间，写字间里程序员；  
                      程序人员写程序，又拿程序换酒钱。  
                      酒醒只在网上坐，酒醉还来网下眠；  
                      酒醉酒醒日复日，网上网下年复年。  
                      但愿老死电脑间，不愿鞠躬老板前；  
                      奔驰宝马贵者趣，公交自行程序员。  
                      别人笑我忒疯癫，我笑自己命太贱；  
                      不见满街漂亮妹，哪个归得程序员？ 

@author: hadoop
'''
import numpy 
import time
import util.util as ul
import math
 
def test():
    t0= time.time() 
    my_matrix = numpy.loadtxt(open("../result/reviews_similarity/similarity_matrix4.csv","rb"),delimiter=",",skiprows=0)
    
    count = 1
    for i in range(my_matrix.shape[0]):
       for j in range(my_matrix.shape[1]): 
           if my_matrix[i][j]>=0.8 and my_matrix[i][j]<1:
               print "第",count,"个","行",i+1,"，列",j+1,my_matrix[i][j]
               count+=1
           #print "行",i,",列",j," : ",my_matrix[i][j]
    t1= time.time() 
    print "花费",t1-t0,"s"
    #print my_matrix
    print my_matrix[1][0]
    print my_matrix[1][1]
    print my_matrix.shape[0]#行
    print my_matrix.shape[1]#列


"""
根据用户评论序号及用户编号获取改评论的最大相似度
input: 用户评论序号、用户编号
output:
      该评论的最大相似度（当前商品评论与该用户的历史评论）
"""
my_matrix = numpy.loadtxt(open("../result/reviews_similarity/similarity_matrix3.csv","rb"),delimiter=",",skiprows=0)
def get_max_similarity(num,userid):
    #读取矩阵的最大相似度！！除去本身
    t0= time.time() 
    
    matrix_score = 0.0
    history_score = 0.0
    count = 1
    try:
        for i in range(my_matrix.shape[1]):#只遍历一行
            if num-1 == i:#去除评论与其本身的相似度
                continue
            if matrix_score<my_matrix[num-1][i]:
               print "第",count,"个","行",num,"，列",i+1,matrix_score,"<",my_matrix[num-1][i]
               matrix_score = my_matrix[num-1][i]
               count+=1
        
    except IndexError,e:
        print e
        pass 
    t1= time.time()
    print "花费",t1-t0,"s"
    
    #读取历史评论的相似度
    count2=1
    try:
        history_similarity = ul.read_csv_file("../result/reviews_similarity/user_history/"+userid+".csv")
        for his_sim in history_similarity:
            if history_score<his_sim[0]:
                print "读取历史评论的相似度:",history_score,"<",his_sim[0]
                history_score = his_sim[0]
    except IOError,e:
        print e
    print matrix_score," ",history_score
    #print matrix_score>=history_score,type(matrix_score),type(float(history_score))
    #返回最大相似度
    if float(matrix_score ) > float(history_score) :#matrix_score>history_score:
        return matrix_score
    else:
        return history_score
    

"""
根据用户评论序号及用户编号获取该评论与商品评论及用户历史评论的最大相似度
input: 用户评论序号、用户编号
output:
      评论与商品评论及用户历史评论的最大相似度 matrix_score,history_score
"""
def get_max_similarity_alone(num,userid):
    #读取矩阵的最大相似度！！除去本身
    t0= time.time() 
    
    matrix_score = 0.0
    history_score = 0.0
    count = 1
    try:
        for i in range(my_matrix.shape[1]):#只遍历一行
            if num-1 == i:#去除评论与其本身的相似度
                continue
            if matrix_score<my_matrix[num-1][i]:
               print "第",count,"个","行",num,"，列",i+1,matrix_score,"<",my_matrix[num-1][i]
               matrix_score = my_matrix[num-1][i]
               count+=1
        
    except IndexError,e:
        print e
        pass 
    t1= time.time()
    print "花费",t1-t0,"s"
    
    #读取历史评论的相似度
    count2=1
    try:
        history_similarity = ul.read_csv_file("../result/reviews_similarity/user_history/"+userid+".csv")
        for his_sim in history_similarity:
            if history_score<his_sim[0]:
                print "读取历史评论的相似度:",history_score,"<",his_sim[0]
                history_score = his_sim[0]
    except IOError,e:
        print e
    print matrix_score," ",history_score
    #print matrix_score>=history_score,type(matrix_score),type(float(history_score))
    #返回最大相似度
    #if float(matrix_score ) > float(history_score) :#matrix_score>history_score:
        #return matrix_score
    #else:
    return matrix_score,history_score



def save_max_similarity_cvs():
    # Load dataset
    openpath = "../result/reviews_with_features/polarity_person.csv"
    savepath = "../result/reviews_with_features/reviews_4k_cut_polarity_person_maxsimilarity2.csv"
    
    review = ul.read_csv_file(openpath)
    ul.write_csv_file_w(savepath, ",".join(review.next())+",当前评论相似度,历史评论相似度")#",第一人称,其他人才,人称之差,正向极性,反向极性,正向平均值,反向平均值,正向方差,反向方差,总体极性（正反差）")
    
    ii=1
    for re in review:
        #获取商品评论的最大相似度
        max_similarity = get_max_similarity_alone(int(re[0]),re[15])#评论序号、用户编号
        
        #写到文件中
        newrow = ",".join(re)
        print newrow
        #print str(max_similarity[0])+","+str(max_similarity[1])
        ul.write_csv_file(savepath,newrow+","+str(max_similarity[0])+","+str(max_similarity[1]))
        ii=ii+1



#test()
save_max_similarity_cvs()
#print get_max_similarity_alone(1000,"49923898")
#print get_max_similarity(10,"4992389800")


