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
    three_up =  os.path.abspath(os.path.join(__file__ ,"../../.."))
    # print(three_up)
    # parse settings file
    with open(os.path.join(three_up,'settings.yml')) as file:
        settings = yaml.full_load(file)

    versioned_gdb = settings.get('gdb').get('versions')[0]

    # make original gdb workspace and scratchWorkspace dynamic, not-hardcoded paths
    original_gdb = os.path.join(three_up,"PC414 CWI Million Acres.gdb")
    workspace = os.path.join(three_up,versioned_gdb)
    scratch_workspace = os.path.join(three_up,"scratch.gdb")

    for w in [workspace,scratch_workspace]:
        if not os.path.exists(w):
            # print(f'Creating new FileGDB: {w}')
            arcpy.management.CreateFileGDB(os.path.dirname(w), os.path.basename(w))

    return original_gdb, workspace, scratch_workspace


# def init_gdb():
#     """
#     Returns local paths to original, current version, and scratch .gdb's and makes the last two if they don't exist.
#     usage: insert this line of code into all other scripts at the top:
#     original_gdb, workspace, scratch_workspace = init_gdb()
#     """
#     three_up =  os.path.abspath(os.path.join(__file__ ,"../../.."))
#     # print(three_up)
#     # parse settings file
#     with open(os.path.join(three_up,'settings.yml')) as file:
#         settings = yaml.full_load(file)

#     versioned_gdb = settings.get('gdb').get('versions')

#     # make original gdb workspace and scratchWorkspace dynamic, not-hardcoded paths
#     original_gdb = os.path.join(three_up,"PC414 CWI Million Acres.gdb")
#     # workspace = os.path.join(three_up,"PC414 CWI Million Acres.gdb")
#     workspace = os.path.join(three_up,versioned_gdb)
#     scratch_workspace = os.path.join(three_up,"scratch.gdb")

#     for w in [workspace,scratch_workspace]:
#         if not os.path.exists(w):
#             # print(f'Creating new FileGDB: {w}')
#             arcpy.management.CreateFileGDB(os.path.dirname(w), os.path.basename(w))

#     return workspace, scratch_workspace

def unique_rename(scratch_fc:str,input_fc:str):
    """
    Creates unique name and renames a scratch object
    Renamed structure: {input_id}_{scratch_id}_{datestring}
    
    args:
    
    scratch_fc: full file path of scratch fc you want to rename ("Pts_enrichment_RCD"))
    input_fc: name of the original input fc for the tool (e.g. "enrich_pts_in")
    """
    scratch_id = os.path.basename(scratch_fc)
    input_id = os.path.basename(input_fc) # for now, keep the whole basename including the date string
    date_id = datetime.utcnow().strftime("%Y-%m-%d").replace('-','') # like 20221216
    # new_name = f"{scratch_id}_{input_id}_{date_id}"
    new_name = f"{input_id}_{scratch_id}_{date_id}"
    renamed = arcpy.management.Rename(scratch_fc, new_name)
    return new_name


def delete_scratch_files(gdb, delete_fc, delete_table, delete_ds):
    """
    Deletes all layers in the scratch GDB
    
    args:

    gdb: full file path to GDB from which you want to delete all files
    delete_table: yes or no (or really anything else)
    delete_fc: yes or no (or really anything else)
    delete_ds: yes or no (or really anything else)
    
    """
    arcpy.env.workspace = gdb
    fc_list = arcpy.ListFeatureClasses()
    tables = arcpy.ListTables()
    ds_list = arcpy.ListDatasets()
    [print(f"Deleting files from {gdb}")]
    #feature classes
    if delete_fc == 'yes':
        for fc in fc_list:
            arcpy.Delete_management(fc)
    else:
        print('did not delete fc')
    #tables
    if delete_table == 'yes':
        for table in tables:
            arcpy.Delete_management(table)
    else:
        print('did not delete tables')
    #data sets
    if delete_ds == 'yes':
        for ds in ds_list:
            arcpy.Delete_management(ds)
    else:
        print('did not delete ds')

def check_exists(fc_list:list,workspace):
    """
    Checks if all datasets exist, returning a list of non-existent datasets if applicable
    """
    arcpy.env.workspace = workspace
    [print(f"Dataset does not exist: {fc}") for fc in fc_list if not arcpy.Exists(fc)]


def og_file_input(prefix:str, filetype:str, gdb):
    """
    Finds input file in the "a_Originals" folder in the workspace
    
    args:

    gdb: full file path to GDB from which you want to delete all files
    
    prefix: prefix of desired file

    filetype: type of feature class desired (Point, Line, Polyline, Polygon, etc.)
    
    """
    arcpy.env.workspace = gdb
    file_list = arcpy.ListFeatureClasses(feature_type = filetype)
    files_w_prefix = []
    for filename in file_list:
        if filename.startswith(prefix):
            files_w_prefix.append(filename) 
    
    if len(files_w_prefix) == 0:
        raise FileNotFoundError(f"File does not match criteria. prefix: {prefix}, file type: {filetype}, workspace: {gdb}")
    
    files_w_prefix.sort()
    most_recent = files_w_prefix[-1]
    return most_recent

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
