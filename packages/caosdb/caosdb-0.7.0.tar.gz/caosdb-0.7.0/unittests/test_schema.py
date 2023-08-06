# -*- coding: utf-8 -*-
#
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2021 Alexander Schlemmer
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

"""Test configuration schema.
A. Schlemmer, 01/2021
"""
from jsonschema.exceptions import ValidationError
from pytest import raises
from glob import glob
import os
from caosdb.configuration import config_to_yaml, validate_yaml_schema
from configparser import ConfigParser


def test_config_files():
    for fn in glob(os.path.join(os.path.dirname(__file__), "test_configs", "*.ini")):
        c = ConfigParser()
        c.read(fn)
        validate_yaml_schema(config_to_yaml(c))


def test_broken_config_files():
    for fn in glob(os.path.join(os.path.dirname(__file__), "broken_configs", "*.ini")):
        print(fn)
        with raises(ValidationError):
            c = ConfigParser()
            c.read(fn)
            validate_yaml_schema(config_to_yaml(c))
