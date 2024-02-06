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
from ._3_calculate_category import Category
from ._3_keep_fields import KeepFields
from ._4_Standardize_Domains import StandardizeDomains
from ._4_counts_to_mas import CountsToMAS
from .utils import init_gdb

workspace, scratch_workspace = init_gdb()

def Crosswalk(Input_Table):
    arcpy.env.overwriteOutput = True

    Crosswalk_Table = os.path.join(workspace, "Crosswalk")

    print("   Calculating Crosswalking Activites...")
    # Process: Add Join (Add Join) (management)
    print("     step 1/8 add join")
    add_join_w_xwalk = arcpy.management.AddJoin(
        in_layer_or_view=Input_Table,
        in_field="Crosswalk",
        join_table=Crosswalk_Table,
        join_field="Original_Activity",
        join_type="KEEP_COMMON",
        index_join_fields="INDEX_JOIN_FIELDS",
    )

    # Process: Calculate Activity Description (Calculate Field) (management)
    print("     step 2/8 calculate activities")
    xwalk_activity_description = arcpy.management.CalculateField(
        in_table=add_join_w_xwalk,
        field="ACTIVITY_DESCRIPTION",
        expression="!Crosswalk.Activity!",
    )

    # Process: Calculate Residue Fate (Calculate Field) (management)
    print("     step 3/8 calculate residue fate field")
    xwalk_residue_fate = arcpy.management.CalculateField(
        in_table=xwalk_activity_description,
        field="RESIDUE_FATE",
        expression="!Crosswalk.Residue_Fate!",
    )

    # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
    print("     step 4/8 select attribute by layer")
    select_tbd_objective = arcpy.management.SelectLayerByAttribute(
        in_layer_or_view=xwalk_residue_fate,
        where_clause="PRIMARY_OBJECTIVE IS NULL Or PRIMARY_OBJECTIVE = 'TBD'",
    )

    # Process: Calculate Objective (Calculate Field) (management)
    print("     step 5/8 calculating objective...")
    xwalk_primary_objective = arcpy.management.CalculateField(
        in_table=select_tbd_objective,
        field="PRIMARY_OBJECTIVE",
        expression="!Crosswalk.Objective!",
    )

    # Process: Select Layer By Attribute (2) (Select Layer By Attribute) (management)
    clear_selection = arcpy.management.SelectLayerByAttribute(
        in_layer_or_view=xwalk_primary_objective, selection_type="CLEAR_SELECTION"
    )

    # Process: Remove Join (2) (Remove Join) (management)
    remove_join = arcpy.management.RemoveJoin(in_layer_or_view=clear_selection)

    # Process: 2f Calculate Category (2f Calculate Category)
    print("     step 6/8 calculate category")
    calc_category = Category(Input_Table=remove_join)

    # Process: 2j Standardize Domains (2j Standardize Domains)
    print("     step 7/8 standardize domains")
    standardize_domains = StandardizeDomains(Input_Table=calc_category)

    print("     step 8/8 counts towards MAS")
    # Process: 2m Counts to MAS (2m Counts to MAS)
    counts_ = CountsToMAS(Input_Table=standardize_domains)
    
    # Process: 2k Keep Fields (2k Keep Fields)
    final_output_table = KeepFields(Keep_table=counts_)

    return final_output_table

