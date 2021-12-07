# Project purpose 
Add user customizable fields to kerkoapp. This should harvest one or more fieldnames and values from the Zotero `EXTRA` field.  An example use-case is to harvest Pubmed identfier numbers encoded in Zotero `Extra` field  (eg., "PMID:123456"). These could either be represented as an identifier number in the kerkoapp template, or "urlized" to "https://pubmed.ncbi.nlm.nih.gov/123456/" in order to provide a link back to their pubmed record.

Some secondary, lower priority goals are defined in the TASKS section

# Conventions
Blocks of newly introduced or changed code are commented `#CF` or `#CF experimental` differentiate from kerkoapp core


# Tasks

### Planned Kerkoapp changes
* Primary
  * provide environment variable defining novel fields 
  * extract novel fields from Zotero `EXTRA` field and pass to `Composer.add_field`
>This is begun in `app/config.py` but an error is being thrown by the passage of too many arguments
>in the __init__ at line 144 should be simple to change -- just not seeing it at time of writing.
>One concern is that some fields may have a 1 to many relationship to Values.  An example is that 
>if funding support is recorded in Zoetero `Extra` as FS (eg., FS:agency1, FS:agency2) the Regex will 
>need to capture both values (eg., [agency1, agency2]) and make them separately accessible to the template engine 

* Secondary
  * clean up tags -- create a presentation alias for tags (example `[LL] Test` cleaned and reported as `Test`, deleting the [LL] string for readability )

### Planned Template changes
* Primary
  * Overwrite item detail template to report customized fields

* Secondary
  * supress fields -- prevent rendering to template of fields (such as the `EXTRA` field, which may contain strngs not intended for general audiences). Given Kerko's reliance on 'extra' for DOI and related values, it seems unlikely that it can be suppressed with the Compose `exclude_default_fields` param.  If that is true, then suppressing at the template rendering stage is acceptable.
  * If item has `open access` tag  -- change "Online Resource" function to acknowledge that full text is available through the URL.
  * confirm that URL above is derived from Zotero `URL` field
  * If item has `Missing Files` tag - add note to item detail that the liplibrary is not in possesion of the article
 











