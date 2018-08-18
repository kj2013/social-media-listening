#pull all the followers of a set of user ids into a file.

import sys
import tweepy
import time
from random import randint
import csv

#auth = tweepy.OAuthHandler("g1Sjkp4srZFeKvaxe4H5Lg","JeOmvXYeoFfvhm1YTvp2RP4dFOGCF7fEbExQIId8cl0")
#auth.set_access_token("34570530-ajYCfKsBZGNIe6SWv59ICnBlnNmSF37qZ9W7BEid1","RxsG2aQd2u3RDmeggVa2Vkn2yxWvRLr1zfE7H3R0s")

#api = tweepy.API(auth)

#ids = []

#for page in tweepy.Cursor(api.followers_ids, screen_name="kat_lumibao").pages():
#    ids.extend(page)
#    time.sleep(10)
#    print(len(ids))
    
#from keys import keys #keep keys in separate file, keys.py
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

try:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    with open('followers.txt', 'w') as f:
        #print("camerhere")
        with open('C:/users/jaidka/Downloads/singapore users/user_ids.txt') as userhandles:
            reader = csv.DictReader(userhandles)
            for line in reader:
                try:
                    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
                    screenname = line['user_handle']
                    c = tweepy.Cursor(api.followers_ids, id = screenname)
#    print "type(c)=", type(c)
                    ids = []
                    for page in c.pages():
                        ids.append(page)
                        print(len(ids))
                        time.sleep(10)
                except:
                    print("Error in pulling followers")
                    pass
                for id in ids:
                    try:
                        f.write(str(id)+ '\n')
                    except:
                        pass
                
    f.close()
#    print "ids=", ids
#    print "ids[0]=", ids[0]
#    print "len(ids[0])=", len(ids[0])
#    print 5/0

except tweepy.TweepError:
    print("tweepy.TweepError=", tweepy.TweepError)#, tweepy.TweepError
except:
    e = sys.exc_info()[0]
    print("Error: %s" % e)
    #print "error."
