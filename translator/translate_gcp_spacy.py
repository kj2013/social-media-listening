# -*- coding: utf-8 -*-
"""
Created on Thu May 28 20:14:52 2020
##pip install --target=C:/ProgramData/Anaconda3/ google-cloud-translate
@author: kokil
"""
##https://stackoverflow.com/questions/52535703/having-a-hard-time-using-the-gcp-translate-api
##didnt do https://cloud.google.com/translate/docs/advanced/batch-translation
#other info but we are ok https://cloud.google.com/translate/quotas


import os
import csv
import spacy
import sys
import time
print(sys.executable)
print(sys.version)
from spacy_langdetect import LanguageDetector
from google.cloud import translate_v2 as translate

## write files using https://community.rstudio.com/t/how-to-write-csv-in-r-where-data-is-cleaned-with-utf-8-characters/22836
## data.table::fwrite(sb_text,"sb_text_fortranslation_full.csv")
def clean(content):
    content = content.replace('\n','')
    content = content.replace('\t','')
    content = content.replace(',','')
    content = content.replace('\r','')
    return content
# We setup the global variable for GCP service account credentials

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'' #json file goes here

# We specify the path to the file we want to load


# Instantiate the Google Translation API Client


############################################first pass with spacy, then GCP, then with googletrans

translate_client = translate.Client()

output = []
count = 0
countlang = 0
nlp = spacy.load('en')
nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)
with open(r'text_fortranslation_full.csv',encoding='UTF-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        with open('full_translated.csv', 'a', encoding='utf-8') as f:
           for row in csv_reader:
                     #   try:
                            count = count + 1
                            print(count) 
                            index = row[0]
                          #  print(index)
                            text = row[1]
                            ## first, remove those which have no text
                            ## first, is this english?
                           
                            doc = nlp(text)
# document level language detection. Think of it like average language of the document!
                            if doc._.language["language"] =="en":
                                    f.write(str(index) + '\t' + clean(str(text))+'\t'+clean(str(text))+'\t'+"en"+'\n')
                                    print("this is english")
                            else:
                                    temp = translate_client.translate(text,   target_language='en'    )
                                    f.write(str(index) + '\t' + clean(temp["input"])+'\t'+clean(temp["translatedText"])+'\t'+temp["detectedSourceLanguage"]+'\n')
                                    print(temp)
                                    countlang = countlang + 1
                                    if(countlang%60==0):
                                        time.sleep(20)
                                    
                                    #f.write(str(index) + '\t' + clean(str(temp))+'\n')
                      #  except:
#                            f.write(str(index) + '\t' + clean(str(text))   + 'NA'+ '\n')
                       #     print("didnt work")
           print("done")
        f.close()
#what is still not working are the transliteration ones
## take the output and if langauge = hi but text is english then https://stackoverflow.com/questions/52834152/use-the-google-transliterate-api-in-python