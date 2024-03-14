from pymatgen.core.lattice import Lattice
from pymatgen.core.structure import Structure
import numpy as np

# construct a pymatgen Structure instance using the site fractional coordinates
coords = np.array( [ [ 0.0, 0.0, 0.0 ] ] )
atom_list = [ 'Li' ]
lattice = Lattice.from_parameters( a=1.0, b=1.0, c=1.0, alpha=90, beta=90, gamma=90 )
parent_structure = Structure( lattice, atom_list, coords ) * [ 4, 4, 1 ]
parent_structure.cart_coords.round(2)

from bsym.interface.pymatgen import unique_structure_substitutions

unique_structures = unique_structure_substitutions( parent_structure, 'Li', { 'Na':1, 'Li':15 } )
print(len( unique_structures ))
for st in unique_structures:
    print(st)
