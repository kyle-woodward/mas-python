"""
# Description: 
#               
#               
#              
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import arcpy
# import os
# from sys import argv
from .utils import init_gdb, runner

original_gdb, workspace, scratch_workspace = init_gdb()


def UtilityVegTreat(Input_Table):  # 2i Utilitiy Veg Treatment Type
    arcpy.env.overwriteOutput = True

    # Process: Calculate Utility ID (Calculate Field) (management)
    Updated_Input_Table = arcpy.management.CalculateField(
        in_table=Input_Table,
        field="UtilityID",
        expression="ifelse(!UtilityID!)",
        code_block="""def ifelse(ID):
    if ID == \"SDG&E\":
        return \"SDGE\"
    else:
        return ID""",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Treatment (Calculate Field) (management)
    Output_Table = arcpy.management.CalculateField(
        in_table=Intermediate_Table,
        field="VegetationTreatmentType",
        expression="ifelse(!VegetationTreatmentType!)",
        code_block="""def ifelse(TY):
    #    if TY.find(\"Pole%\"):
        if 'tandard' in TY:
            return 'Radial clearance - standard'
        elif 'nhance' in TY:
            return 'Radial clearance - enhanced'
        elif 'hang' in TY:
            return 'Overhang clearing'
        elif 'ole' in TY:
            return 'Pole Brushing'
        elif 'azard' in TY:
            return 'Tree removal - hazard tree'
        elif 'ortal' in TY:
            return 'Tree removal - tree mortality'
        elif 'rimming' in TY:
            return 'Tree trimming'
        elif 'reak' in TY:
            return 'Fire break creation'
        elif 'rush' in TY:
            return 'Brush clearance'
        elif 'ult' in TY:
            return 'Other or multiple treatment types - see comment'
        else:
            return TY""",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    return Output_Table


# if __name__ == "__main__":
#     runner(workspace, scratch_workspace, UtilityVegTreat, "*argv[1:]")
    # # Global Environment settings
    # with arcpy.EnvManager(
    # extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""",  outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""",
    # preserveGlobalIds=True,
    # qualifiedFieldNames=False,
    # scratchWorkspace=scratch_workspace,
    # transferDomains=True,
    # transferGDBAttributeProperties=True,
    # workspace=workspace):
    #     UtilityVegTreat(Input_Table=os.path.join(workspace,"WFR_TF_Template"))
