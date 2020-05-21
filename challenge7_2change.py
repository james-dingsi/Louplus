import pandas as pd
from matplotlib import pyplot as plt

def co2_gdp_plot():
    # 使用pd.read_excel方法读取文件中'Data'（默认）表的数据，使用国家代码作为索引
    data = pd.read_excel('ClimateChange.xlsx', index_col='Country code')
    co2_data = pd.DataFrame(data[data['Series code']=='EN.ATM.CO2E.KT']).iloc[:, 5:]
    gdp_data = pd.DataFrame(data[data['Series code']=='NY.GDP.MKTP.CD']).iloc[:, 5:]
    # 使用replace替换源文件中的'..'为NaN，inplace=True务必要写
    co2_data.replace('..', pd.np.nan, inplace=True)
    gdp_data.replace('..', pd.np.nan, inplace=True)
    # 填充数据，先使用前面的数据填充，再使用后面的数据填充，以保证填充完整
    co2_data = (co2_data.fillna(method='ffill', axis=1
            ).fillna(method='bfill', axis=1)).sum(1)
    gdp_data = (gdp_data.fillna(method='ffill', axis=1
            ).fillna(method='bfill', axis=1)).sum(1)
    # 使用concat方法将横向求和后的co2_data和gdp_data进行合并
    co2_gdp = pd.concat([co2_data, gdp_data], 1)
    # 用 0 填充 NaN
    co2_gdp.fillna(0, inplace=True)
    # 数据归一化
    df = co2_gdp.apply(lambda data: (data-data.min())/(data.max()-data.min()))
    df.columns = ['CO2-SUM','GDP-SUM']
    ''' 此部分是绘图需求代码'''
    fig = plt.subplot()
    刻度列表, 标签列表 = [], []
    for i, value in enumerate(df.index):
        if value in ['CHN', 'USA', 'GBR', 'FRA', 'RUS']:
            刻度列表.append(i)
            标签列表.append(value)
    # 使用 df.plot 方法画图
    df.plot(title="GDP-CO2", ax=fig, kind='line')
    plt.ylabel("Values")        # 设置y轴标签
    plt.xlabel("Countries")     # 设置x轴标签
    # 设置横轴刻度标签
    plt.xticks(刻度列表, 标签列表, rotation='vertical')
    plt.show()
    return fig, pd.np.round(df.loc['CHN':'CHN'].values, 3).tolist()[0]

if __name__ == '__main__':
    print(co2_gdp_plot())
