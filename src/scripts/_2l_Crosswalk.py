# -*- coding: utf-8 -*-
"""
"""
import arcpy
import os
from scripts._2f_calculate_category import Category
from scripts._2k_keep_fields import KeepFields
from scripts._2j_Standardize_Domains import StandardizeDomains
from sys import argv
from scripts.utils import init_gdb, runner

original_gdb, workspace, scratch_workspace = init_gdb()

def Crosswalk(Input_Table):  # 2l Crosswalk

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    Crosswalk_Table = os.path.join(workspace,'Fuels_Treatments_Piles_Crosswalk')

    print("   Calculating Crosswalking Activites...")
    # Process: Add Join (Add Join) (management)
    print("     step 1/13 add join")
    add_join_w_xwalk = arcpy.management.AddJoin(in_layer_or_view=Input_Table.__str__().format(**locals(),**globals()), 
                                                      in_field="Crosswalk", 
                                                      join_table=Crosswalk_Table, 
                                                      join_field="Original_Activity", 
                                                      join_type="KEEP_COMMON", 
                                                      index_join_fields="INDEX_JOIN_FIELDS")

    # Process: Calculate Activity Description (Calculate Field) (management)
    print("     step 2/13 calculate activities")
    xwalk_activity_description = arcpy.management.CalculateField(in_table=add_join_w_xwalk, 
                                                             field="ACTIVITY_DESCRIPTION", 
                                                             expression="!Fuels_Treatments_Piles_Crosswalk.Activity!")

    # Process: Calculate Residue Fate (Calculate Field) (management)
    print("     step 3/13 calculate residue fate field")
    xwalk_residue_fate = arcpy.management.CalculateField(in_table=xwalk_activity_description, 
                                                                    field="RESIDUE_FATE", 
                                                                    expression="!Fuels_Treatments_Piles_Crosswalk.Residue_Fate!")

    # Process: Calculate Counts Towards MAS (Calculate Field) (management)
    print("     step 4/13 Counts Towards MAS 1")
    xwalk_counts_to_mas = arcpy.management.CalculateField(in_table=xwalk_residue_fate, 
                                                             field="COUNTS_TO_MAS", 
                                                             expression="!Fuels_Treatments_Piles_Crosswalk.Counts_to_MAS!")

    # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
    print("     step 5/13 select attribute by layer")
    select_tbd_objective = arcpy.management.SelectLayerByAttribute(in_layer_or_view=xwalk_counts_to_mas, 
                                                                     where_clause="PRIMARY_OBJECTIVE IS NULL Or PRIMARY_OBJECTIVE = 'TBD'")

    # Process: Calculate Objective (Calculate Field) (management)
    print('     step 6/13 Calculating Objective...')
    xwalk_primary_objective = arcpy.management.CalculateField(in_table=select_tbd_objective, 
                                                             field="PRIMARY_OBJECTIVE", 
                                                             expression="!Fuels_Treatments_Piles_Crosswalk.Objective!")

    # Process: Select Layer By Attribute (2) (Select Layer By Attribute) (management)
    clear_selection = arcpy.management.SelectLayerByAttribute(in_layer_or_view=xwalk_primary_objective, 
                                                                                         selection_type="CLEAR_SELECTION")

    # Process: Remove Join (2) (Remove Join) (management)
    remove_join = arcpy.management.RemoveJoin(in_layer_or_view=clear_selection)

    # Process: 2f Calculate Category (2f Calculate Category) (PC414CWIMillionAcres)
    print("     step 7/13 calculate category")
    calc_category = Category(Input_Table=remove_join)

    # Process: 2j Standardize Domains (2j Standardize Domains) (PC414CWIMillionAcres)
    print("     step 8/13 standardize domains")
    standardize_domains = StandardizeDomains(Input_Table=calc_category)

    # Process: Calculate Counts Towards MAS PFIRS (Calculate Field) (management)
    print("     step 9/13 Counts Towards MAS 2")
    calc_mas_acres = arcpy.management.CalculateField(in_table=standardize_domains, 
                                                             field="COUNTS_TO_MAS", 
                                                             expression="ifelse(!Source!,!IMPLEMENTING_ORG!,!Counts_to_MAS!)", 
                                                             code_block="""def ifelse(Source, Org, Counts):
                                                                if Source == \"PFIRS\" and Org not in [\"Camp Roberts\", 
                                                                \"California Department of Fish and Wildlife\", 
                                                                \"California State Parks\", 
                                                                \"US Department of Energy\", 
                                                                \"US Military\"]:
                                                                    return \"NO\"
                                                                else:
                                                                    return Counts
                                                                    """)


    # Process: Calculate Counts Towards MAS AC Only (2) (Calculate Field) (management)
    print("     step 10/13 Counts Towards MAS 3")
    calc_mas_acres_2 = arcpy.management.CalculateField(in_table=calc_mas_acres, 
                                                             field="COUNTS_TO_MAS", 
                                                             expression="ifelse(!ACTIVITY_UOM!,!Counts_to_MAS!)", 
                                                             code_block="""def ifelse(UOM, Counts):
                                                                    if UOM != \"AC\":
                                                                        return \"NO\"
                                                                    else:
                                                                        return Counts
                                                                        """)

    # Process: Calculate Counts Towards MAS Status (Calculate Field) (management)
    print("     step 11/13 Counts Towards MAS 4")
    calc_mas_acres_3 = arcpy.management.CalculateField(in_table=calc_mas_acres_2, 
                                                             field="COUNTS_TO_MAS", 
                                                             expression="ifelse(!ACTIVITY_STATUS!,!Counts_to_MAS!)", 
                                                             code_block="""def ifelse(Status, Counts):
                                                                    if Status == \"CANCELLED\":
                                                                        return \"NO\"
                                                                    else:
                                                                        return Counts
                                                                        """)
    
        # Process: Calculate Counts Towards MAS Year (Calculate Field) (management)
    print("     step 12/13 Counts Towards MAS 4")
    calc_mas_acres_4 = arcpy.management.CalculateField(in_table=calc_mas_acres_3, 
                                                             field="COUNTS_TO_MAS", 
                                                             expression="ifelse(!Year!)", 
                                                             code_block="""def ifelse(Year, Counts):
                                                                    if Year < 2020:
                                                                        return \"NO\"
                                                                    if Year > 2022:
                                                                        return \"NO\"
                                                                    if Year is None:
                                                                        return \"NO\"
                                                                    else:
                                                                        return Counts
                                                                        """)
    
    # Process: Calculate Counts Towards MAS Watershed Improvement Category (Calculate Field) (management)
    print("     step 13/13 Counts Towards MAS 5")
    calc_mas_acres_5 = arcpy.management.CalculateField(in_table=calc_mas_acres_4, 
                                                             field="COUNTS_TO_MAS", 
                                                             expression="ifelse(!ACTIVITY_CAT!,!Counts_to_MAS!)", 
                                                             code_block="""def ifelse(ACT, Counts):
                                                                    if ACT == \'WATSHD_IMPRV\':
                                                                        return \"NO\"
                                                                    else:
                                                                        return Counts
                                                                        """)
    
    # Process: Calculate Counts Towards MAS Agency (Calculate Field) (management)
    calc_mas_acres_6 = arcpy.management.CalculateField(in_table=calc_mas_acres_5, 
                                                             field="COUNTS_TO_MAS", 
                                                             expression="ifelse(!AGENCY!,!Counts_to_MAS!)", 
                                                             code_block="""def ifelse(AG, Counts):
                                                                    if AG is None:
                                                                        return \"NO\"
                                                                    if AG == \"OTHER\":
                                                                        return \"NO\"
                                                                    if AG == 'OEIS':
                                                                        return \"NO\"
                                                                    else:
                                                                        return Counts
                                                                        """)
    
    
    # Process: 2k Keep Fields (2k Keep Fields) (PC414CWIMillionAcres)
    final_output_table = KeepFields(Keep_table=calc_mas_acres_6)

    return final_output_table

if __name__ == '__main__':
    runner(workspace,scratch_workspace,Crosswalk, '*argv[1:]')
    # # Global Environment settings
    # with arcpy.EnvManager(extent="-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", outputCoordinateSystem="PROJCS[\"NAD_1983_California_Teale_Albers\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Albers\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",-4000000.0],PARAMETER[\"Central_Meridian\",-120.0],PARAMETER[\"Standard_Parallel_1\",34.0],PARAMETER[\"Standard_Parallel_2\",40.5],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]", preserveGlobalIds=True, 
    #                       qualifiedFieldNames=False, scratchWorkspace="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb", transferGDBAttributeProperties=True, 
    #                       workspace="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb"):
    #     Crosswalk(*argv[1:])
