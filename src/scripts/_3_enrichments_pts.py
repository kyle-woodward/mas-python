"""
# Description:  Adds vegetation, ownership, county, WUI, Task Force Region, and 
#               year attributes to the dataset.
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import arcpy
from ._3_calculate_year import Year
from ._3_keep_fields import KeepFields
from ._3_crosswalk import Crosswalk
from .utils import init_gdb

workspace, scratch_workspace = init_gdb()
#TODO add print steps

def enrich_points(
    enrich_pts_out, enrich_pts_in #, delete_scratch=False
):  
    
    with arcpy.EnvManager(
        outputCoordinateSystem= arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"), #WKID 3310
        cartographicCoordinateSystem=arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"), #WKID 3310
        extent="""450000, -374900, 540100, -604500,
                  DATUM["NAD 1983 California (Teale) Albers (Meters)"]""",
        preserveGlobalIds=True, 
        qualifiedFieldNames=False, 
        scratchWorkspace=scratch_workspace, 
        transferDomains=False, 
        transferGDBAttributeProperties=True, 
        workspace=workspace,
        overwriteOutput = True,
    ):

        # Fuels_Treatments_Piles_Crosswalk = os.path.join(
        #     workspace, "Fuels_Treatments_Piles_Crosswalk"
        # )

        # define file paths to required input datasets (mostly from b_Reference featuredataset in original GDB)
        WUI_Layer = os.path.join(workspace,'b_Reference','WUI')
        Ownership_Layer = os.path.join(workspace,'b_Reference','CALFIRE_Ownership_Update')
        Regions_Layer = os.path.join(workspace,'b_Reference','WFRTF_Regions')
        Veg_Layer = os.path.join(workspace,'b_Reference','Broad_Vegetation_Types')

        # define file paths to intermediary outputs in scratch gdb
        Pts_enrichment_copy = os.path.join(scratch_workspace, "Pts_enrichment_copy")
        Pts_enrichment_Own = os.path.join(scratch_workspace, "Pts_enrichment_Own")
        Pts_enrichment_Region = os.path.join(scratch_workspace, "Pts_enrichment_Region")
        Pts_enrichment_Veg = os.path.join(scratch_workspace, "Pts_enrichment_Veg")
        Pts_enrichment_XY = os.path.join(scratch_workspace, "Pts_enrichment_XY")

        print("Executing Point Enrichments...")
        # Process: Copy Features (Copy Features) (management)
        arcpy.management.CopyFeatures(
            in_features=enrich_pts_in,
            out_feature_class=Pts_enrichment_copy,
            config_keyword="",
            spatial_grid_1=None,
            spatial_grid_2=None,
            spatial_grid_3=None,
        )

        print("   Calculating WUI...")
        # Process: Select WUI Null (Select Layer By Attribute) (management)
        print("     step 13/34 select layer by attribute")
        Pts_enrichment_copy_Layer1 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=Pts_enrichment_copy,
            selection_type="NEW_SELECTION",
            where_clause="IN_WUI IS NULL Or IN_WUI = ''",
            invert_where_clause="",
        )

        # Process: Select WUI Intersect (Select Layer By Location) (management)
        Pts_enrichment_copy_Layer = arcpy.management.SelectLayerByLocation(
            in_layer=[Pts_enrichment_copy_Layer1],
            overlap_type="INTERSECT",
            select_features=WUI_Layer,
            search_distance="",
            selection_type="SUBSET_SELECTION",
            invert_spatial_relationship="NOT_INVERT",
        )

        # Process: Calculate In WUI (Calculate Field) (management)
        print("     step 15/34 calculate WUI yes")
        Pts_enrichment_copy_Layer_2_ = arcpy.management.CalculateField(
            in_table=Pts_enrichment_copy_Layer,
            field="IN_WUI",
            expression='"WUI_AUTO_POP"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Select WUI Null 2 (Select Layer By Attribute) (management)
        print("     step 16/34 select layer by attribute")
        Pts_enrichment_copy_Layer_3_ = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=Pts_enrichment_copy_Layer_2_,
            selection_type="NEW_SELECTION",
            where_clause="IN_WUI IS NULL Or IN_WUI = ''",
            invert_where_clause="",
        )

        # Process: Calculate Non WUI (Calculate Field) (management)
        print("     step 17/34 calculate WUI no")
        Pts_enrichment_copy_Layer_4_ = arcpy.management.CalculateField(
            in_table=Pts_enrichment_copy_Layer_3_,
            field="IN_WUI",
            expression='"NON-WUI_AUTO_POP"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Clear Selection (Select Layer By Attribute) (management)
        print("     step 18/34 clear selection")
        Treatments_Merge3_California_5_ = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=Pts_enrichment_copy_Layer_4_,
            selection_type="CLEAR_SELECTION",
            where_clause="",
            invert_where_clause="",
        )

        print("   Calculating Ownership, Counties, and Regions...")
        # Process: Spatial Join (Spatial Join) (analysis)
        print("     step 20/34 spatial join ownership")
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
        print("     step 21/34 spatial join regions")
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
        print("     step 21/34 spatial join veg")
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
        print("     step 23/34 calculate ownership field")
        Veg_Summarized_Point_Laye_3_ = arcpy.management.CalculateField(
            in_table=Pts_enrichment_Veg,
            field="PRIMARY_OWNERSHIP_GROUP",
            expression="!AGNCY_LEV!",
            # expression="ifelse(!AGNCY_LEV!)",
            expression_type="PYTHON3",
            code_block="",
            # code_block="""def ifelse(Own):
            #     if Own == \"Federal\":
            #         return \"FEDERAL\"
            #     if Own == \"Local\":
            #         return \"LOCAL\"
            #     if Own == \"NGO\":
            #         return \"NGO\"
            #     if Own == \"Private - Industrial\":
            #         return \"PRIVATE_INDUSTRY\"
            #     if Own == \"Private - Non Industrial\":
            #         return \"PRIVATE_NON-INDUSTRY\"
            #     if Own == \"Private - Non-Industrial\":
            #         return \"PRIVATE_NON-INDUSTRY\"
            #     if Own == \"State\":
            #         return \"STATE\"
            #     if Own == \"Tribal\":
            #         return \"TRIBAL\"
            #     else:
            #         return Own""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate County (Calculate Field) (management)
        print("     step 24/34 calculate county field")
        Veg_Summarized_Point_Laye_4_ = arcpy.management.CalculateField(
            in_table=Veg_Summarized_Point_Laye_3_,
            field="COUNTY",
            expression="!COUNTY_1!",
            # expression="ifelse(!COUNTY_1!)",
            expression_type="PYTHON3",
            code_block="",
            # code_block="""def ifelse(CO):
            #     if CO == \"Alameda\":
            #         return \"ALA\"
            #     if CO == \"Alpine\":
            #         return \"ALP\"
            #     if CO == \"Amador\":
            #         return \"AMA\"
            #     if CO == \"Butte\":
            #         return \"BUT\"
            #     if CO == \"Calaveras\":
            #         return \"CAL\"
            #     if CO == \"Colusa\":
            #         return \"COL\"
            #     if CO == \"Contra Costa\":
            #         return \"CC\"
            #     if CO == \"Del Norte\":
            #         return \"DN\"
            #     if CO == \"El Dorado\":
            #         return \"ED\"
            #     if CO == \"Fresno\":
            #         return \"FRE\"
            #     if CO == \"Glenn\":
            #         return \"GLE\"
            #     if CO == \"Humboldt\":
            #         return \"HUM\"
            #     if CO == \"Imperial\":
            #         return \"IMP\"
            #     if CO == \"Inyo\":
            #         return \"INY\"
            #     if CO == \"Kern\":
            #         return \"KER\"
            #     if CO == \"Kings\":
            #         return \"KIN\"
            #     if CO == \"Lake\":
            #         return \"LAK\"
            #     if CO == \"Lassen\":
            #         return \"LAS\"
            #     if CO == \"Los Angeles\":
            #         return \"LA\"
            #     if CO == \"Madera\":
            #         return \"MAD\"
            #     if CO == \"Marin\":
            #         return \"MRN\"
            #     if CO == \"Mariposa\":
            #         return \"MPA\"
            #     if CO == \"Mendocino\":
            #         return \"MEN\"
            #     if CO == \"Merced\":
            #         return \"MER\"
            #     if CO == \"Modoc\":
            #         return \"MOD\"
            #     if CO == \"Monterey\":
            #         return \"MON\"
            #     if CO == \"Mono\":
            #         return \"MNO\"
            #     if CO == \"Napa\":
            #         return \"NAP\"
            #     if CO == \"Nevada\":
            #         return \"NEV\"
            #     if CO == \"Orange\":
            #         return \"ORA\"
            #     if CO == \"Placer\":
            #         return \"PLA\"
            #     if CO == \"Plumas\":
            #         return \"PLU\"
            #     if CO == \"Riverside\":
            #         return \"RIV\"
            #     if CO == \"Sacramento\":
            #         return \"SAC\"
            #     if CO == \"San Benito\":
            #         return \"SBT\"
            #     if CO == \"San Bernardino\":
            #         return \"SBD\"
            #     if CO == \"San Diego\":
            #         return \"SD\"
            #     if CO == \"San Francisco\":
            #         return \"SF\"
            #     if CO == \"San Joaquin\":
            #         return \"SJ\"
            #     if CO == \"San Luis Obispo\":
            #         return \"SLO\"
            #     if CO == \"San Mateo\":
            #         return \"SM\"
            #     if CO == \"Santa Barbara\":
            #         return \"SB\"
            #     if CO == \"Santa Clara\":
            #         return \"SCL\"
            #     if CO == \"Santa Cruz\":
            #         return \"SCR\"
            #     if CO == \"Shasta\":
            #         return \"SHA\"
            #     if CO == \"Sierra\":
            #         return \"SIE\"
            #     if CO == \"Siskiyou\":
            #         return \"SIS\"
            #     if CO == \"Solano\":
            #         return \"SOL\"
            #     if CO == \"Sonoma\":
            #         return \"SON\"
            #     if CO == \"Stanislaus\":
            #         return \"STA\"
            #     if CO == \"Sutter\":
            #         return \"SUT\"
            #     if CO == \"Tehama\":
            #         return \"TEH\"
            #     if CO == \"Tuolumne\":
            #         return \"TUO\"
            #     if CO == \"Trinity\":
            #         return \"TRI\"
            #     if CO == \"Tulare\":
            #         return \"TUL\"
            #     if CO == \"Ventura\":
            #         return \"VEN\"
            #     if CO == \"Yolo\":
            #         return \"YOL\"
            #     if CO == \"Yuba\":
            #         return \"YUB\"
            #     else:
            #         return CO
            # """,
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Region (Calculate Field) (management)
        print("     step 25/34 calculate region field")
        Veg_Summarized_Point_Laye_6_ = arcpy.management.CalculateField(
            in_table=Veg_Summarized_Point_Laye_4_,
            field="REGION",
            expression="!Region!",
            # expression="ifelse(!RFFC_tier1!)",
            expression_type="PYTHON3",
            code_block="",
            # code_block="""def ifelse(Reg):
            #     if Reg == \"Central Coast\":
            #         return \"CENTRAL_COAST\"
            #     if Reg == \"North Coast\":
            #         return \"NORTH_COAST\"
            #     if Reg == \"Sierra Nevada\":
            #         return \"SIERRA_NEVADA\"
            #     if Reg == \"Southern California\":
            #         return \"SOUTHERN_CA\"
            #     else:
            #         return Reg""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Veg (Calculate Field) (management)
        print("     step 25/34 calculate veg type")
        Veg_Summarized_Point_Laye_2_ = arcpy.management.CalculateField(
            in_table=Veg_Summarized_Point_Laye_6_,
            field="BROAD_VEGETATION_TYPE",
            expression="!WHR13NAME!",
            # expression="ifelse(!WHR13NAME!)",
            expression_type="PYTHON3",
            code_block="",
            # code_block="""def ifelse(VEG):
            #     if VEG == \"Agriculture\":
            #         return \"AGRICULTURE\"
            #     elif VEG == \"Barren/Other\":
            #         return \"SPARSE\"
            #     elif VEG == \"Conifer Forest\":
            #         return \"FOREST\"
            #     elif VEG == \"Conifer Woodland\":
            #         return \"FOREST\"
            #     elif VEG == \"Desert Shrub\":
            #         return \"SHRB_CHAP\"
            #     elif VEG == \"Desert Woodland\":
            #         return \"FOREST\"
            #     elif VEG == \"Hardwood Forest\":
            #         return \"FOREST\"
            #     elif VEG == \"Hardwood Woodland\":
            #         return \"FOREST\"
            #     elif VEG == \"Herbaceous\":
            #         return \"GRASS_HERB\"
            #     elif VEG == \"Shrub\":
            #         return \"SHRB_CHAP\"
            #     elif VEG == \"Urban\":
            #         return \"URBAN\"
            #     elif VEG == \"Water\":
            #         return \"WATER\"
            #     elif VEG == \"Wetland\":
            #         return \"WETLAND\"
            #     else:
            #         return VEG""",
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

        print("   step 28/34 Initiating Crosswalk...")
        # Process: Crosswalk
        crosswalk_table = Crosswalk(Input_Table=Pts_enrichment_Veg_2_)
        print("   Crosswalk Complete, Continuing Enrichment...")

        # Process: 2h Calculate Year (2h Calculate Year) (PC414CWIMillionAcres)
        print("     step 27/34 Calculating Years...")
        Pts_enrichment_Year = Year(Year_Input=crosswalk_table)
        arcpy.CopyFeatures_management(Pts_enrichment_Year,Pts_enrichment_XY)

        # Process: Calculate Geometry Attributes (Calculate Geometry Attributes) (management)
        print("     step 29/34 Calculating Latitude and Longitude...")
        Pts_enrichment_Veg_Layer3 = arcpy.CalculateGeometryAttributes_management(
            in_features=Pts_enrichment_XY,
            geometry_property=[
                ["LATITUDE", "POINT_Y"],
                ["LONGITUDE", "POINT_X"],
            ],
            coordinate_system= 4269,  #GCS_North_American_1983 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]',
            coordinate_format="DD"
        )

        # # Process: Delete Identical (Delete Identical) (management)
        # Pts_enrichment_Veg_Layer4 = arcpy.management.DeleteIdentical(
        #     in_dataset=Pts_enrichment_Veg_Layer3,
        #     fields=[
        #         "PROJECTID_USER",
        #         "AGENCY",
        #         "ORG_ADMIN_p",
        #         "PROJECT_CONTACT",
        #         "PROJECT_EMAIL",
        #         "ADMINISTERING_ORG",
        #         "PROJECT_NAME",
        #         "PROJECT_STATUS",
        #         "PROJECT_START",
        #         "PROJECT_END",
        #         "PRIMARY_FUNDING_SOURCE",
        #         "PRIMARY_FUNDING_ORG",
        #         "IMPLEMENTING_ORG",
        #         "LATITUDE",
        #         "LONGITUDE",
        #         "BatchID_p",
        #         "Val_Status_p",
        #         "Val_Message_p",
        #         "Val_RunDate_p",
        #         "Review_Status_p",
        #         "Review_Message_p",
        #         "Review_RunDate_p",
        #         "Dataload_Status_p",
        #         "Dataload_Msg_p",
        #         "TRMTID_USER",
        #         "PROJECTID",
        #         "PROJECTNAME_",
        #         "ORG_ADMIN_t",
        #         "PRIMARY_OWNERSHIP_GROUP",
        #         "PRIMARY_OBJECTIVE",
        #         "SECONDARY_OBJECTIVE",
        #         "TERTIARY_OBJECTIVE",
        #         "TREATMENT_STATUS",
        #         "COUNTY",
        #         "IN_WUI",
        #         "REGION",
        #         "TREATMENT_AREA",
        #         "TREATMENT_START",
        #         "TREATMENT_END",
        #         "RETREATMENT_DATE_EST",
        #         "TREATMENT_NAME",
        #         "BatchID",
        #         "Val_Status_t",
        #         "Val_Message_t",
        #         "Val_RunDate_t",
        #         "Review_Status_t",
        #         "Review_Message_t",
        #         "Review_RunDate_t",
        #         "Dataload_Status_t",
        #         "Dataload_Msg_t",
        #         "ACTIVID_USER",
        #         "TREATMENTID_",
        #         "ORG_ADMIN_a",
        #         "ACTIVITY_DESCRIPTION",
        #         "ACTIVITY_CAT",
        #         "BROAD_VEGETATION_TYPE",
        #         "BVT_USERD",
        #         "ACTIVITY_STATUS",
        #         "ACTIVITY_QUANTITY",
        #         "ACTIVITY_UOM",
        #         "ACTIVITY_START",
        #         "ACTIVITY_END",
        #         "ADMIN_ORG_NAME",
        #         "IMPLEM_ORG_NAME",
        #         "PRIMARY_FUND_SRC_NAME",
        #         "PRIMARY_FUND_ORG_NAME",
        #         "SECONDARY_FUND_SRC_NAME",
        #         "SECONDARY_FUND_ORG_NAME",
        #         "TERTIARY_FUND_SRC_NAME",
        #         "TERTIARY_FUND_ORG_NAME",
        #         "ACTIVITY_PRCT",
        #         "RESIDUE_FATE",
        #         "RESIDUE_FATE_QUANTITY",
        #         "RESIDUE_FATE_UNITS",
        #         "ACTIVITY_NAME",
        #         "VAL_STATUS_a",
        #         "VAL_MSG_a",
        #         "VAL_RUNDATE_a",
        #         "REVIEW_STATUS_a",
        #         "REVIEW_MSG_a",
        #         "REVIEW_RUNDATE_a",
        #         "DATALOAD_STATUS_a",
        #         "DATALOAD_MSG_a",
        #         "Source",
        #         "Year",
        #         "Year_txt",
        #         "Act_Code",
        #         "Crosswalk",
        #         "Federal_FY",
        #         "State_FY",
        #         "TRMT_GEOM",
        #         "COUNTS_TO_MAS"],
        #     xy_tolerance="",
        #     z_tolerance=0,
        # )

        # # Process: Keep Fields (Delete Field) (management)
        print("     step 31/34 removing unnecessary fields")
        Veg_Summarized_Pts_Laye_11_ = KeepFields(Pts_enrichment_Veg_Layer3)       
            
        # Process: Select (Select) (analysis)
        arcpy.analysis.Select(
            in_features=Veg_Summarized_Pts_Laye_11_,
            out_feature_class=enrich_pts_out,
            where_clause="" #"County IS NOT NULL",
        )

        # if delete_scratch:
        #     print("Deleting Scratch Files")
        #     delete_scratch_files(
        #         gdb=scratch_workspace, delete_fc="yes", delete_table="yes", delete_ds="yes"
        #     )
        print("Enrich Points Complete...")


