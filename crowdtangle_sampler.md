

```python
import urllib3
import json
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

### https://github.com/CrowdTangle/API/wiki/Posts
### https://help.crowdtangle.com/en/articles/1189612-crowdtangle-api
```


```python

```


```python
token = ""
```


```python
dataset=pd.DataFrame()
```

#### Key: Made a list of keywords for which I need the reddit posts


```python
#key=["covid", "coronavirus","covid19","covid-19","hospital","mask","death","infection","quarantine","virus","symptom","flu","smell","cough","fever","circuitbreaker","wuhan virus","chinese virus"]

```

#### Now traverse the Key list and fetch the reddit data. Some key parameters in url.
#### Fetched the data for all keywords of "Key" list and appended the data all together to generate single CSV file i.e. "dataset".

code below


```python
for i in range(0,len(key)):
    print(i)
    nexturl = 'https://api.crowdtangle.com/posts/search?token='+token+'&sortBy=date&startDate=2014-11-11T00:00:00&endDate=2014-11-19T00:00:00&searchTerm='+key[i]+'&count=100'
    while(nexturl.strip()):
        time.sleep(20)
        print(nexturl)
        response = requests.get(nexturl)    
        dict = response.json()
        
        if 'result' in dict.keys():
            df = pd.DataFrame(dict['result']['posts'])
            df["Label"]=str(key[i])
            dataset = pd.concat([dataset, df], ignore_index=True)
            if 'nextPage' in dict['result']['pagination'].keys():
                nexturl = dict['result']['pagination']['nextPage']
            else:
                nexturl=''
        else:
            print(dict)
            nexturl=''
    
```

#### Number of posts fetched



```python
dataset.shape
```




    (15665, 22)



#### Count of number of posts for each keyword


```python
dataset.Label.value_counts()
```




    %23lockdown                65536
    %23socialdistancing        65536
    %23sgunited                33367
    %23movementcontrolorder     9681
    %23circuitbreaker           1372
    %23sgtogether               1232
    %23safedistancing            594
    %23igsingapore               538
    %23stayhomesg                 89
    %23circuitbreakersg           43
    %23sgcircuitbreaker           17
    %23stayhomeforsg               9
    Name: Label, dtype: int64



#### Saving csv


```python
dataset.to_csv('sample.csv', index=False) 
```
