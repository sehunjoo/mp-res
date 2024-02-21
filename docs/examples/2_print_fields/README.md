# getting data

This examples describes how to get data for materials containing _at least_ a
list of elements. For example, get data for all Li-containing materials in
the Materials Project database.

## materials.summary

``` python
mpr.materials.summary.search(elements=elements)
```

For example,

``` python
mpr.materials.summary.search(elements=["Li"])
```

This will give SummaryDoc for all Li-containing materials. You will get 21686
materials with 1-8 elements.

``` python
mpr.materials.summary.search(elements=["Li", "Ni", "O"])
```

## materials.thermo

This will give SummaryDoc for all materials contatining at least Li, Ni, O,
elements. You will get 1394 materials with 3-6 elements.

!!! note "Note"
    `mpr.materials.thermo.search` do not support this functionality. It only
    support chemsys and materials_id. So you should generate a list of chemsys
    or materials_ids using `mpr.materials.summary.search`.
    For more information, please see [thermo.py](https://github.com/materialsproject/api/blob/main/mp_api/client/routes/materials/thermo.py)




!!! warning "Long list of material/moldcule IDs"

    When you try to get a list of `materials_id` from the `materials.summary`
    end point and use it as input to the `materials.thermo` end point, you can
    get the following error: 

    ```
    ValueError: List of material/molecule IDs provided is too long. Consider
    removing the ID filter to automatically pull data for all IDs and filter
    locally.
    ```


!!! warning "wild cards for chemsys"

    The wild cards in chemsys doens't seem to work as what I expect. The number
    of docs are different from the one obatained as above.

    ```
    docs = mpr.materials.thermo.search(                                                                                 
        chemsys=["Li-*", "*-Li-*", "*-Li", "Li"],                                                                       
        fields=fields                                                                                                   
    )
    ```
