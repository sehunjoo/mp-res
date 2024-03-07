#!/usr/bin/env python

import sys

from cryan import CryanAtoms
from restar import ResTar


# Main

restar = ResTar.read_as_atoms(sys.argv[1])

cryan = CryanAtoms(restar.structures)

print(cryan.to_str_per_atom())
cryan.calc_vol()
