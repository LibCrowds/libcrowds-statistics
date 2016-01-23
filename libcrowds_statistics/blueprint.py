# -*- coding: utf8 -*-
"""Blueprint module for libcrowds-statistics."""

from flask import Blueprint
from .view import index


class StatisticsBlueprint(Blueprint):
    """Blueprint to support additional views.

    Parameters
    ----------
    **kwargs
        Arbitrary keyword arguments.
    """

    def __init__(self, **kwargs):
        """Initialise blueprint instance."""
        defaults = {'name': 'statistics', 'import_name': __name__}
        defaults.update(kwargs)

        super(StatisticsBlueprint, self).__init__(**defaults)

        self.add_url_rule("/", view_func=index)
