First Steps
===========

You should have a working connection to a CaosDB instance now. If not, please check out the 
:doc:`Getting Started secton</README_SETUP>`.

If you are not yet familiar with Records, RecordTypes and Properties used in CaosDB,
please check out the respective part in the `Web Interface tutorial`_.
You should also know the basics of the CaosDB Query Language (a tutorial is
`here <https://docs.indiscale.com/caosdb-webui/tutorials/query.html>`_).

We recommend that you connect to the `demo instance`_ (hosted by `Indiscale`_) in order to try out
the following examples. You can do this with

>>> import caosdb as db
>>> _ = db.configure_connection(
...    url="https://demo.indiscale.com/", 
...    password_method="plain", 
...    username="admin", 
...    password="caosdb")

or by using corresponding settings in the configuration file
(see :doc:`Getting Started secton</README_SETUP>`.).
However, you can also translate the examples to the data model that you have at hand.

Let's start with a simple query.

>>> response = db.execute_query("FIND RECORD Guitar")

Queries work the same way as in the web interface. You simply provide the 
query string to the corresponding function (``db.execute_query``). However, the result is not 
displayed as beautifully as in the web interface (Try ``print(response)``). That is why browsing through 
data is the strength of the web interface while the automated processing of 
data is the strength of the Python client.

>>> type(response)
<class 'caosdb.common.models.Container'>

As you can see the type of the returned object is Container. Containers are 
simply lists of LinkAhead objects with useful functions to interact with LinkAhead. 
Thus we can easily find out how many Records where returned:

>>> len(response)
3

Let's look at the first element:

>>> firstguitar = response[0]
>>> print(type(firstguitar))
<class 'caosdb.common.models.Record'>
>>> print(firstguitar)
<Record ...

.. The above example needs doctest ELLIPSIS
You see that the object is a Record. It has a Parent and two Properties.

.. note::

    Many useful functions and classes are directly available top level in the module::

        db.Container()
        db.Record()

Accessing Properties
--------------------

Often it is necessary to access the value of a property.

>>> # get the property object
>>> print(firstguitar.get_property("price"))
<Property id="100" name="price" datatype="DOUBLE" unit="€">48.0</Property>
<BLANKLINE>
>>> # the value of it
>>> print(firstguitar.get_property("price").value)
48.0
>>> # What is this?
>>> print(firstguitar.get_property(100))
<Property id="100" name="price" datatype="DOUBLE" unit="€">48.0</Property>
<BLANKLINE>


Why did the second version work? In the web interface we do not realize it that easily, but there is only one thing that uniquely identifies Entities in LinkAhead: the id.

In the xml output you see, that the properties have the ids 100 and 106. Often names of entities are also unique, but this is not guaranteed. Thus in many cases it is preferable or even necessary to use the id for identifying LinkAhead Entities.

Ids can also come in handy when searching. Suppose you have some complicated condition for the object that you want


>>> # This condition is not that complicated and long but let's suppose it was.
>>> record = db.execute_query("FIND Analysis with quality_factor=0.08", unique=True)
>>> # You can use unique=True when you only expect one result Entity. An error will be
>>> # thrown if the number of results is unequal to 1 and the resulting object will be
>>> # an Entity and not a Container
>>> print(type(record))
<class 'caosdb.common.models.Record'>
>>> print(record.id)
123

Now we can continue using the id of the first query. This for example allows to formulate a second query with a condition involving this object without including the potentially long and complicated subquery in this one:

>>> query = "FIND Guitar WHICH IS REFERENCED BY {id}".format(id=record.id)
>>> guitar = db.execute_query(query, unique=True)
>>> print(guitar)
<Record id="115" ...

Files
-----

You can download files (if the LinkAhead server has access to them)

>>> file = db.execute_query("FIND FILE *2019-023" , unique=True)
>>> target_path = el = file.download()

The file will be saved under target_path.
If the files are large data files, it is often a better idea to only retrieve the path of the file and access them via a local mount.



Summary
-------

Now you know, how you can use Python to send queries to CaosDB and you can access
the result Records and their properties. 

The next tutorial shows how to make some meaningful use of this.


.. _`demo instance`: https://demo.indiscale.com
.. _`IndiScale`: https://indiscale.com
.. _`Web Interface tutorial`: https://docs.indiscale.com/caosdb-webui/tutorials/first_steps.html
