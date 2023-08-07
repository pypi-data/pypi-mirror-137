from ipyleaflet import Map, GeoData, basemaps
from rhealpixdggs.dggs import Cell, RHEALPixDGGS
from rhealpixdggs.ellipsoids import WGS84_ELLIPSOID
from DGGSForPoly.cell_helpers import get_cell_poly, str_to_list
import geopandas as gp

def cell_plot(cell_list=None, poly=None, zoom=10, rdggs=None):
    '''
    Plots a shapely object (Polygon) and/or a dggs cell list. 
    
    Parameters
    ---------
    
    cell_list: a list of rhealpix dggs cells as strings or rhealpix cell objects to be plotted
    poly: shapely Polygon (or multipolygon) to be plotted
    zoom: Starting zoom level of map
    rdggs: The rHEALPix DGGS on a given ellipsoid. Defaults to WGS84_ELLIPSOID. Only needed if plotting cells.
    
    '''

    if cell_list: cell_list_to_plot=cell_list.copy() 
      
    if poly: #plot the polygons too.
        poly_df = gp.GeoDataFrame(geometry=gp.GeoSeries([poly]))
        poly_layer = GeoData(geo_dataframe = poly_df,
                       style={'color': 'red', 'opacity':6, 'weight':2.5,'fillOpacity':0.1},
                       name = 'Polygon')
            
    if cell_list: #only if doing cells.
        if not rdggs: #none given, need one for cells.
            rdggs=RHEALPixDGGS(ellipsoid=WGS84_ELLIPSOID, max_areal_resolution=1)

        if isinstance(cell_list_to_plot[0], str): #recieved list of cell strings... convert to cell objects
            for i in range(len(cell_list_to_plot)):
                    cell_list_to_plot[i] = rdggs.cell(suid=str_to_list(cell_list_to_plot[i]))
        
        cell_poly_list = []
        for cell in cell_list_to_plot:
            cell_poly_list.append(get_cell_poly(cell)) #list of polygons (GeoSeries) to be
        
        df_cell = gp.GeoDataFrame(geometry=gp.GeoSeries(cell_poly_list))
        cell_layer = GeoData(geo_dataframe = df_cell,
                       style={'color': 'purple', 'opacity':3, 'weight':1,'fillOpacity':0.4},
                       hover_style={'fillColor': 'red' , 'fillOpacity': 0.1},
                       name = 'DGGS_Cell')
            
    if poly: #use poly for centre
        center = poly.centroid.coords[0]
        center = (center[1],center[0])
    else: #use the a cell for the centre
        center = cell_list_to_plot[0].nucleus(plane=False)
        center = (center[1], center[0]) 
    
    m = Map(zoom=zoom, center=center) 
    if poly: m.add_layer(poly_layer)
    if cell_list: m.add_layer(cell_layer) #if given a cell_list 
    m.layout.height="550px"
    display(m)
    return