

"""
/work/e89/e89/shj29/applic/miniconda3/envs/shjoo/lib/python3.11/site-packages/pymatgen/io/res.py
"""

    @classmethod                                                                                                        
    def _ions_from_sites(cls, sites: list[PeriodicSite]) -> list[Ion]:                                                  
        """Produce a list of entries for a SFAC block from a list of pymatgen PeriodicSite."""                          
        ions: list[Ion] = []                                                                                            
        species = list({str(site.specie) for site in sites})                                                            
        for site in sites:                                                                                              
            for specie, occ in site.species.items():                                                                    
                x, y, z = map(float, site.frac_coords)                                                                  
                spin = site.properties.get("magmom")                                                                    
                spin = spin and float(spin)                                                                             
                ions.append(Ion(specie, species.index(str(specie))+1, (x, y, z), occ, spin))                            
        return species, ions                                                                                            
                                                                                                                        
    @classmethod                                                                                                        
    def _sfac_from_sites(cls, sites: list[PeriodicSite]) -> ResSFAC:                                                    
        """Produce a SFAC block from a list of pymatgen PeriodicSite."""                                                
        species, ions = cls._ions_from_sites(sites)                                                                     
        return ResSFAC(species, ions) 

