#!/usr/bin/env python

from mp_api.client import MPRester
import time

api_key = "d7BCat3ve9lYksDLTojHg3AceBOcN5B9"
mpr = MPRester(api_key)




def example_get_entries():

    #elements=["Li"]

    elements=["Li", "Ni", "O"]
    fields=["nelements", "chemsys"]

    docs = mpr.get_entries(
        chemsys_formula_mpids=chemsys
    )

    chemsys = [doc.chemsys for doc in docs]
    chemsys = list(dict.fromkeys(chemsys))

    nelements = [doc.nelements for doc in docs]
    nelements = list(dict.fromkeys(nelements))

    print(f"# SummaryDoc = {len(docs)}")
    print(f"# chemsys    = {len(chemsys)}")
    print(f"# elements   = {min(nelements)}-{max(nelements)}")

    entries = mpr.get_entries(
        chemsys_formula_mpids=chemsys,
        compatibility_only=True,
        property_data=["chemsys", "nelements"],
        conventional_unit_cell=False,
        additional_criteria=None
    )

    chemsys = [entry.data.get("chemsys") for entry in entries]
    chemsys = list(dict.fromkeys(chemsys))

    nelements = [entry.data.get("nelements") for entry in entries]
    nelements = list(dict.fromkeys(nelements))

    print(f"# ThermoDoc  = {len(entries)}")
    print(f"# chemsys    = {len(chemsys)}")
    print(f"# elements   = {min(nelements)}-{max(nelements)}")


def example_get_entries_chemsys():

    chemsys=["Li-Ni-O"]

    entries = mpr.get_entries(
        chemsys_formula_mpids=chemsys,
        compatibility_only=True,
        property_data=["chemsys", "nelements"],
        conventional_unit_cell=False,
        additional_criteria=None
    )

    chemsys = [entry.data.get("chemsys") for entry in entries]
    chemsys = list(dict.fromkeys(chemsys))

    nelements = [entry.data.get("nelements") for entry in entries]
    nelements = list(dict.fromkeys(nelements))

    print(f"# ThermoDoc  = {len(entries)}")
    print(f"# chemsys    = {len(chemsys)}")
    print(f"# elements   = {min(nelements)}-{max(nelements)}")


def example1():

    print("\nExample - Li\n")

    docs = mpr.materials.summary.search(
        elements=["Li"],
        fields=["chemsys"]
    )

    chemsys = [doc.chemsys for doc in docs]
    chemsys = list(dict.fromkeys(chemsys))

    entries = mpr.get_entries(
        chemsys_formula_mpids=chemsys,
        property_data=["chemsys","nelements"]
    )

    chemsys = [entry.data.get("chemsys") for entry in entries]
    chemsys = list(dict.fromkeys(chemsys))

    nelements = [entry.data.get("nelements") for entry in entries]
    nelements = list(dict.fromkeys(nelements))

    print(f"# ThermoDoc  = {len(entries)}")
    print(f"# chemsys    = {len(chemsys)}")
    print(f"# elements   = {min(nelements)}-{max(nelements)}")

def example2():

    print("\nExample - Li, Ni, O\n")

    docs = mpr.materials.summary.search(
        elements=["Li", "Ni", "O"],
        fields=["chemsys"]
    )

    chemsys = [doc.chemsys for doc in docs]
    chemsys = list(dict.fromkeys(chemsys))

    entries = mpr.get_entries(
        chemsys_formula_mpids=chemsys,
        property_data=["chemsys","nelements"]
    )

    chemsys = [entry.data.get("chemsys") for entry in entries]
    chemsys = list(dict.fromkeys(chemsys))

    nelements = [entry.data.get("nelements") for entry in entries]
    nelements = list(dict.fromkeys(nelements))

    print(f"# ComputedStructureEntry  = {len(entries)}")
    print(f"# chemsys                 = {len(chemsys)}")
    print(f"# elements                = {min(nelements)}-{max(nelements)}")


def example3():

    print("\nExample - Li, Ni, O on the hull\n")

    docs = mpr.materials.summary.search(
        elements=["Li", "Ni", "O"],
        fields=["chemsys"]
    )

    chemsys = [doc.chemsys for doc in docs]
    chemsys = list(dict.fromkeys(chemsys))

    entries = mpr.get_entries(
        chemsys_formula_mpids=chemsys,
        property_data=["chemsys","nelements"]
        
    )

    chemsys = [entry.data.get("chemsys") for entry in entries]
    chemsys = list(dict.fromkeys(chemsys))

    nelements = [entry.data.get("nelements") for entry in entries]
    nelements = list(dict.fromkeys(nelements))

    print(f"# ComputedStructureEntry  = {len(entries)}")
    print(f"# chemsys                 = {len(chemsys)}")
    print(f"# elements                = {min(nelements)}-{max(nelements)}")

def main():

    #example_get_entries_chemsys()
    #example1()
    example2()


main()
