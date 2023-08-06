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
"""Tests for the Entity class."""
# pylint: disable=missing-docstring
import unittest
from lxml import etree

from caosdb import (INTEGER, Entity, Property, Record, RecordType,
                    configure_connection)
from caosdb.connection.mockup import MockUpServerConnection


class TestEntity(unittest.TestCase):

    def setUp(self):
        self.assertIsNotNone(Entity)
        configure_connection(url="unittests", username="testuser",
                             password_method="plain",
                             password="testpassword", timeout=200,
                             implementation=MockUpServerConnection)

    def test_instance_variables(self):
        entity = Entity()
        self.assertTrue(hasattr(entity, "role"))
        self.assertIsNone(entity.role)
        self.assertTrue(hasattr(entity, "id"))
        self.assertTrue(hasattr(entity, "name"))
        self.assertTrue(hasattr(entity, "description"))
        self.assertTrue(hasattr(entity, "parents"))
        self.assertTrue(hasattr(entity, "properties"))

    def test_entity_role_1(self):
        entity = Entity(role="TestRole")
        self.assertEqual(entity.role, "TestRole")
        entity.role = "TestRole2"
        self.assertEqual(entity.role, "TestRole2")

    def test_entity_role_2(self):
        entity = Entity()

        self.assertIsNone(entity.role)
        self.assertEqual(entity.to_xml().tag, "Entity")

        entity.role = "Record"
        self.assertEqual(entity.role, "Record")
        self.assertEqual(entity.to_xml().tag, "Record")

    def test_recordtype_role(self):
        entity = RecordType()

        self.assertEqual(entity.role, "RecordType")
        self.assertEqual(entity.to_xml().tag, "RecordType")

    def test_property_role(self):
        entity = Property()

        self.assertEqual(entity.role, "Property")
        self.assertEqual(entity.to_xml().tag, "Property")

    def test_instantiation(self):
        self.assertRaises(Exception, Entity())

    def test_parse_role(self):
        """During parsing, the role of an entity is set explicitely. All other
        classes use the class name as a "natural" value for the role property.
        """
        parser = etree.XMLParser(remove_comments=True)
        entity = Entity._from_xml(Entity(),
                                  etree.parse("unittests/test_record.xml",
                                              parser).getroot())

        self.assertEqual(entity.role, "Record")
        # test whether the __role property of this object has explicitely been
        # set.
        self.assertEqual(getattr(entity, "_Entity__role"), "Record")
