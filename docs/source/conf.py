# Configuration file for the Sphinx documentation builder.

import os
import sys

sys.path.insert(0, os.path.abspath('../..'))

project = 'MathDoc'
copyright = '2026, Educational Contributors'
author = 'Educational Contributors'
release = '0.1.0'
version = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
]

html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9',
}

html_static_path = ['_static']
html_logo = None

add_module_names = True
add_function_parentheses = True

mathjax_config = {
    'tex2jax': {
        'inlineMath': [['$', '$'], ['\\(', '\\)']],
        'displayMath': [['$$', '$$'], ['\\[', '\\]']],
    },
}

master_doc = 'index'
