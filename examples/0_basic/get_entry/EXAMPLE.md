# Retrieve materials project data as ComputedStructureEntry

!!! note "Note"
    This is a useful section for anyone who only wants to get data calculated
    with a specific functional from Materials Project database and save it as
    files in res format with or without energy correction.

In the Materials Project databsae, each unique material is given a **Material
ID** (also referred to in various places as mp-id, mpid, MPID). This allows a
specific polymorph of a given mterial to be referenced.

All of the infromation for a given material ID is actually a combination of
data generated from many individual calcualtions or tasks. An identifier
referring to an individual calculation task are known as **Task ID**. For
example, DFT caluclations with different functionals have different task ID.

Therefore, a unique material have a material ID and a collection of multiple
different task IDs associated with it. For more information, please see
[FAQ](https://docs.materialsproject.org/frequently-asked-questions).

Each set of paramters and data for different tasks of a given material can be
downloaded through **materials.thermo** endpoint. The data can be downloded in
**ComputedStructureEntry** format that can be easily converted to files in **res
format** as used by AIRSS. The
[MPRester.get_entries()](https://github.com/materialsproject/api/blob/main/mp_api/client/mprester.py#L661) function does this.



## **What is ComputedStructureEntry?**

---

Entry is an container for calculated information. ComputedStructuerEntry is a
object containing the energy associated a specific chemical composition,
paramaters associated with this entry, and any additional data associated with
this entry.

!!! abstract "Example: ComputedStructureEntry of mp-135"
    ```
    print(entry)
    ```
    ```
    mp-135-GGA ComputedStructureEntry - Li1          (Li)
    Energy (Uncorrected)     = -1.9038   eV (-1.9038  eV/atom)
    Correction               = 0.0000    eV (0.0000   eV/atom)
    Energy (Final)           = -1.9038   eV (-1.9038  eV/atom)
    Energy Adjustments:
      None
    Parameters:
      potcar_spec            = [{'titel': 'PAW_PBE Li_sv 23Jan2001', 'hash': '4799bab014a83a07c654d7196c8ecfa9'}]
      is_hubbard             = False
      hubbards               = {}
      run_type               = GGA
    Data:
      oxide_type             = None
      aspherical             = True
      last_updated           = 2020-05-02 23:41:40.352000
      task_id                = mp-1440853
      material_id            = mp-135
      oxidation_states       = {}
      run_type               = GGA
    ```

Please refer to Entry, ComputedEntry, and ComputedStructureEntry classes in
[pymatgen.entries package](https://pymatgen.org/pymatgen.entries.html) for
further details.

??? info "How to get the information held by the ComputedStructureEntry"
    We can get access the values or data by
    ```
    entry.entry_id
    entry.composition
    entry.elements
    entry.uncorrected_energy
    entry.uncorrected_energy_per_atom
    entry.conrrection
    entry.correction_per_atom
    entry.energy
    entry.energy_per_atom
    entry.parameters
    entry.data
    entry.structure
    ```
    Type of return value
    ```
    entry_id                    : <class 'str'>
    composition                 : <class 'pymatgen.core.composition.Composition'>
    elements:                   : <class 'list'>
    energy                      : <class 'float'>
    energy_per_atom             : <class 'float'>
    uncorrected_energy          : <class 'float'>
    uncorrected_energy_per_atom : <class 'float'>
    parameters                  : <class 'dict'>
    data                        : <class 'dict'>
    ```



## **Get entries from the MP database**

---

**mpr.get_entries()** function returns a list of ComputedStructureEntry

```
entries = mpr.get_entries(
    chemsys_formula_mpids=chemsys
)
```

??? info "Arguments to the get_entries() function"

    ```
    entries = mpr.get_entries(
        chemsys_formula_mpids
        compatible_only=True,
        property_data=None,
        conventional_unit_cell=False,
        additional_criteria=None,
    )
    ```

    - chemsys_formula_mpids (str, List[str]):
        A chemical system, list of chemical systems
        (e.g., Li-Fe-O, Si-*, [Si-O, Li-Fe-P]),
        formula, list of formulas
        (e.g., Fe2O3, Si*, [SiO2, BiFeO3]),
        Materials Project ID, or list of Materials Project IDs
        (e.g., mp-22526, [mp-22526, mp-149]).
    - compatible_only (bool): Whether to return only "compatible"
        entries. Compatible entries are entries that have been
        processed using the MaterialsProject2020Compatibility class,
        which performs adjustments to allow mixing of GGA and GGA+U
        calculations for more accurate phase diagrams and reaction
        energies. This data is obtained from the core "thermo" API endpoint.
    - property_data (list): Specify additional properties to include in
        entry.data. If None, only default data is included. Should be a subset of
        input parameters in the 'MPRester.thermo.available_fields' list.
    - conventional_unit_cell (bool): Whether to get the standard
        conventional unit cell
    - additional_criteria (dict): Any additional criteria to pass. The keys and
        values should correspond to proper function inputs to
        `MPRester.thermo.search`. For instance, if you are only interested in
        entries on the convex hull, you could pass
        {"energy_above_hull": (0.0, 0.0)} or {"is_stable": True}.

    There are more functions to get entries, but they are high-level functions
    based on `get_entries()`.

    ```
    entries = mpr.get_entries_in_chemsys(elements=["Li", "Ni", "O"])
    entries = mpr.get_entry_by_material_id(material_id="mp-135")
    ```

### Example - get entries

```
entries = mpr.get_entries(
    chemsys_formula_mpids=["Li"]
)

for i, entry in enumerate(entries):
    print(f"\nEntry {i+1}\n")
    print(entry)
```

This returns a list of StructureComputesEntry for all materials containing only
Li element.

- 25 StructureComputesEntry
- 9 unique material IDs
- 16 unique task IDs
- 2 unique run type : GGA, R2SCAN

### Example - get entries selectively

```
entries = mpr.get_entries(
    chemsys_formula_mpids=["Li"],
    property_data=["chemsys", "nelements", "thermo_type"]
)

for i, entry in enumerate(entries):
    print(f"\nEntry {i+1}\n")
    print(entry)
```

If you specify property_data, entry.data includes additional properties. This
returns a list of StructureComputedEntry for all binary materials containing
only Li and O elements.

- 25 ComputedStructureEntry
- 9 unique material IDs
- 16 unique task IDs
- 2 unique run_type: GGA, R2SCAN
- 1 unique chemsys: Li
- 1 unique nelements: 1


```
entries = mpr.get_entries(
    chemsys_formula_mpids=["Li"],
    property_data=["chemsys", "nelements", "thermo_type"],
    additional_criteria={"is_stable": True}
)

for i, entry in enumerate(entries):
    print(f"\nEntry {i+1}\n")
    print(entry)
```

If you specify additional_criteria with {"is_stable": True}, only the materials
on the convex hull are downloaded. This returns a list of ComputedStructureEntry
for all ternary materials containing only Li-Ni-O elements.

- 3 ComputedStructureEntry
- 1 unique material IDs
- 2 unique task IDs
- 2 unique run_type: GGA, R2SCAN
- 1 unique chemsys: Li
- 1 unique nelements: 1



???+ note "Note"
    There are multiple entries for a single material_id.
    Even for the same_material_id, task_id, run_type, there can be multiple entries.
    Each with different _thermo_type.
    ```
    material_id  task_id      run_type  thermo_type       chemsys       uncorrected_energy  correction    corrected_energy
    mp-1960      mp-1440823   GGA       GGA_GGA+U         Li-O                  -14.263600   -0.687000          -14.950600
    mp-1960      mp-1949896   R2SCAN    R2SCAN            Li-O                  -16.826560    0.000000          -16.826560
    mp-1960      mp-1949896   R2SCAN    GGA_GGA+U_R2SCAN  Li-O                  -16.826560    1.875960          -14.950600
    ```




