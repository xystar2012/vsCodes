#include <iostream>
#include <locale>
#include <sstream>
#include <codecvt>


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

int main()
{
    newLoacal();
    newSplit();
    localConstruct();

    system("pause");

    return 0;
}