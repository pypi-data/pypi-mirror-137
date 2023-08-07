from rhealpixdggs.dggs import Cell, RHEALPixDGGS
from rhealpixdggs.ellipsoids import WGS84_ELLIPSOID
from shapely.geometry import Polygon, MultiPolygon
from math import isclose

def get_cell_poly(cell):
    '''
    Returns the shapely polygon of a rhealpix cell object by first finding the vertices using cell.vertices().
    
    Mostly, returns Polygon(cell.vertices()), but sometimes fixes the result from cell.vertices() for shapely to interpret better. 
    
    For example to interpret a polar cap cell as an area and not a line along constant latitude. 

    Additionally, if a cell boundary crosses or touches the +-180 longitude, the function splits the cell and returns a multipolygon.
    This ensures shapely defines the area of the polygon as not going the long way around the ellipsoid which would be incorrect. 
    
    Parameters
    ---------
    cell: a rhealpix cell object to find the shapely polygon for using EPSG:4326 CRS.
    
    '''
    # this function could be split into a fix_vertices() function. then a get_cell_poly_from_vertices() so other librarys that don't 
    # use shapely can use the fix_vertices() method. I know AusPIX doesn't work well in tasmania (S Region)
    cell_shape = cell.ellipsoidal_shape()   
    vertices = cell.vertices(plane=False, trim_dart=True)
    if cell_shape == 'cap': #make polygon out of line of latitude so shapely iterprets the cap as a poly and not a line
        pole = str(cell)[0]
        if(pole == 'N'):
            height = vertices[0][1]
            vertices = [(-180, 90), (180, 90), (180, height), (-180, height)] # order: NW, NE, SE, SW
            return Polygon(vertices)
        elif(pole == 'S'):
            height = vertices[0][1]
            vertices = [(-180,height), (180, height), (180, -90), (-180, -90)] # order: NW, NE, SE, SW
            return Polygon(vertices)
        else: 
            raise Exception('error1')   # should never happen    
        
    elif cell_shape in ['quad', 'skew_quad', 'dart']: 
        x_coords = [vertices[i][0] for i in range(len(vertices))]
        minx = min(x_coords)
        maxx = max(x_coords)
        
        if(round( abs(maxx - minx))>179 ): # if long way around.
            abs_tol = 0.0000001
            if cell_shape=='dart' and minx<0 and maxx>0: #dart bisects the 180. Need to check minx and maxx               
                y_coords = [vertices[i][1] for i in range(len(vertices))]
                miny = min(y_coords)
                maxy = max(y_coords)   
                pole = str(cell)[0]
                if pole == 'N': #dart is right side up (points up)
                    Poly1 = Polygon([ (-maxx, miny), (-180, miny), (-180, maxy) ]) #neg side
                    Poly2 = Polygon([ (maxx, miny), ( 180, miny), ( 180, maxy) ])
                elif pole =='S': #dart is pointing down
                    Poly1 = Polygon([ (-maxx, maxy), (-180, maxy), (-180, miny) ]) #neg side
                    Poly2 = Polygon([ (maxx, maxy), ( 180, maxy), ( 180, miny) ])   
                else:
                    raise Exception("there are dart in non poles?") # NO
                return MultiPolygon([Poly1, Poly2])     
                raise Exception('shoudlve returned. Not accounted for yet, do they exist?')
            #havent't returned. not crossing dart. but stil defined long way around --> touches and is using wrnog polarity for 180
            for i in range(len(vertices)):
                if isclose(vertices[i][0], -180, abs_tol=abs_tol):
                    vertices[i] = (180, vertices[i][1]) #can't change tuples so re define.
                elif isclose(vertices[i][0], 180, abs_tol=abs_tol):
                    vertices[i] = (-180, vertices[i][1])
            return Polygon(vertices)
        else: #all checks done its ok - return as is from cell.vertices
            return Polygon(vertices)
    else:
        raise Exception('error2')         
    
def str_to_list(mystr):   
    #converts string cell id to list (keeping the letter a str). This is what the cell object constructor requires.
    return [mystr[0]] + [int(i) for i in mystr[1:]]



def get_subcells(cell_str, res=None): # USE list.extend(get_subcells(cell, res=X)). dont append because this returns a list. you wuld be adding an entire list as one element. but doing .extend will run the generator.
    if not res: # return the children (first subcells down)
        children_generator = Cell(suid=str_to_list(cell_str)).subcells()
        return [str(child) for child in children_generator]
    # else , given a resolution to generate cells for!!
    subcells_generator = Cell(suid=str_to_list(cell_str)).subcells(resolution=res)
    return [str(subcell) for subcell in subcells_generator]


# abort writing this - can use the geoscience one in a for loop.
'''
def generate_all_subcells_until_max_res(parent_cell=None, max_res=None):
    # generates all subcell suid's into a list for every resolution finer than the parent cells until max_res
    # e.g. if parent cell is R (which is resolution 0) and max_res == 2 then will return the following list.
    # ['R1','R2',...,'R9','R11', 'R12', ..., 'R99'] # that is, all resolution 1 and 2 cells contained in the resolution 0 cell, 'R'.
    if not parent_cell:
        raise Exception("Please provide parent cell string")
    if not max_res:
        raise Exception("Please provide max resolution to generate subcells until")
    parent_cell = Cell(suid=str_to_list(parent_cell))
    

    # cell = rdggs.cell(suid=str_to_list(cell_str)) 

    children = []
    children.append(parent_cell.subcells())
'''

def hybrid_to_res(cell_list, target_res=None): #converts between resolutions. can go to a coarser res but doesnt remove duplicates. convert to set then back if u want to remove duplicates.
    '''
    Recieves a hybridised DGGS cell lists and compute the equilvalent spatial geometry using cells of target_res.
    Currently only genereates the constant res representation of a cell list for cell_lists whose min res
    is equal to or more coarse than the target res. I.e., target_res must be equal to or finer than the finest used in cell_list.
    # need to remove duplicates if u dont want duplicate coarser cells!!!
    '''
    if not isinstance(cell_list, list):
        raise Exception("cannot work on non list - recieved {0}".format(type(cell_list)))
    if not target_res:
        raise Exception("Please provide a target resolution")

    #cell_list.sort(key=len, reverse=True)
    #input_res = len(cell_list[0])-1
    
    #if target_res<input_res:
    #    raise Exception("target_res must be equal to or finer than the finest used in cell_list. Input res = {0} - target_res = {1}".format(input_res,target_res))
        
    # ok
    cells2 = [] # cell list for the non-hybrid representation.
    
    for cell in cell_list:
        if len(cell)-1==target_res:
            cells2.append(cell)
        else:
            if len(cell)-1<target_res:
             cells2.extend(get_subcells(cell, res=target_res))
            else:
                cells2.append(cell[0:target_res+1])
    return cells2 # need to remove duplicates if u dont want duplicate coarser cells!!!

