#!/usr/bin/env python

from mp_api.client import MPRester
from pymatgen.io.res import ResIO

api_key = "d7BCat3ve9lYksDLTojHg3AceBOcN5B9"
mpr = MPRester(api_key)

def main():

    chemsys_formula_mpids = "Li-Ni-O"

    entries = mpr.get_entries(chemsys_formula_mpids)
    #entries = [entries[0]]

    # Check the type of entries

    #print(type(entries))

    print("number of documents :", len(entries))

    '''
    # Check the type of entry
    for entry in entries:
        print(type(entry))
    '''

    '''
    # Check what information each entry has
    for entry in entries:
        print("-"*100)
        print(entry)
        print("-"*100)
    '''
    
    '''
    # Check what information each entry has
    for entry in entries:
        print("-"*100)
        print("entry_id                              :", entry.entry_id)
        print("composition                           :", entry.composition)
        print("elements                              :", entry.elements)
        print("energy (eV)                           :", entry.energy)
        print("energy_per_atom (eV/atom)             :", entry.energy_per_atom)
        print("correction (eV)                       :", entry.correction)
        print("correction_per_atom (eV/atom)         :", entry.correction_per_atom)
        print("uncorrected_energy (eV)               :", entry.uncorrected_energy)
        print("uncorrected_energy_per_atom (eV/atom) :", entry.uncorrected_energy_per_atom)
        print("parameters                            :", entry.parameters)
        print("data                                  :", entry.data)
        print("-"*100)
    '''

    '''
    # Check what information each entry has
    for entry in entries:
        print("-"*100)
        print("composition                 :", type(entry.composition))
        print("elements:                   :", type(entry.elements))
        print("energy                      :", type(entry.energy))
        print("energy_per_atom             :", type(entry.energy_per_atom))
        print("correction                  :", type(entry.correction))
        print("correction_per_atom         :", type(entry.correction_per_atom))
        print("uncorrected_energy          :", type(entry.uncorrected_energy))
        print("uncorrected_energy_per_atom :", type(entry.uncorrected_energy_per_atom))
        print("parameters                  :", type(entry.parameters))
        print("data                        :", type(entry.data))
        print("entry_id                    :", type(entry.entry_id))
        print("-"*100)
    '''

    '''
    # Save to a resfile without REM lines
    for entry in entries:
        material_id = entry.data.get("material_id", "mp-")
        task_id = entry.data.get("task_id", "mp-")
        run_type = entry.data.get("run_type", "")

        seed = f"{material_id}-{run_type}-{task_id}"

        entry.data.setdefault("seed", seed)

        ResIO.entry_to_file(entry, f"{seed}.res")

    '''

    # Save to a resfile with REM lines
    for entry in entries:

        material_id = entry.data.get("material_id", "mp-")
        task_id = entry.data.get("task_id", "mp-")
        run_type = entry.data.get("run_type", "")

        seed = f"{material_id}-{run_type}-{task_id}"
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

        entry.data.setdefault("seed", seed)
        entry.data.setdefault("rems", rems)

        print(seed)
        ResIO.entry_to_file(entry, f"{seed}.res")

main()
