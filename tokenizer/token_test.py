# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 13:50:43 2019

@author: Kokil
"""

#import happierfuntokenizing_v3
from happierfuntokenizing_v3 import Tokenizer 
import pandas as pd
import csv
import numpy as np
import sys
import time

tokenizer = Tokenizer()


def tokenize_messages(filename,col_text,col_msgid):
    with open(filename,encoding="utf-8") as corpus:
            reader = csv.reader(corpus)    
            rows_list = []
            for row in reader:
                message = row[col_text]
                tokenizer = Tokenizer(preserve_case=True)
                words = tokenizer.tokenize(message.lower())
                totalGrams=0
                freqs = dict()    
                totalChars = 0
                gram = '' 
                for n in range (1,4):
                    for i in range(0,(len(words) - n)+1):
                        totalGrams += 1
                        gram = ' '.join(words[i:i+n])
                        try:
                            freqs[gram] = 1
                        except:
                            print("error")
                freqs["message_id"]=row[col_msgid]
                rows_list.append(freqs)
            df = pd.DataFrame(rows_list) 
            df= df.replace(np.nan, 0)
            print("Writing tokenized messages to csv...")
            timestr = time.strftime("%Y%m%d-%H%M")
            #print timestr
            df.to_csv("tokenized_messages_"+timestr+".csv")
            
############################
            
  
            
###ARGUMENTS described at line xx
if __name__ == '__main__':
    if len(sys.argv) > 1 and (sys.argv[1]):
        filename = sys.argv[1]
        col_text = int(sys.argv[2])
        col_msgid = int(sys.argv[3])
        tokenize_messages(filename,col_text,col_msgid)
    else:
        print("Arguments should be of the form \"filename with messages\" textcolumn msgidcolumn\"" )
##        "C:/Users/User/Dropbox/data/msgs_jun23.csv" 1 0