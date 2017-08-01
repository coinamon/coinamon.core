#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Project metadata #
#==================#

project = 'Coinamon Core'
copyright = '2017 Jiří Janoušek'
author = 'Jiří Janoušek'
language = None
version = '0.1'  # The short X.Y version.
release = '0.1'  # The full version, including alpha/beta/rc tags.

# Directory of modules #
#======================#

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# General Settings #
#==================#

extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.imgmath',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
todo_include_todos = True

# HTML output #
#=============#

html_theme = 'alabaster'
html_theme_options = {
    'show_related': True
}
html_static_path = ['_static']
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
        'donate.html',
    ]
}

# Intersphinx extension #
#=======================#

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

# Autodoc extension #
#===================#

autoclass_content = "both"
autodoc_default_flags = ['members', 'undoc-members', 'private-members']
