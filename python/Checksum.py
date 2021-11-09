# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 14:43:39 2021

@author: keith
@title: checksum checker
"""

to_check = "0x45 00 00 54 00 03 58 50 20 06 00 00 7C 4E 03 02 B4 0E 0F 02"

no_spaces = to_check.replace(" ", "")

lst = []

start = 0

while start < len(no_spaces):
    temp = no_spaces[start:start+4]
    if "x" in temp:
        start += 2
        continue
    else:
        temp_txt = str(temp)
        lst.append(temp_txt)
        start += 4
        
#print(lst)  

binary_lst = [int(item, 16) for item in lst]

#print(binary_lst)

binary_strings = [format(int(item, 16), "016b") for item in lst]

sum = 0

for item in binary_lst:
    sum += item
    if sum > 65535:
        sum -= 65536
        sum += 1
        
print (sum)
print(32767 - sum)

ans = "111111111110000"
print(int(ans, 2))




