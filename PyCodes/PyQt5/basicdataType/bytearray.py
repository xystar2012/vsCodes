import re
import binascii  
import struct
from datetime  import datetime,timedelta,time


def ByteToHex( bins ):
    """
    Convert a byte string to it's hex string representation e.g. for output.
    """
    return ''.join( [ "%02X" % x for x in bins ] ).strip()

def HexToByte( hexStr ):
    """
    Convert a string hex byte values into a byte string. The Hex Byte values may
    or may not be space separated.
    """
    return bytes.fromhex(hexStr)

## 类似wireshark hexData 打印
def hexdump(src,length = 16):
    result = []
    # digits = 4 if isinstance(src,unicode) else 2
    digits = 4 if isinstance(src,str) else 2

    for i in range(0,len(src),length):
        s = src[i:i+length]
        hexa = ' '.join(["%0*X" % (digits,ord(x)) for x in s])
        text = ''.join([x if 0x20 <= ord(x) < 0x7e else b'.' for x in s])
        result.append("%04x    %-*s    %s" %(i,length*(digits + 1),hexa,text))

    print(('\n'.join(result)))

hexdump('title:协议头1234567890hello abcdefghijklmnopqrstuvwxyz')

hexStr2  = "FF FF FF 5F 81 21 07 0C 00 00 FF FF FF FF 5F 81 29 01 0B"
# print(hexStr2[:])
data = bytes.fromhex(hexStr2)
print(data)
data2 = str(data)
print(type(data2),data2)
data = [0x12,0x34,0x56,0x78]
print(ByteToHex(data))

data = b'12345678'
print(type(data),data)
data2 = ":".join('{:02x}'.format(x) for x in data)

print('#-*-'*11,'search byte','#-*-'*11)
data = b'\x00\xe7~\x00\x00\x00\x00\x00\xea\x00\x00\x00\x00\xe7~\x00\x00\x00\x00\x00\xeb\x00\x00\x00\x00\xe7~\x00\x00\x00\x00\x00\xec\x00\x00\x00\x00\xe7'
print(type(data))
hexstr = ' '.join('0X%02X' %  (x) for x in data)  
z = binascii.b2a_hex(data)  ## bytes
print(type(z),z)  ##
m = str(z)   ## str
print(type(m),m)  
rt = re.search('(7e.{20,20}e7)', m)
print(rt.group(0))
m = ' '.join("%02X"% x for x in data)
print(type(m),m)
rt = re.search('(7E.{31,31}E7)', m)
print(rt.group(0))


print('#-*-'*11,'pack data','#-*-'*11)
### 年月日
data = bytearray.fromhex('7e')
dt = datetime.now()
data += struct.pack('=BBB',dt.year - 2000,dt.month,dt.day)
# delta = timedelta(hours=1,milliseconds=123,microseconds=123456)
ms = (dt.hour*3600 + dt.minute*60 + dt.second)*10000 + int(dt.microsecond/100)
data += struct.pack('=I',ms)
print(type(data),data)
print(binascii.b2a_hex(data))
print(binascii.hexlify(data))

d1 = 1000
h1 = struct.pack('I',d1)
print(h1,type(h1),repr(h1))
print(h1[0:2])
# data = bytearray.fromhex(binascii.unhexlify(h1))
# print(type(data),len(data),data)


print('#-*-'*11,'str <=> hexStr','#-*-'*11)
## '53216A' -> [0x53, 0x21, 0x6A]
## 方法：hexstring -> bytearray -> list
x = '53216A'  
y = bytearray.fromhex(x)  
print(type(y),y)
ay = binascii.b2a_hex(y)
print(type(ay),ay)
by = binascii.a2b_hex(ay)
print(type(by),by)

z = list(y) 
print(type(z),z)

"""
# not support in py3+
y = x.encode("hex");
print(y)
"""
 
# 如： [0x53, 0x21, 0x6A] -> '53216A'
# 方法：list -> bytearray -> str -> hexstring
x = [0x53, 0x21, 0x6A]  
y = bytearray(x)    ## 可变
z = binascii.b2a_hex(y) 
print(type(z),z)
z = binascii.hexlify(y) 
print(type(z),z)
y = binascii.unhexlify(z) 
print(type(y),y)







