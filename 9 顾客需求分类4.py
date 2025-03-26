import pandas as pd
import openpyxl
import os, re

def cut_sent(para):
    para = re.sub('([。！？\?])([^”])',r"\1\n\2",para) # 单字符断句符
    para = re.sub('(\.{6})([^”])',r"\1\n\2",para) # 英文省略号
    para = re.sub('(\..{2})([^”])',r"\1\n\2",para) # 中文省略号
    para = re.sub('(”)','”\n',para)   # 把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()       # 段尾如果有多余的\n就去掉它
    #很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")

def main(dfData, to_excel):
    new_all_df = pd.DataFrame(columns=("对应评论序号", "对应整条评论内容", "对应评论句子", "包含产品特征词", "对应顾客需求", "句子长度", "对应评论星级"))
    index_list = dfData['对应评论序号'].values.tolist()
    # print(len(index_list))
    for i in set(index_list):
        print(i)
        sole_df = dfData.loc[dfData['对应评论序号'] == i, ['对应评论句子','包含产品特征词','对应顾客需求']]
        # print(sole_df)

        new_df = sole_df.groupby(['对应顾客需求'])
        # print(new_df)

        new_df1 = new_df['对应评论句子'].apply(lambda x:' '.join(list(set(x.str.cat(sep=' ').split(' '))))).reset_index()
        new_df2 = new_df['包含产品特征词'].apply(lambda x:' '.join(list(set(x.str.cat(sep=' ').split(' '))))).reset_index()
        new_df3 = pd.merge(new_df2,new_df1)
        # print(new_df3)

        jz = [len(re.findall(r'[\u4E00-\u9FFF]', x)) for x in new_df1['对应评论句子']]
        xj = dfData.loc[dfData['对应评论序号'] == i, '对应评论星级'].values.tolist()[0]
        content = dfData.loc[dfData['对应评论序号'] == i, '对应整条评论内容'].values.tolist()[0]
        row_count = len(jz)

        new_df4 = pd.DataFrame({
            "对应评论序号": [i for x in range(row_count)],
            "对应整条评论内容": [content for x in range(row_count)],
            "句子长度": jz,  # 字数
            "对应评论星级": [xj for x in range(row_count)] ,
        })

        new_df5 = pd.concat([new_df3,new_df4],axis=1)
        # print(new_df5)

        new_all_df = pd.concat([new_all_df,new_df5], axis=0)
        # print(new_all_df)

    new_all_df.to_excel(to_excel)



if __name__ == '__main__':
    # open(to_excel='数据/15 顾客需求分类.xlsx')
    # 获取数据
    # dfData = pd.read_excel('数据/16 顾客需求分类3.xlsx',index_col=0)  # ,index_col=0
    dfData = pd.read_excel('数据/16 顾客需求分类3.2.xlsx',index_col=0)  # ,index_col=0

    # iris.reset_index(drop=True, inplace=True) # 重置索引

    # path = '数据/16 顾客需求分类4.xlsx'
    path = '数据/16 顾客需求分类4.2.xlsx'
    main(dfData, to_excel=path)