# Get all materials containing *at least* a set of elements

This examples describes how to get data for materials containing _at least_ a
list of elements from the Materials Project database.

For example:

- all Li-containing materials (Li + α)
- all materials containing earth abundant O and Si (O + Si + α)


## Download entries

---

`get_entries()` makes ComputedStructureEntry using ThermoDoc downloded from
`materials.thermo` endpoint.

Therefore, as shown in the ThermoDoc example, two steps are involved to get all
materials containing a set of elements.

First, a list of chemsys should be generated from materials.summary endpoint
and then be used as input to materials.chemsys endpoint as follows:

``` python
docs = mpr.materials.summary.search(
    elements=elements,
    fields=["chemsys"]
)

chemsys = [doc.chemsys for doc in docs]
chemsys = list(dict.fromkeys(chemsys))

entries = mpr.get_entries(
    chemsys_formula_mpids=chemsys,
)
```


### Examples

``` python
docs = mpr.materials.summary.search(
    elements=["Li"],
    fields=["chemsys"]
)

chemsys = [doc.chemsys for doc in docs]
chemsys = list(dict.fromkeys(chemsys))

entries = mpr.get_entries(
    chemsys_formula_mpids=chemsys,
    property_data=["chemsys","nelements"]
)
```

This returns 21686 SummaryDoc and 45197 StructureComputedEntry with 3372 unique
chemsys and 1-8 elements.


``` python
docs = mpr.materials.summary.search(
    elements=["Li", "Ni", "O"],
    fields=["chemsys"]
)

chemsys = [doc.chemsys for doc in docs]
chemsys = list(dict.fromkeys(chemsys))

docs = mpr.get_entries(
    chemsys=chemsys,
    property_data=["chemsys","nelements"]
)
```

This returns 1394 SummaryDoc and 2828 StructureComputedEntry with 147 unique
chemsys and 3-6 elements.
