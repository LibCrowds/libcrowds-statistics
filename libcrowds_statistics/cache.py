# -*- coding: utf8 -*-
"""Cache module for libcrowds-statistics."""

import operator
import pygeoip
import re
from collections import defaultdict
from sqlalchemy.sql import text
from flask import current_app
from pybossa.core import db
from pybossa.cache import cache, memoize, ONE_HOUR

session = db.slave_session


@cache(timeout=ONE_HOUR, key_prefix="site_n_auth_task_runs")
def n_auth_task_runs_site():
    """Return the number of task runs."""
    sql = text('''SELECT COUNT(task_run.id) AS n_task_runs FROM task_run
               WHERE user_id IS NOT NULL''')
    results = session.execute(sql)
    for row in results:
        n_task_runs = row.n_task_runs
    return n_task_runs or 0


@cache(timeout=ONE_HOUR, key_prefix="site_n_tasks_completed")
def n_tasks_completed():
    """Return the number of completed tasks."""
    sql = text('''SELECT COUNT(task.state) AS n_tasks_completed
               FROM task WHERE task.state = 'completed';''')
    results = session.execute(sql)
    for row in results:
        n_tasks_completed = row.n_tasks_completed
    return n_tasks_completed or 0


@cache(timeout=ONE_HOUR, key_prefix="site_top5_projects_1_week")
def get_top5_projects_1_week():
    """Return the 5 most active projects in the last week."""
    sql = text('''SELECT project.name, project.short_name,
               COUNT(task_run.project_id) AS task_runs
               FROM project, task_run, category
               WHERE project.id=task_run.project_id
               AND project.category_id = category.id
               AND project.published
               AND NOT category.name = 'Staff'
               AND DATE(task_run.finish_time) > NOW() - INTERVAL '1 week'
               GROUP BY project.id
               ORDER BY task_runs DESC LIMIT 5;''')
    results = session.execute(sql)
    top5_projects_1_week = []
    for row in results:
        tmp = dict(name=row.name, short_name=row.short_name[:10],
                   task_runs=row.task_runs)
        top5_projects_1_week.append(tmp)
    return top5_projects_1_week


@cache(timeout=ONE_HOUR, key_prefix="site_top5_users_1_week")
def get_top5_users_1_week():
    """Return the 5 most active users in the last week"""
    sql = text('''SELECT "user".fullname, "user".name,
               COUNT(task_run) AS task_runs FROM "user", task_run
               WHERE "user".id=task_run.user_id
               AND DATE(task_run.finish_time) > NOW() - INTERVAL '1 week'
               AND DATE(task_run.finish_time) <= NOW()
               GROUP BY "user".id
               ORDER BY task_runs DESC LIMIT 5;''')
    results = session.execute(sql)
    top5_users_1_week = []
    for row in results:
        user = dict(fullname=row.fullname, name=row.name,
                    task_runs=row.task_runs)
        top5_users_1_week.append(user)
    return top5_users_1_week


@cache(timeout=ONE_HOUR, key_prefix="site_n_countries")
def n_countries():
    """Get the number of active cities."""
    countries = set()
    if current_app.config['GEO']:
        sql = text('''SELECT DISTINCT(user_ip) AS ip_address
                   FROM task_run
                   GROUP BY ip_address''')
        results = session.execute(sql)

        geolite = current_app.root_path + '/../dat/GeoLiteCity.dat'
        gic = pygeoip.GeoIP(geolite)
        for row in results:
            loc = gic.record_by_addr(row.ip_address)
            countries.add(loc['country_name'])

    return len(countries)


@cache(timeout=ONE_HOUR, key_prefix="site_n_cities")
def n_cities():
    """Get the number of active cities."""
    cities = set()
    if current_app.config['GEO']:
        sql = text('''SELECT DISTINCT(user_ip) AS ip_address
                   FROM task_run
                   GROUP BY ip_address''')
        results = session.execute(sql)

        geolite = current_app.root_path + '/../dat/GeoLiteCity.dat'
        gic = pygeoip.GeoIP(geolite)

        for row in results:
            loc = gic.record_by_addr(row.ip_address)
            cities.add(loc['city'])

    return len(cities)


@cache(timeout=ONE_HOUR, key_prefix="site_n_continents")
def n_continents():
    """Get the number of active continents."""
    continents = set()
    if current_app.config['GEO']:
        sql = text('''SELECT DISTINCT(user_ip) AS ip_address
                   FROM task_run
                   GROUP BY ip_address''')
        results = session.execute(sql)

        geolite = current_app.root_path + '/../dat/GeoLiteCity.dat'
        gic = pygeoip.GeoIP(geolite)

        for row in results:
            loc = gic.record_by_addr(row.ip_address)
            continents.add(loc['continent'])

    return len(continents)


@cache(timeout=ONE_HOUR, key_prefix="site_top_countries")
def get_top_countries(count=None):
    """Get the five most active countries."""
    countries = []
    n_task_runs = []
    if current_app.config['GEO']:
        sql = text('''SELECT DISTINCT(user_ip) AS ip_address,
                   COUNT(id) AS n_task_runs
                   FROM task_run
                   GROUP BY ip_address
                   ORDER BY n_task_runs DESC;''')
        results = session.execute(sql)

        geolite = current_app.root_path + '/../dat/GeoLiteCity.dat'
        gic = pygeoip.GeoIP(geolite)

        all_countries = defaultdict(int)
        for row in results:
            loc = gic.record_by_addr(row.ip_address)
            country = loc['country_name']
            if country:
                all_countries[country] += row.n_task_runs

        sorted_countries = sorted(all_countries.items(),
                                  key=operator.itemgetter(1),
                                  reverse=True)

        for country in sorted_countries[:count]:
            countries.append(country[0])
            n_task_runs.append(country[1])

    return dict(countries=countries, n_task_runs=n_task_runs)


@cache(timeout=ONE_HOUR, key_prefix="site_task_runs_daily")
def get_task_runs_daily():
    """Return a count of task runs each day for the last 14 days."""
    tasks = []
    days = []
    sql = text('''SELECT date_trunc('day', to_timestamp(task_run.finish_time,
               'YYYY-MM-DD'))
               AS "day" , count(task_run.id) AS "tasks"
               FROM task_run WHERE DATE(task_run.finish_time)
               > NOW() - INTERVAL '15 days'
               AND DATE(task_run.finish_time) < NOW() - INTERVAL '1 day'
               GROUP BY "day" ORDER BY "day";''')
    results = session.execute(sql)
    for row in results:
        tasks.append(row.tasks)
        days.append(date_handler(row.day))
    return dict(days=days, tasks=tasks)


@cache(timeout=ONE_HOUR, key_prefix="site_users_daily")
def get_users_daily():
    """Return a count of users each day for the last 14 days."""
    users = []
    days = []
    sql = text('''SELECT day, count(*) AS "users" FROM (
               SELECT DISTINCT date_trunc('day', to_timestamp(finish_time,
               'YYYY-MM-DD')) AS "day", to_char(user_id, '999')
               FROM task_run
               WHERE DATE (task_run.finish_time) > now() - interval '15 days'
               AND DATE (task_run.finish_time) < now() - interval '1 day'
               AND user_id IS NOT NULL
               UNION
               SELECT DISTINCT date_trunc('day', to_timestamp(finish_time,
               'YYYY-MM-DD')) AS "day", user_ip
               FROM task_run
               WHERE DATE (finish_time) > now() - interval '15 days'
               AND DATE (finish_time) < now() - interval '1 day'
               AND user_id IS NULL) AS "temp"
               GROUP BY day
               ORDER BY day ASC;''')
    results = session.execute(sql)

    for row in results:
        users.append(row.users)
        days.append(date_handler(row.day))
    return dict(days=days, users=users)


@cache(timeout=ONE_HOUR, key_prefix="site_dow")
def get_dow():
    """Return average number of tasks completed each day of the week."""
    days = []
    day_ints = []
    percentages = []
    sql = text('''WITH total AS (
               SELECT COUNT(id) AS id FROM task_run
               ) SELECT EXTRACT(DOW FROM DATE(finish_time)) AS "day_int",
               initcap(to_char(finish_time::timestamp, 'day')) AS "day",
               ROUND((COUNT(task_run.id) * 100.0 / total.id),1)::text
               AS percentage
               FROM task_run, total
               GROUP BY day, total.id, day_int
               ORDER by day_int;''')
    results = session.execute(sql)
    for row in results:
        days.append(row.day)
        day_ints.append(row.day_int)
        percentages.append(row.percentage)
    return dict(days=days, day_ints=day_ints, percentages=percentages)


@cache(timeout=ONE_HOUR, key_prefix="site_hourly_activity")
def site_hourly_activity():
    """Return hourly activity statistics."""
    hours = {}
    # initialize keys
    for i in range(0, 24):
        hours[str(i).zfill(2)] = 0

    sql = text('''WITH time_completed AS (
               SELECT to_char(DATE_TRUNC('hour',
               TO_TIMESTAMP(finish_time, 'YYYY-MM-DD"T"HH24:MI:SS.US')),
               'HH24') AS hour,
               COUNT(id) AS n_task_runs
               FROM task_run
               GROUP BY hour)
               SELECT hour,
               ROUND(n_task_runs * 100.0 / COUNT(task_run.id),1)::text
               AS percentage
               FROM time_completed, task_run
               GROUP BY hour, n_task_runs
               ORDER BY hour;''').execution_options(stream=True)
    results = session.execute(sql)
    for row in results:
        hours[row.hour] = row.percentage
    return format_hours(hours)


@memoize(timeout=ONE_HOUR)
def get_top_n_percent(percentage):
    """Return the top n percent of volunteers."""
    sql = text('''SELECT SUM(task_runs)
               FROM (SELECT COUNT(task_run) AS task_runs
               FROM task_run
               WHERE user_id IS NOT NULL
               GROUP BY user_id
               ORDER BY task_runs
               DESC LIMIT (
               SELECT (count(*) * :percentage / 100) AS id FROM "user"
               )) AS n_task_runs;''')
    results = session.execute(sql, dict(percentage=percentage))
    for row in results:
        n_task_runs = row.sum
    return int(n_task_runs) or 0


@cache(timeout=ONE_HOUR, key_prefix="site_n_avg_days_active")
def n_avg_days_active():
    """Return the average number of days a user remains active."""
    sql = text('''WITH days AS (
               SELECT date_part('day', MAX(finish_time::timestamp) -
               MIN(finish_time::timestamp)) + 1 as n_days FROM task_run
               WHERE user_id IS NOT NULL
               GROUP BY user_id)
               SELECT ROUND(avg(n_days)::int, 0) AS n_days
               FROM days;''')
    results = session.execute(sql)
    for row in results:
        n_days = row.n_days
    return int(n_days) or 0


def date_handler(obj):
    """Convert date objects to JSON serializable format."""
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def format_hours(hours):
    """Format hours."""
    hourNewStats = []
    for h in sorted(hours.keys()):
        if (hours[h] != 0):
            hourNewStats.append([int(h), hours[h]])
        else:
            hourNewStats.append([int(h), hours[h]])
    return hourNewStats
