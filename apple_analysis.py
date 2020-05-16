#!/usr/bin/env python3
import numpy as np
import pandas as pd
#
filepath = '/home/shiyanlou/Code/apple.csv'

def quarter_volume():
	# 用pandas的读取csv文件方法读取文件，以Date列为索引，以逗号分隔数据
	data = pd.read_csv(filepath, index_col='Date', header=0, sep=',')
	# 将data的索引(即Date列)转换为时间戳索引
	data.index = pd.DatetimeIndex(data.index)
	# 通过resample方法以季度为频率进行时序数据降采样（Q为季度），并使用sum()方法对季度数据求和
	data_q = data.resample('Q').sum()
	# 通过sort_values方法对Volume列进行降序排列，再使用iloc索引第2行的Volume值，存入变量。（第一行是0）
	second_volume = data_q.sort_values('Volume', ascending=False).iloc[1]['Volume']
	return second_volume

if __name__ == '__main__':
	quarter_volume()
