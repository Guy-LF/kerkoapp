#this config file holds modifiable parameters related to automated posting of new items to social media
#note that a separate .env file is necessary to provide access keys for social media accounts

#main ATOM url
url="http://lipedemalib1222.staging.whiskyechobravo.com/bibliography/atom.xml"

#ATOM url for lf funded facet
url_funded="http://lipedemalib1222.staging.whiskyechobravo.com/bibliography/atom.xml?topic=LF+Funded"

#ATOM url for open access facet
url_oa="http://lipedemalib1222.staging.whiskyechobravo.com/bibliography/atom.xml?topic=Open+Access"


#data governing how many times each item is posted and delays between postings
max_post = 5 #used for testing, limits number of new records posted to social media
timeout = 20 #number of seconds of rest between each post
repeat_post_number = 0 #how many times should the set of posts be repeated? 0 means each item is posted only once. 
repeat_post_delay = (3600*12) #number of seconds to wait between reposts of the series


#need a better solution to this, apparently Twitter really doesn't like bot DMs
#when posts are made, these accounts will be notified via twitter DM
#notified_twitter_accounts = ["@adipotestingbot", "@guyeakin"]
