#!/usr/bin/env python

from mp_api.client import MPRester
from pymatgen.io.res import ResIO
import os

api_key = "d7BCat3ve9lYksDLTojHg3AceBOcN5B9"
mpr = MPRester(api_key)

def ex():

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


def analyze_entries(entries):

    fields = ["material_id", "task_id", "run_type", "chemsys", "nelements", "thermo_type"]

    data_unique = {field: set() for field in fields}
    data_nunique = {field: 0 for field in fields}

    str_entries = " ".join([
        f"{'material_id':12s}",
        f"{'task_id':12s}",
        f"{'run_type':9s}",
        f"{'thermo_type':17s}",
        f"{'chemsys':12s}",
        f"{'uncorrected_energy':>19s}",
        f"{'correction':>11s}",
        f"{'corrected_energy':>19s}",
    ]) + "\n"

    for entry in entries:
        str_entry = " ".join([
            f"{entry.data.get('material_id','NaN'):12s}",
            f"{entry.data.get('task_id', 'NaN'):12s}",
            f"{entry.data.get('run_type', 'NaN'):9s}",
            f"{entry.data.get('thermo_type', 'NaN'):17s}",
            f"{entry.data.get('chemsys', 'NaN'):12s}",
            f"{entry.uncorrected_energy:19f}",
            f"{entry.correction:11f}",
            f"{entry.energy:19f}"
        ])
        str_entries += str_entry + "\n"

        for key in data_unique:
            data_unique[key].add(entry.data.get(key))


    str_unique = ""
    str_nunique = f"{'ComputedStructureEntry':25s} = {len(entries)}\n"

    for field in fields:

        if field == 'thermo_type':
            unique = [str(i) for i in data_unique[field] if i is not None]
        else:
            unique = [i for i in data_unique[field] if i is not None]

        data_unique[field] = unique
        data_nunique[field] = len(unique)

        str_unique += f"{field:25s} = {data_unique[field]}\n"
        str_nunique += f"{field:25s} = {data_nunique[field]}\n"


    with open("out_entries.txt", 'w') as file:
        file.write(str_entries)

    with open("out_unique.txt", 'w') as file:
        file.write(str_unique)

    with open("out_nunique.txt", 'w') as file:
        file.write(str_nunique)

def ex1():

    print("\nExample 1\n")

    entries = mpr.get_entries(
        chemsys_formula_mpids=["Li"]
    )

    for i, entry in enumerate(entries):
        print(f"\nEntry {i+1}\n")
        print(entry)

    # for analysis

    analyze_entries(entries)



def ex2():

    print("\nExample 2\n")

    entries = mpr.get_entries(
        chemsys_formula_mpids=["Li"],
        property_data=["chemsys", "nelements", "thermo_type"]
    )

    for i, entry in enumerate(entries):
        print(f"\nEntry {i+1}\n")
        print(entry)

    # for analysis

    analyze_entries(entries)


def ex3():

    print("\nExample 3\n")

    entries = mpr.get_entries(
        chemsys_formula_mpids=["Li"],
        property_data=["chemsys", "nelements", "thermo_type"],
        additional_criteria={"is_stable": True}
    )

    for i, entry in enumerate(entries):
        print(f"\nEntry {i+1}\n")
        print(entry)

    # for analysis

    analyze_entries(entries)


def ex4():

    print("\nExample 3\n")

    entries = mpr.get_entries(
        chemsys_formula_mpids=["Li", "Ni", "O", "Li-Ni", "Li-O", "Ni-O", "Li-Ni-O"],
        property_data=["chemsys", "nelements", "thermo_type"],
        additional_criteria={"is_stable": True}
    )

    for i, entry in enumerate(entries):
        print(f"\nEntry {i+1}\n")
        print(entry)

    # for analysis

    analyze_entries(entries)

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
def main():
    #ex1()
    #ex2()
    #ex3()
    ex4()

main()
