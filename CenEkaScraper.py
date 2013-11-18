#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Mon Nov 18 17:50:17 2013
"""

import requests, json, re, datetime, pytz
from BeautifulSoup import BeautifulSoup
from google_agenda import makeEvent

base_adress='http://ceneka.ugent.be/ceneka/activiteit/'
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
#dateformat=re.compile('(?P<day>\d*) (?P<month>.*) (?P<year>\d*) om (?P<hour>\d*)u(?P<minutes>\d*)')
dateblock=re.compile('<p> <b>Datum:</b>(?P<day>\d*) (?P<month>.*) (?P<year>\d*) </p>')
placeblock=re.compile('<p> <b>Locatie:</b>(?P<place>.*) </p>')
def ExtractEvent(content):
    page=BeautifulSoup(content)
    post=page.find("div", {"id": "activity-detail"})
    title=str(post.h1(text=True)[0])
    dateloc=str(page.find("div", {"class": "dateLocation"}))
    pmtch=re.search(placeblock,dateloc)
    location=pmtch.group('place')
    try:    
        text=' '.join(post.find("div", {"class": "description"})(text=True)).replace('\r','').replace('\n','')
    except Exception:
        text=''
    mtch=re.search(dateblock,dateloc)
    datum=datetime.datetime(int(mtch.group('year')),months.index(mtch.group('month'))+1,int(mtch.group('day')),0,0)
    return {'title':title,'date':datum.replace(tzinfo = pytz.timezone('Europe/Brussels')),'description':text,'location':location}
def updateCenEka():
    settings=json.load(open('config.json','r'))
    postid=settings['CenEka']['postid']
    r = requests.get(base_adress+str(postid))
    while r.content!=u'<h1>Server Error (500)</h1>':
        event=ExtractEvent(r.content)
        event['description']+='\n link:http://ceneka.ugent.be/ceneka/activiteit/%d'%postid
        print event        
        makeEvent(event)
        postid+=1
        r = requests.get(base_adress+str(postid))
    settings['KLJ']['postid']=postid-1
    json.dump(settings,open('config.json','w'))

if __name__ == '__main__':
    updateCenEka()