
"""
scripts to support management of Zotero tags and notes outside of kerko.
Primary purpose to automate the translation of a set of day to day use
tags (used by LF staff) into a summary-set of tags appropriate
for applying as kerko facets.  In practice, this is the translation of [LF]
designated tags to [LL].  The goal is that human hands should not have
to manage the [LL} prefixed tags.
"""


from pyzotero import zotero
from environs import Env
import re
from bs4 import BeautifulSoup



def get_library(max=1):
    """return zotero instance based on .env variables"""
    env = Env()
    env.read_env()
    zot = zotero.Zotero(env("KERKO_ZOTERO_LIBRARY_ID"),
                    env("KERKO_ZOTERO_LIBRARY_TYPE"),
                    env("KERKO_ZOTERO_API_KEY"))
    return(zot)



class Item():
    def __init__(self,zot,zotero_item):
        self.zot = zot
        self.zotero_item = zotero_item
        self.key = zotero_item['key']
        self.title = zotero_item['data']['title']
        print(f'initializing {self.key} - {self.title}')
        #get tags
        self.tags = []
        if self.zotero_item['data']['tags']:
            for x in self.zotero_item['data']['tags']:
                self.tags.append(x['tag'])
        
        #set children or set to none of attachment
        if self.zotero_item['data']['itemType'] == 'attachment':
            self.children = None
            self.marcom_note = None
        else:
            self.children = zot.children(self.key)
            self.marcom_note = self.get_matched_notes()
        
        self.tag_kill_list = ["[LT]","[LL]"]
        self.lookup = {
                '[LF] Testtag':'[LT] Testtag2',
                '[LF] Lipedema': '[LL] Lipedema',
                '[LF] Open Access':'[LL] Open Access',
                '[LF] Funded':'[LL] LF Funded',
                '[LF] Review': '[LL] Review',
                '[LF] Genetics':'[LL] Genetics',
                '[LF] Guidelines and Consensus':'[LL] Guidelines and Consensus',
                '[LF] Primary data': '[LL] Original studies and data',
                '[LF] Therapeutics': '[LL] Therapeutics',
                '[LF] Nutrition': '[LL] Personal management (diet, excercise, nutrition)',
                }
        #this starts as identical to the zotero item, but is updated
        #by class methods (eg, refresh_tags)
        self.updated_item = self.zotero_item
        self.server_needs_updating = False
        self.refresh_tags()
        return

    def save_item(self):
        #save item with self.updated_item info
        #currently DOES NOT update self.zotero_item to reflect current data
        #on server
        if self.server_needs_updating:
            a = self.zot.update_item(self.updated_item)
            if a:
                self.server_needs_updating = False
        return
    
    def refresh_tags(self):
        """remove any tag that contains any given string from a list of strings.
        in practice this function deletes all [LL] tags from the database in
        preparation for freshly reassigning the tags based on a lookup table.

        assess list of tags, and add additional tags based on lookup table"""
    
        #delete old kerko library related tags
        purgedtags = [tag for tag in self.tags if not self.check_tag(tag)]
        if len(purgedtags) < len(self.tags):
            self.server_needs_updating = True

        #assign new tags based on lookup,
        #old, but correct tags are reapplied
        newtags = []
        for tag in purgedtags:
            if self.lookup.__contains__(tag):
                newtags.append({'tag':self.lookup[tag],'type': 0})
                newtags.append({'tag':tag,'type': 0}) #also add back the non [ll] version of the tag
                self.server_needs_updating = True
            else:
                newtags.append({'tag':tag,'type': 0})
        self.updated_item['data']['tags'] = newtags
        return

    def check_tag(self, tag):
        """return true if any string from a list of strings can be found in
        a given tag.
        Used to strip out all lip library related tags so that they can be
        freshly reassigned"""
        result = False
        for item in self.tag_kill_list:
            if item in tag:
                result = True
            else:
                pass
        return(result)

    def get_matched_notes(self, re_pattern=r'#marcom', strip_html=True):
        """retrieve notes as list of string that contain an re_pattern.
        return note stripped of html by setting strip_html=True

        proof of concept to see if notes prefaced by '#marcom' can be isolated
        and stripped of html tags such that note contents could be shared through
        kerko, or even Social Media API's
        """
        notes = []
        for child in self.children:
            text = None
            if self.zotero_item['data']['itemType'].lower() == 'note':
                match = re.subn(re_pattern,"",self.zotero_item['data']['note'])
                if match[1] > 0:
                    if strip_html:
                        text = BeautifulSoup(match[0]).get_text()
                    else:
                        text = match[0]
                else:
                    pass
                notes.append(text)
        return(notes)



def make_item_inventory(zot):
    """get all items from library and return a list of item object"""

    #get zotero library
    zot = get_library(max=1)
    zot.add_parameters(tag="[LF] Lipedema || [LF] Lipedema related or referenced")
    item_list = zot.everything(zot.top())
    items = []
    j = 1
    for item in item_list:
        print(f'{j}/{len(item_list)} - {item["key"]}')
        items.append(Item(zot,item)) #create Item objects, 
        j += 1
    return(items)


if __name__ == "__main__":
    items = make_item_inventory(get_library())
    i = len(items)
    j = 1
    for x in items:
        print(f'saving {j} of {i} items') 
        x.save_item()
        j += 1
    pass

#snippets
# from zotero_helpers import *; zot = get_library(); item_list = zot.everything(zot.top())
# ii = item_list[0]; i = Item(zot, item_list[0])

import pprint
pp = pprint.PrettyPrinter(indent=2, depth=4).pprint


