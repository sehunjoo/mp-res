# Save to a file in res format

You can save a structure to a file in res using pymatgen.
ASE does not support the AIRSS-RES format.

!!! note "AIRSS-RES" format

    ```
    TITL <seed> <pressure> <volume> <energy> <isd> <iasd> <nfu> <formula> <space group> <#>
    ```

    seed        = unique structure name or file name
    volume      = volume / cell
    energy      = enthalpy / cell
    isd         = integrated spin density / cell
    iasd        = integrated absolute spin density / cell
    nfu         = number of formula untis
    formula     = formula
    space group = space group


## Get ComputedStructureEntry

You need to have a ComputedStructureEntry object to save a structure into a res
format. You can directly download the entries from the Materials Project database.


## Save to RES files

From a ComputedStructureEntry, ResIO takes the information and writes a res file.
The required information are seed, pressure, energy, isd, iasd, and structure,
which can be accesed as follows.

---

??? note "Required Data"
    ```
    entry.data.get("seed")
    entry.energy
    entry.data.get("pressure", 0)
    entry.data.get("isd", 0)
    entry.data.get("iasd", 0)
    entry.data.get("rems", [])
    entry.structure
    ```
    For more information, please refer to,
    **ResIO.entry_to_file** -> **ResWriter._res_from_entry**

If the structure does not have any of those information you can add to the entry.


## Example

```
def mp_entry_to_res(entry):                                                                                             
    '''                                                                                                                 
    Writing a res files with an uncorrected energy                                                                      
    '''                                                                                                                 
    # make energy correction zero                                                                                       
    entry.correction = 0                                                                                                
                                                                                                                        
    material_id = entry.data.get("material_id", "")                                                                     
    task_id = entry.data.get("task_id", "")                                                                             
    run_type = entry.data.get("run_type", "")                                                                           
                                                                                                                        
    # TITL: add seed to entry.data                                                                                      
                                                                                                                        
    seed = f"{material_id}-{run_type}"                                                                                  
    entry.data.update({"seed": seed})                                                                                   
                                                                                                                        
    # TITL: add pressure to entry.data                                                                                  
                                                                                                                        
    entry.data.update({"pressure": 0})                                                                                  
                                                                                                                        
    # TITL: add isd/iasd to entry.data - spin density                                                                   
                                                                                                                        
    isd = 0                                                                                                             
    iasd = 0                                                                                                            
    for site in entry.structure:                                                                                        
        if 'magmom' in site.properties:                                                                                 
             isd += site.properties['magmom']                                                                           
             iasd += abs(site.properties['magmom'])                                                                     
                                                                                                                        
    entry.data.update({"isd": isd})                                                                                     
    entry.data.update({"iasd": iasd})                                                                                   
                                                                                                                        
    # REM: add rems to entry.data - metadata                                                                            
                                                                                                                        
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
                                                                                                                        
    entry.data.update({"rems": rems})                                                                                   
                                                                                                                        
    # write a resfile                                                                                                   
                                                                                                                        
    ResIO.entry_to_file(entry, f"{seed}.res") 
```


!!! bug "Save to a RES file without REM"
    A blank line is created between the TITL line and the CELL line.
    ```
    TITL mp-135-R2SCAN-mp-1943895 0.00 20.3416 -2.37706 0.000000 0.000000 (Im-3m) n - 1

