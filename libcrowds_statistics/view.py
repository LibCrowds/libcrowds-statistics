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
    n_anon = site_stats.n_anon_users()
    n_auth = site_stats.n_auth_users()
    top5_users_24_hours = site_stats.get_top5_users_24_hours()
    top5_users_1_week = extra_stats.get_top5_users_1_week()
    top_10_percent = extra_stats.get_top_n_percent(10)
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
    top5_projects_24_hours = site_stats.get_top5_projects_24_hours()
    top5_projects_1_week = extra_stats.get_top5_projects_1_week()

    # Location stats
    locs = site_stats.get_locs()
    n_continents = extra_stats.n_continents()
    n_cities = extra_stats.n_cities()
    n_countries = extra_stats.n_countries()
    top_countries = extra_stats.get_top_countries()

    users = dict(label="User Statistics",
                 values=dict(n_anon=n_anon,
                             n_auth=n_auth,
                             top5_users_24_hours=top5_users_24_hours,
                             top5_users_1_week=top5_users_1_week,
                             top_10_percent=top_10_percent,
                             users_daily=users_daily,
                             leaderboard=leaderboard,
                             n_avg_days_active=n_avg_days_active))

    tasks = dict(label="Task Statistics",
                 values=dict(n_tasks=n_tasks,
                             n_task_runs=n_task_runs,
                             n_auth_task_runs=n_auth_task_runs,
                             n_tasks_completed=n_tasks_completed,
                             task_runs_daily=task_runs_daily,
                             dow=dow,
                             hourly_activity=hourly_activity))

    projects = dict(label="Project Statistics",
                    values=dict(n_published_projects=n_published_projects,
                                top5_projects_24_hours=top5_projects_24_hours,
                                top5_projects_1_week=top5_projects_1_week))

    locations = dict(label="Location Statistics",
                     values=dict(locs=locs,
                                 n_countries=n_countries,
                                 n_cities=n_cities,
                                 n_continents=n_continents,
                                 top_countries=top_countries))

    return render_template('/stats.html', title=title,
                           description=description,
                           users=json.dumps(users),
                           tasks=json.dumps(tasks),
                           projects=json.dumps(projects),
                           locations=json.dumps(locations))
