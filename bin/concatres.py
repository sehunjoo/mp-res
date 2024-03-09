#!/usr/bin/env python

from ase.io.res import Res

class ConcatRes():

    def __init__(self, filename, structures):
        self.filename = filename
        self.structures = structures


    @ classmethod
    def read_as_atoms(cls, tarname):

        structures = []

        with tarfile.open(tarname, 'r') as tar:
            for member in tar.getmembers():
                if member.isfile() and member.name.endswith('.res'):
                    res_obj = tar.extractfile(member)
                    if res_obj:
                        res_string = res_obj.read().decode('utf-8')
                        # Append the string to the list
                        structures.append(Res.from_string(res_string).atoms)
                    else:
                        print(f'The file {filename} was not found in the archive/')

        return cls(tarname=tarname, structures=structures)

    @ classmethod
    def read_as_atoms(cls, filename):

        structures = []

        with open(filename, 'r') as f:
            f_string = f.read()

        res_string_list = [res.lstrip() + 'END\n' for res in f_string.split('END\n') if res.strip().startswith('TITL')]

        for res_string in res_string_list:
            structures.append(Res.from_string(res_string).atoms)

        return cls(filename=filename, structures=structures)
