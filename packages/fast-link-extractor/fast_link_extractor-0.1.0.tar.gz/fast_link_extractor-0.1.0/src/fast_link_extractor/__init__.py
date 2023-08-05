"""
Set up module access for the base package
"""
from .fast_link_extractor import format_base_url
from .fast_link_extractor import async_get_html
from .fast_link_extractor import get_links
from .fast_link_extractor import get_sub_dirs
from .fast_link_extractor import get_files
from .fast_link_extractor import filter_with_regex
from .fast_link_extractor import prepend_with_baseurl
from .fast_link_extractor import link_extractor

__all__ = ['format_base_url',
           'async_get_html',
           'get_links',
           'get_sub_dirs',
           'get_files',
           'filter_with_regex',
           'prepend_with_baseurl',
           'link_extractor']
