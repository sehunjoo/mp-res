#!/usr/bin/env python

import tarfile
from ase.io.res import Res

class ResTar():

    def __init__(self, tarname, structures):
        self.tarname = tarname
        self.structures = structures


    def get_filelist_from_tar(tarname):
        with tarfile.open(tarname, 'r') as tar:
            files = tar.getnames()
        return files


    def read_file_from_tar(filename, tarname):
        with tarfile.open(tarname, 'r') as tar:
            # <class 'tarfile.ExFileObject'>
            file_obj = tar.extractfile(filename)
            if file_obj:
                # <class 'bytes'>
                file_bytes = file_obj.read()
                # <class 'str'>
                file_str = file_bytes.decode('utf-8')
                print(string)
            else:
                print(f'The file {filename} was not found in the archive/')

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
