# 利用所学，对如下数据进行文本挖掘，主要实现以下四个方面内容：
# 1. 利用机器学习和文本挖掘技术完成情感分析模型搭建。
# 2. 利用情感极性判断与程度计算来判断情感倾向。
# 3. 利用词频和TF-IDF挖掘出正负文本中的关键点情况。
# 4. 利用文本挖掘相关算法找到平台中用户讨论的集中点。
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



def _discribute(df,to_excel):
    """
    观察值的分布情况
    """
    print(df['星级'].unique())
    print(df['点赞数'].unique())
    print(df['评论回复数'].unique())

    """
    观察评论打分情况
    """
    df_evaluate = df['星级'].reset_index()
    df_evaluate.columns = ['Count', '星级']
    df_evaluate = df_evaluate.groupby("星级").aggregate('count').reset_index()
    df_evaluate.sort_values(by='Count', inplace=True, ascending=True)

    plt.figure(figsize=(8,6))
    plt.pie(df_evaluate['Count'], labels=df_evaluate['星级'], autopct='%1.1f%%',shadow=False, radius=1.2)
    plt.savefig('观察/1 观察评论打分情况.png')
    plt.show()

    """
    处理为4的评分，将4分归为5分。
    处理为2的评分，将2分归为1分。

    为了方便，将5变为1，将1变为0,  将3还是3
    """
    dfAdd = pd.DataFrame(columns=['星级（处理后'])
    dfAdd['星级（处理后）'] = df['星级'].map(lambda x: '好评' if x == 4 or x == 5 else '差评' if x == 1 or x == 2 else '一般')
    df = pd.concat([df, dfAdd], axis=1)
    #####################################################
    df.to_excel(to_excel)

    df_evaluate = dfAdd['星级（处理后）'].reset_index()
    df_evaluate.columns = ['Count', '星级（处理后）']
    df_evaluate = df_evaluate.groupby("星级（处理后）").aggregate('count').reset_index()
    df_evaluate.sort_values(by='Count', inplace=True, ascending=True)

    plt.figure(figsize=(8,6))
    plt.pie(df_evaluate['Count'], labels=df_evaluate['星级（处理后）'], autopct='%1.1f%%',shadow=False, radius=1.2)
    plt.savefig('观察/2 观察评论打分处理情况.png')
    plt.show()

    """
    观察每个商品好评与差评的数量分布
    （一个商品好评、差评最多1000条；一个商品好评>=差评）
    """
    # 将'型号'列变为str，否则histplot无法绘制
    df['型号（处理后）'] = df['型号（处理后）'].apply(str)
    plt.figure(figsize=(40,12))  # 大小 表示figure 的大小为宽、长（单位为inch）
    sns.histplot(data=df, x="型号（处理后）", hue="星级", multiple="dodge", shrink=.8) #multiple="dodge" 多个柱状：躲开
    # 旋转标签90度
    plt.xticks(rotation=20)
    plt.savefig('观察/3 每个型号商品好评与差评的数量分布.png')
    plt.show()

    # 将'大小'列变为str，否则histplot无法绘制
    df['大小（处理后）'] = df['大小（处理后）'].apply(str)
    plt.figure(figsize=(40,12))
    sns.histplot(data=df, x="大小（处理后）", hue="星级", multiple="dodge", shrink=.8) #multiple="dodge" 多个柱状：躲开
    # 旋转标签90度
    plt.xticks(rotation=20)
    plt.savefig('观察/4 每个大小商品好评与差评的数量分布.png')
    plt.show()

    # 将'型号'列变为str，否则histplot无法绘制
    df['型号（处理后）'] = df['型号（处理后）'].apply(str)
    plt.figure(figsize=(40,12))
    sns.histplot(data=df, x="型号（处理后）", hue="星级（处理后）", multiple="dodge", shrink=.8) #multiple="dodge" 多个柱状：躲开
    # 旋转标签90度
    plt.xticks(rotation=20)
    plt.savefig('观察/5 每个型号商品好评与差评的数量分布（星级处理后）.png')
    plt.show()

    # 将'大小'列变为str，否则histplot无法绘制
    df['大小（处理后）'] = df['大小（处理后）'].apply(str)
    plt.figure(figsize=(40,12))
    sns.histplot(data=df, x="大小（处理后）", hue="星级（处理后）", multiple="dodge", shrink=.8) #multiple="dodge" 多个柱状：躲开
    # 旋转标签90度
    plt.xticks(rotation=20)
    plt.savefig('观察/6 每个大小商品好评与差评的数量分布（星级处理后）.png')
    plt.show()

    """
    观察每月的商品数量
    （主要集中在近年）
    """
    # df = pd.read_excel('测试数据集2.xlsx')
    df['发表时间'] = df['发表时间'].fillna('未知-时间-0 0:0') # 填充NaN值

    df['发表时间'] = df['发表时间'].map(lambda x: str(x).split('-')[0][-2:] + str(x).split('-')[1])
    df_time = df['发表时间'].reset_index()
    df_time.columns = ['Count', '发表时间']
    df_time = df_time.groupby('发表时间').aggregate('count').reset_index()
    df['发表时间'] = df['发表时间'].apply(str)
    df_time.sort_values(by='发表时间', inplace=True, ascending=True)

    plt.figure(figsize=(40,30))
    sns.lineplot(data=df_time, x='发表时间', y='Count')
    plt.ylabel("数量")
    plt.savefig('观察/7 每月的商品数量情况.png')
    plt.show()

    """
    观察评论长度分布
    （这张图与下一张图结合，可以更好的了解长度的分布）
    """
    length = pd.DataFrame(columns=['length'])
    for index, row in df.iterrows():
        length.loc[index] = len(row['评论内容'])

    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=length, x=range(length.shape[0]), y=np.sort(length['length']))
    plt.xlabel('index')
    plt.ylabel('length')
    plt.savefig('观察/8 长度分布情况（散点图）.png')
    plt.show()

    """
    观察评论长度大小分布情况
    （可以继续查看一下大于200的数量，和小于10的数量）
    """
    plt.figure(figsize=(8, 6))
    sns.histplot(data=length, x="length", bins=70)
    plt.savefig('观察/9 长度分布情况（柱状图）.png')
    plt.show()

def _slove(df,to_excel):
    """
    删除重复值
    """
    df = df.drop_duplicates(subset='评论内容', keep='first')
    # df  # rows:67003->64422->63628

    """ 
    删除标点符号或英文字母过多的评论
    """
    count = []
    for index, row in df.iterrows():
        other = 0
        chinese = 0
        for i in row['评论内容']:
            if '\u4e00' <= i <= '\u9fa5':
                chinese += 1
            else:
                other += 1
        if chinese < other:
            count.append(index)
    for i in count:
        df = df.drop(i)

    """
    处理HTML符号
    """
    df['评论内容'] = df['评论内容'].str.replace('&hellip', '')  # 直接replace只能替换整体相同的，局部的话加str
    df['评论内容'] = df['评论内容'].str.replace('&quot', '')
    df['评论内容'] = df['评论内容'].str.replace('&ldquo', '')
    df['评论内容'] = df['评论内容'].str.replace('&rdquo', '')
    df['评论内容'] = df['评论内容'].str.replace('\n', '')
    df['评论内容'] = df['评论内容'].str.replace(' ', '')

    """
    处理*（可能是违禁语、价格、品牌）
    好评：差评=1:2，应该保留。但每个*的数量还不一样，为了避免jieba分出来多个，将每个出现*的都变为1个*
    """
    df_temp = df[df['评论内容'].str.contains('\*')][['评论内容', '星级']]
    print(len(df_temp[df_temp['星级'] == 1]))
    print(len(df_temp[df_temp['星级'] == 0]))
    regex = re.compile('[*]+')
    df['评论内容'] = df['评论内容'].str.replace(regex, '*')

    """
    将“京东”、“电脑”字样去除（所有商品都是电脑，都来自于京东）
    """
    info = re.compile('[0-9a-zA-Z]|京东|电脑|')
    df['评论内容'] = df['评论内容'].map(lambda x: info.sub('', x))

    '''
    根据京东评论的实际情况，剔除以下无效内容：
    # 运行速度：
    # 屏幕效果：
    # 散热性能：
    # 轻薄程度：
    # 外形外观：
    # 其他特色：
    # 此用户未填写评价内容
    '''
    info = re.compile('[0-9a-zA-Z]|运行速度：|屏幕效果：|散热性能：|轻薄程度：|外形外观：|其他特色：|此用户未填写评价内容|')
    df['评论内容'] = df['评论内容'].map(lambda x: info.sub('', x))

    """
    处理过长过短的评论
    >400：可能随便复制的
    <10：太短没意义
    """
    # print(len(df[df['评论内容'].str.len() > 400]))
    # print(len(df[df['评论内容'].str.len() < 10]))
    df = df.drop(df[df['评论内容'].str.len() < 10].index)
    df = df.drop(df[df['评论内容'].str.len() > 400].index)
    # rows:67003->64422

    '''
    删除缺失值，评论内容和星级为空的评论，可删
    '''
    # df['评论内容'] = df['评论内容'].dropna() # 这种删法，不太行，虽然删除了，但是保存后后还是原表
    # df['星级'] = df['星级'].dropna()
    df = df.drop(df[df['评论内容'].isnull()].index)
    df = df.drop(df[df['星级'].isnull()].index)

    df.to_excel(to_excel)

if __name__ == '__main__':
    """
    获得数据，选择函数
    """
    df = pd.read_excel('数据/2 完整数据集（型号处理后）.xlsx',index_col=0)
    _discribute(df, to_excel='数据/3 完整数据集（型号星级处理后）.xlsx')

    df = pd.read_excel('数据/3 完整数据集（型号星级处理后）.xlsx',index_col=0)
    _slove(df, to_excel='数据/4 完整数据集（删除无效数据后）.xlsx')



























