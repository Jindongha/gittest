# -*- coding: utf-8 -*-
snail_array = []

for i in range(5):
	empty_array = []
	for j in range(5):
		empty_array.append(0)
	snail_array.append(empty_array)

for column in snail_array:
	for num in column:
		print "%2s" % num,
	print
# print init array
 # 0  0  0  0  0
 # 0  0  0  0  0
 # 0  0  0  0  0
 # 0  0  0  0  0
 # 0  0  0  0  0

# change array like this
#  1  2  3  4 5
# 16 17 18 19 6
# 15 24 25 20 7
# 14 23 22 21 8
# 13 12 11 10 9 

######## insert your algorithm here ########
i=-1
j=0
count=1
flag = 0
while count < 26:
	if flag%4 == 0:
		i += 1
		snail_array[i][j] = count

	if flag%4 == 1:		
		j += 1
		snail_array[i][j] = count
		
	if flag%4 == 2:
		i -= 1
		snail_array[i][j] = count

	if flag %4 == 3:
		j -= 1
		snail_array[i][j] = count
		

	if ((i+1)>4 or snail_array[i+1][j] != 0) and flag%4 == 0:
		flag += 1
	if ((j+1)>4 or snail_array[i][j+1] != 0) and flag%4 == 1:
		flag += 1
	if ((i-1)<0 or snail_array[i-1][j] != 0) and flag%4 == 2:
		flag += 1
	if ((j-1)<1 or snail_array[i][j-1] != 0) and flag%4 == 3:
		flag += 1

	count += 1

print 
for i in range(5):
	for j in range(5):
		print "%2s" % snail_array[j][i],
	print
# print result array
# 영어 주석 힘들다.