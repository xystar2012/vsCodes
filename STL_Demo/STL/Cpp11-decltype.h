#include <type_traits>
#include <iostream>
#include <map>

using namespace  std;

void _simpleTest();

double foo(int a)
{
	return double(a) + 0.1;
}

int fool(double a)
{
	return (int)a;
}

template<class T>
auto Forword(T t)->decltype(foo(t))
{
	return fool(t);
}


// 返回函数指针的函数定义 [9/16/2016 xystar]
int(*(*pf())())()
{
	return nullptr;
}


// C++11返回类型 推导增加可读性[9/16/2016 xystar]
auto pf1() ->auto(*)()->int(*)()
{
	return nullptr;
}


/************************************************************************/
/* 
	decltype推导四规则
	如果e是一个没有带括号的标记符表达式或者类成员访问表达式，那么的decltype（e）就是e所命名的实体的类型。
		此外，如果e是一个被重载的函数，则会导致编译错误。
	否则 ，假设e的类型是T，如果e是一个将亡值，那么decltype（e）为T&&
	否则，假设e的类型是T，如果e是一个左值，那么decltype（e）为T&。
	否则，假设e的类型是T，则decltype（e）为T。
	标记符指的是除去关键字、字面量等编译器需要使用的标记之外的程序员自己定义的标记，而单个标记符对应的表达式即为标记符表达式。例如：

	int arr[4]
	则arr为一个标记符表达式，而arr[3]+0不是。

	我们来看下面这段代码：

	int i=10;
	decltype(i) a; //a推导为int
	decltype((i))b=i;//b推导为int&，必须为其初始化，否则编译错误
	仅仅为i加上了()，就导致类型推导结果的差异。这是因为，i是一个标记符表达式，根据推导规则1，类型被推导为int。而(i)为一个左值表达式，所以类型被推导为int&。
*/
/************************************************************************/

void declType()
{
	int i = 4;
	int arr[5] = { 0 };
	int *ptr = arr;
	struct S{ double d; }s;
	void Overloaded(int);
	void Overloaded(char);//重载的函数
	int && RvalRef();
	const bool Func(int);

	//规则一：推导为其类型
	decltype (arr) var1; //int 标记符表达式

	decltype (ptr) var2;//int *  标记符表达式

	decltype(s.d) var3;//doubel 成员访问表达式

	//decltype(Overloaded) var4;//重载函数。编译错误。

	//规则二：将亡值。推导为类型的右值引用。

	decltype (RvalRef()) var5 = 1;

	//规则三：左值，推导为类型的引用。

	decltype ((i))var6 = i;     //int&

	decltype (true ? i : i) var7 = i; //int&  条件表达式返回左值。

	decltype (++i) var8 = i; //int&  ++i返回i的左值。

	decltype(arr[5]) var9 = i;//int&. []操作返回左值

	decltype(*ptr)var10 = i;//int& *操作返回左值

	decltype("hello")var11 = "hello"; //const char(&)[9]  字符串字面常量为左值，且为const左值。


	//规则四：以上都不是，则推导为本类型

	decltype(1) var12;//const int

	decltype(Func(1)) var13 = true;//const bool

	decltype(i++) var14 = i;//int i++返回右值

	// for test [9/16/2016 xystar]
	cout << is_same<decltype(pf), decltype(pf1)>::value << endl;
	cout << is_lvalue_reference<decltype(i++)>::value << endl;
	cout << is_rvalue_reference<decltype(i++)>::value << endl;
}

void _simpleTest()
{
	int i = 10;


	cout <<  "Forword(double): " << Forword(2.0) << endl;
	cout << "Forword(int)" << Forword(3) << endl;

	vector<int> v = { 1, 2, 3, 4, 5 };
	for (auto e : v)  // e 解引用后的 对象
	{
		cout << e << endl;
	}

	for (auto i = v.begin(); i != v.end(); i++)
	{
		cout << *i << endl;  // i 是 迭代器对象
	}
}


typedef std::function<int(int,int)> Pf_add;

void functionalTst()
{
	Pf_add pfAdd1;
	Pf_add pfAdd2(nullptr);

	Pf_add tmp = [](int a, int b)->int
	{

		return a + b;
	};

	pfAdd1 = tmp;

	cout << "pfAdd1:" << (pfAdd1 == nullptr) << ",Value:" << (pfAdd1 && 0x1) << endl;
	cout << "pfAdd2:" << (pfAdd2 == nullptr) << ",Value:" << (pfAdd2 && 0x1) << endl;

	//pfAdd1._Reset;
}

void testTuple()
{
	#define N  10

	std::map<int, std::tuple<bool, int>> device_connection_status;

	for (int i = 1; i < N; i++)
	{
		std::tuple<bool, int>& tu = device_connection_status[i];
		std::get<0>(tu) = true;
		std::get<1>(tu) = 0;
	}

	for (auto it : device_connection_status)
	{
		cout << "first:" << it.first << "\t";
		std::tuple<bool, int>& tu = it.second;
		cout << "second,0:" << std::get<0>(tu) << ",2: " << std::get<1>(tu) << endl;
	}


	for (int i = 1; i < N; i++)
	{
		std::tuple<bool, int>& tu = device_connection_status[i];
		std::get<0>(tu) = false;
		std::get<1>(tu) += 1;
	}

	for (auto it : device_connection_status)
	{
		cout << "first:" << it.first << "\t";
		std::tuple<bool, int>& tu = it.second;
		cout << "second,0:" << std::get<0>(tu) << ",2: " << std::get<1>(tu) << endl;
	}
}


/************************************************************************/
/* 

1.当typeid操作符的操作数是不带有虚函数的类类型时，typeid操作符会指出操作数的类型，而不是底层对象的类型。
2.如果typeid操作符的操作数是至少包含一个虚拟函数的类类型时，并且该表达式是一个基类的引用，则typeid操作符指出底层对象的派生类类型。

*/
/************************************************************************/

#define OUTPUT(f)   cout << #f << "\t: " << typeid(f).name() << endl;  
class BaseA {};
class DeriveA : public BaseA {};

class BaseB
{
	virtual void f(){}
};
class DeriveB : public BaseB {};

static void testTypeID()
{
	cout << "-------直接处理类名-------" << endl;

	OUTPUT(BaseA);
	OUTPUT(DeriveA);
	OUTPUT(BaseB);
	OUTPUT(DeriveB);

	cout << endl << "-------基类不含虚函数-------" << endl;

	BaseA baseA;
	DeriveA deriveA;
	OUTPUT(baseA);
	OUTPUT(deriveA);

	BaseA* pa;
	pa = &baseA;
	OUTPUT(*pa);
	OUTPUT(pa);
	pa = &deriveA;
	OUTPUT(*pa);
	OUTPUT(pa);

	cout << endl << "-------基类含有虚函数-------" << endl;

	BaseB baseB;
	DeriveB deriveB;
	OUTPUT(baseB);
	OUTPUT(deriveB);

	BaseB* pb;
	pb = &baseB;
	OUTPUT(*pb);
	OUTPUT(pb);
	pb = &deriveB;
	OUTPUT(*pb);
	OUTPUT(pb);
}