#!/usr/bin/env python

from mp_api.client import MPRester
from pymatgen.io.res import ResIO

api_key = "d7BCat3ve9lYksDLTojHg3AceBOcN5B9"
mpr = MPRester(api_key)

def main():

    avfields = mpr.materials.summary.available_fields

    print()
    print("Available fields for materials doc")
    print("-"*80)
    print("\n".join(avfields))
    print("-"*80)
    print()


    avfields = mpr.materials.summary.available_fields

    print()
    print("Available fields for materials doc")
    print("-"*80)
    print("\n".join(avfields))
    print("-"*80)
    print()

main()
