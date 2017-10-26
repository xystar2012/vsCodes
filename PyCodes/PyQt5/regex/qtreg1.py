from PyQt5.QtCore import *

rx = QRegExp("(\\d+)")
str = "Offsets: 12 14 99 231 7"
def mysplit(str,pattan):
    rx = QRegExp(pattan)
    pos = 0
    list = []
    while True:
        pos = rx.indexIn(str,pos)
        if pos == -1:
            break
        list.append(rx.cap(0))
        qDebug(rx.cap(0))
        pos += rx.matchedLength()
    print(list)

mysplit(str,rx.pattern())

rx = QRegExp("*.txt");
rx.setPatternSyntax(QRegExp.Wildcard)
ret = rx.exactMatch("README.txt")
ret = rx.exactMatch("welcome.txt.bak")

rx = QRegExp("^\\d\\d?$")  #  match integers 0 to 99
ret = rx.indexIn("123")
rx.indexIn("-6")
rx.indexIn("6")

rx = QRegExp("/([a-z]+)/([a-z]+)")
rx.indexIn("Output /dev/null")
ret = rx.pos(0)  ## returns 7 (position of /dev/null)
ret = rx.pos(1)  ## returns 8 (position of dev) 
ret = rx.pos(2)  ## returns 12 (position of null)

rx = QRegExp("\\b(mail|letter|correspondence)\\b")
ret = rx.indexIn("I sent you an email");     #// returns -1 (no match)
ret = rx.indexIn("Please write the letter"); #// returns 17
captured = rx.cap(1)  ## captured == "letter"

str = '''One Eric another Eirik, and an Ericsson. 
                How many Eiriks, Eric?'''

rx = QRegExp("\\b(Eric|Eirik)\\b")
pos = 0
count = 0
while (pos >= 0):
    pos = rx.indexIn(str, pos)
    if (pos >= 0): 
        pos += 1      #// move along in str
        count += 1    #// count our Eric or Eirik
print(count)

rx = QRegExp("&(?!amp;)")  ## match '&' not follow by !amp
line1 = "This & that"
# line1.replace(rx, "&amp;")
line2 = "His &amp; hers & theirs"
# line2.replace(rx, "&amp;")
print(line1,line2,end='\n')
str = "The Qt Company Ltd\tqt.io\tFinland"
rx = QRegExp()
rx.setPattern("^([^\t]+)\t([^\t]+)\t([^\t]+)$")
if (rx.indexIn(str) != -1):
    print(rx.capturedTexts(),rx.captureCount())
    company = rx.cap(1)
    web = rx.cap(2)
    country = rx.cap(3)

print(company,web,country)

str = rx.pattern()
print(str)
str = QRegExp.escape("bingo")
str = QRegExp.escape("f(x)");    ##  s2 == "f\\(x\\)"
print(str)
# rx =  QRegExp("(" + QRegExp.escape(name) +
#              "|" + QRegExp.escape(alias) + ")")
# print(rx.pattern())

str = "hello,it's-ok,for*me|here!"
mysplit(str,"[^-,'*!|]+")  ###  - 在多个连续字符间有特殊意义
mysplit(str,"[^\W+]+")


def mysplitEx(str,pattan):
    rx = QRegularExpression(pattan)
    pos = 0
    match = QRegularExpressionMatch()
    list = []
    print(mysplitEx.__name__,end='')
    while pos < len(str):
        match = rx.match(str,pos)
        if not match.hasMatch():
            break
        list.append(match.captured())
        pos = match.capturedEnd()
    print(list)

mysplitEx(str,r"[^\W+]+")



re= QRegularExpression("^(?'date'\\d\\d)/(?<month>\\d\\d)/(?<year>\\d\\d\\d\\d)$")

match = re.match("08/12/1985");
if match.hasMatch():
    date = match.captured("date")  # // date == "08"
    month = match.captured("month") #// month == "12"
    year = match.captured("year") # // year == 1985
    print(date,month,year)

print(re.namedCaptureGroups())  ## ['', 'date', 'month', 'year']

str = QDateTime.currentDateTime().toString('dd/MM/yy') 
match = re.match(str) 
print('match.lastCapturedIndex:',match.lastCapturedIndex(),'text:',match.capturedTexts())
for i in range(match.lastCapturedIndex()):
      print(match.captured(i)) 




