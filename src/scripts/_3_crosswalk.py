"""
# Description: Utilizes the Crosswalk Table to standardize activity description,
#              activity category, primary objective, residue fate and counts towards
#              Million Acre Strategy from the native dataset into Task Force domain values
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import arcpy
from ._3_category import Category
from ._3_keep_fields import KeepFields
from ._3_standardize_domains import StandardizeDomains
from ._3_counts_to_mas import CountsToMAS
from .utils import init_gdb

workspace, scratch_workspace = init_gdb()

def Crosswalk(Input_Table):
    arcpy.env.overwriteOutput = True

    Crosswalk_Table = os.path.join(workspace, "Crosswalk")

    print("      Calculating Crosswalking Activites...")
    print("          cross step 1/8 add join")
    add_join_w_xwalk = arcpy.management.AddJoin(
        in_layer_or_view=Input_Table,
        in_field="Crosswalk",
        join_table=Crosswalk_Table,
        join_field="Original_Activity",
        join_type="KEEP_COMMON",
        index_join_fields="INDEX_JOIN_FIELDS",
    )

    print("          cross step 2/8 calculate activities")
    calc_field_1 = arcpy.management.CalculateField(
        in_table=add_join_w_xwalk,
        field="ACTIVITY_DESCRIPTION",
        expression="!Crosswalk.Activity!",
    )

    print("          cross step 3/8 calculate residue fate field")
    calc_field_2 = arcpy.management.CalculateField(
        in_table=calc_field_1,
        field="RESIDUE_FATE",
        expression="!Crosswalk.Residue_Fate!",
    )

    print("          cross step 4/8 select attribute by layer")
    select_1 = arcpy.management.SelectLayerByAttribute(
        in_layer_or_view=calc_field_2,
        where_clause="PRIMARY_OBJECTIVE IS NULL Or PRIMARY_OBJECTIVE = 'TBD'",
    )

    print("          cross step 5/8 calculating objective...")
    calc_field_3 = arcpy.management.CalculateField(
        in_table=select_1,
        field="PRIMARY_OBJECTIVE",
        expression="!Crosswalk.Objective!",
    )

    clear_selection = arcpy.management.SelectLayerByAttribute(
        in_layer_or_view=calc_field_3, selection_type="CLEAR_SELECTION"
    )

    remove_join = arcpy.management.RemoveJoin(in_layer_or_view=clear_selection)

    print("          cross step 6/8 calculate category")
    calc_category = Category(Input_Table=remove_join)

    print("          cross step 7/8 standardize domains")
    standardize_domains = StandardizeDomains(Input_Table=calc_category)

    print("          cross step 8/8 counts towards MAS")
    counts_1 = CountsToMAS(Input_Table=standardize_domains)
    
    final_output_table = KeepFields(Keep_table=counts_1)

    return final_output_table

