#!/usr/bin/env python

import os
import argparse
import itertools
import tarfile
from mp_api.client import MPRester
from pymatgen.io.res import ResIO

api_key = "d7BCat3ve9lYksDLTojHg3AceBOcN5B9"
mpr = MPRester(api_key)

#==============================================================================
# arguments
#==============================================================================


def get_args():
    """
    Parse arguments
    """

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Retrieve structures from Materials Project database",
        epilog="examples:\n"
               "    mp_query.py -el Li,Ni,O\n"
               "    mp_query.py -el Li,Ni,O -in 20\n"
    )
    parser.add_argument('-el', '--elementlist', type=str, dest='elements',
                        default=None,
                        help='Comma separated list of elements')
    parser.add_argument('-m', '--mode', type=str, dest='mode',
                        default='and',
                        help='Nmode')
    parser.add_argument('-eah', '--energy_above_hull', type=float, dest='eah',
                        default=None,
                        help='Energy above hull (meV/atom)')
    parser.add_argument('-nsites', '--nsites', type=int, dest='nsites',
                        default=None,
                        help='Maximum number of ions/atoms/sites')
    args = parser.parse_args()


    # banner

    banner = [
        f"",
        f"     {os.path.basename(__file__)}",
        f"",
        f"       Author: Se Hun Joo (shj29@cam.ac.uk)",
        f"",
        f"       Summary of arguments",
        f""
    ]

    banner += [
        f"         {attr:<20}: {getattr(args, attr)}"
        for attr in dir(args)
        if not attr.startswith('_')
    ]

    print("\n".join(banner) + "\n")

    return args


#==============================================================================
# query
#==============================================================================


def get_chemsys_from_elements(
    elements: list[str],
    mode: str = "only-or",
    nelements: int = 0
) -> list[str]:

    """
    Generates a list of chemical systems from provided elements according
    to the specified mode. The chemical systems are combinations of element
    symbols, sorted alphabetically and joined by "-".

    Args:
        elements (List[str]): List of chemical element symbols
                              (e.g., ["Li", "Ni", "O"]).
        mode (str): Mode for generating chemical systems. Options include
                    "and" for a single system containing all elements,
                    "or" for all possible combinations of elements, and
                    "atleast" for systems containing at least the specified
                    elements. "atleast" mode requires an external API call
                    and is not implemented in this function.
        nelements (int): Specifies the number of elements in the generated
                         systems. A value of 0 indicates all possible
                         combinations. For binary systems, set to 2.
                         This parameter is ignored in "and" mode.

    Returns:
        List[str]: List of chemical systems, each a string of element symbols
                   joined by "-", sorted alphabetically within each system.
    """

    chemsys = []

    if mode == "and":
        chemsys.append("-".join(sorted(elements)))

    elif mode == "or":
        nrange = range(1, len(elements) + 1) if nelements == 0 else [nelements]
        for n in nrange:
            for combo in itertools.combinations(elements, n):
                chemsys.append("-".join(sorted(combo)))

    elif mode == 'atleast':
        docs = mpr.materials.summary.search(
            elements=elements,
            fields=["chemsys"]
        )
        chemsys.extend({doc.chemsys for doc in docs})

        raise ValueError(f"Unsupported mode: {mode}")

    return chemsys


#==============================================================================
# download
#==============================================================================


def get_mp_entry(
    chemsys: str | list[str],
    eah: float | None = None,
    nsites: float | None = None,
):
    """
    Download entries from the Materials Poject database
    Referece
    https://github.com/materialsproject/api/blob/main/mp_api/client/mprester.py
    https://github.com/materialsproject/api/blob/main/mp_api/client/routes/materials/thermo.py

    Args:
        chemsys (str | list[str]): Chemical systems

    Returns:
        list[ComputedStructureEntry]
    """
    property_data = None
    additional_criteria = None

    if eah:
        if eah >= 0:
            additional_criteria = {"energy_above_hull": (0.0, eah/1000)}
        else:
            raise ValueError(f"energy_above_hull should be positive")
    if nsites:
        property_data = ["nsites"]

    entries = mpr.get_entries(
        chemsys_formula_mpids=chemsys,
        compatible_only=True,
        property_data=property_data,
        conventional_unit_cell=False,
        additional_criteria=additional_criteria
    )

    if nsites:
        entries = [entry for entry in entries if entry.data.get('nsites', -1) < nsites]

    return entries


#==============================================================================
# io
#==============================================================================


def mp_entry_to_res_entry(entry):
    '''
    Writing a res files with an uncorrected energy
    '''
    # make energy correction zero
    entry.correction = 0

    material_id = entry.data.get("material_id", "")
    task_id = entry.data.get("task_id", "")
    run_type = entry.data.get("run_type", "")

    # TITL: add seed to entry.data

    seed = f"{material_id}-{run_type}"
    entry.data.update({"seed": seed})

    # TITL: add pressure to entry.data

    entry.data.update({"pressure": 0})

    # TITL: add isd/iasd to entry.data - spin density

    isd = 0
    iasd = 0
    for site in entry.structure:
        if 'magmom' in site.properties:
             isd += site.properties['magmom']
             iasd += abs(site.properties['magmom'])

    entry.data.update({"isd": isd})
    entry.data.update({"iasd": iasd})

    # REM: add rems to entry.data - metadata

    rems = [
            f"",
            f'Downloaded from the Materials Project database',
            f"",
            f"Energy (Uncorrected)     = {entry.uncorrected_energy:<16.8f} eV",
            f"Correction               = {entry.correction:<16.8f} eV",
            f"Energy (Final)           = {entry.energy:<16.8f} eV",
            f"",
            f"material_id              = {material_id}",
            f"run_type                 = {run_type}",
            f"task_id                  = {task_id}",
            f""
    ]

    entry.data.update({"rems": rems})

    return entry


def entries_to_restar(entries, tarname):
    filelist = []
    with tarfile.open(tarname, 'a') as tar:
        for entry in entries:

            filename= entry.data.get("seed", "") + ".res"

            if filename in filelist:
                #print(f"skip: {filename} already exist")
                continue

            ResIO.entry_to_file(entry, filename)
            tar.add(filename, arcname=filename)
            os.remove(filename)
            filelist.append(filename)


#############################
# Main
#############################


def main():

    # Get arguments

    args = get_args()

    # Check arguments

    if args.elements == None:
        print("A list of elements should be provided")
        exit()
    else:
        elements = args.elements.split(",")
        elements.sort()

    mode = args.mode
    eah = args.eah
    nsites = args.nsites


    # Generate query

    chemsys = get_chemsys_from_elements(
        elements=elements,
        mode=mode
    )
    print("chemsys:\n", chemsys)

    # Download data from the Materials Project database

    entries = get_mp_entry(
        chemsys=chemsys,
        eah=eah,
        nsites=nsites
    )

    # Write res files
    entries = [mp_entry_to_res_entry(entry) for entry in entries]

    tarname = '-'.join(elements)
    if eah:
        if eah >= 0:
            tarname += f"_eah{int(eah)}"
    if nsites:
        tarname += f"_nsites{nsites}"
    tarname += '.res.tar'

    entries_to_restar(entries, tarname)


main()
