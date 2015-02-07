# -*- encoding: utf-8 -*-
import urllib
import re
import requests
from requests_oauthlib import OAuth1
import json
import click
import pprint
from ftfy import fix_text
from readability import ParserClient
from keys import * # this is your keys.py file!

# CLI params
@click.command()
@click.option('--url', required=True, help='The URL you want to analyze')
@click.option('--rel', default=70, help='Keyword relevancy threshold [default 70%]')
@click.option('--ent', default=1, help='(1) Extract named entities [default], (0) ignore')
@click.option('--con', default=1, help='(1) Extract concepts [default], (0) ignore')
def run(url, rel, ent, con):
    txt = getHTML(url)
    print txt

    terms = analyze(txt, rel, ent, con)

    print "\nKEYWORDS: \n"
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(terms)

    allHash(terms)

##### Analysis functions

# get keywords from URL & initiate hashtag search
def analyze(txt, rel, ent, con):
    print "\nGETTING KEYWORDS FROM TEXTALYTICS API"
    pl = {'key': Tkey, 'lang': lang, 'txt': txt, 'txtf': 'markup', 'tt': 'ec', 'src': 'sdk-python-1.2'}
    h = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
    p = requests.post(api, params=pl, headers=h)
    r = p.json()
    print "\n(Textalytics API status:", r['status']['msg']+ ", remaining credits:", r['status']['remaining_credits']+")"

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
    print "\n["+t+"] (RiteTag API status: ("+ str(r.json()['code']) +")",r.json()['message']

    if str(r.json()['code']) == '200':
        h = r.json()['data']

        try:
            if len(h) > 0:
                for i in range(len(h)):
                    if int(h[i]['color']) > 1:
                        #print h[i]['tag']
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
        if x:
            aTags.append(x)
    print "\nHASHTAGS:\n"

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(aTags)

def getHTML(url):
    print '\nPROCESSING URL'
    parser = ParserClient(rk)
    p = parser.get_article_content(url)
    html = p.content['content']
    #print cleanHTML(html)
    return cleanHTML(html)

def cleanHTML(html) :
    h = re.sub(u'[\u02bc\u2018\u2019\u201a\u201b\u2039\u203a\u300c\u300d]',"'",html)
    # Replace "smart" and other double-quote like things
    h = re.sub(u'[\u00ab\u00bb\u201c\u201d\u201e\u201f\u300e\u300f]','"', h)
    # Replace copyright symbol
    h = re.sub(u'[\u00a9\u24b8\u24d2]', '(c)', h)
    # Replace registered trademark symbol
    h = re.sub(u'[\u00ae\u24c7]', '(r)', h)
    # Replace sound recording copyright symbol
    h = re.sub(u'[\u2117\u24c5\u24df]', '(p)', h)
    # Replace service mark symbol
    h = re.sub(u'[\u2120]', '(sm)', h)
    # Replace trademark symbol
    h = re.sub(u'[\u2122]', '(tm)', h)
    # Replace em & em dashes
    h = re.sub(u'[\u2013]', '&ndash;', h)
    h = re.sub(u'[\u2014]', '&mdash;', h)
    # weird hyphen replace
    h = re.sub(u'[\xad]', '&shy;', h)
    # Replace/clobber any remaining UTF-8 characters that aren't in ISO-8859-1
    #print fix_text(h)
    return fix_text(h)

if __name__ =='__main__':
    run()
