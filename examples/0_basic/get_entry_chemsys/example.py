#!/usr/bin/env python

from mp_api.client import MPRester
import time

api_key = "d7BCat3ve9lYksDLTojHg3AceBOcN5B9"
mpr = MPRester(api_key)

def example_get_entries_chemsys():

    #chemsys=["Li-Ni-O"]
    #chemsys=["O-Ni-Li"]
    chemsys=["Li", "Ni", "O", "Li-Ni", "Li-O", "Ni-O", "Li-Ni-O"]

    entries = mpr.get_entries(
        chemsys_formula_mpids=chemsys,
        property_data=["chemsys", "nelements"],
        additional_criteria={"is_stable": True}
    )

    chemsys = [entry.data.get("chemsys") for entry in entries]
    chemsys = list(dict.fromkeys(chemsys))

    nelements = [entry.data.get("nelements") for entry in entries]
    nelements = list(dict.fromkeys(nelements))

    print(f"# ThermoDoc  = {len(entries)}")
    print(f"# chemsys    = {len(chemsys)}")
    print(f"# elements   = {min(nelements)}-{max(nelements)}")




def main():

    example_get_entries_chemsys()


main()
