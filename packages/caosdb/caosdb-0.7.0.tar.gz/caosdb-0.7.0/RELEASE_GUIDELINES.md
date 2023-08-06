# Release Guidelines for the CaosDB Python Client Library

This document specifies release guidelines in addition to the general release
guidelines of the CaosDB Project
([RELEASE_GUIDELINES.md](https://gitlab.com/caosdb/caosdb/blob/dev/RELEASE_GUIDELINES.md))

## General Prerequisites

* All tests are passing.
* FEATURES.md is up-to-date and a public API is being declared in that document.
* CHANGELOG.md is up-to-date.
* DEPENDENCIES.md is up-to-date.

## Steps

1. Create a release branch from the dev branch. This prevents further changes
   to the code base and a never ending release process. Naming: `release-<VERSION>`

2. Update CHANGELOG.md

3. Check all general prerequisites.

4. Prepare [setup.py](./setup.py): Check the `MAJOR`, `MINOR`, `MICRO`, `PRE`
   variables and set `ISRELEASED` to `True`. Use the possibility to issue
   pre-release versions for testing.

5. Merge the release branch into the main branch.

6. Tag the latest commit of the main branch with `v<VERSION>`.

7. Delete the release branch.

8. Remove possibly existing `./dist` directory with old release.

9. Publish the release by executing `./release.sh` with uploads the caosdb
   module to the Python Package Index [pypi.org](https://pypi.org).

10. Merge the main branch back into the dev branch.

11. After the merge of main to dev, start a new development version by
    setting `ISRELEASED` to `False` and by increasing at least the `MICRO`
    version in [setup.py](./setup.py) and preparing CHANGELOG.md.
