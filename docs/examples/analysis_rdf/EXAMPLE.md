# RDF using ASE


!!! info "Info"
    ase.geometry.analysis

    class Analysis(images, nl, kwargs)

    - images: class
        - ase.Atoms object or list of such Images to analyze.
    - nl: None | class
        - ase.neighborlist.NeiborList object or list of such Neighborlists for
          the given images. 
        - One or nImages, depending if bonding pattern changes or is constant.
        - Using Neiborlist greatly improves speed.
    - kwargs:
        - Arguments for constructing ase.neighborlist.NeiborList object if nl is
          None. (build_neighbor_list)

    Analysis._get_slice(imageIdx)
    ```
    ase.ga.utilities.get_rdf(
        atoms,
        rmax,
        nbins,
        distance_maxtrix=None,
        elements=None,
        no_dists=False
    )
    ```
    - rmax : float                                                                                                        
        - The maximum distance that will contribute to the rdf.                                                           
        - The unit cell should be large enough so that it encloses a                                                      
        - sphere with radius rmax in the periodic directions.                                                             
                                                                                                                        
    - nbins : int                                                                                                         
        - Number of bins to divide the rdf into.                                                                          
                                                                                                                        
    - distance_matrix : numpy.array                                                                                       
        - An array of distances between atoms, typically                                                                  
        - obtained by atoms.get_all_distances().                                                                          
        - Default None meaning that it will be calculated.                                                                
                                                                                                                        
    - elements : list or tuple                                                                                            
        - List of two atomic numbers. If elements is not None the partial                                                 
        - rdf for the supplied elements will be returned.                                                                 
                                                                                                                        
    - no_dists : bool                                                                                                     
        - If True then the second array with rdf distances will not be returned 



    - rmax: float
        - Maximum distance of RDF.
    - nbins: int
        - Number of bins to divide RDF.
    - imageIdx: int | slice | None
        - Images to analyze.
        - 
    - elements: str | int | list | tupule
        - Make partial RDFs.
        - All: If elements is None, a full RDF is calculated.
        - Specific atoms: If elements is an integer or a list/tuple of integers,
          only those atoms will contribute to the RDF (like a mask). 
        - Specific elements: If elements is a string or a list/tupule of
          strings, only atoms of those elements will contribute.

          

    Here, images indicate list of ase.Atoms objects, probably the snapshots of
    MD trajectory.



