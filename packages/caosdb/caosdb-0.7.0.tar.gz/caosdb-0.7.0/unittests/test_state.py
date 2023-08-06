import pytest
import caosdb as db
from caosdb import State, Transition
from caosdb.common.models import parse_xml, ACL
from lxml import etree


def test_state_xml():
    state = State(model="model1", name="state1")
    xml = etree.tostring(state.to_xml())

    assert xml == b'<State name="state1" model="model1"/>'
    state = State.from_xml(etree.fromstring(xml))
    assert state.name == "state1"
    assert state.model == "model1"

    assert xml == etree.tostring(state.to_xml())


def test_entity_xml():
    r = db.Record()
    assert r.state is None
    r.state = State(model="model1", name="state1")

    xml = etree.tostring(r.to_xml())
    assert xml == b'<Record><State name="state1" model="model1"/></Record>'

    r = parse_xml(xml)
    assert r.state == State(model="model1", name="state1")


def test_description():
    xml = b'<State name="state1" model="model1"/>'
    state = State.from_xml(etree.fromstring(xml))
    assert state.description is None

    with pytest.raises(AttributeError):
        state.description = "test"

    xml = b'<State name="state1" model="model1" description="test2"/>'
    state = State.from_xml(etree.fromstring(xml))
    assert state.description == "test2"


def test_id():
    xml = b'<State name="state1" model="model1"/>'
    state = State.from_xml(etree.fromstring(xml))
    assert state.id is None

    with pytest.raises(AttributeError):
        state.id = "2345"

    xml = b'<State name="state1" model="model1" id="1234"/>'
    state = State.from_xml(etree.fromstring(xml))
    assert state.id == "1234"


def test_create_state_acl():
    acl = ACL()
    acl.grant(role="role1", permission="DO:IT")
    acl.grant(role="?OWNER?", permission="DO:THAT")
    state_acl = State.create_state_acl(acl)
    assert state_acl.get_permissions_for_role("?STATE?role1?") == {"DO:IT"}
    assert state_acl.get_permissions_for_role("?STATE??OWNER??") == {"DO:THAT"}


def test_transitions():
    xml = b'<State name="state1" model="model1"/>'
    state = State.from_xml(etree.fromstring(xml))
    assert state.transitions is None

    with pytest.raises(AttributeError):
        state.transitions = []

    xml = b'<State name="state1" model="model1" id="1234"><Transition name="t1"><FromState name="state1"/><ToState name="state2"/></Transition></State>'
    state = State.from_xml(etree.fromstring(xml))
    assert state.transitions == set([Transition(name="t1", from_state="state1", to_state="state2")])
