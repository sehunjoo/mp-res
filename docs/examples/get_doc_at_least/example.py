#!/usr/bin/env python

from mp_api.client import MPRester
import time

api_key = "d7BCat3ve9lYksDLTojHg3AceBOcN5B9"
mpr = MPRester(api_key)



def example_materials_summary():

    elements=["Li"]
    #elements=["Li", "Ni", "O"]
    fields=["nelements", "chemsys"]

    docs = mpr.materials.summary.search(
        elements=elements, 
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

    elements=["Li"]
    fields=["nelements", "chemsys"]

    docs = mpr.materials.summary.search(
        elements=elements,
        fields=fields
    )

    chemsys = [doc.chemsys for doc in docs]
    chemsys = list(dict.fromkeys(chemsys))

    nelements = [doc.nelements for doc in docs]
    nelements = list(dict.fromkeys(nelements))

    print(f"# SummaryDoc = {len(docs)}")
    print(f"# chemsys    = {len(chemsys)}")
    print(f"# elements   = {min(nelements)}-{max(nelements)}")

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



def error_example_materials_thermo_id():

    elements=["Li"]
    fields=["nelements", "chemsys"]

    docs = mpr.materials.summary.search(
        elements=elements,
        fields=["material_id"]
    )

    material_ids = [doc.material_id for doc in docs]

    docs = mpr.materials.thermo.search(
        material_ids=material_ids,
        fields=fields
    )



def error_example_materials_thermo_chemsys_wildcard():

    elements=["Li"]
    fields=["nelements", "chemsys"]

    docs = mpr.materials.thermo.search(
        chemsys=["Li-*", "*-Li"],
        fields=fields
    )

    chemsys = [doc.chemsys for doc in docs]
    chemsys = list(dict.fromkeys(chemsys))

    nelements = [doc.nelements for doc in docs]
    nelements = list(dict.fromkeys(nelements))

    print(f"# SummaryDoc = {len(docs)}")
    print(f"# chemsys    = {len(chemsys)}")
    print(f"# elements  = {min(nelements)}-{max(nelements)}")
    
    docs = mpr.materials.thermo.search(
        chemsys=["Li-*-*", "*-Li-*", "*-*-Li"],
        fields=fields
    )

    chemsys = [doc.chemsys for doc in docs]
    chemsys = list(dict.fromkeys(chemsys))

    nelements = [doc.nelements for doc in docs]
    nelements = list(dict.fromkeys(nelements))

    print(f"# SummaryDoc = {len(docs)}")
    print(f"# chemsys    = {len(chemsys)}")
    print(f"# elements  = {min(nelements)}-{max(nelements)}")



def main():

    #example_materials_summary()
    example_materials_thermo()

    #error_example_materials_thermo_id()
    #error_example_materials_thermo_chemsys_wildcard()

main()
