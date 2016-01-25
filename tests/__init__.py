# -*- coding: utf8 -*-

import sys
import os
import libcrowds_statistics as plugin

# Use the PyBossa test suite
sys.path.append(os.path.abspath("./pybossa/test"))

os.environ['STATISTICS_SETTINGS'] = '../settings_test.py'


def setUpPackage():
    """Setup the plugin."""
    from default import flask_app
    with flask_app.app_context():
        plugin_dir = os.path.dirname(plugin.__file__)
        plugin.LibCrowdsStatistics(plugin_dir).setup()
