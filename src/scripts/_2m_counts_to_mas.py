"""
# Description: Part 1 in calculating whether an activity counts towards the
#              Million Acre Strategy.
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import arcpy
from scripts.utils import init_gdb
workspace, scratch_workspace = init_gdb()
# TODO add print steps, rename variables
def CountsToMAS(Input_Table):
    arcpy.env.overwriteOutput = True

    # Process: Calculate No (Calculate Field) (management)
    CDFW_Enriched_Ln_Table_20230801_4_ = arcpy.management.CalculateField(
                        in_table=Input_Table, 
                        field="COUNTS_TO_MAS", 
                        expression="'NO'"
                        )

    # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
    CDFW_Enriched_Ln_Table_20230801_5_, Count = arcpy.management.SelectLayerByAttribute(
                        in_layer_or_view=CDFW_Enriched_Ln_Table_20230801_4_, 
                        where_clause="ACTIVITY_END >= timestamp '2020-01-01 00:00:00' And ACTIVITY_END < timestamp '2023-01-01 00:00:00'"
                        )

    # Process: Calculate Counts (Calculate Field) (management)
    Updated_Input_Table = arcpy.management.CalculateField(
                        in_table=CDFW_Enriched_Ln_Table_20230801_5_, 
                        field="COUNTS_TO_MAS", expression="ifelse(!ACTIVITY_DESCRIPTION!)", code_block="""def ifelse(Act):
                            if Act in ['BIOMASS_REMOVAL',
                            'BROADCAST_BURN',
                            'CHAIN_CRUSH',
                            'CHIPPING',
                            'COMM_THIN',
                            'DISCING',
                            'GRP_SELECTION_HARVEST',
                            'HERBICIDE_APP',
                            'INV_PLANT_REMOVAL',
                            'LANDING_TRT',
                            'LOP_AND_SCAT',
                            'MASTICATION',
                            'MOWING',
                            'OAK_WDLND_MGMT',
                            'PEST_CNTRL',
                            'PILE_BURN',
                            'PILING',
                            'PL_TREAT_BURNED', 
                            'PRESCRB_HERBIVORY',
                            'PRUNING',
                            'REHAB_UNDRSTK_AREA',
                            'ROAD_CLEAR',
                            'SANI_HARVEST',
                            'SINGLE_TREE_SELECTION',
                            'SITE_PREP',
                            'SLASH_DISPOSAL',
                            'SP_PRODUCTS',
                            'THIN_MAN',
                            'THIN_MECH',
                            'TRANSITION_HARVEST',
                            'TREE_FELL',
                            'TREE_PLNTING',
                            'TREE_RELEASE_WEED',
                            'TREE_SEEDING',
                            'UTIL_RIGHTOFWAY_CLR',
                            'VARIABLE_RETEN_HARVEST',
                            'YARDING']:
                                return 'YES'
                            else:
                                return 'NO'"""
                                )

    # Process: Calculate Counts Towards MAS AC Only (Calculate Field) (management)
    Updated_Input_Table_2_ = arcpy.management.CalculateField(
                        in_table=Updated_Input_Table, 
                        field="COUNTS_TO_MAS", expression="ifelse(!ACTIVITY_UOM!,!Counts_to_MAS!)", 
                        code_block="""def ifelse(UOM, Counts):
                            if UOM != \"AC\":
                                return \"NO\"
                            else:
                                return Counts
                                """
                                )

    # Process: Calculate Counts Towards MAS Status (Calculate Field) (management)
    Updated_Input_Table_4_ = arcpy.management.CalculateField(
                        in_table=Updated_Input_Table_2_, 
                        field="COUNTS_TO_MAS", expression="ifelse(!ACTIVITY_STATUS!,!Counts_to_MAS!)", 
                        code_block="""def ifelse(Status, Counts):
                            if Status == \"CANCELLED\" or Status == 'PLANNED' or Status == 'OUTYEAR' or Status == 'PROPOSED':
                                return \"NO\"
                            else:
                                return Counts
                                """
                                )

    # Process: Calculate Counts Towards MAS Watershed Health (Calculate Field) (management)
    Updated_Input_Table_5_ = arcpy.management.CalculateField(
                        in_table=Updated_Input_Table_4_, 
                        field="COUNTS_TO_MAS", expression="ifelse(!ACTIVITY_CAT!,!Counts_to_MAS!)", 
                        code_block="""def ifelse(Cat, Counts):
                            if Cat == 'WATSHD_IMPRV':
                                return \"NO\"
                            else:
                                return Counts"""
                                )

    # Process: Calculate PFIRS (Calculate Field) (management)
    Updated_Input_Table_6_ = arcpy.management.CalculateField(
                        in_table=Updated_Input_Table_5_, 
                        field="COUNTS_TO_MAS", expression="ifelse(!AGENCY!,!ORG_ADMIN_p!,!COUNTS_TO_MAS!)", 
                        code_block="""def ifelse(Agency, Admin, Counts):
                            if Agency == 'OTHER' and Admin == 'CARB':
                                return 'NO'
                            else:
                                return Counts"""
                                )

    # Process: Calculate USFS Active (Calculate Field) (management)
    Updated_Input_Table_3_ = arcpy.management.CalculateField(
                        in_table=Updated_Input_Table_6_, 
                        field="COUNTS_TO_MAS", 
                        expression="ifelse(!ADMINISTERING_ORG!, !ACTIVITY_STATUS!, !COUNTS_TO_MAS!)", 
                        code_block="""def ifelse(org, status, counts):
                            if org == 'USFS' and status == 'ACTIVE':
                                return 'NO'
                            else:
                                return counts"""
                                )

    # Process: Calculate Other Org out (Calculate Field) (management)
    Updated_Input_Table_7_ = arcpy.management.CalculateField(
                        in_table=Updated_Input_Table_3_, 
                        field="COUNTS_TO_MAS", 
                        expression="ifelse(!ADMINISTERING_ORG!,!COUNTS_TO_MAS!)", 
                        code_block="""def ifelse(Admin, Counts):
                            if Admin in ['BOF', 'CCC', 'SMMC', 'SNC', 'SCC', 'SDRC', 'MRCA', 'RMC', 'OTHER']:
                                return 'NO' 
                            else:
                                return Counts"""
                                )

    # Process: Select Layer By Attribute (2) (Select Layer By Attribute) (management)
    counts_final = arcpy.management.SelectLayerByAttribute(
                        in_layer_or_view=Updated_Input_Table_7_, 
                        selection_type="CLEAR_SELECTION"
                        )

    return counts_final

