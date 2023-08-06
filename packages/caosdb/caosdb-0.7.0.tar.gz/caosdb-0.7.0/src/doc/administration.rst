Administration
==============

The Python script ``caosdb_admin.py`` should be used for administrative tasks.
Call ``caosdb_admin.py --help`` to see how to use it.

The most common task is to create a new user (in the CaosDB realm) and set a 
password for the user (note that a user typically needs to be activated)::

     caosdb_admin.py create_user anna
     caosdb_admin.py set_user_password anna
     caosdb_admin.py add_user_roles anna administration
     caosdb_admin.py activate_user anna

