# import re

# regex = r"(\S{1,100})\/(\S{1,100})"

# test_str = ("test/test2\n"
# 	"+-*//////////+-*///")

# matches = re.search(regex, test_str, re.MULTILINE)

# # print(matches.group(2))
# # Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.

dict = {"a": 1, "b": 2, "c": 3}
for i, j in dict.items():
    print(i, j)