# -*- coding: utf8 -*-

from default import with_context, Test
from mock import patch, MagicMock
from factories import UserFactory, ProjectFactory, TaskFactory
from factories import TaskRunFactory, AnonymousTaskRunFactory
from datetime import date, datetime, timedelta

from libcrowds_statistics import cache


class TestCacheWithoutData(Test):


    def test_n_auth_task_runs_site_returns_zero_when_no_data(self):
        n = cache.n_auth_task_runs_site()

        assert n == 0


    def test_n_tasks_completed_returns_zero_when_no_data(self):
        n = cache.n_tasks_completed()

        assert n == 0


    def test_get_top5_projects_1_week_returns_empty_list_when_no_data(self):
        l = cache.get_top5_projects_1_week()

        assert l == []


    def test_get_top5_users_1_week_returns_empty_list_when_no_data(self):
        l = cache.get_top5_users_1_week()

        assert l == []


    @with_context
    def test_n_countries_returns_zero_when_no_data(self):
        n = cache.n_countries()

        assert n == 0


    @with_context
    def test_n_cities_returns_zero_when_no_data(self):
        n = cache.n_cities()

        assert n == 0


    @with_context
    def test_n_continents_returns_zero_when_no_data(self):
        n = cache.n_continents()

        assert n == 0


    @with_context
    def test_get_top_countries_returns_empty_dataset_when_no_data(self):
        d = cache.get_top_countries()

        assert d == {'countries': [], 'n_task_runs': []}, d


    def test_get_task_runs_daily_returns_empty_dataset_when_no_data(self):
        d = cache.get_task_runs_daily()

        assert d == {'days': [], 'tasks': []}


    def test_get_users_daily_returns_empty_dataset_when_no_data(self):
        d = cache.get_users_daily()

        assert d == {'days': [], 'users': []}


    def test_get_dow_returns_empty_dataset_when_no_data(self):
        d = cache.get_dow()

        assert d == {'days': [], 'day_ints': [], 'percentages': []}


    def test_site_hourly_activity_returns_no_task_runs_when_no_data(self):
        d = cache.site_hourly_activity()
        tr = sum([float(str(i[1])) for i in d])

        assert tr == 0.0


    def test_site_hourly_activity_returns_array_of_24_lists(self):
        d = cache.site_hourly_activity()

        assert len(d) == 24


    def test_get_top_n_percent_returns_zero_when_no_data(self):
        n = cache.get_top_n_percent(20)

        assert n == 0


    def test_n_avg_days_active_returns_zero_when_no_data(self):
        n = cache.n_avg_days_active()

        assert n == 0


    def test_hours_formatted_from_dict_to_list_array(self):
        unformatted = {'1': 4, '2': 5, '3': 6}
        formatted = cache.format_hours(unformatted)

        assert formatted == [[1, 4], [2, 5], [3, 6]]


class TestCacheWithData(Test):


    def setUp(self):
        super(TestCacheWithData, self).setUp()
        self.pr = ProjectFactory.create()
        self.task = TaskFactory.create(project=self.pr, n_answers=3)
        self.user = UserFactory.create()
        self.day1 = date.today() - timedelta(days=6)
        self.auth_tr = TaskRunFactory.create(project=self.pr,
                                             created=self.day1,
                                             finish_time=self.day1,
                                             task=self.task,
                                             user=self.user)
        self.day2 = date.today() - timedelta(days=14)
        self.anon_tr = AnonymousTaskRunFactory.create(project=self.pr,
                                                      created=self.day2,
                                                      finish_time=self.day2,
                                                      task=self.task)
        self.day3 = date.today() - timedelta(days=15)
        self.anon_tr2 = AnonymousTaskRunFactory.create(project=self.pr,
                                                       created=self.day3,
                                                       finish_time=self.day3,
                                                       task=self.task)


    def create_mock_ip_addresses(self, geoip_mock):
        geoip_instance = MagicMock()
        loc = {'latitude': 1, 'longitude': 1, 'country_name': 'england',
               'city': 'london', 'continent': 'europe'}
        geoip_instance.record_by_addr.return_value = loc
        geoip_mock.return_value = geoip_instance

        AnonymousTaskRunFactory.create(user_ip="1.1.1.1")
        AnonymousTaskRunFactory.create(user_ip="2.2.2.2")


    def test_n_auth_task_runs_returned(self):
        n = cache.n_auth_task_runs_site()

        assert n == 1


    def test_n_tasks_completed_returned(self):
        n = cache.n_tasks_completed()

        assert n == 1


    def test_top5_projects_1_week_returned(self):
        l = cache.get_top5_projects_1_week()

        assert l[0]['name'] == self.pr.name


    def test_top5_users_1_week_returned(self):
        l = cache.get_top5_users_1_week()

        assert l[0]['fullname'] == self.user.fullname


    @with_context
    @patch('libcrowds_statistics.cache.current_app')
    @patch('libcrowds_statistics.cache.pygeoip.GeoIP')
    def test_n_countries_returned(self, geoip_mock, current_app):
        current_app.config = {'GEO': True}
        self.create_mock_ip_addresses(geoip_mock)
        n = cache.n_countries()

        assert n == 1


    @with_context
    @patch('libcrowds_statistics.cache.current_app')
    @patch('libcrowds_statistics.cache.pygeoip.GeoIP')
    def test_n_cities_returned(self, geoip_mock, current_app):
        current_app.config = {'GEO': True}
        self.create_mock_ip_addresses(geoip_mock)
        n = cache.n_cities()

        assert n == 1


    @with_context
    @patch('libcrowds_statistics.cache.current_app')
    @patch('libcrowds_statistics.cache.pygeoip.GeoIP')
    def test_n_continents_returned(self, geoip_mock, current_app):
        current_app.config = {'GEO': True}
        self.create_mock_ip_addresses(geoip_mock)
        n = cache.n_continents()

        assert n == 1


    @with_context
    @patch('libcrowds_statistics.cache.current_app')
    @patch('libcrowds_statistics.cache.pygeoip.GeoIP')
    def test_top_countries_returned(self, geoip_mock, current_app):
        current_app.config = {'GEO': True}
        self.create_mock_ip_addresses(geoip_mock)
        d = cache.get_top_countries()

        assert d == {'countries': ['england'], 'n_task_runs': [5]}, d


    def test_task_runs_daily_returns_correct_dates(self):
        d = cache.get_task_runs_daily()
        days = [day[:10] for day in d['days']]

        assert days == [str(self.day2), str(self.day1)]


    def test_task_runs_daily_returns_correct_number_of_tasks(self):
        d = cache.get_task_runs_daily()

        assert d['tasks'] == [1, 1]


    def test_users_daily_returns_correct_dates(self):
        d = cache.get_users_daily()
        days = [day[:10] for day in d['days']]

        assert days == [str(self.day2), str(self.day1)]


    def test_users_daily_returns_correct_number_of_tasks(self):
        d = cache.get_users_daily()

        assert d['users'] == [1, 1]


    def test_dow_percentages_split_correctly(self):
        d = cache.get_dow()

        assert d['percentages'] == ['33.3', '33.3', '33.3']


    def test_site_hourly_activity_equals_100_percent(self):
        d = cache.site_hourly_activity()
        tr = sum([float(str(i[1])) for i in d])

        assert tr == 100.0


    def test_all_users_returned_from_top_100_percent(self):
        n = cache.get_top_n_percent(100)

        assert n == 1


    def test_no_users_returned_from_top_0_percent(self):
        n = cache.get_top_n_percent(0)

        assert n == 0


    def test_average_number_of_days_active_returned(self):
        n = cache.n_avg_days_active()

        assert n == 1
