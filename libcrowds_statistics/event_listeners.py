# -*- coding: utf8 -*-
"""Event listeners module for libcrowds-statistics."""

from flask import request
from flask import current_app as app
from pybossa.model.task_run import TaskRun
from sqlalchemy import event

record_ips = app.config['STATISTICS_RECORD_ALL_IPS']


@event.listens_for(TaskRun, 'before_insert')
def add_task_run_event(mapper, conn, target):
    """Record user IP address for all task runs.

    By default PyBossa only records IP address for unregistered users but this
    plugin presents statistics that are more useful if the locations of all
    users are known. The method also takes proxy servers into account.
    """
    if record_ips:
        if request.access_route:
            trusted_proxies = {'127.0.0.1'}
            route = request.access_route + [request.remote_addr]
            ip = next((addr for addr in reversed(route)
                       if addr not in trusted_proxies), request.remote_addr)
        else:
            ip = request.remote_addr

        target.info['ip_address'] = ip
