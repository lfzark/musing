#
# Copyright (C) 2009-2019 the musing authors and contributors
#
# This example is part of python-sqlparse and is released under
# the BSD License: https://opensource.org/licenses/BSD-3-Clause
#
# Example for retrieving column definitions from a CREATE statement
# using low-level functions.

from musing import Musing
muse = Musing("/home/tmp/musing/examples/data/I_Want_It_That_Way.midi")
for instr  in muse.get_instruments():
        print instr
muse.play()