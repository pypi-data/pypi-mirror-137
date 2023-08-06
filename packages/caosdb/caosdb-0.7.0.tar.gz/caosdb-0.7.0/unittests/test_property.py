# -*- encoding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
# Copyright (C) 2020 IndiScale GmbH <info@indiscale.com>
# Copyright (C) 2020 Timm Fitschen <t.fitschen@indiscale.com>
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
"""Tests for the Property class."""
import os

import caosdb as db
from caosdb import Entity, Property, Record
# pylint: disable=missing-docstring
from lxml import etree

parser = etree.XMLParser(remove_comments=True)
testrecord = Record._from_xml(
    Record(),
    etree.parse(os.path.join(os.path.dirname(__file__), "test_record.xml"),
                parser).getroot())


def test_is_entity():
    prop = Property()
    assert isinstance(prop, Entity)


def test_instance_variables():
    prop = Property()
    assert hasattr(prop, "datatype")
    assert hasattr(prop, "unit")
    assert hasattr(prop, "value")


def test_null_empty_text_value_1():
    assert testrecord.get_property("LISTofTEXT").value == ["One", "Two",
                                                           "Three", None, ""]


def test_null_empty_text_value_2():
    assert testrecord.get_property("NULLTEXT1").value is None


def test_null_empty_text_value_3():
    assert testrecord.get_property("NULLTEXT2").value is None


def test_null_empty_text_value_4():
    assert testrecord.get_property("EMPTYTEXT1").value == ""


def test_null_empty_text_value_5():
    assert testrecord.get_property("EMPTYTEXT2").value == ""


def test_list_of_references_with_null():
    assert testrecord.get_property("MultiRecRecording").value[0] is None
    assert testrecord.get_property("MultiRecRecording").value[1] == 170651


def test_role():
    prop = Property()
    assert prop.role == "Property"


def test_get_property_with_entity():
    p = Property(name="Prop")
    r = Record().add_property("Prop", "blub")
    assert r.get_property(p).value == "blub"

    p = Property(id=1234)
    r.add_property(id=1234, value="bla")
    assert r.get_property(p).value == "bla"


def test_selected_reference_list():
    assert len(testrecord.get_property("Conductor").value) == 1
    assert isinstance(testrecord.get_property("Conductor").value[0], Entity)


def test_is_reference():
    PROPS = {
        10:  db.INTEGER,
        20:  db.REFERENCE,
        30:  "SomeRT",
    }

    def dummy_retrieve(self):
        self.datatype = PROPS[self.id]
        self.is_valid = lambda: True
    # replace retrieve function by dummy
    real_retrieve = Entity.retrieve
    Entity.retrieve = dummy_retrieve

    p1 = Property(id=1, datatype=db.INTEGER)
    p2 = Property(id=2, datatype=db.DOUBLE)
    p3 = Property(id=3, datatype=db.TEXT)
    p4 = Property(id=4, datatype=db.DATETIME)
    p5 = Property(id=5, datatype=db.BOOLEAN)
    p6 = Property(id=6, datatype=db.REFERENCE)
    assert p1.is_reference() is False
    assert p2.is_reference() is False
    assert p3.is_reference() is False
    assert p4.is_reference() is False
    assert p5.is_reference() is False
    assert p6.is_reference() is True

    p7 = Property(id=7)
    p8 = Property(id=8, value=db.RecordType(id=1000))
    p8.is_valid = lambda: True
    assert p7.is_reference() is None  # cannot be resolved without calling a server
    assert p8.is_reference() is True

    p10 = Property(id=10)
    p20 = Property(id=20)
    p30 = Property(id=30)
    assert p10.is_reference(server_retrieval=True) is False
    assert p20.is_reference(server_retrieval=True) is True
    assert p30.is_reference(server_retrieval=True) is True

    # restore retrieve function with original
    Entity.retrieve = real_retrieve
