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
"""test_authentication_keyring.

Tests for the caosdb.connection.authentication.keyring module.
"""
import sys
from pytest import raises
from caosdb.connection.authentication.keyring import KeyringCaller


def test_initialization():
    def _callback(**config):
        assert not config
        raise Exception("_callback")
    k = KeyringCaller(callback=_callback)
    k.configure()
    with raises(Exception) as exc_info:
        assert k.password is None
    assert exc_info.value.args[0] == "_callback"
