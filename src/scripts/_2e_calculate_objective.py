# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2022-11-29 12:13:37
"""

import arcpy
import os
from sys import argv
from scripts.utils import init_gdb, runner
workspace, scratch_workspace = init_gdb()

def Objective(Input_Table):  # 2e Calculate Objective

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False


    # Process: Calculate Objective (Calculate Field) (management)
    Veg_Summarized_Polygons_Laye3_2_ = arcpy.management.CalculateField(in_table=Input_Table, field="PRIMARY_OBJECTIVE", expression="ifelse(!Fuels_Treatments_Piles_Crosswalk.Objective!)", expression_type="PYTHON3", code_block="""def ifelse(OBJ):
    if OBJ ==\"Biomass Utilization\":
        return \"BIOMASS_UTIL\"
    elif OBJ == \"Burned Area Restoration\":
        return \"BURNED_AREA_RESTOR\"
    elif OBJ == \"Carbon Storage\":
        return \"CARBON_STORAGE\"
    elif OBJ == \"Cultural Burn\":
        return \"CULTURAL_BURN\"
    elif OBJ == \"Ecological Restoration\":
        return \"ECO_RESTOR\"
    elif OBJ == \"Fire Prevention\":
        return \"FIRE_PREVENTION\"
    elif OBJ == \"Forest Pest Control\":
        return \"FOREST_PEST_CNTRL\"
    elif OBJ == \"Forestland Stewardship\":
        return \"FOREST_STEWARDSHIP\"
    elif OBJ == \"Fuel Break\":
        return \"FUEL_BREAK\"
    elif OBJ == \"Habitat Restoration\":
        return \"HABITAT_RESTOR\"
    elif OBJ == \"Invasive Species Control\":
        return \"INV_SPECIES_CNTRL\"
    elif OBJ == \"Land Protection\":
        return \"LAND_PROTECTION\"
    elif OBJ == \"Mountain Meadow Restoration\":
        return \"MTN_MEADOW_RESTOR\"
    elif OBJ == \"Non-Timber Products\":
        return \"NON-TIMB_PRODUCTS\"
    elif OBJ == \"Other Forest Management\":
        return \"OTHER_FOREST_MGMT\"
    elif OBJ == \"Other Fuels Reduction\":
        return \"OTHER_FUELS_REDUCTION\"
    elif OBJ == \"Prescribed Fire\":
        return \"PRESCRB_FIRE\"
    elif OBJ == \"Recreation\":
        return \"RECREATION\"
    elif OBJ == \"Reforestation\":
        return \"REFORESTATION\"
    elif OBJ == \"Riparian Restoration\":
        return \"RIPARIAN_RESTOR\"
    elif OBJ == \"Roadway Clearance\":
        return \"ROADWAY_CLEARANCE\"
    elif OBJ == \"Site Preparation\":
        return \"SITE_PREP\"
    elif OBJ == \"Timber Harvest\":
        return \"TIMBER_HARVEST\"
    elif OBJ == \"Utility Right of Way Clearance\":
        return \"UTIL_RIGHT_OF_WAY\"
    elif OBJ == \"Watershed Restoration\":
        return \"WATSHD_RESTOR\"
    elif OBJ == \"Wetland Restoration\":
        return \"WETLAND_RESTOR\"
    elif OBJ == \"Not Defined\":
        return \"NOT_DEFINED\"
    else:
        return \"TBD\"""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")

    return Veg_Summarized_Polygons_Laye3_2_

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
        Objective(Input_Table=os.path.join(workspace,"WFR_TF_Template"))