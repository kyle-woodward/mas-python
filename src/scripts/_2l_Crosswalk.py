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
from ._2k_keep_fields import KeepFields
from .utils import init_gdb

workspace, scratch_workspace = init_gdb()
# TODO add print steps, rename variables

def Crosswalk(Input_Table):
    arcpy.env.overwriteOutput = True

    # Crosswalk_Table = os.path.join(workspace, "Crosswalk")
    Crosswalk_Table = "C:\\Users\\sageg\\source\\repos\\mas-python\\Interagency Tracking System.gdb\\Crosswalk"
    Output_FC = os.path.join(scratch_workspace, "Cross_Output")

    print("   Calculating Crosswalking Activites...")
    # Process: Add Join (Add Join) (management)
    print("     step 1/7 add join")
    add_join_w_xwalk = arcpy.management.AddJoin(
        in_layer_or_view=Input_Table, 
        in_field="Crosswalk", 
        join_table=Crosswalk_Table, 
        join_field="Original_Activity", 
        # join_type="KEEP_COMMON",
        index_join_fields="INDEX_JOIN_FIELDS"
        )

    print("     step 2/7 copy features")
    # Output = os.path.join(scratch_workspace, "Cross_Output")
    Copy_Join = arcpy.CopyFeatures_management(
        in_features=add_join_w_xwalk, 
        out_feature_class=Output_FC
    )

    # Process: Calculate Activity Description (Calculate Field) (management)
    print("     step 2/7 calculate activities")
    xwalk_activity_description = arcpy.management.CalculateField(
        in_table=Copy_Join,
        field="ACTIVITY_DESCRIPTION",
        expression="!Activity!",
    )

    # Process: Calculate Residue Fate (Calculate Field) (management)
    print("     step 3/7 calculate residue fate field")
    xwalk_residue_fate = arcpy.management.CalculateField(
        in_table=xwalk_activity_description,
        field="RESIDUE_FATE",
        expression="!Residue_Fate_1!",
    )

    # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
    print("     step 4/7 select attribute by layer")
    select_tbd_objective = arcpy.management.SelectLayerByAttribute(
        in_layer_or_view=xwalk_residue_fate,
        where_clause="PRIMARY_OBJECTIVE IS NULL Or PRIMARY_OBJECTIVE = 'TBD'",
    )

    # Process: Calculate Objective (Calculate Field) (management)
    print("     step 5/7 calculating objective...")
    xwalk_primary_objective = arcpy.management.CalculateField(
        in_table=select_tbd_objective,
        field="PRIMARY_OBJECTIVE",
        expression="!Objective!",
    )

    # Process: Select Layer By Attribute (2) (Select Layer By Attribute) (management)
    clear_selection = arcpy.management.SelectLayerByAttribute(
        in_layer_or_view=xwalk_primary_objective, selection_type="CLEAR_SELECTION"
    )

    # # Process: Remove Join (2) (Remove Join) (management)
    # remove_join = arcpy.management.RemoveJoin(in_layer_or_view=clear_selection)

    # # Process: 2f Calculate Category (2f Calculate Category)
    # print("     step 6/7 calculate category")
    # calc_category = Category(Input_Table=remove_join)

    print("     step 7/7 keep fields")
    # Process: 2k Keep Fields (2k Keep Fields)
    final_output_table = KeepFields(Keep_table=clear_selection)

    return final_output_table

