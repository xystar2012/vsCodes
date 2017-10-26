import re
import collections

ret = re.match("c", "abcdef")    # No match
ret = re.search("c", "abcdef")   # Match
ret = re.search("^a", "abcdef")  # Match
rt = re.search("^c", "abcdef")  # No match
rt = re.match('X', 'A\nB\nX', re.MULTILINE)  # No match
rt = re.search('X', 'A\nB\nX', re.MULTILINE)  # No match
if rt:
    print(rt.span())
rt = re.search('^X.*', 'A\nB\nXabcdef', re.MULTILINE)  # Match
print(rt.group(0))
print(type(ret),ret)

## search replace
data = 'hello this is for test'
data = data.replace('hello','say',2)
print(data)
data = re.sub('[ae]', 'X', 'abcdef')
print(data)
data = re.findall('car', 'carry the barcardi to the car')
print(data)
data = re.findall('\w*?\.jpg|\w*?\.png',"flower is __aa.jpg bb.png cc.jpgdd.png11.jpg22.png")
print(data)
m = re.search('(?<=-)\w+', 'spam-egg')
print(m.group(0))
m = re.search('(?<=abc)def', 'abcdef')
print(m.group(0))
print( re.split('\W+', 'Words, words, words.'))
print(re.split('(\W+)', 'Words, words, words.'),1)
rt = re.split('[a-f]+', '0a3B9', flags=re.IGNORECASE)
rt = pattern = re.compile("d")
rt = pattern.search("dog")     # Match at index 0
rt = pattern.search("dog", 1)  # No match; search doesn't include the "d"

m = re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")
rt = m.group(0)       # The entire match
rt = m.group(1)       # The first parenthesized subgroup.
rt = m.group(2)       # The second parenthesized subgroup.
rt = m.group(1, 2)    # Multiple arguments give us a tuple.

m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Malcolm Reynolds")
m.group('first_name')
m = re.match(r"(..)+", "a1b2c3")  # Matches 3 times.
rt = m.group(1)                        # Returns only the last match.
m = re.match(r"(\d+)\.(\d+)", "24.1632")
rt = m.groups()
m = re.match(r"(\d+)\.?(\d+)?", "24")
rt = m.groups()      # Second group defaults to None.
rt = m.groups('0')   # Now, the second group defaults to '0'.
email = "tony@tiremove_thisger.net"
m = re.search("remove_this", email)
## 匹配的开头结尾
rt = email[:m.start()] + email[m.end():]
rt = m.string[m.start():m.end()]

def displaymatch(match):
    if match is None:
        return None
    return '<Match: %r, groups=%r>' % (match.group(), match.groups())
valid = re.compile(r"^[a2-9tjqk]{5}$")
rt = displaymatch(valid.match("akt5q"))


text = """Ross McFluff: 834.345.1254 155 Elm Street
Ronald Heathmore: 892.345.3428 436 Finley Avenue
Frank Burger: 925.541.7625 662 South Dogwood Way
Heather Albrecht: 548.326.4584 919 Park Place"""

entries = re.split("\n+", text)
rt = [re.split(":? ", entry, 3) for entry in entries]
# print(rt)
rt = [re.split(":? ", entry, 4) for entry in entries]
# print(rt)
text = "He was carefully disguised but captured quickly by police."
rt = re.findall(r"\w+ly", text)
for m in re.finditer(r"\w+ly", text):
    print('%02d-%02d: %s' % (m.start(), m.end(), m.group(0)))

Token = collections.namedtuple('Token', ['typ', 'value', 'line', 'column'])
def tokenize(code):
    keywords = {'IF', 'THEN', 'ENDIF', 'FOR', 'NEXT', 'GOSUB', 'RETURN'}
    token_specification = [
        ('NUMBER',  r'\d+(\.\d*)?'),  # Integer or decimal number
        ('ASSIGN',  r':='),           # Assignment operator
        ('END',     r';'),            # Statement terminator
        ('ID',      r'[A-Za-z]+'),    # Identifiers
        ('OP',      r'[+\-*/]'),      # Arithmetic operators
        ('NEWLINE', r'\n'),           # Line endings
        ('SKIP',    r'[ \t]+'),       # Skip over spaces and tabs
        ('MISMATCH',r'.'),            # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
        elif kind == 'SKIP':
            pass
        elif kind == 'MISMATCH':
            raise RuntimeError('%r unexpected on line %d' % (value, line_num))
        else:
            if kind == 'ID' and value in keywords:
                kind = value
            column = mo.start() - line_start
            yield Token(kind, value, line_num, column)
statements = '''
    IF quantity THEN
        total := total + price * quantity;
        tax := price * 0.05;
    ENDIF;
'''
for token in tokenize(statements):
    print(token)