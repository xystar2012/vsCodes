#include "Poco/Poco.h"
#include "Poco/String.h"  
#include "Poco/NumberFormatter.h"  //// not ok
#include "Poco/Format.h"  
#include <vector> 

using namespace Poco;

static void str_cat()
{
    std::vector<std::string> colors;  
    colors.push_back("red");  
    colors.push_back("green");  
    colors.push_back("blue");  
    std::string s;  
    s = Poco::cat(std::string(", "), colors.begin(), colors.end());// "red, green, blue"  

    std::string hello(" Hello, world! ");  
    std::string s1(trimLeft(hello)); // "Hello, world! "  
    trimRightInPlace(s1);// "Hello, world!"  
    std::string s2(trim(hello));// "Hello, world!"  
}

#include "Poco/StringTokenizer.h"
using Poco::StringTokenizer;

static void str_token()
{
    std::string tokens = "white; black; magenta, blue, green; yellow";
	StringTokenizer tokenizer(tokens, ";,", StringTokenizer::TOK_TRIM);
	for (StringTokenizer::Iterator it = tokenizer.begin(); it != tokenizer.end(); ++it)
	{
		std::cout << *it << std::endl;
	}
}

static void str_format()
{
    using Poco::format;  

    std::string s;  
    int n = 42;  

    format(s, "The answer to life, the universe and everything is %d", n);  
    s = format("%d + %d = %d", 2, 2, 4); // "2 + 2 = 4"  
    s = format("%4d", 42);// " 42"  
    s = format("%-4d", 42);// "42 "  
    format(s, "%d", std::string("foo")); // "[ERRFMT]"  
}

#include "Poco/Timer.h"  
#include "Poco/Thread.h"  
using Poco::Timer;  
using Poco::TimerCallback;  
  
class TimerExample  
{  
    public:  
    void onTimer(Poco::Timer& timer)  
    {  
        std::cout << "onTimer called." << std::endl;  
    }  
};  


static void timer_demo()
{
    TimerExample te;  
    Timer timer(250, 500); // fire after 250ms, repeat every 500ms  
    timer.start(TimerCallback<TimerExample>(te, &TimerExample::onTimer));  
    Thread::sleep(5000);  
    timer.stop();  
}

#include "Poco/MemoryPool.h"  
using Poco::MemoryPool;  

static void mempool()
{
    MemoryPool pool(1024); // unlimited number of 1024 byte blocks  
    // MemoryPool pool(1024, 4, 16); // at most 16 blocks; 4 preallocated  
    char* buffer = reinterpret_cast<char*>(pool.get());  
    std::cin.read(buffer, pool.blockSize());  
    std::streamsize n = std::cin.gcount();  
    std::string s(buffer, n);  
    pool.release(buffer);  
    
    std::cout << s << std::endl;  
}

#include "Poco/Process.h" 
#include "Poco/PipeStream.h" 
#include "Poco/StreamCopier.h" 
#include <fstream> 

using Poco::Process; 
using Poco::ProcessHandle; 

static void doCmd()
{
    std::string cmd("cmd"); 
    std::vector<std::string> args;
    args.push_back("\/c");
    args.push_back("for"); 
    args.push_back("\/?");
    Poco::Pipe outPipe; 
    ProcessHandle ph = Process::launch(cmd, args, 0, &outPipe, 0); 
    Poco::PipeInputStream istr(outPipe); 
    std::ofstream ostr("processes.txt"); 
    Poco::StreamCopier::copyStream(istr, ostr); 
}


#include "Poco/LocalDateTime.h"
#include "Poco/DateTime.h"
#include "Poco/DateTimeFormat.h"
#include "Poco/DateTimeFormatter.h"
#include "Poco/DateTimeParser.h"

using Poco::LocalDateTime;
using Poco::DateTime;
using Poco::DateTimeFormat;
using Poco::DateTimeFormatter;
using Poco::DateTimeParser;

static void dataTime()
{
    LocalDateTime now;
	
	std::string str = DateTimeFormatter::format(now, DateTimeFormat::ISO8601_FORMAT);
	DateTime dt;
	int tzd;
	DateTimeParser::parse(DateTimeFormat::ISO8601_FORMAT, str, dt, tzd);
	dt.makeUTC(tzd);
	LocalDateTime ldt(tzd, dt);
}

#include "Poco/DirectoryIterator.h"
#include "Poco/File.h"
#include "Poco/Path.h"
#include "Poco/DateTimeFormatter.h"
#include "Poco/DateTimeFormat.h"
#include "Poco/Exception.h"

using Poco::DirectoryIterator;
using Poco::File;
using Poco::Path;
using Poco::DateTimeFormatter;
using Poco::DateTimeFormat;

static void dir_test()
{
    std::string dir;

	dir = Path::current();	
	try
	{
		DirectoryIterator it(dir);
		DirectoryIterator end;
		while (it != end)
		{
			Path p(it->path());
			std::cout << (it->isDirectory() ? 'd' : '-')
					  << (it->canRead() ? 'r' : '-')
					  << (it->canWrite() ? 'w' : '-')
					  << ' '
					  << DateTimeFormatter::format(it->getLastModified(), DateTimeFormat::SORTABLE_FORMAT)
					  << ' '
					  << p.getFileName()
					  << std::endl;
			++it;
		}
	}
	catch (Poco::Exception& exc)
	{
		std::cerr << exc.displayText() << std::endl;
		return ;
	}
}

int main(int argc, char** argv)  
{  
    dir_test();
    dataTime();
    str_token();
    str_format();
    str_cat();
    // timer_demo();
    // mempool();
    doCmd();

    return 0;  
}  