#include "Poco/Activity.h"  
#include "Poco/Thread.h"  
#include <iostream> 
using Poco::Thread;   // demo1

#include "Poco/ActiveMethod.h"
#include "Poco/ActiveResult.h"
#include <utility>

using Poco::ActiveMethod;
using Poco::ActiveResult;

class ActiveAdder
{
public:
    ActiveAdder(): add(this, &ActiveAdder::addImpl)
    {
    }

    ActiveMethod<int, std::pair<int, int>, ActiveAdder> add;

private:
    int addImpl(const std::pair<int, int>& args)
    {
        return args.first + args.second;
    }
};

static int  active_add()
{
    ActiveAdder adder;

    ActiveResult<int> sum = adder.add(std::make_pair(1, 2));
    // do other things
    sum.wait();
    std::cout << sum.data() << std::endl;

    return 0;
}

class ActivityExample  
{  
public:  
      ActivityExample(): _activity(this,   
         &ActivityExample::runActivity)  
      {}  
      void start()  
      {  
           _activity.start();  
      }  
      void stop()  
      {  
           _activity.stop(); // request stop  
           _activity.wait(); // wait until activity actually stops  
      }  
protected:  
    void runActivity()  
    {  
        while (!_activity.isStopped())  
        {  
            std::cout << "bingzhe running." << std::endl;  
            Thread::sleep(200);  
        }  
    }  
private:  
      Poco::Activity<ActivityExample> _activity;  
};  
  
static void thread_obj()
{
    ActivityExample example;  
    example.start();  
    Thread::sleep(2000);  
    example.stop(); 
    std::cout << "continus ...\n";
    example.start();
    Thread::sleep(1000);  
	example.stop();
}



int main(int argc, char** argv)  
{  
    active_add();
    thread_obj();
    
    return 0;  
}  