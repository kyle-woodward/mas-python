# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2022-11-29 12:13:25
"""
import arcpy
from sys import argv

def Activity(Input_Table):  # 2d Calculate Activity

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False


    # Process: Calculate Activity (Calculate Field) (management)
    Veg_Summarized_Polygons_Laye3_4_ = arcpy.management.CalculateField(in_table=Input_Table, field="ACTIVITY_DESCRIPTION", expression="ifelse(!Fuels_Treatments_Piles_Crosswalk.Activity!)", expression_type="PYTHON3", code_block="""def ifelse(ACT):
    if ACT == \"Aspen/Meadow/Wet Area Restoration\":
        return \"AMW_AREA_RESTOR\"
    elif ACT == \"Biomass Removal\":
        return \"BIOMASS_REMOVAL\"
    elif ACT == \"Broadcast Burn\":
        return \"BROADCAST_BURN\"
    elif ACT == \"Chaining/Crushing\":
        return \"CHAIN_CRUSH\"
    elif ACT == \"Chipping\":
        return \"CHIPPING\"
    elif ACT == \"Clearcut\":
        return \"CLEARCUT\"
    elif ACT == \"Commercial Thin\":
        return \"COMM_THIN\"
    elif ACT == \"Conversion\":
        return \"CONVERSION\"
    elif ACT == \"Discing\":
        return \"DISCING\"
    elif ACT == \"Dozer\":
        return \"DOZER_LINE\"
    elif ACT == \"Easement\":
        return \"EASEMENT\"
    elif ACT == \"Erosion Control\":
        return \"EROSION_CONTROL\"
    elif ACT == \"Group Selection Harvest\":
        return \"GRP_SELECTION_HARVEST\"
    elif ACT == \"Habitat Revegetation\":
        return \"HABITAT_REVEG\"
    elif ACT == \"Handline\":
        return \"HANDLINE\"
    elif ACT == \"Herbicide Application\":
        return \"HERBICIDE_APP\"
    elif ACT == \"Invasive Plant Removal\":
        return \"INV_PLANT_REMOVAL\"
    elif ACT == \"Land Acquisitions\":
        return \"LAND_ACQ\"
    elif ACT == \"Landing Treated - Area Mitigated\":
        return \"LANDING_TRT\"
    elif ACT == \"Lop and Scatter\":
        return \"LOP_AND_SCAT\"
    elif ACT == \"Mastication\":
        return \"MASTICATION\"
    elif ACT == \"Mowing\":
        return \"MOWING\"
    elif ACT == \"Noncommercial Thinning (Mechanical)\":
        return \"NONCOM_THIN_MECH\"
    elif ACT == \"Noncommercial Thinning (Manual)\":
        return \"NONCOM_THIN_MAN\"
    elif ACT == \"Oak Woodland Management\":
        return \"OAK_WDLND_MGMT\"
    elif ACT == \"Pest Control\":
        return \"PEST_CNTRL\"
    elif ACT == \"Pile Burning\":
        return \"PILE_BURN\"
    elif ACT == \"Piling\":
        return \"PILING\"
    elif ACT == \"Precommercial Thinning (Manual)\":
        return \"PRECOM_THIN_MAN\"
    elif ACT == \"Precommercial Thinning (Mechanical)\":
        return \"PRECOM_THIN_MECH\"
    elif ACT == \"Prescribed Herbivory\":
        return \"PRESCRB_HERBIVORY\"
    elif ACT == \"Pruning\":
        return \"PRUNING\"
    elif ACT == \"Rehabilitation of Understocked Area\":
        return \"REHAB_UNDRSTK_AREA\"
    elif ACT == \"Road Obliteration\":
        return \"ROAD_OBLITERATION\"
    elif ACT == \"Sanitation and Salvage Harvest\":
        return \"SANI_SALVG_HARVEST\"
    elif ACT == \"Seedbed Preparation\":
        return \"SEEDBED_PREP\"
    elif ACT == \"Seed Tree Prep Step\":
        return \"SEED_TREE_PREP_STEP\"
    elif ACT == \"Seed Tree Removal Step\":
        return \"SEED_TREE_REM_STEP\"
    elif ACT == \"Seed Tree Seed Step\":
        return \"SEED_TREE_SEED_STEP\"
    elif ACT == \"Shelterwood Prep Step\":
        return \"SHELTERWD_PREP_STEP\"
    elif ACT == \"Shelterwood Removal Step\":
        return \"SHELTERWD_REM_STEP\"
    elif ACT == \"Shelterwood Seed Step\":
        return \"SHELTERWD_SEED_STEP\"
    elif ACT == \"Single Tree Selection\":
        return \"SINGLE_TREE_SELECTION\"
    elif ACT == \"Site Preparation\":
        return \"SITE_PREP\"
    elif ACT == \"Slash Disposal\":
        return \"SLASH_DISPOSAL\"
    elif ACT == \"Stream Channel Improvement\":
        return \"STREAM_CHNL_IMPRV\"
    elif ACT == \"Transition Harvest\":
        return \"TRANSITION_HARVEST\"
    elif ACT == \"Tree Planting\":
        return \"TREE_PLNTING\"
    elif ACT == \"Tree Release and Weed\":
        return \"TREE_RELEASE_WEED\"
    elif ACT == \"Tree Seeding\":
        return \"TREE_SEEDING\"
    elif ACT == \"Trees Felled (> 6in dbh)\":
        return \"TREE_FELL\"
    elif ACT == \"Variable Retention Harvest\":
        return \"VARIABLE_RETEN_HARVEST\"
    elif ACT == \"Wetland Restoration\":
        return \"WETLAND_RESTOR\"
    elif ACT == \"Wildfire Managed for Resource Benefit\":
        return \"WM_RESRC_BENEFIT\"
    elif ACT == \"Yarding/Skidding\":
        return \"YARDING\"
    elif ACT == \"Not Defined\":
        return \"NOT_DEFINED\"
    else:
        return \"TBD\"""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    return Veg_Summarized_Polygons_Laye3_4_

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(extent="-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]", outputCoordinateSystem="PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]", preserveGlobalIds=True, 
                          qualifiedFieldNames=False, scratchWorkspace=r"C:\Users\sageg\Documents\ArcGIS\Projects\PC414 CWI Million Acres\scratch.gdb", transferDomains=True, 
                          transferGDBAttributeProperties=True, workspace=r"C:\Users\sageg\Documents\ArcGIS\Projects\PC414 CWI Million Acres\PC414 CWI Million Acres.gdb"):
        Activity(*argv[1:])
