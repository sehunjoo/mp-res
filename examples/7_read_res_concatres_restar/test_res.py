#!/usr/bin/env python

from res import Res, ConcatRes, ResTar


def test_read_res():
    filename = 'mp-865631-R2SCAN.res'
    print('-'*100)
    res = Res.from_file(filename, fmt='pymatgen')
    print(res.structure)
    print('-'*100)
    res = Res.from_file(filename, fmt='ase')
    print(res.structure)


def test_read_concatres():
    filename = 'data.res'
    print('-'*100)
    res = ConcatRes.from_file(filename, fmt='pymatgen')
    for st in res.structures:
        print(st)
        print()
    print('-'*100)
    res = ConcatRes.from_file(filename, fmt='ase')
    for st in res.structures:
        print(st)
        print()

def test_read_restar():
    filename = 'Li-Ni-O_eah0.res.tar'
    print('-'*100)
    res = ResTar.from_file(filename, fmt='pymatgen')
    for st in res.structures:
        print(st)
        print()
    print('-'*100)
    res = ResTar.from_file(filename, fmt='ase')
    for st in res.structures:
        print(st)
        print()



#test_read_res()
#test_read_concatres()
test_read_restar()
