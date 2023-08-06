# -*- encoding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2021 Indiscale GmbH <info@indiscale.com>
# Copyright (C) 2021 Timm Fitschen <f.fitschen@indiscale.com>
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
from lxml import etree
import caosdb as db


def test_query_parsing():
    s = '<Query string="FIND bla" results="0" cached="true" etag="asdf"/>'
    q = db.Query(etree.fromstring(s))
    assert q.q == "FIND bla"
    assert q.results == 0
    assert q.cached is True
    assert q.etag == "asdf"

    s = '<Query string="COUNT bla" results="1" cached="false" etag="asdf"/>'
    q = db.Query(etree.fromstring(s))
    assert q.q == "COUNT bla"
    assert q.results == 1
    assert q.cached is False
    assert q.etag == "asdf"

    s = '<Query string="COUNT blub" results="4"/>'
    q = db.Query(etree.fromstring(s))
    assert q.q == "COUNT blub"
    assert q.results == 4
    assert q.cached is False
    assert q.etag is None
