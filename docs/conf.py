"""Sphinx configuration."""
project = "Blueprint"
author = "Michael Barrowman"
copyright = "2024, Michael Barrowman"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
