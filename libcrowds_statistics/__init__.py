# -*- coding: utf8 -*-
"""
LibCrowdsStatistics
-------------------

Global statistics page for LibCrowds.
"""

import os
from flask import current_app as app
from flask.ext.plugins import Plugin

__plugin__ = "LibCrowdsStatistics"
__version__ = "0.0.1"


class LibCrowdsStatistics(Plugin):
    """Libcrowds statistics plugin class."""

    def setup(self):
        """Setup plugin."""
        self.setup_blueprint()


    def setup_blueprint(self):
        """Setup blueprint."""
        from .blueprint import StatisticsBlueprint
        template_folder = os.path.abspath('templates')
        static_folder = os.path.abspath('static')

        blueprint = StatisticsBlueprint(template_folder=template_folder,
                                        static_folder=static_folder,
                                        static_url_path='/statistics/static')
        app.register_blueprint(blueprint, url_prefix="/statistics")
