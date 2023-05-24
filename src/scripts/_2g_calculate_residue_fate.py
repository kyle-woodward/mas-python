import arcpy
import os
from sys import argv
from scripts.utils import init_gdb, runner
original_gdb, workspace, scratch_workspace = init_gdb()

def Residue(Input_Table):  # 2g Calculate Residue Fate
    arcpy.env.overwriteOutput = True

    # Process: Calculate Residue Fate (Calculate Field) (management)
    Veg_Summarized_Polygons_Laye3_3_ = arcpy.management.CalculateField(in_table=Input_Table, field="RESIDUE_FATE", expression="ifelse(!Fuels_Treatments_Piles_Crosswalk.Residue_Fate!)", expression_type="PYTHON3", code_block="""def ifelse(RES):
    if RES == \"Biochar or Other Pyrolysis\":
        return \"BIOCHAR_PYROLYSIS\"
    elif RES == \"Broadcast Burn\":
        return \"BROADCAST_BURN\"
    elif RES == \"Chipping\":
        return \"CHIPPING\"
    elif RES == \"Durable Products\":
        return \"DURABLE_PRODUCTS\"
    elif RES == \"Firewood\":
        return \"FIREWOOD\"
    elif RES == \"Landfill\":
        return \"LANDFILL\"
    elif RES == \"Left on Sight\":
        return \"LEFT_ON_SITE\"
    elif RES == \"Liquid Fuels\":
        return \"LIQUID_FUELS\"
    elif RES == \"Lop and Scatter\":
        return \"LOP_SCATTER\"
    elif RES == \"No Residue/Not Applicable\":
        return \"NO_RESIDUE/NOT_APPLICABLE\"
    elif RES == \"Offsite Bioenergy\":
        return \"OFFSITE_BIOENERGY\"
    elif RES == \"Other\":
        return \"OTHER\"
    elif RES == \"Pile Burning\":
        return \"PILE_BURNING\"
    elif RES == \"Short-Lived Products\":
        return \"SHORT-LIVED_PRODUCTS\"
    else:
        return None
   """, field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")

    return Veg_Summarized_Polygons_Laye3_3_

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
        Residue(Input_Table=os.path.join(workspace,"WFR_TF_Template"))
