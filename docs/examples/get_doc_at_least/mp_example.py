#!/usr/bin/env python

from mp_api.client import MPRester
from pymatgen.io.res import ResWriter

api_key = "d7BCat3ve9lYksDLTojHg3AceBOcN5B9"
mpr = MPRester(api_key)

# https://docs.materialsproject.org/downloading-data/using-the-api/examples

def mp_example():

    print()

    chemsys = "Ni"

    fields = ["material_id",
        "chemsys",
        "formula_pretty",
        "is_stable",
        "theoretical",
        "nsites",
        "nelements",
        "symmetry",
        "task_ids"
    ]


    #docs = mpr.materials.summary.search(
    #    chemsys=chemsys
    #)
    docs = mpr.thermo.search(
        chemsys=chemsys
    )

    print("Print the type of docs", "-"*84, sep="\n")
    print("<class 'list'>")
    print(type(docs))
    print()

    print("Print the number of docs", "-"*84, sep="\n")
    print(len(docs))
    print()

    print("Print entries", "-"*84, sep="\n")
    print("This will print a concatenated entry")
    #print(docs)
    print()

    doc = docs[0]

    print("Print the type of doc", "-"*84, sep="\n")
    print("<class 'mp_api.client.core.client.MPDataDoc'>")
    print(type(doc))
    print()

    print("Print the type of doc", "-"*84, sep="\n")
    print(type(doc.entries))
    #print()

    #print(docs[0])
    #print()

    #print(docs[0].structure)


mp_example()
