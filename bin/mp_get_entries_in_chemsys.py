#!/usr/bin/env python

import subprocess
from mp_api.client import MPRester
from pymatgen.io.res import ResWriter, Res
import pandas as pd

api_key = "d7BCat3ve9lYksDLTojHg3AceBOcN5B9"
mpr = MPRester(api_key)

# https://docs.materialsproject.org/downloading-data/using-the-api/examples

def mp_example():

    # get list of entries
    # return a list, each element of which is ComputedStructureEntry of pymatgen

    entries = mpr.get_entries_in_chemsys(elements=["Li", "Fe", "O"], 
                                         additional_criteria={"thermo_types": ["GGA_GGA+U"]}) 


    print("", "type of entries", "-"*84, sep="\n")
    print(type(entries))
    print()

    for entry in entries:
        print("type of each entry", type(entry))
        print(entry)
        print()
        exit()
    #print(entries)

    #for entry in entries:
    #    print('----------------------------')
    #    type(entry)
    #    print(entry)
    #    res = ResWriter(entry)
    #    print(res)

mp_example()
