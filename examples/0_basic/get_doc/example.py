#!/usr/bin/env python

from mp_api.client import MPRester

api_key = "d7BCat3ve9lYksDLTojHg3AceBOcN5B9"
mpr = MPRester(api_key)

def main():

    avfields = mpr.materials.summary.available_fields

    print()
    print("-"*80)
    print("Endpoint (Document Model) = materials.summary (SummaryDoc)")
    print(f"# available fields        = {len(avfields)}")
    print("-"*80)
    print("\n".join(avfields))
    print("-"*80)
    print()


    avfields = mpr.materials.thermo.available_fields

    print()
    print("-"*80)
    print("Endpoint (Document Model) = materials.thermo (ThermoDoc)")
    print(f"# available fields        = {len(avfields)}")
    print("-"*80)
    print("\n".join(avfields))
    print("-"*80)
    print()

main()
