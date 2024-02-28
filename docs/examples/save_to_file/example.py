#!/usr/bin/env python

from mp_api.client import MPRester
from pymatgen.io.res import ResIO
import os

api_key = "d7BCat3ve9lYksDLTojHg3AceBOcN5B9"
mpr = MPRester(api_key)



def mp_entry_to_res(entry):
    '''
    Writing a res files with an uncorrected energy
    '''
    print(entry)
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

    # write a resfile

    ResIO.entry_to_file(entry, f"{seed}.res")
    print(entry)


def ex1():

    print("\nExample 1\n")

    entries = mpr.get_entries(
        chemsys_formula_mpids=["mp-841"]
    )

    for i, entry in enumerate(entries):
        print(f"\nEntry {i}\n")
        print(entry)
        mp_entry_to_res(entry)






def main():
    ex1()

main()
