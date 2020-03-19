#!/use/bin/env python3
import sys

list_s = []
list_l = []
for a in sys.argv[1:]:
	if len(a) <= 3:
		list_s.append(a)	
	else:
		list_l.append(a)	
print(' '.join(list_s))
print('+'.join(list_l))




