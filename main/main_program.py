#coding=utf-8
'''
Created on 2016年7月22日

@author: hadoop
'''
import util.util as ul
import preprocessing.preprocessing as pp
import similarity.reviews_similarity as rs
import get_features.get_polarity_person as gpp

#1.根据某店评论获取该店评论所有用户编号
pp.gen_userid("../data/food_reviews/reviews_4k.csv","../result/userid/user_id.csv")
#2.对商品评论进行分词-去停止词，写入新的csv【用于相似度计算】
pp.cut_review_to_csv("../data/food_reviews/reviews_4k.csv","../result/reviewsbypreprocessing/reviews_4k_cut.csv")

#3.对用户历史评论进行分词-去停止词，写入新的csv【用于相似度计算】（30w）已省略
###pp.cut_review_to_csv("../data/personal_reviews/all_reviews_sort_30w.csv","../result/reviewsbypreprocessing/all_reviews_30w_cut.csv")
#4.按用户将历史评论切分
pp.split_reviews_by_user("../data/personal_reviews/all_reviews_sort_30w.csv","../data/userid/userid_sort.csv")


#5.相似度计算
#  相似度矩阵
#rs.similarity_toMatrix("../result/reviewsbypreprocessing/reviews_4k_cut.csv","../result/reviewsbypreprocessing/reviews_4k_cut.csv","../result/reviews_similarity/similarity_matrix2.csv")
#  相似度文件


#6.极性计算&人称统计->保存到新的csv中【新增9维特征】
gpp.save_polarity_person_cvs()

#7.读取相似性矩阵最大值->保存到新的csv中



