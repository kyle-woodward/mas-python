import arcpy
import os
from sys import argv
from scripts.utils import init_gdb, runner
original_gdb, workspace, scratch_workspace = init_gdb()

def CountsToMAS(Input_Table):  # 2m Counts to MAS
    arcpy.env.overwriteOutput = True

    # Process: Calculate No (Calculate Field) (management)
    CDFW_Enriched_Ln_Table_20230801_4_ = arcpy.management.CalculateField(
                                                                        in_table=Input_Table, #.__str__().format(**locals(),**globals()), 
                                                                         field="COUNTS_TO_MAS", expression="'NO'"
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
                            if Admin in ['BOF', 'CCC', 'SMMC', 'SNC', 'SCC', 'SDRC']:
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

if __name__ == '__main__':
    runner(workspace,scratch_workspace,CountsToMAS, '*argv[1:]')
    # Global Environment settings
    # with arcpy.EnvManager(
    # extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""",  outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""", 
    # preserveGlobalIds=True, 
    # qualifiedFieldNames=False, 
    # scratchWorkspace=scratch_workspace, 
    # transferDomains=True, 
    # transferGDBAttributeProperties=True, 
    # workspace=workspace):
        # Year(Input_Table=os.path.join(workspace,"WFR_TF_Template"))
