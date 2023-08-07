# DGGSForPoly

## poly_fill
Contains a function that returns a set of rHEALPIX DGGS cells that describe the geometry of the inputted polygon. 

The function is built on top of the AusPIX DGGS Engine (https://github.com/GeoscienceAustralia/AusPIX_DGGS/) and makes use of Shapely's Binary Predicates (which is a possible area for future optimisation).

#### Fill Strategies
poly_fill() function has 3 fill_strategies:   
    1) poly_fully_covered_by_cells -  returns a set of cells that completly encapsulating the polygon -> over estimates area   
    2) centroids_in_poly -  returns a set of cells whose centroids are contained by the polygon.   
    3) cells_fully_contained_in_poly -  returns a set of cells completely encapsulated *by* the Polygon -> under estimates area   

## cell_operations
Contains modules for calculating area of cell list and for visualising sets of cells and the polygon they represent. poly_fill utilises some functions in the helper module.  

## Setting up environment

```
$ python3 -m venv .venv
$ source .venv/bin/activate
# or on Windows: source .venv/Scripts/activate
$ python setup.py install
```

Include testing
```
$ pip install -U pytest
$ pytest
```