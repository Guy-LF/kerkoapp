# Project purpose
Add user customizable fields to kerkoapp. This should harvest one or more fieldnames and values from the Zotero `EXTRA` field.  An example use-case is to harvest Pubmed identfier numbers encoded in Zotero `Extra` field  (eg., "PMID:123456"). These could either be represented as an identifier number in the kerkoapp template, or "urlized" to "https://pubmed.ncbi.nlm.nih.gov/123456/" in order to provide a link back to their pubmed record.

Some secondary, lower priority goals are defined in the TASKS section

# Conventions
Blocks of newly introduced or changed code relative to orginal whiskey bravo kerkoapp are commented `#CF` or `#CF experimental` to differentiate from kerkoapp core


# Tasks

### Kerkoapp changes

* custom fields from zotero EXTRA content
  * extract novel fields from Zotero `EXTRA` field and pass to `Composer.add_field`
  * this is accomplished in config.py by declaration of field_keys `cf_VARIABLE` where `VARIABLE` is the name of the field. Regex expressions are used agains each line of the `EXTRA` field, to harvest text coded in the form `VARIABLE:text`.
  * Custom fields are rendered below standard fields in the item template. `EXTRA` is suppressed from rendering by the KERKOAPP_EXCLUDE_DEFAULT_FIELDS environment variable.

* pretty tags
  * create a presentation alias for tags (example `[LL] Test` cleaned and reported as `Test`, deleting the [LL] string for readability )
  * This is controlled by regex defined in `config.py` `tag_cleanup_pattern`. Currently the `[LL]` and `[LF]` tags are cleaned in this fashion.

* If item has `[LF] Open Access` tag  -- change "Online Resource" function to acknowledge that full text is available through the URL.

* If item has `[LF] Missing files` tag - add note to item detail that the liplibrary is not in possession of the article

* If item has a tag that matches the `^\[LF\] Alert.*$` regular expression, it gets excluded from Atom feeds. The custom boolean field `lf_feed_exclude` implements this flag, in `config.py`.
