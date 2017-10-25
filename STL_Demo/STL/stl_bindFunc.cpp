#include <iostream>  
#include <functional>  
#include <string>
using namespace std;  
  
class A  
{  
public:  
    A() :m_a(0){}  
    ~A(){}  
  
    virtual void SetA(const int& a){ cout << "A:" << this << endl;  m_a = a; }  
    int GetA()const { return m_a; }  
protected:  
    int m_a;  
};  
class B: public A  
{  
public:  
    B():A(){;}  
    ~B(){;}  
    virtual void SetA(const int& a){ cout << "B:" << this << endl; m_a = a; }  
private:  
};  


static void bindDemo()
{
    string strText = "\033[34mBlueColor";
    // 颜色输出失败
    std::cout <<strText.c_str() << endl;
    printf("\033[34mHelloBlue\n");
    A a;  
    cout << "A:" << &a << endl;//0  
    function<void(const int&)> func1 = std::bind(&A::SetA, a, std::placeholders::_1);  
    func1(1);  
    cout << a.GetA() << endl;//0    调用时产生了一个临时对象，然后调用临时对象的SetA；
    function<void(const int&)> func2 = std::bind(&A::SetA, &a, std::placeholders::_1);  
    func2(2);  
    cout << a.GetA() << endl;//2   func2调用的是a.SetA，改变了对象a中m_a的值；
  
    cout << "---------" << endl;  
    A* pa = new B();  
    cout << "B:" << pa << endl;//0  
    function<void(const int&)> func3 = std::bind(&A::SetA, pa, std::placeholders::_1);  
    func3(3);  
    cout << pa->GetA() << endl;//3   func3调用的是pa->SetA，输出B:0060A4A8，调用的时B的SetA改变了pa->m_a；
    function<void(const int&)> func4 = std::bind(&A::SetA, *pa, std::placeholders::_1);  
    func4(4);  
    cout << pa->GetA() << endl;//3   func4调用时产生了一个临时对象，然后调用临时对象的A::SetA；
    delete pa;  
    // 结论：std::bind中第二个参数应该是对象的指针，且std::bind支持虚函数。
}
  
int main(void)  
{  
    bindDemo();
    
    system("pause");  

    return 0;  
}  