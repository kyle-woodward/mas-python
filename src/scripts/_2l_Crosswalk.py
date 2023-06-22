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

    Fuels_Treatments_Piles_Crosswalk = os.path.join(workspace,'Fuels_Treatments_Piles_Crosswalk')

    # Process: Add Join (Add Join) (management)
    add_join_w_xwalk = arcpy.management.AddJoin(in_layer_or_view=Input_Table.__str__().format(**locals(),**globals()), 
                                                      in_field="Crosswalk", 
                                                      join_table=Fuels_Treatments_Piles_Crosswalk, 
                                                      join_field="Original_Activity", 
                                                      join_type="KEEP_COMMON", 
                                                      index_join_fields="INDEX_JOIN_FIELDS")

    # Process: Calculate Activity Description (Calculate Field) (management)
    xwalk_activity_description = arcpy.management.CalculateField(in_table=add_join_w_xwalk, 
                                                             field="ACTIVITY_DESCRIPTION", 
                                                             expression="!Fuels_Treatments_Piles_Crosswalk.Activity!")

    # Process: Calculate Residue Fate (Calculate Field) (management)
    xwalk_residue_fate = arcpy.management.CalculateField(in_table=xwalk_activity_description, 
                                                                    field="RESIDUE_FATE", 
                                                                    expression="!Fuels_Treatments_Piles_Crosswalk.Residue_Fate!")

    # Process: Calculate Counts Towards MAS (Calculate Field) (management)
    xwalk_counts_to_mas = arcpy.management.CalculateField(in_table=xwalk_residue_fate, 
                                                             field="COUNTS_TO_MAS", 
                                                             expression="!Fuels_Treatments_Piles_Crosswalk.Counts_to_MAS!")

    # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
    select_tbd_objective = arcpy.management.SelectLayerByAttribute(in_layer_or_view=xwalk_counts_to_mas, 
                                                                                     where_clause="PRIMARY_OBJECTIVE IS NULL Or PRIMARY_OBJECTIVE = 'TBD'")

    # Process: Calculate Objective (Calculate Field) (management)
    xwalk_primary_objective = arcpy.management.CalculateField(in_table=select_tbd_objective, 
                                                             field="PRIMARY_OBJECTIVE", 
                                                             expression="!Fuels_Treatments_Piles_Crosswalk.Objective!")[0]

    # Process: Select Layer By Attribute (2) (Select Layer By Attribute) (management)
    clear_selection = arcpy.management.SelectLayerByAttribute(in_layer_or_view=xwalk_primary_objective, 
                                                                                         selection_type="CLEAR_SELECTION")

    # Process: Remove Join (2) (Remove Join) (management)
    remove_join = arcpy.management.RemoveJoin(in_layer_or_view=clear_selection)[0]

    # Process: 2f Calculate Category (2f Calculate Category) (PC414CWIMillionAcres)
    calc_category = Category(Input_Table=remove_join)#[0]

    # Process: 2j Standardize Domains (2j Standardize Domains) (PC414CWIMillionAcres)
    standardize_domains = StandardizeDomains(Input_Table=calc_category)#[0]

    # Process: Calculate Counts Towards MAS AC Only (Calculate Field) (management)
    calc_mas_acres = arcpy.management.CalculateField(in_table=standardize_domains, 
                                                             field="COUNTS_TO_MAS", 
                                                             expression="ifelse(!ACTIVITY_UOM!,!ACTIVITY_STATUS!,!Counts_to_MAS!)", 
                                                             code_block="""def ifelse(UOM, Status, Counts):
    if UOM != \"AC\":
        return \"NO\"
    if Status == \"CANCELLED\":
        return \"NO\"
    else:
        return Counts
        """)[0]

    # Process: Calculate Counts Towards MAS AC Only (2) (Calculate Field) (management)
    calc_mas_acres_2 = arcpy.management.CalculateField(in_table=calc_mas_acres, 
                                                             field="COUNTS_TO_MAS", 
                                                             expression="ifelse(!Source!,!IMPLEMENTING_ORG!,!Counts_to_MAS!)", 
                                                             code_block="""def ifelse(Source, Org, Counts):
    if Source == \"PIFIRS\" and Org not in [\"Camp Roberts\", \"California Department of Fish and Wildlife\", \"California State Parks\", \"US Department of Energy\", \"US Military\"]:
        return \"NO\"
    else:
        return Counts
        """)[0]

    # Process: 2k Keep Fields (2k Keep Fields) (PC414CWIMillionAcres)
    final_output_table = KeepFields(input_table=calc_mas_acres_2)#[0]

if __name__ == '__main__':
    runner(workspace,scratch_workspace,Crosswalk, '*argv[1:]')
    # # Global Environment settings
    # with arcpy.EnvManager(extent="-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", outputCoordinateSystem="PROJCS[\"NAD_1983_California_Teale_Albers\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Albers\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",-4000000.0],PARAMETER[\"Central_Meridian\",-120.0],PARAMETER[\"Standard_Parallel_1\",34.0],PARAMETER[\"Standard_Parallel_2\",40.5],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]", preserveGlobalIds=True, 
    #                       qualifiedFieldNames=False, scratchWorkspace="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb", transferGDBAttributeProperties=True, 
    #                       workspace="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb"):
    #     Crosswalk(*argv[1:])
