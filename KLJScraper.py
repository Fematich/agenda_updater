#!./venv/bin python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Tue Oct 22 18:04:08 2013
"""

import requests, json, re, datetime, pytz
from BeautifulSoup import BeautifulSoup
from google_agenda import makeEvent

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
dateformat=re.compile('(?P<day>\d*) (?P<month>.*) (?P<year>\d*) om (?P<hour>\d*)u(?P<minutes>\d*)')

def ExtractEvent(content):
    page=BeautifulSoup(content)
    post=page.find("div", {"class": "post"})
    _,title,_,date=post.h3(text=True)
    try:    
        text=post.p(text=True)
    except Exception:
        text=''
    mtch=re.search(dateformat,date)
    datum=datetime.datetime(int(mtch.group('year')),months.index(mtch.group('month'))+1,int(mtch.group('day')),int(mtch.group('hour')),int(mtch.group('minutes')))
    return {'title':title,'date':datum.replace(tzinfo = pytz.timezone('Europe/Brussels')),'description':text,'location':'KLJ-lokaal'}
def updateKLJ():
    settings=json.load(open('config.json','r'))
    postid=settings['KLJ']['postid']
    r = requests.get(base_adress+str(postid))
    while r.url!=u'http://kljichtegem.be/events/calendar':
        event=ExtractEvent(r.content)
        print event        
        makeEvent(event)
        postid+=1
        r = requests.get(base_adress+str(postid))
    settings['KLJ']['postid']=postid-1
    json.dump(settings,open('config.json','w'))

if __name__ == '__main__':
    updateKLJ()