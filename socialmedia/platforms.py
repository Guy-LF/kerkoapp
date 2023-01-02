
import tweepy
import os
from time import sleep
from dotenv import load_dotenv
import imagemaker as im 
import socialmediaconfig as config
load_dotenv()
  
class Twitter():
    def __init__(self):
        self.api = self.auth()
        return
    def auth(self):
        twitter_auth_keys = {
            "consumer_key"        : os.getenv("consumer_key"),
            "consumer_secret"     : os.getenv("consumer_secret"),
            "access_token"        : os.getenv("access_token"),
            "access_token_secret" : os.getenv("access_token_secret")
        }

        auth = tweepy.OAuth1UserHandler(
                twitter_auth_keys['consumer_key'],
                twitter_auth_keys['consumer_secret']
                )
        auth.set_access_token(
                twitter_auth_keys['access_token'],
                twitter_auth_keys['access_token_secret']
                )
        self.api = tweepy.API(auth)
        return(self.api)

    #necessary only for creating testing accounts
    def kill_recent(self):
        """destroy recent posts"""
        recent = self.api.user_timeline()
        for x in recent:
            self.api.destroy_status(x.id)
        return(True)
    #necessary only for creating testing accounts
    def kill_favorites(self):
        recent = self.api.get_favorites()
        for x in recent:
            self.api.destroy_favorite(x.id)
        return(True)
    def kill_favorites_count(self, count):
        while count > 0:
            self.kill_favorites()
            print(count)
            count -= 20
            sleep(20)
        return
    
    def notify(self, text=None):
      """ideally this will send a DM to the social media account to alert them that new info was recently posted"""
      #currentkly does not work - may require OAuth2.0 tokens
      if not text:
          text = "A post has been made by the Legato library to social media"
      for person in config.notified_twitter_accounts:
          x = self.api.send_direct_message(person,text)
      return
    
    def post(self,open_access=False, funded=False, add_image=True, text="This is a test", 
             title="Not available", author="Not available",abstract="Not availalable",year="Not available"):
        # Upload image  (this may need to be platform specific)
        
        if add_image:
            media = self.api.media_upload("lf_legato.png")
            if open_access:
                media = self.api.media_upload("lf_legato_oa.png")
            if funded:
                media = self.api.media_upload("lf_legato_funded.png")
            if (funded and open_access):
                media = self.api.media_upload("lf_legato_funded_oa.png")
            
            #create image of abstract
            x = im.main(title=title, abstract=abstract, author=author, year=year)       
            media2 = self.api.media_upload("abstract.png")
        else:
            media = None
            media2 = None

        # Post tweet with image
        if media:
            post_result = self.api.update_status(status=text, media_ids=[media.media_id, media2.media_id])
        else:
            post_result = self.api.update_status(status=text)
            
        return(post_result.id)
    
#class LinkedIn():
#    #same as twitter
#    def auth():
#        return
#    def post():
#        return
