"""
generic SM posting script with image

intent is to 
1) monitor legato\kerko main ATOM feed for new posts
1a) monitor legato search feeds for LF Funded and Open Access items

2) compose a standard form text from the ATOM syndication data
    eg  "[first author] - [truncated title ...]  [legato permalink] #lipedema #medtwitter"
2a) include media image -  eg., "NewLipedemaResearch.jpg"
2b) bonus points -- edit media image dynamically to include entire citation and/or abstract
2c) bonus points -- modify or select image dependent on tags (eg, LF Funded, Imaging, Genetics, open access, etc)

3) Post to SM
3a) if multiple new items, space posts out over time.  Do not tweet all at once.
3b)  bonus points -- trigger some notification to communications staff to acknowledge that a tweet was made. possibly twitter DM to self. 

3c) consider cross posting to multiple SM accounts -- eg., LinkedIn - https://pypi.org/project/python3-linkedin/
"""
####


import feedparser
import os
from dotenv import load_dotenv
load_dotenv()

from platforms import Twitter

def get_previously_published():
    return

def parse_test():
    d = feedparser.parse('./atomfeed-sample.xml')
    itemlist = [x.guid for x in d['entries']]
    return(d, itemlist)

def getfeeds(url=None, url_funded=None, url_oa=None):
    """retrieve atom main feed, open access item ids, and lf funded item ids. """
    
    #testing urls 
    if ((not url) and (not url_funded) and (not url_oa)):
        url="https://demo.kerko.whiskyechobravo.com/bibliography/atom.xml",
        url_funded="https://demo.kerko.whiskyechobravo.com/bibliography/atom.xml?topic=JTZGXUV6",
        url_oa="https://demo.kerko.whiskyechobravo.com/bibliography/atom.xml?topic=HRXC7ZKM"
    
    #pull main feed and list if ids
    feed = feedparser.parse(url)
    feed_ids = [x.guid for x in feed['entries']]
    
    ##create list of ID's associated with specific tags
    openaccess_ids = [x.guid for x in \
        feedparser.parse(url_oa)['entries']]
    lf_funded_ids = [x.guid for x in \
        feedparser.parse(url_funded)['entries']]
    return({
        "feed":feed,
        "feed_ids":feed_ids,
        "openaccess_ids":openaccess_ids,
        "lf_funded_ids":lf_funded_ids,
        })

def get_history():    
    with open("history.txt") as f:
        history = f.readlines()
        # remove new line characters
        history = [x.strip() for x in history]
    return(history)

def compare_to_history(feed, history):
    """return list of item ids from feed that are NOT recorded in the history logfile"""
    postable_ids = [x for x in feed if (x not in history)]
    return(postable_ids)
    
def harvest_item_data(feed, postable_ids, openaccess_ids, lf_funded_ids):
    #receive cleaned entries and harvest data needed for posting
 
    docket = []
    gen = (entry for entry in feed.entries if (entry.guid in postable_ids))
    
    for entry in gen:  #limit entries only to those that are 'postable'
    
        #todo: might be necessary to examine item creation date and 
        #decline to post if older than x days
        
        #assign open access and funded 'tags'
        oa = False
        funded = False
        
        if entry.guid in openaccess_ids:
            oa = True
        if entry.guid in lf_funded_ids:
            funded = True
      
        docket.append({
            "title":entry.title,
            "abstract":entry.summary, #abstract
            "author":entry.author_detail.name.split(',')[0],      # last name of first author
            "year":entry.updated_parsed.tm_year,                   # this seems to be article publication date (year)
            "url":entry.link,
            "open access":oa,
            "funded":funded,
            }
            )
    return(docket)

#need section to iterate over docket, extract info, and compose post
def parse_docket(docket):
    parsed_docket = [compose_post(entry) for entry in docket]
    return(parsed_docket)

def compose_post(entry):
    """return text, media intended for posting to social media
    likey needs to pick different media depending on whether project is LF funded or not (maybe other tags as well) 
    """
    temp = f"{entry.author} -!#!- {entry.url} #lipedema #medtwitter"
    remainder = 280 - len(temp)
    entry['post_text'] = temp.replace('-!#!-',entry.title[:remainder])
    entry['add_image'] = True
    #open_access=False, funded=False, add_image=True, text="This is a test")  
    return(entry)


if __name__ == "__main__":
    apis = [
        Twitter(), 
        #LinkedIn(),
    ]
    parse_docket(getdocket())
    for platform in apis:
        platform.post(text)
            
    main_twitter()
