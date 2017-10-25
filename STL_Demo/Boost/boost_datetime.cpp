#include <iostream>
#include <sstream> // istringstream
#include <fstream>
#include <string>
#include <vector>
#include <Windows.h>

#include <boost/timer.hpp>
#include <boost/progress.hpp>
#include <boost/date_time/gregorian/gregorian.hpp>   // 公历
#include <boost/date_time/posix_time/posix_time.hpp> //

using namespace std;

int main()
{
    boost::timer t;
    std::cout << "Max " << t.elapsed_max() << endl;
    std::cout << "Min " << t.elapsed_min() << endl;
    std::cout << "elapsed: " << t.elapsed() << endl;
    t.restart();
    Sleep(100);
    std::cout << "elapsed: " << t.elapsed() << endl;
    cout << "---------------------------" << endl;
    stringstream ss;
    {
        boost::progress_timer t(ss);
        Sleep(300);
    }
    cout << ss.str();
    cout << "---------------------------" << endl;

    vector<string> v(100);
    //Do Data Fill......
    ofstream fs("test.txt", std::ios::out);

    boost::progress_display pd(v.size());
    vector<string>::iterator pos;
    for (pos = v.begin(); pos != v.end(); ++pos)
    {
        fs << *pos << endl;
        Sleep(10);
        ++pd;
        //pd.restart(v.size());
        //pd+=(pos-v.begin() +1);
    }
    fs.close();
    cout << "---------------------------" << endl;

    {
        using namespace boost::gregorian;
        cout << "-----------------  date ------------------" << endl;
        date d1;
        date d2(2013, 4, 7);
        date d3(2013, Apr, 7);
        date d4(d2);

        assert(d1 == date(not_a_date_time)); //默认初始化为无效日期
        assert(d2 == d4);
        assert(d3 == d2);

        d1 = from_string("1999,9,9");
        date d5(from_string("2008/8/8"));
        d3 = from_undelimited_string("20110111");

        cout << day_clock::local_day() << endl;
        cout << day_clock::universal_day() << endl;

        date d6(neg_infin);
        date d7(pos_infin);
        cout << d6 << endl;
        cout << d7 << endl;

        cout << "---------------------------" << endl;
        date today(2013, 4, 17);
        assert(today.year() == 2013);
        assert(today.month() == 4);
        assert(today.day() == 17);

        date::ymd_type ymd = today.year_month_day();
        assert(ymd.year == 2013);
        assert(ymd.month == 4);
        assert(ymd.day == 17);

        assert(today.day_of_week() == 3);                  //星期几 周日为0
        cout << today.day_of_year() << endl;               //在一年中是第几天
        assert(today.end_of_month() == date(2013, 4, 30)); //当月的最后一天
        cout << today.week_number() << endl;               //当年的第几周 范围0~53 年初的半周归为上一年，即53
        assert(d6.is_infinity());                          //日期为无限日期
        assert(d6.is_neg_infinity());
        cout << "---------------------------" << endl;

        cout << to_simple_string(today) << endl;
        cout << to_iso_string(today) << endl;
        cout << to_iso_extended_string(today) << endl; //常用日期格式YYYY-MM-DD
        cout << today << endl;

        cout << "---------------------------" << endl;
        tm t = to_tm(today);
        assert(t.tm_hour == 0 && t.tm_min == 0);

        date new_today = date_from_tm(t); //从tm转为date
        assert(new_today == today);

        cout << "-------------- days(date_duration) --------------" << endl;
        days dd1(10), dd2(-20), dd3(365);
        assert(dd1 > dd2 && dd1 < dd3);
        assert(dd1 + dd2 == days(-10));
        assert((dd2 + dd3).days() == 345);
        assert(dd3 / 5 == days(73));

        weeks w(3); //3个星期
        assert(w.days() == 21);

        months m(5);
        years y(2);

        months m2 = y + m;
        assert(m2.number_of_months() == 29);
        assert((y * 2).number_of_years() == 4);

        cout << "-------------- Calc --------------" << endl;
        date dA(2000, 1, 1), dB(2008, 8, 8);
        cout << dB - dA << endl; //3142天

        dA += days(10);
        assert(dA.day() == 11);
        dA += months(2);
        assert(dA.month() == 3 && dA.day() == 11);

        dA -= weeks(1);
        assert(dA.day() == 4);

        dB -= years(7);
        assert(dA.year() == dB.year() - 1);

        //如果日期是月末的最后一天，加减月或年会得到月末的时间，而不是简单的月、年加1
        date sp(2013, 3, 30);
        sp -= months(1);
        assert(sp.month() == 2 && sp.day() == 28);
        sp -= months(1);
        assert(sp.month() == 1 && sp.day() == 31);
        sp += months(2);
        assert(sp.day() == 31); //与原来的日期已经不相等！

        cout << "-------------- date_period --------------" << endl;
        date_period dp(date(2013, 4, 17), days(14)); //左开右闭与STL的容器相似
        assert(!dp.is_null());
        assert(dp.begin().day() == 17);
        assert(dp.last().day() == 30);
        assert(dp.end().day() == 1);

        cout << dp << endl;

        date_period new_dp = dp;
        new_dp.shift(days(3)); //将时间区间向后移动
        assert(new_dp.begin().day() == 20);
        assert(new_dp.length().days() == 14);

        new_dp.expand(days(3)); //区间两段延长n天，即延长2n天。
        assert(new_dp.begin().day() == 17);
        assert(new_dp.length().days() == 20);

        assert(dp.is_after(date(2013, 1, 1)));
        assert(dp.contains(date(2013, 4, 20)));

        date_period dp2(date(2013, 4, 17), days(5));
        assert(dp.contains(dp2));

        assert(dp.intersects(dp2)); //交集
        assert(dp.intersection(dp2) == dp2);

        date_period dp3(date(2013, 5, 1), days(5));
        assert(!dp3.intersects(dp));
        assert(dp3.intersection(dp2).is_null());

        assert(dp.is_adjacent(dp3));

        date_period dp4(date(2013, 4, 17), days(19)); //并集
        assert(dp.merge(dp3).is_null());              //无交集返回空
        assert(dp.span(dp3) == dp4);                  //填充中间区域

        cout << "-------------- date_iterator --------------" << endl;
        date last(2013, 4, 17);

        day_iterator d_iter(last); //日期迭代器

        assert(d_iter == last);
        ++d_iter;
        assert(d_iter == date(2013, 4, 18));

        year_iterator y_iter(*d_iter, 3); //增减步长为3
        assert(y_iter == last + days(1));

        ++y_iter;
        assert(y_iter->year() == 2016);

        cout << "-------------- func --------------" << endl;
        cout << (gregorian_calendar::is_leap_year(2000) ? "Yes" : "no") << endl; //闰年
        assert(gregorian_calendar::end_of_month_day(2013, 2) == 28);             //月末天
    }

    {
        using namespace boost::posix_time;
        cout << "-------------- time_duration --------------" << endl;
        time_duration td(1, 1, 1); //时、分、秒 会自动借、进位
        hours h0(1);
        minutes m(1);
        seconds s(1);
        millisec ms(1);

        time_duration td2 = h0 + m + s + ms;
        time_duration td3 = hours(2) + minutes(10);
        time_duration td4 = duration_from_string("1:10:10:300");

        assert(td4.hours() == 1 && td4.minutes() == 10 && td4.seconds() == 10);
        assert(td.total_seconds() == 1 * 3600 + 1 * 60 + 1); //转为sec

        hours h(-10);
        assert(h.is_negative());

        time_duration h2 = h.invert_sign(); //取反
        assert(!h2.is_negative() && h2.hours() == 10);

        cout << td3 - td2 << endl;
        cout << to_simple_string(td4) << endl;
        cout << to_iso_string(td4) << endl;

        cout << "-------------- ptime --------------" << endl;
        {
            using namespace boost::gregorian;
            ptime p(date(2013, 4, 17), hours(1)); //ptime相当于date+time_duration
            ptime p1 = time_from_string("2013-4-17 16:25:00.255");
            cout << p << endl;
            cout << p1 << endl;
            ptime p2 = second_clock::local_time();       //常用时间输出
            ptime p3 = microsec_clock::universal_time(); //取得UTC时间 微秒精度
            cout << p2 << endl
                 << p3 << endl;

            {
                string timeStr = to_simple_string(p2);
                ptime pt = microsec_clock::local_time();
                time_facet *tf = new boost::posix_time::time_facet("%Y %m %d %H %M %S %f");
                std::stringstream ss;
                ss.imbue(std::locale(std::cout.getloc(), tf));
                ss << pt;
                int a, b, c, d, e, f, g;
                ss >> a >> b >> c >> d >> e >> f >> g;
                cout << a << b << c << d << e << f << g;
                cout << timeStr << "\t" << to_iso_string(microsec_clock::local_time()) << "\t" << ss.str() << endl;
            }

            ptime op(date(2013, 4, 17), hours(1) + minutes(30));
            date d = op.date();
            time_duration optd = op.time_of_day();
            assert(d.day() == 17 && d.month() == 4);
            assert(optd.hours() == 1 && optd.minutes() == 30);
            cout << to_iso_extended_string(op) << endl;

            tm t = to_tm(op); //不可逆，此处与date不同
                              //只能用date_from_tm先得到日期，再填充时间。

            cout << "-------------- time_period --------------" << endl;
            time_period tp1(op, hours(8));
            time_period tp2(op + hours(8), hours(1));
            assert(tp1.end() == tp2.begin() && tp1.is_adjacent(tp2));
            assert(!tp1.intersects(tp2));

            tp1.shift(hours(1));
            assert(tp1.is_after(op));
            assert(tp1.intersects(tp2));

            tp2.expand(hours(10));
            assert(tp2.contains(op) && tp2.contains(tp1));

            cout << "-------------- time_iterator --------------" << endl;
            for (time_iterator t_iter(op, minutes(10)); t_iter < op + hours(1); ++t_iter)
            {
                cout << *t_iter << endl;
            }
            cout << "-------------- formate --------------" << endl;
            date_facet *dfacet = new date_facet("%Y%m%d ");
            cout.imbue(locale(cout.getloc(), dfacet));
            cout << date(2013, 4, 17) << endl;

            time_facet *tfacet = new time_facet("%Y年%m月%d日 %H:%M:%S:%F");
            cout.imbue(locale(cout.getloc(), tfacet));
            cout << op << endl;
        }
    }

    system("pause");

    return 0;
}