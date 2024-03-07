#!/usr/bin/env python

import itertools

def get_chemsys_from_elements(
    elements: list[str],
    mode: str = "any",
    nelements: int = 0
) -> list[str]:
    """
    Get a list of chemical system based on the provided elements.

    Args:
        elements (list):
            A list of chemical elements
        mode
        nelements (int): The number of chemical elements to generate
            combinatorial chemical systems. Defaults to 0, which generated all
            possible combinatorial chemical systems. Set 2 for binary systems.
        

    Returns:
        
    """
    chemsys = []

    if nelements != 0:
        for els in itertools.combinations(elements, nelements):
            chemsys.append("-".join(sorted(els)))
    else:
        for i in range(len(elements)):
            for els in itertools.combinations(elements, i + 1):
                chemsys.append("-".join(sorted(els)))

    return chemsys


def get_structure_from_chemsys(                                                                                         
    chemsys: str | list[str],                                                                                           
    longname: bool = False,                                                                                             
    fmt: str = "POSCAR",                                                                                                
                                                                                                                        
    csv: bool = False,                                                                                                  
    maxnsites: int = 99999                                                                                              
):                                                                                                                      
    """                                                                                                                 
    Get a list of Materials Project IDs for materials containing only elements specified                                
                                                                                                                        
    Args:                                                                                                               
        chemsys (str | list[str]): Chemical systems e.g., Li-Ni-O                                                       
        longname (bool): Output the structure to a file with a long name                                                
        csv (bool): Write a csv file                                                                                    
    """                                                                                                                 
                                                                                                                        
    # set up parameters for retreving documents from Materials Project database                                         
                                                                                                                        
    fields = ["material_id", "chemsys", "structure"]                                                                    
                                                                                                                        
    if longname:                                                                                                        
        fields += ["formula_pretty", "nsites", "symmetry"]                                                              
                                                                                                                        
    if csv:                                                                                                             
        fields_csv = ["material_id",                                                                                    
                        "chemsys",                                                                                      
                        "formula_pretty",                                                                               
                        "is_stable",                                                                                    
                        "theoretical",                                                                                  
                        "nsites",                                                                                       
                        "nelements",                                                                                    
                        "symmetry"]                                                                                     
        d_csv = {field: [] for field in fields_csv}                                                                     
        fields = list(dict.fromkeys(fields + fields_csv)) # unique                                                      
                                                                                                                        
                                                                                                                        
    # retrieve documents from Materials Project database                                                                
                                                                                                                        
    print("Retrieving data from Materials Project ...")                                                                 
    print("Chemical Systems: ", chemsys)                                                                                
    print("Fields: ", fields)                                                                                           
    start_time = time.time()                                                                                            
                                                                                                                        
    docs = mpr.materials.summary.search(                                                                                
        chemsys=chemsys,                                                                                                
        fields=fields,                                                                                                  
        num_sites=(0,maxnsites)                                                                                         
    )                                                                                                                   
                                                                                                                        
    end_time = time.time()                                                                                              
    duration = end_time - start_time                                                                                    
    print(f"Time taken: {duration} seconds")                                                                            
                                                                                                                        
                                                                                                                        
    # write a csv file                                                                                                  
                                                                                                                        
    if csv:                                                                                                             
        for doc in docs:                                                                                                
            for field in fields_csv:                                                                                    
                if field == "symmetry":                                                                                 
                    d_csv[field].append(getattr(doc, field).symbol)                                                     
                else:                                                                                                   
                    d_csv[field].append(getattr(doc, field))                                                            
        df_csv = pd.DataFrame(d_csv)                                                                                    
        df_csv.to_csv('mp.csv', sep=',', index=False)                                                                   
        print("mp.csv is created")                                                                                      
                                                                                                                        
                                                                                                                        
    # output structures to files                                                                                        
                                                                                                                        
    for doc in docs:                                                                                                    
        mpid = doc.material_id                                                                                          
        chemsys = doc.chemsys                                                                                           
        structure = doc.structure                                                                                       
                                                                                                                        
        crudroot = "mp_pbe" if not gga_u_applied(chemsys.split('-')) else "mp_pbe+u"                                    
        filename = f"{crudroot}-{mpid}.{fmt}"                                                                           
                                                                                                                        
        if longname:                                                                                                    
            formula = doc.formula_pretty                                                                                
            nsites = doc.nsites                                                                                         
            sg = doc.symmetry.symbol                                                                                    
            sg = sg.replace("/","").replace("_","")                                                                     
            filename = f"{crudroot}-{formula}-{nsites}-{sg}-{mpid}.{fmt}"                                               
                                                                                                                        
                                                                                                                        
        structure.to(filename=filename, fmt=fmt)   

def get_entry_from_summarydoc(                                                                                          
    chemsys: str | list[str]                                                                                            
):                                                                                                                      
    """                                                                                                                 
    Download entries from the Materials Poject database                                                                 
                                                                                                                        
    Args:                                                                                                               
        chemsys (str | list[str]): Chemical systems                                                                     
                                                                                                                        
    Returns:                                                                                                            
        list[ComputedStructureEntry]                                                                                    
    """                                                                                                                 
                                                                                                                        
    return mpr.get_entries(                                                                                             
        chemsys_formula_mpids=chemsys,                                                                                  
        compatible_only=True,                                                                                           
        property_data=None,                                                                                             
        conventional_unit_cell=False,                                                                                   
        additional_criteria=None,                                                                                       
    )    


def gga_u_applied(elements: list[str]) -> bool:                                                                         
    """                                                                                                                 
    Check if the GGA+U method has been applied to the given system.                                                     
    Hubbard U correction is applied to oxides or fluorides in the Materials Project database.                           
    """                                                                                                                 
    return any(e in elements for e in ['O', 'F']) and \                                                                 
           any(e in elements for e in ['Co', 'Cr', 'Fe', 'Mn', 'Mo', 'Ni', 'V', 'W'])    
