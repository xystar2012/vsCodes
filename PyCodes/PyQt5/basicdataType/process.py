# -*- coding: utf-8 -*-
import shlex, subprocess


def callbat():
    try:
        #用wmi连接到远程服务器
        conn = wmi.WMI(computer=ipaddress, user=username, password=password)
        filename=r"D:\apps\autorun.bat"   #此文件在远程服务器上
        cmd_callbat=r"cmd /c call %s"%filename
        conn.Win32_Process.Create(CommandLine=cmd_callbat)  #执行bat文件
        print ("执行成功!")
    except Exception as e:
        print("bat exec error here:",e)

def callbatInSubProcess():
    child = subprocess.Popen(["ping","-c","5","www.baidu.com"])
    child.wait()
    print("parent process")

    out = subprocess.call(r"cmd /c for /?", shell=True)
    print(type(out),out)

    ret = subprocess.run(r"cmd /c dir", stdout=subprocess.PIPE)
    print(type(ret))
    print(type(ret.stdout),ret.stdout.decode('gbk'))
    # out = subprocess.call("cd ..", shell=True)


def proc_output1():
    
    p = subprocess.Popen(['ping', 'www.baidu.com', '-n' ,'11'], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    while True: 
        r = p.stdout.readline().strip().decode('gbk')
        if r:
            print(r)
        if subprocess.Popen.poll(p) != None and not r:
            break

def proc_input():
    command_line = r'cmd /c dir'  #input()
    args = shlex.split(command_line)
    print(args)
    p = subprocess.Popen(args, stdout=subprocess.PIPE) # Success!
    print(p.stdout.read())

if __name__=='__main__':
    proc_output1()
    
