# -*- coding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2020 Timm Fitschen <t.fitschen@indiscale.com>
# Copyright (C) 2020 IndiScale GmbH <info@indiscale.com>
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
"""test_authentication_unauthenticated

Unit tests for the module caosdb.connection.authentication.unauthenticated.
"""

from __future__ import unicode_literals
from pytest import raises
from unittest.mock import Mock
from caosdb.connection.authentication import unauthenticated
from caosdb.connection.mockup import MockUpServerConnection, MockUpResponse
from caosdb.connection.utils import parse_auth_token
from caosdb.exceptions import LoginFailedError
from caosdb import configure_connection
from .test_authentication_auth_token import response_with_auth_token


def test_get_authentication_provider():
    ap = unauthenticated.get_authentication_provider()
    assert isinstance(ap, unauthenticated.Unauthenticated)


def test_configure_connection():
    mock = Mock()

    def request_has_no_auth_token(**kwargs):
        """test resource"""
        assert "Cookie" not in kwargs["headers"]
        mock.method()
        return response_with_auth_token()

    c = configure_connection(password_method="unauthenticated",
                             implementation=MockUpServerConnection)
    assert isinstance(c._authenticator, unauthenticated.Unauthenticated)

    c._delegate_connection.resources.append(request_has_no_auth_token)

    assert c._authenticator.auth_token is None
    response = c._http_request(method="GET", path="test")
    assert response.read() == "ok"
    mock.method.assert_called_once()
    assert c._authenticator.auth_token is None


def test_login_raises():
    c = configure_connection(url="https://example.com",
                             password_method="unauthenticated")
    with raises(LoginFailedError):
        c._login()
