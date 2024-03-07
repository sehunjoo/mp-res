#!/usr/bin/env python

from mp_api.client import MPRester
from pymatgen.io.res import ResIO

api_key = "d7BCat3ve9lYksDLTojHg3AceBOcN5B9"
mpr = MPRester(api_key)

def main():

    chemsys_formula_mpids = "Li-Ni-O"

    entries = mpr.get_entries(chemsys_formula_mpids)

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
