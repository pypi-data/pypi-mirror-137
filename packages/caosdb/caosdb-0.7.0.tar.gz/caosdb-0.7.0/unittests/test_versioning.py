# -*- coding: utf-8 -*-
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

from __future__ import absolute_import
from caosdb import Record
from caosdb.common.utils import xml2str
from caosdb.common.versioning import Version
from .test_property import testrecord
from lxml import etree


def test_constructor():
    v = Version(id="1234abcd", date="2020-01-01T20:15:00.000UTC",
                username="testuser", realm="CaosDB", is_head=True,
                predecessors=[Version(id="2345abdc",
                                      date="2020-01-01T20:00:00.000UTC")],
                successors=[Version(id="3465abdc",
                                    date="2020-01-01T20:30:00.000UTC")])
    assert v.id == "1234abcd"
    assert v.date == "2020-01-01T20:15:00.000UTC"
    assert v.username == "testuser"
    assert v.realm == "CaosDB"
    assert v.is_head is True
    assert isinstance(v.predecessors, list)
    assert isinstance(v.predecessors[0], Version)
    assert isinstance(v.successors, list)
    assert isinstance(v.successors[0], Version)

    return v


def test_to_xml():
    v = test_constructor()
    xmlstr = xml2str(v.to_xml())
    assert xmlstr == ('<Version id="{i}" date="{d}" username="{u}" realm="{r}"'
                      ' head="{h}">\n'
                      '  <Predecessor id="{pi}" date="{pd}"/>\n'
                      '  <Successor id="{si}" date="{sd}"/>\n'
                      '</Version>\n').format(i=v.id, d=v.date,
                                             u=v.username, r=v.realm,
                                             h=str(v.is_head).lower(),
                                             pi=v.predecessors[0].id,
                                             pd=v.predecessors[0].date,
                                             si=v.successors[0].id,
                                             sd=v.successors[0].date)

    xmlstr2 = xml2str(v.to_xml(tag="OtherVersionTag"))
    assert xmlstr2 == ('<OtherVersionTag id="{i}" date="{d}" username="{u}" '
                       'realm="{r}" head="{h}">\n'
                       '  <Predecessor id="{pi}" date="{pd}"/>\n'
                       '  <Successor id="{si}" date="{sd}"/>\n'
                       '</OtherVersionTag>\n'
                       ).format(i=v.id, d=v.date, u=v.username, r=v.realm,
                                h=str(v.is_head).lower(),
                                pi=v.predecessors[0].id,
                                pd=v.predecessors[0].date,
                                si=v.successors[0].id, sd=v.successors[0].date)


def test_equality():
    v = test_constructor()
    assert hash(v) == hash(v)
    v2 = test_constructor()
    assert hash(v) == hash(v2)
    assert v == v2

    v = Version()
    v2 = Version()
    assert hash(v) == hash(v2)
    assert v == v2

    v = Version(id="123")
    v2 = Version(id="123")
    v3 = Version(id="2345")
    assert hash(v) == hash(v2)
    assert v == v2
    assert hash(v) != hash(v3)
    assert v != v3

    v = Version(id="123", date="2345", predecessors=None)
    v2 = Version(id="123", date="2345", predecessors=[])
    v3 = Version(id="123", date="Another date", predecessors=[])
    assert hash(v) == hash(v2)
    assert v == v2
    assert hash(v) != hash(v3)
    assert v != v3

    v = Version(id="123", date="2345", predecessors=[Version(id="bla")])
    v2 = Version(id="123", date="2345", predecessors=[Version(id="bla")])
    v3 = Version(id="123", date="2345", predecessors=[Version(id="blub")])
    v4 = Version(id="123", date="2345", predecessors=[Version(id="bla"),
                                                      Version(id="bla")])
    assert hash(v) == hash(v2)
    assert v == v2
    assert hash(v) != hash(v3)
    assert v != v3
    assert hash(v) != hash(v4)
    assert v != v4

    v = Version(id="123", date="2345", predecessors=[Version(id="bla")],
                successors=[Version(id="234")])
    v2 = Version(id="123", date="2345", predecessors=[Version(id="bla")],
                 successors=[Version(id="234")])
    v3 = Version(id="123", date="2345", predecessors=[Version(id="bla")],
                 successors=[Version(id="bluup")])
    assert hash(v) == hash(v2)
    assert v == v2
    assert hash(v) != hash(v3)
    assert v != v3


def test_from_xml():
    v = test_constructor()
    xml = v.to_xml()

    v2 = Version.from_xml(xml)

    assert hash(v) == hash(v2)
    assert v == v2
    assert str(v) == str(v2)


def test_version_deserialization():
    assert testrecord.version == Version(id="version-str",
                                         date="2019-04-02T12:22:34.837UTC")


def test_version_serialization():
    r = Record()
    r.version = Version(id="test-version", date="asdfsadf")

    # <Record><Version id="test-version" date="asdfsadf"/></Record>
    assert "test-version" == r.to_xml().xpath("/Record/Version/@id")[0]
    assert "asdfsadf" == r.to_xml().xpath("/Record/Version/@date")[0]


def test_get_history():
    xml_str = """
    <Version id="vid6" username="user1" realm="Realm1" date="date6" completeHistory="true">
      <Predecessor id="vid5" username="user1" realm="Realm1" date="date5">
        <Predecessor id="vid4" username="user1" realm="Realm1" date="date4">
          <Predecessor id="vid3" username="user1" realm="Realm1" date="date3">
            <Predecessor id="vid2" username="user1" realm="Realm1" date="date2">
              <Predecessor id="vid1" username="user1" realm="Realm1" date="date1" />
            </Predecessor>
          </Predecessor>
        </Predecessor>
      </Predecessor>
      <Successor id="vid7" username="user1" realm="Realm1" date="date7">
        <Successor id="vid8" username="user1" realm="Realm1" date="date8">
          <Successor id="vid9" username="user1" realm="Realm1" date="date9">
            <Successor id="vid10" username="user1" realm="Realm1" date="date10" />
          </Successor>
        </Successor>
      </Successor>
    </Version>"""
    version = Version.from_xml(etree.fromstring(xml_str))
    assert version.is_complete_history is True
    assert version.get_history() == [Version(id=f"vid{i+1}", date=f"date{i+1}",
                                             username="user1", realm="Realm1")
                                     for i in range(10)]
