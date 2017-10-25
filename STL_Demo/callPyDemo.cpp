// python_c++.cpp : 定义控制台应用程序的入口点。
//

//  undef Py_Debug    python27 OK

// #define PyString_FromString  PyBytes_FromString
#include "c_python_utils.h"

static int callPy1()
{
    // 初始化Python
    Py_Initialize();
    // 检查初始化是否成功
    if (!Py_IsInitialized()) {
        return -1;
    }
    // 添加当前路径
    //把输入的字符串作为Python代码直接运行，返回0
    //表示成功，-1表示有错。大多时候错误都是因为字符串中有语法错误。
    PyRun_SimpleString("import sys");
    int result = PyRun_SimpleString("print('----------import sys-------')");
    if (result!=-1){
        printf("test pyhon OK!\n\n");
    }
    
    PyRun_SimpleString("sys.path.append('./bin')");
    PyRun_SimpleString("print(sys.path)");

    // 载入名为pytest的脚本
    // PyObject *pName = PyBytes_FromString("pytest");
    PyObject *pName = PyString_FromString("pytest");
    PyObject *pModule = PyImport_Import(pName);
    if (!pModule) 
    {
        printf("can't find pytest.py");
        getchar();
        return -1;
    }

    PyObject *pDict = PyModule_GetDict(pModule);
    if (!pDict) {
        getchar();
        return -1;
    }

    //下面这段是查找函数test 并执行test
    PyObject *pFunc = PyDict_GetItemString(pDict, "test");
    if (!pFunc || !PyCallable_Check(pFunc)) {
        printf("can't find function [test2]");
        getchar();
        return -1;
    }

    typedef struct header_ {
        int buf1;
        int buf2;
        char buf3[11];
        int buf4;
    }header;

    //创建结构体
    header input;
    memset(&input,0,sizeof(input));
    input.buf1 = 1;
    input.buf2 = 2;
    input.buf4 = 3;
    strcpy_s(input.buf3, "kjac");
    
    //打包成byte*
    char * byInput = new char(sizeof(input));
    memcpy(byInput, &input, sizeof(input));

    //申请python入参
    PyObject *pArgs = PyTuple_New(1);
    //对python入参进行赋值; s代表char*格式, #代表传入指定长度
    PyTuple_SetItem(pArgs, 0, Py_BuildValue("s#", byInput, sizeof(input)));

    //执行函数
    PyObject *pResult = PyObject_CallObject(pFunc, pArgs);

    char* pRsp;
    //获取返回值
    PyArg_Parse(pResult, "s", &pRsp);

    //转成结构体
    header* pstRsp = (header*)pRsp;
    printf("\n-----------c++层接收py返回:buf1:%d,buf2:%d,buf3:%s,buf4:%d\n", 
    pstRsp->buf1, pstRsp->buf2, pstRsp->buf3, pstRsp->buf4);

    //释放
    Py_DECREF(pName);
    Py_DECREF(pArgs);
    Py_DECREF(pModule);

    // 关闭Python
    Py_Finalize();
}


static void callPy2()
{
    init();
    char* rlt_char = py_call("hello", "power", "liupan", "()");
    finit();

    printf("%s\n", rlt_char);
}

int main()
{
    callPy1();
    // callPy2();
    system("pause");
    return 0;
}