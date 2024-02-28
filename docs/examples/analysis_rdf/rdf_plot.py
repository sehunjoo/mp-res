import numpy as np
import matplotlib.pyplot as plt

# Reading the data

r = np.loadtxt("rdf_r.txt", dtype=float)
rdfs = np.loadtxt("rdf_rdfs.txt", dtype=float)

rdf_avg = np.mean(rdfs, axis=0)



fig, axes = plt.subplots(2,1, figsize=(4, 6))

axes[0].set_xlim(0, np.max(r))
axes[0].set_ylim(0, 50)
axes[0].set_xlabel('r[Angstrom]')
axes[0].set_ylabel('g(r)')

for rdf in rdfs:
    axes[0].plot(r, rdf,
        color='gray',
        alpha=0.005
    )



bar_width = r[1] - r[0]
axes[1].bar(r, rdf_avg,
    width=bar_width,
    align='center',
    color='black'
)

axes[1].set_xlim(0, np.max(r))
axes[1].set_xlabel('r[Angstrom]')
axes[1].set_ylabel('g(r)')

plt.tight_layout()
plt.show()


