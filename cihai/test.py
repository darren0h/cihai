# -*- coding: utf-8 -*-
"""Helpers for cihai testsuite.

cihai.test
~~~~~~~~~~

"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

import logging
import os

logger = logging.getLogger(__name__)

database_url_default = 'sqlite:///:memory:'
database_url_environ = os.environ.get("DATABASE_URL")
data_path_default = ''
data_path_environ = os.environ.get("DATA_PATH")


database_url = (database_url_environ or database_url_default)
data_path = (data_path_environ or data_path_default)


def get_datafile(filename):
    """Wrapper around util.get_datafile for picking test fixtures."""

    if data_path_environ:
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'fixtures/', filename)
    else:
        from ..util import get_datafile
        return get_datafile(filename)
