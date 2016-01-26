# -*- coding: utf8 -*-

import sys
import os
import libcrowds_statistics as plugin
from pybossa.model.task_run import TaskRun
from sqlalchemy import event
from libcrowds_statistics import event_listeners

# Use the PyBossa test suite
sys.path.append(os.path.abspath("./pybossa/test"))


def setUpPackage():
    """Setup the plugin."""
    from default import flask_app
    with flask_app.app_context():
        plugin_dir = os.path.dirname(plugin.__file__)
        plugin.LibCrowdsStatistics(plugin_dir).setup()

        # Remove event listeners
        func = event_listeners.record_new_task_run_ip_event
        event.remove(TaskRun, 'before_insert', func)
