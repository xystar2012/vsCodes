#include <iostream>
#include <iterator>
#include <string>
#include <regex>
#include <locale>
#include <ctime> 
#include <functional>

using namespace std;

static void findAndReplace()
{
    std::string s = "Some people, when confronted with a problem, think "
                    "\"I know, I'll use regular expressions.\" "
                    "Now they have two problems.";

    std::regex self_regex("REGULAR EXPRESSIONS",
                          std::regex_constants::ECMAScript | std::regex_constants::icase);
    if (std::regex_search(s, self_regex))
    {
        std::cout << "Text contains the phrase 'regular expressions'\n";
    }

    std::regex word_regex("(\\S+)");
    auto words_begin =
        std::sregex_iterator(s.begin(), s.end(), word_regex);
    auto words_end = std::sregex_iterator();

    std::cout << "Found "
              << std::distance(words_begin, words_end)
              << " words\n";

    const int N = 6;
    std::cout << "Words longer than " << N << " characters:\n";
    for (std::sregex_iterator i = words_begin; i != words_end; ++i)
    {
        std::smatch match = *i;
        std::string match_str = match.str();
        if (match_str.size() > N)
        {
            std::cout << "  " << match_str << '\n';
        }
    }

    std::regex long_word_regex("(\\w{7,})");
    std::string new_s = std::regex_replace(s, long_word_regex, "[$&]");
    std::cout << new_s << '\n';
}


static void reg_replace()
{
    std::string text = "Quick brown fox";
    std::regex vowel_re("a|e|i|o|u");
  
    // write the results to an output iterator
    std::regex_replace(std::ostreambuf_iterator<char>(std::cout),
                       text.begin(), text.end(), vowel_re, "*");
  
    // construct a string holding the results
    std::cout << '\n' << std::regex_replace(text, vowel_re, "[$&]") << '\n';
}

static void reg_search()
{
    std::string lines[] = {"Roses are #ff0000",
                           "violets are #0000ff",
                           "all of my base are belong to you"};

    std::regex color_regex("#([a-f0-9]{2})"
                           "([a-f0-9]{2})"
                           "([a-f0-9]{2})");

    // simple match
    for (const auto &line : lines)
    {
        std::cout << line << ": " << std::boolalpha
                  << std::regex_search(line, color_regex) << '\n';
    }
    std::cout << '\n';

    // show contents of marked subexpressions within each match
    std::smatch color_match;
    for (const auto &line : lines)
    {
        if (std::regex_search(line, color_match, color_regex))
        {
            std::cout << "matches for '" << line << "'\n";
            std::cout << "Prefix: '" << color_match.prefix() << "'\n";
            for (size_t i = 0; i < color_match.size(); ++i)
                std::cout << i << ": " << color_match[i] << '\n';
            std::cout << "Suffix: '" << color_match.suffix() << "\'\n\n";
        }
    }

    // repeated search (see also std::regex_iterator)
    std::string log(R"(
                        Speed:  366
                        Mass:   35
                        Speed:  378
                        Mass:   32
                        Speed:  400
                        Mass:   30)");
    std::regex r(R"(Speed:\t\d*)");
    std::smatch sm;
    while (regex_search(log, sm, r))
    {
        std::cout << sm.str() << '\n';
        log = sm.suffix();
    }

    // C-style string demo
    std::cmatch cm;
    if (std::regex_search("this is a test", cm, std::regex("test")))
        std::cout << "\nFound " << cm[0] << " at position " << cm.prefix().length();
}


static void reg_result()
{
    {
        std::regex re("a(a)*b");
        std::string target("aaab");
        std::smatch sm;
     
        std::cout << sm.size() << '\n';
     
        std::regex_match(target, sm, re);
        std::cout << sm.size() << '\n';    
    }

    {
        std::string target("baaaby");
        std::smatch sm;
     
        std::regex re1("a(a)*b");
        std::regex_search(target, sm, re1);
        std::cout << "entire match: " << sm.str(0) << '\n'
                  << "submatch #1: " << sm.str(1) << '\n';
     
        std::regex re2("a(a*)b");
        std::regex_search(target, sm, re2);
        std::cout << "entire match: " << sm.str(0) << '\n'
                  << "submatch #1: " << sm.str(1) << '\n';
    
    }

    {
        std::regex re("a(a)*b");
        std::string target("aaab");
        std::smatch sm;
     
        std::regex_match(target, sm, re);
        std::cout << sm.position(1) << '\n';    
    }
 
}

static void reg_match()
{
    bool bRet = false;
    std::regex re("Get|GetValue");
    std::cmatch m;
    bRet =  std::regex_search("GetValue", m, re);  // returns true, and m[0] contains "Get"
    bRet = std::regex_match ("GetValue", m, re);  // returns true, and m[0] contains "GetValue"
    bRet = std::regex_search("GetValues", m, re); // returns true, and m[0] contains "Get"
    bRet = std::regex_match ("GetValues", m, re); // returns false

     // Simple regular expression matching
     std::string fnames[] = {"foo.txt", "bar.txt", "baz.dat", "zoidberg"};
     std::regex txt_regex("[a-z]+\\.txt");
  
     for (const auto &fname : fnames) {
         std::cout << fname << ": " << std::regex_match(fname, txt_regex) << '\n';
     }   
  
     // Extraction of a sub-match
     std::regex base_regex("([a-z]+)\\.txt");
     std::smatch base_match;
  
     for (const auto &fname : fnames) {
         if (std::regex_match(fname, base_match, base_regex)) {
             // The first sub_match is the whole string; the next
             // sub_match is the first parenthesized expression.
             if (base_match.size() == 2) {
                 std::ssub_match base_sub_match = base_match[1];
                 std::string base = base_sub_match.str();
                 std::cout << fname << " has a base of " << base << '\n';
             }
         }
     }
  
     // Extraction of several sub-matches
     std::regex pieces_regex("([a-z]+)\\.([a-z]+)");
     std::smatch pieces_match;
  
     for (const auto &fname : fnames) {
         if (std::regex_match(fname, pieces_match, pieces_regex)) {
             std::cout << fname << '\n';
             for (size_t i = 0; i < pieces_match.size(); ++i) {
                 std::ssub_match sub_match = pieces_match[i];
                 std::string piece = sub_match.str();
                 std::cout << "  submatch " << i << ": " << piece << '\n';
             }   
         }   
     }   
}

static void reg_iter()
{
    const std::string s = "Quick brown fox.";
    
       std::regex words_regex("[^\\s]+");
       auto words_begin = 
           std::sregex_iterator(s.begin(), s.end(), words_regex);
       auto words_end = std::sregex_iterator();
    
       std::cout << "Found " 
                 << std::distance(words_begin, words_end) 
                 << " words:\n";
    
       for (std::sregex_iterator i = words_begin; i != words_end; ++i) {
           std::smatch match = *i;                                                 
           std::string match_str = match.str(); 
           std::cout << match_str << '\n';
       }  
}

static void reg_token()
{
    reg_iter();
    std::string text = "Quick brown fox.";
    // tokenization (non-matched fragments)
    // Note that regex is matched only two times: when the third value is obtained
    // the iterator is a suffix iterator.
    std::regex ws_re("\\s+"); // whitespace
    std::copy( std::sregex_token_iterator(text.begin(), text.end(), ws_re, -1),
               std::sregex_token_iterator(),
               std::ostream_iterator<std::string>(std::cout, "\n"));
  
    // iterating the first submatches
    std::string html = "<p><a href=\"http://google.com\">google</a> "
                       "< a HREF =\"http://cppreference.com\">cppreference</a>\n</p>";
    std::regex url_re("<\\s*A\\s+[^>]*href\\s*=\\s*\"([^\"]*)\"", std::regex::icase);
    // 0 -- 全部  
    std::copy( std::sregex_token_iterator(html.begin(), html.end(), url_re, 1),
               std::sregex_token_iterator(),
               std::ostream_iterator<std::string>(std::cout, "\n"));
}

int main(int argc,char** argv)
{
    // findAndReplace();
    // reg_replace();
    // reg_search();
    // reg_result();
    
    // reg_match();
    reg_token();
    // system("pause");

    return 0;
}
