# Check list of available fields (data) for each Endpoint or Document Model

A list of avaialble fields (properties) can be obtained from the MPRester.

```
available_fields = mpr.[endpoint].available_fields
```

The `available_fields` property for APIs is meant to refer to
the data available from the endpoint.

For example:

```
available_fields = mpr.materials.summary.available_fields
available_feilds = mpr.materials.thermo.available_fields

!!! note "Note"
    The available fields are not necessarily which fields you can use to query
    that data with via `search()`. See the API-specific search() kwargs for
    details on which parameters can be used for filtering queries.


