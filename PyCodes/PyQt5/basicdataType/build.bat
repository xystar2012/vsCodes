@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" x86
REM 输出无换行
set /p="projectFile:%1% " < nul  
set /p="args:%2% " < nul  
echo  %3% 
set fileBasename=%1%
set buildType=%2%
set binType=%3%
devenv  %fileBasename%  %buildType%  %binType%