# -*- coding: utf8 -*-
"""
LibCrowdsStatistics
-------------------

Global statistics page for LibCrowds.
"""

import os
import json
from flask import current_app as app
from flask.ext.plugins import Plugin

__plugin__ = "LibCrowdsStatistics"
__version__ =  json.load(open(os.path.join(os.path.dirname(__file__),
                                           'info.json')))['version']

class LibCrowdsStatistics(Plugin):
    """Libcrowds statistics plugin class."""

    def setup(self):
        """Setup the plugin."""
        self.setup_blueprint()
        from . import event_listeners

    def setup_blueprint(self):
        """Setup blueprint."""
        from .blueprint import StatisticsBlueprint
        here = os.path.dirname(os.path.abspath(__file__))
        template_folder = os.path.join(here, 'templates')
        static_folder = os.path.join(here, 'static')
        blueprint = StatisticsBlueprint(template_folder=template_folder,
                                        static_folder=static_folder)
        app.register_blueprint(blueprint, url_prefix="/statistics")
