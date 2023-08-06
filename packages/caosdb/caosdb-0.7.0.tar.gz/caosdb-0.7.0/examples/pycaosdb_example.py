#!/usr/bin/env python3
"""A small example to get started with caosdb-pylib.

Make sure that a `pycaosdb.ini` is readable at one of the expected locations.
"""

import random

import caosdb as db


def reconfigure_connection():
    """Change the current connection configuration."""
    conf = db.configuration.get_config()
    conf.set("Connection", "url", "https://demo.indiscale.com")
    db.configure_connection()


def main():
    """Shows a few examples how to use the CaosDB library."""
    conf = dict(db.configuration.get_config().items("Connection"))
    print("##### Config:\n{}\n".format(conf))

    if conf["cacert"] == "/path/to/caosdb.ca.pem":
        print("Very likely, the path the the TLS certificate is not correct, "
              "please fix it.")

    # Query the server, the result is a Container
    result = db.Query("FIND Record").execute()
    print("##### First query result:\n{}\n".format(result[0]))

    # Retrieve a random Record
    rec_id = random.choice([rec.id for rec in result])
    rec = db.Record(id=rec_id).retrieve()
    print("##### Randomly retrieved Record:\n{}\n".format(rec))


if __name__ == "__main__":
    main()
