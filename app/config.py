import pathlib
import re  # CF
from functools import partial  # CF

from environs import Env
from flask_babel import lazy_gettext as _
from kerko import codecs, extractors, transformers  # CF
from kerko.composer import Composer
from kerko.specs import CollectionFacetSpec, FieldSpec, FlatFacetSpec  # CF
from whoosh.fields import BOOLEAN, ID, STORED, TEXT  # CF
from whoosh.query import Term  # CF

from .extractors import MatchesTagExtractor  # CF
from .specs import LabeledFieldSpec  # CF
from .transformers import clean_data_extra, clean_lines  # CF

# pylint: disable=invalid-name

env = Env()
env.read_env()


@env.parser_for('collection_spec')
def collection_spec_parser(value):
    try:
        return [tuple(i.strip() for i in v.split(':', maxsplit=2)) for v in value.split(';')]
    except:  # noqa  # pylint: disable=bare-except
        return value


class Config:

    def __init__(self):
        app_dir = pathlib.Path(env.str('FLASK_APP')).parent.absolute()

        self.check_deprecated_options()

        self.SECRET_KEY = env.str('SECRET_KEY')
        self.PROXY_FIX = env.bool('PROXY_FIX', False)
        self.BABEL_DEFAULT_LOCALE = env.str('BABEL_DEFAULT_LOCALE', 'en')
        self.BABEL_DEFAULT_TIMEZONE = env.str('BABEL_DEFAULT_TIMEZONE', 'UTC')

        # Set Kerko variables from the environment. Some are deliberately omitted
        # because it would make more sense to set them in the app's Config object
        # directly.
        self.KERKO_TITLE = env.str('KERKO_TITLE', _("Kerko App"))
        self.KERKO_DATA_DIR = env.path('KERKO_DATA_DIR', str(app_dir / 'data' / 'kerko'))
        self.KERKO_WHOOSH_LANGUAGE = env.str('KERKO_WHOOSH_LANGUAGE', 'en')
        self.KERKO_ZOTERO_LOCALE = env.str('KERKO_ZOTERO_LOCALE', 'en-US')
        self.KERKO_ZOTERO_API_KEY = env.str('KERKO_ZOTERO_API_KEY')
        self.KERKO_ZOTERO_LIBRARY_ID = env.str('KERKO_ZOTERO_LIBRARY_ID')
        self.KERKO_ZOTERO_LIBRARY_TYPE = env.str('KERKO_ZOTERO_LIBRARY_TYPE')
        self.KERKO_ZOTERO_MAX_ATTEMPTS = env.int('KERKO_ZOTERO_MAX_ATTEMPTS', 10)
        self.KERKO_ZOTERO_WAIT = env.int('KERKO_ZOTERO_WAIT', 120)  # In seconds.
        self.KERKO_ZOTERO_BATCH_SIZE = env.int('KERKO_ZOTERO_BATCH_SIZE', 100)
        self.KERKO_PAGE_LEN = env.int('KERKO_PAGE_LEN', 20)
        self.KERKO_PAGER_LINKS = env.int('KERKO_PAGER_LINKS', 4)
        self.KERKO_CSL_STYLE = env.str('KERKO_CSL_STYLE', 'apa')
        self.KERKO_RESULTS_ABSTRACTS = env.bool('KERKO_RESULTS_ABSTRACTS', False)
        self.KERKO_RESULTS_ABSTRACTS_TOGGLER = env.bool('KERKO_RESULTS_ABSTRACTS_TOGGLER', True)
        self.KERKO_RESULTS_ABSTRACTS_MAX_LENGTH = env.int('KERKO_RESULTS_ABSTRACTS_MAX_LENGTH', 0)
        self.KERKO_RESULTS_ABSTRACTS_MAX_LENGTH_LEEWAY = env.int(
            'KERKO_RESULTS_ABSTRACTS_MAX_LENGTH_LEEWAY', 0
        )
        self.KERKO_RESULTS_ATTACHMENT_LINKS = env.bool('KERKO_RESULTS_ATTACHMENT_LINKS', True)
        self.KERKO_RESULTS_URL_LINKS = env.bool('KERKO_RESULTS_URL_LINKS', True)
        self.KERKO_FULLTEXT_SEARCH = env.bool('KERKO_FULLTEXT_SEARCH', True)
        self.KERKO_PRINT_ITEM_LINK = env.bool('KERKO_PRINT_ITEM_LINK', False)
        self.KERKO_PRINT_CITATIONS_LINK = env.bool('KERKO_PRINT_CITATIONS_LINK', False)
        self.KERKO_PRINT_CITATIONS_MAX_COUNT = env.int('KERKO_PRINT_CITATIONS_MAX_COUNT', 0)
        self.KERKO_DOWNLOAD_CITATIONS_LINK = env.bool('KERKO_DOWNLOAD_CITATIONS_LINK', True)
        self.KERKO_DOWNLOAD_CITATIONS_MAX_COUNT = env.int('KERKO_DOWNLOAD_CITATIONS_MAX_COUNT', 0)
        self.KERKO_DOWNLOAD_ATTACHMENT_NEW_WINDOW = env.bool(
            'KERKO_DOWNLOAD_ATTACHMENT_NEW_WINDOW', False
        )
        self.KERKO_HIGHWIREPRESS_TAGS = env.bool('KERKO_HIGHWIREPRESS_TAGS', True)
        self.KERKO_RELATIONS_INITIAL_LIMIT = env.int('KERKO_RELATIONS_INITIAL_LIMIT', 5)
        self.KERKO_RELATIONS_LINKS = env.bool('KERKO_RELATIONS_LINKS', False)
        self.KERKO_FEEDS = env.list('KERKO_FEEDS', ['atom'], subcast=str)
        self.KERKO_FEEDS_MAX_DAYS = env.int('KERKO_FEEDS_MAX_DAYS', 0)

        self.KERKO_COMPOSER = Composer(
            whoosh_language=self.KERKO_WHOOSH_LANGUAGE,
            exclude_default_scopes=env.list(
                'KERKOAPP_EXCLUDE_DEFAULT_SCOPES',
                [] if self.KERKO_FULLTEXT_SEARCH else ['fulltext', 'metadata'],
                # The 'metadata' scope does the same as the 'all' scope when
                # full-text search is disabled, hence its removal in that case.
                subcast=str,
            ),
            exclude_default_fields=env.list(
                'KERKOAPP_EXCLUDE_DEFAULT_FIELDS',
                [] if self.KERKO_FULLTEXT_SEARCH else ['text_docs'],
                subcast=str,
            ),
            exclude_default_facets=env.list('KERKOAPP_EXCLUDE_DEFAULT_FACETS', [], subcast=str),
            exclude_default_sorts=env.list('KERKOAPP_EXCLUDE_DEFAULT_SORTS', [], subcast=str),
            exclude_default_citation_formats=env.list(
                'KERKOAPP_EXCLUDE_DEFAULT_CITATION_FORMATS', [], subcast=str
            ),
            exclude_default_badges=env.list('KERKOAPP_EXCLUDE_DEFAULT_BADGES', [], subcast=str),
            default_item_include_re=env.str('KERKOAPP_ITEM_INCLUDE_RE', ''),
            default_item_exclude_re=env.str('KERKOAPP_ITEM_EXCLUDE_RE', ''),
            default_tag_include_re=env.str(
                'KERKOAPP_TAG_INCLUDE_RE', env.str('KERKOAPP_TAG_WHITELIST_RE', '')
            ),
            default_tag_exclude_re=env.str(
                'KERKOAPP_TAG_EXCLUDE_RE', env.str('KERKOAPP_TAG_BLACKLIST_RE', r'^_')
            ),
            default_child_include_re=env.str(
                'KERKOAPP_CHILD_INCLUDE_RE', env.str('KERKOAPP_CHILD_WHITELIST_RE', '')
            ),
            default_child_exclude_re=env.str(
                'KERKOAPP_CHILD_EXCLUDE_RE', env.str('KERKOAPP_CHILD_BLACKLIST_RE', r'^_')
            ),
            mime_types=env.list('KERKOAPP_MIME_TYPES', ['application/pdf'], subcast=str),
            facet_initial_limit=env.int('KERKOAPP_FACET_INITIAL_LIMIT', 0),
            facet_initial_limit_leeway=env.int('KERKOAPP_FACET_INITIAL_LIMIT_LEEWAY', 0),
        )

        # Add collection facets.
        collection_spec = env.collection_spec('KERKOAPP_COLLECTION_FACETS', None)
        if collection_spec:
            for collection_key, weight, title in collection_spec:
                self.KERKO_COMPOSER.add_facet(
                    CollectionFacetSpec(
                        title=title,
                        weight=int(weight),
                        collection_key=collection_key,
                        initial_limit=env.int('KERKOAPP_FACET_INITIAL_LIMIT', 0),
                        initial_limit_leeway=env.int('KERKOAPP_FACET_INITIAL_LIMIT_LEEWAY', 0),
                    )
                )

        # CF template overrides.
        self.KERKO_TEMPLATE_ITEM = 'kerko-overrides/item.html.jinja2'
        self.KERKO_TEMPLATE_SEARCH = 'kerko-overrides/search.html.jinja2'

        # CF custom fields, in rendering order.
        for new_field in [
            # Kerko already indexes ISBN, ISSN and DOI, thus they don't need to
            # be searchable. We still need to store them because they will be
            # cleaned up from the 'extra' field and rendered separately.
            {
                'kwargs': dict(
                    key='cf_isbn',
                    label='ISBN',
                    field_type=STORED,
                    scopes=None,
                ),
                're': r'^\s*ISBN\s*:\s*(.*)$',
            },
            {
                'kwargs': dict(
                    key='cf_issn',
                    label='ISSN',
                    field_type=STORED,
                    scopes=None,
                ),
                're': r'^\s*ISSN\s*:\s*(.*)$',
            },
            {
                'kwargs': dict(
                    key='cf_doi',
                    label='DOI',
                    field_type=STORED,
                    scopes=None,
                ),
                're': r'^\s*DOI\s*:\s*(.*)$',
            },
            # The following fields are also useful as search keys.
            {
                'kwargs': dict(
                    key='cf_pmid',
                    label='PMID',
                    field_type=ID(**self.KERKO_COMPOSER.primary_id_kwargs, stored=True),
                    scopes=['all', 'metadata'],
                ),
                're': r'^\s*PMID\s*:\s*(.*)$',
            },
            {
                'kwargs': dict(
                    key='cf_pmcid',
                    label='PMCID',
                    field_type=ID(**self.KERKO_COMPOSER.primary_id_kwargs, stored=True),
                    scopes=['all', 'metadata'],
                ),
                're': r'^\s*PMCID\s*:\s*(.*)$',
            },
            # The following IDs are often to short to be useful in searches.
            {
                'kwargs': dict(
                    key='cf_lfaward',
                    label='Lipedema Foundation Award',
                    field_type=STORED,
                    scopes=None,
                ),
                're': r'^\s*LFAward\s*:\s*(.*)$',
            },
        ]:
            self.KERKO_COMPOSER.add_field(
                LabeledFieldSpec(
                    **new_field['kwargs'],
                    extractor=extractors.TransformerExtractor(
                        extractor=extractors.ItemDataExtractor(key='extra'),
                        transformers=[
                            transformers.find(
                                regex=new_field['re'],
                                flags=re.IGNORECASE | re.MULTILINE,
                                max_matches=0,
                            )
                        ]
                    )
                )
            )

        # CF replace the default 'data' and 'z_extra' fields by ones where the
        # 'extra' field is stripped of unwanted lines, i.e., stripped of any
        # line that matches the regular expression below.
        extra_cleanup_pattern = re.compile(
            r'^\s*(PMID|PMCID|LFAward|DOI|ISBN|ISSN).+', re.IGNORECASE
        )
        # CAUTION: This requires that 'data' and 'z_extra' be added to the
        # KERKOAPP_EXCLUDE_DEFAULT_FIELDS environment variable.
        self.KERKO_COMPOSER.add_field(
            FieldSpec(
                key='data',
                field_type=STORED,
                extractor=extractors.TransformerExtractor(
                    extractor=extractors.RawDataExtractor(),
                    transformers=[
                        partial(clean_data_extra, pattern=extra_cleanup_pattern),
                    ],
                ),
            )
        )
        self.KERKO_COMPOSER.add_field(
            FieldSpec(
                key='z_extra',
                field_type=TEXT(**self.KERKO_COMPOSER.primary_text_kwargs),
                scopes=['all', 'metadata'],
                extractor=extractors.TransformerExtractor(
                    extractor=extractors.ItemDataExtractor(key='extra'),
                    transformers=[
                        partial(clean_lines, pattern=extra_cleanup_pattern),
                    ],
                ),
            )
        )

        # CF replace the default 'text_tags' field and 'facet_tag' facet by ones
        # where the tags are cleaned up using the regular expression below.
        tag_cleanup_pattern = re.compile(r'^\s*\[L(L|F)\]\s*', re.IGNORECASE)
        # CAUTION: This requires that 'text_tags' be added to the
        # KERKOAPP_EXCLUDE_DEFAULT_FIELDS environment variable.
        self.KERKO_COMPOSER.add_field(
            FieldSpec(
                key='text_tags',
                field_type=TEXT(**self.KERKO_COMPOSER.secondary_title_text_kwargs),
                scopes=['all', 'metadata'],
                extractor=extractors.TransformerExtractor(
                    extractor=extractors.TagsTextExtractor(
                        include_re=self.KERKO_COMPOSER.default_tag_include_re,
                        exclude_re=self.KERKO_COMPOSER.default_tag_exclude_re
                    ),
                    transformers=[
                        lambda value: tag_cleanup_pattern.sub('', value) if value else value,
                    ],
                )
            )
        )
        # CAUTION: This requires that 'facet_tag' be added to the
        # KERKOAPP_EXCLUDE_DEFAULT_FACETS environment variable.
        self.KERKO_COMPOSER.add_facet(
            FlatFacetSpec(
                key='facet_tag',
                title=_('Topic'),
                filter_key='topic',
                weight=100,
                initial_limit=env.int('KERKOAPP_FACET_INITIAL_LIMIT', 0),
                initial_limit_leeway=env.int('KERKOAPP_FACET_INITIAL_LIMIT_LEEWAY', 0),
                field_type=ID(stored=True),
                extractor=extractors.TransformerExtractor(
                    extractor=extractors.TagsFacetExtractor(
                        include_re=self.KERKO_COMPOSER.default_tag_include_re,
                        exclude_re=self.KERKO_COMPOSER.default_tag_exclude_re
                    ),
                    transformers=[
                        lambda value: list({tag_cleanup_pattern.sub('', s) for s in value}) if value else value,
                    ],
                ),
                codec=codecs.BaseFacetCodec(),
                missing_label=None,
                sort_key=['label'],
                sort_reverse=False,
                item_view=True,
                allow_overlap=True,
                query_class=Term
            )
        )

        # CF add "open access" facet.
        self.KERKO_COMPOSER.add_facet(
            FlatFacetSpec(
                key='lf_facet_open_access',
                title=_('Publication'),
                filter_key='openaccess',
                weight=320,  # Position after the "Publication year" facet.
                initial_limit=env.int('KERKOAPP_FACET_INITIAL_LIMIT', 0),
                initial_limit_leeway=env.int('KERKOAPP_FACET_INITIAL_LIMIT_LEEWAY', 0),
                field_type=ID(stored=True),
                extractor=extractors.TransformerExtractor(
                    extractor=extractors.TagsFacetExtractor(
                        include_re=r'^\[LF\] Open Access$'
                    ),
                    transformers=[
                        lambda value: list({tag_cleanup_pattern.sub('', s) for s in value}) if value else value,
                    ],
                ),
                codec=codecs.BaseFacetCodec(),
                missing_label=None,
                sort_key=['label'],
                sort_reverse=False,
                item_view=True,
                allow_overlap=True,
                query_class=Term
            )
        )
        # CF add "open access" boolean field.
        self.KERKO_COMPOSER.add_field(
            FieldSpec(
                key='lf_open_access',
                field_type=BOOLEAN(stored=True),
                extractor=MatchesTagExtractor(r'\[LF\] Open Access$', re.IGNORECASE),
            )
        )
        # CF add "missing files" boolean field.
        self.KERKO_COMPOSER.add_field(
            FieldSpec(
                key='lf_missing_files',
                field_type=BOOLEAN(stored=True),
                extractor=MatchesTagExtractor(r'^\[LF\] Missing files$', re.IGNORECASE),
            )
        )
        # CF add flag for excluding item from web feeds.
        self.KERKO_COMPOSER.add_field(
            FieldSpec(
                key='lf_feed_exclude',
                field_type=BOOLEAN,
                extractor=MatchesTagExtractor(r'^\[LF\] Alert.*$', re.IGNORECASE),
            )
        )

        # CF configure web feed filter.
        self.KERKO_FEEDS_REJECT_ANY = {'lf_feed_exclude': [True]}

        # CF override list of fields to retrieve with search results.
        self.KERKO_RESULTS_FIELDS = ['id', 'attachments', 'bib', 'coins', 'data', 'url', 'lf_open_access']

    @staticmethod
    def check_deprecated_options():
        if env.str('KERKOAPP_TAG_WHITELIST_RE', '') or env.str('KERKOAPP_TAG_BLACKLIST_RE', ''):
            # Deprecated after version 0.6.
            print(
                "WARNING: The 'KERKOAPP_TAG_WHITELIST_RE' and 'KERKOAPP_TAG_BLACKLIST_RE' "
                "environment variables are deprecated. Please use 'KERKOAPP_TAG_INCLUDE_RE' "
                "and 'KERKOAPP_TAG_EXCLUDE_RE' instead."
            )
        if env.str('KERKOAPP_CHILD_WHITELIST_RE', '') or env.str('KERKOAPP_CHILD_BLACKLIST_RE', ''):
            # Deprecated after version 0.6.
            print(
                "WARNING: The 'KERKOAPP_CHILD_WHITELIST_RE' and 'KERKOAPP_CHILD_BLACKLIST_RE' "
                "environment variables are deprecated. Please use 'KERKOAPP_CHILD_INCLUDE_RE' "
                "and 'KERKOAPP_CHILD_EXCLUDE_RE' instead."
            )
        if env.str('KERKOAPP_NOTE_WHITELIST_RE', '') or env.str('KERKOAPP_NOTE_BLACKLIST_RE', ''):
            # Deprecated after version 0.4.
            raise SystemExit(
                "ERROR: The 'KERKOAPP_NOTE_WHITELIST_RE' and 'KERKOAPP_NOTE_BLACKLIST_RE' "
                "environment variables are no longer supported. Please use "
                "'KERKOAPP_CHILD_INCLUDE_RE' and 'KERKOAPP_CHILD_EXCLUDE_RE' instead."
            )


class DevelopmentConfig(Config):

    def __init__(self):
        super().__init__()

        self.CONFIG = 'development'
        self.DEBUG = True
        self.LOGGING_LEVEL = env.str('LOGGING_LEVEL', 'DEBUG')
        # self.EXPLAIN_TEMPLATE_LOADING = True


class ProductionConfig(Config):

    def __init__(self):
        super().__init__()

        self.CONFIG = 'production'
        self.DEBUG = False
        self.LOGGING_HANDLER = env.str('LOGGING_HANDLER', 'syslog')
        self.LOGGING_ADDRESS = env.str('LOGGING_ADDRESS', '/dev/log')
        self.LOGGING_LEVEL = env.str('LOGGING_LEVEL', 'WARNING')
        self.GOOGLE_ANALYTICS_ID = env.str('GOOGLE_ANALYTICS_ID', '')


CONFIGS = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
