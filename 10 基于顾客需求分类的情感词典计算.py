import jieba
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
import math
import re

'''定义函数，统计情感词前面否定词个数是偶数还是奇数, even代表偶数，odd代表奇数'''
def judgeodd(num):
    if int(num / 2) * 2 == num:
        return 'even'
    else:
        return 'odd'

'''把负面词典放入列表'''
negativewords = open(r'工具\情感词典\Negative1.txt', 'r', encoding='utf-8')
neglst = []
for line1 in negativewords:
    neglst.append(line1.strip())
'''把正面词典放入列表'''
positivewords = open(r'工具\情感词典\positive.txt', 'r', encoding='utf-8')
poslst = []
for line2 in positivewords:
    poslst.append(line2.strip())

'''打开程度词词典'''
mostdict = open(r'工具\情感词典\mostdict.txt', 'r', encoding='utf-8')
verydict = open(r'工具\情感词典\verydict.txt', 'r', encoding='utf-8')
moredict = open(r'工具\情感词典\moredict.txt', 'r', encoding='utf-8')
ishdict = open(r'工具\情感词典\ishdict.txt', 'r', encoding='utf-8')
insufficientdict = open(r'工具\情感词典\insufficientdict.txt', 'r', encoding='utf-8')
overdict = open(r'工具\情感词典\overdict.txt', 'r', encoding='utf-8')


def main(dfData, to_excel):
    dfAdd = pd.DataFrame(columns=("pos", "neg"))

    for index, row in dfData.iterrows():
        # customer_demand = list(str(dfData.loc[index, '对应顾客需求']).split(' '))
        production_sentence = str(dfData.loc[index, '对应评论句子'])
        '''计算每一条新闻/评论的情感值'''
        seg = []
        '''jieba分词的三种模式：
        1.全模式：将可以成词的词语都扫描出来，但是不解决歧义       cut_all=True
        2.精确模式：将所有句子精确地分开      cut_all=False
        3.搜索引擎模式：在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词。
        '''
        jieba.load_userdict(r"数据\8 词频统计.txt") # 自定义词典
        seg2 = jieba.cut(production_sentence, cut_all=True)
        for item in seg2:
            seg.append(item.strip())    #把切词结果放入列表seg
        i = 0  # 记录扫描到的词的位置
        preswpos = 0  # 记录上一个情感词的位置
        swpos = 0  # 记录当前情感词的位置
        weight = 0  # 程度词权重
        currentposgrade = 0  # 当前正面情感词分值
        currentneggrade = 0  # 当前负面情感词分值
        totalpos = 0   # 积极词的总分值
        totalneg = 0   # 负面词的总分值
        c = 0          # 记录否定词个数
        # print(seg)
        for item in seg:  # 扫描分词列表中的每一行,其位置由i来记录
            if (item in poslst) or (item in neglst):
                swpos = seg.index(item)  # 当前情感词位置
                if item in poslst:
                    currentposgrade = 1
                    for w in seg[preswpos:swpos]:  # 扫描上一个情感词和当前情感词之间的程度词,for循环用来计算程度词权重
                        if w in mostdict:
                            weight += 3.0
                        elif w in verydict:
                            weight += 2.5
                        elif w in moredict:
                            weight += 2.0
                        elif w in overdict:
                            weight += 1.5
                        elif w in insufficientdict:
                            weight += 0.5
                        elif w in ishdict:
                            c += 1
                        else:
                            weight = 1
                    currentposgrade *= weight  # 当前情感词分值
                    totalpos += currentposgrade
                    if judgeodd(c) == 'odd':  # 扫描情感词前的否定词数
                        currentposgrade *= -1  # 当前正面的情感词变为负面情感
                        totalneg += currentposgrade
                if item in neglst:
                    currentneggrade = -1
                    for w in seg[preswpos:swpos]:  # 扫描上一个情感词和当前情感词之间的程度词,for循环用来计算程度词权重
                        if w in mostdict:
                            weight += 3.0
                        elif w in verydict:
                            weight += 2.5
                        elif w in moredict:
                            weight += 2.0
                        elif w in overdict :
                            weight += 1.5
                        elif w in insufficientdict:
                            weight += 0.5
                        elif w in ishdict:
                            c += 1
                        else:
                            weight = 1
                    currentneggrade *= weight  # 当前情感词分值
                    totalneg += currentneggrade
                    if judgeodd(c) == 'odd':  # 扫描情感词前的否定词数
                        currentneggrade *= -1.0  # 当前正面的情感词变为负面情感
                        totalpos += currentneggrade
                preswpos = i + 1  # 上一个情感词位置
            i += 1
        dataAdd = pd.Series({"pos": totalpos, "neg": totalneg})
        print(dataAdd)
        dfAdd = dfAdd.append(dataAdd, ignore_index=True)

        print(index)
        # break

    dfResult = pd.concat([dfData, dfAdd], axis=1)
    dfResult.to_excel(to_excel)

if __name__ == '__main__':
    # dfData = pd.read_excel('数据/16 顾客需求分类2.xlsx',index_col=0)
    # main(dfData, to_excel='数据/17 顾客需求分类2情感预测.xlsx')

    # dfData = pd.read_excel('数据/16 顾客需求分类4.xlsx',index_col=0)
    # main(dfData, to_excel='数据/17 顾客需求分类2情感预测3.xlsx')

    dfData = pd.read_excel('数据/16 顾客需求分类4.2.xlsx',index_col=0)
    dfData.reset_index(drop=True, inplace=True) # 更新重置索引
    main(dfData, to_excel='数据/17 顾客需求分类2情感预测3.2.xlsx')






