# -*- encoding: utf-8 -*-
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
"""Tests for the administration class."""
# pylint: disable=missing-docstring
from __future__ import unicode_literals
from pytest import raises
from caosdb import administration, configure_connection, get_connection
from caosdb.connection.mockup import MockUpServerConnection, MockUpResponse


def setup_module():
    configure_connection(url="unittests", username="testuser",
                         password_method="plain",
                         password="testpassword", timeout=200,
                         implementation=MockUpServerConnection)


def test_get_server_properties_success():
    properties = "<Properties><TEST_PROP>TEST_VAL</TEST_PROP></Properties>"
    get_connection()._delegate_connection.resources.append(
        lambda **kwargs: MockUpResponse(200, {}, properties))
    props = administration.get_server_properties()
    assert isinstance(props, dict)


def test_get_server_property_success():
    properties = "<Properties><TEST_PROP>TEST_VAL</TEST_PROP></Properties>"
    get_connection()._delegate_connection.resources.append(
        lambda **kwargs: MockUpResponse(200, {}, properties))
    assert "TEST_VAL" == administration.get_server_property("TEST_PROP")


def test_get_server_property_key_error():
    properties = "<Properties><TEST_PROP>TEST_VAL</TEST_PROP></Properties>"
    get_connection()._delegate_connection.resources.append(
        lambda **kwargs: MockUpResponse(200, {}, properties))
    with raises(KeyError) as e:
        assert administration.get_server_property("BLA")


def test_set_server_property():
    def check_form(**kwargs):
        assert kwargs["path"] == "_server_properties"
        assert kwargs["method"] == "POST"
        assert kwargs["body"] == "TEST_PROP=TEST_VAL".encode()
        assert kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
        return MockUpResponse(200, {}, "<Properties><TEST_PROP>TEST_VAL</TEST_PROP></Properties>")
    get_connection()._delegate_connection.resources.append(check_form)
    administration.set_server_property("TEST_PROP", "TEST_VAL")
