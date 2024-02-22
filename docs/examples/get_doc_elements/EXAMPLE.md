# Get all materials containing *at least* a set of elements

This examples describes how to get data for materials containing _at least_ a
list of elements from the Materials Project database.

For example:

- all Li-containing materials (Li + α)
- all materials containing earth abundant O and Si (O + Si + α)


## **materials.summary** endpoint

---

You can get a list of SummaryDoc for all materials containing at least a list
of elements specified to the `elements` argument, as follows:

``` python
docs = mpr.materials.summary.search(
    elements=elements
)
```

### Examples

``` python
docs = mpr.materials.summary.search(
    elements=["Li"]
)
```

The above returns a list of SummaryDoc for all Li-contatining materials from the
Materials Project database. It returns a total of 21686 SummaryDoc with 3372
unique chemsys and 1-8 elements.

``` python
docs = mpr.materials.summary.search(
    elements=["Li", "Ni", "O"]
)
```

This returns a list of SummaryDoc for all materials containing at least Li, Ni,
and O elements from the Materials Project database. It returns a total of 1394
SummaryDoc with 147 unique chemsys and 3-6 elements.


## **materials.thermo** endpoint

---

From the materials.thermo endpoint, you can't get a list of ThermoDoc for all
materials containing a set of elements. materials.thermo do not support
`elements` arguments. `materials_id` and `chemsys` are only available.
For more information, please see [thermo.py](https://github.com/materialsproject/api/blob/main/mp_api/client/routes/materials/thermo.py)

Therefore, a list of chemsys should be generated from materials.summary endpoint
and then be used as input to materials.chemsys endpoint as follows:

``` python

docs = mpr.materials.summary.search(
    elements=elements,
    fields=["chemsys"]
)

chemsys = [doc.chemsys for doc in docs]
chemsys = list(dict.fromkeys(chemsys))

docs = mpr.materials.thermo.search(
    chemsys=chemsys,
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

docs = mpr.materials.thermo.search(
    chemsys=chemsys,
)
```

This returns a total of 45197 ThermoDoc with 3372 unique chemsys and 1-8
elements.

``` python
docs = mpr.materials.summary.search(
    elements=["Li", "Ni", "O"],
    fields=["chemsys"]
)

chemsys = [doc.chemsys for doc in docs]
chemsys = list(dict.fromkeys(chemsys))

docs = mpr.materials.thermo.search(
    chemsys=chemsys,
)
```

This returns a total of 2828 ThermoDoc with 147 unique chemsys and 3-6
elements.






!!! warning "Long list of material/moldcule IDs"

    When you try to get a list of `materials_id` from the `materials.summary`
    endpoint and use it as input to the `materials.thermo` endpoint, you can
    get the following error:

    ``` python
    elements=["Li"]
    fields=["nelements", "chemsys"]

    docs = mpr.materials.summary.search(
        elements=elements,
        fields=["material_id"]
    )

    material_ids = [doc.material_id for doc in docs]

    docs = mpr.materials.thermo.search(
        material_ids=material_ids,
        fields=fields
    )
    ```

    ```
    ValueError: List of material/molecule IDs provided is too long. Consider
    removing the ID filter to automatically pull data for all IDs and filter
    locally.
    ```

    I would recommend getting a list of `chemsys` instead of `materials_id`.



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
