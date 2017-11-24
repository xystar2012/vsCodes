#include <iostream>
#include <locale>
#include <sstream>
#include <codecvt>
#include <time.h>
#include <sys/timeb.h>
#include <thread>
#include <chrono>
#include <iomanip>

using std::chrono::milliseconds;

struct csv_whitespace : std::ctype<wchar_t>
{
    bool do_is(mask m, char_type c) const
    {   
        if ((m & space) && c == L' ') {
            return false; // space will NOT be classified as whitespace
        }
        if ((m & space) && c == L',') {
            return true; // comma will be classified as whitespace
        }
        return ctype::do_is(m, c); // leave the rest to the parent class
    } 
};

static void newSplit()
{
    std::wstring in = L"Column 1,Column 2,Column 3\n123,456,789";
    std::wstring token;
 
    std::wcout << "default locale:\n";
    std::wistringstream s1(in);
    while (s1 >> token) {
        std::wcout << "  " << token << '\n';
    }
 
    std::wcout << "locale with modified ctype:\n";
    std::wistringstream s2(in);
    csv_whitespace* my_ws = new csv_whitespace; // note: this allocation is not leaked
    s2.imbue(std::locale(s2.getloc(), my_ws));
    while (s2 >> token) {
        std::wcout << "  " << token<< '\n';
    }
}

static void localConstruct()
{
    std::locale loc(std::locale(), new std::ctype<char>);
    std::cout << "The default locale is " << std::locale().name() << '\n'
              << "The user's locale is " << std::locale("").name() << '\n'
              << "A nameless locale is " << loc.name() << '\n';


    std::locale l1;  // l1 is a copy of the classic "C" locale
    // en_US.UTF8
    std::locale l2(std::locale("").name()); // l2 is a unicode locale
    
    // template <class charT>
    // class ctype : public locale::facet, public ctype_base
    std::locale l3(l1, l2, std::locale::ctype); // l3 is "C" except for ctype, which is unicode

    // template <class internT, class externT, class stateT>
    //class codecvt : public locale::facet, public codecvt_base
    std::locale l4(l1, new std::codecvt_utf8<wchar_t>); // l4 is "C" except for codecvt
    std::cout << "Locale names:\nl1: " << l1.name() << "\nl2: " << l2.name()
               << "\nl3: " << l3.name() << "\nl4: " << l4.name() << '\n';

}


// minimal custom facet
struct myfacet : public std::locale::facet {
    static std::locale::id id;
};
 
std::locale::id myfacet::id;
 
static void newLoacal()
{
    // loc is a "C" locale with myfacet added
    std::locale loc(std::locale::classic(), new myfacet);
    std::cout << std::boolalpha
              << "Can loc classify chars? "
              << std::has_facet<std::ctype<char>>(loc) << '\n'
              << "Can loc classify char32_t? "
              << std::has_facet<std::ctype<char32_t>>(loc) << '\n'
              << "Does loc implement myfacet? "
              << std::has_facet<myfacet>(loc) << '\n';
}


// struct   timeb{
//     time_t   time;                      /* 为1970-01-01至今的秒数*/
//     unsigned   short   millitm;   /* 千分之一秒即毫秒 */
//     short   timezonel;               /* 为目前时区和Greenwich相差的时间，单位为分钟 */
//     short   dstflag;                   /* 为日光节约时间的修正状态，如果为非0代表启用日光节约时间修正 */
// };

static void millSec()
{
    struct timeb tb;
    int nLoop = 0;

    do
    {
        ftime(&tb);
        printf("UTC:   %s", asctime(gmtime(&tb.time)));
        printf("local: %s", asctime(localtime(&tb.time)));
        printf(".%03d\n",tb.millitm);
        std::this_thread::sleep_for(milliseconds(1000*1 + nLoop*10));
        char mbstr[100];
        if (std::strftime(mbstr, sizeof(mbstr), "%T ", std::localtime(&tb.time))) {
            std::cout << mbstr << '\n';
        }
    
    }while(++nLoop < 10);
}

void static clockTest()
{
    std::function<void ()> f = []()
    {
        volatile double d = 0;
        for(int n=0; n<10000; ++n)
           for(int m=0; m<10000; ++m)
               d += d*n*m;
    };

    std::clock_t c_start = std::clock();
    auto t_start = std::chrono::high_resolution_clock::now();
    std::thread t1(f);
    std::thread t2(f); // f() is called on two threads
    t1.join();
    t2.join();
    std::clock_t c_end = std::clock();
    auto t_end = std::chrono::high_resolution_clock::now();
 
    std::cout << std::fixed << std::setprecision(2) << "CPU time used: "
              << 1000.0 * (c_end-c_start) / CLOCKS_PER_SEC << " ms\n"
              << "Wall clock time passed: "
              << std::chrono::duration<double, std::milli>(t_end-t_start).count()
              << " ms\n";
}

int main()
{
    // clockTest();
    millSec();
    newLoacal();
    newSplit();
    localConstruct();

    system("pause");

    return 0;
}