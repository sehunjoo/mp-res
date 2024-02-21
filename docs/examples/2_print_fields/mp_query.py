#!/usr/bin/env python

from mp_api.client import MPRester
import sys
import argparse
import itertools
import pandas as pd
import time

api_key = "d7BCat3ve9lYksDLTojHg3AceBOcN5B9"
mpr = MPRester(api_key)


def parse():
    """
    Parse arguments
    """

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Retrieve structures from Materials Project database",
        epilog="examples:\n"
               "    mp_query.py -el Li,Ni,O\n"
               "    mp_query.py -el Li,Ni,O -in 20\n"
    )

    parser.add_argument('-el', '--elementlist', type=str, dest='elements',
                        default=None,
                        help='Comma separated list of elements')
    parser.add_argument('-sn', '--speciesnumber', type=int, dest='nelements',
                        default=0,
                        help='Number of species, e.g 2 for binary')
    parser.add_argument('-in', '--ionsnumber', type=int, dest='maxnsites',
                        default=99999,
                        help='Number of ions, range up to')
    parser.add_argument('-f', '--format', type=str, dest='fmt',
                        default='POSCAR',
                        help='Format to output to; cif, poscar, cssr, json, xsf, mcsqs, prismatic, yaml, fleur-impgen')
    parser.add_argument('-af', '--availablefields', dest='availablefields', action='store_const', const=True,
                        default=False,
                        help='Check a list of avaialble fields')
    parser.add_argument('-t', '--test', dest='test', action='store_const', const=True,
                        default=False,
                        help='Test')
    args = parser.parse_args()

    for attr in dir(args):
        if not attr.startswith('_'):
            print(f"{attr:<20}: {getattr(args, attr)}")
    print()

    return args



def get_chemsys_from_elements(elements: list[str], nelements: int = 0) -> list:
    """
    Get a full combinatorial expansion into all possible chemical subsystems.

    Args:
        elements (list): A list of chemical elements
        nelements (int): The number of chemical elements to generate combinatorial chemical systems.
            Defaults to 0, which generated all possible combinatorial chemical systems. Set 2 for binary systems.

    Returns:
        
    """
    chemsys = []

    if nelements != 0:
        for els in itertools.combinations(elements, nelements):
            chemsys.append("-".join(sorted(els)))
    else:
        for i in range(len(elements)):
            for els in itertools.combinations(elements, i + 1):
                chemsys.append("-".join(sorted(els)))

    return chemsys



def gga_u_applied(elements: list[str]) -> bool:
    """
    Check if the GGA+U method has been applied to the given system.
    Hubbard U correction is applied to oxides or fluorides in the Materials Project database.
    """
    return any(e in elements for e in ['O', 'F']) and \
           any(e in elements for e in ['Co', 'Cr', 'Fe', 'Mn', 'Mo', 'Ni', 'V', 'W'])


def print_available_fields():
    """
    print a list of available fields
    """
    list_of_available_fields = mpr.materials.summary.available_fields
    print("-"*50)
    print("List of available fields")
    print("-"*50)
    print("\n".join(list_of_available_fields))
    print()



# Query data

def get_structure_from_chemsys(
    chemsys: str | list[str],
    longname: bool = False,
    fmt: str = "POSCAR",
    csv: bool = False,
    maxnsites: int = 99999
):
    """
    Get a list of Materials Project IDs for materials containing only elements specified

    Args:
        chemsys (str | list[str]): Chemical systems e.g., Li-Ni-O
        longname (bool): Output the structure to a file with a long name
        fmt (str): Format to output to. Options include “cif”, “poscar”, “cssr”, “json”, “xsf”, “mcsqs”, “prismatic”, “yaml”, “fleur-inpgen”. Non-case sensitive.
        csv (bool): Write a csv file
    """

    # set up parameters for retreving documents from Materials Project database

    fields = ["material_id", "chemsys", "structure"]

    if longname:
        fields += ["formula_pretty", "nsites", "symmetry"]

    if csv:
        fields_csv = ["material_id",
                        "chemsys",
                        "formula_pretty",
                        "is_stable",
                        "theoretical",
                        "nsites",
                        "nelements",
                        "symmetry"]
        d_csv = {field: [] for field in fields_csv}
        fields = list(dict.fromkeys(fields + fields_csv)) # unique


    # retrieve documents from Materials Project database

    print("Retrieving data from Materials Project ...")
    print("Chemical Systems: ", chemsys)
    print("Fields: ", fields)
    start_time = time.time()
    docs = mpr.materials.summary.search(chemsys=chemsys, fields=fields, num_sites=(0,maxnsites))
    end_time = time.time()
    duration = end_time - start_time
    print(f"Time taken: {duration} seconds")


    # write a csv file

    if csv:
        for doc in docs:
            for field in fields_csv:
                if field == "symmetry":
                    d_csv[field].append(getattr(doc, field).symbol)
                else:
                    d_csv[field].append(getattr(doc, field))
        df_csv = pd.DataFrame(d_csv)
        df_csv.to_csv('mp.csv', sep=',', index=False)
        print("mp.csv is created")


    # output structures to files

    for doc in docs:
        mpid = doc.material_id
        chemsys = doc.chemsys
        structure = doc.structure

        crudroot = "mp_pbe" if not gga_u_applied(chemsys.split('-')) else "mp_pbe+u"
        filename = f"{crudroot}-{mpid}.{fmt}"

        if longname:
            formula = doc.formula_pretty
            nsites = doc.nsites
            sg = doc.symmetry.symbol
            sg = sg.replace("/","").replace("_","")
            filename = f"{crudroot}-{formula}-{nsites}-{sg}-{mpid}.{fmt}"


        structure.to(filename=filename, fmt=fmt)

# Query data

def get_structure_from_elements(
    elements: str | list[str],
    longname: bool = False,
    fmt: str = "POSCAR",
    csv: bool = False,
    maxnsites: int = 99999
):
    """
    Get a list of Materials Project IDs for materials containing only elements specified

    Args:
        chemsys (str | list[str]): Chemical systems e.g., Li-Ni-O
        longname (bool): Output the structure to a file with a long name
        fmt (str): Format to output to. Options include “cif”, “poscar”, “cssr”, “json”, “xsf”, “mcsqs”, “prismatic”, “yaml”, “fleur-inpgen”. Non-case sensitive.
        csv (bool): Write a csv file
    """

    # set up parameters for retreving documents from Materials Project database

    fields = ["material_id", "chemsys", "structure"]

    if longname:
        fields += ["formula_pretty", "nsites", "symmetry"]

    if csv:
        fields_csv = ["material_id",
                        "chemsys",
                        "formula_pretty",
                        "is_stable",
                        "theoretical",
                        "nsites",
                        "nelements",
                        "symmetry"]
        d_csv = {field: [] for field in fields_csv}
        fields = list(dict.fromkeys(fields + fields_csv)) # unique


    # retrieve documents from Materials Project database

    print("Retrieving data from Materials Project ...")
    print("Elements: ", elements)
    print("Fields: ", fields)
    start_time = time.time()
    docs = mpr.materials.summary.search(elements=["Li"], fields=fields, num_sites=(0,maxnsites))
    end_time = time.time()
    duration = end_time - start_time
    print(f"Time taken: {duration} seconds")


    # write a csv file

    if csv:
        for doc in docs:
            for field in fields_csv:
                if field == "symmetry":
                    d_csv[field].append(getattr(doc, field).symbol)
                else:
                    d_csv[field].append(getattr(doc, field))
        df_csv = pd.DataFrame(d_csv)
        df_csv.to_csv('mp.csv', sep=',', index=False)
        print("mp.csv is created")


    # output structures to files

    for doc in docs:
        mpid = doc.material_id
        chemsys = doc.chemsys
        structure = doc.structure

        crudroot = "mp_pbe" if not gga_u_applied(chemsys.split('-')) else "mp_pbe+u"
        crudroot = "mp"
        filename = f"{crudroot}-{mpid}.{fmt}"

        if longname:
            formula = doc.formula_pretty
            nsites = doc.nsites
            sg = doc.symmetry.symbol
            sg = sg.replace("/","").replace("_","")
            filename = f"{crudroot}-{formula}-{nsites}-{sg}-{mpid}.{fmt}"


        structure.to(filename=filename, fmt=fmt)


############################
# for test
############################
def test(args):
    elements = args.elements.split(",")
    fmt = args.fmt
    chemsys = get_chemsys_from_elements(elements)
    get_mpid_from_chemsys(chemsys, csv=True)
    pass

#############################
# Main
#############################


def main():

    args = parse()

    if args.availablefields:
        print_available_fields()
        exit()

    if args.test:
        test(args)
        exit()

    if args.elements != None:

        elements = args.elements.split(",")
        fmt = args.fmt
        maxnsites = args.maxnsites

        #chemsys = get_chemsys_from_elements(elements)

        #get_structure_from_chemsys(chemsys=chemsys, csv=True, fmt=fmt, maxnsites=maxnsites)
        get_structure_from_elements(elements=elements, csv=True, fmt=fmt, maxnsites=maxnsites)



main()
