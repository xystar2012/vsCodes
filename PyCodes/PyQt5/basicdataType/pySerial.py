# code:utf-8
import sys
import serial
import time
import struct
from datetime import datetime
import random,re

print(sys.path,sys.version_info)

def fmtDateSend():
        global _count
        ### 年 月 日
        rate = 1 if bVariantData else 0
        _count = _count + 1
        data = bytearray.fromhex('7e')
        # date = QDateTime.currentDateTime()
        dt = datetime.now()
        # dt = date.date()
        data += struct.pack('=BBB',dt.year - 2000,dt.month,dt.day)
        # tm = dt.time()
        # delta = timedelta(hours=1,milliseconds=123,microseconds=123456)
        ms = (dt.hour*3600 + dt.minute*60 + dt.second)*10000 + int(dt.microsecond/100)
        data += struct.pack('=I',ms)

        ## 帧频   相机类型8,9  ok
        i = 0x1 if rate*_count%2 else 0x10
        data += struct.pack('=BB',i,0x02)
        # print(type(data),len(data),data)
        ## A、E 角度
        A = int((10.123456 + rate*int(random.uniform(1,9)))*pow(2,24)/360)
        E = int((20.123456 + rate*int(random.uniform(1,9)))*pow(2,24)/360)
        dA = struct.pack('I',A)
        data += dA[0:3]
        dE = struct.pack('I',E)
        data += dE[0:3]

        ## 调光调焦 16,17   0.0560456
        foclen = (20 + rate*random.uniform(0.1,0.9))*pow(10,3)/1.6
        # print('foclen',hex((int(foclen))))
        data += struct.pack('=H',int(foclen))
        data += bytearray.fromhex('00'*2)
        ## 目标距离
        data += struct.pack('=I',50 + rate*int(random.uniform(1,9)))
        
        ## 滤光片  拖把量 24,25
        list1 = [0x01,0x02,0x2,0x3,0x4]
        list2 = [0x0,0x11]
        data += struct.pack('=BB',list1[rate*_count%4],list2[rate*_count%2])
        ### miss A E
        missAE = struct.pack('=HH',0x8000 + rate*int(random.uniform(1,9)),0x7000 + rate*int(random.uniform(1,9)))
        # print('missAE:',missAE)
        data += missAE
        data += bytearray.fromhex('00'*1)
        ## A  E 速度
        A = int((10.123456 + rate*int(random.uniform(1,9)))*pow(2,24)/360)
        E = int((20.123456 + rate*int(random.uniform(1,9)))*pow(2,24)/360)
        dA = struct.pack('I',A)
        data += dA[0:3]
        dE = struct.pack('I',E)
        data += dE[0:3]
        # print('AESpeed:',A,E)
        data += bytearray.fromhex('00'*2)
        ## 尾部
        data += bytearray.fromhex('e7')
        # print(len(data))
        return data

if __name__ == '__main__':
    
    bVariantData = True
    _count = int(0)

    # ser = serial.Serial('com7',460800)
    ser = serial.Serial('com4',9600)
    ser.timeout = 0.5
    
    if not ser.isOpen():
        sys.exit()
    
    while True:
        data = ser.read(100)
        # hexstr = ''.join(hex(x) for x in data)
        hexstr = ' '.join('{:02x}'.format(x) for x in data)  
        m = re.search('(7e.{31,31}e7)', hexstr)
        if m:
            requestStr = m.group(0)
            print(requestStr)

        data = fmtDateSend()
        # str = data.decode()
        # print(str)
        n = ser.write(data)  
        # time.sleep(0.1)
