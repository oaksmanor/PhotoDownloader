"""

This program is used for downloading pictures in sequential order
by useing [000-000] to indicated download file from 1st para to 2nd para.jpg
Currently, parameters have to be number from 0 to 9, however, I will add more
function to make it support letters in the near future.

Example:
    PhotoDownloader http://www.domainname.com/directory/subdirectory/filename[00-16].jpg
Then, it will download from filename00.jpg to filename16.jpg to current directory.

"""

import urllib.request
import argparse
import sys

from urllib.error import HTTPError
from urllib.request import urlretrieve


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def getRange(url_in_series):
    url_vector = url_in_series.split()
    len_url = len(url_vector)
    substring = find_between(url_in_series, '[', ']')  # will be something like "0-13" in substring
    delimiter = substring.split('-')  # delimiter is an array which contain 0 and 15 two elements
    return delimiter


def zero_substring(full_len, current_not_zero):
    zero_string = ''
    for n in range(0, full_len - current_not_zero):
        zero_string += '0'
    return zero_string


print("This is the name of the script: ", sys.argv[0])
print("Number of arguments: ", len(sys.argv))
print("The arguments are: ", str(sys.argv))

url = sys.argv[1]
url_vector = url.split('/')
url_len = len(url_vector)
name_section = url_vector[url_len-1]  # should be something as "***[?-?].jpg"
name_section = name_section.split('[')
name_section = name_section[0]  # should be something as "***" or just ""
url_vector = url_vector[:-1]  # use the slicing notation to keep everything except the last item
file_directory = ""
for i in url_vector:
    if i == 'http:':
        file_directory += i + '//'
    elif i != '':
        file_directory += i + '/'
series_range = getRange(url)
for j in range(int(series_range[0]), int(series_range[1])):
    try:
        ring_substring = zero_substring(len(series_range[0]), len(str(j)));
        if len(str(j)) < len(series_range[0]):
            urlretrieve(file_directory + name_section + ring_substring + str(j) + '.jpg',
                    name_section + ring_substring + str(j) + '.jpg')
        else:
            urlretrieve(file_directory + name_section + str(j) + '.jpg',
                        name_section + str(j) + '.jpg')
    except FileNotFoundError as err:
        print(err)  # something wrong with local path
    except HTTPError as err:
        print(err)  # something wrong with url