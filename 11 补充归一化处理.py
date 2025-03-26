# 数据处理
import pandas as pd
import math

def main(dfData, to_excel):
    # print(dfData)
    dfData['归一化处理pos'] = ''
    dfData['归一化处理nes'] = ''
    dfData['取整处理pos'] = ''
    dfData['取整处理nes'] = ''
    pos_max = max(dfData['情感pos数'].tolist())
    pos_min = min(dfData['情感pos数'].tolist())
    nes_max = max(dfData['情感nes数'].tolist())
    nes_min = min(dfData['情感nes数'].tolist())

    count = 0
    for i in range(len(dfData)):
        pos = dfData['情感pos数'].iloc[i]
        nes = dfData['情感nes数'].iloc[i]
        guiyi_pos = 0 + (15 - 0) / (pos_max - pos_min)*(pos - pos_min)
        guiyi_nes = -15 + (0 + 15) / (nes_max - nes_min)*(nes - nes_min)


        dfData['归一化处理pos'].iloc[i] = '= 0 + (15 - 0) / ({} - {})*({} - {})'.format(pos_max, pos_min, pos, pos_min)
        dfData['归一化处理nes'].iloc[i] = '= -15 + (0 + 15) / ({} - {})*({} - {})'.format(nes_max, nes_min, nes, nes_min)
        dfData['取整处理pos'].iloc[i] = '=CEILING({},0.5)'.format(guiyi_pos)
        dfData['取整处理nes'].iloc[i] = '=CEILING({},-0.5)'.format(guiyi_nes)

        # dfData['归一化处理pos'].iloc[i] = 0 + (15 - 0) / (pos_max - pos_min)*(pos - pos_min)
        # dfData['归一化处理nes'].iloc[i] = -15 + (0 + 15) / (nes_max - nes_min)*(nes - nes_min)

        count += 1
        print(count)

    dfData.to_excel(to_excel)

if __name__ == '__main__':
    ## 获取数据
    # dfData = pd.read_excel('数据/17 顾客需求分类2情感预测4.xlsx',index_col=0)
    # main(dfData, to_excel='数据/18 顾客需求分类2情感预测5（归一化后）2.xlsx')

    dfData = pd.read_excel('数据/17 顾客需求分类2情感预测4.2.xlsx',index_col=0)
    main(dfData, to_excel='数据/18 顾客需求分类2情感预测5（归一化后）2.2.xlsx')  # 记得处理文件，手动复制粘贴，去掉公式