#!/usr/bin/env python

from mp_api.client import MPRester
import time

api_key = "d7BCat3ve9lYksDLTojHg3AceBOcN5B9"
mpr = MPRester(api_key)



def example_materials_summary():

    #chemsys=["Li-Ni-O"]
    chemsys=["Li", "Ni", "O", "Li-Ni", "Li-O", "Ni-O", "Li-Ni-O"]
    fields=["nelements", "chemsys"]

    docs = mpr.materials.summary.search(
        chemsys=chemsys, 
        fields=fields
    )

    chemsys = [doc.chemsys for doc in docs]
    chemsys = list(dict.fromkeys(chemsys))

    nelements = [doc.nelements for doc in docs]
    nelements = list(dict.fromkeys(nelements))

    print(f"# SummaryDoc = {len(docs)}")
    print(f"# chemsys    = {len(chemsys)}")
    print(f"# elements  = {min(nelements)}-{max(nelements)}")
    #print("\n".join(chemsys_unique))
    #print(nelements_unique)


def example_materials_thermo():

    #chemsys=["Li-Ni-O"]
    chemsys=["Li", "Ni", "O", "Li-Ni", "Li-O", "Ni-O", "Li-Ni-O"]
    fields=["nelements", "chemsys"]

    docs = mpr.materials.thermo.search(
        chemsys=chemsys,
        fields=fields
    )

    chemsys = [doc.chemsys for doc in docs]
    chemsys = list(dict.fromkeys(chemsys))

    nelements = [doc.nelements for doc in docs]
    nelements = list(dict.fromkeys(nelements))

    print(f"# ThermoDoc  = {len(docs)}")
    print(f"# chemsys    = {len(chemsys)}")
    print(f"# elements   = {min(nelements)}-{max(nelements)}")




def main():

    #example_materials_summary()
    example_materials_thermo()


main()
