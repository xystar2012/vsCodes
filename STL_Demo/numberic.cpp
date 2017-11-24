// STL
#include <iostream>
#include <string>
#include <set>  // for std::set
#include <algorithm>  //如果要使用算法函数，你必须要包含这个头文件。
#include <numeric>  // 包含accumulate（求和）函数的头文件
#include <vector>
#include <fstream>
#include <limits>
#include <map>
#include <codecvt>
#include <stdint.h>
#include <type_traits>
#include <assert.h>

using namespace std;

static void sizeofOper()
{
    struct Empty {};
    struct Base { int a; };
    struct Derived : Base { int b; };
    struct Bit { unsigned bit: 1; };

    Empty e;
    Derived d;
    Base& b = d;
    Bit bit;
    int a[10];
    std::cout << "size of empty class: "              << sizeof e          << '\n'
              << "size of pointer : "                 << sizeof &e         << '\n'
//            << "size of function: "                 << sizeof(void())    << '\n'  // error
//            << "size of incomplete type: "          << sizeof(int[])     << '\n'  // error
//            << "size of bit field: "                << sizeof bit.bit    << '\n'  // error
              << "size of array of 10 int: "          << sizeof(int[10])   << '\n'
              << "size of array of 10 int (2): "      << sizeof a          << '\n'
              << "length of array of 10 int: "        << ((sizeof a) / (sizeof *a)) << '\n'
              << "length of array of 10 int (2): "    << ((sizeof a) / (sizeof a[0])) << '\n'
              << "size of the Derived: "              << sizeof d          << '\n'
              << "size of the Derived through Base: " << sizeof b          << '\n';

              #define MAX_CAMERA_NUM 4

                typedef struct {
                    unsigned short pixel_x;		//Line resolution
                    unsigned short pixel_y;		//Column resolution
                    unsigned short frame_rate;	//frame rate
                    unsigned short color_depth;	//color deepth
                    unsigned int total_frame;	//total frame
                    char recd_start_time[14];		//exp start time,20150716152510
                    char recd_end_time[14];
                }ccd_exp_info;

              typedef struct exp_info
              {
                char exp_name[48];			//exp name, "TASK0001_RECD0001_check"
                char task_start_time[14];	//20150716152510
                char task_end_time[14];		//20150716152510, if has no end_time, 00000000000000
                unsigned int pack;			//
                unsigned int image_type;	//0:normal task; 1:off-line horizontal; 2:off-line vertical;
                unsigned int raid;			//0:RAID0; 1:RAID1
                unsigned int disk_bitmap;	//disk bitmap each byte represent one ccd
                ccd_exp_info _ccd_exp_info[MAX_CAMERA_NUM];
              }exp_info;

              cout << sizeof(long) << " ccd_exp_info:" << sizeof(ccd_exp_info) << " exp_info:" << sizeof (exp_info) << std::endl;
              
}

namespace vpxStruct {
    #define MAX_CHANNEL_NUM 4
    typedef struct {
        unsigned short head_size;		//frame head size;
        unsigned long		data_size;		//frame data size;
        unsigned int total_frame;	//total frame
        char recd_start_time[14];		//exp start time,20150716152510
        char recd_end_time[14];			//exp start time,20150716152510, if has no end_time, 00000000000000
    }ccd_exp_info;

    //detail info of each record, support 4 cameras at most
    typedef struct
    {
        char exp_name[50];			//exp name, "TASK0001_RECD0001_check"
        char task_start_time[14];	//20150716152510
        char task_end_time[14];		//20150716152510, if has no end_time, 00000000000000
        unsigned int pack;			//
        unsigned int image_type;	//0:normal task; 1:off-line horizontal; 2:off-line vertical;
        unsigned int raid;			//0:RAID0; 1:RAID1
        unsigned int disk_bitmap[MAX_CHANNEL_NUM];	//disk bitmap each byte represent one ccd
        ccd_exp_info _ccd_exp_info[MAX_CHANNEL_NUM];
    }exp_info;
}

static void sizeofRecChannel()
{
    cout <<"vpxccdInfo:" << sizeof (vpxStruct::ccd_exp_info) <<"RecChannelsize:" << sizeof (vpxStruct::exp_info) << std::endl;
}


static void isConvert()
{
    class A {};
    class B : public A {};
    class C {};
 
    bool b2a = std::is_convertible<B*, A*>::value;
    bool a2b = std::is_convertible<A*, B*>::value;
    bool b2c = std::is_convertible<B*, C*>::value;
 
    std::cout << std::boolalpha;
    std::cout << b2a << '\n';
    std::cout << a2b << '\n';
    std::cout << b2c << '\n';
}

static void limit()
{
    long data = -1;

    cout << hex;
    cout << "-1 data:" << data;
    cout << "sizeof int:" << sizeof(int) << " max int:" <<(std::numeric_limits<int>::max)() << endl;
    cout << "sizeof uint32_t:" << sizeof(int32_t) << " max int:" <<(std::numeric_limits<int32_t>::max)() << endl;
    cout << "sizeof long:" << sizeof(long) << " max int:" <<(std::numeric_limits<long>::max)() << endl;
    cout << "sizeof uint64_t:" << sizeof(uint64_t) << " max int:" <<(std::numeric_limits<uint64_t>::max)() << endl;
    cout << "sizeof uint32_t:" << sizeof(uint32_t) << " max int:" <<(std::numeric_limits<uint32_t>::max)() << endl;
    cout << "sizeof int8_t:" << sizeof(int8_t) << " max int8_t:" <<(std::numeric_limits<int8_t>::max)() << endl;
    int8_t n = 0x90;
    char szData[16] = {0};
    
    sprintf(szData,"%d",(uint8_t)n);
    cout << n << " szData:" << szData << endl;
}


static void mapDemo()
{
    map<int,string> mapData;
    mapData[1] = ("How");
    mapData[2] = ("Are");
    mapData[3] = ("You");
    mapData.insert(std::pair<int,string>(4,"Today"));
    //mapData.push_back(std::pair<int,string>(5,"Now"));
   for(auto it :mapData)
   {
        cout << it.first << ","  << it.second << endl;
   }

    auto tmp = mapData.erase(mapData.begin());
    //mapData.erase(mapData.rbegin());
    cout << tmp->first << ","  << tmp->second << endl;

    cout << "==============" <<endl;

    for_each(mapData.begin(),mapData.end(),[](std::pair<int,string> it)
    {
        cout << it.first << ","  << it.second << endl; 
    });
}

#define DATA_SIZE(column,line,bits) ((column)*(line)*(bits)/8)
#define FRAME_SIZE(column,line,bits) (((((column)*(line)*(bits)/8 + 128) >> 9) + 1) << 9)
#define HEAD_SIZE(column,line,bits) ( FRAME_SIZE(column,line,bits)- DATA_SIZE(column,line,bits))


void static getHeadSize()
{
    cout <<"Head:"  
        << HEAD_SIZE(640,512,8) << " "
        << HEAD_SIZE(1024,1024,8) << " "
        << HEAD_SIZE(2048,2048,8)<< endl;

    assert(true);  // 对错误表达式检测
}

int main()
{
    getHeadSize();
    // limit();
    isConvert();
    sizeofOper();
    sizeofRecChannel();

    return 0;
}