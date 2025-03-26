# -*- coding:utf-8 -*-
import pymysql
import pandas as pd
import re
import math
import openpyxl
# 分词
import jieba
import jieba.analyse
# 词性识别
import jieba.posseg as posseg


def fenci(text):
    """
    分词函数
    """
    # 保留中文、英文（jieba不会把英文单词分开）、*
    #     cut_word = [i for i in list(jieba.cut(text)) if '\u4e00' <= i <= '\u9fff']
    # 只会比词的第一个（注意这里“\u0039”必须4个数，不够用0补）
    # print(list(jieba.cut(text)))
    cut_word = [i for i in list(jieba.cut(str(text))) if
                '\u4e00' <= i <= '\u9fff' or '\u0030' <= i <= '\u0039' or '\u0061' <= i <= '\u007a' or '\u0041' <= i <= '\u005a' or i == '\u002A']
    text = ' '.join(cut_word)
    return text

def Identify_property(text):
    """
    jieba.posseg词性识别函数
    """
    cut_word = [(x.word, x.flag) for x in posseg.cut(str(text))]
    return cut_word

def jie_ba(df,to_excel):
    """
    jieba分词
    """
    df = df.reset_index(drop=True)
    df['分词后'] = ''
    df['分词后有效字数'] = ''

    for i in range(len(df)):
        df['分词后'].iloc[i] = fenci(df['评论内容'].iloc[i])
    """
    获得停用词
    """
    negation = pd.read_csv('工具/否定词.txt', header=None, sep='\n', encoding='utf-8')
    negation_list = negation[0].tolist()
    stopwords = [i.strip() for i in open('工具/stoplist.txt', 'r', encoding='utf-8').readlines()]
    stopwords = [i for i in stopwords if i not in negation_list]
    """
    根据停用词处理分词结果
    """
    for index, row in df.iterrows():
        str_ = ''
        list_ = row['分词后'].split(' ')
        for i in list_:
            if i not in stopwords:
                str_ += i
                str_ += ' '
        str_ = str_.rstrip()
        # 注意只有这样写才能替换df里对应的值
        df.loc[index, '分词后'] = str_
        df.loc[index, '分词后有效字数'] = len(re.findall(r'[\u4E00-\u9FFF]', str_))

    """
    词性识别
    """
    df['词性'] = ''
    for i in range(len(df)):
        df['词性'].iloc[i] = Identify_property(df['评论内容'].iloc[i])
    """
    根据停用词处理词性结果
    """
    # 必须转一下，要不然放不了list
    df['词性'] = df['词性'].astype('object')
    for index, row in df.iterrows():
        list_ = []
        for i in row['词性']:
            if i[0] not in stopwords:
                list_.append(i)
        # df.loc不能放list只能放str，因为它认为list长度不为一，所以不对应。set_value也被淘汰了，用at
        #     df.loc[index, '词性'] = list_
        #     df.set_value(index, '词性', list_)
        df.at[index, '词性'] = list_

    '''
    删除缺失值, 为了避免删除停用词后，评论出现NaN值，在分词后一列再进行一次删除缺失值
    '''
    # df['分词后'] = df['分词后'].dropna() # 这种删法，不太行，虽然删除了，但是保存后后还是原表
    df = df.drop(df[df['分词后'].isnull()].index)

    df['分词后有效字数'] = df['分词后有效字数'].astype(str)  # 更改类型为str
    # 原列df['分词后'] 的type为 object。但是 df['分词后有效字数']的type为int64 --> 不能作为str处理
    df = df.drop(df[df['分词后有效字数'].str.contains('0') == True].index)  # str包含‘0’，删除，出错在于10,20等也会被删掉
    df = df.drop(df[df['分词后有效字数'] == '0'].index)

    df.to_excel(to_excel)

def cut_sent(para):
    para = re.sub('([。！？\?])([^”])',r"\1\n\2",para) # 单字符断句符
    para = re.sub('(\.{6})([^”])',r"\1\n\2",para) # 英文省略号
    para = re.sub('(\..{2})([^”])',r"\1\n\2",para) # 中文省略号
    para = re.sub('(”)','”\n',para)   # 把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()       # 段尾如果有多余的\n就去掉它
    #很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")

def productFeature():
    df = pd.read_excel('工具/Dictionary/电脑产品特征词.xlsx')  # ,index_col=0
    dict_word = {}
    for d in range(len(df['顾客需求'])):
        customer_demand = df['顾客需求'][d]
        print(customer_demand)
        feature_word = str(df['特征词'][d]).split(' ')
        print(feature_word)
        if '' in feature_word:
            feature_word.remove('')
        dict_word.update({customer_demand: feature_word})

    otherProductList = []
    with open('工具/Dictionary/其他电脑产品（不含华为）.txt', 'r') as f:
        for line in f:
            otherProductList.append(list(line.strip('\n').split(',')))
    while [''] in otherProductList:
        otherProductList.remove([''])
    return dict_word,otherProductList

def dosegment(sentence):
    # print(sentence)
    sentence = str(sentence)
    sentence_seged = posseg.cut(sentence.strip())
    outstr = ''
    for x in sentence_seged:
        outstr+="{}/{},".format(x.word,x.flag)
    return outstr

def senSubObj(rowData):
    # 打开词典文件，返回列表
    senSubObjReturn = 0

    def open_dict(Dict, path):
        dictionary = open(path, 'r', encoding='utf-8')
        dict = []
        for word in dictionary:
            word = word.strip('\n')
            dict.append(word)
        return dict
    posdict = open_dict(Dict='positive', path=r'工具/Dictionary/positive.txt')
    negdict = open_dict(Dict='negative', path=r'工具/Dictionary/negative.txt')
    segtmp = jieba.lcut(rowData, cut_all=False)  # 把句子进行分词，以列表的形式返回
    for word in segtmp:
        # print(word)
        # print("\n")
        if word in posdict or word in negdict:  # 判断词语是否是情感词
            senSubObjReturn = senSubObjReturn + 1
        #     break
        # else:
        #     senSubObjReturn = 0
    return senSubObjReturn


def main(dfData, df_Feature, otherProductList, to_excel):
    dfAdd = pd.DataFrame(columns=("字数","形容词数", "动词数",

                                  "产品特征数", "含有产品特征词",
                                  "顾客需求数(去重）", "所属顾客需求",
                                  "其他产品数",'提到其他产品',

                                  "分句", "句子数", "句子平均长度", "主观句子数", "客观句子数",
                                  "提到产品特征的句子数", '提到产品特征的句子',
                                  "产品特征数/提到产品特征的句子数", "提到产品特征数/句子数", "提到产品特征句子数/句子数"))  # 创建一个空的dataframe

    for index, row in dfData.iterrows():
        rowData = str(dfData.loc[index, '评论内容'])
        fenci_rowData = str(dfData.loc[index, '分词后'])
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@', fenci_rowData)

        # 去掉空格空行
        rowData = str(rowData)
        rowData.strip()
        rowData = list(re.split('[ \n]', rowData))  # 先分割输入字串，并生成列表
        rowData = ''.join(rowData)  # 把列表内容合并起来，生成新的字串

        words_num = len(re.findall(r'[\u4E00-\u9FFF]', rowData))  # 字数
        sentence_statu = cut_sent(rowData)
        sentence_num = len(cut_sent(rowData))  # 句子数

        tagCount = dosegment(fenci_rowData)  # 词性统计要用分词后的数据列
        # print(tagCount)
        adj_num = tagCount.count("/a")  # 形容词数
        verb_num = tagCount.count("/v")  # 动词数

        product_word = str(fenci_rowData).split(' ')
        if '' in product_word:
            product_word.remove('')

        productNum = 0
        customer_demand_Num = 0
        otherProductNum = 0
        productSentenceNum = 0
        subSenNum = 0
        objSenNum = 0
        productNum_productSentenceNum = 0
        product_word_Add = '' # "含有产品特征词"
        customer_demand_Add = '' # "所属顾客需求"
        otherProduct = ''
        sentence_list = []

        for i in range(len(product_word)):  # 对每一行中的评论内容的每一个分词进行处理
            for d in range(len(df_Feature['顾客需求'])):
                customer_demand = df_Feature['顾客需求'][d]
                # print(customer_demand)
                feature_word = str(df_Feature['特征词'][d]).split(' ')
                # print(feature_word)
                if '' in feature_word:
                    feature_word.remove('')

                if product_word[i] in feature_word:
                    product_word_Add = product_word_Add + ' ' + str(product_word[i])
                    customer_demand_Add = customer_demand_Add + ' ' + str(customer_demand)
                    productNum = productNum + 1  # 特征词数

                if product_word[i] in otherProductList:  # 其他产品数统计
                    otherProductNum = otherProductNum + 1  # 其他产品数
                    otherProduct= otherProduct + ' ' + str(product_word[i])

        # print(sentence_statu)
        product_word_Add_list = product_word_Add.split()
        for sentence in sentence_statu:
            for p in product_word_Add_list:
                # print(sentence)
                if p in sentence:
                    productSentenceNum = productSentenceNum + 1  # 提到产品特征的句子数
                    sentence_list.append(sentence)
                    break

        for sentence in sentence_statu:
            if senSubObj(sentence) > 0:
                subSenNum = 1 + subSenNum  # 主观句子数
        objSenNum = sentence_num - subSenNum  # 客观句子数

        if productSentenceNum != 0:
            productNum_productSentenceNum = productNum / productSentenceNum

        customer_demand_Num = len(set(customer_demand_Add.split()))
        dataAdd = pd.Series(
            { "字数": words_num,"形容词数": adj_num, "动词数": verb_num,
              "产品特征数": productNum, "含有产品特征词": product_word_Add,
              "顾客需求数(去重）": customer_demand_Num, "所属顾客需求": customer_demand_Add,
              "其他产品数": otherProductNum,'提到其他产品': otherProduct,

              "分句": sentence_statu, "句子数": sentence_num, "句子平均长度": words_num / sentence_num,
              "主观句子数": subSenNum, "客观句子数": objSenNum,

              "提到产品特征的句子数": productSentenceNum, '提到产品特征的句子': sentence_list,
              "产品特征数/提到产品特征的句子数": productNum_productSentenceNum,
              "提到产品特征数/句子数": productNum / sentence_num,
              "提到产品特征句子数/句子数": productSentenceNum / sentence_num
             } )
                                # "分句", "句子数", "句子平均长度", "主观句子数", "客观句子数",
                                  # "提到产品特征的句子数", '提到产品特征的句子'
                                  # "产品特征数/提到产品特征的句子数", "提到产品特征数/句子数", "提到产品特征句子数/句子数"))

        dfAdd = dfAdd.append(dataAdd, ignore_index=True)

    dfResult = pd.concat([dfData, dfAdd], axis=1)
    dfResult.to_excel(to_excel)


if __name__ == '__main__':
    # 获取数据
    # dfData = pd.read_excel('数据/4 完整数据集（删除无效数据后）.xlsx',index_col=0)  # 测试数据集2
    #
    # jie_ba(dfData, to_excel='数据/5 完整数据集（分词删除停用词词性标注后）.xlsx')

    # dfData2 = pd.read_excel('数据/测试.xlsx',index_col=0)
    dfData2 = pd.read_excel('数据/5 完整数据集（分词删除停用词词性标注后）.xlsx',index_col=0)
    # 不更新索引，main()函数会把删去的无效值，空缺索引补上空行，导致index出错。
    # 更新索引，法一：df2.index = range(len(df2))
    dfData2 = dfData2.reset_index(drop=True) # drop=True表示删除原索引，不然会在数据表格中新生成一列'index'数据

    df_Feature = pd.read_excel('工具/Dictionary/电脑产品特征词.xlsx')

    otherProductList = []
    with open('工具/Dictionary/其他电脑产品（不含华为）.txt', 'r') as f:
        for line in f:
            otherProductList.append(list(line.strip('\n').split(',')))
    while [''] in otherProductList:
        otherProductList.remove([''])

    main(dfData2, df_Feature, otherProductList, to_excel="数据/6 完整数据集（句子产品特征词性统计后）(新）.xlsx")

