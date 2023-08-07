from rhealpixdggs.dggs import Cell, RHEALPixDGGS
from rhealpixdggs.ellipsoids import WGS84_ELLIPSOID

def area_of_cells(rdggs=RHEALPixDGGS(ellipsoid=WGS84_ELLIPSOID, max_areal_resolution=1), cells=None):
    '''
    Returns the area occupied by a set of cells in metres squared.
    
    Parameters
    ----------
    cells: A list of rdggs.cell objects or strings to calculate the area of.
    rdggs: The rHEALPix DGGS on a given ellipsoid for which these cells based on.
    '''
    if (cells==None): #can be empty (in this case 0 area) so equate with None
        raise Exception("no cell list provided.") 
    
    if not isinstance(cells, list):
        raise Exception(f"Please Provide a list. Recieved {type(cells)}") 

    if not cells: #it is empty cell list.
        return 0
    
    #Else all good, calculate area.
    res_freqs = {}
    for res in range(0, rdggs.max_resolution+1): res_freqs[res]=0 #initialise possible counts to 0 rather than both checking if statements a million times
    for cell in cells:
        res_freqs[len(str(cell))-1]+=1
    tot_area=0
    for res, freq in res_freqs.items():
         tot_area+=freq*rdggs.cell_area(res, plane=False)
    return tot_area
