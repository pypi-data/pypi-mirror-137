#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ** end header
#
"""server_side_script.py.

An example which implements a minimal server-side script.

1) This script expects to find a *.txt file in the .upload_files dir which is
printed to stdout.

2) It executes a "Count stars" query and prints the result to stdout.

3) It will return with code 0 if everything is ok, or with any code that is
specified with the commandline option --exit
"""

import sys
from os import listdir
from caosdb import configure_connection, execute_query


# parse --auth-token option and configure connection
CODE = 0
QUERY = "COUNT stars"
for arg in sys.argv:
    if arg.startswith("--auth-token="):
        auth_token = arg[13:]
        configure_connection(auth_token=auth_token)
    if arg.startswith("--exit="):
        CODE = int(arg[7:])
    if arg.startswith("--query="):
        QUERY = arg[8:]


############################################################
# 1 # find and print *.txt file ############################
############################################################

try:
    for fname in listdir(".upload_files"):
        if fname.endswith(".txt"):
            with open(".upload_files/{}".format(fname)) as f:
                print(f.read())
except FileNotFoundError:
    pass


############################################################
# 2 # query "COUNT stars" ##################################
############################################################

RESULT = execute_query(QUERY)
print(RESULT)

############################################################
# 3 ########################################################
############################################################

sys.exit(CODE)
