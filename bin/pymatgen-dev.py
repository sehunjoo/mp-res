    @classmethod                                                                                                        
    def _ions_from_sites(cls, sites: list[PeriodicSite]) -> list[Ion]:                                                  
        """Produce a list of entries for a SFAC block from a list of pymatgen PeriodicSite."""                          
        ions: list[Ion] = []                                                                                            
        sfac = list({str(site.specie) for site in sites})                                                               
        for site in sites:                                                                                              
            for specie, occ in site.species.items():                                                                    
                x, y, z = map(float, site.frac_coords)                                                                  
                spin = site.properties.get("magmom")                                                                    
                spin = spin and float(spin)                                                                             
                ions.append(Ion(specie, sfac.index(str(specie))+1, (x, y, z), occ, spin))                               
        return ions  
