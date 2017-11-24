import os,sys

rootdir = './'                                # 指明被遍历的文件夹

def findAllFiles():
    for parent,dirnames,filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for dirname in  dirnames:                       #输出文件夹信息
            print ("parent is:" , parent)
            print ("dirname is" , dirname)

        for filename in filenames:                        #输出文件信息
            print ("parent is:" , parent)
            print ("filename is:", filename)
            print ("the full name of the file is:" , os.path.join(parent,filename)) #输出文件路径信息
        break


def curPath():
    print ("__file__=%s" % __file__)
    print ("os.path.realpath(__file__)=%s" % os.path.realpath(__file__))
    print ("os.path.dirname(os.path.realpath(__file__))=%s" % os.path.dirname(os.path.realpath(__file__)))
    print (r"os.path.split(os.path.realpath(__file__))=%s" % os.path.split(os.path.realpath(__file__))[0] )
    print ("os.path.abspath(__file__)=%s" % os.path.abspath(__file__))
    print ("os.getcwd()=%s" % os.getcwd())
    print ("sys.path[0]=%s" % sys.path[0])
    print ("sys.argv[0]=%s" % sys.argv[0])
    path = sys.path[0]
    print('listdir:' + '-*-'*30)
    for file in os.listdir(path):
        print(os.path.join(path,file))

def curPath():
    fullPath = os.path.realpath(sys.argv[0])
    print(os.curdir,os.sep,os.pardir)
    print(os.defpath,os.devnull)
    print(os.urandom(10))
    print(__file__,sys.path[0])
    print(sys.argv[0],fullPath)
    filename = os.path.basename(fullPath)
    nameNoExt = os.path.splitext(filename)
    print(filename,nameNoExt)

def findAllFilesQuick(path = '.'):
    for entry in os.scandir(path):
        if not entry.name.startswith('.') and entry.is_file():
            print(entry.name)


if __name__=="__main__":
    curPath()
    findAllFilesQuick()
    print('findAllFiles:' + '-*-'*30)
    findAllFiles()
    