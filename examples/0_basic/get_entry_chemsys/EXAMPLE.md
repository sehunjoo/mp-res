# Get all materials containing **only** a set of elements

This examples describes how to get data for materials containing _only_ a
list of elements from the Materials Project database.

For example:

- all Li-Ni-O ternary compounds (Li + Ni + O)
- all elemental, binary, ternary compounds in Li-Ni-O chemical system.


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

This returns a list of ComputedStructureEntry for all materials containing
only Li, Ni, and O elements from the Materials Project database.

!!! info "Order of elements in a hyphenated list of chemsys"
    Elements can be listed in any order. For example, Li-Ni-O, O-Li-Ni, and
    Ni-O-Li are all considered same.

``` python
entries = mpr.get_entries(
    chemsys_formula_mpids=["Li-Ni-O"]
    property_data=["chemsys", "nelements"]
)
```

If you specify `property_data`, `entry.data` includes additional properties.
This returns a list of ComputedStructureEntry for all materials containing
only Li, Ni, and O elements from the Materials Project database. It returns a
total of 311 entries with 1 unique chemsys and 3 elements.

``` python
entries = mpr.get_entries(
    chemsys_formula_mpids=["Li", "Ni", "O", "Li-Ni", "Li-O", "Ni-O", "Li-Ni-O"],
    property_data=["chemsys", "nelements"]
)
```

This returns a list of ComputedStructureEntry for all elementa, binary, and
ternary materials containing Li, Ni, or O elements from the Materials Project
database. It returns a total of 526 entries with 7 unique chemsys and 1-3
elements.


``` python
entries = mpr.get_entries(
    chemsys_formula_mpids=["Li", "Ni", "O", "Li-Ni", "Li-O", "Ni-O", "Li-Ni-O"],
    property_data=["chemsys", "nelements"],
    additional_criteria={"is_stable": True}
)

```
If you specify `additional_criteria` with `{"is_stable": True}`, only the
materials on the convex hull are downloaded.
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
    


