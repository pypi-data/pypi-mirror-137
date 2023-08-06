# -*- encoding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
# Copyright (C) 2019 Henrik tom Wörden
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
"""Tests for the Record class."""
# pylint: disable=missing-docstring
from caosdb import Entity, Record, RecordType


def test_is_entity():
    record = Record()
    assert isinstance(record, Entity)


def test_role():
    record = Record()
    assert record.role == "Record"


def test_property_access():
    rec = Record(id=123)
    rec.add_property("Prop")
    assert rec.get_property("Pop") is None
    assert rec.get_property("Prop") is not None
    assert rec.get_property("prop") is not None
    assert rec.get_property("prOp") is not None


def test_get_parent_by_name():
    rec = Record(id="123")
    rec.add_parent(name="Test")
    assert rec.get_parent(None) is None
    assert rec.get_parent("Not existing") is None
    assert rec.get_parent("Test") is not None
    assert rec.get_parent("test") is not None
    assert rec.get_parent("tEsT") is not None


def test_get_parent_by_id():
    rec = Record(id="123")
    rec.add_parent(234)
    assert rec.get_parent(None) is None
    assert rec.get_parent(234) is not None


def test_get_parent_by_entity():
    rec = Record(id="123")
    rt = RecordType("Test", id=234)
    rec.add_parent(rt)
    assert rec.get_parent(rt) is not None

    rec = Record()
    rec.add_parent(234)
    assert rec.get_parent(rt) is not None

    rec = Record()
    rec.add_parent("Test")
    assert rec.get_parent(rt) is not None
