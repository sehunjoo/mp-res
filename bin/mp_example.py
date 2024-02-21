#!/usr/bin/env python

import subprocess
from mp_api.client import MPRester
import pandas as pd

api_key = "d7BCat3ve9lYksDLTojHg3AceBOcN5B9"
mpr = MPRester(api_key)

# https://docs.materialsproject.org/downloading-data/using-the-api/examples

def mp_example():
    docs = mpr.summary.search(material_ids=["mp-1271793"], fields=["structure", "elements"])
    doc = docs[0]
    structure = doc.structure
    print("\nPrint document\n")
    print(docs[0])
    print("\nPrint structure\n")
    print(structure)
    print("elements: ", getattr(doc, "elements"))
    #help(structure)
    structure.to(filename="hi", fmt="POSCAR")

mp_example()
