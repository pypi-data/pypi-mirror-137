# -*- encoding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2020 Indiscale GmbH <info@indiscale.com>
# Copyright (C) 2020 Florian Spreckelsen <f.spreckelsen@indiscale.com>
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
"""Test the new (as of June 2020) error handling. All errors should
be TransactionErrors at first which may have one or more level of
children.

"""
import caosdb as db
from caosdb.common.models import raise_errors
from caosdb.exceptions import (AuthorizationError,
                               EntityDoesNotExistError, EntityError,
                               EntityHasNoDatatypeError,
                               TransactionError, UniqueNamesError,
                               UnqualifiedParentsError,
                               UnqualifiedPropertiesError)

from pytest import raises


# #################### Single Error Tests ####################


def _add_error_message_to_entity(entity, code, description="Error message"):
    """Attach error message with code and description to entity"""
    message = db.Message(type="Error", code=code,
                         description=description)
    entity.add_message(message)

    return entity


def test_has_no_datatype_error():
    """Code 110; property without datatype"""
    code = 110
    prop = _add_error_message_to_entity(db.Property(name="TestProp"),
                                        code)
    with raises(TransactionError) as e:
        raise_errors(prop)
    # There should be exactly one child
    assert len(e.value.errors) == 1
    err = e.value.errors[0]
    # check type and entity of only child
    assert isinstance(err, EntityHasNoDatatypeError)
    assert err.entity.name == prop.name


def test_entity_does_not_exist_error():
    """Code 101; entity does not exist"""
    code = 101
    ent = _add_error_message_to_entity(db.Entity(name="TestEnt"),
                                       code)
    with raises(TransactionError) as e:
        raise_errors(ent)
    # There should be exactly one child
    assert len(e.value.errors) == 1
    err = e.value.errors[0]
    # check type and entity of only child
    assert isinstance(err, EntityDoesNotExistError)
    assert err.entity.name == ent.name


def test_entity_error():
    """Code 0; most basic."""
    code = 0
    ent = _add_error_message_to_entity(db.Entity(name="TestEnt"),
                                       code)
    with raises(TransactionError) as e:
        raise_errors(ent)
    assert len(e.value.errors) == 1
    err = e.value.errors[0]
    assert isinstance(err, EntityError)
    assert err.entity.name == ent.name


def test_unique_names_error():
    """Code 152; name is not unique"""
    code = 152
    ent = _add_error_message_to_entity(db.Entity(name="TestEnt"),
                                       code)
    with raises(TransactionError) as e:
        raise_errors(ent)
    assert len(e.value.errors) == 1
    err = e.value.errors[0]
    assert isinstance(err, UniqueNamesError)
    assert err.entity.name == ent.name


def test_authorization_exception():
    """Code 403; transaction not allowed"""
    code = 403
    ent = _add_error_message_to_entity(db.Entity(name="TestEnt"),
                                       code)
    with raises(TransactionError) as e:
        raise_errors(ent)
    assert len(e.value.errors) == 1
    err = e.value.errors[0]
    assert isinstance(err, AuthorizationError)
    assert err.entity.name == ent.name


def test_empty_container_with_error():
    """Has to raise an error, even though container is empty."""
    code = 0
    cont = _add_error_message_to_entity(db.Container(), code)
    with raises(TransactionError) as e:
        raise_errors(cont)
    # No entity errors
    assert len(e.value.errors) == 0
    assert e.value.container == cont
    assert int(e.value.code) == code


def test_faulty_container_with_healthy_entities():
    """Raises a TransactionError without any EntityErrors since only the
    container, but none of its entities has an error.

    """
    code = 0
    cont = _add_error_message_to_entity(db.Container(), code)
    cont.append(db.Entity("TestHealthyEnt1"))
    cont.append(db.Entity("TestHealthyEnt2"))
    with raises(TransactionError) as e:
        raise_errors(cont)
    # No entity errors
    assert len(e.value.errors) == 0
    assert len(e.value.entities) == 0
    assert e.value.container == cont
    assert int(e.value.code) == code


# #################### Children with children ####################


def test_unqualified_parents_error():
    """Code 116; parent does not exist"""
    code = 116
    entity_does_not_exist_code = 101
    parent = _add_error_message_to_entity(
        db.RecordType(name="TestParent"),
        entity_does_not_exist_code)
    rec = _add_error_message_to_entity(db.Record(name="TestRecord"),
                                       code)
    rec.add_parent(parent)
    with raises(TransactionError) as e:
        raise_errors(rec)
    te = e.value
    # One direct child, two errors in total
    assert len(te.errors) == 1
    assert len(te.all_errors) == 2
    # UnqualifiedParentsError in Record ...
    assert isinstance(te.errors[0], UnqualifiedParentsError)
    assert te.errors[0].entity.name == rec.name
    # ... caused by non-existing parent
    assert isinstance(te.errors[0].errors[0], EntityDoesNotExistError)
    assert te.errors[0].errors[0].entity.name == parent.name


def test_unqualified_properties_error():
    """Code 114; properties do not exist or have wrong data types or
    values.

    """
    code = 114
    entity_code = 0
    no_entity_code = 101
    prop1 = _add_error_message_to_entity(db.Property(
        name="TestProp1"), entity_code)
    prop2 = _add_error_message_to_entity(db.Property(
        name="TestProp2"), no_entity_code)
    rec = _add_error_message_to_entity(db.Record(name="TestRecord"),
                                       code)
    rec.add_property(prop1).add_property(prop2)
    with raises(TransactionError) as e:
        raise_errors(rec)
    te = e.value
    assert len(te.errors) == 1
    upe = te.errors[0]
    assert upe.entity.name == rec.name
    assert len(upe.errors) == 2
    for error_t in [UnqualifiedPropertiesError, EntityError,
                    EntityDoesNotExistError]:
        assert any([isinstance(x, error_t) for x in te.all_errors])
    assert upe.code == code


# #################### Multiple errors ####################

def test_parent_and_properties_errors():
    """Record with UnqualifiedParentsError and UnqualifiedPropertiesError,
    and corresponding parent and properties with their errors as
    above. Test whether all levels are in order.

    """
    prop_code = 114
    parent_code = 116
    entity_code = 0
    no_entity_code = 101
    parent = _add_error_message_to_entity(
        db.RecordType(name="TestParent"), no_entity_code)
    prop1 = _add_error_message_to_entity(db.Property(
        name="TestProp1"), entity_code)
    prop2 = _add_error_message_to_entity(db.Property(
        name="TestProp2"), no_entity_code)
    rec = _add_error_message_to_entity(db.Record(name="TestRecord"),
                                       prop_code)
    rec = _add_error_message_to_entity(rec, parent_code)
    rec.add_parent(parent)
    rec.add_property(prop1).add_property(prop2)
    with raises(TransactionError) as e:
        raise_errors(rec)
    # Now there should be two direct children; both have to be
    # displayed correctly.
    te = e.value
    # exactly two children:
    assert len(te.errors) == 2
    # both have to have the right codes and entities
    found_parent = False
    found_prop = False
    for err in te.errors:
        if err.code == parent_code:
            found_parent = True
            assert err.errors[0].entity.name == parent.name
            assert prop1.name not in [x.name for x in
                                      err.all_entities]
            assert prop2.name not in [x.name for x in
                                      err.all_entities]
        elif err.code == prop_code:
            found_prop = True
            assert parent.name not in [x.name for x in
                                       err.all_entities]
            for sub_err in err.errors:
                if sub_err.code == entity_code:
                    assert sub_err.entity.name == prop1.name
                elif sub_err.code == no_entity_code:
                    assert sub_err.entity.name == prop2.name
    assert found_parent
    assert found_prop


def test_container_with_faulty_elements():
    """Code 12; container with valid and invalid entities. All faulty
    entities have to be reflected correctly in the errors list of the
    TransactionError raised by the container.

    """
    container_code = 12
    prop_code = 114
    parent_code = 116
    name_code = 152
    auth_code = 403
    entity_code = 0
    no_entity_code = 101
    # Broken parents and properties
    parent = _add_error_message_to_entity(
        db.RecordType(name="TestParent"), no_entity_code)
    prop1 = _add_error_message_to_entity(db.Property(
        name="TestProp1"), entity_code)
    prop2 = _add_error_message_to_entity(db.Property(
        name="TestProp2"), no_entity_code)
    cont = _add_error_message_to_entity(db.Container(),
                                        container_code)
    # healthy record and property
    good_rec = db.Record(name="TestRecord1")
    good_prop = db.Property(name="TestProp3")
    cont.extend([good_rec, good_prop])
    # broken records with single and multiole errors
    rec_name = _add_error_message_to_entity(db.Record(name="TestRecord2"),
                                            code=name_code)
    rec_auth = _add_error_message_to_entity(db.Record(name="TestRecord3"),
                                            code=auth_code)
    rec_par_prop = _add_error_message_to_entity(
        db.Record(name="TestRecord"), prop_code)
    rec_par_prop = _add_error_message_to_entity(rec_par_prop, parent_code)
    rec_par_prop.add_parent(parent)
    rec_par_prop.add_property(prop1).add_property(prop2)
    cont.extend([rec_name, rec_auth, rec_par_prop])
    with raises(TransactionError) as e:
        raise_errors(cont)
    te = e.value
    assert te.container == cont
    assert te.code == container_code
    # no healthy entity caused an error
    for good in [good_rec, good_prop]:
        assert good not in te.all_entities
    # all records that caused problems
    assert {rec_name, rec_auth, rec_par_prop}.issubset(te.all_entities)
    # the container error contains the errors caused by the records
    for err in te.errors:
        if err.entity.name == rec_name.name:
            assert isinstance(err, UniqueNamesError)
        elif err.entity.name == rec_auth.name:
            assert isinstance(err, AuthorizationError)
        elif err.entity.name == rec_par_prop.name:
            # record raises both of them
            assert (isinstance(err, UnqualifiedParentsError) or
                    isinstance(err, UnqualifiedPropertiesError))
