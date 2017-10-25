#include <functional>
#include <iostream>
#include <stdint.h>
#include <tuple>
#include <vector>
#include <mutex>
#include <thread>
#include <sstream>
#include <chrono>
#include "./Cpp11-decltype.h"

using namespace std;

std::mutex cout_mutex; // control access to std::cout
std::timed_mutex mutex;


void job(int id) 
{
    using Ms = std::chrono::milliseconds;
    std::ostringstream stream;
 
    // for (int i = 0; i < 3; ++i) {
    //     if (mutex.try_lock_for(Ms(100))) {
    //         stream << "success ";
    //         std::this_thread::sleep_for(Ms(100));
    //         mutex.unlock();
    //     } else {
    //         stream << "failed ";
    //     }
    //     std::this_thread::sleep_for(Ms(100));
    // }
 
    std::lock_guard<std::mutex> lock(cout_mutex);
    std::cout << "[" << id << "] " << stream.str() << "\n";
}

static void testLock()
{
    std::vector<std::thread> threads;
    for (int i = 0; i < 4; ++i) {
        threads.emplace_back(job, i);
    }
    
    for (auto& i: threads) {
        i.join();
    }
}


static void tryLock()
{
    int foo_count = 0;
    std::mutex foo_count_mutex;
    int bar_count = 0;
    std::mutex bar_count_mutex;
    int overall_count = 0;
    bool done = false;
    std::mutex done_mutex;
 
    auto increment = [](int &counter, std::mutex &m,  const char *desc) {
        for (int i = 0; i < 10; ++i) {
            std::unique_lock<std::mutex> lock(m);
            ++counter;
            std::cout << desc << ": " << counter << '\n';
            lock.unlock();
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }
    };
 
    std::thread increment_foo(increment, std::ref(foo_count), 
        std::ref(foo_count_mutex), "foo");
    std::thread increment_bar(increment, std::ref(bar_count), 
        std::ref(bar_count_mutex), "bar");
 
    std::thread update_overall([&]() {
        done_mutex.lock();
        while (!done) {
            done_mutex.unlock();
            int result = std::try_lock(foo_count_mutex, bar_count_mutex);
            if (result == -1) {
                overall_count += foo_count + bar_count;
                foo_count = 0;
                bar_count = 0;
                std::cout << "overall: " << overall_count << '\n';
                foo_count_mutex.unlock();
                bar_count_mutex.unlock();
            }
            std::this_thread::sleep_for(std::chrono::seconds(2));
            done_mutex.lock();
        }
        done_mutex.unlock();
    });
 
    increment_foo.join();
    increment_bar.join();
    done_mutex.lock();
    done = true;
    done_mutex.unlock();
    update_overall.join();
 
    std::cout << "Done processing\n"
              << "foo: " << foo_count << '\n'
              << "bar: " << bar_count << '\n'
              << "overall: " << overall_count << '\n';
}

static void c11Test()
{
    string strTest = "test string";
    int nLoop = 10;
    std::thread t1([&]()->int
    {
        do{
            nLoop--;
           // sleep(100);
            std::cout << "sleep:" << nLoop << std::endl;
            continue;
            nLoop-= 2;

        }while(nLoop > 0);

        return 0;
    });

    t1.join();

    std::function<int (int,int)> pf = [](int a,int b)->int
    {
        return a + b;
    };

    std::cout << pf(3,3) << endl;

    return;
}

static void offset()
{
    float foclen = 100.567;
    uint32_t dwFoc = 0;
    
    std::function<tuple<int,int>(uint32_t)> bitPf = [](uint32_t data) ->tuple<int,int> {
        int ret = (data & (0x1 << 31)) ? -1 : 1;
        int value = ret*(data & 0x7FFFFFFF);
        return std::make_tuple(ret,value);
    };

    memcpy(&dwFoc, &foclen, 4);
    memcpy(&foclen, &dwFoc, 4);

    std::cout << sizeof(float) << ",dwFoc:" << dwFoc << " floatValue:" << float(dwFoc)
              << " OrgValue:" << foclen << std::endl;

    uint32_t ndata1 = 0x8fffffff;
    uint32_t ndata2 = 0x7fffffff;

    cout << hex;
    cout << ndata1 << " ret:" << dec << std::get<0>(bitPf(ndata1)) << hex << " " << std::get<1>(bitPf(ndata1))
    << " " << ndata2 << " ret:" << dec << std::get<0>(bitPf(ndata2)) << hex <<" " << std::get<1>(bitPf(ndata2)) <<endl;

    
}


int main()
{
    tryLock();
    testLock();
    // testTuple();
    // testTypeID();

    // offset();
    // c11Test();

    return 0;
}