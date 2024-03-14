#!/usr/bin/env python

"""
Read/Write *.res, data.res, *.res.tar
"""

import tarfile

from ase import Atoms
from ase.io.res import Res as aseRes  # Res, read_res, write_res

from pymatgen.entries.computed_entries import ComputedStructureEntry
from pymatgen.io.res import ResIO as pymatgenResIO # ResIO, AirssProvider
from pymatgen.io.res import AirssProvider as pymatgenAirssProvider


# Read res files


class Res():
    """
    Read a single res file as
        - ASE Atoms
        - Pymatgen ComputedStructureEntry (recommended)

    Args:
    - filename: str
    - structure: Atoms | ComputedStructureEntry
    """

    def __init__(self, filename: str, structure: Atoms | ComputedStructureEntry):
        """
        This class can be constructed from either a ASE Atoms object
        or pymatgen ComputedStructureEntry.
        """
        self.filename = filename
        self.structure = structure


    @classmethod
    def ase_atoms_from_file(cls, filename: str) -> Atoms:
        """
        Read a res file as ASE Atoms object
        """
        with open(filename, 'r') as f:
            return cls.ase_atoms_from_str(f.read())

    @classmethod
    def ase_atoms_from_str(cls, string: str) -> Atoms:
        """
        Read a res file as ASE Atoms object
        """
        return aseRes.from_string(string).atoms

    @classmethod
    def pymatgen_entry_from_file(cls, filename: str) -> ComputedStructureEntry:
        """
        Read a res file as Pymatgen ComputedStructureEntry object
        """
        with open(filename, 'r') as f:
            #return AirssProvider.from_str(string).entry
            return cls.pymatgen_entry_from_str(f.read())

    @classmethod
    def pymatgen_entry_from_str(cls, string: str) -> ComputedStructureEntry:
        """
        Read a res file as Pymatgen ComputedStructureEntry object
        """
        res = pymatgenAirssProvider.from_str(string)
        return ComputedStructureEntry(
            res.structure,
            res.energy,
            data={
                "seed": res.seed,
                "pressure": res.pressure,
                "rems": res.rems
            }
        )

    @classmethod
    def from_file(cls, filename: str, fmt: str='pymatgen') -> 'Res':
        """
        Read a res file
        """
        if fmt == 'pymatgen':
            structure = cls.pymatgen_entry_from_file(filename)
        elif fmt == 'ase':
            structure = cls.ase_atoms_from_file(filename)
        else:
            raise ValueError("Unsupported format: {}".format(fmt))
        return cls(filename, structure)


    @property
    def entry(self):
        return self.structure

    @property
    def atoms(self):
        return self.structure


class ConcatRes():
    """
    Read a single concatenated res file as
        - ASE Atoms
        - Pymatgen ComputedStructureEntry (recommended)

    Args:
    - filename: str
    - structure: list[Atoms] | list[ComputedStructureEntry]
    """

    def __init__(self,
        filename: str,
        structures: list[Atoms] | list[ComputedStructureEntry]
    ):
        """
        Initializes the ConcatRes object with a filename and a list of structures.
        """
        self.filename = filename
        self.structures = structures


    @classmethod
    def ase_atoms_from_file(cls, filename: str) -> list[Atoms]:
        """
        Read a concatenated res file as a list of ASE Atoms object.
        """
        with open(filename, 'r') as f:
            return cls.ase_atoms_from_str(f.read())

    @classmethod
    def ase_atoms_from_str(cls, string: str) -> list[Atoms]:
        """
        Read a concatenated res file as a list of ASE Atoms object.
        """
        structures = []
        resstrs = [resstr.lstrip() + 'END\n' for resstr in string.split('END\n')
                   if resstr.strip().startswith('TITL')]

        for resstr in resstrs:
            structures.append(aseRes.from_string(resstr).atoms)

        return structures

    @classmethod
    def pymatgen_entry_from_file(cls, filename: str
    ) -> list[ComputedStructureEntry]:
        """
        Read a res file as Pymatgen ComputedStructureEntry object
        """
        with open(filename, 'r') as f:
            return cls.pymatgen_entry_from_str(f.read())

    @classmethod
    def pymatgen_entry_from_str(cls, string: str
    ) -> list[ComputedStructureEntry]:
        """
        Read a res file as Pymatgen ComputedStructureEntry object
        """
        structures = []
        resstrs = [resstr.lstrip() + 'END\n' for resstr in string.split('END\n')
                   if resstr.strip().startswith('TITL')]

        for resstr in resstrs:
            structures.append(pymatgenResIO.entry_from_str(resstr))

        return structures

    @classmethod
    def from_file(cls, filename: str, fmt: str='pymatgen') -> list['Res']:
        """
        Read a res file
        """
        if fmt == 'pymatgen':
            structures = cls.pymatgen_entry_from_file(filename)
        elif fmt == 'ase':
            structures = cls.ase_atoms_from_file(filename)
        else:
            raise ValueError("Unsupported format: {}".format(fmt))
        return cls(filename, structures)



class ResTar():

    def __init__(self,
        tarname: str,
        structures: list[Atoms] | list[ComputedStructureEntry]
    ):
        self.tarname = tarname
        self.structures = structures


    @ classmethod
    def ase_atoms_from_file(cls, tarname: str) -> list[Atoms]:
        """
        Read a restar file as a list of ASE Atoms objects
        """
        structures = []
        with tarfile.open(tarname, 'r') as tar:
            for member in tar.getmembers():
                if member.isfile() and member.name.endswith('.res'):
                    res_obj = tar.extractfile(member)
                    if res_obj:
                        string = res_obj.read().decode('utf-8')
                        structures.append(aseRes.from_string(string).atoms)
                    else:
                        print(f'The file {filename} was not found in the archive/')

        return structures


    @ classmethod
    def pymatgen_entry_from_file(cls, tarname: str
    ) -> list[ComputedStructureEntry]:
        """
        Read a restar file as a list of pymatgen ComputedStructureEntry objects
        """
        structures = []
        with tarfile.open(tarname, 'r') as tar:
            for member in tar.getmembers():
                if member.isfile() and member.name.endswith('.res'):
                    res_obj = tar.extractfile(member)
                    if res_obj:
                        string = res_obj.read().decode('utf-8')
                        structures.append(pymatgenResIO.entry_from_str(string))
                    else:
                        print(f'The file {filename} was not found in the archive/')

        return structures

    @classmethod
    def from_file(cls, filename: str, fmt: str='pymatgen') -> list['Res']:
        """
        Read a res file
        """
        if fmt == 'pymatgen':
            structures = cls.pymatgen_entry_from_file(filename)
        elif fmt == 'ase':
            structures = cls.ase_atoms_from_file(filename)
        else:
            raise ValueError("Unsupported format: {}".format(fmt))
        return cls(filename, structures)


    def read_file_from_tar(filename, tarname):
        """
        Work on this later
        """
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

    def get_filelist_from_tar(tarname):
        """
        Work on this later
        """
        with tarfile.open(tarname, 'r') as tar:
            files = tar.getnames()
        return files
