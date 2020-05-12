#!/usr/bin/python3
import json
import pandas as pd

filepath = '/home/shiyanlou/Code/user_study.json'
def analysis(file, user_id):
	times = 0
	minutes = 0
	try:
		userdata = pd.read_json(file, orient='value', encoding='utf8')

		times = userdata[userdata['user_id'] == user_id]['minutes'].count()
		minutes = userdata[userdata['user_id'] == user_id]['minutes'].sum()
	except:
		return 0
	return times, minutes

if __name__ == '__main__':
#	print(analysis(filepath, 168577))
	analysis()

