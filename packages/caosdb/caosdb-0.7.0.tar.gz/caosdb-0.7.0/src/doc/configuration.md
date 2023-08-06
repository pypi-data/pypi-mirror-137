# Configuration of PyCaosDB #
The behavior of PyCaosDB is defined via a configuration that is provided using configuration files.
PyCaosDB tries to read from the inifile specified in the environment variable `PYCAOSDBINI` or
alternatively in `~/.pycaosdb.ini` upon import.  After that, the ini file `pycaosdb.ini` in the
current working directory will be read additionally, if it exists.

## Authentication ##

The default configuration (that your are asked for your password when ever a connection is created
can be changed by setting `password_method`:

* with `password_method=input` password (and possibly user) will be queried on demand (**default**)
* use the password manager [pass](https://www.passwordstore.org) by using `pass` as value, see also the [ArchWiki
  entry](https://wiki.archlinux.org/index.php/Pass#Basic_usage). This also requires `password_identifier` which refers to the identifier within pass
  for the desired password.
* install the python package [keyring](https://pypi.org/project/keyring), to use the system keyring/wallet (macOS, GNOME, KDE,
  Windows). The password will be queried on first usage.
* with `password_method=plain` (**strongly discouraged**)

```ini
[Connection]
username=YOUR_USERNAME

# password using "pass" password manager
#password_method=pass
#password_identifier=...

# using the system keyring/wallet (macOS, GNOME, KDE, Windows)
#password_method=keyring

#discouraged: password in plain text
#password_method=plain
#password=YOUR_PASSWORD
```

## SSL Certificate ##

You can set the pass to the ssl certificate to be used:

```ini
[Connection]
cacert=/path/to/caosdb.ca.pem
```

## Further Settings ##

`debug=0` ensures that debug information is **not** printed to the terminal every time you interact
with CaosDB which makes the experience much less verbose. Set it to 1 or 2 in case you want to help
debugging (which I hope will not be necessary for this tutorial) or if you want to learn more about
the internals of the protocol. 

A complete list of options can be found in the 
[pycaosdb.ini file](https://gitlab.com/caosdb/caosdb-pylib/-/blob/main/examples/pycaosdb.ini) in 
the examples folder of the source code.
