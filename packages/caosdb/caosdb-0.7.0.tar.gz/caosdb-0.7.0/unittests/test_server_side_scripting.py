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

import json
from urllib.parse import parse_qs
from unittest.mock import Mock
from caosdb.utils import server_side_scripting as sss
from caosdb.connection.mockup import MockUpServerConnection, MockUpResponse
from caosdb import configure_connection

_REMOVE_FILES_AFTERWARDS = []


def setup_module():
    c = configure_connection(password_method="unauthenticated",
                             implementation=MockUpServerConnection)
    xml = ('<Response><script code="{code}">'
           ' <call>{call}</call>'
           ' <stdout>{stdout}</stdout>'
           ' <stderr>{stderr}</stderr>'
           '</script></Response>')

    def scripting_resource(**kwargs):
        assert kwargs["path"] == "scripting"
        content_type = kwargs["headers"]["Content-Type"]

        if content_type.startswith("multipart/form-data; boundary"):
            parts = kwargs["body"]
            stdout = []
            for part in parts:
                if hasattr(part, "decode"):
                    stdout.append(part.decode("utf-8"))
                else:
                    stdout.append(part)
            stdout = json.dumps(stdout)
        else:
            assert content_type == "application/x-www-form-urlencoded"
            stdout = json.dumps(parse_qs(kwargs["body"].decode("utf-8"),
                                         encoding="utf-8"))
        scripting_response = xml.format(code="123",
                                        call="call string",
                                        stdout=stdout,
                                        stderr="stderr string")
        return MockUpResponse(200, {}, scripting_response)
    c._delegate_connection.resources.append(scripting_resource)


def teardown_module():
    from os import remove
    from os.path import exists, isdir
    from shutil import rmtree
    for obsolete in _REMOVE_FILES_AFTERWARDS:
        if exists(obsolete):
            if isdir(obsolete):
                rmtree(obsolete)
            else:
                remove(obsolete)


def test_run_server_side_script():
    assert type(sss.run_server_side_script).__name__ == "function"
    r = sss.run_server_side_script("cat", "/etc/passwd", files=None,
                                   option1="val1")
    assert r.call == "call string"
    assert r.code == 123
    assert r.stderr == "stderr string"

    form = json.loads(r.stdout)
    assert form["call"] == ["cat"]
    assert form["-p0"] == ["/etc/passwd"]
    assert form["-Ooption1"] == ["val1"]


def test_run_server_side_script_with_file():
    _REMOVE_FILES_AFTERWARDS.append("test_file.txt")
    with open("test_file.txt", "w") as f:
        f.write("this is a test")

    assert type(sss.run_server_side_script).__name__ == "function"
    r = sss.run_server_side_script("cat", "/etc/passwd",
                                   files={"file1": "test_file.txt"},
                                   option1="val1")
    assert r.call == "call string"
    assert r.code == 123
    assert r.stderr == "stderr string"

    parts = json.loads(r.stdout)
    print(parts)
    assert 'name="call"' in parts[0]
    assert "\r\n\r\ncat\r\n" in parts[0]

    assert 'name="-Ooption1"' in parts[1]
    assert "\r\n\r\nval1\r\n" in parts[1]

    assert 'name="-p0"' in parts[2]
    assert "\r\n\r\n/etc/passwd\r\n" in parts[2]

    assert 'name="file1"' in parts[3]
    assert 'filename="test_file.txt"' in parts[3]

    assert parts[4] == "this is a test"
