# -*- coding: utf8 -*-
"""
LibCrowdsStatistics
-------------------

Global statistics page for LibCrowds.
"""

import os
from flask import current_app as app
from flask.ext.plugins import Plugin
import default_settings

__plugin__ = "LibCrowdsStatistics"
__version__ = "0.0.1"


class LibCrowdsStatistics(Plugin):
    """Libcrowds statistics plugin class."""

    def setup(self):
        """Setup plugin."""
        self.load_config()
        self.setup_blueprint()
        from . import event_listeners


    def load_config(self):
        """Configure the plugin."""
        app.config.from_envvar('STATISTICS_SETTINGS', silent=True)
        if not os.environ.get('STATISTICS_SETTINGS'):  # pragma: no cover
            settings = [key for key in dir(default_settings) if key.isupper()]

            for s in settings:
                if not app.config.get(s):
                    app.config[s] = getattr(default_settings, s)



    def setup_blueprint(self):
        """Setup blueprint."""
        from .blueprint import StatisticsBlueprint
        here = os.path.dirname(os.path.abspath(__file__))
        template_folder = os.path.join(here, 'templates')
        static_folder = os.path.join(here, 'static')

        blueprint = StatisticsBlueprint(template_folder=template_folder,
                                        static_folder=static_folder)
        app.register_blueprint(blueprint, url_prefix="/statistics")
