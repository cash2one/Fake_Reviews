 
#coding=utf-8
import numpy as np
import xlrd
import jieba
import util.util as ul



    


# 2. 极性计算Sentiment dictionary analysis basic function
# 程度副词Function of matching adverbs of degree and set weights
def match(word, sentiment_value):#匹配词、
    #print "match:",word
    if word in mostdict:#绝对程度
        sentiment_value *= 2.0
        print word,"*2"
    elif word in verydict:#非常程度
        sentiment_value *= 1.5
        print word,"*1.5"
    elif word in moredict:#比较程度
        sentiment_value *= 1.25
        print word,"*1.25"
    elif word in ishdict:#轻微程度+1
        sentiment_value *= 0.5
        print word,"*0.5"
    elif word in insufficientdict:#轻微程度
        sentiment_value *= 0.25
        print word,"*0.25"
    elif word in inversedict:#否定词
        sentiment_value *= -1
        print word,"*-1"
    return sentiment_value

# 极性统一化Function of transforming negative score to positive score
# Example: [5, -2] →  [7, 0]; [-4, 8] →  [0, 12]
def transform_to_positive_num(poscount, negcount):
    pos_count = 0
    neg_count = 0
    if poscount < 0 and negcount >= 0:
        neg_count += negcount - poscount
        pos_count = 0
    elif negcount < 0 and poscount >= 0:
        pos_count = poscount - negcount
        neg_count = 0
    elif poscount < 0 and negcount < 0:
        neg_count = -poscount
        pos_count = -negcount
    else:
        pos_count = poscount
        neg_count = negcount
    return [pos_count, neg_count]

# 3.1 计算单条评论的正反极性Single review's positive and negative score
# 计算每条句子的情感极性、均值、标准差Function of calculating review's every sentence sentiment score
def sumup_sentence_sentiment_score(score_list):
    score_array = np.array(score_list) # Change list to a numpy array
    Pos = np.sum(score_array[:,0]) # 正向极性分数 Compute positive score
    Neg = np.sum(score_array[:,1]) # 反向极性分数
    AvgPos = np.mean(score_array[:,0]) # Compute review positive average score, average score = score/sentence number
    AvgNeg = np.mean(score_array[:,1])
    StdPos = np.std(score_array[:,0]) #标准差 Compute review positive standard deviation score
    StdNeg = np.std(score_array[:,1])#标准差

    return [Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg]

#计算整条评论的情感极性
def single_review_sentiment_score(review):
    single_review_senti_score = [] 
    cuted_review = ul.cut_sentence(review)#对一条评论进行分句["这手机的画面极好"   "操作也比较流畅"  "不过拍照真的太烂了！"    "系统也不好。"]
    for sent in cuted_review:#对于每一句  "这手机的画面极好"
        seg_sent = ul.segmentation(sent, 'list')#对句子进行分词
        i = 0 # 当前词的位置，word position counter
        s = 0 # sentiment word position
        poscount = 0 # count a positive word
        negcount = 0 # count a negative word
        #presentiment=0

        for word in seg_sent:#对于每个词  [0"这" 1"手机" 2"画面" 3"极" 4"好"]
            if word in posdict:#word为正向情感词
                poscount += 1
                print word,'-','posdict','-',poscount
                for w in seg_sent[s:i]:
                   poscount = match(w, poscount)#返回分数
                #a = i + 1
                s = i + 1
                #presentiment = 'pos'

            elif word in negdict:#word为反向情感词
                negcount += 1
                print word,'-','negdict','-',negcount
                for w in seg_sent[s:i]:
                    negcount = match(w, negcount)
                #a = i + 1
                s = i + 1
                #presentiment = 'neg'

            # Match "!" in the review, every "!" has a weight of +2
            elif word == "！".decode('utf8') or word == "!".decode('utf8'):#分句后有"！","!"
                '''
                #for w2 in seg_sent[::-1]:#seg_sent[::-1]为逆序，从后往前，防止多感叹号计算多次
                for w2 in seg_sent[::-1]:
                    if w2 in posdict:
                        poscount += 2
                        break
                    elif w2 in negdict:
                        negcount += 2
                        break
                '''
                if poscount>negcount:
                    poscount += 2
                elif poscount<negcount:
                    negcount += 2
                #presentiment = 'exclamation'
            i += 1

        single_review_senti_score.append(transform_to_positive_num(poscount, negcount))#将每句的正反极性存在single_review_senti_score
        review_sentiment_score = sumup_sentence_sentiment_score(single_review_senti_score)#累加得到总分

    return review_sentiment_score


def calculate_polarity():
   

    ii=0
    #f = open("./results/reviews_polatities.xlsx",'w')
    #f.write('正向极性'+'\t'+'反向极性'+'\t'+'总体极性（正反差）'+'\t'+'正向平均值'+'\t'+'反向平均值'+'\t'+'正向方差'+'\t'+'反向方差'+'\t'+'\n')
     
    for re in review:
        #print type(re[6].decode("utf-8")),re[6].decode("utf-8")
        print '第',ii,'条-',single_review_sentiment_score(re[6].decode("utf-8"))
        #f.write(str(single_review_sentiment_score(re)[0])+'\t'+str(single_review_sentiment_score(re)[1])+'\t'+str(single_review_sentiment_score(re)[0]-single_review_sentiment_score(re)[1])+'\t'+str(single_review_sentiment_score(re)[2])+'\t'+str(single_review_sentiment_score(re)[3])+'\t'+str(single_review_sentiment_score(re)[4])+'\t'+str(single_review_sentiment_score(re)[5])+'\t'+'\n')
        ii=ii+1
    #f.close()


jieba.load_userdict('../dict/others/userdict.txt') #Load user dictionary to increse segmentation accuracy
# 1. 加载词典和数据集
# 加载情感词典
posdict = ul.read_txt_file("../dict/dictionary_of_sentiment/posdict.txt","lines")
negdict = ul.read_txt_file("../dict/dictionary_of_sentiment/negdict.txt","lines")

# 加载长度副词
mostdict = ul.read_txt_file('../dict/adverbs_of_degree_dictionary/most.txt', 'lines')
verydict = ul.read_txt_file('../dict/adverbs_of_degree_dictionary/very.txt', 'lines')
moredict = ul.read_txt_file('../dict/adverbs_of_degree_dictionary/more.txt', 'lines')
ishdict = ul.read_txt_file('../dict/adverbs_of_degree_dictionary/ish.txt', 'lines')
insufficientdict = ul.read_txt_file('../dict/adverbs_of_degree_dictionary/insufficiently.txt', 'lines')
inversedict = ul.read_txt_file('../dict/adverbs_of_degree_dictionary/inverse.txt', 'lines')


# Load dataset
#review = get_excel_data("./data/reviews.xlsx", "1", "1", "data") 
review = ul.read_csv_file("../result/reviewsbypreprocessing/reviews_4k_cut.csv")
review.next()
#calculate_polarity()




# Testing
'''
#print single_review_sentiment_score("手机的画面极好".decode("utf-8"))
#print single_review_sentiment_score("操作也比较流畅".decode("utf-8"))
print single_review_sentiment_score("北京天安门不过拍照真的太烂了！".decode("utf-8"))
#print single_review_sentiment_score("系统也不好。".decode("utf-8"))
#print single_review_sentiment_score("这手机的画面不是很好！！!".decode("utf-8"))
#print single_review_sentiment_score("这手机的画面极好，操作也比较流畅。不过拍照真的太烂了！系统也不好。".decode("utf-8"))
ii=0
for re in review:
    print ii,'-',single_review_sentiment_score(re)
    ii=ii+1
'''
 


'''
print single_review_sentiment_score("总体很烂，出品还不错，不是非常不好，就是服务有点跟不上，服务员都很忙。".decode("utf-8"))

seg_list = jieba.cut("总体好烂，出品都蛮不错，就是服务有点跟不上，服务员都很忙。".decode("utf-8"))
seg_result = ' '.join(seg_list)#以' '作为分隔符，将seg_list所有的元素合并成一个新的字符串
print seg_result
''' 












 