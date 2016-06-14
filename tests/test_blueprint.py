# -*- coding: utf8 -*-

import os
import tempfile
from default import with_context
from helper import web
from flask import url_for
from libcrowds_statistics import view


class TestBlueprint(web.Helper):

    def test_all_view_functions_registered(self):
        funcs = [view.index]
        registered = [r for r in self.flask_app.url_map.iter_rules()]
        assert not set(funcs).issubset(set(registered))

    def test_templates_folder_exists(self):
        bp = self.flask_app.blueprints['statistics']
        template_folder = os.path.abspath(bp.template_folder)
        assert os.path.isdir(template_folder), template_folder

    def test_static_folder_exists(self):
        bp = self.flask_app.blueprints['statistics']
        static_folder = os.path.abspath(bp.static_folder)
        assert os.path.isdir(static_folder), static_folder

    @with_context
    def test_static_folder_available_at_expected_route(self):
        bp = self.flask_app.blueprints['statistics']
        static_folder = bp.static_folder
        tmp = tempfile.NamedTemporaryFile(dir=static_folder)
        tmp_fn = os.path.basename(tmp.name)
        res = self.app.get(url_for('statistics.static', filename=tmp_fn))
        assert res.status_code == 200, res.status_code
