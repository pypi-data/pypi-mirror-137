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

import pytest
import caosdb as db
from os import environ, getcwd, remove
from os.path import expanduser, isfile, join
from pytest import raises


@pytest.fixture
def temp_ini_files():
    created_temp_ini_cwd = False
    created_temp_ini_home = False
    if not isfile(join(getcwd(), "pycaosdb.ini")):
        open("pycaosdb.ini", 'a').close()  # create temporary ini file
        created_temp_ini_cwd = True
    if not isfile(expanduser("~/.pycaosdb.ini")):
        open(expanduser("~/.pycaosdb.ini"), 'a').close()  # create temporary ini file in home directory
        created_temp_ini_home = True
    yield 0
    if created_temp_ini_cwd:
        remove("pycaosdb.ini")
    if created_temp_ini_home:
        remove(expanduser("~/.pycaosdb.ini"))
    environ["PYCAOSDBINI"] = "~/.pycaosdb.ini"


def test_config_ini_via_envvar(temp_ini_files):

    with raises(KeyError):
        environ["PYCAOSDBINI"]

    environ["PYCAOSDBINI"] = "bla bla"
    assert environ["PYCAOSDBINI"] == "bla bla"
    # test wrong configuration file in envvar
    assert not expanduser(environ["PYCAOSDBINI"]) in db.configuration._read_config_files()
    # test good configuration file in envvar
    environ["PYCAOSDBINI"] = "~/.pycaosdb.ini"
    assert expanduser("~/.pycaosdb.ini") in db.configuration._read_config_files()
    # test without envvar
    environ.pop("PYCAOSDBINI")
    assert expanduser("~/.pycaosdb.ini") in db.configuration._read_config_files()
    # test configuration file in cwd
    assert join(getcwd(), "pycaosdb.ini") in db.configuration._read_config_files()
