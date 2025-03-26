import pandas as pd

df = pd.read_excel("数据/7 完整数据集（情感词典预测）.xlsx",index_col=0)

# 统计行数 len(df)
print(len(df))

# 统计有多少种不同的值 df[‘lable’].nunique()
print(df['会员'].nunique())
# 对 列 中每种不同的值 进行计数 df[‘lable’].value_counts()
print(df['会员'].value_counts())


# 对整张表格进行统计描述（这里仅对数值形的列进行统计）仅对数值型
print(df.describe())

# 对整张表格进行统计描述（所有类型进行统计）
print(df.describe(include='all'))

# # 对指定的列Math_A，进行统计描述
# print(df.Math_A.describe())

out_df = df.describe()
out_df.to_excel("数据/14 极值、标准差等数据统计.xlsx")



# # 指定统计方式
# # 求和
# sum()
#
# # 计数
# df.count()
#
# # 中位数
# df.median()
#
# # 分位数
# df.quantile()
#
# # 最大值 / 最小值
# df.max() / df.min()
#
# # 均值
# df.mean()
#
# # 方差 / 标准差
# df.var() / df.std()
#
# # 批量操作（对每个元素应用同一个自定义函数）df.apply()
# def double (x):
#     return x*2
# print(df.Math_B.apply(double))




