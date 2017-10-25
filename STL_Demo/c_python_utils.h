/***************************************************************************************************
c_python_utils.h
    C++ Network Library, Copyright (c) Datatom Software, Inc.(2015)

Author:
    liu.pan (liu.pan@datatom.com)
    
Creating Time:
    2015-5-4
***************************************************************************************************/
#ifndef _DTCORE_C_PYTHON_UTILS_H_
#define _DTCORE_C_PYTHON_UTILS_H_

#include <Python.h>
#include <stdio.h>

#ifdef __cplusplus
extern "C" {
#endif /* C++ */

/**
* 调用python类中的成员函数
* @param module python脚本名称，不含扩展
* @param class_name python类名称
* @param function python类成员函数
* @param format python类函数参数格式
* @return 返回字符串
*/
char* py_call( const char* module, const char* class_name, char* function, char* format, ... )
{
    PyObject* pName     = NULL;
    PyObject* pMod         = NULL;
    PyObject* pDict     = NULL;
    PyObject* pClass    = NULL;
    PyObject* pInstance = NULL;
    PyObject* pParam     = NULL;
    PyObject* pResult     = NULL;

    // 导入模块
    pName = PyString_FromString(module);
    pMod = PyImport_Import(pName);
    if( !pMod )
    {
        return "";
    }

    // 获取模块字典属性
    pDict = PyModule_GetDict(pMod);
    if ( !pDict )
    {
        return "";
    }

    // 通过字典获取模块中的类
    pClass = PyDict_GetItemString(pDict, class_name);
    if ( !pClass )
    {
        return "";
    }

    pInstance = PyInstance_New(pClass, NULL, NULL);
    if ( !pInstance )
    {
        return "";
    }

    pResult = PyObject_CallMethod(pInstance, function, format);
    
    char *rlt_ch = NULL;
    PyArg_Parse( pResult, "s", &rlt_ch );

    return rlt_ch;
}

/**
* 一些环境的初始化
* 
*/
void init()
{
    Py_Initialize();
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('./')");
}

/**
* 逆初始化
*/
void finit()
{
    Py_Finalize();
}

#ifdef __cplusplus
} /* extern "C" */
#endif /* C++ */

#endif  //_DTCORE_C_PYTHON_UTILS_H_