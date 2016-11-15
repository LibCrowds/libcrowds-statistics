# -*- coding: utf8 -*-

from default import with_context
from helper import web


class TestView(web.Helper):

    @with_context
    def test_stats_view_available_at_expected_route(self):
        res = self.app.get('/statistics/')
        assert res.status_code == 200
