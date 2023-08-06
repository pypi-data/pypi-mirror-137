#! -*- coding: utf-8 -*-
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
"""test_authentication_external.

Tests for the external_credentials_provider modul.
"""

from __future__ import unicode_literals
import logging
from pytest import raises
from caosdb.connection.authentication import (
    external_credentials_provider as ecp
)


class _TestCaller(ecp.ExternalCredentialsProvider):
    pass


def test_callback():
    def _callback(**config):
        assert "opt" in config
        return "secret"
    t = _TestCaller(callback=_callback)
    t.configure(opt=None)
    assert t.password == "secret"


def test_log_password_incident():
    class _mylogger(logging.Logger):
        def log(self, level, msg, *args, **kwargs):
            assert level == logging.WARNING
            assert "`password` defined." in msg
            raise Exception("log")

    t = _TestCaller(callback=None)
    t.logger = _mylogger("mylogger")
    with raises(Exception) as exc_info:
        t.configure(password="password")
    assert exc_info.value.args[0] == "log"
