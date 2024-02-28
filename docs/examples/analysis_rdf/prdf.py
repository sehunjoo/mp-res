import os
import glob
import numpy as np
import argparse
from ase.io import read
from ase.build import make_supercell
from ase.ga.utilities import get_rdf
from concurrent.futures import ProcessPoolExecutor

def parse_args():
    """
    Parse arguments
    """

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="",
        epilog="examples:\n"
               "    prdf.py -mpinp 10\n"
    )

    parser.add_argument('-rcut', '--rcut', type=int, dest='rcut',
                        default=7,
                        help='Cutoff radius')
    parser.add_argument('-nbins', '--nbins', type=int, dest='nbins',
                        default=140,
                        help='Number of ions, range up to')
    parser.add_argument('-mpinp', '--mpinp', type=int, dest='mpinp',
                        default=4,
                        help='Number of cores')
    parser.add_argument('-workdir', '--workdir', type=str, dest='workdir',
                        default='.',
                        help='Directory where res files exist')
    args = parser.parse_args()

    for attr in dir(args):
        if not attr.startswith('_'):
            print(f"{attr:<20}: {getattr(args, attr)}")
    print()

    return args


def calculate_rdf(resfile, rcut=7, nbins=140):
    '''
    Calculate radial distribution function (RDF) using ASE
    ase.ga.utilities.get_rdf
    '''
    print(resfile)

    atoms = read(resfile, format='res')

    cell = atoms.get_cell()
    vol = atoms.get_volume()
    h = [vol / np.linalg.norm(np.cross(cell[(i + 1) % 3], cell[(i + 2) % 3])) for i in range(3)]
    supercell_nn = [max(1, int(np.ceil(rcut / (hi / 2)))) for hi in h]
    supercell_matrix = np.diag(supercell_nn)
    supercell = make_supercell(atoms, supercell_matrix)

    rdf, r = get_rdf(
        atoms=supercell,
        rmax=rcut,
        nbins=nbins,
        distance_matrix=None,
        elements=None,
        no_dists=False
    )

    if not os.path.exists('rdf_f.txt'):
        with open('rdf_r.txt', 'w') as f:
            np.savetxt(f, r[np.newaxis], fmt="%f")

    with open('rdf_rdfs.txt', 'ab') as f:
            np.savetxt(f, rdf[np.newaxis], fmt="%f")

    return rdf, r


if __name__ == "__main__":

    args = parse_args()

    rcut = args.rcut
    nbins = args.nbins
    mpinp = args.mpinp
    workdir = args.workdir

    # Load .res files
    res_files = glob.glob(workdir + '/*.res')

    if os.path.exists('rdf_r.txt'):
        os.remove('rdf_r.txt')
    if os.path.exists('rdf_rdfs.txt'):
        os.remove('rdf_rdfs.txt')

    # Calculate RDFs in parallel and gather results
    os.nice(19)
    with ProcessPoolExecutor(max_workers=mpinp) as executor:
        #results = list(executor.map(calculate_rdf, res_files))
        results = list(executor.map(lambda resfile: calculate_rdf(resfile, rcut=rcut, nbins=nbins), res_files))

