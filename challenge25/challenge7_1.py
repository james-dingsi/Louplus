import pandas as pd

def co2():
        # 使用pd.read_excel方法读取文件中'Data'表的数据(默认读取第一张表)，使用国家代码作为索引
        data = pd.read_excel('ClimateChange.xlsx', index_col='Country code')
        # 将data中Series code列中值为'EN.ATM.CO2E.KT'的数据筛选出来存入co2_data中，直接用==，也可以用isin
        co2_data = pd.DataFrame(data[data['Series code']=='EN.ATM.CO2E.KT'])
        #删除前5个不需要的列，axis代表竖向,inplace=True代表写入源文件
        co2_data.drop(co2_data.columns[0:5], axis=1, inplace=True)
        # 使用replace替换源文件中的'..'为NaN，inplace=True务必要写
        co2_data.replace('..', pd.np.nan, inplace=True)
        # 填充数据，先使用前面的数据填充，再使用后面的数据填充，以保证填充完整
        co2_data = co2_data.fillna(method='ffill', axis=1).fillna(
                method='bfill', axis=1)
        # 使用pd.read_excel方法读取文件中'Country'表的数据，不用写sheetname
        # 使用国家代码作为索引，再删除其中三个不需要的列
        country = pd.read_excel('ClimateChange.xlsx', 'Country', 
                index_col='Country code'
        ).drop(['Capital city', 'Region', 'Lending category'], axis=1)
        # 使用concat方法将co2_data中的数据横向求和后，与country表中数据进行合并
        result_data = pd.concat([co2_data.sum(axis=1), country], axis=1)
        # Sum emissions 表示相应收入群体（Income group）的总排放量
        sum_emissions = result_data.groupby('Income group').sum()
        sum_emissions.columns = ['Sum emissions']
        # Highest emission country 为相应收入群体里排放量最高的国家名称（Country name）
        # 这时的列名是默认的0，先分组后排序，取第一条最大值，同时设置索引
        High_emission = result_data.sort_values(0, ascending=False).groupby(
                'Income group').head(1).set_index('Income group')
        # 改列名
        High_emission.columns = ['Highest emissions', 'Highest emission country']
        # Lowest emission country 为相应收入群体里排放量最低的国家名称
        Lowest_emission = result_data[result_data[0]>0].sort_values(0).groupby(
                'Income group').head(1).set_index('Income group')
        Lowest_emission.columns = ['Lowest emissions', 'Lowest emission country']
        # 合成待输出的DataFrame，列的顺序可以不同
        results = pd.concat([sum_emissions , High_emission , Lowest_emission], axis=1)
        return results

if __name__ == '__main__':
        print(co2())
