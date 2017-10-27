#include <stdlib.h>  
#include <stdio.h>

// Boost
#include <boost/array.hpp>  // for boost array
#include <boost/tuple/tuple.hpp>  // for boost tuple
#include <boost/algorithm/string.hpp>  // for join split
#include <boost/tokenizer.hpp>  // for boost token
#include "boost/filesystem/path.hpp"
#include "boost/filesystem/operations.hpp"
#include "boost/filesystem.hpp"
#include "boost/timer.hpp"


// STL
#include <iostream>
#include <string>
#include <set>  // for std::set
#include <algorithm>  //如果要使用算法函数，你必须要包含这个头文件。
#include <numeric>  // 包含accumulate（求和）函数的头文件
#include <vector>
#include <fstream>
#include <limits>
using namespace std;

#include <windows.h>  // forWindows

static  void boostArry()
{
    boost::array<std::string,4> seasons = 
    {
        { "spring", "summer", "autumn", "winter" }

    };

    boost::array<std::string,4>::const_iterator pos;
    boost::array<std::string,4>::reverse_iterator reverse_pos;

    for(pos=seasons.begin();pos!=seasons.end();++pos)
    {
       std::cout<<*pos<<'\n';
    }

    for(reverse_pos=seasons.rbegin(); reverse_pos< seasons.rend(); ++reverse_pos)
    {
       std::cout<<*reverse_pos<<'\n';
    }

}

static void test_string_tokenizer()  
{  
    using namespace boost;  

    /*
        foreach
        for(tokenizer<>::iterator beg=tok.begin(); beg!=tok.end();++beg){ 
         cout << *beg << " "; 

    */
  
    // 1. 使用缺省模板参数创建分词对象, 默认把所有的空格和标点作为分隔符.   
    {  
        std::string str("Link raise the master-sword.");  
  
        tokenizer<> tok(str);  
        for (auto pos : tok)  
            std::cout << "[" << pos << "]";  
        std::cout << std::endl;  
        // [Link][raise][the][master][sword]  
    }  
  
    // 2. char_separator()  
    {  
        std::string str("Link raise the master-sword.");  
  
        // 一个char_separator对象, 默认构造函数(保留标点但将它看作分隔符)  
        char_separator<char> sep;  
        tokenizer<char_separator<char> > tok(str, sep);  
        for (auto pos : tok)  
            std::cout << "[" << pos << "]";  
        std::cout << std::endl;  
        // [Link][raise][the][master][-][sword][.]  
    }  
  
    // 3. char_separator(const Char* dropped_delims,  
    //                   const Char* kept_delims = 0,   
    //                   empty_token_policy empty_tokens = drop_empty_tokens)  
    {  
        std::string str = ";!!;Hello|world||-foo--bar;yow;baz|";  
  
        char_separator<char> sep1("-;|");  
        tokenizer<char_separator<char> > tok1(str, sep1);  
         for (auto pos : tok1)  
            std::cout << "[" << pos << "]";  
        std::cout << std::endl;  
        // [!!][Hello][world][foo][bar][yow][baz]  
  
        char_separator<char> sep2("-;", "|");  // , keep_empty_tokens  
        tokenizer<char_separator<char> > tok2(str, sep2);  
         for (auto pos : tok2)  
            std::cout << "[" << pos << "]";  
        std::cout << std::endl;  
        // [][!!][Hello][|][world][|][][|][][foo][][bar][yow][baz][|][]  
    }  
  
    // 4. escaped_list_separator  
    {  
        std::string str = "Field 1,\"putting quotes around fields, allows commas\",Field 3";  
        // 下面三个字符做为分隔符: '\', ',', '"'
        tokenizer<escaped_list_separator<char> > tok(str);  
        for (auto pos : tok)  
            std::cout << "[" << pos << "]";  
        std::cout << std::endl;  
        // [Field 1][putting quotes around fields, allows commas][Field 3]  
        // 引号内的逗号不可做为分隔符.  
    }  
      
    // 5. offset_separator  
    {  
        std::string str = "12252001400";  
  
        int offsets[] = {2, 2, 4};  
        offset_separator f(offsets, offsets + 3,false,false);  
        tokenizer<offset_separator> tok(str, f);  
  
         for (auto pos : tok)    
            std::cout << "[" << pos << "]";  
        std::cout << std::endl;  
    }  
}  

static void boostSplitJoin()
{
    using namespace boost::algorithm;
    string strIn = "this is for test";
    vector<string> strRet;
    split(strRet,strIn,is_space());
    strIn = join(strRet,"+");
    std::copy(strRet.begin(),strRet.end(),ostream_iterator<string>(cout,"\t"));

    cout <<"\n" <<  strIn << endl;
}

static void testSTDSet()
{
    using namespace std;
    set <string> strset;
    set <string>::iterator si;
    strset.insert("cantaloupes");
    strset.insert("apple");
    strset.insert("orange");
    strset.insert("banana");
    strset.insert("grapes");
    strset.insert("grapes");  
    std::copy(strset.begin(),strset.end(),ostream_iterator<string>(cout,"\n"));
    // 输出： apple banana cantaloupes grapes orange
    //注意：输出的集合中的元素是按字母大小顺序排列的，而且每个值都不重复。

    cout << endl;
}

void splitString()
{
    using namespace std;
    vector<string> strRet;
    string strSrc = "are you ok ?. ";

    int nPos = 0;
    do
    {
        nPos = strSrc.find(" ");
        if(nPos != -1)
        {
            strRet.push_back(strSrc.substr(0,nPos));
            strSrc.erase(0,nPos + 1);
        }
        
    }while(nPos != std::string::npos);
    
    strRet.push_back(strSrc);

    copy(strRet.begin(),strRet.end(),ostream_iterator<string>(cout,"\t"));
    cout << endl;
}

static void boostFs()
{
    namespace fs = boost::filesystem;
	boost::timer t;

	cout << "max timespan: " << t.elapsed_max() / 3600 << "h" << endl;
	cout << "min timespan: " << t.elapsed_min() << "s" << endl;
	cout << "now time elapsed: " << t.elapsed() << "s" << endl;
	
 	boost::filesystem::path p("c:/xystar/pics");
 	for (boost::filesystem::directory_iterator item_begin(p); item_begin != boost::filesystem::directory_iterator(); item_begin++)
 	{
 		if (boost::filesystem::is_regular_file(*item_begin))
 		{
 			std::wstring name = item_begin->path().filename().wstring();
 			std::wcout << name << std::endl;
 		}
 	}
}

int main(void)
{
    //fileCheck();
    //splitString();
    //testSTDSet();
    // boostFs();
    boostSplitJoin();
    boostArry();
    test_string_tokenizer();

    return 0;
}

