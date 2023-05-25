#NOTE: Might not need to work this one as output (WFR_TF_Template feature class) is in the b_Reference feature dataset, might be a one-off tool to make it
import arcpy
import os
from ._1b_add_fields import AddFields2 # importable scripts as modules in other scripts can't start with a number, so we add a '_' to script namer
from sys import argv
from .utils import init_gdb, runner

original_gdb, workspace, scratch_workspace = init_gdb()

def WFRTFtemplate():  # 1a Template

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False


    # Process: Create Feature Class (Create Feature Class) (management)
    b_Reference_original_path=os.path.join(original_gdb,"b_Reference") # original b_Reference dataset in orig gdb
    b_Reference_new_path = os.path.join(workspace,'b_Reference')
    # Must make b_Reference feature dataset if doesn't already exist
    if not os.path.exists(b_Reference_new_path):
        arcpy.management.CreateFeatureDataset(out_dataset_path=workspace, out_name="b_Reference") # {spatial_reference} is third opt arg, think don't need since we are always running with EnvManager..?
    
    WFRTF_Template = arcpy.management.CreateFeatureclass(out_path=b_Reference_new_path, out_name="WFR_TF_Template", geometry_type="POLYGON", template=[], has_m="DISABLED", has_z="DISABLED", spatial_reference="PROJCS[\"NAD_1983_California_Teale_Albers\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Albers\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",-4000000.0],PARAMETER[\"Central_Meridian\",-120.0],PARAMETER[\"Standard_Parallel_1\",34.0],PARAMETER[\"Standard_Parallel_2\",40.5],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]];-16909700 -8597000 10000;#;#;0.001;#;#;IsHighPrecision", config_keyword="", spatial_grid_1=0, spatial_grid_2=0, spatial_grid_3=0, out_alias="")

    # Process: 1b Add Fields (1b Add Fields) (PC414CWIMillionAcres)
    WFRTF_Template_5_ = AddFields2(Input_Table=os.path.join(b_Reference_new_path,"WFR_TF_Template"))

    return

if __name__ == '__main__':
    # Global Environment settings
    # run desired function with environment settings set by arcpy.EnvManager, don't think this is gonna work
    #runner(workspace,scratch_workspace,WFRTFtemplate)

    with arcpy.EnvManager(
    extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""", 
    outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""", 
    preserveGlobalIds=True, 
    qualifiedFieldNames=False, 
    scratchWorkspace=scratch_workspace, 
    transferDomains=True, 
    transferGDBAttributeProperties=True, 
    workspace=workspace):
        # WFRTFtemplate(*argv[1:])
        WFRTFtemplate()


