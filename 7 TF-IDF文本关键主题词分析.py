# 利用文本挖掘相关算法找到平台中用户讨论的集中点
"""
积极、消极、中立评论主题分析
"""
# TF-IDF(term frequency-inverse document frequency)词频-逆向文件频率。
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from collections import Counter
# 数据处理
import pandas as pd
# 数学计算
import numpy as np
# 画图
from matplotlib import pyplot as plt
# 用来关闭警告
import warnings

#不显示警告
warnings.filterwarnings("ignore")

# 基于matplotlib更便捷的画图
import seaborn as sns
# 为了图片可以使用中文
from pylab import *
# sns.set_context("talk", font_scale=0.5, rc={"lines.linewidth":4})
# 设置字体
sns.set(font_scale=1.2)
# 设置线条
sns.set(rc={"lines.linewidth":1})
# 设置风格
sns.set_style("whitegrid")
# 设置中文
mpl.rcParams['font.sans-serif'] = u'SimHei' # mpl基于pylab
plt.rcParams['axes.unicode_minus'] = False

'''
使用sklearn中的TruncatedSVD进行文本主题分析
通过主题分析，我们可以得到一个语料中的关键主题，即各个词语在主题中的重要程度，各个文章在各个主题上的倾向程度。
并且可以根据它们，得到主题对应的关键词以及代表性文本。

TruncatedSVD 用于计算大矩阵 X 的前 K 个奇异值和向量。 
当 n_components 较小时，速度要快得多，例如在使用 3 个分量进行 3D 可视化时使用 PCA。 
cuML 的 TruncatedSVD 是一个 array-like 对象或 cuDF DataFrame，并提供 2 种算法 Full 和 Jacobi。

奇异值分解（SVD）可能是最著名和使用最广泛的矩阵分解方法。
特征分解（eigendecomposition）
'''
def main(pos, png, f):
    tv_pos_transfer = TfidfVectorizer()
    tv_pos_data = tv_pos_transfer.fit_transform(list(pos['分词后']))

    tsvd = TruncatedSVD(n_components=5, algorithm='randomized', n_iter=100, random_state=1)
    pos_topics = tsvd.fit_transform(tv_pos_data)
    print(pos_topics)

    """
    取出主题词
    """
    terms = tv_pos_transfer.get_feature_names()
    for i in range(5):
        # 取出当前主题词的权重
        weight = tsvd.components_[i]
        # 转化下字典
        dz = dict(zip(terms, weight))
        # 进行排序
        dz_s = sorted(dz.items(), key=lambda x: x[1], reverse=True)[:10]
        # 打印结果
        print('主题' + str(i+1) + ':' + ' '.join(d[0] for d in dz_s))
        f.write('主题' + str(i+1) + ':' + ' '.join(d[0] for d in dz_s) + '\n')

    """
    查看分组情况
    """
    # 取出每一列的最大数对应的主题
    res_pos = np.argmax(pos_topics, axis=1)
    arr = Counter(res_pos)      # print(arr) # Counter({0: 809, 3: 86, 2: 84, 4: 69, 1: 2})
    dict_size = dict(arr)       # print(dict(arr)) # {0: 809, 3: 86, 2: 84, 4: 69, 1: 2}
    # collections模块 ==> Python标准库，数据结构常用的模块；collections包含了一些特殊的容器，针对Python内置的容器，例如list、dict、set和tuple，提供了另一种选择。
    # 计数器（Counter）是dict的子类，计算可hash的对象
    print(dict_size.values())
    f.write(str(arr))
    f.write('\n\n')

    """
    绘制饼图
    """
    labels = ['主题一', '主题二', '主题三', '主题四', '主题五']
    sizes = dict_size.values()
    explode = (0, 0.1, 0.1, 0.1, 0.1)

    length = len(list(dict_size.values()))
    labels = labels[: length]
    explode = explode[: length]
    print(length,labels,explode)

    plt.figure(figsize=(12,8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%',shadow=False, explode=explode)
    plt.title(png)
    plt.savefig('观察/{}.png'.format(png))
    plt.show()

if __name__ == '__main__':
    df = pd.read_excel('数据/7 完整数据集（情感词典预测）.xlsx')

    pos = df[df['星级（处理后）'] == '好评']
    # pos.append(df[df['星级（处理后）'] == 4])
    neg = df[df['星级（处理后）'] == '差评']
    # neg.append(df[df['星级（处理后）'] == 2])
    zhongli = df[df['星级（处理后）'] == '一般']

    f = open('数据/10 三类情感主题关键词.txt', 'w', encoding='utf-8')
    main(pos=pos, png="13 积极主题分布图", f=f)
    main(pos=neg, png='14 消极主题分布图', f=f)
    main(pos=zhongli, png='15 中性主题分布图', f=f)
    f.close()




