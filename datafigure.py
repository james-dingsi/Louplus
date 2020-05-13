#!/usr/bin/env python3
import numpy as np
import pandas as pd
import json
from matplotlib import pyplot as plt
from pandas import Series, DataFrame

filepath = '/home/shiyanlou/Code/user_study.json'
def data_plot():
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
        # 从json文件中导入
	userdata = pd.read_json(filepath, orient='value', encoding='utf8')
	# 保留user_id和minutes列,并以user_id为索引进行分组去重，sum叠加minutes值
	data = userdata[['user_id', 'minutes']].groupby('user_id').sum()
	
	major_ticks_x = np.arange(0, data.index.max(), 50000)  #建立x轴刻度从0开始，到user_id最大值结束，间隔5万，注意此时user_id为索引
	major_ticks_y = np.arange(0, data['minutes'].max(), 500) #建立y轴刻度从0到Minutes的最大值，间隔500
	plt.title("StudyData") # 设置绘图名称
	plt.xticks(major_ticks_x) # 设置x轴的刻度
	plt.yticks(major_ticks_y) # 设置y轴的刻度
	plt.ylabel("Study Time") # 设置y轴标签名
	plt.xlabel("User ID") # 设置x轴标签

	# 由于data对象的索引是user_id，所以直接打印累加后的时间
	plt.plot(data['minutes'], color='r')
	plt.show()
	return ax

if __name__ == '__main__':
	data_plot()


