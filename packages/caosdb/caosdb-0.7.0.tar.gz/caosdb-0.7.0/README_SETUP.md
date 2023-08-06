# Getting started with PyCaosDB #

## Installation ##

### Requirements ###

PyCaosDB needs at least Python 3.6.  Additionally, the following packages are required (they will
typically be installed automatically):

- `lxml`
- `PyYaml`
- `PySocks`

Optional packages:
- `keyring`
- `jsonschema`

### How to install ###

#### Linux ####

Make sure that Python (at least version 3.6) and pip is installed, using your system tools and
documentation.

Then open a terminal and continue in the [Generic installation](#generic-installation) section.

#### Windows ####

If a Python distribution is not yet installed, we recommend Anaconda Python, which you can download
for free from [https://www.anaconda.com](https://www.anaconda.com).  The "Anaconda Individual Edition" provides most of all
packages you will ever need out of the box.  If you prefer, you may also install the leaner
"Miniconda" installer, which allows you to install packages as you need them.

After installation, open an Anaconda prompt from the Windows menu and continue in the [Generic
installation](#generic-installation) section.

#### MacOS ####

If there is no Python 3 installed yet, there are two main ways to
obtain it: Either get the binary package from
[python.org](https://www.python.org/downloads/) or, for advanced
users, install via [Homebrew](https://brew.sh/). After installation
from python.org, it is recommended to also update the TLS certificates
for Python (this requires administrator rights for your user):

```sh
# Replace this with your Python version number:
cd /Applications/Python\ 3.9/

# This needs administrator rights:
sudo ./Install\ Certificates.command
```

After these steps, you may continue with the [Generic
installation](#generic-installation).

#### Generic installation ####

To install PyCaosDB locally, use `pip3` (also called `pip` on some systems):

```sh
pip3 install --user caosdb
```

---

Alternatively, obtain the sources from GitLab and install from there (`git` must be installed for
this option):

```sh
git clone https://gitlab.com/caosdb/caosdb-pylib
cd caosdb-pylib
pip3 install --user .
```

For installation of optional packages, install with an additional option, e.g. for 
validating with the caosdb json schema:

```sh
pip3 install --user .[jsonschema]
```

## Configuration ##

The  configuration is done using `ini` configuration files.
PyCaosDB tries to read from the inifile specified in the environment variable `PYCAOSDBINI` or
alternatively in `~/.pycaosdb.ini` upon import.  After that, the ini file `pycaosdb.ini` in the
current working directory will be read additionally, if it exists.

Here, we will look at the most common configuration options. For a full and 
comprehensive description please check out 
[pycaosdb.ini file](https://gitlab.com/caosdb/caosdb-pylib/-/blob/main/examples/pycaosdb.ini) 
You can download this file and use it as a starting point.


Typically, you need to change at least the `url` and `username` fields as required. 
(Ask your CaosDB administrator or IT crowd if
you do not know what to put there, but for the demo instances https://demo.indiscale.com, `username=admin`
and `password=caosdb` should work).

### Authentication ###

The default configuration (that your are asked for your password when ever a connection is created
can be changed by setting `password_method`:

* with `password_method=input` password (and possibly user) will be queried on demand (**default**)
* use the password manager [pass](https://www.passwordstore.org) by using `pass` as value, see also the [ArchWiki
  entry](https://wiki.archlinux.org/index.php/Pass#Basic_usage). This also requires `password_identifier` which refers to the identifier within pass
  for the desired password.
* install the python package [keyring](https://pypi.org/project/keyring), to use the system keyring/wallet (macOS, GNOME, KDE,
  Windows). The password will be queried on first usage.
* with `password_method=plain` (**strongly discouraged**)

The following illustrates the recommended options:

```ini
[Connection]
# using "pass" password manager
#password_method=pass
#password_identifier=...

# using the system keyring/wallet (macOS, GNOME, KDE, Windows)
#password_method=keyring
```

### SSL Certificate ###
In some cases (especially if you are testing CaosDB) you might need to supply 
an SSL certificate to allow SSL encryption.

```ini
[Connection]
cacert=/path/to/caosdb.ca.pem
```

### Further Settings ###
As mentioned above, a complete list of options can be found in the 
[pycaosdb.ini file](https://gitlab.com/caosdb/caosdb-pylib/-/blob/main/examples/pycaosdb.ini) in 
the examples folder of the source code.

## Try it out ##

Start Python and check whether the you can access the database. (You will be asked for the
password):

```python
In [1]: import caosdb as db
In [2]: db.Info()
Please enter the password:  # It's `caosdb` for the demo server.
Out[2]: Connection to CaosDB with 501 Records.
```

Note: This setup will ask you for your password whenever a new connection is created. If you do not
like this, check out the "Authentication" section in the [configuration documentation](configuration.md).

Now would be a good time to continue with the [tutorials](tutorials/index).

## Run Unit Tests
tox

## Documentation ##

Build documentation in `build/` with `make doc`.

### Requirements ###

- `sphinx`
- `sphinx-autoapi`
- `recommonmark`

### Troubleshooting ###
If the client is to be executed directly from the `/src` folder, an initial `.\setup.py install --user` must be called.
