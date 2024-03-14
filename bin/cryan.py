#!/usr/bin/env python

import os
import numpy as np
import matplotlib.pyplot as plt

from ase import Atoms
from ase.build import make_supercell
from ase.ga.utilities import get_rdf

from concurrent.futures import ProcessPoolExecutor


class CryanAtoms():

    def __init__(self, structures: list[Atoms]):
        self.structures = structures
        self.add_info_init()

    def __str__(self):
        lines = [
            f"{st.info.get('name'):<20}"
            f" {st.info.get('pressure'):>8.2f}"
            f" {st.info.get('volume')/st.info.get('nfu'):>9.3f}"
            f" {st.info.get('energy')/st.info.get('nfu'):>11.3f}"
            f" {st.info.get('nfu'):4d}"
            f" {st.info.get('formula'):15s}"
            f" {st.info.get('spacegroup'):<10}"
            for st in self.structures
        ]
        sorted_lines = sorted(
            lines,
            key=lambda line: (len(line.split()[5]), line.split()[5], -float(line.split()[3]))
        )
        return "\n".join(sorted_lines)

    def to_str_per_atom(self):
        lines = [
            f"{st.info.get('name'):<20}"
            f" {st.info.get('pressure'):>8.2f}"
            f" {st.info.get('volume')/st.info.get('natoms'):>9.3f}"
            f" {st.info.get('energy')/st.info.get('natoms'):>11.3f}"
            f" {st.info.get('natoms'):4d}"
            f" {st.info.get('formula'):15s}"
            f" {st.info.get('spacegroup'):<10}"
            for st in self.structures
        ]
        sorted_lines = sorted(
            lines,
            key=lambda line: (len(line.split()[5]), line.split()[5], -float(line.split()[3]))
            #key=lambda line: (float(line.split()[2]))
        )
        return "\n".join(sorted_lines)

    def add_info_init(self):
        for st in self.structures:
            # volume
            st.info['volume'] = st.get_volume()
            # formula
            fu, nfu = st.symbols.formula.convert('hill').reduce()
            st.info['formula'] = str(fu)
            st.info['nfu'] = nfu
            # others
            st.info['natoms'] = len(st)
            st.info['nelements'] = len(set(st.get_chemical_symbols()))

    def add_info_volume(self):
        for st in self.structures:
            st.info['volume'] = st.get_volume()

    def add_info_formula(self):
        for st in self.structures:
            fu, nfu = st.symbols.formula.convert('hill').reduce()
            st.info['formula'] = str(fu)
            st.info['nfu'] = nfu

    def add_info_nelements(self):
        for st in self.structures:
            st.info['nelements'] = len(set(st.get_chemical_symbols()))

    def nstructures(self):
        return len(self.structures)

    def ncompositions(self):
        return len({st.info.get('formula') for st in self.structures})

    def summary(self):
        return "\n".join([
            f"Number of structures   : {self.nstructures():6}",
            f"Number of compositions : {self.ncompositions():6}"
        ])


    def calc_vol(self):

        vol = {}
        vol_str = []

        for key in ['all', 'element', 'compound']:
            vol[key] = []

        for st in self.structures:
            volume = st.info.get('volume') / st.info.get('natoms')

            vol['all'].append(volume)
            if st.info.get('nelements') == 1:
                vol['element'].append(volume)
            else:
                vol['compound'].append(volume)

        for k, v in vol.items():

            array = np.array(v)
            stat = {
                'array': array,
                'min': np.min(array),
                'max': np.max(array),
                'mean': np.mean(array),
                'median': np.median(array),
            }
            if k == 'all':
                bin_width = 0.5
                nbins = np.ceil((stat['max'] - stat['min']) / bin_width).astype(int)
                bins = np.arange(stat['min'], stat['max'] + bin_width, bin_width)

            vol_str.append(
                f"{k:10s}: {stat['min']:6.2f}-{stat['max']:.2f}"
                + f"  (mean = {stat['mean']:6.2f}, median = {stat['median']:6.2f})"
            )

        # write data file

        with open('cryan_vol.txt', 'w') as f:
            f.write("\n".join(vol_str) + "\n")


        # Plot

        plt.rcParams['figure.dpi'] = 300

        aspect_ratio = 4/3 
        width = 4
        height = width / aspect_ratio

        # Figure 1

        fig, ax = plt.subplots(1, 1, figsize=(width, height))

        ax.hist(vol['all'], bins=bins, rwidth=0.85, color='gray')
        ax.set_xlabel(r'Volume (Å$^{3}$/atom)')
        ax.set_ylabel('Frequency')

        plt.tight_layout()
        fig.savefig('cryan_vol_all.png', dpi=300, bbox_inches='tight')

        # Figure 2

        fig, axs = plt.subplots(2, 1, figsize=(width, height))

        for i, k in enumerate(['element','compound']):
            axs[i].hist(vol[k], bins=bins, rwidth=0.85, color='gray', label=k)
            axs[i].set_xlabel(r'Volume (Å$^{3}$/atom)')
            axs[i].set_ylabel('Frequency')
            axs[i].legend(frameon=False, loc='upper right')

        plt.tight_layout()
        fig.savefig('cryan_vol_cmp.png', dpi=300, bbox_inches='tight')

        plt.show()



    def _calc_rdf(self, st, rcut, nbins, filename_x, filename_y):

        cell = st.get_cell()
        vol = st.get_volume()
        h = [vol / np.linalg.norm(np.cross(cell[(i + 1) % 3], cell[(i + 2) % 3])) for i in range(3)]
        supercell_nn = [max(1, int(np.ceil(rcut / (hi / 2)))) for hi in h]
        supercell_matrix = np.diag(supercell_nn)
        supercell = make_supercell(st, supercell_matrix)

        rdf, r = get_rdf(
            atoms=supercell,
            rmax=rcut,
            nbins=nbins,
            distance_matrix=None,
            elements=None,
            no_dists=False
        )
        if not os.path.exists(filename_x):
            with open(filename_x, 'w') as f:
                np.savetxt(f, r[np.newaxis], fmt="%f")

        with open(filename_y, 'ab') as f:
                np.savetxt(f, rdf[np.newaxis], fmt="%f")


    def calc_rdf(self, rcut=7, nbins=140, mpinp=4):

        filename_x = 'cryan_rdf_x.txt'
        filename_y = 'cryan_rdf_y.txt'

        if os.path.exists(filename_x):
            os.remove(filename_x)
        if os.path.exists(filename_y):
            os.remove(filename_y)

        os.nice(19)


        with ProcessPoolExecutor(max_workers=mpinp) as executor:
            futures = [executor.submit(self._calc_rdf, st, rcut, nbins, filename_x, filename_y) 
                       for st in self.structures]
            # Ensure all futures are executed.
            for future in futures:
                future.result()  # Wait for each future to finish.


    def plot_rdf(self):

        import matplotlib.pyplot as plt
        import numpy as np
        
        r = np.loadtxt('cryan_rdf_x.txt')
        rdfs = np.loadtxt('cryan_rdf_y.txt')
        rdfs_avg = np.mean(rdfs, axis=0)

        rdfs_max = np.max(rdfs, axis=1)

        xmax = np.ceil(np.max(r))
        ymax_rdfs = (np.mean(rdfs_max) + np.max(rdfs_max))/2
        ymax_rdfs_avg = np.max(rdfs_avg) * 1.2

        # default setting

        plt.rcParams['figure.dpi'] = 300
        aspect_ratio = 4/3 
        width = 4
        height = width / aspect_ratio * 2 / 2

        fig, axes = plt.subplots(2, 1, figsize=(width, height))
        
        axes[0].set_xlim(0, xmax)
        axes[0].set_ylim(0, ymax_rdfs)
        axes[0].set_xlabel('r (Å)')
        axes[0].set_ylabel('RDF')
        axes[0].grid(True, linestyle='dotted', alpha=0.7, axis='x', color='dimgray')
        
        for rdf in rdfs:
            axes[0].plot(r, rdf,
                color='dimgray',
                alpha=0.03
            )

        axes[1].set_xlim(0, xmax)
        axes[1].set_ylim(0, ymax_rdfs_avg)
        axes[1].set_xlabel('r (Å)')
        axes[1].set_ylabel('RDF')
        axes[1].grid(True, linestyle='dotted', alpha=0.7, axis='x', color='dimgray')

        bar_width = r[1] - r[0]
        axes[1].bar(r, rdfs_avg,
            width=bar_width,
            align='center',
            color='black'
        )
        

        plt.tight_layout()
        fig.savefig('cryan_rdf.png', dpi=300, bbox_inches='tight')
        
        plt.show()
