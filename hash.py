# -*- encoding: utf-8 -*-
import urllib
import requests
from requests_oauthlib import OAuth1
import json
import click
import pprint
from keys import * # this is your keys.py file!

# CLI params
@click.command()
@click.option('--url', required=True, help='The URL you want to analyze')
@click.option('--rel', default=70, help='Keyword relevancy threshold [default 70%]')
@click.option('--ent', default=1, help='(1) Extract named entities [default], (0) ignore')
@click.option('--con', default=1, help='(1) Extract concepts [default], (0) ignore')
def run(url, rel, ent, con):
    terms = analyzeURL(url,rel, ent, con)

    print "\nKEYWORDS: \n"
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(terms)

    allHash(terms)

##### Analysis functions

# get keywords from URL & initiate hashtag search
def analyzeURL(url, rel, ent, con):
    print "\nGETTING KEYWORDS FROM TEXTABILITY API"
    pl = {'key': Tkey, 'lang': lang, 'url': url, 'tt': 'ec', 'src': 'sdk-python-1.2'}
    h = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
    p = requests.post(api, params=pl, headers=h)
    r = p.json()
    print "\n(Textability API status:", r['status']['msg']+ ", remaining credits:", r['status']['remaining_credits']+")"

    #### ENTITIES ####
    h = []
    try:
      if len(r['entity_list']) > 0 and ent > 0:
        ent = r['entity_list']
        for index in range(len(ent)):
          if int(ent[index]['relevance']) >= rel:
              h.append(ent[index]['form'])
      else:
        pass
    except KeyError:
      pass

    #### CONCEPTS ####
    try:
      if len(r['concept_list']) > 0 and con > 0:
        con = r['concept_list']
        for index in range(len(con)):
          if int(con[index]['relevance']) >= rel:
              h.append(con[index]['form'])
      else:
        pass
    except KeyError:
      pass

    h = sorted(set(h))
    return h

# get hashtags for ONE keyword
def oneHash(a, t):
    u = 'https://ritetag.com/api/v2/ai/twitter/'+urllib.quote_plus(t)
    r = requests.get(u, auth=a)
    tags = []
    print "(RiteTag API status: ("+ str(r.json()['code']) +")",r.json()['message']
    if r.json()['code'] == '200':
        print "\n("+t+"):\n"
        h = r.json()['data']
        try:
            if len(h) > 0:
                for i in range(len(h)):
                    if int(h[i]['color']) > 1:
                        print h[i]['tag']
                        tags.append(h[i]['tag'])
                return sorted(set(tags))
            else:
                pass
        except KeyError:
            pass
    else:
        return None

# get hashtags for ALL keywords
def allHash(l):
    aTags=[]
    a = OAuth1(ck, cs, ot, os)
    print "\nGETTING HASHTAGS FROM RITETAG API\n"
    for t in l:
        x = oneHash(a, t)
        if x is not None:
            aTags.append(x)
    print "\nHASHTAGS:\n"
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(aTags)

if __name__ =='__main__':
    run()
