
Server Side Scripting
=====================

The administrator may store regularly needed scripts, e.g. for computing a
standardized analysis, on the same machine as the CaosDB server, "on the server
side", where they can be run directly by the server.

The execution of those scripts can be initiated using the Python client, or the
web interface.

Call a Script
~~~~~~~~~~~~~

If you have access to the server and sufficient permissions to run the script,
execution is fairly simple:

.. code:: python

    from caosdb.utils.server_side_scripting import run_server_side_script
    response = run_server_side_script('scriptname.py')
    print(response.stderr,response.stdout)


This makes the server run the script ``scriptname.py``. The output of the
script (``stderr`` and ``stdout``) is returned within an response object.


If the script requires additional arguments, those can be provided after the 
script's name.

Note that by default the script runs with your CaosDB account. It has your
permissions and changes are logged as if they were done by you directly.


Testing it
~~~~~~~~~~

You can try this out using for example the ``diagnostics.py`` script (it is part
of the `CaosDB server repository
<https://gitlab.indiscale.com/caosdb/src/caosdb-server/-/blob/main/scripting/bin/administration/diagnostics.py>`_
and is also available on https://demo.indiscale.com). The script returns
information about the server in JSON format. You can do for example the
following:

.. code:: python

    import json
    from caosdb.utils.server_side_scripting import run_server_side_script
    response = run_server_side_script('administration/diagnostics.py')
    print("JSON content:")
    print(json.loads(response.stdout))
    print("stderr:")
    print(response.stderr)


Further Information
~~~~~~~~~~~~~~~~~~~

Additionally, you might want to have a look at
https://docs.indiscale.com/caosdb-server/specification/Server-side-scripting.html
