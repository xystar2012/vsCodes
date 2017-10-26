# -*- coding: UTF-8 -*-
from random import randint
import random
# from twisted.internet import protocol, reactor
# from SocketServer import TCPServer as TCP, StreamRequestHandler as SRH


print ("choice([1, 2, 3, 5, 9]) : ", random.choice([1, 2, 3, 5, 9]))
print ("choice('A String') : ", random.choice('A String'))

def simpleGen():
    yield 1
    yield '2 --> punch!'

for eachItem in simpleGen():
    print (eachItem)

def randGen(aList):
    while len(aList) >0:
        yield aList.pop(randint(0,len(aList)))

# for item in randGen(['how','are','you!']):
#     print(item)

## 11.10.2 加强的生成器特性
def counter(start_at=0):
    count = start_at
    while True:
        val = (yield count) 
        if val is not None:
            count = val
    else:
        count += 1
count = counter(5)
## py3++
print(next(count))
print(count.send(9))
print(next(count))
count.close()
# print(next(count))

# 生成器
print('-*-'*20 + 'gen---->')
def gen():
    a = 100
    yield a
    a = a*8
    yield a
    yield 1000

for i in gen():
    print(i)

print('-*-'*20 + 'gen end ---')

def gen():
    for i in range(4):
        yield i

## 它又可以写成生成器表达式(Generator Expression):
G = (x for x in range(4))
print(G)
print(next(G))

## 表推导
xl = [1,3,5]
yl = [9,12,13]
L  = [ x**2 for (x,y) in zip(xl,yl) if y > 10]
print(list(zip(xl,yl)))
print(L)  ##  9 25
