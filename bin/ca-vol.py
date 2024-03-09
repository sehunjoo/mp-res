#!/usr/bin/env python

import sys

from cryan import CryanAtoms
from restar import ResTar
from concatres import ConcatRes



# Main

filename = sys.argv[1]

if filename.endswith('res.tar'):
    structures = ResTar.read_as_atoms(filename).structures
elif filename == 'data.res':
    structures = ConcatRes.read_as_atoms(filename).structures
else:
    pass

cryan = CryanAtoms(structures)

print(cryan.to_str_per_atom())
cryan.calc_vol()
