from bs4 import BeautifulSoup
import requests
import nltk
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from string import punctuation
import os
import sys
import time
import matplotlib.pyplot as plt

# input and output path arguments from commandline
inputpath = sys.argv[1]
outputpath = sys.argv[2]
print(inputpath)
filenamelist = []

# Reading filenames from the below input directory
def getfilenames():
    for path, dirs, files in os.walk(inputpath):
        for f in files:
            filename = os.path.join(path, f)
            filenamelist.append(filename)
    return filenamelist

# To tokenize the words with the help of BeautifulSoup library

# list of all tokenized words and total time taken to process eversy single input file
tokenizedwordlist = []
timetaken = []
wordfrquency = {}
frequency = {}

def tokenizewords():
    filenames = getfilenames()
    start = time.time()
    for file in filenames:
        with open(file, 'r', encoding='utf8', errors='ignore') as Html_File:
            soupfile = BeautifulSoup(Html_File, features='html.parser')
            text = soupfile.get_text()
            text = text.lower()
            text = text.strip()
            # assignment 2 continuation, please ignore below two lines for now
            # tokenizedwordlist = nltk.word_tokenize(text)
            # stopwordslist = set(stopwords.words('english') + list(punctuation))
            regexptokenizer = RegexpTokenizer(r'[a-zA-Z]+')
            tokenizedwordlist = regexptokenizer.tokenize(text)
            for word in tokenizedwordlist:
                # print("printing word", word)
                if word not in wordfrquency:
                    wordfrquency[word] = 1
                else:
                    wordfrquency[word] += 1
            # Writing an output of every html document to new text file.
            outputfile = os.path.join(outputpath, os.path.basename(file))
            with open(outputfile, 'w', encoding='utf8') as opf:
                for token in tokenizedwordlist:
                    opf.write(str(token) + "\n")
            end = time.time()
            timetaken.append(end-start)
    return tokenizedwordlist

print(timetaken)

t = tokenizewords()
print(wordfrquency)
# token as in word based sorted list
Sortedkey = sorted(wordfrquency)
with open(os.path.join(outputpath, 'Tokens.txt'), 'w', encoding='utf8') as newtokenizedfile:
    for i in range(0, len(Sortedkey)):
        newtokenizedfile.write(Sortedkey[i] + '\n')


# To sort based on word frequency
a = list(sorted(wordfrquency.items(), key=lambda x: x[1], reverse=True))
print(a)
with open(os.path.join(outputpath, 'Tokens_sorted_by_frequency.txt'), 'w', encoding='utf8') as newtokenizedfile:
    for i in range(0, len(a)):
        newtokenizedfile.write(str(a[i][0]) + ' : ' + str(wordfrquency[a[i][0]]) +'\n')

plt.xlabel('Files')
plt.ylabel('Time taken in seconds')
x_values = filenamelist
y_values = timetaken
plt.plot(x_values, y_values)
plt.show()


