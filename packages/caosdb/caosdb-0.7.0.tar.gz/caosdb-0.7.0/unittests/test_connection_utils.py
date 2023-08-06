# -*- coding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ** end header
#
"""Test caosdb.connection.utils."""
# pylint: disable=missing-docstring
from __future__ import unicode_literals, print_function
from pytest import raises
from nose.tools import (assert_equal as eq, assert_raises as raiz, assert_true
                        as tru, assert_is_not_none as there, assert_false as
                        falz)
from caosdb.exceptions import ConfigurationError, LoginFailedError
from caosdb.connection.utils import parse_auth_token, auth_token_to_cookie
from caosdb.connection.connection import (
    configure_connection, CaosDBServerConnection,
    _DefaultCaosDBServerConnection)
from caosdb.connection.mockup import (MockUpServerConnection, MockUpResponse,
                                      _request_log_message)
from caosdb.configuration import get_config, _reset_config
from caosdb.connection.authentication.interface import CredentialsAuthenticator
from caosdb import execute_query


def setup_module():
    _reset_config()


def test_parse_auth_token():
    assert parse_auth_token(
        "SessionToken=%5Bblablabla%5D; expires=bla; ...") == "[blablabla]"


def test_auth_token_to_cookie():
    assert auth_token_to_cookie(
        "[blablabla]") == "SessionToken=%5Bblablabla%5D;"
