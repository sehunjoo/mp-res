#!/usr/bin/env python

import sys

from cryan import CryanAtoms
from res import Res, ConcatRes, ResTar


def get_args():                                                                                                         
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
    parser.add_argument('-f', '--files', nargs='+', dest='files',
                        default=None,
                        help='files to process')
    parser.add_argument('-rdf', '--rdf', type=bool, dest='rdf',                                              
                        default=False,                                                                                   
                        help='Comma separated list of elements')                                                        
    parser.add_argument('-vol', '--vol', type=bool, dest='vol',                                              
                        default=False,                                                                                   
                        help='Comma separated list of elements')                                                        
    args = parser.parse_args()                                                                                          
                                                                                                                        
                                                                                                                        
    # banner                                                                                                            
                                                                                                                        
    banner = [                                                                                                          
        f"",                                                                                                            
        f"     {os.path.basename(__file__)}",                                                                           
        f"",                                                                                                            
        f"       Author: Se Hun Joo (shj29@cam.ac.uk)",                                                                 
        f"",                                                                                                            
        f"       Summary of arguments",                                                                                 
        f""                                                                                                             
    ]                                                                                                                   
                                                                                                                        
    banner += [                                                                                                         
        f"         {attr:<20}: {getattr(args, attr)}"                                                                   
        for attr in dir(args)                                                                                           
        if not attr.startswith('_')                                                                                     
    ]                                                                                                                   
                                                                                                                        
    print("\n".join(banner) + "\n")                                                                                     
                                                                                                                        
    return args                                                                                                         
                     

#==============================================================================
# Main
#==============================================================================

# get arguments

args = get_args()

# check arguments

if not args.files:
    exit()

files = args.files

# read res filles

structures = []
fmt='ase'

for filename in filenames:
    if filename.endswith('res.tar'):
        restar = ResTar.from_file(filename, fmt=fmt)
        structures += restar.structures
    elif filename.endswith('.res'):
        concatres = ConcatRes.from_file(filename, fmt=fmt)
        structures += concatres.structures
    else:
        print(f"Warning: {filename}")

# print per-formula / per-atom information

cryan = CryanAtoms(structures)
#print(cryan)
print(cryan.to_str_per_atom())
print(cryan.summary())

if args.rdf:
    cryan.calc_rdf()                                                                                                        
    cryan.plot_rdf()

if args.vol:
    print(cryan.to_str_per_atom())                                                                                          
    cryan.calc_vol()  
