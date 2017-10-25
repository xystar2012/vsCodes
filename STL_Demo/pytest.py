import struct

def test(a):
    print("----------------------------python 1-----------------------")
    ret = struct.unpack('ii11si', a)
    print("----------------------------python deal-----------------------")
    print("--------------------python receive c++ struct:")
    print("begin unpack:")
    print("")
    print(ret)
    buf1 = ret[0] + 1
    buf2 = ret[1] + 1
    buf4 = ret[3] + 1
    print("--------------------begin pack data and begin send to c++")
    print("")
    bin_buf_all = struct.pack('ii11si', buf1, buf2, "dfds", buf4)
    print("----------------------------python end-----------------------")
    return bin_buf_all