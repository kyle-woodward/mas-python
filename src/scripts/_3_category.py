"""
# Description:  Calculates Activity Category using Activity Description, Broad 
#               Vegetation Type and Primary Objective
#              
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import arcpy
from scripts.utils import init_gdb

workspace, scratch_workspace = init_gdb()


def Category(Input_Table):
    arcpy.env.overwriteOutput = True

    print("      Calculate Activity Category Step 1/1")
    category_calculated = arcpy.management.CalculateField(
        in_table=Input_Table,
        field="ACTIVITY_CAT",
        expression="ifelse(!ACTIVITY_DESCRIPTION!, !BROAD_VEGETATION_TYPE!, !PRIMARY_OBJECTIVE!)",
        expression_type="PYTHON3",
        code_block="""def ifelse(Act, Veg, Obj):
            if Act in ['MECH_HFR', 'BENEFICIAL_FIRE', 'GRAZING', 'LAND_PROTEC',  
            'TIMB_HARV', 'TREE_PLNTING', 'WATSHD_IMPRV']:
                return Act
            if Act in ["BIOMASS_REMOVAL", "CHIPPING", "CHAIN_CRUSH", "DISCING", "DOZER_LINE", "HANDLINE", 
            "LANDING_TRT", "LOP_AND_SCAT", "MASTICATION", "MOWING", "PILE_BURN", "PILING", "PRUNING", 'ROAD_CLEAR',  
            "SLASH_DISPOSAL", "THIN_MAN", "THIN_MECH", "TREE_RELEASE_WEED", "TREE_FELL", "UTIL_RIGHTOFWAY_CLR", "YARDING"]:
                return "MECH_HFR"
            if Act in ["CLEARCUT", "COMM_THIN", "CONVERSION", "GRP_SELECTION_HARVEST", 
            "REHAB_UNDRSTK_AREA", "SEED_TREE_PREP_STEP", "SEED_TREE_REM_STEP", "SEED_TREE_SEED_STEP", 
            "SHELTERWD_PREP_STEP", "SHELTERWD_REM_STEP", "SHELTERWD_SEED_STEP", "SINGLE_TREE_SELECTION", 
            "SP_PRODUCTS", "TRANSITION_HARVEST", "VARIABLE_RETEN_HARVEST"]:
                return "TIMB_HARV"
            if Act in ["SALVG_HARVEST", 'SANI_HARVEST']:
                # return "SANI_SALVG"
                return "TIMB_HARV"
            if Act == "PEST_CNTRL" and Veg == "FOREST":
                return "SANI_SALVG"
            if Act == "PEST_CNTRL" and Veg != "FOREST":
                return "WATSHD_IMPRV"
            if Act in ["INV_PLANT_REMOVAL", "ECO_HAB_RESTORATION"]:
                return "WATSHD_IMPRV"
            if Act == "HERBICIDE_APP" and Obj in ["BURNED_AREA_RESTOR", "CARBON_STORAGE", 
            "ECO_RESTOR", "HABITAT_RESTOR", "INV_SPECIES_CNTRL", "LAND_PROTECTION", 
            "MTN_MEADOW_RESTOR", "RIPARIAN_RESTOR", "WATSHD_RESTOR", "WETLAND_RESTOR"]:
                return "WATSHD_IMPRV"
            if Act == "HERBICIDE_APP" and Obj in ["FOREST_PEST_CNTRL", "FOREST_STEWARDSHIP", 
            "OTHER_FOREST_MGMT", "REFORESTATION", "SITE_PREP"]:
                return "TREE_PLNTING"
            if Act == "HERBICIDE_APP" and Obj in ["BIOMASS_UTIL", "CULTURAL_BURN", 
            "FIRE_PREVENTION", "FUEL_BREAK", "NON-TIMB_PRODUCTS", "OTHER_FUELS_REDUCTION", 
            "PRESCRB_FIRE", "RECREATION", "ROADWAY_CLEARANCE", "TIMBER_HARVEST", "UTIL_RIGHT_OF_WAY"]:
                return "MECH_HFR"
            if Act in ["SITE_PREP", "TREE_PLNTING", "TREE_SEEDING"]:
                return "TREE_PLNTING"
            if Act in ["BROADCAST_BURN", "PL_TREAT_BURNED", "WM_RESRC_BENEFIT"]:
                return "BENEFICIAL_FIRE"
            if Act == "PRESCRB_HERBIVORY":
                return "GRAZING"
            if Act in ["EASEMENT", "FEE_TITLE", "LAND_ACQ"]:
                return "LAND_PROTEC"
            if Act in ["AMW_AREA_RESTOR", "EROSION_CONTROL", "HABITAT_REVEG", 
            "OAK_WDLND_MGMT", "ROAD_OBLITERATION", "SEEDBED_PREP", "STREAM_CHNL_IMPRV", "WETLAND_RESTOR"]:
                return "WATSHD_IMPRV"
            else:
                return \"NOT_DEFINED\"""",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    return category_calculated

