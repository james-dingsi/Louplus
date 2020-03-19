#!/usr/bin/env python3
import sys
temp_set = set()

for a in sys.argv[1:]:
	if a not in temp_set:
		temp_set.add(a)
print(temp_set)
	