import jieba,sys,re
import pandas as pd


def res_cpu(string):
    cpu_result1 = re.search("(i|R)(3|5|7|9)", str(string), re.I)
    if cpu_result1 == None:
        cpu_result1 = ''
    else:
        cpu_result1 = cpu_result1.group()
    panding = None
    cpu_result2 = re.search("(8|16|32)G", str(string), re.I)
    if cpu_result2 == None:
        cpu_result2 = re.search("8|16|32", str(string), re.I)
        if cpu_result2 == None:
            cpu_result2 = ''
        else:
            cpu_result2 = cpu_result2.group() + 'G'
            panding = True
    else:
        cpu_result2 = cpu_result2.group()

    cpu_result3 = re.search("256G|512G|1T", str(string), re.I)
    if cpu_result3 == None:
        cpu_result3 = re.search("256|512|1T", str(string), re.I)
        if cpu_result3 == None:
            cpu_result3 = ''
            if panding == True:
                cpu_result3 = ''
        else:
            cpu_result3 = cpu_result3.group() + 'G'
    else:
        cpu_result3 = cpu_result3.group()

    cpu_result4 = re.search("独显|集显", str(string), re.I)
    if cpu_result4 == None:
        cpu_result4 = ''
        # cpu_result4 = re.search("锐炬", str(string), re.I)
        # if cpu_result4 == None:
        #     cpu_result4 = ''
        # else:
        #     cpu_result4 = '集显'
    else:
        cpu_result4 = cpu_result4.group()

    # ret = cpu_result1 + str(' ' if cpu_result1 != '' else '') + cpu_result2 + str(' ' if cpu_result2 != '' else '') + cpu_result3 + str(' ' if cpu_result3 != '' else '') + cpu_result4
    ret = cpu_result1 + str(' ') + cpu_result2 + str(' ') + cpu_result3 + str(' ') + cpu_result4

    # print(ret)
    # if ret == '':
    #     pass
    return ret

def res_computer(string):
    cpu_result1 = re.search("D|X", str(string), re.I)
    if cpu_result1 == None:
        cpu_result1 = ''
    else:
        cpu_result1 = cpu_result1.group()
        # if cpu_result1 == 'x':
            # pass

    cpu_result2 = re.search("13|14|15[^5]", str(string)+' ', re.I)
    if cpu_result2 == None:
        cpu_result2 = re.search("16[^G]", str(string)+' ', re.I)
        if cpu_result2 != None:
            cpu_result2 = cpu_result2.group()
            if '16' in cpu_result2:
                panding3 = re.search("D|16s", str(string), re.I)
                if panding3 != None:
                    cpu_result2 = cpu_result2[:2]
                else:
                    panding2 = re.search("256|512|1T|G", str(string), re.I)
                    if panding2 == None:
                        cpu_result2 = cpu_result2[:2]
                    else:
                        cpu_result2 = ''
            else:
                cpu_result2 = ''
        else:
            cpu_result2 = ''
    else:
        cpu_result2 = cpu_result2.group()
        if '15' in cpu_result2 and len(str(cpu_result2)) >= 2:
            cpu_result2 = cpu_result2[:2]


    cpu_result3 = re.search("Pro|SE|s", str(string), re.I)
    if cpu_result3 == None:
        cpu_result3 = ''
    else:
        cpu_result3 = cpu_result3.group()

    ret = cpu_result1 + cpu_result2 + cpu_result3
    # print(cpu_result1
    #       + cpu_result2
    #       + cpu_result3)
    if ret != '':
        xh = ['D13', 'D14', 'D15', 'D16', '13', '14', '15','16', '13s', '14s', '15s', '16s', '13SE', 'D14SE', 'D15SE', 'D16SE', 'XPro', 'X', 'SE']
        for a in xh:
            if ret == a:
                return ret
    else:
        return ret

def main():
    df = pd.read_excel('数据/1 完整数据集.xlsx')

    # df1 = df['大小']
    # df2 = df['版本']
    dfAdd = pd.DataFrame(columns=['型号（处理后）','大小（处理后）'])

    for i in range(len(df)):
        string = df['大小'].loc[i]
        string2 = df['版本'].loc[i]

        cpu_result = ''
        cpu_result1 = res_cpu(string)
        cpu_result2 = res_cpu(string2)
        if cpu_result1:
            if cpu_result2:
                if len(cpu_result1)>= len(cpu_result2):
                    cpu_result = cpu_result1
                else:
                    cpu_result = cpu_result2
            else:
                cpu_result = cpu_result1
        else:
            cpu_result = cpu_result2

        computer_result = ''
        computer_result1 = res_computer(string)
        computer_result2 = res_computer(string2)
        if computer_result1:
            if computer_result2:
                if len(computer_result1)>= len(computer_result2):
                    computer_result = computer_result1
                else:
                    computer_result = computer_result2
            else:
                computer_result = computer_result1
        else:
            computer_result = computer_result2

        # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        if computer_result:
            computer_result = 'MateBook'+ computer_result
            
        dataAdd = pd.Series({'型号（处理后）': computer_result,'大小（处理后）': cpu_result})
        # dataAdd = pd.Series({'型号（处理后）': None,'大小（处理后）': None})
        dfAdd = dfAdd.append(dataAdd, ignore_index=True)

    df = pd.concat([df, dfAdd], axis=1)
    #####################################################
    df.to_excel('数据/2 完整数据集（型号处理后）.xlsx')

if __name__ == '__main__':
    main()





















# import numpy as np
# a = np.array([0.10543472,0.02998181,0.04402333,0.02680416,0.05376939,0.70458054
# ,0.72077824,0.05229933,0.72365343,0.04058434,0.02115428,0.06846068
# ,0.05404611,0.6593681,0.02898275,0.03792834,0.01832938,0.03162993
# ,0.05548955,0.02948952,0.01940297,0.03286444,0.02392882,0.04523665
# ,0.0382132,0.02165476,0.04902908,0.05016392,0.04596556,0.01869377
# ,0.06509076,0.74513214,0.05763709,0.11297088,0.03292263,0.05745483
# ,0.04068091,0.02309868,0.00962077,0.0294642,0.01603032,0.03952796
# ,0.02853536,0.0283375,0.01419937,0.03965699,0.67179015,0.03397994
# ,0.0271247,0.03373744,0.72504974,0.78870007,0.07407517,0.02674506
# ,0.03071419,0.03650212,0.05438661,0.01425351,0.01786918,0.01820283
# ,0.03472881,0.02226377,0.01748793,0.05208284,0.01646321,0.00745972
# ,0.03202994,0.07141689])
#
# print(type(a))
# print(a)
# list_ = []
# for i in a:
#     i = str(i)[2]
#     # print(i)
#     if i == '0':
#         a = 0
#     else:
#         a = 1
#     print(a)
#     list_.append(a)
# b = np.array(list_)
# print(b)