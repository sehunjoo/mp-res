# Get all materials containing **only** a set of elements

This examples describes how to get data for materials containing _only_ a
list of elements from the Materials Project database.

For example:

- all Li-Ni-O ternary compounds (Li + Ni + O)
- all elemental, binary, ternary compounds in Li-Ni-O chemical system.


## **get_entries()** function

---

``` python
entries = mpr.get_entries(
    chemsys_formula_mpids
    compatible_only=True,
    property_data=None,
    conventional_unit_cell=False,
    additional_criteria=None,
)
```

??? info "Arguments"
    chemsys_formula_mpids (str, List[str]): A chemical system, list of chemical
systems
        (e.g., Li-Fe-O, Si-*, [Si-O, Li-Fe-P]), formula, list of formulas
        (e.g., Fe2O3, Si*, [SiO2, BiFeO3]), Materials Project ID, or list of
Materials
        Project IDs (e.g., mp-22526, [mp-22526, mp-149]).
    compatible_only (bool): Whether to return only "compatible"
        entries. Compatible entries are entries that have been
        processed using the MaterialsProject2020Compatibility class,
        which performs adjustments to allow mixing of GGA and GGA+U
        calculations for more accurate phase diagrams and reaction
        energies. This data is obtained from the core "thermo" API endpoint.
    property_data (list): Specify additional properties to include in
        entry.data. If None, only default data is included. Should be a subset
of
        input parameters in the 'MPRester.thermo.available_fields' list.
    conventional_unit_cell (bool): Whether to get the standard
        conventional unit cell
    additional_criteria (dict): Any additional criteria to pass. The keys and
values should
        correspond to proper function inputs to `MPRester.thermo.search`. For
instance,
        if you are only interested in entries on the convex hull, you could pass
        {"energy_above_hull": (0.0, 0.0)} or {"is_stable": True}.



You can get a list of ComputedStructureEntry for all materials containing only a
hyphenated list of elements specified to the `chemsys` argument, as follows:

``` python
entries = mpr.get_entries(
    chemsys_formula_mpids=chemsys
)
```

### Examples

``` python
entries = mpr.get_entries(
    chemsys_formula_mpids=["Li-Ni-O"]
)
```

If you specify `property_data`, `entry.data` includes additional properties.

``` python
entries = mpr.get_entries(
    chemsys_formula_mpids=["Li-Ni-O"]
    property_data=["chemsys", "nelements"]
)
```
This returns a list of ThermoDoc for all materials containing only Li, Ni, and
O elements from the Materials Project database. It returns a total of 311
ThermoDoc with 1 unique chemsys and 3 elements.

!!! info Order in hyphenated list of elements
    Elements can be listed in any order. For example, Li-Ni-O, O-Li-Ni, and
    Ni-O-Li are all considered equal.


``` python
entries = mpr.get_entries(
    chemsys_formula_mpids=["Li", "Ni", "O", "Li-Ni", "Li-O", "Ni-O", "Li-Ni-O"],
    property_data=["chemsys", "nelements"]
)
```

This returns a list of ThermoDoc for all elementa, binary, and ternary
materials containing Li, Ni, or O elements from the Materials Project database.
It returns a total of 526 ThermoDoc with 7 unique chemsys and 1-3 elements.


``` python
entries = mpr.get_entries(
    chemsys_formula_mpids=["Li", "Ni", "O", "Li-Ni", "Li-O", "Ni-O", "Li-Ni-O"],
    property_data=["chemsys", "nelements"],
    additional_criteria={"is_stable": True}
)

```
This returns a list of ThermoDoc for all elementa, binary, and ternary
materials containing Li, Ni, or O elements from the Materials Project database.
It returns a total of 36 ThermoDoc with 6 unique chemsys and 1-3 elements.

info tip "Thermodynamically stable structures"
    If you are interested in the materials on the convex hull,

    ``` python
    additional_criteria={"is_stable": True}
    or
    additional_criteria={"energy_above_hull": (0.0, 0.0)}
    ```

    If you are interested in stable/metastable materials within 0.1 eV/atom of the hull

    ``` python
    additional_criteria={"energy_above_hull": (0.0, 0.1)}
    ```
    


