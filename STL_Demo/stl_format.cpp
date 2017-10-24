#include <iostream>
#include <iomanip>
#include <cmath>

using namespace std;


static void setWidth()
{
    cout << fixed << right;
    
        cout << setw(6)  << "N" <<  setw(14) << "sqart root"
            << setw(15) << "fourth root\n";
        
        double root;
    
        for(int n = 10;n <= 100; n+= 10)
        {
            root = sqrt(double(n));
    
            cout << setw(6) << setfill('.') << n << setfill(' ')
                << setw(12) << setprecision(3) << root
                << setw(14) << setprecision(4) << sqrt(root)
                << endl;
        }
}

static void setJustify()
{
    cout.setf(ios_base::left,ios_base::adjustfield);
    cout.setf(ios_base::showpos);
    cout.setf(ios_base::showpoint);
    cout.precision(3);

    ios_base::fmtflags old = cout.setf(ios_base::scientific,ios_base::floatfield);

    cout << "left Justification: \n";
    long n;

    for(n = 1;n <=41;n += 10)
    {
        cout.width(4);
        cout << n << "|";
        cout.width(12);
        cout << sqrt(double(n)) << "|\n";
    }

    cout.setf(ios_base::internal,ios_base::adjustfield);
    cout.setf(old,ios_base::floatfield);
    cout << "internal Justification:\n";

    for(n = 1;n <=41;n += 10)
    {
        cout.width(4);
        cout << n << "|";
        cout.width(12);
        cout << sqrt(double(n)) << "|\n";
    }


    cout.setf(ios_base::right,ios_base::adjustfield);
    cout.setf(ios_base::fixed,ios_base::floatfield);
    cout << "Right Justification:\n";
    
    for(n = 1;n <=41;n += 10)
    {
        cout.width(4);
        cout << n << "|";
        cout.width(12);
        cout << sqrt(double(n)) << "|\n";
    }


    int temperature = 63;
    cout.setf(ios_base::showpos);  // + -
    cout << "temperature:\n" << temperature << endl;
    cout << std::hex << temperature << endl;
    cout.setf(ios_base::uppercase);  // FF 
    cout.setf(ios_base::showbase);  // 0X
    cout << temperature << endl;
    cout.setf(ios_base::boolalpha);
    cout << "Ture:" << true << endl;

    return ;
}

int main()
{
    setJustify();

    return 0;
    
}