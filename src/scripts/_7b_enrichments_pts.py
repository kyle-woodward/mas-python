"""
# Description:  Adds vegetation, ownership, county, WUI, Task Force Region, and 
#               year attributes to the dataset.
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import arcpy
from ._2h_calculate_year import Year
from ._2m_counts_to_mas import CountsToMAS
from ._2k_keep_fields import KeepFields
from ._2l_crosswalk import Crosswalk
from .utils import init_gdb

workspace, scratch_workspace = init_gdb()

#TODO add print steps

def enrich_points(
    enrich_pts_out, enrich_pts_in
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

        # define file paths to required input datasets (mostly from a_Reference featuredataset in original GDB)
        Ownership_Layer = os.path.join(workspace,'a_Reference','CALFIRE_Ownership_Update')
        Regions_Layer = os.path.join(workspace,'a_Reference','WFRTF_Regions')
        Veg_Layer = os.path.join(workspace,'a_Reference','Broad_Vegetation_Types')
        WUI_Layer = os.path.join(workspace,'a_Reference','WUI')

        # define file paths to intermediary outputs in scratch gdb
        Pts_enrichment_Copy = os.path.join(scratch_workspace, "Pts_enrichment_Copy")
        Pts_enrichment_Own = os.path.join(scratch_workspace, "Pts_enrichment_Own")
        Pts_enrichment_Region = os.path.join(scratch_workspace, "Pts_enrichment_Region")
        Pts_enrichment_Veg = os.path.join(scratch_workspace, "Pts_enrichment_Veg")
        Pts_enrichment_XY = os.path.join(scratch_workspace, "Pts_enrichment_XY")

        print("Executing Point Enrichments...")
        # Process: Copy Features (Copy Features) (management)
        arcpy.management.CopyFeatures(
            in_features=enrich_pts_in,
            out_feature_class=Pts_enrichment_Copy,
        )

        print("   Calculating WUI...")
        # Process: Select WUI Null (Select Layer By Attribute) (management)
        print("     step 1/18 select layer by attribute")
        Pts_enrichment_Copy_Layer1 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=Pts_enrichment_Copy,
            selection_type="NEW_SELECTION",
            where_clause="IN_WUI IS NULL Or IN_WUI = ''",
            invert_where_clause="",
        )

        print("     step 2/18 intersect WUI")
        # Process: Select WUI Intersect (Select Layer By Location) (management)
        Pts_enrichment_Copy_Layer = arcpy.management.SelectLayerByLocation(
            in_layer=[Pts_enrichment_Copy_Layer1],
            overlap_type="INTERSECT",
            select_features=WUI_Layer,
            search_distance="",
            selection_type="SUBSET_SELECTION",
            invert_spatial_relationship="NOT_INVERT",
        )

        # Process: Calculate In WUI (Calculate Field) (management)
        print(f"     step 3/18 calculate WUI yes")
        Pts_enrichment_Copy_Layer_2_ = arcpy.management.CalculateField(
            in_table=Pts_enrichment_Copy_Layer,
            field="IN_WUI",
            expression='"WUI_AUTO_POP"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Select WUI Null 2 (Select Layer By Attribute) (management)
        print("     step 4/18 select layer by attribute")
        Pts_enrichment_Copy_Layer_3_ = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=Pts_enrichment_Copy_Layer_2_,
            selection_type="NEW_SELECTION",
            where_clause="IN_WUI IS NULL Or IN_WUI = ''",
            invert_where_clause="",
        )

        # Process: Calculate Non WUI (Calculate Field) (management)
        print("     step 5/18 calculate WUI no")
        Pts_enrichment_Copy_Layer_4_ = arcpy.management.CalculateField(
            in_table=Pts_enrichment_Copy_Layer_3_,
            field="IN_WUI",
            expression='"NON-WUI_AUTO_POP"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Clear Selection (Select Layer By Attribute) (management)
        print("     step 6/18 clear selection")
        Treatments_Merge3_California_5_ = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=Pts_enrichment_Copy_Layer_4_,
            selection_type="CLEAR_SELECTION",
            where_clause="",
            invert_where_clause="",
        )

        print("   Calculating Ownership, Counties, and Regions...")
        # Process: Spatial Join (Spatial Join) (analysis)
        print(f"     step 7/18 spatial join ownership")
        arcpy.analysis.SpatialJoin(
            target_features=Treatments_Merge3_California_5_,
            join_features=Ownership_Layer,
            out_feature_class=Pts_enrichment_Own,
            join_operation="JOIN_ONE_TO_ONE",
            join_type="KEEP_ALL",
            field_mapping="",
            match_option="CLOSEST",
            search_radius="",
            distance_field_name="",
        )

        # Process: Spatial Join (2) (Spatial Join) (analysis)
        print(f"     step 8/18 spatial join regions")
        arcpy.analysis.SpatialJoin(
            target_features=Pts_enrichment_Own,
            join_features=Regions_Layer,
            out_feature_class=Pts_enrichment_Region,
            join_operation="JOIN_ONE_TO_ONE",
            join_type="KEEP_ALL",
            field_mapping="",
            match_option="CLOSEST",
            search_radius="",
            distance_field_name="",
        )

        # Process: Spatial Join (3) (Spatial Join) (analysis)
        print(f"     step 9/18 spatial join veg")
        arcpy.analysis.SpatialJoin(
            target_features=Pts_enrichment_Region,
            join_features=Veg_Layer,
            out_feature_class=Pts_enrichment_Veg,
            join_operation="JOIN_ONE_TO_ONE",
            join_type="KEEP_ALL",
            field_mapping="",
            match_option="CLOSEST",
            search_radius="",
            distance_field_name="",
        )

        # Process: Calculate Owner (Calculate Field) (management)
        print(f"     step 10/18 calculate ownership field")
        Veg_Summarized_Point_Laye_3_ = arcpy.management.CalculateField(
            in_table=Pts_enrichment_Veg,
            field="PRIMARY_OWNERSHIP_GROUP",
            expression="!AGNCY_LEV!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate County (Calculate Field) (management)
        print("     step 11/18 calculate county field")
        Veg_Summarized_Point_Laye_4_ = arcpy.management.CalculateField(
            in_table=Veg_Summarized_Point_Laye_3_,
            field="COUNTY",
            expression="!COUNTY_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Region (Calculate Field) (management)
        print("     step 12/18 calculate region field")
        Veg_Summarized_Point_Laye_6_ = arcpy.management.CalculateField(
            in_table=Veg_Summarized_Point_Laye_4_,
            field="REGION",
            expression="!Region_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Veg (Calculate Field) (management)
        print("     step 13/18 calculate veg type")
        Veg_Summarized_Point_Laye_2_ = arcpy.management.CalculateField(
            in_table=Veg_Summarized_Point_Laye_6_,
            field="BROAD_VEGETATION_TYPE",
            expression="!WHR13NAME!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate BVT User Defined (Calculate Field) (management)
        Pts_enrichment_Veg_2_ = arcpy.management.CalculateField(
            in_table=Veg_Summarized_Point_Laye_2_,
            field="BVT_USERD",
            expression='"NO"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        print(f"     step 14/18 initiating crosswalk..")
        # Process: Crosswalk
        crosswalk_table = Crosswalk(Input_Table=Pts_enrichment_Veg_2_)
        print(f"   Crosswalk Complete, Continuing Enrichment..")

        # Process: 2h Calculate Year (2h Calculate Year)
        print("     step 15/18 Calculating Years...")
        Pts_enrichment_Year = Year(Year_Input=crosswalk_table)
        
        #TODO Needed?
        arcpy.CopyFeatures_management(Pts_enrichment_Year, Pts_enrichment_XY)

        # Process: Calculate Geometry Attributes (Calculate Geometry Attributes) (management)
        print(f"     step 16/18 Calculating Latitude and Longitude..")
        Pts_enrichment_Veg_Layer3 = arcpy.CalculateGeometryAttributes_management(
            in_features=Pts_enrichment_XY,
            geometry_property=[
                ["LATITUDE", "POINT_Y"],
                ["LONGITUDE", "POINT_X"]],
            coordinate_system= arcpy.SpatialReference("GCS_WGS_1984"), #4269,
            coordinate_format="DD"
        )

        print("     step 17/18 counts to MAS")
        # Process: 2m Counts to MAS (2m Counts to MAS)
        counts_ = CountsToMAS(Pts_enrichment_Veg_Layer3)

        # # Process: Keep Fields (Delete Field) (management)
        print("     step 18/18 removing unnecessary fields")
        Veg_Summarized_Pts_Laye_11_ = KeepFields(counts_)       
            
        # Process: Select (Select) (analysis)
        arcpy.analysis.Select(
            in_features=Veg_Summarized_Pts_Laye_11_,
            out_feature_class=enrich_pts_out,
            where_clause="" #"County IS NOT NULL",
        )

        print(f"Enrich Points Complete..")

