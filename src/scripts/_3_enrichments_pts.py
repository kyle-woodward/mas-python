"""
# Description:  Adds vegetation, ownership, county, WUI, Task Force Region, and 
#               year attributes to the dataset.
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import datetime
start_pt = datetime.datetime.now()

import os
import arcpy
from ._3_year import Year
from ._3_keep_fields import KeepFields
from ._3_crosswalk import Crosswalk
from .utils import init_gdb

workspace, scratch_workspace = init_gdb()


def enrich_points(
    enrich_pts_in,
    enrich_pts_out
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
        overwriteOutput = True,
    ):
        print("   Executing Point Enrichments...")
        print(f"     Point Enrichment Start Time {start_pt}")

        # define file paths to required input datasets (mostly from b_Reference featuredataset in original GDB)
        WUI_Layer = os.path.join(workspace,'a_Reference','WUI')
        Ownership_Layer = os.path.join(workspace,'a_Reference','CALFIRE_Ownership_Update')
        Regions_Layer = os.path.join(workspace,'a_Reference','WFRTF_Regions')
        Veg_Layer = os.path.join(workspace,'a_Reference','Broad_Vegetation_Types')

        # define file paths to intermediary outputs in scratch gdb
        Pts_enrichment_copy = os.path.join(scratch_workspace, "Pts_enrichment_copy")
        Pts_enrichment_Own = os.path.join(scratch_workspace, "Pts_enrichment_Own")
        Pts_enrichment_Region = os.path.join(scratch_workspace, "Pts_enrichment_Region")
        Pts_enrichment_Veg = os.path.join(scratch_workspace, "Pts_enrichment_Veg")
        Pts_enrichment_XY = os.path.join(scratch_workspace, "Pts_enrichment_XY")

        ## BEGIN TOOL CHAIN
        arcpy.management.CopyFeatures(
            in_features=enrich_pts_in,
            out_feature_class=Pts_enrichment_copy,
        )

        print("     Calculating WUI...")
        print("       enrich step 1/16 select layer by WUI")
        select_1 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=Pts_enrichment_copy,
            selection_type="NEW_SELECTION",
            where_clause="IN_WUI IS NULL Or IN_WUI = ''",
            invert_where_clause="",
        )

        select_2 = arcpy.management.SelectLayerByLocation(
            in_layer=[select_1],
            overlap_type="INTERSECT",
            select_features=WUI_Layer,
            search_distance="",
            selection_type="SUBSET_SELECTION",
            invert_spatial_relationship="NOT_INVERT",
        )

        print("       enrich step 2/16 calculate WUI yes")
        calc_field_1 = arcpy.management.CalculateField(
            in_table=select_2,
            field="IN_WUI",
            expression='"WUI_AUTO_POP"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        print("       enrich step 3/16 switch selection")
        select_3 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=calc_field_1,
            selection_type="NEW_SELECTION",
            where_clause="IN_WUI IS NULL Or IN_WUI = ''",
            invert_where_clause="",
        )

        print("       enrich step 4/16 calculate WUI no")
        calc_field_2 = arcpy.management.CalculateField(
            in_table=select_3,
            field="IN_WUI",
            expression='"NON-WUI_AUTO_POP"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        print("       enrich step 5/16 clear selection")
        select_4 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=calc_field_2,
            selection_type="CLEAR_SELECTION",
            where_clause="",
            invert_where_clause="",
        )

        print("     Calculating Ownership, Counties, and Regions...")
        print("       enrich step 6/16 spatial join ownership")
        join_1 = arcpy.analysis.SpatialJoin(
            target_features=select_4,
            join_features=Ownership_Layer,
            out_feature_class=Pts_enrichment_Own,
            join_operation="JOIN_ONE_TO_ONE",
            join_type="KEEP_ALL",
            field_mapping="",
            match_option="CLOSEST",
            search_radius="",
            distance_field_name="",
        )

        print("       enrich step 7/16 spatial join regions")
        join_2 = arcpy.analysis.SpatialJoin(
            target_features=join_1,
            join_features=Regions_Layer,
            out_feature_class=Pts_enrichment_Region,
            join_operation="JOIN_ONE_TO_ONE",
            join_type="KEEP_ALL",
            field_mapping="",
            match_option="CLOSEST",
            search_radius="",
            distance_field_name="",
        )

        print("       enrich step 8/16 spatial join veg")
        join_3 = arcpy.analysis.SpatialJoin(
            target_features=join_2,
            join_features=Veg_Layer,
            out_feature_class=Pts_enrichment_Veg,
            join_operation="JOIN_ONE_TO_ONE",
            join_type="KEEP_ALL",
            field_mapping="",
            match_option="CLOSEST",
            search_radius="",
            distance_field_name="",
        )

        print("       enrich step 9/16 calculate ownership")
        calc_field_3 = arcpy.management.CalculateField(
            in_table=join_3,
            field="PRIMARY_OWNERSHIP_GROUP",
            expression="!AGNCY_LEV!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        print("       enrich step 10/16 calculate county")
        calc_field_4 = arcpy.management.CalculateField(
            in_table=calc_field_3,
            field="COUNTY",
            expression="!COUNTY_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        print("       enrich step 11/16 calculate region")
        calc_field_5 = arcpy.management.CalculateField(
            in_table=calc_field_4,
            field="REGION",
            expression="!Region_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        print("       enrich step 12/16 calculate veg type")
        calc_field_6 = arcpy.management.CalculateField(
            in_table=calc_field_5,
            field="BROAD_VEGETATION_TYPE",
            expression="!WHR13NAME!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_7 = arcpy.management.CalculateField(
            in_table=calc_field_6,
            field="BVT_USERD",
            expression='"NO"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        print("       enrich step 13/16 Initiating Crosswalk")
        crosswalk_table = Crosswalk(Input_Table=calc_field_7)
        print("     Crosswalk Complete, Continuing Enrichment")

        print("       enrich step 14/16 Calculating Years")
        Pts_enrichment_Year = Year(Year_Input=crosswalk_table)
        arcpy.CopyFeatures_management(Pts_enrichment_Year,Pts_enrichment_XY)

        print("       enrich step 15/16 Calculating Latitude and Longitude")
        calc_geom_1 = arcpy.CalculateGeometryAttributes_management(
            in_features=Pts_enrichment_XY,
            geometry_property=[
                ["LATITUDE", "POINT_Y"],
                ["LONGITUDE", "POINT_X"],
            ],
            coordinate_system= 4269,  # "GCS_WGS_1984"
            coordinate_format="DD"
        )

        calc_field_8 = arcpy.management.CalculateField(
            in_table=calc_geom_1, 
            field="TRMT_GEOM", 
            expression="'POINT'"
        )

        print("       enrich step 16/16 removing unnecessary fields")
        keep_fields_1 = KeepFields(calc_field_8)       
            
        arcpy.analysis.Select(
            in_features=keep_fields_1,
            out_feature_class=enrich_pts_out,
            where_clause="" #"County IS NOT NULL",
        )

        end_pt = datetime.datetime.now()
        elapsed_pt = (end_pt-start_pt)
        hours, remainder1 = divmod(elapsed_pt.total_seconds(), 3600)
        minutes, remainder2 = divmod(remainder1, 60)
        seconds, remainder3 = divmod(remainder2, 1)
        print("   Enrich Points Complete...")
        print(f"     Enrichment Points script took: {int(hours)}h, {int(minutes)}m, {seconds}s to complete")

        return enrich_pts_out


