#!/usr/bin/env python

from mp_api.client import MPRester
import time

api_key = "d7BCat3ve9lYksDLTojHg3AceBOcN5B9"
mpr = MPRester(api_key)


def example_materials_summary():

    elements=["Li"]
    fields=["nelements", "chemsys"]

    docs = mpr.materials.summary.search(
        elements=elements, 
        fields=fields
    )

    chemsys = [doc.chemsys for doc in docs]
    chemsys_unique = list(dict.fromkeys(chemsys))
    print("\n".join(chemsys_unique))

    nelements = [doc.nelements for doc in docs]
    nelements_unique = list(dict.fromkeys(nelements))
    print(nelements_unique)

def example_materials_thermo_id_fail():


    elements=["Li"]
    fields=["nelements"]

    docs = mpr.materials.summary.search(
        elements=elements,
        fields=["material_id"]
    )

    material_ids = [doc.material_id for doc in docs]

    docs = mpr.materials.thermo.search(
        material_ids=material_ids,
        fields=fields
    )

    nelements = [doc.nelements for doc in docs]
    nelements_unique = list(dict.fromkeys(nelements))
    print(nelements_unique)


def main():


    elements=["Li"]
    fields=["nelements"]

    #docs = mpr.materials.summary.search(
    #    elements=elements,
    #    fields=["chemsys"]
    #)

    #chemsys = [doc.chemsys for doc in docs]
    #chemsys_unique = list(dict.fromkeys(chemsys))
    #print(f"# chemsys = {len(chemsys_unique)}")

    #docs = mpr.materials.thermo.search(
    #    chemsys=chemsys_unique,
    #    fields=fields
    #)

    docs = mpr.materials.thermo.search(
        chemsys=["Li-*"],
        fields=fields
    )

    docs = mpr.materials.thermo.search(
        chemsys="Li-*",
        fields=fields
    )

    docs = mpr.materials.thermo.search(
        chemsys=["Li-*", "*-Li-*", "*-Li", "Li"],
        fields=fields
    )
    


main()
