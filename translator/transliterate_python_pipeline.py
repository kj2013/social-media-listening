# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 17:13:05 2020

@author: kokil
"""
import http.client
import csv
import sys
import string
print(sys.executable)
print(sys.version)

## write files using https://community.rstudio.com/t/how-to-write-csv-in-r-where-data-is-cleaned-with-utf-8-characters/22836
## data.table::fwrite(sb_text,"sb_text_fortranslation_full.csv")
def clean(content):
    content = content.replace('\n','')
    content = content.replace('\t','')
    content = content.replace(',','')
    content = content.replace('\r','')
    return content
# We setup the global variable for GCP service account credentials


# We specify the path to the file we want to load


# Instantiate the Google Translation API Client
import re

def only_letters(tested_string):
    pattern = re.compile("^[a-zA-Z]+$")
    match = pattern.match(tested_string)
    return match is not None



def request(input):
    conn = http.client.HTTPSConnection('inputtools.google.com')
    conn.request('GET', '/request?text=' + input + '&itc=' + 'hi-t-i0-und' + '&num=1&cp=0&cs=1&ie=utf-8&oe=utf-8&app=test')
    res = conn.getresponse()
    return res

def driver(input):
    output = ''
    if ' ' in input:
        input = input.split(' ')
        for i in input:
            #print(i)
            if only_letters(i):
                #print("it is english")
                res = request(input = i)
                #print(res.read() )
                res = res.read()
                if i==0:
                    output = str(res, encoding = 'utf-8')[14+4+len(i):-31]
                else:
                    output = output + ' ' + str(res, encoding = 'utf-8')[14+4+len(i):-31]
            else:
                #print("it was not english")
                res = i
                if i==0:
                    output = str(res)
                else:
                    output = output + ' ' + str(res)

    else:
        res = request(input = input)
        res = res.read()
        output = str(res, encoding = 'utf-8')[14+4+len(input):-31]
    return(output)

############################################first pass with spacy, then GCP, then with googletrans

output = []
count = 0
countlang = 0

with open(r'file.csv',encoding='UTF-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        with open('file_transliterated.csv', 'a', encoding='utf-8') as f:
           for row in csv_reader:
                     #   try:
                            count = count + 1
                            print(count) 
                            index = row[0]
                            text = row[4]
                            language = row[3]
                            try:
                                transliterated = driver(text)
                            except:
                                transliterated = text
                            print(transliterated)
                            f.write(str(index) + '\t' + clean(transliterated)+'\n')



driver('mein sahi hun')