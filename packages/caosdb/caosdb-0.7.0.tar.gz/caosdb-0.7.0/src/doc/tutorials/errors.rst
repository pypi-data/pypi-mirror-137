
Error Handling
==============

In case of erroneous transactions, connection problems and a lot of
other cases, PyCaosDB may raise specific errors in order to pinpoint
the problem as precisely as possible. Some of these errors a
representations of errors in the CaosDB server, others stem from
problems that occurred on the client side.

The errors and exceptions are ordered hierarchically form the most
general exceptions to specific transaction or connection problems. The
most important error types and the hierarchy will be explained in the
following. For more information on specific error types, see also the
:doc:`source code<../_apidoc/caosdb.exceptions>`.

.. note::

   Starting from PyCaosDB 0.5, the error handling has changed
   significantly. New error classes have been introduced and the
   behavior of ``TransactionError`` and ``EntityError`` has been
   re-worked. In the following, only the "new" errors are
   discussed. Please refer to the documentation of PyCaosDB 0.4.1 and
   earlier for the old error handling.

CaosDBException
----------------

``CaosDBException`` is the most generic exception and all other error classes inherit
from this one. Because of its generality, it doesn't tell you much
except that some component of PyCaosDB raised an exception. If you
want to catch all possible CaosDB errors, this is the class to use.

TransactionError
----------------

Every transaction (calling ``insert``, ``update``, ``retrieve``, or
``delete`` on a container or an entity) may finish with errors. They
indicate, for instance, that an entity does not exist or that you need
to specify a data type for your property and much more. If and only if
one or more errors occur during a transaction a ``TransactionError``
will be raised by the transaction method. The ``TransactionError``
class is a container for all errors which occur during a
transaction. It usually contains one or more :ref:`entity
errors<EntityError>` which you can inspect in order to learn why the
transaction failed. For this inspection, there are some helpful
attributes and methods provided by the ``TransactionError``:

* ``entities``: a list of all entities that directly caused at least one error
  in this transaction.

* ``errors``: a list of all ``EntityError`` objects that directly caused the
  transaction to fail.

* ``all_entities``, ``all_errors``: sets of all entities and errors
  that, directly or indirectly, caused either this ``TransactionError`` or any of the
  ``EntityError`` objects it contains.

* ``has_error(error_t)``: Check whether an error of type ``error_t``
  occurred during the transaction.

Additionally, ``print(transaction_error)`` prints a tree-like
representation of all errors regarding the transaction in question.

EntityError
-----------

An ``EntityError`` specifies the entity and the error proper that
caused a transaction to fail. It is never raised on its own but is
contained in a ``TransactionError`` (which may or may not contain
other ``EntityError`` objects) which is then raised. ``EntityError``
has several :ref:`subclasses<Special Errors>` that further specify the
error that occurred.

The ``EntityError`` class is in fact a subclass of
``TransactionError``. Thus, it has the same methods and attributes as
the ``TransactionError`` explained
:ref:`above<TransactionError>`. This is important in case of an
``EntityError`` that was caused by other faulty entities (e.g., broken
parents or properties). In that case these problematic entities and
errors can again be inspected by visiting the ``entities`` and
``errors`` lists as above.

Special Errors
~~~~~~~~~~~~~~

Subclasses of ``EntityError`` for special purposes:

* ``EntityDoesNotExistError``

* ``EntityHasNoDataTypeError``

* ``UniqueNamesError``

* ``UnqualifiedParentsError``

* ``UnqualifiedPropertiesError``

* ``ConsistencyError``

* ``AuthorizationError``

* ``AmbiguousEntityError``

BadQueryError
-------------

A ``BadQueryError`` is raised when a query could not be processed by
the server. In contrast to a ``TransactionError`` it is not
necessarily caused by problematic entities or
containers. ``BadQueryError`` has the two important subclasses
``EmptyUniqueQueryError`` and ``QueryNotUniqueError`` for queries with
``unique=True`` which found no or ambiguous entities, respectively.

HTTP Errors
-----------

An ``HTTPClientError`` or an ``HTTPServerError`` is raised in case of
http(s) connection problems caused by the Python client or the CaosDB
server, respectively. There are the following subclasses of
``HTTPClientError`` that are used to specify the connection problem:

* ``HTTPURITooLongError``: The URI of the request was too long to be
  processed by the server.

* ``HTTPForbiddenError``: You're not allowed to access this resource.

* ``HTTPResourceNotFoundError``: The requested resource doesn't exist.

Other Errors
------------

There are further subclasses of ``CaosDBException`` that are raised in
case of faulty configurations or other problems. They should be rather
self-explanatory from their names; see the :doc:`source code<../_apidoc/caosdb.exceptions>`
for further information.

* ``ConfigurationError``

* ``LoginFailedError``

* ``MismatchingEntitiesError``

* ``ServerConfigurationException``

Examples
--------

.. code-block:: python3

   import caosdb as db

   def link_and_insert(entity, linked, link=True):
     """Link the ENTITY to LINKED and insert it."""
     if link:
       entity.add_property(db.Property(name="link", value=linked))
     try:
       entity.insert()
     except db.TransactionError as tre:
       # Unique names problem may be worked around by using another name
       if tre.has_error(db.UniqueNamesError):
         for ent_error in tre.errors:
           if (isinstance(ent_error, db.UniqueNamesError)
               and entity in ent_error.entities):
             entity.name = entity.name + "_new"  # Try again with new name.
             link_and_insert(entity, linked, link=False)
             break
       # Unqualified properties will be handled by the caller
       elif tre.has_error(db.UnqualifiedPropertiesError):
         for ent_error in tre.errors:
           if (isinstance(ent_error, db.UnqualifiedPropertiesError_
               and entity in ent_error.entities):
             raise RuntimeError("One of the properties was unqualified: " + str(ent_error))
       # Other problems are not covered by this tutorial
       else:
         raise NotImplementedError("Unhandled TransactionError: " + str(tre))
