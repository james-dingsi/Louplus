import re
from collections import Counter

# 使用正则表达式解析日志文件，返回数据列表
def open_parser(filename):
	with open(filename) as logfile:
		# 解析日志文件
		pattern = (r''
					r'(\d+.\d+.\d+.\d+)\s-\s-\s' # IP地址
					r'\[(.+)\]\s' # 时间
					r'"GET\s(.+)\s\w+/.+"\s' # 请求路径
					r'(\d+)\s'  # 状态码
					r'(\d+)\s'  # 数据大小
					r'"(.+)"\s' # 请求头
					r'"(.+)"'   # 客户端信息
					)
		parsers = re.findall(pattern, logfile.read())
		return parsers

def main():
	# 使用正则解析日志文件
	logs = open_parser('/home/shiyanlou/Code/nginx.log')
	# 建立两个空列表用于存储统计对象
	ip_count = []
	url_count = []
	for item in logs:
		# 根据题目要求提取列表中的时间值：列表下标为1
		# 使用:将字符串分割后取最前面的值，并和11/1/2017比对
		if '11/Jan/2017' == item[1].split(':')[0]:
			# 如果匹配，则将此条目中的IP地址（下标为0）存入列表
			ip_count.append(item[0])
			# 和404比对，符合条件的将url存入列表（下标为2）
		if '404' == item[3]:
			url_count.append(item[2])

		# 使用collections模块的Counter方法统计列表中的重复项和次数,返回一个可迭代对象
		# 统计最大值，存入变量
	max_ip = max(Counter(ip_count).values())
	max_404 = max(Counter(url_count).values())
		# 根据最大值来匹配对应的键，存入字典
	for k, v in Counter(ip_count).items():
		if v == max_ip:
			ip_dict = {k: v}
	for k, v in Counter(url_count).items():
		if v == max_404:
			url_dict = {k: v}

	return ip_dict, url_dict

if __name__ == '__main__':
	ip_dict, url_dict = main()
	print(ip_dict, url_dict)

