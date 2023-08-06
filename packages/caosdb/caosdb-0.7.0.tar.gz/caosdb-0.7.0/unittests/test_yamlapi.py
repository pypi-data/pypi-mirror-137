# -*- coding: utf-8 -*-
#
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2021 IndiScale GmbH <info@indiscale.com>
# Copyright (C) 2021 Alexander Kreft <akreft@trineo.org>
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

import os
import warnings
import tempfile
from caosdb.yamlapi import (append_sublist, kv_to_xml,
                            dict_to_xml, yaml_to_xml,
                            process, yaml_file_to_xml)

with warnings.catch_warnings(record=True) as w:
    # Cause all warnings to always be triggered.
    warnings.simplefilter("always")

    append_sublist(None, None, None)

    assert issubclass(w[-1].category, DeprecationWarning)
    assert "This function is deprecated" in str(w[-1].message)

with warnings.catch_warnings(record=True) as w:
    # Cause all warnings to always be triggered.
    warnings.simplefilter("always")

    kv_to_xml("None", "None")
    assert len(w) == 1
    assert issubclass(w[-1].category, DeprecationWarning)
    assert "This function is deprecated" in str(w[-1].message)

with warnings.catch_warnings(record=True) as w:
    # Cause all warnings to always be triggered.
    warnings.simplefilter("always")

    dict_to_xml(None)

    assert issubclass(w[-1].category, DeprecationWarning)
    assert "This function is deprecated" in str(w[-1].message)

with warnings.catch_warnings(record=True) as w:
    # Cause all warnings to always be triggered.
    warnings.simplefilter("always")

    yaml_to_xml("None")

    assert issubclass(w[-1].category, DeprecationWarning)
    assert "This function is deprecated" in str(w[-1].message)

with warnings.catch_warnings(record=True) as w:
    # Cause all warnings to always be triggered.
    warnings.simplefilter("always")

    process("None")

    assert issubclass(w[-1].category, DeprecationWarning)
    assert "This function is deprecated" in str(w[-1].message)

with warnings.catch_warnings(record=True) as w:
    # Cause all warnings to always be triggered.
    warnings.simplefilter("always")

    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpfile = os.path.join(tmpdirname, 'yamlfile')
        with open(tmpfile, 'w') as tf:
            tf.write("")
        yaml_file_to_xml(tmpfile)

    assert issubclass(w[-1].category, DeprecationWarning)
    assert "This function is deprecated" in str(w[-1].message)
