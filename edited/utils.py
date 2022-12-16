#%%
import os 
import arcpy
import yaml
from datetime import datetime
# usage: insert this line of code into all other scripts at the top:
# original_gdb, workspace, scratch_workspace = init_gdb()
def init_gdb():
    """
    Returns local paths to original, current version, and scratch .gdb's and makes the last two if they don't exist.
    usage: insert this line of code into all other scripts at the top:
    original_gdb, workspace, scratch_workspace = init_gdb()
    """
    # parse settings file
    with open(os.path.join(os.path.dirname(__file__),'settings.yml')) as file:
        settings = yaml.full_load(file)

    versioned_gdb = settings.get('gdb').get('versions')[0]

    # make original gdb workspace and scratchWorkspace dynamic, not-hardcoded paths
    original_gdb = os.path.join(os.path.dirname(os.path.dirname(__file__)),"PC414 CWI Million Acres.gdb")
    workspace = os.path.join(f"{os.path.dirname(os.path.dirname(__file__))}",versioned_gdb)
    scratch_workspace = os.path.join(f"{os.path.dirname(os.path.dirname(__file__))}","scratch.gdb")

    for w in [workspace,scratch_workspace]:
        if not os.path.exists(w):
            # print(f'Creating new FileGDB: {w}')
            arcpy.management.CreateFileGDB(os.path.dirname(w), os.path.basename(w))

    return original_gdb, workspace, scratch_workspace


def unique_path(input_fc:str,out_string:str):
    """
    Constructs a unique file path for a scratch object that is to be created
    
    args:
    
    input_fc: full file path to input fc your process is to be run on
    out_string: unique string to use in the basename of the scratch file (e.g. "Pts_enrichment_Veg")
    """
    _,_,scratch_workspace = init_gdb()
    input_id = os.path.basename(input_fc) # for now, keep the whole basename including the date string
    date_id = datetime.utcnow().strftime("%Y-%m-%d").replace('-','') # like 20221216
    new_path = os.path.join(scratch_workspace,f"{input_id}_{out_string}_{date_id}")
    return new_path

def runner(workspace:str,scratch_workspace:str,func):
    with arcpy.EnvManager(
    extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""", 
    outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""", 
    preserveGlobalIds=True, 
    qualifiedFieldNames=False, 
    scratchWorkspace=scratch_workspace, 
    transferDomains=True, 
    transferGDBAttributeProperties=True, 
    workspace=workspace):
        func()

#%%
# Testing
# original_gdb, workspace, scratch_workspace = init_gdb()
# enrich_pts_in = os.path.join(workspace,'c_Standardized','BLM_standardized_20220912')
# scratch_string = 'WHR_Summary'
# new_path = unique_path(enrich_pts_in,scratch_string)
# print(new_path)
# %%
