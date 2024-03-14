#!/usr/bin/env python

import sys

from cryan import CryanAtoms
from res import Res, ConcatRes, ResTar


# Main

filenames = sys.argv[1:]

structures = []
fmt='ase'

for filename in filenames:
    if filename.endswith('res.tar'):
        restar = ResTar.from_file(filename, fmt=fmt)
        structures += restar.structures
    elif filename.endswith('.res'):
        concatres = ConcatRes.from_file(filename, fmt=fmt)
        structures += concatres.structures
    else:
        print(f"Warning: {filename}")

cryan = CryanAtoms(structures)
print(cryan)
print(cryan.summary())
