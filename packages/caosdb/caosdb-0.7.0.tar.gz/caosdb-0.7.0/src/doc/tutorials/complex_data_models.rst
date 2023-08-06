Complex Data Models
-------------------

With CaosDB it is possible to create very complex data models.

E.g. it is possible to add properties to properties to cover complex relations
in data management workflows.

One example for a use case is meta data that is added to very specific properties of
datasets, e.g. data privacy information can be added to properties which themselves
could already be considered meta data of a dataset.

The example below tries to cover some complex cases for data models:

Examples
--------

.. code-block:: python3

   import caosdb as db

   # Create two record types with descriptions:
   rt1 = db.RecordType(name="TypeA", description="The first type")
   rt2 = db.RecordType(name="TypeB", description="The second type")

   # Create a record using the first record type as parent:
   r1 = db.Record(name="Test_R_1", description="A record")
   r1.add_parent(rt1)

   # Create two files (the files named test.txt and testfile2.txt should exist in the
   # current working directory:
   f1 = db.File(name="Test file", path="/test.txt", file="test.txt")
   f2 = db.File(name="Test file 2", path="/testfile2.txt", file="testfile2.txt")

   # Create two properties with different data types:
   p1 = db.Property(name="TestFileProperty", datatype=db.FILE)
   p2 = db.Property(name="TestDoubleProperty", datatype=db.DOUBLE, unit="m")
   p3 = db.Property(name="TestIntegerProperty", datatype=db.INTEGER, unit="s")

   # Create a reference property that points to records of record type 2:
   p4 = db.Property(name="TestReferenceProperty", datatype=rt2)

   # Create a complex record:
   r2 = db.Record(name="Test_R_2", description="A second record")
   r2.add_parent(rt2)
   r2.add_property(rt1, value=r1)  # this is a reference to the first record type
   r2.add_property(p1, value=f1)  # this is a reference to the first file
   r2.add_property(p2, value=24.8)  # this is a double property with a value
   r2.add_property(p3, value=1)  # this is an integer property with a value

   # Very complex part of the data model:
   # Case 1: File added to another file
   f2.add_property(p1, value=f1)  # this adds a file property with value first file
		                  # to the second file

   # Case 2: Property added to a property
   p2.add_property(p3, value=27)  # this adds an integer property with value 27 to the
		                  # double property

   # Case 3: Reference property added to a property
   # The property p2 now has two sub properties, one is pointing to
   # record p2 which itself has the property p2, therefore this can be
   # considered a loop in the data model.
   p2.add_property(p4, value=r2)  # this adds a reference property pointing to
		                  # record 2 to the double property

   # Insert a container containing all the newly created entities:
   c = db.Container().extend([rt1, rt2, r1, r2, f1, p1, p2, p3, f2, p4])
   c.insert()

   # Useful for testing: wait until the user presses a key
   # Meanwhile have a look at the WebUI: You can e.g. query "FIND Test*" to view
   # all the entities created here and see the relations and links between them.
   b = input("Press any key to cleanup.")
   # cleanup everything after the user presses any button.
   c.delete()
