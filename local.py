#!/usr/bin/env python3

def change():
	global a
	a = 100
	print(a)

a = 9
print("Before the function call", a)
print("Inside change function", end=" ")
change()
print("After the function call it", a)
