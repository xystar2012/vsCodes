from collections import Iterable 
import sys,os
import itertools

def fab1(max): 
   n, a, b = 0, 0, 1 
   L = [] 
   while n < max: 
       L.append(b) 
       a, b = b, a + b 
       n = n + 1 
   return L
print("-*-"*20)
for n in fab1(5): 
    print(n)

class Fab(object): 
   def __init__(self, max): 
       self.max = max 
       self.n, self.a, self.b = 0, 0, 1 
 
   def __iter__(self): 
       return self 
 
   def next(self): 
       if self.n < self.max: 
           r = self.b 
           self.a, self.b = self.b, self.a + self.b 
           self.n = self.n + 1 
           return r 
       raise StopIteration()

# for n in Fab(5):
#     print (n)


def fab(max): 
    n, a, b = 0, 0, 1 
    while n < max: 
        yield b 
        # print b 
        a, b = b, a + b 
        n = n + 1 
print("-*-"*20)
for n in fab(5): 
    print(n)

print("-*-"*20)
f = fab(5)
for i in range(5):
    print(next(f))

print(isinstance(fab, Iterable))
print(isinstance(fab(1), Iterable)) 

def read_file(fpath): 
   BLOCK_SIZE = 1024 
   with open(fpath, 'rb') as f: 
       while True: 
           block = f.read(BLOCK_SIZE) 
           if block: 
               yield block 
           else: 
               return
print("-*-"*20)
n = read_file(sys.argv[0])
print(type(n),n)

for n in read_file(sys.argv[0]):
    print(str(n,'utf-8'))

print("-*-"*20)
mygenerator = (x*x for x in range(3))
print(type(mygenerator),mygenerator)
for i in mygenerator:
    print(i)

mygenerator = [x*x for x in range(3)]
print(type(mygenerator),mygenerator)

def createGenerator():
    mylist = range(3)
    for i in mylist:
        yield i*i

mygenerator = createGenerator() # create a generator
print(mygenerator) # mygenerator is an object!
for i in mygenerator:
    print (type(i),i)

horses = [1, 2, 3, 4]
races = itertools.permutations(horses)
print(races)
print(list(itertools.permutations(horses)))
