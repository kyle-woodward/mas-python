# -*- coding: utf-8 -*-
"""
"""
import arcpy
import os
from scripts._2f_calculate_category import Category
from scripts._2k_keep_fields import KeepFields
from scripts._2j_standardize_domains import StandardizeDomains
from ._2m_counts_to_mas import CountsToMAS
from sys import argv
from scripts.utils import init_gdb, runner

original_gdb, workspace, scratch_workspace = init_gdb()


def Crosswalk(Input_Table):  # 2l Crosswalk
    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    Crosswalk_Table = os.path.join(workspace, "Fuels_Treatments_Piles_Crosswalk")

    print("   Calculating Crosswalking Activites...")
    # Process: Add Join (Add Join) (management)
    print("     step 1/8 add join")
    add_join_w_xwalk = arcpy.management.AddJoin(
        in_layer_or_view=Input_Table.__str__().format(**locals(), **globals()),
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
        expression="!Fuels_Treatments_Piles_Crosswalk.Activity!",
    )

    # Process: Calculate Residue Fate (Calculate Field) (management)
    print("     step 3/8 calculate residue fate field")
    xwalk_residue_fate = arcpy.management.CalculateField(
        in_table=xwalk_activity_description,
        field="RESIDUE_FATE",
        expression="!Fuels_Treatments_Piles_Crosswalk.Residue_Fate!",
    )

    # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
    print("     step 4/8 select attribute by layer")
    select_tbd_objective = arcpy.management.SelectLayerByAttribute(
        in_layer_or_view=xwalk_counts_to_mas,
        where_clause="PRIMARY_OBJECTIVE IS NULL Or PRIMARY_OBJECTIVE = 'TBD'",
    )

    # Process: Calculate Objective (Calculate Field) (management)
    print("     step 5/8 Calculating Objective...")
    xwalk_primary_objective = arcpy.management.CalculateField(
        in_table=select_tbd_objective,
        field="PRIMARY_OBJECTIVE",
        expression="!Fuels_Treatments_Piles_Crosswalk.Objective!",
    )

    # Process: Select Layer By Attribute (2) (Select Layer By Attribute) (management)
    clear_selection = arcpy.management.SelectLayerByAttribute(
        in_layer_or_view=xwalk_primary_objective, selection_type="CLEAR_SELECTION"
    )

    # Process: Remove Join (2) (Remove Join) (management)
    remove_join = arcpy.management.RemoveJoin(in_layer_or_view=clear_selection)

    # Process: 2f Calculate Category (2f Calculate Category) (PC414CWIMillionAcres)
    print("     step 6/8 calculate category")
    calc_category = Category(Input_Table=remove_join)

    # Process: 2j Standardize Domains (2j Standardize Domains) (PC414CWIMillionAcres)
    print("     step 7/8 standardize domains")
    standardize_domains = StandardizeDomains(Input_Table=calc_category)

    print("     step 8/8 counts towards MAS")
    # Process: 2m Counts to MAS (2m Counts to MAS) (PC414CWIMillionAcres)
    counts_ = CountsToMAS(Input_Table=standardize_domains)
    
    # Process: 2k Keep Fields (2k Keep Fields) (PC414CWIMillionAcres)
    final_output_table = KeepFields(Keep_table=counts_)

    return final_output_table


if __name__ == "__main__":
    runner(workspace, scratch_workspace, Crosswalk, "*argv[1:]")
    # # Global Environment settings
    # with arcpy.EnvManager(extent="-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", outputCoordinateSystem="PROJCS[\"NAD_1983_California_Teale_Albers\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Albers\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",-4000000.0],PARAMETER[\"Central_Meridian\",-120.0],PARAMETER[\"Standard_Parallel_1\",34.0],PARAMETER[\"Standard_Parallel_2\",40.5],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]", preserveGlobalIds=True,
    #                       qualifiedFieldNames=False, scratchWorkspace="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb", transferGDBAttributeProperties=True,
    #                       workspace="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb"):
    #     Crosswalk(*argv[1:])
