# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


import os
import sys
_HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(_HERE, '../src')))

import sparc.client

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'sparc.client'
copyright = '2023, NIH SPARC'
author = 'NIH SPARC'
release = '0.0.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc', # Core library for html generation from docstrings
    'sphinx.ext.viewcode', # Add links to highlighted source code
    'sphinx.ext.napoleon', # Support for NumPy and Google style docstrings
    'sphinx.ext.doctest', # Test snippets in the documentation¶
    'sphinx.ext.coverage', # Collect doc coverage stats
    'sphinx.ext.autosummary',  # Create neat summary tables
    'sphinx.ext.githubpages', # Creates .nojekyll
    'sphinx.ext.viewcode', # Add links to highlighted source code
]

autosummary_generate = True  # Turn on sphinx.ext.autosummary
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_options = {'navigation_depth': 2}