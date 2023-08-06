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
"""Test caosdb.connection."""
# pylint: disable=missing-docstring
from __future__ import print_function, unicode_literals

import re
from builtins import bytes, str  # pylint: disable=redefined-builtin

from caosdb import execute_query
from caosdb.configuration import _reset_config, get_config
from caosdb.connection.authentication.interface import CredentialsAuthenticator
from caosdb.connection.connection import (CaosDBServerConnection,
                                          _DefaultCaosDBServerConnection,
                                          configure_connection)
from caosdb.connection.mockup import (MockUpResponse, MockUpServerConnection,
                                      _request_log_message)
from caosdb.connection.utils import make_uri_path, quote, urlencode
from caosdb.exceptions import ConfigurationError, LoginFailedError
from nose.tools import assert_equal as eq
from nose.tools import assert_false as falz
from nose.tools import assert_is_not_none as there
from nose.tools import assert_raises as raiz
from nose.tools import assert_true as tru
from pytest import raises


def setup_module():
    _reset_config()


def test_quote():
    unenc = 'ö'
    eq('%C3%B6', quote(unenc))

    unenc = '\xf6'
    eq('%C3%B6', quote(unenc))

    unenc = str('ö')
    eq('%C3%B6', quote(unenc))


def test_urlencode():
    eq(urlencode({}), '')
    eq(urlencode({'key1': 'val1'}), 'key1=val1')
    eq(urlencode({'keynoval': None}), 'keynoval=')
    eq(urlencode({'kèy': 'välüe'}), 'k%C3%A8y=v%C3%A4l%C3%BCe')
    with raiz(AttributeError):
        urlencode({bytes('asdf', 'utf-8'): 'asdf'})
    with raiz(AttributeError):
        urlencode({'asdf': bytes('asdf', 'utf-8')})
    with raiz(AttributeError):
        urlencode({None: 'asdf'})


def test_make_uri_path():
    eq(make_uri_path(None, None), '')
    eq(make_uri_path(None, {"key": "val"}), "?key=val")
    eq(make_uri_path([]), "")
    eq(make_uri_path(['a', 'b']), 'a/b')
    eq(make_uri_path(['a', str('b')]), 'a/b')
    eq(make_uri_path(['a', 'ö']), 'a/%C3%B6')
    eq(make_uri_path(['a', str('ö')]), 'a/%C3%B6')
    eq(make_uri_path(['a', 'b'], {'key': 'val'}), 'a/b?key=val')
    eq(make_uri_path([], {"key": "val"}), "?key=val")
    eq(make_uri_path([], {"key": str("val")}), "?key=val")
    eq(make_uri_path([], {"key": None}), "?key=")
    tru(
        re.match(r"^\?(key1=val1&key2=val2|key2=val2&key1=val1)$",
                 make_uri_path([], {
                     "key1": "val1",
                     "key2": "val2"
                 })))
    eq(make_uri_path(['a', 'with/slash']), 'a/with%2Fslash')


def test_configure_connection():
    if not get_config().has_section("Connection"):
        get_config().add_section("Connection")
    get_config().set("Connection", "url", "https://host.de")
    get_config().set("Connection", "username", "test_username")
    get_config().set("Connection", "password_method", "plain")
    get_config().set("Connection", "password", "test_password")
    get_config().set("Connection", "timeout", "200")

    there(configure_connection)
    tru(hasattr(configure_connection, "__call__"))
    c = configure_connection()
    there(c)
    tru(isinstance(c._delegate_connection, _DefaultCaosDBServerConnection))
    tru(isinstance(c._authenticator, CredentialsAuthenticator))

    c = configure_connection(
        implementation=MockUpServerConnection)
    tru(isinstance(c._delegate_connection, MockUpServerConnection))


def test_connection_interface():
    with raiz(TypeError) as cm:
        CaosDBServerConnection()
    eq(cm.exception.args[0][:55],
       "Can't instantiate abstract class CaosDBServerConnection")

    tru(hasattr(CaosDBServerConnection, "request"))
    tru(hasattr(CaosDBServerConnection.request, "__call__"))

    tru(hasattr(CaosDBServerConnection, "configure"))
    tru(hasattr(CaosDBServerConnection.configure, "__call__"))


def test_use_mockup_implementation():
    with raiz(RuntimeError) as rerr:
        execute_query("FIND Something")
    print(rerr.exception.args[0])
    eq(rerr.exception.args[0],
       "No response for this request - GET: Entity?query=FIND%20Something")


def test_request_log_message():
    headers = {"k0": "v0"}
    body = "this is the body"
    eq(
        _request_log_message(
            method="GET", path="path", headers=None, body=None), "GET: path")
    eq(
        _request_log_message(
            method="GET", path="path", headers=headers, body=None),
        "GET: path\n" + str(headers))
    eq(
        _request_log_message(
            method="GET", path="path", headers=headers, body=body),
        "GET: path\n" + str(headers) + "\n" + str(body))


def test_init_response():
    response = MockUpResponse(
        status=200, headers={"sessionToken": "SessionToken"}, body="Body")
    there(response)

    return response


def test_getter_status():
    response = test_init_response()
    eq(response.status, 200)


def test_read():
    response = test_init_response()
    tru(hasattr(response, "read"))
    eq(response.read(), "Body")


def test_getter_session_token():
    response = test_init_response()
    tru(hasattr(response, "getheader"))
    eq(response.getheader("sessionToken"), "SessionToken")


def test_init_connection():
    connection = MockUpServerConnection()
    there(connection)

    return connection


def test_resources_list():
    connection = test_init_connection()
    assert hasattr(connection, "resources")
    assert len(connection.resources) == 1
    connection.resources.append(lambda **kwargs: test_init_response())
    assert len(connection.resources) == 2

    return connection


def test_request_basics():
    connection = test_init_connection()
    tru(hasattr(connection, "request"))
    with raiz(RuntimeError) as cm:
        connection.request(method="GET", path="asdf")
    eq(cm.exception.args[0], "No response for this request - GET: asdf")
    connection = test_resources_list()
    there(connection.request(method="GET", path="asdf"))


def setup_two_resources():
    def r1(**kwargs):
        if kwargs["method"] == "GET":
            return MockUpResponse(status=200, headers=kwargs["headers"], body="response r1")

    def r2(**kwargs):
        if kwargs["path"] == "matching/path/":
            return MockUpResponse(
                status=456, headers={"key": "val"}, body="response r2")

    def r3(**kwargs):
        if kwargs["path"] == "401":
            return MockUpResponse(
                status=401, headers={}, body="please login")

    connection = test_init_connection()
    connection.resources.extend([r1, r2, r3])

    return connection


def test_test_request_with_two_responses():
    connection = setup_two_resources()
    eq(connection.request(method="GET", path="any", headers={}).status, 200)
    eq(connection.request(method="POST", path="matching/path/").status, 456)


def test_missing_implementation():
    connection = configure_connection()
    with raises(ConfigurationError) as exc_info:
        connection.configure()
    assert exc_info.value.args[0].startswith(
        "Missing CaosDBServerConnection implementation.")


def test_bad_implementation_not_callable():
    connection = configure_connection()
    with raises(ConfigurationError) as exc_info:
        connection.configure(implementation=None)
    assert exc_info.value.args[0].startswith(
        "Bad CaosDBServerConnection implementation.")
    assert "'NoneType' object is not callable" in exc_info.value.args[0]


def test_bad_implementation_wrong_class():
    connection = configure_connection()
    with raises(ConfigurationError) as exc_info:
        connection.configure(implementation=dict)
    assert exc_info.value.args[0].startswith(
        "Bad CaosDBServerConnection implementation.")
    assert ("The `implementation` callable did not return an instance of "
            "CaosDBServerConnection.") in exc_info.value.args[0]


def test_missing_auth_method():
    connection = configure_connection()
    with raises(ConfigurationError) as exc_info:
        connection.configure(implementation=MockUpServerConnection)
    assert exc_info.value.args[0].startswith("Missing password_method.")


def test_missing_password():
    connection = configure_connection()
    connection.configure(implementation=setup_two_resources,
                         password_method="plain")
    connection._authenticator.auth_token = "[test-auth-token]"
    assert connection.retrieve(
        ["some"]).headers["Cookie"] == "SessionToken=%5Btest-auth-token%5D;"

    connection.configure(implementation=setup_two_resources,
                         password_method="plain")
    with raises(LoginFailedError):
        connection.delete(["401"])


def test_auth_token_connection():
    connection = configure_connection(auth_token="blablabla",
                                      password_method="auth_token",
                                      implementation=setup_two_resources)
    connection.retrieve(
        ["some"]).headers["Cookie"] == "SessionToken=blablabla;"

    connection._logout()
    with raises(LoginFailedError) as cm:
        connection.retrieve(
            ["some"]).headers["Cookie"] == "SessionToken=blablabla;"
    assert cm.value.args[0] == ("The authentication token is expired or you "
                                "have been logged out otherwise. The "
                                "auth_token authenticator cannot log in "
                                "again. You must provide a new authentication "
                                "token.")
