"""
generic SM posting script with image

intent is to 
1) monitor legato\kerko main ATOM feed for new posts
1a) monitor legato search feeds for LF Funded and Open Access items, flagging new posts appropriately

2) compose a standard form text from the ATOM syndication data
    eg  "[first author] - [truncated title ...]  [legato permalink] #lipedema"
    
    
2a) include a specific media image dependent on tags (eg, LF Funded, Open Access)

3) Post to SM
3a) if multiple new items, space posts out over time.  Do not tweet all at once.
3b) consider cross posting to multiple SM accounts -- eg., LinkedIn - https://pypi.org/project/python3-linkedin/
"""
####


import feedparser
import os
from time import sleep
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

from platforms import Twitter
import socialmediaconfig as config




def getfeeds(url=None, url_funded=None, url_oa=None):
    """retrieve atom main feed, open access item ids, and lf funded item ids. """
    
    #testing urls 
    if ((not url) and (not url_funded) and (not url_oa)):
        url = config.url
        url_funded = config.url_funded
        url_oa = config.url_oa

    #pull main feed and list if ids
    feed = feedparser.parse(url)
    feed_ids = [x.guid for x in feed['entries']]
    
    ##create list of ID's associated with specific tags
    openaccess_ids = [x.guid for x in \
        feedparser.parse(url_oa)['entries']]
    lf_funded_ids = [x.guid for x in \
        feedparser.parse(url_funded)['entries']]
    
    print(f"found {len(feed_ids)} items in main feed")
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

def compare_to_history(feed_ids, history):
    """return list of item ids from feed that are NOT recorded in the history logfile"""
    postable_ids = [x for x in feed_ids if (x not in history)]
    print(f"found {len(postable_ids)} postable items relative to {len(history)} previously posted items")
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
        
        try:
            title = entry.title
        except:
            title = ''
        try:
            abstract = entry.summary #abstract
        except:
            abstract = ''
        try:
            author = entry.author_detail.name.split(',')[0]      # last name of first author
        except:
            author = ''
        try:
            year = f"({entry.updated_parsed.tm_year})"                   # this seems to be article publication date (year)
        except:
            year = ''
        try:
            url = entry.link
        except:
            url = 'https://library.lipedema.org'
        try:
            guid = entry.guid
        except:
            guid = None
    
        docket.append({
            "title":title,
            "abstract":abstract,
            "author":author,      # last name of first author
            "year":year,                   # this seems to be article publication date (year)
            "url":url,
            "open access":oa,
            "funded":funded,
            "guid":guid,
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
    temp = f"{entry['author']} {entry['year']}: -!#!- {entry['url']} #lipedema"
    remainder = 280 - len(temp)
    entry['post_text'] = temp.replace('-!#!-',entry['title'][:remainder])
    entry['add_image'] = True
    return(entry)


def log_ids(item_guid):
    """todo, save ids of posted material to the history.txt file"""
    print(f"---logging: {item_guid}")
    with open('history.txt', 'a', encoding='utf-8') as f:   #append data
        f.write(f'{item_guid}\n')
    return


def main():  
    print(f"------ begin post cycle at {datetime.now().strftime('%Y:%m:%d %H:%M:%S %Z %z')} --------")
    
    max_post = config.max_post #used for testing, limits number of new records posted to social media
    timeout = config.timeout #number of seconds of rest between each post
    repeat_post_number = config.repeat_post_number  #how many times should the set of posts be repeated? 0 means each item is posted only once. 
    repeat_post_delay = config.repeat_post_delay #number of seconds to wait between reposts of the series
    
    feeds = getfeeds()
    history = get_history()
    postable_ids = compare_to_history(feeds['feed_ids'],history)
    docket = harvest_item_data(feeds['feed'],postable_ids,feeds['openaccess_ids'],feeds['lf_funded_ids'])    
    parsed_docket = parse_docket(docket)
    t = Twitter()
    
    while repeat_post_number >= 0:
        print(f"--- {repeat_post_number} cycles of posts remaining")
        for x in parsed_docket[:max_post]:
            print(f"posting {x['guid']}")
            t.post(open_access=x['open access'], funded=x['funded'], add_image=True, text=x['post_text'], 
                title=x['title'], author=x['author'],year=x['year'], abstract=x['abstract'])
            log_ids(x['guid'])
            sleep(timeout)
        repeat_post_number -= 1
        if repeat_post_number > 0:
            print(f"reposting this series {repeat_post_number} more times with {repeat_post_delay} seconds between cycles")
            print(f"beginning at {datetime.now().strftime('%Y:%m:%d %H:%M:%S %Z %z')}")
            sleep(repeat_post_delay)
    print(f" ------- wrapping up at {datetime.now().strftime('%Y:%m:%d %H:%M:%S %Z %z')}")
    return()


if __name__ == "__main__":
    main()          
  
