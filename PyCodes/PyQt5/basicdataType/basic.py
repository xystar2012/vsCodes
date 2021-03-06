from queue import Queue
from itertools import groupby
import random,sys

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

print('-*-'*20 + 'enclose ----')

#一个函数和它的环境变量合在一起，就构成了一个闭包(closure)。
# 在Python中，所谓的闭包是一个包含有环境变量取值的函数对象。
# 环境变量取值被保存在函数对象的__closure__属性中。比如下面的代码：
def line_conf():
    b = 15
    def line(x):
        return 2*x+b
    return line       # return a function object

b = 5
my_line = line_conf()
print(my_line(5))  
print(my_line.__closure__)
print(my_line.__closure__[0].cell_contents)


## senior

def line_conf(a, b):
    def line(x):
        return a*x + b
    return line

line1 = line_conf(1, 1)
line2 = line_conf(4, 5)
print(line1(5), line2(5))

print('-*-'*20 + 'enclose end ---')


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

try:
    aa = 1/0
    cc = dd
except Exception as e:
    print ('Error', e)
    print('SysErr:',sys.exc_info(),sys.exc_info()[1])