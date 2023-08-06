# Changelog #

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] ##

### Added ###

### Changed ###

### Deprecated ###

### Removed ###

### Fixed ###

### Security ###

## [0.7.0] - 2022-01-21 ##

### Added ###

- Function in administration that generates passwords that comply with the rules.

### Fixed ###

- #90 compare_entities function in apiutils does not check units

### Security ###

## [0.6.1] - 2021-12-03 ##

### Fixed ###

- #50 keyring can be used as password input method again
* #81 compare_entities from apiutils does not compare entity values

## [0.6.0] - 2021-10-19 ##

### Added ###

- It is possible now to supply a password for caosdb_admin on the command line
  and also activate the user directly using "-c".
* Added examples for complex data models to documentation
* extended apiutils with `resolve_reference(Property)`
* is_reference function for Properties
* function `retrieve_substructure` that recursively adds connected entities.

### Changed ###

* Retrievals of entities where the class does not match the entity role raise
  a ValueError now. See
  [here](https://gitlab.indiscale.com/caosdb/src/caosdb-pylib/-/issues/66) for more
  information. Updating a role is now being done by setting the `Entity.role`
  to the new role (as string).
* Entity.add_property and Entity.add_parent do not accept `**kwargs`-style
  keywords anymore. Formerly known keywords have been refactored into named
  parameters.
* [#35](https://gitlab.com/caosdb/caosdb-pylib/-/issues/35) Loggers now use the
  name of the unit where they are called instead of a static name

### Deprecated ###

* `id_query(ids)` in apiutils (to be removed with >=0.5.4)
* The whole yamlapi with the following functions (to be removed with >=0.5.4):
  * `append_sublist`
  * `kv_to_xml`
  * `dict_to_xml`
  * `yaml_to_xml`
  * `process`
  * `yaml_file_to_xml`
  * `insert_yaml_file`

### Removed ###

### Fixed ###

* #60 Unintuitive behavior of `Entity.role` after a `Entity(id).retrieve()`
  Originally the role was `None`. The correct role is present now.
* #53 Documentation of inheritance
* #38 Dependencies in chunk-deletion of containers

### Security ###

## [0.5.2] - 2021-06-03 ##

### Added ###

* Entity State support (experimental, no StateModel support yet). See the
  `caosdb.State` class for more information.
* `etag` property for the `caosdb.Query` class. The etag allows to debug the
  caching and to decide whether the server has changed between queries.
* function `_read_config_files` to read `pycaosdb.ini` files from different paths.

### Changed ###

* Updated error-handling tutorial in documentation to reflect the new
  error classes

### Deprecated ###

### Removed ###

### Fixed ###
* #45 - test_config_ini_via_envvar

### Security ###

## [0.5.1] - 2021-02-12 ##

### Fixed ###

* #43 - Error with `execute_query` when server doesn't support query caching.

## [0.5.0] - 2021-02-11 ##

### Added ###

* New exceptions `HTTPForbiddenException` and
  `HTTPResourceNotFoundException` for HTTP 403 and 404 errors,
  respectively.
* `BadQueryError`, `EmptyUniqueQueryError`, and `QueryNotUniqueError`
  for bad (unique) queries.
* Added `cache` paramter to `execute_query` and `Query.execute` which indicates
  whether server may use the cache for the query execution.
* Added `cached` property to the `Query` class which indicates whether the
  server used the cache for the execution of the last query.
* Documentation moved from wiki to this repository and enhanced.

### Changed ###

* Renaming of `URITooLongException` to `HTTPURITooLongError`.
* Raising of entity exceptions and transaction errors. Whenever any
  transaction fails, a `TransactionError` is raised. If one ore more
  entities caused that failure, corresponding entity errors are
  attached as direct and indirect children of the
  `TransactionError`. They can be accessed via the `get_errors`
  (direct children) and `get_all_errors` (direct and indirect
  children) methods; the causing entities are accessed by
  `get_entities` and `get_all_entities`. The `has_error` method can be
  used to check whether a `TransactionError` was caused by a specific
  `EntityError`.
* Unique queries will now result in `EmptyUniqueQueryError` or
  `QueryNotUniqueError` if no or more than one possible candidate is
  found, respectively.

### Removed ###

* Dynamic exception type `EntityMultiError`. 
* `get_something` functions from all error object in `exceptions.py`
* `AmbiguityException`

## [0.4.1] - 2021-02-10 ##

### Added ###

* Versioning support (experimental). The version db.Version class can
  represents particular entity versions and also the complete history of an
  entity.
* Automated documentation builds: `make doc`

### Fixed ###

* deepcopy of `_Messages` objects

## [0.4.0] - 2020-07-17##

### Added ###

* `[Entity|Container].get_property_values` for deeply nested references, e.g.
  from results of SELECT queries.
* two new `password_method`s for the `pycaosdb.ini` and the
  `configure_connection` function: `unauthenticated` for staying
  unauthenticated (and using the anonymous user) and `auth_token`. If
  `password_method == "auth_token"` the `auth_token` option is required as
  well.
* Empty string support (See caosdb-server#33)

### Changed ###

* `get_property` method also accepts instances of properties now, e.g.
  `record.get_property(Property(name="length"))`
* the value of properties is parsed to python types (int, float, boolean) when
  setting the value with the setter and when the datatype changes. Before this
  change, the value was parsed to python types only when parsing an xml and
  only for int and float.

### Deprecated ###

* Setting the `auth_token` option without setting the `password_method` to
  `auth_token`. This affects both the `pycaosdb.ini` and the
  `configure_connection` function. During the deprecation phase it will be
  assumed that `password_method` is `auth_token` if the the `auth_token` is
  set.

### Removed ###

### Fixed ###

- Replaced deprecated Logger.warn() method.

### Security ###

## [0.3.0] - 2020-04-24##

### Added ###

* `apiutils.apply_to_ids` -- a helper which applies a function to all ids which
  are used by an entity (own entity, parents, properties, references etc.).

### Changed ###

### Deprecated ###

### Fixed ###

* import bugs in apiutils

## [0.2.4] - 2020-04-23

### Added

- An `auth_token` parameter for `caosdb.configure_connection(...)`. This
  parameter accepts a plain text auth token (which can only be issued by the
  CaosDB Server). Under the hood, auth tokens are stored plain, instead of
  urlencoded now.
- New type of exception: `ConfigurationException` for misconfigurations.
- Some unit tests, mainly for the `caosdb.connection.authentication` module
- Advanced setup.py for easy versioning and publication as pypi repository.
- `caosdb.apiutils` has new functions `id_query` and
  `retrieve_entities_with_ids`
- New exception: `EntityDoesNotExistError`
- `RELEASE_GUIDELINES.md` with release instructions.
- More documentation and tests.

### Changed

- [pytest](https://docs.pytest.org/en/latest/) is the new preferred unit test
  frame work.
- If a password is specified in the configuration even though the
  password_method is not set to `plain`, a warning is logged.
- Under the hood, the password of from a `pass` or `keyring` call is not stored
  anymore. Instead the password is requested each time a login is necessary.
- Always load system default CA repository into the ssl context.
- Datatypes are now in `caosdb.common.datatype` (though still available in the
  main `caosdb` namespace).
- Logging to stdout is now more configurable.

### Deprecated

- Unit test frame work: [Nose](https://nose.readthedocs.io/en/latest/) should
  not be used anymore. Please use [pytest](https://docs.pytest.org/en/latest/)
  instead.

### Fixed

- #1 - Problems with pass as a credentials provider
- #3 - Python client does login before the first request to circumvent problems
  with anonymous role.
- Many other fixes


## [0.1.0] - 2018-10-09 ##

Tag `v0.1` - Commit 6fc0dcaa


### Added
- everything
