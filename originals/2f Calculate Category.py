# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2022-11-29 12:13:46
"""
import arcpy
from sys import argv

def Category(Input_Table):  # 2f Calculate Category

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False


    # Process: Calculate Category (Calculate Field) (management)
    Updated_Input_Table = arcpy.management.CalculateField(in_table=Input_Table, field="ACTIVITY_CAT", expression="ifelse(!ACTIVITY_DESCRIPTION!, !BROAD_VEGETATION_TYPE!, !PRIMARY_OBJECTIVE!)", expression_type="PYTHON3", code_block="""def ifelse(Act, Veg, Obj):
    if Act in [\"CHIPPING\", \"CHAIN_CRUSH\" \"DOZER_LINE\", \"HANDLINE\", \"LANDING_TRT\", \"LOP_AND_SCAT\", \"MASTICATION\", \"MOWING\", \"PILE_BURN\", \"PILING\", \"PRECOM_THIN_MAN\", \"PRECOM_THIN_MECH\", \"PRUNING\", \"SLASH_DISPOSAL\", \"TREE_RELEASE_WEED\", \"TREE_FELL\", \"YARDING\"]:
        return \"MECH_HFR\"
    elif Act in [\"CLEARCUT\", \"COMM_THIN\", \"CONVERSION\", \"GRP_SELECTION_HARVEST\", \"REHAB_UNDRSTK_AREA\", \"SEED_TREE_PREP_STEP\", \"SEED_TREE_REM_STEP\", \"SEED_TREE_SEED_STEP\", \"SHELTERWD_PREP_STEP\", \"SHELTERWD_REM_STEP\", \"SHELTERWD_SEED_STEP\", \"SINGLE_TREE_SELECTION\", \"TRANSITION_HARVEST\", \"VARIABLE_RETEN_HARVEST\"]:
        return \"TIMB_HARV\"
    elif Act == \"SANI_SALVG_HARVEST\":
        return \"SANI_SALVG\"
    elif Act == \"PEST_CNTRL\" and Veg == \"FOREST\":
        return \"SANI_SALVG\"
    elif Act == \"PEST_CNTRL\" and Veg != \"FOREST\":
        return \"WATSHD_IMPRV\"
    elif Act == \"HERBICIDE_APP\" and Obj in [\"FOREST_PEST_CNTRL\", \"FOREST_STEWARDSHIP\", \"OTHER_FOREST_MGMT\", \"REFORESTATION\", \"SITE_PREP\"]:
        return \"TREE_PLNTING\"
    elif Act == \"HERBICIDE_APP\" and Obj in [\"BURNED_AREA_RESTOR\", \"CARBON_STORAGE\", \"ECO_RESTOR\", \"HABITAT_RESTOR\", \"INV_SPECIES_CNTRL\", \"LAND_PROTECTION\", \"MTN_MEADOW_RESTOR\", \"RIPARIAN_RESTOR\", \"WATSHD_RESTOR\", \"WETLAND_RESTOR\"]:
        return \"WATSHD_IMPRV\"
    elif Act == \"HERBICIDE_APP\" and Obj in [\"BIOMASS_UTIL\", \"CULTURAL_BURN\", \"FIRE_PREVENTION\", \"FUEL_BREAK\", \"NON-TIMB_PRODUCTS\", \"OTHER_FUELS_REDUCTION\", \"PRESCRB_FIRE\", \"RECREATION\", \"ROADWAY_CLEARANCE\", \"TIMBER_HARVEST\", \"UTIL_RIGHT_OF_WAY\"]:
        return \"MECH_HFR\"
    elif Act in [\"SITE_PREP\", \"TREE_PLNTING\", \"TREE_SEEDING\"]:
        return \"TREE_PLNTING\"
    elif Act in [\"BROADCAST_BURN\", \"WM_RESRC_BENEFIT\"]:
        return \"BENEFICIAL_FIRE\"
    elif Act == \"PRESCRB_HERBIVORY\":
        return \"GRAZING\"
    elif Act in [\"EASEMENT\", \"LAND_ACQ\"]:
        return \"LAND_PROTEC\"
    elif Act in [\"AMW_AREA_RESTOR\", \"EROSION_CONTROL\", \"HABITAT_REVEG\", \"OAK_WDLND_MGMT\", \"ROAD_OBLITERATION\", \"STREAM_CHNL_IMPRV\", \"WETLAND_RESTOR\"]:
        return \"WATSHD_IMPRV\"
    else:
        return \"NOT_DEFINED\"""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    return Updated_Input_Table

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(extent="-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]", outputCoordinateSystem="PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]", preserveGlobalIds=True, 
                          qualifiedFieldNames=False, scratchWorkspace=r"C:\Users\sageg\Documents\ArcGIS\Projects\PC414 CWI Million Acres\scratch.gdb", transferDomains=True, 
                          transferGDBAttributeProperties=True, workspace=r"C:\Users\sageg\Documents\ArcGIS\Projects\PC414 CWI Million Acres\PC414 CWI Million Acres.gdb"):
        Category(*argv[1:])
