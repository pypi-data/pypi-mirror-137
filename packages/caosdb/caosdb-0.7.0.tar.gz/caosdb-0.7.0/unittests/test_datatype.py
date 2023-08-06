# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (c) 2020 IndiScale GmbH
# Copyright (c) 2020 Daniel Hornung (d.hornung@indiscale.com)
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
from pytest import raises
import caosdb as db
from caosdb.common import datatype
from caosdb.common.models import _parse_value


def test_list():
    assert db.LIST("RT") == "LIST<RT>"
    assert db.LIST(db.RecordType("bla")) == "LIST<bla>"


def test_list_utilites():
    """Test for example if get_list_datatype works."""
    dtype = db.LIST(db.INTEGER)
    assert datatype.get_list_datatype(dtype) == db.INTEGER


def test_parsing_of_intger_list_values():
    dtype = db.LIST(db.INTEGER)
    assert _parse_value(dtype, [1, 2, 3]) == [1, 2, 3]
    assert _parse_value(dtype, [1]) == [1]
    assert _parse_value(dtype, [None, 1, 2, 3]) == [None, 1, 2, 3]
    assert _parse_value(dtype, [1, None, 1, 2, 3]) == [1, None, 1, 2, 3]
    assert _parse_value(dtype, ["4", 4]) == [4, 4]
    assert _parse_value(dtype, []) == []
    assert _parse_value(dtype, None) is None
    assert _parse_value(None, [1, 2, 3.14, "asdf"]) == [1, 2, 3.14, "asdf"]
    assert _parse_value(dtype, 1) == [1]

    with raises(ValueError):
        # float value in list
        _parse_value(dtype, ["4.3", 4])


def test_parsing_of_boolean_list_values():
    dtype = db.LIST(db.BOOLEAN)
    assert _parse_value(dtype, [True, False, True]) == [True, False, True]
    assert _parse_value(dtype, ["true", False, None]) == [True, False, None]

    with raises(ValueError):
        _parse_value(dtype, ["not a boolean"])


def test_parsing_of_unknown_col_datatype():
    dtype = "Arraay<TEXT>"
    obj = {"a": "b"}
    assert id(_parse_value(dtype, obj)) == id(obj)


def test_parsing_of_references():
    dtype = "Person"
    assert _parse_value(dtype, "Anna Lytik") == "Anna Lytik"
    assert _parse_value(None, "Anna Lytik") == "Anna Lytik"
    assert _parse_value(dtype, "2345@sdfg") == "2345@sdfg"
    assert _parse_value(dtype, "2345") == 2345
    assert _parse_value(dtype, 2345) == 2345

    entity = db.Record(name="bla")
    assert id(_parse_value(dtype, entity)) == id(entity)

    dtype = db.RecordType(name="Person")
    assert _parse_value(dtype, "Anna Lytik") == "Anna Lytik"
    assert _parse_value(None, "Anna Lytik") == "Anna Lytik"
    assert _parse_value(dtype, "2345@sdfg") == "2345@sdfg"
    assert _parse_value(dtype, "2345") == 2345
    assert _parse_value(dtype, 2345) == 2345

    entity = db.Record(name="bla")
    assert id(_parse_value(dtype, entity)) == id(entity)
