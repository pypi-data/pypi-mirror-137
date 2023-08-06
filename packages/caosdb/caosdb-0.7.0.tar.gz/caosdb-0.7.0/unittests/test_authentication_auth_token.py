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
"""test_authentication_auth_token

Unit tests for the module caosdb.connection.authentication.auth_token
"""

from __future__ import unicode_literals
from pytest import raises
from unittest.mock import Mock
from caosdb.connection.authentication import auth_token as at
from caosdb.connection.mockup import MockUpServerConnection, MockUpResponse
from caosdb.connection.utils import parse_auth_token
from caosdb.exceptions import LoginFailedError
from caosdb import configure_connection


def test_get_authentication_provider():
    ap = at.get_authentication_provider()
    assert isinstance(ap, at.AuthTokenAuthenticator)


def response_with_auth_token():
    token = "SessionToken=[response token];"
    assert parse_auth_token(token) is not None, "cookie not ok"

    return MockUpResponse(200, {"Set-Cookie": token}, "ok")


def test_configure_connection():
    def request_has_auth_token(**kwargs):
        """test resources"""
        cookie = kwargs["headers"]["Cookie"]
        assert cookie is not None
        assert cookie == "SessionToken=%5Brequest%20token%5D;"

        return response_with_auth_token()

    c = configure_connection(password_method="auth_token",
                             auth_token="[request token]",
                             implementation=MockUpServerConnection)
    assert isinstance(c._authenticator, at.AuthTokenAuthenticator)

    c._delegate_connection.resources.append(request_has_auth_token)
    assert c._authenticator.auth_token == "[request token]"
    response = c._http_request(method="GET", path="test")
    assert response.read() == "ok"
    assert c._authenticator.auth_token == "[response token]"


def test_login_raises():
    c = configure_connection(url="https://example.com",
                             password_method="auth_token",
                             auth_token="[auth_token]")
    with raises(LoginFailedError):
        c._login()


def test_logout_calls_delete():
    mock = Mock()

    def logout_resource(**kwargs):
        """logout with auth_token"""
        mock.method()
        assert kwargs["path"] == "logout"
        assert kwargs["method"] == "DELETE"

        cookie = kwargs["headers"]["Cookie"]
        assert cookie is not None
        assert cookie == "SessionToken=%5Brequest%20token%5D;"

        return MockUpResponse(200, {}, "ok")

    c = configure_connection(password_method="auth_token",
                             auth_token="[request token]",
                             implementation=MockUpServerConnection)

    c._delegate_connection.resources.append(logout_resource)
    c._logout()
    mock.method.assert_called_once()
