# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 15:21:21 2018

@author: jaidka
"""


import argparse
from urllib.parse import urlparse 
import urllib
import csv
import tweepy
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread
from collections import Counter
from nltk.corpus import stopwords
import vincent
import random
import pandas
from collections import Counter
import operator 
import json
import string
#import wordcloud as WordCloud
from wordcloud import WordCloud, STOPWORDS
from nltk import bigrams 
#from nltk import SentimentIntensityAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

import re
 
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

# URL CLEANUP


def url_fix(s, charset='utf-8'):
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))

# COMMAND PARSER
def tw_parser():
    global qw, ge, l, t, c, d

# USE EXAMPLES:
# =-=-=-=-=-=-=
# % twsearch <search term>            --- searches term
# % twsearch <search term> -g sf      --- searches term in SF geographic box <DEFAULT = none>
# % twsearch <search term> -l en      --- searches term with lang=en (English) <DEFAULT = en>
# % twsearch <search term> -t {m,r,p} --- searches term of type: mixed, recent, or popular <DEFAULT = recent>
# % twsearch <search term> -c 12      --- searches term and returns 12 tweets (count=12) <DEFAULT = 1>
# % twsearch <search term> -o {ca, tx, id, co, rtc)   --- searches term and sets output options <DEFAULT = ca, tx>

# Parse the command
    parser = argparse.ArgumentParser(description='Twitter Search')
    parser.add_argument(action='store', dest='query', help='Search term string')
    parser.add_argument('-g', action='store', dest='loca', help='Location (lo, nyl, nym, nyu, dc, sf, nb')
    parser.add_argument('-l', action='store', dest='l', help='Language (en = English, fr = French, etc...)')
    parser.add_argument('-t', action='store', dest='t', help='Search type: mixed, recent, or popular')
    parser.add_argument('-c', action='store', dest='c', help='Tweet count (must be <50)')
    args = parser.parse_args()

    qw = args.query     # Actual query word(s)
    ge = ''

    # Location
    loca = args.loca
    if (not(loca in ('lo', 'nyl', 'nym', 'nyu', 'dc', 'sf', 'nb')) and (loca)):
        print ("WARNING: Location must be one of these: lo, nyl, nym, nyu, dc, sf, nb")
        exit()
    if loca:
        ge = locords[loca]

    # Language
    l = args.l
    if (not l):
        l = "en"
    if (not(l in ('en','fr','es','po','ko', 'ar'))):
        print ("WARNING: Languages currently supported are: en (English), fr (French), es (Spanish), po (Portuguese), ko (Korean), ar (Arabic)")
        exit()

    # Tweet type
    t = args.t
    if (not t):
        t = "recent"
    if (not(t in ('mixed','recent','popular'))):
        print ("WARNING: Search type must be one of: (m)ixed, (r)ecent, or (p)opular")
        exit()

    # Tweet count
    if args.c:
        c = int(args.c)
        if (c > cmax):
            print ("Resetting count to ",cmax," (maximum allowed)")
            c = cmax
        if (not (c) or (c < 1)):
            c = 1
    if not(args.c):
        c = 1

    print ("Query: %s, Location: %s, Language: %s, Search type: %s, Count: %s" %(qw,ge,l,t,c))


# AUTHENTICATION (OAuth)
def tw_oauth(authfile):
    with open(authfile, "r") as f:
        ak = f.readlines()
    f.close()
    auth1 = tweepy.auth.OAuthHandler(ak[0].replace("\n",""), ak[1].replace("\n",""))
    auth1.set_access_token(ak[2].replace("\n",""), ak[3].replace("\n",""))
    return tweepy.API(auth1)

# TWEEPY SEARCH FUNCTION
def tw_search(api):
    counter = 0
    # Open/Create a file to append data
    csvFile = open('result.csv','w',newline='')
    #Use csv Writer
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["created", "text", "retwc", "hashtag", "followers", "friends","positive","negative","compound"])
    corpus= ""
    corp = []
    for tweet in tweepy.Cursor(api.search,
                                q = qw,
                                g = ge,
                                lang = l,
                                result_type = t,
                                count = c).items():

        #TWEET INFO
        created = tweet.created_at   #tweet created
        text    = tweet.text         #tweet text
        tweet_id = tweet.id          #tweet ID# (not author ID#)
        cords   = tweet.coordinates  #geographic co-ordinates
        retwc   = tweet.retweet_count #re-tweet count
        try:
            hashtag = tweet.entities[u'hashtags'][0][u'text'] #hashtags used
        except:
            hashtag = "None"
        try:
            rawurl = tweet.entities[u'urls'][0][u'url'] #URLs used
            urls = url_fix(rawurl)
        except:
            urls    = "None"
        #AUTHOR INFO
        username  = tweet.author.name            #author/user name
        usersince = tweet.author.created_at      #author/user profile creation date
        followers = tweet.author.followers_count #number of author/user followers (inlink)
        friends   = tweet.author.friends_count   #number of author/user friends (outlink)
        authorid  = tweet.author.id              #author/user ID#
        authorloc = tweet.author.location        #author/user location
        #TECHNOLOGY INFO
        geoenable = tweet.author.geo_enabled     #is author/user account geo enabled?
        source    = tweet.source                 #platform source for tweet
        ss = tw_sent(text)
        corpus=corpus+ " " +text
        try:
            csvWriter.writerow([created, str(text).encode("utf-8"), retwc, hashtag, followers, friends,ss.get('pos'),ss['neg'],ss['compound']])
            counter = counter +1
            if (counter == c):
                break
        except:
            pass
    csvFile.close()
    return corpus

def tw_stream(api):
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener())
    myStream.filter(track=qw, async=True)
# FUNCTIONS for ANALYSIS

def tw_sent(text):
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(text)
    #print(type(ss))
#    print(ss)
    return(ss)
    #print('{0}:{1}'.format(text,ss['compound']),end='')



def generate_wordcloud(corpus):
    wordcloud = WordCloud(background_color="white", max_words=2000,max_font_size=40,
                      stopwords = {'to', 'of','follow', 'it','your','you','with','join','on','be','we','all','our','this','up','that','in','not','are','about','will','by','have','as','much','new','how','my','can','amp','let','nfrisbie83','kh9zmX25Mo','https','RT','and','the','is','for','co'} # set or space-separated string
                      ).generate(corpus)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


def generate_plot(corpus):
    c=Counter(corpus.split(" "))
    print(c.most_common())
    counts = c.values()
    plt.bar(range(len(counts)), counts)
    plt.show()
    
def generate_sentiplot(sentiscores):
    c=Counter(corpus.split(" "))
    print(c.most_common())
    counts = c.values()
    plt.bar(range(len(counts)), counts)
    plt.show()

def generate_vincent(corpus):
    punctuation = list(string.punctuation)
    count_all = Counter()
    stop = stopwords.words('english') + punctuation + ['rt','retweet','…','th','via']
    corpus=str.lower(corpus)
#   terms_stop = [term for term in preprocess(corpus) if term not in stop]
#   terms_all = [term for term in preprocess(corpus)]
#   terms_bigram = bigrams(terms_stop)          

# Count terms only (no hashtags, no mentions)
    terms_only = [term for term in preprocess(corpus) 
              if term not in stop and
              not term.startswith(('#', '@'))] 
              # mind the ((double brackets))
              # startswith() takes a tuple (not a list) if 
              # we pass a list of inputs
    count_all.update(terms_only)
    print(count_all.most_common(10))
    word_freq = count_all.most_common(20)
    labels, freq = zip(*word_freq)
    data = {'data': freq, 'x': labels}
    bar = vincent.Bar(data, iter_idx='x')
    bar.to_json('term_freq.json', html_out=True, html_path='chart.html')
  

def main():

    global api, cmax, locords

    # Geo-coordinates of five metropolitan areas
    # London, NYC (lower, middle, upper), Wash DC, San Francisco, New Brunswick (NJ)
    locords =  {'lo': '0, 51.503, 20km',
                'nyl': '-74, 40.73, 2mi',
                'nym': '-74, 40.74, 2mi',
                'nyu': '-73.96, 40.78, 2mi',
                'dc': '-77.04, 38.91, 2mi',
                'sf': '-122.45, 37.74, 5km',
                'nb': '-74.45, 40.49, 2mi'}
    # Maximum allowed tweet count (note: Twitter sets this to ~180 per 15 minutes)
    cmax = 50
    # OAuth key file
    authfile = './authh.k'

    tw_parser()
    api = tw_oauth(authfile)
    corpus = tw_search(api)
    
#    generate_vincent(corpus)
#    generate_plot(corpus)
    generate_wordcloud(corpus)


#    print(counts)
if __name__ == "__main__":
    main()
