"""
# Description:  Part 1 in calculating whether an activity counts towards the
#               Million Acre Strategy.  Part 2 is completed during the reporting
#               scripts.
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import arcpy
from scripts.utils import init_gdb

workspace, scratch_workspace = init_gdb()

def CountsToMAS(Input_Table):  
    arcpy.env.overwriteOutput = True

    print("      Calculating 'Counts to MAS'")
    print("        counts step 1/8: set to 'NO'")
    calc_field_1 = arcpy.management.CalculateField(
                                                                        in_table=Input_Table, 
                                                                         field="COUNTS_TO_MAS", expression="'NO'"
                                                                         )

    print("        counts step 2/8: select by bounding years (2020-2023)")
    select_1 = arcpy.management.SelectLayerByAttribute(
                        in_layer_or_view=calc_field_1, 
                        where_clause="ACTIVITY_END >= timestamp '2020-01-01 00:00:00' And ACTIVITY_END < timestamp '2023-01-01 00:00:00'"
                        )

    print("        counts step 3/8: set to 'YES' if activity description is in the list")
    calc_field_2 = arcpy.management.CalculateField(
                        in_table=select_1, 
                        field="COUNTS_TO_MAS", 
                        expression="ifelse(!ACTIVITY_DESCRIPTION!)", 
                        code_block="""def ifelse(Act):
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

    print("        counts step 3/8: set to 'NO' if not 'Acres'")
    calc_field_3 = arcpy.management.CalculateField(
                        in_table=calc_field_2, 
                        field="COUNTS_TO_MAS", expression="ifelse(!ACTIVITY_UOM!,!Counts_to_MAS!)", 
                        code_block="""def ifelse(UOM, Counts):
                            if UOM != \"AC\":
                                return \"NO\"
                            else:
                                return Counts
                                """
                                )

    print("        counts step 4/8: set to 'NO' if status is 'Canceled', 'Planned', 'Outyear', or 'Proposed'")
    calc_field_4 = arcpy.management.CalculateField(
                        in_table=calc_field_3, 
                        field="COUNTS_TO_MAS", expression="ifelse(!ACTIVITY_STATUS!,!Counts_to_MAS!)", 
                        code_block="""def ifelse(Status, Counts):
                            if Status == \"CANCELLED\" or Status == 'PLANNED' or Status == 'OUTYEAR' or Status == 'PROPOSED':
                                return \"NO\"
                            else:
                                return Counts
                                """
                                )

    print("        counts step 5/8: set to 'NO' if Activity Category is 'Watershed Improvement'")
    calc_field_5 = arcpy.management.CalculateField(
                        in_table=calc_field_4, 
                        field="COUNTS_TO_MAS", expression="ifelse(!ACTIVITY_CAT!,!Counts_to_MAS!)", 
                        code_block="""def ifelse(Cat, Counts):
                            if Cat == 'WATSHD_IMPRV':
                                return \"NO\"
                            else:
                                return Counts"""
                                )

    print("        counts step 6/8: set to 'NO' if Agency is 'Other' and Admin is 'CARB'") # aimed at PIFIRS data
    calc_field_6 = arcpy.management.CalculateField(
                        in_table=calc_field_5, 
                        field="COUNTS_TO_MAS", expression="ifelse(!AGENCY!,!ORG_ADMIN_p!,!COUNTS_TO_MAS!)", 
                        code_block="""def ifelse(Agency, Admin, Counts):
                            if Agency == 'OTHER' and Admin == 'CARB':
                                return 'NO'
                            else:
                                return Counts"""
                                )

    print("        counts step 7/8: set to 'NO' if Org is 'USFS' and Status is 'Active'")
    calc_field_7 = arcpy.management.CalculateField(
                        in_table=calc_field_6, 
                        field="COUNTS_TO_MAS", 
                        expression="ifelse(!ADMINISTERING_ORG!, !ACTIVITY_STATUS!, !COUNTS_TO_MAS!)", 
                        code_block="""def ifelse(org, status, counts):
                            if org == 'USFS' and status == 'ACTIVE':
                                return 'NO'
                            else:
                                return counts"""
                                )

    print("        counts step 8/8: set to 'NO' if Admin is in the list")
    calc_field_8 = arcpy.management.CalculateField(
                        in_table=calc_field_7, 
                        field="COUNTS_TO_MAS", 
                        expression="ifelse(!ADMINISTERING_ORG!,!COUNTS_TO_MAS!)", 
                        code_block="""def ifelse(Admin, Counts):
                            if Admin in ['BOF', 'CCC', 'SMMC', 'SNC', 'SCC', 'SDRC', 'MRCA', 'RMC', 'OTHER']:
                                return 'NO' 
                            else:
                                return Counts"""
                                )

    counts_final = arcpy.management.SelectLayerByAttribute(
                        in_layer_or_view=calc_field_8, 
                        selection_type="CLEAR_SELECTION"
                        )

    return counts_final

