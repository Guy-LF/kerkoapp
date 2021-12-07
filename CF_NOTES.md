# Project purpose 
add user customizable fields to kerkoapp. This should harvest one or more fieldnames and values
form the Zotero `EXTRA` field. 

some secondary, lower priority goals are defined in the TASKS section

# Conventions
Blocks of newly introduced or changed code are commented `#CF` or `#CF experimental` to facilitate searching


# Tasks

### Planned Kerkoapp changes
* Primary
[x] provide environment variable defining novel fields 
[] extract novel fields from Zotero `EXTRA` field and pass to `Composer.add_field`
>This is begun in `app/config.py` but an error is being thrown by the passage of too many arguments
>in the __init__ at line 144 should be simple to change -- just not seeing it at time of writing

* Secondary
[] supress fields -- prevent rendering to template of fields such as the `EXTRA` field
[] clean up tags -- create a presentation alias for tags (example `[LL] Test` cleaned and reported as `Test` 

### Planned Template changes
* Primary
[] Overwrite item detail template to include customized fields

* Secondary
[] If item has `open access` tag  -- change "Online Resource" function to acknowledge that full text is available through the URL
[] confirm that URL above is derived from zotero `URL` field
[] If item has `Missing Files` tag - add note to item detail that the liplibrary is not in possesion of the article
 


## Novel Fields - Extrafield -> new kerkoapp fields

### per David Lesieur email
Pulling data from the Extra field should be a bit easier than pulling from notes as there is no 
risk for the data to get mixed with HTML in the Extra field. That would require 
forking KerkoApp 
and adding the new fields with calls to self.KERKO_COMPOSER.add_field() at the bottom of 
app.Config.__init__(). 

Kerko has helper functions for pulling data from other fields using a regex. 

Then the forked app could also override Kerko's item template in order to display the 
new fields nicely.








