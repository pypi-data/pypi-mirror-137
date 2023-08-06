__version__ = '0.1.0'

from docums.plugins import BasePlugin
import docums.utils as utils
import os.path
import copy

class NavTitleLoader(BasePlugin):

    def on_nav(self, nav, config, files):
        for page in nav.pages:
            page.read_source(config)

