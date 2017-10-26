# -*- coding: utf-8 -*-
import json

dic1 = {'type':'dic1','username':'loleina','age':16}
json_dic1 = json.dumps(dic1)
print (json_dic1)
## ,encoding="utf-8",ensure_ascii=True
json_dic2 = json.dumps(dic1,sort_keys=True,indent =4,separators=(',', ': '),ensure_ascii=True)
print (json_dic2)

 # 将python对象test转换json对象
test = [{"username":"测试","age":16},(2,3),1]
print (type(test))
python_to_json = json.dumps(test,ensure_ascii=False)
print (python_to_json)
print (type(python_to_json))

# 将json对象转换成python对象
json_to_python = json.loads(python_to_json)
print (json_to_python)
print (type(json_to_python))