import arcpy
from sys import argv
from .utils import init_gdb
import time
import os
original_gdb, workspace, scratch_workspace = init_gdb()

def TransformCheck(Input_Table, Output_Duplicates):  # 9c Transform Check Duplicates

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    Value = time.strftime("%Y%m%d-%H%M%S").replace('-','')
    # Process: Assess Duplicates Frequency (2) (Frequency) (analysis)
    Transform_Treatmen_Frequency_3_ = os.path.join(scratch_workspace,fr"duplicates_{Value}")
    arcpy.analysis.Frequency(in_table=Input_Table.__str__().format(**locals(),**globals()), 
                             out_table=Transform_Treatmen_Frequency_3_, 
                             frequency_fields=["PROJECTID_USER"])

    # Process: Assess Duplicates Add Join (2) (Add Join) (management)
    Transform_Projects_Dissolve_ = arcpy.management.AddJoin(in_layer_or_view=Input_Table.__str__().format(**locals(),**globals()), 
                                                            in_field="PROJECTID_USER", 
                                                            join_table=Transform_Treatmen_Frequency_3_,
                                                            join_field="PROJECTID_USER")

    # Process: Select (4) (Select) (analysis)
    arcpy.analysis.Select(in_features=Transform_Projects_Dissolve_, 
                          out_feature_class=Output_Duplicates.__str__().format(**locals(),**globals()), 
                          where_clause="FREQUENCY <> 1")

    # Process: Remove Join (Remove Join) (management)
    if Output_Duplicates:
        Layer_With_Join_Removed = arcpy.management.RemoveJoin(in_layer_or_view=Transform_Projects_Dissolve_)

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(
    extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""",  outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""", 
    preserveGlobalIds=True, 
    qualifiedFieldNames=False, 
    scratchWorkspace=scratch_workspace, 
    transferDomains=True, 
    transferGDBAttributeProperties=True, 
    workspace=workspace):
        TransformCheck(*argv[1:])
