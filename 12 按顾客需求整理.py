# 第一步：调用pandas包
import pandas as pd
import openpyxl

def main(p1, p2):
    #第二步：读取数据
    iris = pd.read_excel(p1, index_col=0 )#读入数据文件
    # iris.reset_index(drop=True, inplace=True)

    class_list = list(iris['对应顾客需求'].drop_duplicates())#获取数据class列，去重并放入列表
    # 第三步：按照类别分sheet存放数据、
    workbook = openpyxl.Workbook()
    workbook.save(p2)
    writer = pd.ExcelWriter(p2)#创建数据存放路径
    for i in class_list:
        iris1 = iris[iris['对应顾客需求']==i]
        iris1.reset_index(drop=True, inplace=True)
        iris1.to_excel(writer,i)

    writer.save()#文件保存
    # writer.close()#文件关闭
    print('分类整理 成功！')

if __name__ == '__main__':
    # main('数据/17 顾客需求分类2情感预测2.xlsx', '数据/19 按顾客需求分类整理.xlsx')

    # main('数据/18 顾客需求分类2情感预测5（归一化后）.xlsx', '数据/19 按顾客需求分类整理2.xlsx') # 直接处理，公式的数据不会被保留，手动在excel变为普通数字

    # main('数据/18 顾客需求分类2情感预测5（归一化后）2.xlsx', '数据/19 按顾客需求分类整理2.xlsx')  # # 记得处理文件，手动复制粘贴，去掉公式

    main('数据/18 顾客需求分类2情感预测5（归一化后）2.2.xlsx', '数据/19 按顾客需求分类整理2.2.xlsx')  # # 记得处理文件，手动复制粘贴，去掉公式