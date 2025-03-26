# 利用情感极性判断与程度计算来判断情感倾向。
"""
导入包
"""
# 数据处理
import pandas as pd

'''本部分中使用情感词典进行情感分析的思路为：
1. 对文档分词，找出文档中的情感词、否定词以及程度副词
2. 然后判断每个情感词之前是否有否定词及程度副词，将它之前的否定词和程度副词划分为一个组
3. 如果有否定词将情感词的情感权值乘以-1，如果有程度副词就乘以程度副词的程度值
4. 最后所有组的得分加起来，大于0的归于正向，小于0的归于负向。(得分的绝对值大小反映了积极或消极的程度)'''

"""
读取否定词文件和程度副词
"""
negation = pd.read_csv('工具/否定词.txt', header=None, sep='\n', encoding='utf-8')
adv = pd.read_csv('工具/程度副词X.txt', header=None, sep='\,', encoding='utf-8')
emotion = pd.read_csv('工具/BosonNLP_sentiment_score.txt', header=None, sep=' ', encoding='utf-8')

"""
分别变成list与dict
"""
negation_list = negation[0].tolist()         ######
adv1 = adv[0].tolist()
adv2 = adv[1].tolist()
adv_dict = dict(zip(adv1, adv2))              ######
emotion1 = emotion[0].tolist()
emotion2 = emotion[1].tolist()
emotion_dict = dict(zip(emotion1, emotion2))  ######

"""
根据情感词计算情感分数
"""
def score_sentiment(negation_list, adv_dict, emotion_dict, words):
    word_list =  words.split(' ')
    score = 0
    W = 1
    flag = False
    for i in range(len(word_list)):
        if flag == True:
            W = 1
        if word_list[i] in negation_list:
            flag = False
            W = -1 * W
        elif word_list[i] in adv_dict:
            flag = False
            W = W * adv_dict.get(word_list[i])
        elif word_list[i] in emotion_dict:
            flag = True
            score += W * emotion_dict.get(word_list[i])
    return score

"""
计算正确率函数
"""
def calculate_accuracy(df):
    right = 0
    for index, row in df.iterrows():
        if df['情感词典预测可信度'].iloc[index] == '可信':
            right += 1
        if df['情感词典预测可信度'].iloc[index] == '待考量':
            right += 0.5
    sol = '预测可信数量：' + str(right) + '\n' + '评论总数量：' + str(len(df)) + '\n' + '预测可信度：' + str(right / len(df) * 100) + '%'
    return sol

def main(df, to_excel):
    df['情感词典预测'] = ''
    df['情感词典预测分数'] = ''
    df['情感词典预测可信度'] = ''

    for i in range(len(df)):
        score = score_sentiment(negation_list, adv_dict, emotion_dict, df['分词后'].iloc[i])
        df['情感词典预测分数'].iloc[i] = score
        if score > 5:
            df['情感词典预测'].iloc[i] = '积极'
        elif 5 >= score > 0:
            df['情感词典预测'].iloc[i] = '中性'
        else:
            df['情感词典预测'].iloc[i] = '消极'

        if (df['星级（处理后）'].iloc[i] == '好评' and score > 5) or (df['星级（处理后）'].iloc[i] == '差评' and score <= 0)  \
                or (df['星级（处理后）'].iloc[i] == '一般' and -7 < score <= 10):
            df['情感词典预测可信度'].iloc[i] = '可信'
        elif df['星级（处理后）'].iloc[i] == '一般' and (20 > score > 10 or -10 < score < -7)\
                or (3 <= score <= 5 and df['星级（处理后）'].iloc[i] == '好评')\
                or (0 < score <= 5 and df['星级（处理后）'].iloc[i] == '差评'):
            df['情感词典预测可信度'].iloc[i] = '待考量'
        else:
            df['情感词典预测可信度'].iloc[i] = '不可信'

    df.to_excel(to_excel)

    """
    计算正确率
    """
    f = open('数据/7 情感词典预测正确率.txt','w', encoding='utf-8')
    f.write('情感词典预测正确率：'+ str(calculate_accuracy(df)))
    f.close()
    print('情感词典预测正确率：', calculate_accuracy(df))

if __name__ == '__main__':
    ## 获取数据
    dfData = pd.read_excel('数据/6 完整数据集（句子产品特征词性统计后）.xlsx', index_col=0)  # 6 完整数据集（句子产品特征词性统计后）

    main(dfData, to_excel='数据/7 完整数据集（情感词典预测）.xlsx')












