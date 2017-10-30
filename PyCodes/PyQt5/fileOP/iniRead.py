import configparser
import os,sys
from PyQt5.QtCore import *

os.chdir(sys.path[0])

## python 内置 ini config， 增加 default 节，逗号 字段不解析位 List
# Qt ini config 增加 General 节点，逗号字段解析为 List

config=configparser.ConfigParser()
#IpConfig.ini可以是一个不存在的文件，意味着准备新建配置文件。
config.read("ipConfig.ini")

try:
    if 'School' not in config.sections():
        #添加节School
        config.add_section("School")
   
    #添加新的IP地址参数
    config.set("School","IP","192.168.1.120")
    config.set("School","Mask","255.255.255.0")
    config.set("School","Gateway","192.168.1.1")
    config.set("School","DNS","211.82.96.1")
except configparser.DuplicateSectionError:
    print("Section 'Match' already exists")

#由于ini文件中可能有同名项，所以做了异常处理
try:
    if 'Match' not in config.sections():
        config.add_section("Match")

    config.set("Match","IP","172.17.29.120")
    config.set("Match","Mask","255.255.255.0")
    config.set("Match","Gateway","172.17.29.1")
    config.set("Match","DNS","0.0.0.0")
    config.set("Match","List",'1,2,3,4,5')
except configparser.DuplicateSectionError:
    print("Section 'Match' already exists")

saveName = "IpConfigSave.ini"
config.write(open(saveName, "w"))

ip=config.get("School","IP")
mask=config.get("School","mask")
gateway=config.get("School","Gateway")
dns=config.get("School","DNS")
l = config.get("Match","List")
print((ip,mask + '\n' + gateway,dns),'==',type(l),l)


config = QSettings(saveName,QSettings.IniFormat)
config.beginGroup('Match')
rt = config.value('List')
print(type(rt),rt)
config.setValue('List',['aa','bb','cc'])
# config.setValue('List','a,b,c,d,e,f') # to string
rt = config.value('List')
print(type(rt),rt)
config.endGroup()
config.sync()
del config

with open(saveName)  as myFile:
    for eachLine in myFile:
        print(eachLine)

