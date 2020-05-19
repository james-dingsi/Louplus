
import pandas as pd
import numpy as np
from pandas import DataFrame, Series

# 设置文件路径
filepath = 'C:/Users/DS/Downloads/ClimateChange.xlsx'

# 使用pd.read_excel方法读取文件中'Data'表的数据，使用国家代码作为索引，
data = pd.read_excel(filepath, sheet_name='Data', index_col='Country code')
# 将data中Series code列中值为'EN.ATM.CO2E.KT'的数据筛选出来存入co2_data中
co2_data = pd.DataFrame(data[data['Series code'].isin(['EN.ATM.CO2E.KT'])])
#删除前5个不需要的列，axis代表竖向,inplace=True代表写入源文件
co2_data.drop(co2_data.columns[0:5], axis=1, inplace=True)
# 使用replace替换源文件中的'..'为NaN，inplace=True务必要写
co2_data.replace('..', np.nan, inplace=True)
# 填充数据，先使用前面的数据填充，再使用后面的数据填充，以保证填充完整
co2_data = co2_data.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)

# 使用pd.read_excel方法读取文件中'Country'表的数据，使用国家代码作为索引，再删除其中三个不需要的列
country = pd.read_excel(filepath, sheet_name='Country', index_col='Country code').drop(['Capital city', 'Region', 'Lending category'], axis=1)
# 使用concat方法将co2_data中的数据横向求和后，与country表中数据进行合并
result_data = pd.concat([co2_data.sum(axis=1), country], axis=1)
# 给结果重新定义列明，主要是Total列如果没定义名称则会产生默认的0列名，但在之前的代码中Total是统计结果，不知道怎么取列明
result_data.columns = ['Total','Country name','Income group']
# 删除值为0的数据
result_data = result_data[~result_data['Total'].isin([0])]

'''
    相关数据说明：
•	Sum emissions 表示相应收入群体（Income group）的总排放量
	#Sum emissions数据通过Data表第1528至1745行之间的数据进行汇总
•	Highest emission country 为相应收入群体里排放量最高的国家名称（Country name）。
	#Highest emission country数据通过County表中5个收入群体分类进行汇总和筛选，使用.max()函数查找最高值对应的国家名称
•	Highest emissions 为排放量最高的国家对应的排放量数值。
	#方法同上，使用.max()函数查找最高值对应的排放量后，横向.sum()
•	Lowest emission country 为相应收入群体里排放量最低的国家名称。
	# Lowest emission country数据通过Country表中的5个收入群体分类进行汇总和筛选，使用.min()函数查找最低值对应的国家名称
•	Lowest emissions 为排放量最低的国家对应的排放量数值。
	# 方法同上，查找到相关国家后横向求和

'''
print('----------result_data-----------')
print(result_data.head())

# Sum emissions 表示相应收入群体（Income group）的总排放量
sum_emissions = result_data[['Total','Income group']].groupby('Income group').sum()
sum_emissions.columns = ['Sum emissions']
print('----------sum_emissions-----------')
print(sum_emissions)

# Highest emission country 为相应收入群体里排放量最高的国家名称（Country name）
# 注意列表中的列名顺序决定了生成的新数组的列顺序，下同
High_emission = result_data[['Country name', 'Total', 'Income group']].groupby('Income group').max()
High_emission.columns = ['Highest emission country', 'Highest emission']
print('----------High_emission-----------')
print(High_emission)

# Lowest emission country 为相应收入群体里排放量最低的国家名称
Lowest_emission = result_data[['Country name', 'Total', 'Income group']].groupby('Income group').min()
Lowest_emission.columns = ['Lowest emission country', 'Lowest emissions']
print('----------Lowest_emission-----------')
print(Lowest_emission)

# 合成待输出的DataFrame
output_data = pd.concat([sum_emissions , High_emission , Lowest_emission], axis=1)
print('------------Output Data------------')
print(output_data)


writer = pd.ExcelWriter('C:/Users/DS/Downloads/challenge7_3.xlsx')
output_data.to_excel(writer)
writer.save()
