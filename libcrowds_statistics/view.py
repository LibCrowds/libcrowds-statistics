# -*- coding: utf8 -*-
"""View module for libcrowds-statistics."""

import json
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

    # User stats
    n_anon = extra_stats.n_anon_users()
    n_auth = site_stats.n_auth_users()
    top_5_users_1_week = extra_stats.get_top_n_users_k_days(5, 7)
    n_tr_top_10_percent = extra_stats.get_top_n_percent(10)
    users_daily = extra_stats.get_users_daily()
    leaderboard = cached_users.get_leaderboard(10)
    n_avg_days_active = extra_stats.n_avg_days_active()

    # Task stats
    n_tasks = site_stats.n_tasks_site()
    n_task_runs = site_stats.n_task_runs_site()
    n_auth_task_runs = extra_stats.n_auth_task_runs_site()
    n_tasks_completed = extra_stats.n_tasks_completed()
    task_runs_daily = extra_stats.get_task_runs_daily()
    dow = extra_stats.get_dow()
    hourly_activity = extra_stats.site_hourly_activity()

    # Project stats
    n_published_projects = cached_projects.n_published()
    top_5_pr_1_week = extra_stats.get_top_n_projects_k_days(5, 7)

    # Location stats
    locs = extra_stats.get_locations()
    n_continents = extra_stats.n_continents()
    n_cities = extra_stats.n_cities()
    n_countries = extra_stats.n_countries()
    top_countries = extra_stats.get_top_n_countries()

    stats = dict(n_auth=n_auth,
                 n_anon=n_anon,
                 n_published_projects=n_published_projects,
                 n_tasks=n_tasks,
                 n_task_runs=n_task_runs,
                 n_auth_task_runs=n_auth_task_runs,
                 n_tasks_completed=n_tasks_completed,
                 n_countries=n_countries,
                 n_cities=n_cities,
                 n_continents=n_continents,
                 n_avg_days_active=n_avg_days_active,
                 n_tr_top_10_percent=n_tr_top_10_percent)

    return render_template('/stats.html', title=title,
                           description=description,
                           stats=json.dumps(stats),
                           locs=json.dumps(locs),
                           users_daily=json.dumps(users_daily),
                           task_runs_daily=json.dumps(task_runs_daily),
                           top_countries=json.dumps(top_countries),
                           top_5_pr_1_week=json.dumps(top_5_pr_1_week),
                           top_5_users_1_week=json.dumps(top_5_users_1_week),
                           hourly_activity=json.dumps(hourly_activity),
                           dow=json.dumps(dow),
                           leaderboard=json.dumps(leaderboard))
