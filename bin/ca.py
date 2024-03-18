#!/usr/bin/env python

import os
import sys
import glob
import argparse
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
               "    ca.py -el Li,Ni,O\n"                                                                          
               "    mp_query.py -el Li,Ni,O -in 20\n"                                                                   
    )                                                                                                                   
    parser.add_argument('-f', '--files', nargs='+', dest='files',
                        default=None,
                        help='files to process')
    parser.add_argument('-r', '--rank', action='store_true',
                        help='Rank structures based on energy')                                                        
    parser.add_argument('-rp', '--rankpressure', action='store_true',
                        help='Rank structures based on pressure')                                                        
    parser.add_argument('-rv', '--rankvolume', action='store_true',
                        help='Rank structures based on volume')                                                        
    parser.add_argument('-pa', '--peratom', action='store_true',
                        help='Rank structures based on per-atom properties')                                                        
    parser.add_argument('-rdf', '--rdf', action='store_true',
                        help='Calculate radial distribution function')                                                        
    parser.add_argument('-cv', '--volume', action='store_true',
                        help='Calculate volume distribution')                                                        
    parser.add_argument('-cp', '--pressure',action='store_true',
                        help='Calculate pressure distribution')                                                        
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
                                                                                                                        
    print("\n".join(banner) + "\n",file=sys.stderr)                                                          
                                                                                                                        
    return args                                                                                                         
                     

#==============================================================================
# Main
#==============================================================================

# get arguments

args = get_args()

# check arguments

if args.files:
    files = args.files
else:
    patterns = ['*.res', '*.res.xz', '*.res.tar', '*.res.tar.xz']
    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern))

# read res filles

structures = []
fmt='ase'


for filename in files:

    if filename.endswith('res.tar') or filename.endswith('res.tar.xz'):
        restar = ResTar.from_file(filename, fmt=fmt)
        structures += restar.structures

    elif filename.endswith('.res') or filename.endswith('.res.xz'):
        concatres = ConcatRes.from_file(filename, fmt=fmt)
        structures += concatres.structures

    else:
        print(f"Warning: {filename}")

# print per-formula / per-atom information

cryan = CryanAtoms(structures)

norm = 'atom' if args.peratom else 'formula'

if args.rank:
    print(cryan.to_str(norm=norm))
    print(cryan.summary(), file=sys.stderr)
elif args.rankpressure:
    print(cryan.to_str(norm=norm, sort='pressure'))
    print(cryan.summary(), file=sys.stderr)
elif args.rankvolume:
    print(cryan.to_str(norm=norm, sort='volume'))
    print(cryan.summary(), file=sys.stderr)

if args.rdf:
    cryan.calc_rdf()                                                                                                        
    cryan.plot_rdf()

if args.volume:
    cryan.calc_vol()  

if args.pressure:
    cryan.calc_press()  
