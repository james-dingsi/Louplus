import pandas as pd
import numpy as np
from pandas import DataFrame, Series
from matplotlib import pyplot as plt
# 设置文件路径
filepath = 'C:/Users/DS/Downloads/ClimateChange.xlsx'

'''此部分是归一化处理'''
def min_max(normal_data):

    min_v = normal_data.min()
    max_v = normal_data.max()
    pro_data = (normal_data - min_v) / (max_v - min_v)

    return pro_data

def co2_gdp_plot():


    # 使用pd.read_excel方法读取文件中'Data'（默认）表的数据，使用国家代码作为索引，
    data = pd.read_excel(filepath, index_col='Country code')

    # 将data中Series code列中值为'EN.ATM.CO2E.KT'的数据筛选出来存入co2_data中，并删除前5列，只保留数值和索引
    co2_data = pd.DataFrame(data[data['Series code']=='EN.ATM.CO2E.KT'])
    co2_data.drop(co2_data.columns[0:5], axis=1, inplace=True)
    # 使用replace替换源文件中的'..'为NaN，inplace=True务必要写
    co2_data.replace('..', np.nan, inplace=True)
    # 填充数据，先使用前面的数据填充，再使用后面的数据填充，以保证填充完整
    co2_data = (co2_data.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)).sum(axis=1)

    # GDP数据操作同上
    gdp_data = pd.DataFrame(data[data['Series code']=='NY.GDP.MKTP.CD'])
    gdp_data.drop(gdp_data.columns[0:5], axis=1, inplace=True)
    gdp_data.replace('..', np.nan, inplace=True)
    gdp_data = (gdp_data.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)).sum(axis=1)

    print('-----------co2_data------------')
    print(co2_data)

    print('-----------gdp_data------------')
    print(gdp_data)


    # 使用concat方法将横向求和后的co2_data和gdp_data进行合并
    #result_data = pd.concat([co2_data.sum(axis=1), gdp_data.sum(axis=1)], axis=1)
    # 给结果重新定义列明，主要是Total列如果没定义名称则会产生默认的0列名，但在之前的代码中Total是统计结果，不知道怎么取列明
    #result_data.columns = ['CO2-SUM','GDP-SUM']

    #print('----------result_data-----------')
    #print(result_data.head(10))



    # 生成绘图所需数据

    print('+++++++++ 1 ++++++++++')
    print(min_max(co2_data))
    print('+++++++++ 2 ++++++++++')
    print(min_max(gdp_data))
    print('======================')
    co2_gdp = pd.concat([min_max(co2_data), min_max(gdp_data)], axis=1)
    co2_gdp.columns = ['CO2-SUM','GDP-SUM']
    china = [co2_gdp.loc['CHN'][0].round(3), co2_gdp.loc['CHN'][1].round(3)]

    print('中国', china)

    ''' 此部分是绘图需求代码'''
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    x = len(co2_gdp.index)
    xx = range(218)
    major_ticks_x = ['CHN', 'USA', 'GBR', 'FRA','RUS']
    major_ticks_y = np.arange(0, 1, 0.2)
    plt.title("GDP-CO2")  # 设置绘图名称
    plt.xticks(xx, major_ticks_x)  # 设置x轴的刻度
    plt.yticks(major_ticks_y)  # 设置y轴的刻度
    plt.ylabel("Values")  # 设置y轴标签名
    plt.xlabel("Countries")  # 设置x轴标签


    plt.plot(co2_gdp['CO2-SUM'])
    plt.plot(co2_gdp['GDP-SUM'], color='r')
    plt.show()

    return fig, china

if __name__ == '__main__':
    co2_gdp_plot()


'''
writer = pd.ExcelWriter('C:/Users/DS/Downloads/challenge7_3.xlsx')
result_data.to_excel(writer)
writer.save()
'''