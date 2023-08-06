Data Insertion
==============

Data Models
~~~~~~~~~~~

Data is stored and structured in CaosDB using a concept of RecordTypes, Properties, Records etc. If
you do not know what these are, please look at the chapter :doc:`Data
Model<caosdb-server:Data-Model>` in the CaosDB server documentation.

In order to insert some actual data, we need to create a data model
using RecordTypes and Properties (You may skip this if you use a CaosDB
instance that already has the required types). When you create a new Property 
you must supply a datatype. So, let’s create a simple
Property called “a” of datatype double. This is very easy in pylib:

.. code:: python

   a = db.Property(name="a", datatype=db.DOUBLE)

There are a few basic datatypes like db.INTEGER, db.DOUBLE, or db.TEXT. See the
`data types
<https://docs.indiscale.com/caosdb-server/specification/Datatype.html>`_ for a
full list.

We can create our own small data model for e.g. a simulation by adding
two more Properties and a RecordType:

.. code:: python

   b = db.Property(name="b", datatype=db.DOUBLE)
   epsilon = db.Property(name="epsilon", datatype=db.DOUBLE)
   recordtype = db.RecordType(name="BarkleySimulation")
   recordtype.add_property(a)
   recordtype.add_property(b)
   recordtype.add_property(epsilon)
   container = db.Container()
   container.extend([a, b, epsilon, recordtype])
   container.insert()

.. _tutorial-inheritance-properties:

Inheritance of Properties
-------------------------

Suppose you want to create a new RecordType “2D_BarkleySimulation”
that denotes spatially extended Barkley simulations. This is a subtype
of the “BarkleySimulation” RecordType above and should have all its
parameters, i.e., properties. It may be assigned more, e.g., spatial
resolution, but we'll omit this for the sake of brevity for now.

.. code:: python

   rt = db.RecordType(name="2D_BarkleySimulation",
                  description="Spatially extended Barkley simulation")
   # inherit all properties from the BarkleySimulation RecordType
   rt.add_parent(name="BarkleySimulation", inheritance="all")
   rt.insert()

   print(rt.get_property(name="epsilon").importance) ### rt has a "epsilon" property with the same importance as "BarkleySimulation"

The parameter ``inheritance=(obligatory|recommended|fix|all|none)`` of
:py:meth:`Entity.add_parent()<caosdb.common.models.Entity.add_parent>` tells the server to assign
all properties of the parent RecordType with the chosen importance (and properties with a higher
importance) to the child RecordType
automatically upon insertion. See the chapter on `importance
<https://docs.indiscale.com/caosdb-server/specification/RecordType.html#importance>`_ in the
documentation of the CaosDB server for more information on the importance and inheritance of
properties.

.. note::

   The inherited properties will only be visible after the insertion since they are set by the
   CaosDB server, not by the Python client.


Insert Actual Data
~~~~~~~~~~~~~~~~~~

Suppose the RecordType “Experiment” and the Property “date” exist in the
database. You can then create single data Records by using the
corresponding python class:

.. code:: python

   rec = db.Record()
   rec.add_parent(name="Experiment")
   rec.add_property(name="date", value="2020-01-07")
   rec.insert()

Here, the record has a parent: The RecordType “Experiment”. And a
Property: date.

Note, that if you want to use a property that is not a primitive
datatype like db.INTEGER and so on, you need to use the ID of the Entity
that you are referencing.

.. code:: python

   rec = db.Record()
   rec.add_parent(name="Experiment")
   rec.add_property(name="report", value=235507)
   rec.add_property(name="Analysis", value=230007)
   rec.insert()

Of course, the IDs 235507 and 230007 need to exist in CaosDB. The first
example shows how to use a db.REFERENCE Property (report) and the second
shows that you can use any RecordType as Property to reference a Record
that has such a parent.

Most Records do not have name however it can absolutely make sense. In
that case use the name argument when creating it. Another useful feature
is the fact that properties can have units:

.. code:: python

   rec = db.Record("DeviceNo-AB110")
   rec.add_parent(name="SlicingMachine")
   rec.add_property(name="weight", value="1749", unit="kg")
   rec.insert()

If you are in some kind of analysis you can do this in batch mode with a
container. E.g. if you have a python list ``analysis_results``:

.. code:: python

   cont = db.Container()
   for date, result in analysis_results:
      rec = db.Record()
      rec.add_parent(name="Experiment")
      rec.add_property(name="date", value=date)
      rec.add_property(name="result", value=result)
      cont.append(rec)

   cont.insert()

Useful is also, that you can insert directly tabular data.

.. code:: python

   from caosadvancedtools.table_converter import from_tsv

   recs = from_tsv("test.csv", "Experiment")
   print(recs)
   recs.insert()

With this example file
`test.csv <uploads/4f2c8756a26a3984c0af09d206d583e5/test.csv>`__.

List Properties
---------------

As you may already know, properties can also have list values instead of scalar
values. They can be accessed, set, and updated as you would expect from any
list-valued attribute in Python, as the following example illustrates.

.. code:: python

   import caosdb as db
   db.Property(name="TestList", datatype=db.LIST(db.DOUBLE)).insert()
   db.RecordType(name="TestType").add_property(name="TestList").insert()
   db.Record(name="TestRec").add_parent("TestType").add_property(
       name="TestList", value=[1,2,3]).insert()
   retrieved = db.Record(name="TestRec").retrieve()
   retrieved.get_property("TestList").value += [4,5]
   retrieved.update()

   # Check update
   retrieved = db.Record(name="TestRec").retrieve()
   print(retrieved.get_property("TestList").value)


File Update
-----------

Updating an existing file by uploading a new version.

1. Retrieve the file record of interest, e.g. by ID:

.. code:: python

   import caosdb as db

   file_upd = db.File(id=174).retrieve()

2. Set the new local file path. The remote file path is stored in the
   file object as ``file_upd.path`` while the local path can be found in
   ``file_upd.file``.

.. code:: python

   file_upd.file = "./supplements.pdf"

3. Update the file:

.. code:: python

   file_upd.update()
