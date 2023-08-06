# -*- encoding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
# Copyright (C) 2020 Indiscale GmbH <info@indiscale.com>
# Copyright (C) 2020 Timm Fitschen <f.fitschen@indiscale.com>
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
from pytest import raises
import caosdb as db


def test_no_parameter():
    rec = db.Record()
    assert 0 == len(rec.get_properties())

    with raises(UserWarning) as cm:
        rec.add_property()
    assert cm.value.args[0] == ("This method expects you to pass at "
                                "least an entity, a name or an id.")
    assert 0 == len(rec.get_properties())


def test_only_value_parameter():
    rec = db.Record()
    assert 0 == len(rec.get_properties())

    with raises(UserWarning) as cm:
        rec.add_property(value="bla")
    assert cm.value.args[0] == ("This method expects you to pass at "
                                "least an entity, a name or an id.")
    assert 0 == len(rec.get_properties())


def test_property_name_ambiguity_1():
    rec = db.Record()
    assert 0 == len(rec.get_properties())

    with raises(UserWarning) as cm:
        rec.add_property("one_name", name="another_name")
    assert cm.value.args[0] == ("The first parameter was neither an "
                                "instance of Entity nor an integer. "
                                "Therefore the string representation of "
                                "your first parameter would normally be "
                                "interpreted name of the property which "
                                "is to be added. But you have also "
                                "specified a parameter 'name' in the "
                                "method call. This is ambiguous and "
                                "cannot be processed.")
    assert 0 == len(rec.get_properties())


def test_property_name_ambiguity_2():
    rec = db.Record()
    assert 0 == len(rec.get_properties())

    with raises(UserWarning) as cm:
        rec.add_property({}, name="another_name")
    assert cm.value.args[0] == ("The first parameter was neither an "
                                "instance of Entity nor an integer. "
                                "Therefore the string representation of "
                                "your first parameter would normally be "
                                "interpreted name of the property which "
                                "is to be added. But you have also "
                                "specified a parameter 'name' in the "
                                "method call. This is ambiguous and "
                                "cannot be processed.")
    assert 0 == len(rec.get_properties())


def test_property_id_ambiguity():
    rec = db.Record()
    assert 0 == len(rec.get_properties())

    with raises(UserWarning) as cm:
        rec.add_property(25, id=26)

    assert cm.value.args[0] == ("The first parameter was an integer which "
                                "would normally be interpreted as the id of "
                                "the property which is to be added. But you "
                                "have also specified a parameter 'id' in the "
                                "method call. This is ambiguous and cannot be "
                                "processed.")
    assert 0 == len(rec.get_properties())


def test_property_parameter_with_entity():
    rec = db.Record()
    abstract_property = db.Property(
        name="length",
        id=512,
        datatype=db.DOUBLE,
        unit="m",
        description="This is the length of something.")

    assert 0 == len(rec.get_properties())
    rec.add_property(abstract_property)
    assert 1 == len(rec.get_properties())
    concrete_property = rec.get_property("length")
    assert concrete_property is not None
    assert concrete_property.name == "length"
    assert concrete_property.id == 512
    assert concrete_property.description == "This is the length of something."
    assert concrete_property.unit == "m"
    assert concrete_property.datatype == db.DOUBLE
    assert concrete_property._wrapped_entity == abstract_property


def test_property_parameter_with_entity_and_value():
    rec = db.Record()
    abstract_property = db.Property(
        name="length",
        id=512,
        datatype=db.DOUBLE,
        unit="m",
        description="This is the length of something.")

    assert 0 == len(rec.get_properties())
    rec.add_property(abstract_property, 3.14)
    assert 1 == len(rec.get_properties())
    concrete_property = rec.get_property("length")
    assert concrete_property is not None
    assert concrete_property.name == "length"
    assert concrete_property.id == 512
    assert concrete_property.description == "This is the length of something."
    assert concrete_property.unit == "m"
    assert concrete_property.value == 3.14
    assert concrete_property.datatype == db.DOUBLE
    assert concrete_property._wrapped_entity == abstract_property


def test_property_parameter_with_id():
    rec = db.Record()

    assert 0 == len(rec.get_properties())
    rec.add_property(512)
    assert 1 == len(rec.get_properties())
    concrete_property = rec.get_property(512)
    assert concrete_property is not None
    assert concrete_property.id == 512


def test_property_parameter_with_id_and_value():
    rec = db.Record()

    assert 0 == len(rec.get_properties())
    rec.add_property(512, 3.14)
    assert 1 == len(rec.get_properties())
    concrete_property = rec.get_property(512)
    assert concrete_property is not None
    assert concrete_property.id == 512
    assert concrete_property.value == 3.14


def test_datatype():
    rec = db.Record()

    assert 0 == len(rec.get_properties())
    rec.add_property(512, 3.14)
    assert 1 == len(rec.get_properties())
    concrete_property = rec.get_property(512)
    assert concrete_property is not None
    assert concrete_property.id == 512
    assert concrete_property.value == 3.14


def test_property_parameter_with_entity_and_datatype():
    rec = db.Record()
    abstract_property = db.Property(
        name="length",
        id=512,
        datatype=db.DOUBLE,
        unit="m",
        description="This is the length of something.")

    assert 0 == len(rec.get_properties())
    rec.add_property(abstract_property, 300, datatype=db.INTEGER)
    assert 1 == len(rec.get_properties())
    concrete_property = rec.get_property("length")
    assert concrete_property is not None
    assert concrete_property.name == "length"
    assert concrete_property.id == 512
    assert concrete_property.description == "This is the length of something."
    assert concrete_property.unit == "m"
    assert concrete_property.value == 300
    assert concrete_property.datatype == db.INTEGER
    assert id(concrete_property._wrapped_entity) == id(abstract_property)

    concrete_property.value = None

    with raises(ValueError):
        # cannot parse 3.14 to integer
        concrete_property.value = 3.14

    assert concrete_property.value is None
    assert concrete_property.datatype == db.INTEGER

    concrete_property.datatype = db.DOUBLE
    concrete_property.value = 3.14

    with raises(ValueError):
        # cannot parse 3.14 to integer
        concrete_property.datatype = db.INTEGER

    # nothing should've changed after the ValueError
    assert concrete_property.datatype == db.DOUBLE
    assert concrete_property.value == 3.14


def test_kw_name_and_value():
    rec = db.Record()

    assert 0 == len(rec.get_properties())
    rec.add_property(name="length", value=3.14)
    assert 1 == len(rec.get_properties())
    concrete_property = rec.get_property("length")
    assert concrete_property is not None
    assert concrete_property.value == 3.14


def test_kw_id_and_value():
    rec = db.Record()

    assert 0 == len(rec.get_properties())
    rec.add_property(id=512, value=3.14)
    assert 1 == len(rec.get_properties())
    concrete_property = rec.get_property(512)
    assert concrete_property is not None
    assert concrete_property.value == 3.14


def test_add_list_of_entitities():
    rec = db.Record()
    values = []
    for i in range(10):
        values.append(db.Record(name=str(i)))
    rec.add_property("listOfEntities", values)
    for e in rec.get_property("listOfEntities").value:
        assert e.id is None

    i = 0
    for val in values:
        val.id = i
        i += 1

    i = 0
    for e in rec.get_property("listOfEntities").value:
        assert i == e.id
        i += 1


def test_add_property_with_wrong_role():
    entity = db.Entity()

    r = db.Record()
    rt = db.RecordType()
    p = db.Property()
    f = db.File()
    e = db.Entity()

    entity.add_property(rt)
    entity.add_property(p)
    entity.add_property(e)

    with raises(ValueError) as cm:
        entity.add_property(r)
    assert cm.value.args[0] == ("The property parameter is a Record. This is "
                                "very unusual and probably not what you want. "
                                "Otherwise, construct a property from a "
                                "Record using the Property class and add that "
                                "to this entity.")

    with raises(ValueError) as cm:
        entity.add_property(f)
    assert cm.value.args[0] == ("The property parameter is a File. This is "
                                "very unusual and probably not what you want. "
                                "Otherwise, construct a property from a File "
                                "using the Property class and add that to "
                                "this entity.")
