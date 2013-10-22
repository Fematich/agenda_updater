#!./venv/bin python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Tue Oct 22 18:04:08 2013
"""

import requests
from BeautifulSoup import BeautifulSoup
import json

base_adress='http://kljichtegem.be/events/view/'
month_labels='''
januari
februari
maart
april
mei
juni
juli
augustus
september
oktober
november
december
'''
months=month_labels.split()

def ExtractEvent(content):
    page=BeautifulSoup(content)
    post=page.find("div", {"class": "post"})
    _,title,_,date=post.h3(text=True)
    try:    
        text=post.p(text=True)
    except Exception:
        text=''
    return title,date,text

if __name__ == '__main__':
    settings=json.load(open('config.json','r'))
    postid=settings['postid']
    r = requests.get(base_adress+str(postid))
    while r.url!=u'http://kljichtegem.be/events/calendar':
        print ExtractEvent(r.content)
        postid+=1
        r = requests.get(base_adress+str(postid))
    settings['postid']=postid-1
    json.dump(settings,open('config.json','w'))