# -*- coding: utf8 -*-
"""Event listeners module for libcrowds-statistics."""

from flask import request
from pybossa.model.task_run import TaskRun
from sqlalchemy import event


@event.listens_for(TaskRun, 'before_insert')
def record_new_task_run_ip_event(mapper, conn, target):
    """Record user IP address for task run.

    By default PyBossa only records IP address for unregistered users but this
    plugin presents statistics that are more useful if the locations of all
    users are known. The method also takes proxy servers into account.
    """
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr

    target.info['ip_address'] = ip
