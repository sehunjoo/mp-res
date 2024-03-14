#!/usr/bin/env python


import argparse
from pymatgen.core import Structure, Element, Composition
from pymatgen.transformations.standard_transformations import RemoveSpeciesTransformation
from res import Res, ResTar, ConcatRes
from dataclasses import dataclass
from pymatgen.entries.computed_entries import ComputedStructureEntry, ComputedEntry



def remove_li(structure: Structure) -> Structure:
    """
    Remove Li atoms using pymatgen.trnasformations package

    Args:
        structure: pymatgen Structure class
    Return:
        structure with Li atoms removed pymatgen Structure class
    """

    #print(structure)
    trans = RemoveSpeciesTransformation(["Li"])
    transformed_structure = trans.apply_transformation(structure)
    #print(transformed_structure)

    return transformed_structure

"""
if args.seed != None:

    seed = args.seed
    fmt = args.fmt

    structure = Structure.from_file(f'{seed}.res')
    
    #print(structure)
    
    trans = RemoveSpeciesTransformation(["Li"])
    
    transformed_structure = trans.apply_transformation(structure)
    
    #print(transformed_structure)
    
    transformed_structure.to(filename=f'{seed}-Li000.{fmt}', fmt=fmt)
"""

@dataclass
class Electrode():
    """
    Electrode material
    """
    entry_electrode: ComputedStructureEntry
    working_ion: str
    rcomp_electrode: str
    rcomp_framework: str
    nfu_electrode: str
    nfu_framework: str
    mass_electrode: float
    mass_framework: float

    @classmethod
    def from_entry(cls,
        working_electrode: ComputedStructureEntry,
        working_ion: str
    ):
        # cathode : working electrode - new material being tested
        entry_we = working_electrode
        # anode : counter/reference - metal
        element_wion = Element(working_ion)
        symbol_wion = element_wion.symbol

        # check that working electrode conatins the working ion
        if not entry_we.composition.get_atomic_fraction(element_wion) > 0:
            raise ValueError("The working ion must be present in the working electrode")

        # working electrode
        comp_we = entry_we.composition
        rcomp_we, nfu_we = comp_we.get_reduced_composition_and_factor()
        mass_we = comp_we.weight / nfu_we
        frac_we = comp_we.get_atomic_fraction(element_wion)

        # framework
        comp_fw = Composition({el: comp_we[el] for el in comp_we if el.symbol != symbol_wion})
        rcomp_fw, nfu_fw = comp_fw.get_reduced_composition_and_factor()
        mass_fw = comp_fw.weight / rcomp_fw
        frac_fw = comp_fw.get_atomic_fraction(element_wion)

        x_we = comp_we['Li'] / nfu_fw

        return cls(
            entry_electrode=entry_we,
            working_ion=working_ion,
            rcomp_electrode=rcomp_we,
            rcomp_framework=rcomp_fw,
            nfu_electrode=nfu_we,
            nfu_framework=nfu_fw,
            mass_electrode=mass_we,
            mass_framework=mass_fw,
        )

    def __repr__(self):
        output = [
            f"{'formula_electrode':20s} = {self.rcomp_electrode.reduced_formula} / {self.rcomp_framework.reduced_formula}",
            f"{'mass_electrode':20s} = {self.mass_electrode} / {self.mass_framework}",
        ]
        return "\n".join(output)



class HalfCellCharger():
    """
    Battery: Electrode materials | Li metal anode
    Charging - Deintercalation, Removal, Extraction, Moving out
    """

    def __init__(self,
        electrode: ComputedStructureEntry,
        working_ion: str
    ):
        self.entry = electrode
        self.seed = self.entry.data.get('seed')
        self.structure = self.entry.structure
        self.working_ion = working_ion
        self.framework = self.structure.copy()
        self.framework.remove_species([working_ion])
        self.x = self.structure.composition[working_ion] / self.framework.composition.get_reduced_composition_and_factor()[1]
        print("-"*100)
        print(self.entry)
        print("-"*100)
        print(self.structure)
        print("framework" + "-"*100)
        print(self.framework)
        print("-"*100)

    def __str__(self):
        output = [
            f"electrode : {self.entry.composition.reduced_formula}",
            f"framework : {self.framework.composition.reduced_formula}",
            f"x : {self.x}",
            f"working ion : {self.working_ion}",
            f"seed : {self.seed}"
        ]
        return "\n".join(output)


    def generate(self, n=2):
        from itertools import combinations
        import copy
        from pymatgen.entries.computed_entries import ComputedStructureEntry
        from bsym.interface.pymatgen import unique_structure_substitutions

        matrix = [[n, 0, 0], [0, n, 0], [0, 0, n]]

        elec = self.structure.make_supercell(matrix)
        fw = elec.copy()
        fw.remove_species([self.working_ion])
        nfu_fw = fw.composition.get_reduced_composition_and_factor()[1]

        ion_indices = [i for i, site in enumerate(elec)
                     if site.species_string == self.working_ion]
        nions = len(ion_indices)

        entries = []

        counter = 0
        cnt = 0
        for nextract in range(nions + 1):
            for i, indices in enumerate(combinations(ion_indices, nextract)):
                counter += 1
                cnt += 1

            d = {'Na': nextract, 'Li': nions-nextract}
            print(d)
            unique_structures = unique_structure_substitutions(
                elec,
                'Li',
                d,
                atol = 0.001
            )
            print(f"{nextract:10d} : {cnt} {len(unique_structures)}")
            cnt =0
        print("The number of structuers", counter)

        for nextract in range(nions + 1):
            x_elec = (nions - nextract) / nfu_fw
            ion_ppm = int(x_elec * 1000000)
            print("-"*100)
            print(f"number of ios to extract: {nextract} out of {nions}")
            print(f"Li contect: {x_elec} % {ion_ppm} ppm)")
            print("-"*100)
            for i, indices in enumerate(combinations(ion_indices, nextract)):
                elec_charge = elec.copy()
                elec_charge.remove_sites(indices=indices)
                entry = ComputedStructureEntry(
                    structure=elec_charge,
                    energy=0,
                    data={
                        'seed': f"{self.seed}-{ion_ppm:09d}-{i+1}",
                        'pressure': 0,
                        'isd': 0,
                        'iasd': 0
                    }
                )
                entries.append(entry)

        for entry in entries:
            print(entry)




res = Res.from_file('mp-865631-R2SCAN.res')
print(res.entry)
#
#e = Electrode.from_entry(res.entry, 'Li')
#print(e)

charger = HalfCellCharger(res.structure, 'Li')
print(charger)
charger.generate(n=2)
