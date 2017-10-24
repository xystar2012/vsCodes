#include <iostream>
#include <iterator>
#include <string>
#include <regex>
#include <locale>
#include <ctime> 
#include <functional>

using namespace std;

static void testEmail()
{
    std::function<bool(const std::string&)> is_email_valid = [](string email)->bool{

        static const std::regex pattern("(\\w+)(\\.|_)?(\\w*)@(\\w+)(\\.(\\w+))+");
        return std::regex_match(email, pattern);
    };

    std::string email1 = "marius.bancila@domain.com";
    std::string email2 = "mariusbancila@domain.com";
    std::string email3 = "marius_b@domain.co.uk";
    std::string email4 = "marius@domain";

    std::cout << email1 << " : " << (is_email_valid(email1) ?
        "valid" : "invalid") << std::endl;
    std::cout << email2 << " : " << (is_email_valid(email2) ?
        "valid" : "invalid") << std::endl;
    std::cout << email3 << " : " << (is_email_valid(email3) ?
        "valid" : "invalid") << std::endl;
    std::cout << email4 << " : " << (is_email_valid(email4) ?
        "valid" : "invalid") << std::endl;
}


void testIP()
{
    std::function<void (const std::string&)> show_ip_parts = [](string ip){
        
       const std::regex pattern("(\\d{1,3}):(\\d{1,3}):(\\d{1,3}):(\\d{1,3})");
      // object that will contain the sequence of sub-matches
      std:: match_results<std::string::const_iterator> result;
      // match the IP address with the regular expression
      bool valid = std:: regex_match(ip, result, pattern);
      std::cout << ip << " \t: " << (valid ? "valid" : "invalid") << std::endl;
                
      // if the IP address matched the regex, then print the parts
      if(valid)
      {
         std::cout << "entireMatch: " << result[0] << "\t";
         std::cout << "b1: " << result[1] << "\t";
         std::cout << "b2: " << result[2] << "\t";
         std::cout << "b3: " << result[3] << "\t";
         std::cout << "b4: " << result[4] << std::endl;
      }
    };

    show_ip_parts("1:22:33:444");
    show_ip_parts("1:22:33:4444");
    show_ip_parts("100:200");
}


static void input_regSearch()
{   
    const char* reg_esp = "^A*B+C?$";  
    regex rgx(reg_esp);  
    cmatch match;  
    const char* target = "AAAAAAAAABBBBBBBBC";  
    if(regex_search(target,match,rgx))  
    {  
        for(size_t a = 0;a < match.size();a++)  
            cout << string(match[a].first,match[a].second) << endl;  
    }  
    else  
        cout << "No Match Case !" << endl;  


    std::string input;
    while(std::cin >> input && input != "")
    {
        std::regex self_regex("^\\w{1,5}$");
        std::cout << "Get input:" << input << std::endl;
        if (std::regex_search(input, self_regex))
        {
            std::cout << "Text contains the phrase 'regular expressions'\n";
        }
    }
}


static void tmstr_split()
{
    // zh_CN.utf8
    std::locale::global(std::locale(""));
    std::time_t t = std::time(NULL);

    char mbstr[100];
    if (std::strftime(mbstr, sizeof(mbstr), "%A %c", std::localtime(&t))) 
    {
        std::cout << "TimeStr:" << mbstr << '\n';
    }
    // 星期四 2017/9/7 10:16:31  ==> xxx-xxxx-x-x-xx-xx-xx
    string ret  =std::regex_replace(string(mbstr), std::regex("\\s|\/|:"), "-");
    std::cout <<  ret << endl;
    // "(\\S+)"
    std::regex regTm("([^-]+)");
    std::smatch sm;
    // std:: match_results<std::string::const_iterator> result;
    
    auto words_begin = std::sregex_iterator(ret.begin(), ret.end(), regTm);
    auto words_end = std::sregex_iterator();

    for_each(words_begin,words_end,[](std::smatch it){

        std::cout << "  " << it.str() << '\n';
    });
    
    std::regex unregTm("\-+");
    std::copy(std::sregex_token_iterator(ret.begin(), ret.end(), unregTm, -1),
    std::sregex_token_iterator(),
    std::ostream_iterator<std::string>(std::cout, "\n"));
}


static void stringSplit()
{
    string ret = "hello:,are you ok,it's-me??";

    /**
    
        -1 means that you are interested in all the subsequences 
            between matched regular expressions (token separators).
        0 means that you are interested in all the matched regular expressions (token separators).
        Any other value n means that you are interested in the matched 
        nth subexpression inside the regular expressions.
    */
    std::regex reg("[:|,|\\s|\\-|?]+");
    std::copy(std::sregex_token_iterator(ret.begin(), ret.end(), reg, -1),
    std::sregex_token_iterator(),
    std::ostream_iterator<std::string>(std::cout, "\n"));
}

int main(int argc,char** argv)
{
    // testIP();
    // testEmail();
    // input_regSearch();
    // tmstr_split();

    stringSplit();
    
    // system("pause");

    return 0;
}
