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
"""Tests for the _ConcreteProperty class."""


from caosdb import configure_connection
from caosdb.common.models import _ConcreteProperty
from caosdb.connection.mockup import MockUpServerConnection
# pylint: disable=missing-docstring
from nose.tools import assert_equal as eq
from nose.tools import assert_is_not_none as there
from nose.tools import assert_true as tru


def setup_module():
    there(_ConcreteProperty)
    configure_connection(url="unittests", username="testuser",
                         password_method="plain",
                         password="testpassword", timeout=200,
                         implementation=MockUpServerConnection)


def hat(obj, attr):
    tru(hasattr(obj, attr))


def test_init():
    concrete_prop = _ConcreteProperty()
    there(concrete_prop)
