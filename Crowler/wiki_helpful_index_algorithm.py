from requests_html import HTMLSession
from lxml import html
import pandas as pd
import unicodedata
from hazm import *
import bleach
import csv
import re

# Base Function
def SaveDoc (DataDoc):

    # Open File And set mode Write
    f = open("DocFile.txt", 'w',encoding='utf-8', newline='')
    f.write(DataDoc)
    f.close()

# values Init
page = 0
max_result = 1
Text = ''
Search = "بازیابی_اطلاعات"
url = 'https://fa.wikipedia.org/wiki/{}'.format(Search)
finallyList = []

# objects Init
session = HTMLSession()

# Init Arrays
Token = []
TokenTemp = []

# Start APP
r = session.get(url)
body = r.html.find('#content',first=True)
Token = str(body.text)

# Text Cleaning
clean = bleach.clean(Token).replace('[ویرایش]','')
clean = re.sub(r'http\S+', '', clean)
clean = re.sub(r'\\S+', '', clean)
clean = re.sub(r'[a-zA-Z0-9!@#$*&^%{}()\[\]<:;،؛,×––÷\-\_\'?ö«"».↑/\\=۱۹۴۵۲۰۳•٫۷۶]', '', clean).strip()
clean = clean.replace(u'\ufeff', '')
clean = clean.replace('ö','')
clean = clean.replace('o','')
clean = clean.replace(u'\u200c', '')
clean = unicodedata.normalize("NFKD", clean)

# Text Noramalizetion
normalizer = Normalizer()
clean = normalizer.normalize(clean)

# SaveDoc Test
SaveDoc(clean)

# Creat Token
ListToken = sent_tokenize(clean)

# Creat Word
for v in ListToken:finallyList.extend(word_tokenize(v))

Token = []
stemmer=Stemmer()
# Creat Rest Token
for v in finallyList:Token.append(stemmer.stem(v))

# Clear Token Copy
TokenTemp = Token

# Get unique values from a list
Token = list(set(Token))

# sort Token
Token.sort()

# Init Index List [ TokenIndex ]
TokenFinally = []

for word in Token:
    if (len(word) > 2) : TokenFinally.append(word) 

ListFindeWord = []
wordSplitHistory = []
for word in TokenFinally:
    Min = 0
    Max = 2
    while(len(word)>Max):
        findeWords = []
        wordSplit = word[Min:Max]
        if wordSplit not in wordSplitHistory :
            wordSplitHistory.append(wordSplit)
            findeWords.append(wordSplit)
            for t in TokenFinally :
                if wordSplit in t :
                    findeWords.append(t)
            # Save Finded words
            ListFindeWord.append(findeWords)
        # Change Pin
        Min += 2
        Max += 2
        

print(ListFindeWord)
