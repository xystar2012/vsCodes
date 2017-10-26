import configparser
import os,sys

os.chdir(sys.path[0])

config=configparser.ConfigParser()
#IpConfig.ini可以是一个不存在的文件，意味着准备新建配置文件。
config.read("ipConfig.ini")

try:
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
    config.add_section("Match")
    config.set("Match","IP","172.17.29.120")
    config.set("Match","Mask","255.255.255.0")
    config.set("Match","Gateway","172.17.29.1")
    config.set("Match","DNS","0.0.0.0")
except configparser.DuplicateSectionError:
    print("Section 'Match' already exists")

saveName = "IpConfigSave.ini"
config.write(open(saveName, "w"))


ip=config.get("School","IP")
mask=config.get("School","mask")
gateway=config.get("School","Gateway")
dns=config.get("School","DNS")
print((ip,mask + '\n' + gateway,dns))

myFile = open(saveName)
for eachLine in myFile:
    print(eachLine)