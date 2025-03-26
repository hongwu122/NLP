# 利用词频和TF-IDF挖掘出正负文本中的关键点情况
"""
导入各种包
"""
# 分词
import jieba
# 词性识别
import jieba.posseg as pseg
# 数据处理
import pandas as pd
# 数学计算
import numpy as np
# 读取系统文件
import os
# 用来关闭警告
import warnings
# 画图
from matplotlib import pyplot as plt
# 基于matplotlib更便捷的画图
import seaborn as sns
# 为了图片可以使用中文
from pylab import *
# 来画云词图
from wordcloud import WordCloud
# from PIL import Image #导入模块PIL(Python Imaging Library)图像处理库
# 正则表达式
import re

#不显示警告
warnings.filterwarnings("ignore")

# sns.set_context("talk", font_scale=0.5, rc={"lines.linewidth":4})
# 设置字体
sns.set(font_scale=1.2)
# 设置线条
sns.set(rc={"lines.linewidth":1})
# 设置风格
sns.set_style("whitegrid")
# 设置中文
mpl.rcParams['font.sans-serif'] = u'SimHei'
plt.rcParams['axes.unicode_minus'] = False

"""
利用Tf-idf将文字转为有权重的特征值
"""
from sklearn.feature_extraction.text import TfidfVectorizer
'''
TF-IDF(term frequency-inverse document frequency)词频-逆向文件频率。
在处理文本时，如何将文字转化为模型可以处理的向量呢？TF-IDF就是这个问题的解决方案之一。
字词的重要性与其在文本中出现的频率成正比(TF)，与其在语料库中出现的频率成反比(IDF)。
TF：词频。TF(w)=(词w在文档中出现的次数)/(文档的总词数)
IDF：逆向文件频率。有些词可能在文本中频繁出现，但并不重要，也即信息量小，如is,of,that这些单词，这些单词在语料库中出现的频率也非常大，
我们就可以利用这点，降低其权重。IDF(w)=log_e(语料库的总文档数)/(语料库中词w出现的文档数)
'''
# TfidfVectorizer = CountVectorizer + TfidfTransformer()
# tv_pos_transfer = TfidfVectorizer()
# tv_pos_data = tv_pos_transfer.fit_transform(list(pos['分词后']))
# tv_neg_transfer = TfidfVectorizer()
# tv_neg_data = tv_neg_transfer.fit_transform(list(neg['分词后']))
# tv_zho_transfer = TfidfVectorizer()
# tv_zho_data = tv_zho_transfer.fit_transform(list(zhongli['分词后']))

"""
计算共现的次数函数
"""
def document(words):
    edge_dict = {}
    for w in words:
        ws = w.split(' ')
        for i in range(len(ws)):
            now_w = ws[i]
            # 取出其其它词
            ws_s = ws[i:]
            for w_s in ws_s:
                a, b = now_w, w_s
                # 如果词相同
                if a == b:
                    continue
                # 转化下两个词的顺序
                if a > b:
                    a, b = b, a
                # 生成边
                key = a + ',' + b
                # 统计词频
                if key not in edge_dict:
                    edge_dict[key] = 1
                else:
                    edge_dict[key] += 1
    # 转化为dataframe
    df = pd.DataFrame([edge_dict]).T.reset_index()
    df.columns = ['label', 'weight']
    df = df.sort_values(by='weight', ascending=False)
    # 拆分
    df['source'] = df['label'].map(lambda x: x.split(',')[0])
    df['target'] = df['label'].map(lambda x: x.split(',')[1])
    return df

"""
利用共现矩阵查看具体一个词说了什么，大约1200-300，重要性高的词调高end
"""
def find_detail(word, start, end, df):
    x_df = df[df['weight'].map(lambda x: x < end and x > start)]
    for index, row in x_df.iterrows():
        if word == row['source']:
            print(x_df.loc[index]['target'])
        if word == row['target']:
            print(x_df.loc[index]['source'])

def ciyun(pos, png):
    # 本部分用于制作词云图
    """
    查看每个特征的情况
    """

    tv_pos_transfer = TfidfVectorizer()
    tv_pos_data = tv_pos_transfer.fit_transform(list(pos['分词后']))
    # 获得横坐标
    sorted_pos = sorted(tv_pos_transfer.vocabulary_.items(), key=lambda x: x[1])  # .items()可以遍历将{,,,,}变为[(,),(,)]
    # 变成dataframe
    sorted_pos = [i[0] for i in sorted_pos]

    df_pos = pd.DataFrame(tv_pos_data.toarray(), columns=sorted_pos)

    """
    根据权重排名，取出权重比较大的特征
    """
    pos_res = df_pos.mean().sort_values(ascending=False)
    print('权重排名前五十:', pos_res[:50])

    """
    绘制云词图
    """
    # from wordcloud import WordCloud
    plt.figure(figsize=(20, 9))
    wordcloud = WordCloud(font_path="工具/msyh.ttf", background_color='white', width=2800,
                          height=1200, max_words=300, max_font_size=180).generate_from_frequencies(pos_res)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.savefig(png)
    plt.show()


if __name__ == '__main__':
    ######################################################################
    df = pd.read_excel('数据/7 完整数据集（情感词典预测）.xlsx')

    pos = df[df['星级（处理后）'] == '好评']
    # pos.append(df[df['星级（处理后）'] == 4])
    neg = df[df['星级（处理后）'] == '差评']
    # neg.append(df[df['星级（处理后）'] == 2])
    zhongli = df[df['星级（处理后）'] == '一般']

    '''
    制作词云图
    '''
    ciyun(pos=pos, png='观察/10 好评主题词云图.png')
    ciyun(pos=neg, png='观察/11 差评主题词云图.png')
    ciyun(pos=zhongli, png='观察/12 中评主题词云图.png')

    """
    生成共现矩阵
    """
    pos_df = document(list(pos['分词后']))
    neg_df = document(list(neg['分词后']))
    zho_df = document(list(zhongli['分词后']))

    pos_df.to_excel('数据/pos_df.xlsx')
    neg_df.to_excel('数据/neg_df.xlsx')
    zho_df.to_excel('数据/zho_df.xlsx')

    """
    查看共现情况
    """
    find_detail('速度', 400, 1000, pos_df)
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    find_detail('降价', 100, 500, neg_df)
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    find_detail('客服', 100, 500, zho_df)






