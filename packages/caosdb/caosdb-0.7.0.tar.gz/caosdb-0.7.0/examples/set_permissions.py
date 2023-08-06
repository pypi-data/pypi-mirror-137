#!/usr/bin/env python3

# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (c) 2019 IndiScale GmbH
# Copyright (c) 2019 Daniel Hornung <d.hornung@indiscale.com>
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

"""Creates role and user, then sets the permissions of an entity.

As a result, only a specific user or group may access it.

This script assumes that the user specified in the pycaosdb.ini
configuration can create new entities.

"""

import caosdb as db
from caosdb import administration as admin


def assert_user_and_role():
    """Make sure that users and roles exist.

After calling this function, there will be a user "jane" with the role "human"
and the user "xaxys" with the role "alien".  These users and roles are returned.

Returns
-------
out : tuple
  ((human_user, human_role), (alien_user, alien_role))

    """
    try:
        human_user = admin._retrieve_user("jane")
        admin._update_user(name="jane", status="ACTIVE")
    except db.HTTPResourceNotFoundError:
        human_user = admin._insert_user(
            "jane", password="Human_Rememberable_Password_1234", status="ACTIVE")

    try:
        alien_user = admin._retrieve_user("xaxys")
        admin._update_user(name="xaxys", status="ACTIVE")
    except db.HTTPResourceNotFoundError:
        alien_user = admin._insert_user("xaxys", password="4321_Syxax",
                                        status="ACTIVE")

    # At the moment, the return value is only "ok" for successful insertions.
    try:
        human_role = admin._retrieve_role("human")
    except db.HTTPResourceNotFoundError:
        human_role = admin._insert_role("human", "An Earthling.")

    try:
        alien_role = admin._retrieve_role("alien")
    except db.HTTPResourceNotFoundError:
        alien_role = admin._insert_role("alien", "An Extra-terrestrial.")

    admin._set_roles("jane", ["human"])
    admin._set_roles("xaxys", ["alien"])

    return (("jane", list(admin._get_roles("jane"))),
            ("xaxys", list(admin._get_roles("xaxys"))))


def get_entities(count=1):
    """Retrieve one or more entities.

Parameters
----------
count : int, optional
    How many entities to retrieve.

Returns
-------
out : Container
    A container of retrieved entities, the length is given by the parameter count.
    """
    cont = db.execute_query("FIND RECORD 'Human Food'", flags={
                            "P": "0L{n}".format(n=count)})
    if len(cont) != count:
        raise db.CaosDBException(
            msg="Incorrect number of entitities returned.")
    return cont


def set_permission(role_grant, role_deny, cont=None, general=False):
    """Set the permissions of some entities.

Parameters
----------
role_grant : str
    Role which is granted permissions.

role_deny : str
    Role which is denied permissions.

cont : Container
    Entities for which permissions are set.

general : bool, optional
    If True, the permissions for the roles will be set.  If False (the default),
    permissions for the entities in the container will be set.
    """

    # Set general permissions
    if general:
        grant = admin.PermissionRule(
            action="grant", permission="RETRIEVE:OWNER")
        deny = admin.PermissionRule(action="deny", permission="RETRIEVE:FILE")

        admin._set_permissions(role=role_grant, permission_rules=[grant])
        admin._set_permissions(role=role_deny, permission_rules=[deny])
        return

    if cont is None or len(cont) == 0:
        raise ValueError("Container not given or empty!")

    perm = "RETRIEVE:*"
    for ent in cont:
        ent.retrieve_acl()
        ent.acl.grant(role=role_grant, permission=perm)
        ent.acl.deny(role=role_deny, permission=perm)
    cont.update()
    print("Permissions updated.")


def test_permission(granted_user, denied_user, cont):
    """Tests if the permissions are set correctly for two users.

Parameters
----------
granted_user : (str, str)
    The user which should have permissions to retrieve the entities in `cont`.
    Given as (user, password).

denied_user : (str, str)
    The user which should have no permission to retrieve the entities in `cont`.
    Given as (user, password).

cont :  Container
    Entities for which permissions are tested.


Returns
-------
None

    """

    # Switch to user with permissions
    db.configure_connection(username=granted_user[0], password=granted_user[1],
                            password_method="plain")
    db.connection.connection.get_connection()._login()
    print("Trying to retrieve entities as {}...".format(granted_user[0]))
    try:
        for ent in cont:
            ent.retrieve()
        print("Successfully retrieved all entities.")
    except db.TransactionError as te:
        if te.has_error(db.AuthorizationError):
            print(ent)
            print("Could not retrieve this entity although it should have been possible!")
        else:
            raise te

    # Switch to user without permissions
    db.configure_connection(username=denied_user[0], password=denied_user[1],
                            password_method="plain")
    db.connection.connection.get_connection()._login()
    print("\nTrying to retrieve entities as {}...".format(denied_user[0]))

    denied_all = True
    for ent in cont:
        try:
            ent.retrieve()
            denied_all = False
            print(ent)
            print("Could retrieve this entity although it should not have been possible!")
        except db.TransactionError as te:
            # Only do something if an error wasn't caused by an
            # AuthorizationError
            if not te.has_error(db.AuthorizationError):
                raise te
    if denied_all:
        print("Retrieval of all entities was successfully denied.")


def create_test_entities():
    """Create some test entities.
    After calling this function, there will be a RecordType "Human Food" with the corresponding Records
    "Bread", "Tomatoes", and "Twinkies" inserted in the database.
    """
    rt = db.RecordType(
        name="Human Food", description="Food that can be eaten only by humans").insert()
    food = ("Bread", "Tomatoes", "Twinkies")

    cont = db.Container()
    for i in range(len(food)):
        rec = db.Record(food[i])
        rec.add_parent(name="Human Food")
        cont.append(rec)

    cont.insert()


def main():
    """The main function of this script."""

    """Create some test entities"""
    create_test_entities()
    """Create new users"""
    human, alien = assert_user_and_role()
    """Load the newly created entities."""
    entities = get_entities(count=3)
    """Set permission for the entities (only humans are allowed to eat human food)"""
    set_permission(human[1][0], alien[1][0], entities)
    """Test the permissions"""
    test_permission((human[0], "Human_Rememberable_Password_1234"),
                    (alien[0], "4321_Syxax"), entities)


if __name__ == "__main__":
    main()
