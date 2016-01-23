# -*- coding: utf8 -*-
"""View module for libcrowds-statistics."""

import json
from flask import Blueprint
from flask import render_template
from pybossa.cache import site_stats
from pybossa.cache import users as cached_users
from pybossa.cache import projects as cached_projects
from . import cache as extra_stats


def index():
    """Return Global Statistics for the site."""
    title = "Statistics"
    description = """Statistical analysis of contributions made via the
                  LibCrowds crowdsourcing platform."""

    n_auth = site_stats.n_auth_users()
    n_anon = site_stats.n_anon_users()
    n_tasks = site_stats.n_tasks_site()
    n_task_runs = site_stats.n_task_runs_site()
    n_continents = extra_stats.n_continents()
    n_cities = extra_stats.n_cities()
    n_countries = extra_stats.n_countries()
    n_auth_task_runs = extra_stats.n_auth_task_runs_site()
    n_tasks_completed = extra_stats.n_tasks_completed()
    n_avg_days_active = extra_stats.n_avg_days_active()
    n_published_projects = cached_projects.n_published()

    top5_projects_24_hours = site_stats.get_top5_projects_24_hours()
    top5_users_24_hours = site_stats.get_top5_users_24_hours()
    top5_projects_1_week = extra_stats.get_top5_projects_1_week()
    top5_users_1_week = extra_stats.get_top5_users_1_week()

    top_users = cached_users.get_leaderboard(10)
    top_10_percent = extra_stats.get_top_n_percent(10)
    task_runs_daily = extra_stats.get_task_runs_daily()
    users_daily = extra_stats.get_users_daily()
    dow = extra_stats.get_dow()
    hourly_activity = extra_stats.site_hourly_activity()

    locs = site_stats.get_locs()
    show_locs = True if len(locs) > 0 else False
    top_countries = extra_stats.get_top_countries()

    stats = dict(n_auth=n_auth,
                 n_anon=n_anon,
                 n_tasks=n_tasks,
                 n_task_runs=n_task_runs,
                 n_auth_task_runs=n_auth_task_runs,
                 n_tasks_completed=n_tasks_completed,
                 n_countries=n_countries,
                 n_cities=n_cities,
                 n_continents=n_continents,
                 n_avg_days_active=n_avg_days_active,
                 n_published_projects=n_published_projects)

    users = dict(label="User Statistics",
                 values=[dict(label='Anonymous', value=[0, n_anon]),
                         dict(label='Authenticated', value=[0, n_auth])])

    tasks = dict(label="Task and Task Run Statistics",
                 values=[dict(label='Tasks', value=[0, n_tasks]),
                         dict(label='Task Runs', value=[1, n_task_runs])])

    return render_template('/stats.html', title=title,
                           description=description,
                           stats=stats,
                           users=json.dumps(users),
                           tasks=json.dumps(tasks),
                           locs=json.dumps(locs),
                           show_locs=show_locs,
                           top_countries=json.dumps(top_countries),
                           top5_users_24_hours=top5_users_24_hours,
                           top5_users_1_week=top5_users_1_week,
                           top5_projects_24_hours=top5_projects_24_hours,
                           top5_projects_1_week=top5_projects_1_week,
                           top_10_percent=top_10_percent,
                           task_runs_daily=json.dumps(task_runs_daily),
                           users_daily=json.dumps(users_daily),
                           dow=json.dumps(dow),
                           top_users=top_users,
                           hourly_activity=json.dumps(hourly_activity))
