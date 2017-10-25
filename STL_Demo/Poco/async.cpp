#include "Poco/Notification.h"  
#include "Poco/NotificationQueue.h"  
#include "Poco/ThreadPool.h"  
#include "Poco/Runnable.h"  
#include "Poco/AutoPtr.h"  
#include "Poco/Thread.h"
using Poco::Notification;  
using Poco::NotificationQueue;  
using Poco::ThreadPool;  
using Poco::Runnable;  
using Poco::AutoPtr;  

class WorkNotification: public Notification  
{  
public:  
    WorkNotification(int data): _data(data) {}  
    int data() const  
    {  
        return _data;  
    }  
private:  
    int _data;  
};  
  
  
class Worker: public Runnable  
{  
public:  
    Worker(NotificationQueue& queue): _queue(queue) {}  
    void run()  
    {  
        AutoPtr<Notification> pNf(_queue.waitDequeueNotification());  
        while (pNf)  
        {  
            WorkNotification* pWorkNf =  
                dynamic_cast<WorkNotification*>(pNf.get());  
            if (pWorkNf)  
            {  
                printf("hi!bingzhe");
            //    Sleep(100);
               Poco::Thread::sleep(200); 
            }  
            pNf = _queue.waitDequeueNotification();  
        }  
    }  
private:  
    NotificationQueue& _queue;  
};  



static void async_demo()
{
    NotificationQueue queue;  
    Worker worker1(queue); // create worker threads  
    Worker worker2(queue);  
    ThreadPool::defaultPool().start(worker1); // start workers  
    ThreadPool::defaultPool().start(worker2);  
    // create some work  
    for (int i = 0; i < 100; ++i)  
    {  
        queue.enqueueNotification(new WorkNotification(i));  
    }  
    while (!queue.empty()) // wait until all work is done  
        Poco::Thread::sleep(100);  
    queue.wakeUpAll(); // tell workers they're done  
    ThreadPool::defaultPool().joinAll();  
}

int main()
{
    async_demo();

    return 0;
}

