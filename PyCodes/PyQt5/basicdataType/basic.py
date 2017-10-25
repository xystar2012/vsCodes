from queue import Queue
from itertools import groupby
import random

print('-*-'*20 + 'group by ----')
def compress(l):
    return [a for a,b in groupby(l)]

def pack(l):
    return [list(b) for a,b in groupby(l)]
x = [random.randint(0,5) for x in range(20)]
print(x)
arr = [(a,list(b)) for a,b in groupby(x)]
print('compress:',compress(arr))
print('pack:',pack(x))

arr = [a for a,b in groupby(sorted(x))]
print(arr)
arr = [list(b) for a,b in groupby(sorted(x))]
print(arr)
dic = dict([(a,len(list(b))) for a,b in groupby(sorted(x))])
print(dic)
arr = [a for a,b in groupby(x) if len(list(b)) > 1]
print(arr)
print('-*-'*20 + 'group by end ---')

q = Queue()

l1 = [2,3,4]
l2 = [4,5,6]

for (x,y) in zip(l1,l2):
    print (x,y,'--->',x*y)

a = 10
print (a,type(a)) 
a = 'hello world'
print(a,type(a))
s1 = (2, 1.3, 'love', 5.6, 9, 12, False)  
s2 = [True, 5, 'smile'] 
print(s1,type(s1))
print(s2,type(s2))
s2[1] = 3.0
print(s2)
s3 = [1,[3,4,5]]
print(s3,type(s3),s3[1][2])
print(s1[0:5:2])  # 从下标0到下标4 (下标5不包括在内)，每隔2取一个元素 （下标为0，2，4的元素）
print(s1[-1])             # 序列最后一个元素
print(s1[-3])             # 序列倒数第三个元素

# for a in range(10):
#     print (a**2)

# for i in range(10):
#     if i % 2: 
#         continue
#     print (i)

i = 0
while i < 8:
    i = i + 1;
    if i % 2: 
        continue
a = 1

def change_integer(a):   #第一个例子，我们将一个整数变量传递给函数，函数对它进行操作，但原整数变量a不发生变化。
    a = a + 1
    return a

print (change_integer(a))
print (a)

b = [1,2,3]

def change_list(b):
    b[0] = b[0] + 1
    return b

print (change_list(b))
print (b)

# print (dir(list))
# print (help(list))