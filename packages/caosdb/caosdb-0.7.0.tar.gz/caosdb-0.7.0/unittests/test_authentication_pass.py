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
"""test_authentication_pass.

Tests for the caosdb.connection.authentication.pass module.
"""
import sys
from pytest import raises
_PASSCALLER = "caosdb.connection.authentication.pass"
__import__(_PASSCALLER)
PassCaller = sys.modules[_PASSCALLER].PassCaller


def test_initialization():
    def _callback(**config):
        assert not config
        raise Exception("_callback")
    p = PassCaller(callback=_callback)
    p.configure()
    with raises(Exception) as exc_info:
        p.password
    assert exc_info.value.args[0] == "_callback"
