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

import tweepy
import feedparser
from dotenv import load_dotenv
load_dotenv()

#probably rewrite this as a class , incorporating auth and posting as attributes/fxns     
class Twitter():
    def auth():
        twitter_auth_keys = {
            "consumer_key"        : "REPLACE_THIS_WITH_YOUR_CONSUMER_KEY",
            "consumer_secret"     : "REPLACE_THIS_WITH_YOUR_CONSUMER_SECRET",
            "access_token"        : "REPLACE_THIS_WITH_YOUR_ACCESS_TOKEN",
            "access_token_secret" : "REPLACE_THIS_WITH_YOUR_ACCESS_TOKEN_SECRET"
        }

        auth = tweepy.OAuth1UserHandler(
                twitter_auth_keys['consumer_key'],
                twitter_auth_keys['consumer_secret']
                )
        auth.set_access_token(
                twitter_auth_keys['access_token'],
                twitter_auth_keys['access_token_secret']
                )
        api = tweepy.API(auth)
        return(api)

    def post(open_access=False, funded=False):
        # Upload image  (this may need to be platform specific)
        media = api.media_upload("lf_legato.jpg")
        if open_access:
            media = api.media_upload("lf_legato.jpg")
        if funded:
            media = api.media_upload("lf_legato.jpg")
        if (funded and open_access):
            media = api.media_upload("lf_legato.jpg")
        

        # Post tweet with image
        tweet = "this is test tweet"
        post_result = self.api.update_status(status=tweet, media_ids=[media.media_id])
        return()
    
class LinkedIn():
    #same as twitter
    def auth():
        return
    def post():
        return
    
    
def getdocket():
    """get ATOM feeds and isolate postable information"""
    feed = feedparser.parse("http://feedparser.org/docs/examples/atom10.xml")
    
    ##create list of ID's associated with specific tags
    openaccess = [x for x.guid in feedparser.parse("http://feedparser.org/docs/examples/atom10.xml")]
    lf_funded = [x for x.guid in feedparser.parse("http://feedparser.org/docs/examples/atom10.xml")
    
    #print('Number of posts in RSS feed :', len(feed.entries))
    docket = []
    for entry in feed.entries:
        oa = False
        funded = False
        
        date_tuple = entry.created_parsed
        # !!! need an if/then to compare ATOM publication date to today's date 
                 
        if entry.guid in openaccess:
            oa = True
        if entry.guid in lf_funded:
            funded = True
      
        docket.append({
            "title":entry.title,
            "description":entry.description,
            # first author
            # article publication date (year)
            "url":entry.url,
            "open access":oa,
            "funded":funded,
            }
            )
    return docket

#need section to iterate over docket, extract info, and compose post
def parse_docket(docket):
    for item in docket:
        compose_post(item)
    return

def compose_post(docket_item):
    """return text, media intended for posting to social media
    likey needs to pick different media depending on whether project is LF funded or not (maybe other tags as well) 
    """
    text = ""
    image_default = ""
    image_funded = ""
      
    return


if __name__ == "__main__":
    apis = [Twitter(), LinkedIn()]
    parse_docket(getdocket())
    for platform in apis:
        platform.post(text)
            
    main_twitter()
