import re
import collections

## advance re for scrapy using
data = re.findall('car', 'carry the barcardi to the car')
print(data)
data = re.findall('\w*?\.jpg|\w*?\.png',"flower is __aa.jpg bb.png cc.jpgdd.png11.jpg22.png")
print(data)

rt = re.search('(hello){2}','hello it hellohelloboy')
print(rt,rt.groups(),rt.group(0))
rt = re.search('hello{2}','hello it helloohelloboy')
print(rt,rt.groups(),rt.group(0))
###  非获取匹配
rt = re.match('industr(?:y|ies)','industry')
print(rt,rt.group(0))

rt = re.match('industr(?:y|ies)','industries')
print(rt,rt.group(0))
## 正向 预查 构造不回溯
rt = re.match('Windows(?=95|98|2000|NT)','Windows95')
print(rt,rt.group(0))
## 负向 预查
rt = re.match('Windows(?!95|98|2000|NT)','Windows3.1')
print(rt,rt.group(0))
## 负向 预查  非 un 开头单词  构造不回溯
rt = re.match(r'\b(?!un)\w+\b','happy re pattarn')
print(rt,rt.group(0))

##  子表达式在此位置的左侧 匹配时 才继续匹配
m = re.search('(?<=-)\w+', 'spam-egg')
print(m,m.group(0))
m = re.search('(?<=abc)def', 'abcdef')
print(m,m.group(0))
m = re.search('(?<=19)\d+', '198520803')
print(m,m.group(0))
## 全 字匹配
m = re.search('(?<!20)\d+', '17920712')
print(m,m.group(0))
##  (?> )  表达式 未实现
# m = re.search(r'this->(?> func)', 'this->function()')
# print(m,m.group(0))