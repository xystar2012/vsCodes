#include "Poco/NotificationCenter.h"  
#include "Poco/Notification.h"  
#include "Poco/Observer.h"  
#include "Poco/NObserver.h"  
#include "Poco/AutoPtr.h"  
#include <iostream>  
using Poco::NotificationCenter;  
using Poco::Notification;  
using Poco::Observer;  
using Poco::NObserver;  
using Poco::AutoPtr;  
class BaseNotification: public Notification  
{  
public: void dosome(){
        printf("fuck!");
    }
};  
class SubNotification: public BaseNotification  
{  

};  
  
  
class Target  
{  
public:  
    void handleBase(BaseNotification* pNf)  
    {  
        std::cout << "handleBase: " << pNf->name() << std::endl;  
        pNf->dosome();
        pNf->release(); // we got ownership, so we must release  
    }  
    void handleSub(const AutoPtr<SubNotification>& pNf)  
    {  
        std::cout << "handleSub: " << pNf->name() << std::endl;  
    }  
};  
  
static void notify_bug()
{
    NotificationCenter nc;  
    Target target;  
    nc.addObserver(  
        Observer<Target, BaseNotification>(target, &Target::handleBase)  
        );  
    nc.addObserver(  
        NObserver<Target, SubNotification>(target, &Target::handleSub)  
        );  
    nc.postNotification(new BaseNotification);  
    nc.postNotification(new SubNotification);  
    nc.removeObserver(  
        Observer<Target, BaseNotification>(target, &Target::handleBase)  
        );  
    nc.removeObserver(  
        NObserver<Target, SubNotification>(target, &Target::handleSub)  
        );  
}

#include "Poco/BasicEvent.h"
#include "Poco/Delegate.h"

using Poco::BasicEvent;
using Poco::Delegate;

class Source
{
public:
    BasicEvent<int> theEvent;

    void fireEvent(int n)
    {
        theEvent(this, n);
    }
};

class TargetEvt
{
public:
    void onEvent(const void* pSender, int& arg)
    {
        std::cout << "onEvent: " << arg << std::endl;
    }
};

static void fireEvt()
{
    Source source;
    TargetEvt target;

    source.theEvent += Delegate<TargetEvt, int>(
        &target, &TargetEvt::onEvent);

    source.fireEvent(42);
    source.fireEvent(12);

    source.theEvent -= Delegate<TargetEvt, int>(
        &target, &TargetEvt::onEvent);
    
    source.fireEvent(22);
}

  
int main(int argc, char** argv)  
{  
    fireEvt();
    notify_bug();

    return 0;  
}  