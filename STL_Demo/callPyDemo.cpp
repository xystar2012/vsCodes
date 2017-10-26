// python_c++.cpp : �������̨Ӧ�ó������ڵ㡣
//

//  undef Py_Debug    python27 OK

// #define PyString_FromString  PyBytes_FromString
#include "c_python_utils.h"

static int callPy1()
{
    // ��ʼ��Python
    Py_Initialize();
    // ����ʼ���Ƿ�ɹ�
    if (!Py_IsInitialized()) {
        return -1;
    }
    // ��ӵ�ǰ·��
    //��������ַ�����ΪPython����ֱ�����У�����0
    //��ʾ�ɹ���-1��ʾ�д����ʱ���������Ϊ�ַ��������﷨����
    PyRun_SimpleString("import sys");
    int result = PyRun_SimpleString("print('----------import sys-------')");
    if (result!=-1){
        printf("test pyhon OK!\n\n");
    }
    
    PyRun_SimpleString("sys.path.append('./bin')");
    PyRun_SimpleString("print(sys.path)");

    // ������Ϊpytest�Ľű�
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

    //��������ǲ��Һ���test ��ִ��test
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

    //�����ṹ��
    header input;
    memset(&input,0,sizeof(input));
    input.buf1 = 1;
    input.buf2 = 2;
    input.buf4 = 3;
    strcpy_s(input.buf3, "kjac");
    
    //�����byte*
    char * byInput = new char(sizeof(input));
    memcpy(byInput, &input, sizeof(input));

    //����python���
    PyObject *pArgs = PyTuple_New(1);
    //��python��ν��и�ֵ; s����char*��ʽ, #������ָ������
    PyTuple_SetItem(pArgs, 0, Py_BuildValue("s#", byInput, sizeof(input)));

    //ִ�к���
    PyObject *pResult = PyObject_CallObject(pFunc, pArgs);

    char* pRsp;
    //��ȡ����ֵ
    PyArg_Parse(pResult, "s", &pRsp);

    //ת�ɽṹ��
    header* pstRsp = (header*)pRsp;
    printf("\n-----------c++�����py����:buf1:%d,buf2:%d,buf3:%s,buf4:%d\n", 
    pstRsp->buf1, pstRsp->buf2, pstRsp->buf3, pstRsp->buf4);

    //�ͷ�
    Py_DECREF(pName);
    Py_DECREF(pArgs);
    Py_DECREF(pModule);

    // �ر�Python
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