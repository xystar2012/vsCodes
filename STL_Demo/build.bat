@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" x86   
set incPaths=/I"D:\local\boost_1_64_0"  
REM MD MT 多线程 动态 静态C运行库
set compilerflags=/Od /Zi /EHsc  %incPaths% /D "WIN32"  /MD
set fileBasename=%1%
if not exist bin;md bin
set libPath="D:\local\boost_1_64_0\lib32-msvc-12.0"
set libs="ws2_32.lib" 
set obj=bin/%fileBasename%.exe
REM /NODEFAULTLIB:library
set linkerflags=/OUT:%obj% /MACHINE:X86 /LIBPATH:%libPath% /DYNAMICBASE %libs%
cl.exe %compilerflags%  %fileBasename%.cpp /link %linkerflags%