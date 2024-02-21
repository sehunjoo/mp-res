# Retrieve materials project data as ComputedStructureEntry


## What is ComputedStructureEntry?

---

Entries are containers for calculated information in pymatgen.
Please refer to `Entry`, `ComputedEntry`, `ComputedStructureEntry` classes in
[pymatgen.entries package](https://pymatgen.org/pymatgen.entries.html) for
further details.

!!! info "mp-135"
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

!!! info "Inforamtion that ComputedStructureEntry has"
    We can get access the values or data by 
    ```
    entry.entry_id
    entry.composition
    entry.elements
    entry.energy
    entry.energy_per_atom
    entry.uncorrected_energy
    entry.uncorrected_energy_per_atom
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


## How to get data as ComputedStructureEntry from Materials Project

---

### Download data

`mpr.get_entries()` return a list of computed entries

``` python
entries = mpr.get_entries("Li")

print(type(entries))

for entry in entries:
    print(type(entry))
```

Tye type of entries is `<class 'list'>`.
The type of each entry in the list is `<class 'pymatgen.entries.computed_entries.ComputedStructureEntry'>`

There are more functions to get entries, but they are high-level functions
based on `get_entries()`.

``` python
entries = mpr.get_entries_in_chemsys(elements=["Li", "Ni", "O"])
entries = mpr.get_entry_by_material_id(material_id="mp-135")


``` python
entries = mpr.get_entries("Li")

for entry in entries:
    print("-"*100)
    print(type(entry))
    print("-"*100)
```

```

You can get properties from 

### Save to RES files

``` python
for entry in entries:                                                                                               
                                                                                                                    
    material_id = entry.data.get("material_id", "mp-")                                                              
    task_id = entry.data.get("task_id", "mp-")                                                                      
    run_type = entry.data.get("run_type", "")                                                                       
                                                                                                                    
    seed = f"{material_id}-{run_type}-{task_id}"                                                                    
    rems = [                                                                                                        
            f"",                                                                                                    
            f'Downloaded from the Materials Project database',                                                      
            f"",                                                                                                    
            f"Energy (Uncorrected)     = {entry.uncorrected_energy:<16.8f} eV",                                     
            f"Correction               = {entry.correction:<16.8f} eV",                                             
            f"Energy (Final)           = {entry.energy:<16.8f} eV",                                                 
            f"",                                                                                                    
            f"material_id              = {material_id}",                                                            
            f"run_type                 = {run_type}",                                                               
            f"task_id                  = {task_id}",                                                                
            f""                                                                                                     
    ]                                                                                                               
                                                                                                                    
    entry.data.setdefault("seed", seed)                                                                             
    entry.data.setdefault("rems", rems)                                                                             
                                                                                                                    
    print(seed)                                                                                                     
    ResIO.entry_to_file(entry, f"{seed}.res")    
```


!!! bug "Save to a RES file without REM"
    A blank line is created between the TITL line and the CELL line.
    ```
    TITL mp-135-R2SCAN-mp-1943895 0.00 20.3416 -2.37706 0.000000 0.000000 (Im-3m) n - 1
    
    CELL 1.00000 2.97853 2.97853 2.97853 109.47122 109.47122 109.47121
    LATT -1
    SFAC Li
    Li     1  0.00000000 0.00000000 0.00000000 1.000000  0.00
    END
    ```

!!! bug "END without new line"
    You should add `+ "\n"` at the end of Res class in `res.py` as follows:
    ```
    @dataclass(frozen=True)                                                                                                 
    class Res:                                                                                                              
        """Representation for the data in a res file."""                                                                    
                                                                                                                            
        TITL: AirssTITL | None                                                                                              
        REMS: list[str]                                                                                                     
        CELL: ResCELL                                                                                                       
        SFAC: ResSFAC                                                                                                       
                                                                                                                            
        def __str__(self) -> str:                                                                                           
            return "\n".join(                                                                                               
                [                                                                                                           
                    "TITL" if self.TITL is None else str(self.TITL),                                                        
                    "\n".join(f"REM {rem}" for rem in self.REMS),                                                           
                    str(self.CELL),                                                                                         
                    "LATT -1",                                                                                              
                    str(self.SFAC),                                                                                         
                ]                                                                                                           
            ) + "\n"
    ```

