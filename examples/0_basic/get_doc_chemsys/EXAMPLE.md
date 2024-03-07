# Get all materials containing **only** a set of elements

This examples describes how to get data for materials containing _only_ a
list of elements from the Materials Project database.

For example:

- all Li-Ni-O ternary compounds (Li + Ni + O)
- all elemental, binary, ternary compounds in Li-Ni-O chemical system.


## **materials.summary** endpoint

---

You can get a list of SummaryDoc for all materials containing only a hyphenated
list of elements specified to the `chemsys` argument, as follows:

``` python
docs = mpr.materials.summary.search(
    chemsys=chemsys
)
```

!!! info Order in hyphenated list of elements
    Elements can be listed in any order. For example, Li-Ni-O, O-Li-Ni, and
    Ni-O-Li are all considered equal.


### Examples

``` python
docs = mpr.materials.summary.search(
    chemsys=["Li-Ni-O"]
)
```

This returns a list of SummaryDoc for all materials containing only Li, Ni, and
O elements from the Materials Project database. It returns a total of 142
SummaryDoc with 1 unique chemsys and 3 elements.


``` python
docs = mpr.materials.summary.search(
    chemsys=["Li", "Ni", O", "Li-Ni", "Li-O", "Ni-O", "Li-Ni-O"]
)
```

This returns a list of SummaryDoc for all elementa, binary, and ternary
materials containing Li, Ni, or O elements from the Materials Project database.
It returns a total of 240 SummaryDoc with 7 unique chemsys and 1-3 elements.

!!! tip "Generating all combinatorial chemsys"

    All combinatorial chemical systems can be easily generated using itertools

    ```
    chemsys = []                                                                                                        
    for i in range(len(elements)):                                                                                  
        for els in itertools.combinations(elements, i + 1):                                                         
            chemsys.append("-".join(sorted(els)))                                                                   
    ```


## **materials.thermo** endpoint

---

You can get a list of ThermoDoc for all materials containing only a hyphenated
list of elements specified to the `chemsys` argument, as follows:

``` python
docs = mpr.materials.thermo.search(
    chemsys=chemsys
)
```

!!! info Order in hyphenated list of elements
    Elements can be listed in any order. For example, Li-Ni-O, O-Li-Ni, and
    Ni-O-Li are all considered equal.

### Examples

``` python
docs = mpr.materials.thermo.search(
    chemsys=["Li-Ni-O"]
)
```

This returns a list of ThermoDoc for all materials containing only Li, Ni, and
O elements from the Materials Project database. It returns a total of 311
ThermoDoc with 1 unique chemsys and 3 elements.


``` python
docs = mpr.materials.thermo.search(
    chemsys=["Li", "Ni", O", "Li-Ni", "Li-O", "Ni-O", "Li-Ni-O"]
)
```

This returns a list of ThermoDoc for all elementa, binary, and ternary
materials containing Li, Ni, or O elements from the Materials Project database.
It returns a total of 526 ThermoDoc with 7 unique chemsys and 1-3 elements.


!!! warning "Wild cards in chemsys"

    wild cards in chemsys don't seem to work as expected.
    Each `*` just replace on element in a chemsys. For example:

    ```
    docs = mpr.materials.thermo.search(
        chemsys=['Li-*', '*-Li']
    )
    ```

    gives only binary Li-containing compounds.

    ```
    docs = mpr.materials.thermo.search(
        chemsys=['Li-*-*', '*-Li-*', '*-*-Li']
    )
    ```

    gives only ternary Li-containing compounds.

    I would recommend getting a list of `chemsys` from the `materials.summary`
    endpoint.
