import arcpy
from sys import argv
import os
from scripts.utils import init_gdb, runner
original_gdb, workspace, scratch_workspace = init_gdb()

def Activity(Input_Table):  # 2d Calculate Activity
    """Assign new values to ACTIVITY_DESCRIPTION field in the input table. Requires that Fuels_Treatments_Piles_Crosswalk table is already joined to the input table."""
    arcpy.env.overwriteOutput = True


    # Process: Calculate Activity (Calculate Field) (management)
    Veg_Summarized_Polygons_Laye3_4_ = arcpy.management.CalculateField(in_table=Input_Table, field="ACTIVITY_DESCRIPTION", expression="ifelse(!Fuels_Treatments_Piles_Crosswalk.Activity!)", expression_type="PYTHON3", code_block="""def ifelse(ACT):
    if ACT in [\'AMW_AREA_RESTOR\', 
    \'BIOMASS_REMOVAL\', 
    \'BROADCAST_BURN\', 
    \'CHAIN_CRUSH\', 
    \'CHIPPING\', 
    \'CLEARCUT\', 
    \'COMM_THIN\', 
    \'CONVERSION\', 
    \'DISCING\', 
    \'DOZER_LINE\', 
    \'EASEMENT\', 
    \'ECO_HAB_RESTORATION\', 
    \'EROSION_CONTROL\', 
    \'FEE_TITLE\', 
    \'GRP_SELECTION_HARVEST\', 
    \'HABITAT_REVEG\', 
    \'HANDLINE\', 
    \'HERBICIDE_APP\', 
    \'INV_PLANT_REMOVAL\', 
    \'LAND_ACQ\', 
    \'LANDING_TRT\', 
    \'LOP_AND_SCAT\', 
    \'MASTICATION\', 
    \'MOWING\', 
    \'NOT_DEFINED\', 
    \'OAK_WDLND_MGMT\', 
    \'PEST_CNTRL\', 
    \'PILE_BURN\', 
    \'PILING\', 
    \'PL_TREAT_BURNED\', 
    \'PRESCRB_HERBIVORY\', 
    \'PRUNING\', 
    \'REHAB_UNDRSTK_AREA\', 
    \'ROAD_CLEAR\', 
    \'ROAD_OBLITERATION\', 
    \'SALVG_HARVEST\', 
    \'SANI_HARVEST\', 
    \'SEED_TREE_PREP_STEP\', 
    \'SEED_TREE_REM_STEP\', 
    \'SEED_TREE_SEED_STEP\', 
    \'SEEDBED_PREP\', 
    \'SHELTERWD_PREP_STEP\', 
    \'SHELTERWD_REM_STEP\', 
    \'SHELTERWD_SEED_STEP\', 
    \'SINGLE_TREE_SELECTION\', 
    \'SITE_PREP\', 
    \'SLASH_DISPOSAL\', 
    \'SP_PRODUCTS\', 
    \'STREAM_CHNL_IMPRV\', 
    \'THIN_MAN\', 
    \'THIN_MECH\', 
    \'TRANSITION_HARVEST\', 
    \'TREE_FELL\', 
    \'TREE_PLNTING\', 
    \'TREE_RELEASE_WEED\', 
    \'TREE_SEEDING\', 
    \'UTIL_RIGHTOFWAY_CLR\', 
    \'VARIABLE_RETEN_HARVEST\', 
    \'WETLAND_RESTOR\', 
    \'WM_RESRC_BENEFIT\', 
    \'YARDING\']:
        return ACT
    elif ACT == \"Aspen/Meadow/Wet Area Restoration\":
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
    elif ACT == \"Oak Woodland Management\":
        return \"OAK_WDLND_MGMT\"
    elif ACT == \"Pest Control\":
        return \"PEST_CNTRL\"
    elif ACT == \"Pile Burning\":
        return \"PILE_BURN\"
    elif ACT == \"Piling\":
        return \"PILING\"
    elif ACT ==\"Planned Treatment Burned in Wildfire\":
        return \"PL_TREAT_BURNED\"
    elif ACT == \"Prescribed Herbivory\":
        return \"PRESCRB_HERBIVORY\"
    elif ACT == \"Pruning\":
        return \"PRUNING\"
    elif ACT == \"Rehabilitation of Understocked Area\":
        return \"REHAB_UNDRSTK_AREA\"
    elif ACT == \"Roadway Clearance\":
        return \"ROAD_CLEAR\"
    elif ACT == \"Road Obliteration\":
        return \"ROAD_OBLITERATION\"
    elif ACT == \"Sanitation and Salvage Harvest\":
        return \"SALVG_HARVEST\"
    elif ACT == \"Sanitation Harvest\":
        return \"SALNI_HARVEST\"
    elif ACT == \"Salvage Harvest\":
        return \"SALVG_HARVEST\"
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
    elif ACT == \"Special Products Removal\":
        return \"SP_PRODUCTS\"
    elif ACT == \"Stream Channel Improvement\":
        return \"STREAM_CHNL_IMPRV\"
    elif ACT == \"Thinning (Manual)\":
        return \"THIN_MAN\"
    elif ACT == \"Thinning (Mechanical)\":
        return \"THIN_MECH\"
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
        return \"TBD\"""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")

    return Veg_Summarized_Polygons_Laye3_4_

if __name__ == '__main__':
    # Global Environment settings
    #NOTE: For extent and output_coordinate_system, i had to wrap the whole string value in triple quotes to remove error
    with arcpy.EnvManager(
    extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""", 
    outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""", 
    preserveGlobalIds=True, 
    qualifiedFieldNames=False, 
    scratchWorkspace=scratch_workspace, 
    transferDomains=True, 
    transferGDBAttributeProperties=True, 
    workspace=workspace):
        Activity(*argv[1:])
