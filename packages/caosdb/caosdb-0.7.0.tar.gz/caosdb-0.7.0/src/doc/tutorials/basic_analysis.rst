
Basic Analysis
==============

If you have not yet, configure a connection with the demo instance. E.g.:

>>> import caosdb as db
>>> _ = db.configure_connection(
...    url="https://demo.indiscale.com/", 
...    password_method="plain", 
...    username="admin", 
...    password="caosdb")

A basic Analysis of data in CaosDB could start like:

>>> 
>>> analyses =  db.execute_query("FIND RECORD Analysis with quality_factor")
>>> qfs = [el.get_property("quality_factor").value for el in analyses]

This first retrieves all analysis records that have a ``quality_factor`` and 
then creates a Python list that contains the values. You could create a 
histogram of those for example by (**warning** this is a very boring histogram)::

    import matplotlib
    import matplotlib.pyplot as plt
    plt.hist(qfs)
    plt.xlabel("quality factors")
    plt.ylabel("count")
    plt.show()



Often we are interested in table like data for our processing. And the disentangling of the property values as above is a bit annoying. Thus there is a convenience function for that.

>>> from caosadvancedtools.table_converter import to_table
>>> # Let us retrieve the data in a table like form using `SELECT`
>>> data = db.execute_query("SELECT quality_factor FROM RECORD Analysis with quality_factor" )
>>> table = to_table(data)
>>> print(table)
  quality_factor
0           ...

Summary
-------

Now you know, how you can collect query results in lists or tables that can then 
be used for further processing.
