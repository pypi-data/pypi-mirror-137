# -*- encoding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
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
# Test apiutils
# A. Schlemmer, 02/2018

import pickle
import tempfile

import caosdb as db
import caosdb.apiutils
from caosdb.apiutils import (apply_to_ids, compare_entities, create_id_query,
                             resolve_reference)

from .test_property import testrecord


def test_convert_object():
    r2 = db.apiutils.convert_to_python_object(testrecord)
    assert r2.species == "Rabbit"


def test_pickle_object():
    r2 = db.apiutils.convert_to_python_object(testrecord)
    with tempfile.TemporaryFile() as f:
        pickle.dump(r2, f)
        f.seek(0)
        rn2 = pickle.load(f)
    assert r2.date == rn2.date


def test_apply_to_ids():
    parent = db.RecordType(id=3456)
    rec = db.Record(id=23)
    p = db.Property(id=23345, datatype=db.INTEGER)
    rec.add_parent(parent)
    rec.add_property(p)

    def invert(id_):
        return id_ * -1
    apply_to_ids([rec], invert)

    assert invert(3456) == -3456
    assert rec.parents[0].id == -3456
    assert rec.properties[0].id == -23345
    assert rec.id == -23


def test_id_query():
    ids = [1, 2, 3, 4, 5]
    assert create_id_query(ids) == 'FIND ENTITY WITH ID=1 OR ID=2 OR ID=3 OR '\
        'ID=4 OR ID=5'


def test_resolve_reference():
    original_retrieve_entity_with_id = caosdb.apiutils.retrieve_entity_with_id
    caosdb.apiutils.retrieve_entity_with_id = lambda eid: db.Record(id=eid)

    prop = db.Property(id=1, datatype=db.REFERENCE, value=100)
    prop.is_valid = lambda: True
    items = [200, 300, 400]
    prop_list = db.Property(datatype=db.LIST(db.REFERENCE),
                            value=items)
    prop_list2 = db.Property(datatype=db.LIST(db.REFERENCE),
                             value=[db.Record(id=500)])
    resolve_reference(prop)
    resolve_reference(prop_list)
    resolve_reference(prop_list2)
    assert prop.value.id == 100
    assert isinstance(prop.value, db.Entity)

    prop_list_ids = []

    for i in prop_list.value:
        prop_list_ids.append(i.id)
        assert isinstance(i, db.Entity)
    assert prop_list_ids == items

    for i in prop_list2.value:
        assert i.id == 500
        assert isinstance(i, db.Entity)

    no_reference = db.Property(id=5000, datatype=db.INTEGER, value=2)
    resolve_reference(no_reference)
    assert no_reference.value == 2
    assert no_reference.datatype is db.INTEGER

    # restore retrive_entity_with_id
    caosdb.apiutils.retrieve_entity_with_id = original_retrieve_entity_with_id


def test_compare_entities():
    r1 = db.Record()
    r2 = db.Record()
    r1.add_parent("bla")
    r2.add_parent("bla")
    r1.add_parent("lopp")
    r1.add_property("test", value=2)
    r2.add_property("test", value=2)
    r1.add_property("tests", value=3)
    r2.add_property("tests", value=45)
    r1.add_property("tester", value=3)
    r2.add_property("tester", )
    r1.add_property("tests_234234", value=45)
    r2.add_property("tests_TT", value=45)

    diff_r1, diff_r2 = compare_entities(r1, r2)

    assert len(diff_r1["parents"]) == 1
    assert len(diff_r2["parents"]) == 0
    assert len(diff_r1["properties"]) == 3
    assert len(diff_r2["properties"]) == 3

    assert "test" not in diff_r1["properties"]
    assert "test" not in diff_r2["properties"]

    assert "tests" in diff_r1["properties"]
    assert "tests" in diff_r2["properties"]

    assert "tester" in diff_r1["properties"]
    assert "tester" in diff_r2["properties"]

    assert "tests_234234" in diff_r1["properties"]
    assert "tests_TT" in diff_r2["properties"]


def test_compare_entities_units():
    r1 = db.Record()
    r2 = db.Record()
    r1.add_parent("bla")
    r2.add_parent("bla")
    r1.add_parent("lopp")
    r1.add_property("test", value=2, unit="cm")
    r2.add_property("test", value=2, unit="m")
    r1.add_property("tests", value=3, unit="cm")
    r2.add_property("tests", value=45, unit="cm")
    r1.add_property("tester", value=3)
    r2.add_property("tester", )
    r1.add_property("tests_234234", value=45, unit="cm")
    r2.add_property("tests_TT", value=45, unit="cm")

    diff_r1, diff_r2 = compare_entities(r1, r2)

    assert len(diff_r1["parents"]) == 1
    assert len(diff_r2["parents"]) == 0
    assert len(diff_r1["properties"]) == 4
    assert len(diff_r2["properties"]) == 4

    assert "tests" in diff_r1["properties"]
    assert "tests" in diff_r2["properties"]

    assert "tester" in diff_r1["properties"]
    assert "tester" in diff_r2["properties"]

    assert "tests_234234" in diff_r1["properties"]
    assert "tests_TT" in diff_r2["properties"]

    assert diff_r1["properties"]["test"]["unit"] == "cm"
    assert diff_r2["properties"]["test"]["unit"] == "m"
