#!/usr/bin/env python3

num = input("Enter number: ")
try:
    new_num = int(num)
    print('INT:{}'.format(new_num))
except:
	print("ERROR:{}".format(num))

