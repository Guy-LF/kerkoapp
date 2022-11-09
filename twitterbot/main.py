import tweepy
import feedparser

#####
"""
generic twitter posting script with image

intent is to 
1) monitor legato\kerko ATOM feed for new posts
1a) may be necessary to identify a signal in ATOM that implies whether there is permission from the curator to post this item to social media.

2) compose a standard form text from the ATOM syndication data
    eg  "[first author] - [truncated title ...]  [legato permalink] #lipedema #medtwitter"
3) include media image -  eg., "NewLipedemaResearch.jpg"

2b) bonus points -- edit media image dynamically to include entire citation and/or abstract
2c) bonus points -- modify or select image dependent on tags (eg, LF Funded, Imaging, Genetics, open access, etc)

4) if multiple new items, space tweets out over time.  Do not tweet all at once.
4c)  bonus points -- trigger some notification to communications staff to acknowledge that a tweet was made. possibly twitter DM to self. 
"""
####
  
  
def main():
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
 

    #need section to iterate over docket, extract info, and compose tweet
    
    # Upload image
    media = api.media_upload("lf_legato.jpg")
 
    # Post tweet with image
    tweet = "this is test tweet"
    post_result = api.update_status(status=tweet, media_ids=[media.media_id])

    

def getdocket():
    """get rss feed and isolate postable information"""
    feed = feedparser.parse("http://feedparser.org/docs/examples/atom10.xml")
    #print('Number of posts in RSS feed :', len(feed.entries))
    docket = []
    for entry in feed.entries:
        date_tuple = entry.created_parsed
      
        # !!! need an if/then to compare publication date to today's date 
      
        docket.append({
            "title":entry.title,
            "description":entry.description,
            "url":entry.url,
            #lf funded tag?
            }
            )
    return docket

def compose_tweet(docket_item):
    """return text, media intended for posting to twitter
    likey needs to pick different media depending on whether project is LF funded or not (maybe other tags as well) 
    """
    return


if __name__ == "__main__":
    main()
