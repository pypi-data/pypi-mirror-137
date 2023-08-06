
# -*- encoding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
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
"""Tests for the Container class."""
from __future__ import absolute_import

import caosdb as db


def test_get_property_values():
    rt_house = db.RecordType("House")
    rt_window = db.RecordType("Window")
    rt_owner = db.RecordType("Owner")
    p_height = db.Property("Height", datatype=db.DOUBLE)

    window = db.Record().add_parent(rt_window)
    window.id = 1001
    window.add_property(p_height, 20.5, unit="m")

    owner = db.Record("The Queen").add_parent(rt_owner)

    house = db.Record("Buckingham Palace")
    house.add_parent(rt_house)
    house.add_property(rt_owner, owner)
    house.add_property(rt_window, window)
    house.add_property(p_height, 40.2, unit="ft")

    container = db.Container()
    container.extend([
        house,
        owner
    ])

    assert getattr(house.get_property(p_height), "unit") == "ft"
    assert getattr(window.get_property(p_height), "unit") == "m"

    table = container.get_property_values("naME",
                                          "height",
                                          ("height", "unit"),
                                          "window",
                                          ("window", "non-existing"),
                                          ("window", "non-existing", "unit"),
                                          ("window", "unit"),
                                          ("window", "heiGHT"),
                                          ("window", "heiGHT", "value"),
                                          ("window", "heiGHT", "unit"),
                                          "owner",
                                          )
    assert len(table) == 2
    house_row = table[0]
    assert house_row == (house.name, 40.2, "ft", window.id, None, None, None, 20.5, 20.5, "m", owner.name)

    owner_row = table[1]
    assert owner_row == (owner.name, None, None, None, None, None, None, None, None, None, None)

    assert container.get_property_values("non-existing") == [(None,), (None,)]
    assert container.get_property_values("name") == [(house.name,),
                                                     (owner.name,)]


def test_container_dependencies_for_deletion():
    not_included_rt = 1000
    rt = db.RecordType("Just a RecordType")
    rt.id = 1001
    rt_record_with_parent = db.RecordType("Records with parent")
    rt_record_with_parent.id = 1005
    property_which_is_not_a_record = db.Property(
        "Normal Property", datatype=db.DOUBLE, value=1006)
    property_which_is_not_a_record.id = 1006
    property_which_shall_be_deleted = db.Property(
        "Normal Property 2", datatype=db.DOUBLE, value=1006)
    property_which_shall_be_deleted .id = 1007

    record_without_dependencies = db.Record().add_parent(not_included_rt)
    record_without_dependencies.id = 2003

    record_referenced = db.Record().add_parent(not_included_rt)
    record_referenced.id = 2002
    record_with_dependencies = db.Record().add_parent(not_included_rt)
    record_with_dependencies.id = 2004
    record_with_dependencies.add_property(not_included_rt,
                                          record_referenced,
                                          datatype="not_included_rt")

    record_with_parent = db.Record().add_parent(rt_record_with_parent)
    record_with_parent.id = 2005

    record_with_property_which_is_not_a_record = db.Record(
    ).add_parent(not_included_rt)
    record_with_property_which_is_not_a_record.id = 2006
    record_with_property_which_is_not_a_record.add_property(
        property_which_is_not_a_record)
    record_with_property_which_is_not_a_record.add_property(
        property_which_shall_be_deleted)

    container = db.Container()
    container.extend([
        rt,
        rt_record_with_parent,  # 1005, dependency
        record_without_dependencies,
        property_which_shall_be_deleted,  # 1007, dependency
        record_referenced,  # 2002, dependency
        record_with_dependencies,
        record_with_parent,
        record_with_property_which_is_not_a_record
    ])
    assert (db.Container()._test_dependencies_in_container(container)
            == {2002, 1005, 1007})


def test_container_dependencies_for_deletion_with_lists():
    not_included_rt = 1000

    record_referenced = db.Record().add_parent(not_included_rt)
    record_referenced.id = 2001

    record_with_list = db.Record().add_parent(not_included_rt)
    record_with_list.id = 2002
    record_with_list.add_property(not_included_rt, datatype=db.LIST(
        not_included_rt), value=[record_referenced, 2003, 2004, 2005, 2006])

    container = db.Container()
    container.extend([record_with_list, record_referenced])

    assert db.Container()._test_dependencies_in_container(container) == {2001}
