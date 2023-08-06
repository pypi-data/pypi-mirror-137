# encoding: utf-8
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
# Copyright (C) 2020 IndiScale GmbH <info@indiscale.com>
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
import caosdb as db
from copy import deepcopy


def test_messages_dict_behavior():
    from caosdb.common.models import Message
    from caosdb.common.models import _Messages

    msgs = _Messages()

    # create Message
    msg = Message(
        type="HelloWorld",
        code=1,
        description="Greeting the world",
        body="Hello, world!")

    # append it to the _Messages
    assert repr(msg) == '<HelloWorld code="1" description="Greeting the world">Hello, world!</HelloWorld>\n'
    msgs.append(msg)
    assert len(msgs) == 1

    # use _Messages as list of Message objects
    for m in msgs:
        assert isinstance(m, Message)

    # remove it
    msgs.remove(msg)
    assert len(msgs) == 0

    # ok append it again ...
    msgs.append(msg)
    assert len(msgs) == 1
    # get it back via get(...) and the key tuple (type, code)
    assert id(msgs.get("HelloWorld", 1)) == id(msg)

    # delete Message via remove and the (type,code) tuple
    msgs.remove("HelloWorld", 1)
    assert msgs.get("HelloWorld", 1) is None
    assert len(msgs) == 0

    # short version of adding/setting/resetting a new Message
    msgs["HelloWorld", 2] = "Greeting the world in German", "Hallo, Welt!"
    assert len(msgs) == 1
    assert msgs["HelloWorld", 2] == (
        "Greeting the world in German", "Hallo, Welt!")

    msgs["HelloWorld", 2] = "Greeting the world in German", "Huhu, Welt!"
    assert len(msgs) == 1
    assert msgs["HelloWorld", 2] == (
        "Greeting the world in German", "Huhu, Welt!")
    del msgs["HelloWorld", 2]
    assert msgs.get("HelloWorld", 2) is None

    # this Message has no code and no description (make easy things easy...)
    msgs["HelloWorld"] = "Hello!"
    assert msgs["HelloWorld"] == "Hello!"


def test_deepcopy():
    """Test whether deepcopy of _Messages objects doesn't mess up
    contained Messages objects.

    """
    msgs = db.common.models._Messages()
    msg = db.Message(type="bla", code=1234, description="desc", body="blabla")
    msgs.append(msg)
    msg_copy = deepcopy(msgs)[0]

    # make sure type is string-like (formerly caused problems)
    assert hasattr(msg_copy.type, "lower")
    assert msg_copy.type == msg.type
    assert msg_copy.code == msg.code
    assert msg_copy.description == msg.description
    assert msg_copy.body == msg.body


def test_deepcopy_clear_server():

    msgs = db.common.models._Messages()
    msg = db.Message(type="bla", code=1234, description="desc", body="blabla")
    err_msg = db.Message(type="Error", code=1357, description="error")
    msgs.extend([msg, err_msg])
    copied_msgs = deepcopy(msgs)

    assert len(copied_msgs) == 2
    assert copied_msgs.get("Error", err_msg.code).code == err_msg.code
    assert copied_msgs.get("bla", msg.code).code == msg.code

    # Only the error should be removed
    copied_msgs.clear_server_messages()
    assert len(copied_msgs) == 1
    assert copied_msgs[0].code == msg.code
