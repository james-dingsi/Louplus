#!/usr/bin/env python3

def compute(base, value):
	base.append(value)
	result = sum(base)
	print(result)
	base.pop()


if __name__ == '__main__':
	testlist = [10, 20, 30]
	compute(testlist, 15)
	print(testlist)
	compute(testlist, 25)
	print(testlist)
	compute(testlist, 35)
	print(testlist)
