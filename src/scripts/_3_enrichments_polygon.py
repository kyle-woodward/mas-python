"""
# Description:  Adds vegetation, ownership, county, WUI, Task Force Region, and 
#               year attributes to the dataset.
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import datetime
start_ply = datetime.datetime.now()

import os
import arcpy
from ._3_year import Year
from ._3_keep_fields import KeepFields
from ._3_crosswalk import Crosswalk
from .utils import init_gdb

workspace, scratch_workspace = init_gdb()

def enrich_polygons(
    enrich_in, 
    enrich_out
):
    with arcpy.EnvManager(
        workspace=workspace,
        scratchWorkspace=scratch_workspace, 
        outputCoordinateSystem= arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"), #WKID 3310
        cartographicCoordinateSystem=arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"), #WKID 3310
        extent="xmin=-374900, ymin=-604500, xmax=540100, ymax=450000, spatial_reference='NAD 1983 California (Teale) Albers (Meters)'", 
        preserveGlobalIds=True, 
        qualifiedFieldNames=False, 
        transferDomains=False, 
        transferGDBAttributeProperties=False, 
        overwriteOutput = True
    ):
        print("   Executing Polygon Enrichments...")
        print(f"     Polygon Enrichment Start Time {start_ply}")

        # define file paths to required input datasets (mostly from b_Reference featuredataset in original GDB)
        Veg_Layer = os.path.join(workspace,'a_Reference','Broad_Vegetation_Types')
        WUI_Layer = os.path.join(workspace,'a_Reference','WUI')
        Ownership_Layer = os.path.join(workspace,'a_Reference','CALFIRE_Ownership_Update')
        Regions_Layer = os.path.join(workspace,'a_Reference','WFRTF_Regions')
        
        # define file paths to intermediary outputs in scratch gdb
        veg_sum = os.path.join(scratch_workspace, "Veg_Summarized_Polygons")
        group_table = os.path.join(scratch_workspace, "WHR13NAME_Summary")
        sum_table = os.path.join(scratch_workspace, "WHR13NAME_Summary_SummarizeAttributes")
        Veg_Summarized_Centroids = os.path.join(scratch_workspace, "Veg_Summarized_Centroids")
        Veg_Summarized_Join1_Own = os.path.join(scratch_workspace, "Veg_Summarized_Join1_Own")
        Veg_Summarized_Join2_Region = os.path.join(scratch_workspace, "Veg_Summarized_Join2_Region")
                
        ## BEGIN TOOL CHAIN

        print("     Calculating Broad Vegetation Type...")
        # summarize_1 is the input to summarize_2 and join_2
        print("       enrich step 1/32 summarize veg within polygons")
        summarize_1 = arcpy.analysis.SummarizeWithin(
            in_polygons=enrich_in,
            in_sum_features=Veg_Layer,
            out_feature_class=veg_sum,
            keep_all_polygons="KEEP_ALL",
            sum_fields=None,
            sum_shape="ADD_SHAPE_SUM",
            shape_unit="ACRES",
            group_field="WHR13NAME",
            add_min_maj="NO_MIN_MAJ",
            add_group_percent="NO_PERCENT",
            out_group_table=group_table,
        )

        print("       enrich step 2/32 summarize attributes")
        summarize_2 = arcpy.gapro.SummarizeAttributes(
            input_layer=group_table,
            out_table=sum_table,
            fields=["Join_ID"],
            summary_fields=[["sum_Area_ACRES", "MAX"]],
            time_step_interval=None,
            time_step_repeat=None,
            time_step_reference=None,
        )

        print("       enrich step 3/32 add join")
        join_1 = arcpy.management.AddJoin(
            in_layer_or_view=sum_table,
            in_field="MAX_Sum_Area_ACRES",
            join_table=group_table,
            join_field="sum_Area_ACRES",
            join_type="KEEP_ALL",
            index_join_fields="INDEX_JOIN_FIELDS",
        )

        print("       enrich step 4/32 convert table to table")
        sum_table = arcpy.conversion.TableToTable(
            in_rows=join_1,
            out_path=scratch_workspace,
            out_name="WHR13NAME_Summary_temp",
            where_clause="",
            config_keyword="",
        )

        print("       enrich step 5/32 delete identical")
        delete_identical_1 = arcpy.management.DeleteIdentical(
            in_dataset=sum_table,
            fields=["Join_ID", "MAX_Sum_Area_ACRES", "WHR13NAME"],
            xy_tolerance="",
            z_tolerance=0,
        )

        Count1 = arcpy.management.GetCount(delete_identical_1)
        print("         step has {} records".format(Count1[0]))

        print("       enrich step 6/32 add join")
        join_2 = arcpy.management.AddJoin(
            in_layer_or_view=veg_sum,
            in_field="Join_ID",
            join_table=delete_identical_1,
            join_field="Join_ID",
            join_type="KEEP_ALL",
            index_join_fields="INDEX_JOIN_FIELDS",
        )

        print("       enrich step 7/32 select layer by attribute")
        select_1 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=join_2,
            selection_type="NEW_SELECTION",
            where_clause="BROAD_VEGETATION_TYPE IS NOT NULL",
            invert_where_clause="",
        )

        print("       enrich step 8/32 calculate user defined veg field yes")
        calc_field_1 = arcpy.management.CalculateField(
            in_table=select_1,
            field="BVT_USERD",
            expression='"YES"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        print("       enrich step 9/32 select layer by attribute")
        select_2 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=calc_field_1,
            selection_type="SWITCH_SELECTION",
            where_clause="",
            invert_where_clause="",
        )

        print("       enrich step 10/32 calculate veg domain code")
        calc_field_2 = arcpy.management.CalculateField(
            in_table=select_2,
            field="Veg_Summarized_Polygons.BROAD_VEGETATION_TYPE",
            expression="!WHR13NAME_Summary_temp.WHR13NAME!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS"
        )

        print("       enrich step 11/32 calculate user defined veg field no")
        calc_field_3 = arcpy.management.CalculateField(
            in_table=calc_field_2,
            field="BVT_USERD",
            expression='"NO"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        select_3 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=calc_field_3, 
            selection_type="CLEAR_SELECTION", 
            where_clause="", 
            invert_where_clause=""
        )

        print("       enrich step 12/32 remove join")
        remove_join_1 = arcpy.management.RemoveJoin(
            in_layer_or_view=select_3, join_name="WHR13NAME_Summary_temp"
        )
        Count2 = arcpy.management.GetCount(remove_join_1)
        print("         step has {} records".format(Count2[0]))

        print("     Calculating WUI...")
        print("       enrich step 13/32 select layer by attribute")
        select_4 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=remove_join_1,
            selection_type="NEW_SELECTION",
            where_clause="IN_WUI IS NULL Or IN_WUI = ''",
            invert_where_clause="",
        )

        print("       enrich step 14/32 select layer by WUI location")
        select_5 = arcpy.management.SelectLayerByLocation(
            in_layer=[select_4],
            overlap_type="INTERSECT",
            select_features=WUI_Layer,
            search_distance="",
            selection_type="SUBSET_SELECTION",
            invert_spatial_relationship="NOT_INVERT",
        )

        print("       enrich step 15/32 calculate WUI yes")
        calc_field_4 = arcpy.management.CalculateField(
            in_table=select_5,
            field="IN_WUI",
            expression='"WUI_AUTO_POP"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        print("       enrich step 16/32 select layer by attribute")
        select_6 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=calc_field_4,
            selection_type="NEW_SELECTION",
            where_clause="IN_WUI IS NULL Or IN_WUI = ''",
            invert_where_clause="",
        )

        print("       enrich step 17/32 calculate WUI no")
        calc_field_5 = arcpy.management.CalculateField(
            in_table=select_6,
            field="IN_WUI",
            expression='"NON-WUI_AUTO_POP"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # input to join_3
        print("       enrich step 18/32 clear selection")
        select_7 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=calc_field_5, 
            selection_type="CLEAR_SELECTION", 
            where_clause="", 
            invert_where_clause=""
        )
        
        print("       enrich step 19/32 feature to point")
        to_points = arcpy.management.FeatureToPoint(
            in_features=select_7,
            out_feature_class=Veg_Summarized_Centroids,
            point_location="INSIDE",
        )

        print("     Calculating Ownership, Counties, and Regions...")
        print("       enrich step 20/32 spatial join ownership")
        spatial_join_1 = arcpy.analysis.SpatialJoin(
            target_features=to_points,
            join_features=Ownership_Layer,
            out_feature_class=Veg_Summarized_Join1_Own,
            join_operation="JOIN_ONE_TO_ONE",
            join_type="KEEP_ALL",
            match_option="INTERSECT",
            search_radius="",
            distance_field_name="",
        )

        print("       enrich step 21/32 spatial join veg")
        spatial_join_2 = arcpy.analysis.SpatialJoin(
            target_features=spatial_join_1,
            join_features=Regions_Layer,
            out_feature_class=Veg_Summarized_Join2_Region,
            join_operation="JOIN_ONE_TO_ONE",
            join_type="KEEP_ALL",
            match_option="INTERSECT",
            search_radius="",
            distance_field_name="",
        )

        print("       enrich step 22/32 add join")
        join_3 = arcpy.management.AddJoin(
            in_layer_or_view=select_7,
            in_field="OBJECTID",
            join_table=spatial_join_2,
            join_field="ORIG_FID",
            join_type="KEEP_ALL",
            index_join_fields="INDEX_JOIN_FIELDS",
        )

        print("       enrich step 23/32 calculate ownership field")
        calc_field_6 = arcpy.management.CalculateField(
            in_table=join_3,
            field="Veg_Summarized_Polygons.PRIMARY_OWNERSHIP_GROUP",
            expression="!Veg_Summarized_Join2_Region.AGNCY_LEV!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        print("       enrich step 24/32 calculate county field")
        calc_field_7 = arcpy.management.CalculateField(
            in_table=calc_field_6,
            field="Veg_Summarized_Polygons.COUNTY",
            expression="!Veg_Summarized_Join2_Region.COUNTY_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        print("       enrich step 25/32 calculate region field")
        calc_field_8 = arcpy.management.CalculateField(
            in_table=calc_field_7,
            field="Veg_Summarized_Polygons.REGION",
            expression="!Veg_Summarized_Join2_Region.Region_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        print("       enrich step 26/32 remove join")
        remove_join_2 = arcpy.management.RemoveJoin(
            in_layer_or_view=calc_field_8,
            join_name="Veg_Summarized_Join2_Region",
        )

        calc_field_9 = arcpy.management.CalculateField(
            in_table=remove_join_2, 
            field="TRMT_GEOM", 
            expression="'POLYGON'"
        )

        Count3 = arcpy.management.GetCount(calc_field_9)
        print("         step has {} records".format(Count3[0]))

        print("       enrich step 27/32 Calculating Years...")
        year = Year(Year_Input=calc_field_9)
        
        print("       enrich step 28/32 Initiating Crosswalk...")
        crosswalk_table = Crosswalk(Input_Table=year)
        print("     Crosswalk Complete, Continuing Enrichment...")

        Count4 = arcpy.management.GetCount(crosswalk_table)
        print('         step has {} records'.format(Count4[0]))

        print("       enrich step 29/32 Calculating Latitude and Longitude...")
        calc_geom_1 = arcpy.management.CalculateGeometryAttributes(
            in_features=crosswalk_table,
            geometry_property=[
                ["LATITUDE", "INSIDE_Y"], 
                ["LONGITUDE", "INSIDE_X"]],
            length_unit="",
            area_unit="",
            coordinate_system=4269,  # "GCS_WGS_1984"
            coordinate_format="DD",
        )

        print("       enrich step 30/32 calculate treatment acres")
        calc_geom_2 = arcpy.management.CalculateGeometryAttributes(
            in_features=calc_geom_1,
            geometry_property=[["TREATMENT_AREA", "AREA"]],
            length_unit="",
            area_unit="ACRES_US",
            coordinate_system=3310, # "NAD_1983_California_Teale_Albers"
            coordinate_format="SAME_AS_INPUT",
        )

        print("       enrich step 31/32 removing unnecessary fields")
        keep_fields_1 = KeepFields(calc_geom_2)       
        
        Count5 = arcpy.management.GetCount(keep_fields_1)
        print('         step has {} records'.format(Count5[0]))

        print("       enrich step 32/32") # delete if County is Null")
        select_8 = arcpy.analysis.Select(
            in_features=keep_fields_1,
            out_feature_class=enrich_out,
            where_clause="" # "County IS NOT NULL",
        )

        Count6 = arcpy.management.GetCount(select_8)
        print("         step has {} records".format(Count6[0]))
        
        end_ply = datetime.datetime.now()
        elapsed_ply = (end_ply-start_ply)
        hours, remainder1 = divmod(elapsed_ply.total_seconds(), 3600)
        minutes, remainder2 = divmod(remainder1, 60)
        seconds, remainder3 = divmod(remainder2, 1)
        print("   Enrich Polygons Complete...")
        print(f"     Enrichment Polygon script took: {int(hours)}h, {int(minutes)}m, {seconds}s to complete")

        return enrich_out
