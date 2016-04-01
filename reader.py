import json
import os
import nltk
import re
import time

import csv
import time


def clean(content):
    content = content.replace('\n',"")
    content = content.replace('\t',"")
    content = content.replace(',',"")
    content = content.replace('\r',"")
    return content

count=0
fl = open("C:\\Users\\jaidka\\Desktop\\election_dump.sql","r")
f2 = open("randomfile","w")

month='Jan'
day=0
x=fl.readline()
x=fl.readline()
for line in fl :
       print line
       ca = ''
       idstr = ''
       txt = ''
       in_reply_to = ''
       in_reply_to_user = ''
       name = ''
       usr = ''
       location = ''
       description = ''
       folcount = ''
       fricount = ''
       created = ''
       coord1 = ''
       coord2 = ''
       coord3 = ''
       coord4 = ''
       coord5 = ''
       retweet = ''
       timezone = ''
       user_fav = ''
       fav = ''
       link=''
       status = line.split('\t')[1].replace("\\\\","\\\\\\")
       
       
#       status = '{"contributors": null, "truncated": false, "text": "RT @BloggerNetwork2: Gas pricing issue: FIR filed after Arvind Kejriwal`s allegations; Mukesh Ambani, Veerappa Moily name http://t.co/LOfYO\\u2026", "in_reply_to_status_id": null, "id": 436289104012410881, "favorite_count": 0, "source": "<a href=\\"http://twitter.com/download/iphone\\" rel=\\"nofollow\\">Twitter for iPhone</a>", "retweeted": false, "coordinates": null, "entities": {"symbols": [], "user_mentions": [{"id": 2273178612, "indices": [3, 19], "id_str": "2273178612", "screen_name": "BloggerNetwork2", "name": "Blogger Network"}], "hashtags": [], "urls": [{"url": "http://t.co/LOfYOxF1HH", "indices": [139, 140], "expanded_url": "http://fb.me/3cIdQE5a5", "display_url": "fb.me/3cIdQE5a5"}]}, "in_reply_to_screen_name": null, "id_str": "436289104012410881", "retweet_count": 0, "in_reply_to_user_id": null, "favorited": false, "retweeted_status": {"contributors": null, "truncated": false, "text": "Gas pricing issue: FIR filed after Arvind Kejriwal`s allegations; Mukesh Ambani, Veerappa Moily name http://t.co/LOfYOxF1HH", "in_reply_to_status_id": null, "id": 433616600478928897, "favorite_count": 0, "source": "<a href=\\"http://www.facebook.com/twitter\\" rel=\\"nofollow\\">Facebook</a>", "retweeted": false, "coordinates": null, "entities": {"symbols": [], "user_mentions": [], "hashtags": [], "urls": [{"url": "http://t.co/LOfYOxF1HH", "indices": [101, 123], "expanded_url": "http://fb.me/3cIdQE5a5", "display_url": "fb.me/3cIdQE5a5"}]}, "in_reply_to_screen_name": null, "id_str": "433616600478928897", "retweet_count": 0, "in_reply_to_user_id": null, "favorited": false, "user": {"follow_request_sent": null, "profile_use_background_image": true, "default_profile_image": false, "id": 2273178612, "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png", "verified": false, "profile_image_url_https": "https://pbs.twimg.com/profile_images/418800833044549633/D8qoEjtP_normal.jpeg", "profile_sidebar_fill_color": "DDEEF6", "profile_text_color": "333333", "followers_count": 7, "profile_sidebar_border_color": "C0DEED", "id_str": "2273178612", "profile_background_color": "C0DEED", "listed_count": 0, "is_translation_enabled": false, "utc_offset": null, "statuses_count": 2287, "description": "World News", "friends_count": 11, "location": "", "profile_link_color": "0084B4", "profile_image_url": "http://pbs.twimg.com/profile_images/418800833044549633/D8qoEjtP_normal.jpeg", "following": null, "geo_enabled": false, "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png", "name": "Blogger Network", "lang": "it", "profile_background_tile": false, "favourites_count": 0, "screen_name": "BloggerNetwork2", "notifications": null, "url": "http://www.blogger-net.com", "created_at": "Thu Jan 02 15:36:14 +0000 2014", "contributors_enabled": false, "time_zone": null, "protected": false, "default_profile": true, "is_translator": false}, "geo": null, "in_reply_to_user_id_str": null, "possibly_sensitive": false, "lang": "en", "created_at": "Wed Feb 12 15:00:28 +0000 2014", "in_reply_to_status_id_str": null, "place": null}, "user": {"follow_request_sent": null, "profile_use_background_image": true, "default_profile_image": false, "id": 156666863, "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme16/bg.gif", "verified": false, "profile_image_url_https": "https://pbs.twimg.com/profile_images/1422955176/c-store_normal.jpg", "profile_sidebar_fill_color": "DDFFCC", "profile_text_color": "333333", "followers_count": 2096, "profile_sidebar_border_color": "BDDCAD", "id_str": "156666863", "profile_background_color": "9AE4E8", "listed_count": 24, "is_translation_enabled": false, "utc_offset": -21600, "statuses_count": 24184, "description": "C-Store News\\r\\nCar Wash Marketing \\r\\nC-Store Marketing\\r\\nC-Store Category Reviews\\r\\nCPG Reviews", "friends_count": 2306, "location": "Chicago", "profile_link_color": "0084B4", "profile_image_url": "http://pbs.twimg.com/profile_images/1422955176/c-store_normal.jpg", "following": null, "geo_enabled": false, "profile_background_image_url": "http://abs.twimg.com/images/themes/theme16/bg.gif", "name": "C-Store News ", "lang": "en", "profile_background_tile": false, "favourites_count": 23, "screen_name": "CStoreNews_", "notifications": null, "url": "http://cstorenews.blogspot.com/", "created_at": "Thu Jun 17 15:20:29 +0000 2010", "contributors_enabled": false, "time_zone": "Central Time (US & Canada)", "protected": false, "default_profile": false, "is_translator": false}, "geo": null, "in_reply_to_user_id_str": null, "possibly_sensitive": false, "lang": "en", "created_at": "Thu Feb 20 00:00:02 +0000 2014", "filter_level": "medium", "in_reply_to_status_id_str": null, "place": null}'
       
              
       status = json.loads(status)
       ca = status['created_at']
       monthnew = ca.split(' ')[1]
       daynew = ca.split(' ')[2]
       if (monthnew!=month):
           f2.close()
           f2 = open("\\"+monthnew+"\\"+daynew+".csv","a")
           f2.write("statusdateposted,useridstring,statuscontent,statusinreplytostatusid,statusinreplytoscreenname,username,userscreename,statustimezone,userlocation,userdescription,userfolcount,userfriendcount,useraccountcreated,userpostsmade,usercoordinates,userplace,statusgeoname,statusgeocountrycode,statusgeocountry,statusretweetcount,statusfavs,link,userfavs"  )
           month=monthnew
           day=daynew
       idstr = status['id_str']
       txt = status['text']
       txt = clean(txt)
       in_reply_to = status['in_reply_to_status_id']
       in_reply_to_user = status['in_reply_to_screen_name']
       name = status['user']['name']
       name = clean(name)
       usr = status['user']['screen_name']
       usr = clean(usr)
       location = status['user']['location']
       location = clean(location)
       if 'description' in 'user':
           description = status['user']['description']
           description = clean(description)
       folcount = status['user']['followers_count']
       fricount = status['user']['friends_count']
       created = status['user']['created_at']
       statcount = status ['user']['statuses_count']
       coord1 = status['coordinates']
       if 'place' in status:
           coord2 = status['place']
       #    coord2 = clean(coord2)
       timezone = status['user']['time_zone']
       if 'name' in 'geo':
           coord3 = status['geo']['name']
       coord3 = clean(coord3)
       if 'country_code' in 'geo':
           coord4 = status['geo']['country_code']
       coord4 = clean(coord4)
       if 'country' in 'geo':
           coord5 = status['geo']['country']
       coord4 = clean(coord4)
       retweet = status['retweet_count']
       if 'favourite_count' in status:
           fav = status['favourite_count']
       if 'urls' in 'entities':
           link = status['entities']['urls']['expanded_url']
       coord3 = clean(coord3)
       user_fav = status['user']['favourites_count']
       entry = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (ca,idstr,txt,in_reply_to,in_reply_to_user,name,usr,timezone,location,description,folcount,fricount,created,statcount,coord1,coord2,coord3,coord4,coord5,retweet,fav,link,user_fav)
       entry = entry.encode('utf-8')
       f2.write(entry)
       count=count+1
       #print txt
       if count>99:
           exit()
fl.close() 
