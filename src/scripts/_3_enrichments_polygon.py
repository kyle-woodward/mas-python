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
from scripts.utils import init_gdb, delete_scratch_files

workspace, scratch_workspace = init_gdb()

def enrich_polygons(
    enrich_in, enrich_out, delete_scratch=False
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
        # define file paths to required input datasets (mostly from b_Reference featuredataset in original GDB)
        Veg_Layer = os.path.join(workspace,'b_Reference','Broad_Vegetation_Types')
        WUI_Layer = os.path.join(workspace,'b_Reference','WUI')
        Ownership_Layer = os.path.join(workspace,'b_Reference','CALFIRE_Ownership_Update')
        Regions_Layer = os.path.join(workspace,'b_Reference','WFRTF_Regions')
        
        # define file paths to intermediary outputs in scratch gdb
        Veg_Summarized_Polygons = os.path.join(
            scratch_workspace, "Veg_Summarized_Polygons"
        )
        WHR13NAME_Summary = os.path.join(scratch_workspace, "WHR13NAME_Summary")
        WHR13NAME_Summary_SummarizeAttributes = os.path.join(
            scratch_workspace, "WHR13NAME_Summary_SummarizeAttributes"
        )
        Veg_Summarized_Centroids = os.path.join(
            scratch_workspace, "Veg_Summarized_Centroids"
        )
        Veg_Summarized_Join1_Own = os.path.join(
            scratch_workspace, "Veg_Summarized_Join1_Own"
        )
        Veg_Summarized_Join2_RCD = os.path.join(
            scratch_workspace, "Veg_Summarized_Join2_RCD"
        )
        WHR13NAME_Summary_temp = os.path.join(
            scratch_workspace, "WHR13NAME_Summary_temp"
        )
        
        # BEGIN TOOL CHAIN

        print("Executing Polygon Enrichments...")
        print("   Calculating Broad Vegetation Type...")
        # Process: Summarize Within (Summarize Within) (analysis)
        print("     step 1/34 summarize veg within polygons")
        arcpy.analysis.SummarizeWithin(
            in_polygons=enrich_in,
            in_sum_features=Veg_Layer,
            out_feature_class=Veg_Summarized_Polygons,
            keep_all_polygons="KEEP_ALL",
            sum_fields=None,  # changed from []
            sum_shape="ADD_SHAPE_SUM",
            shape_unit="ACRES",
            group_field="WHR13NAME",
            add_min_maj="NO_MIN_MAJ",
            add_group_percent="NO_PERCENT",
            out_group_table=WHR13NAME_Summary,
        )

        # Process: Summarize Attributes (Summarize Attributes) (gapro)
        print("     step 2/34 summarize attributes")
        arcpy.gapro.SummarizeAttributes(
            input_layer=WHR13NAME_Summary,
            out_table=WHR13NAME_Summary_SummarizeAttributes,
            fields=["Join_ID"],
            summary_fields=[["sum_Area_ACRES", "MAX"]],
            time_step_interval=None,
            time_step_repeat=None,
            time_step_reference=None,
        )

        # print('   Performing Field Modifications...')
        # Process: Add Join (2) (Add Join) (management)
        print("     step 3/34 add join")
        WHR13NAME_Summary_SummarizeA = arcpy.management.AddJoin(
            in_layer_or_view=WHR13NAME_Summary_SummarizeAttributes,
            in_field="MAX_Sum_Area_ACRES",
            join_table=WHR13NAME_Summary,
            join_field="sum_Area_ACRES",
            join_type="KEEP_ALL",
            index_join_fields="INDEX_JOIN_FIELDS",
        )

        # Process: Table To Table (Table To Table) (conversion)
        print("     step 4/34 convert table to table")
        WHR13NAME_Summary_temp = arcpy.conversion.TableToTable(
            in_rows=WHR13NAME_Summary_SummarizeA,
            out_path=scratch_workspace,
            out_name="WHR13NAME_Summary_temp",
            where_clause="",
            config_keyword="",
        )

        # Process: Delete Identical (Delete Identical) (management)
        print("     step 5/34 delete identical")
        WHR13NAME_Summary_temp_2_ = arcpy.management.DeleteIdentical(
            in_dataset=WHR13NAME_Summary_temp,
            fields=["Join_ID", "MAX_Sum_Area_ACRES", "WHR13NAME"],
            xy_tolerance="",
            z_tolerance=0,
        )

        # Count1 = arcpy.management.GetCount(WHR13NAME_Summary_temp_2_)
        # print("{} has {} records".format(WHR13NAME_Summary_temp_2_, Count1[0]))

        # Process: Add Join (3) (Add Join) (management)
        print("     step 6/34 add join")
        usfs_haz_fuels_treatments_re = arcpy.management.AddJoin(
            in_layer_or_view=Veg_Summarized_Polygons,
            in_field="Join_ID",
            join_table=WHR13NAME_Summary_temp_2_,
            join_field="Join_ID",
            join_type="KEEP_ALL",
            index_join_fields="INDEX_JOIN_FIELDS",
        )

        # Process: Select Layer By BVT Not Null (Select Layer By Attribute) (management)
        print("     step 7/34 select layer by attribute")
        (
            Veg_Summarized_Polygons_Laye_3_,
            Count,
        ) = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=usfs_haz_fuels_treatments_re,
            selection_type="NEW_SELECTION",
            where_clause="BROAD_VEGETATION_TYPE IS NOT NULL",
            invert_where_clause="",
        )

        # Process: Calculate BVT User Defined Yes (Calculate Field) (management)
        print("     step 8/34 calculate user defined veg field yes")
        Updated_Input_Table_2_ = arcpy.management.CalculateField(
            in_table=Veg_Summarized_Polygons_Laye_3_,
            field="BVT_USERD",
            expression='"YES"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Switch Selection (Select Layer By Attribute) (management)
        print("     step 9/34 select layer by attribute")
        Updated_Layer_Or_Table_View, Count_5_ = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=Updated_Input_Table_2_,
            selection_type="SWITCH_SELECTION",
            where_clause="",
            invert_where_clause="",
        )

        # Process: Calculate Veg (Calculate Field) (management)
        print("     step 10/34 calculate veg domain code")
        Veg_Summarized_Polygons_Laye_2_ = arcpy.management.CalculateField(
            in_table=Updated_Layer_Or_Table_View,
            field="Veg_Summarized_Polygons.BROAD_VEGETATION_TYPE",
            expression="ifelse(!WHR13NAME_Summary_temp.WHR13NAME!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(VEG):
                                            if VEG == \"Agriculture\":
                                                return \"AGRICULTURE\"
                                            elif VEG == \"Barren/Other\":
                                                return \"SPARSE\"
                                            elif VEG == \"Conifer Forest\":
                                                return \"FOREST\"
                                            elif VEG == \"Conifer Woodland\":
                                                return \"FOREST\"
                                            elif VEG == \"Desert Shrub\":
                                                return \"SHRB_CHAP\"
                                            elif VEG == \"Desert Woodland\":
                                                return \"FOREST\"
                                            elif VEG == \"Hardwood Forest\":
                                                return \"FOREST\"
                                            elif VEG == \"Hardwood Woodland\":
                                                return \"FOREST\"
                                            elif VEG == \"Herbaceous\":
                                                return \"GRASS_HERB\"
                                            elif VEG == \"Shrub\":
                                                return \"SHRB_CHAP\"
                                            elif VEG == \"Urban\":
                                                return \"URBAN\"
                                            elif VEG == \"Water\":
                                                return \"WATER\"
                                            elif VEG == \"Wetland\":
                                                return \"WETLAND\"
                                            else:
                                                return VEG""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate BVT User Defined No (Calculate Field) (management)
        print("     step 11/34 calculate user defined veg field no")
        Updated_Input_Table_4_ = arcpy.management.CalculateField(
            in_table=Veg_Summarized_Polygons_Laye_2_,
            field="BVT_USERD",
            expression='"NO"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Switch Selection (Select Layer By Attribute) (management)
        Updated_Input_Table_4a_ = arcpy.management.SelectLayerByAttribute(
                                            in_layer_or_view=Updated_Input_Table_4_, 
                                            selection_type="CLEAR_SELECTION", 
                                            where_clause="", 
                                            invert_where_clause=""
                                            )

        # Process: Remove Join (Remove Join) (management)
        print("     step 12/34 remove join")
        Layer_With_Join_Removed = arcpy.management.RemoveJoin(
            in_layer_or_view=Updated_Input_Table_4a_, join_name="WHR13NAME_Summary_temp"
        )
        # Count2 = arcpy.management.GetCount(Layer_With_Join_Removed)
        # print("{} has {} records".format(Layer_With_Join_Removed, Count2[0]))

        print("   Calculating WUI...")
        # Process: Select Layer WUI Null (Select Layer By Attribute) (management)
        print("     step 13/34 select layer by attribute")
        Veg_Summarized_Polygons_Laye_7_, Count_8_, = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=Layer_With_Join_Removed,
            selection_type="NEW_SELECTION",
            where_clause="IN_WUI IS NULL Or IN_WUI = ''",
            invert_where_clause="",
        )

        # Process: Select Layer By WUI (Select Layer By Location) (management)
        print("     step 14/34 select layer by WUI location")
        Veg_Summarized_Polygons_Laye1_2_, Output_Layer_Names_2_, Count_2_, = arcpy.management.SelectLayerByLocation(
            in_layer=[Veg_Summarized_Polygons_Laye_7_],
            overlap_type="INTERSECT",
            select_features=WUI_Layer,
            search_distance="",
            selection_type="SUBSET_SELECTION",
            invert_spatial_relationship="NOT_INVERT",
        )

        # Process: Calculate WUI Auto Yes (Calculate Field) (management)
        print("     step 15/34 calculate WUI yes")
        usfs_haz_fuels_treatments_re3 = arcpy.management.CalculateField(
            in_table=Veg_Summarized_Polygons_Laye1_2_,
            field="IN_WUI",
            expression='"WUI_AUTO_POP"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Select Layer WUI Auto No (Select Layer By Attribute) (management)
        print("     step 16/34 select layer by attribute")
        Veg_Summarized_Polygons_Laye_5_, Count_6_, = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=usfs_haz_fuels_treatments_re3,
            selection_type="NEW_SELECTION",
            where_clause="IN_WUI IS NULL Or IN_WUI = ''",
            invert_where_clause="",
        )

        # Process: Calculate WUI No (Calculate Field) (management)
        print("     step 17/34 calculate WUI no")
        usfs_haz_fuels_treatments_re3_2_ = arcpy.management.CalculateField(
            in_table=Veg_Summarized_Polygons_Laye_5_,
            field="IN_WUI",
            expression='"NON-WUI_AUTO_POP"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Clear Selection (Select Layer By Attribute) (management)
        print("     step 18/34 clear selection")
        Treatments_Merge3_California_5_, Count_4_ = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=usfs_haz_fuels_treatments_re3_2_, 
            selection_type="CLEAR_SELECTION", 
            where_clause="", 
            invert_where_clause=""
        )
        # Count3 = arcpy.management.GetCount(Treatments_Merge3_California_5_)
        # print('{} has {} records'.format(Treatments_Merge3_California_5_, Count3[0]))
        
        # Process: Feature To Point (Feature To Point) (management)
        print("     step 19/34 feature to point")
        arcpy.management.FeatureToPoint(
            in_features=Treatments_Merge3_California_5_,
            out_feature_class=Veg_Summarized_Centroids,
            point_location="INSIDE",
        )

        print("   Calculating Ownership, Counties, and Regions...")
        # Process: Spatial Join (Spatial Join) (analysis)
        print("     step 20/34 spatial join ownership")
        arcpy.analysis.SpatialJoin(
            target_features=Veg_Summarized_Centroids,
            join_features=Ownership_Layer,
            out_feature_class=Veg_Summarized_Join1_Own,
            join_operation="JOIN_ONE_TO_ONE",
            join_type="KEEP_ALL",
            match_option="INTERSECT",
            search_radius="",
            distance_field_name="",
        )

        # Process: Spatial Join (2) (Spatial Join) (analysis)
        print("     step 21/34 spatial join veg")
        arcpy.analysis.SpatialJoin(
            target_features=Veg_Summarized_Join1_Own,
            join_features=Regions_Layer,
            out_feature_class=Veg_Summarized_Join2_RCD,
            join_operation="JOIN_ONE_TO_ONE",
            join_type="KEEP_ALL",
            match_option="INTERSECT",
            search_radius="",
            distance_field_name="",
        )

        # Process: Add Join (19) (Add Join) (management)
        print("     step 22/34 add join")
        Veg_Summarized_Polygons_Laye2_2_ = arcpy.management.AddJoin(
            in_layer_or_view=Treatments_Merge3_California_5_,
            in_field="OBJECTID",
            join_table=Veg_Summarized_Join2_RCD,
            join_field="ORIG_FID",
            join_type="KEEP_ALL",
            index_join_fields="INDEX_JOIN_FIELDS",
        )

        # Process: Calculate Owner (Calculate Field) (management)
        print("     step 23/34 calculate ownership field")
        Veg_Summarized_Polygons_Laye = arcpy.management.CalculateField(
            in_table=Veg_Summarized_Polygons_Laye2_2_,
            field="Veg_Summarized_Polygons.PRIMARY_OWNERSHIP_GROUP",
            expression="ifelse(!Veg_Summarized_Join2_RCD.AGNCY_LEV!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(Own):
                                        if Own == \"Federal\":
                                            return \"FEDERAL\"
                                        if Own == \"Local\":
                                            return \"LOCAL\"
                                        if Own == \"NGO\":
                                            return \"NGO\"
                                        if Own == \"Private - Industrial\":
                                            return \"PRIVATE_INDUSTRY\"
                                        if Own == \"Private - Non Industrial\":
                                            return \"PRIVATE_NON-INDUSTRY\"
                                        if Own == \"Private - Non-Industrial\":
                                            return \"PRIVATE_NON-INDUSTRY\"
                                        if Own == \"State\":
                                            return \"STATE\"
                                        if Own == \"Tribal\":
                                            return \"TRIBAL\"
                                        else:
                                            return Own""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate County (Calculate Field) (management)
        print("     step 24/34 calculate county field")
        Veg_Summarized_Polygons_Laye2_4_ = arcpy.management.CalculateField(
            in_table=Veg_Summarized_Polygons_Laye,
            field="Veg_Summarized_Polygons.COUNTY",
            expression="ifelse(!Veg_Summarized_Join2_RCD.COUNTY_1!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(CO):
                                            if CO == \"Alameda\":
                                                return \"ALA\"
                                            if CO == \"Alpine\":
                                                return \"ALP\"
                                            if CO == \"Amador\":
                                                return \"AMA\"
                                            if CO == \"Butte\":
                                                return \"BUT\"
                                            if CO == \"Calaveras\":
                                                return \"CAL\"
                                            if CO == \"Colusa\":
                                                return \"COL\"
                                            if CO == \"Contra Costa\":
                                                return \"CC\"
                                            if CO == \"Del Norte\":
                                                return \"DN\"
                                            if CO == \"El Dorado\":
                                                return \"ED\"
                                            if CO == \"Fresno\":
                                                return \"FRE\"
                                            if CO == \"Glenn\":
                                                return \"GLE\"
                                            if CO == \"Humboldt\":
                                                return \"HUM\"
                                            if CO == \"Imperial\":
                                                return \"IMP\"
                                            if CO == \"Inyo\":
                                                return \"INY\"
                                            if CO == \"Kern\":
                                                return \"KER\"
                                            if CO == \"Kings\":
                                                return \"KIN\"
                                            if CO == \"Lake\":
                                                return \"LAK\"
                                            if CO == \"Lassen\":
                                                return \"LAS\"
                                            if CO == \"Los Angeles\":
                                                return \"LA\"
                                            if CO == \"Madera\":
                                                return \"MAD\"
                                            if CO == \"Marin\":
                                                return \"MRN\"
                                            if CO == \"Mariposa\":
                                                return \"MPA\"
                                            if CO == \"Mendocino\":
                                                return \"MEN\"
                                            if CO == \"Merced\":
                                                return \"MER\"
                                            if CO == \"Modoc\":
                                                return \"MOD\"
                                            if CO == \"Monterey\":
                                                return \"MON\"
                                            if CO == \"Mono\":
                                                return \"MNO\"
                                            if CO == \"Napa\":
                                                return \"NAP\"
                                            if CO == \"Nevada\":
                                                return \"NEV\"
                                            if CO == \"Orange\":
                                                return \"ORA\"
                                            if CO == \"Placer\":
                                                return \"PLA\"
                                            if CO == \"Plumas\":
                                                return \"PLU\"
                                            if CO == \"Riverside\":
                                                return \"RIV\"
                                            if CO == \"Sacramento\":
                                                return \"SAC\"
                                            if CO == \"San Benito\":
                                                return \"SBT\"
                                            if CO == \"San Bernardino\":
                                                return \"SBD\"
                                            if CO == \"San Diego\":
                                                return \"SD\"
                                            if CO == \"San Francisco\":
                                                return \"SF\"
                                            if CO == \"San Joaquin\":
                                                return \"SJ\"
                                            if CO == \"San Luis Obispo\":
                                                return \"SLO\"
                                            if CO == \"San Mateo\":
                                                return \"SM\"
                                            if CO == \"Santa Barbara\":
                                                return \"SB\"
                                            if CO == \"Santa Clara\":
                                                return \"SCL\"
                                            if CO == \"Santa Cruz\":
                                                return \"SCR\"
                                            if CO == \"Shasta\":
                                                return \"SHA\"
                                            if CO == \"Sierra\":
                                                return \"SIE\"
                                            if CO == \"Siskiyou\":
                                                return \"SIS\"
                                            if CO == \"Solano\":
                                                return \"SOL\"
                                            if CO == \"Sonoma\":
                                                return \"SON\"
                                            if CO == \"Stanislaus\":
                                                return \"STA\"
                                            if CO == \"Sutter\":
                                                return \"SUT\"
                                            if CO == \"Tehama\":
                                                return \"TEH\"
                                            if CO == \"Tuolumne\":
                                                return \"TUO\"
                                            if CO == \"Trinity\":
                                                return \"TRI\"
                                            if CO == \"Tulare\":
                                                return \"TUL\"
                                            if CO == \"Ventura\":
                                                return \"VEN\"
                                            if CO == \"Yolo\":
                                                return \"YOL\"
                                            if CO == \"Yuba\":
                                                return \"YUB\"
                                            else:
                                                return CO""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Region (Calculate Field) (management)
        print("     step 25/34 calculate region field")
        Veg_Summarized_Polygons_Laye_6_ = arcpy.management.CalculateField(
            in_table=Veg_Summarized_Polygons_Laye2_4_,
            field="Veg_Summarized_Polygons.REGION",
            expression="ifelse(!Veg_Summarized_Join2_RCD.Region!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(Reg):
                                        if Reg == \"Central Coast\":
                                            return \"CENTRAL_COAST\"
                                        if Reg == \"North Coast\":
                                            return \"NORTH_COAST\"
                                        if Reg == \"Sierra Nevada\":
                                            return \"SIERRA_NEVADA\"
                                        if Reg == \"Southern California\":
                                            return \"SOUTHERN_CA\"
                                        else:
                                            return Reg""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Remove Join (10) (Remove Join) (management)
        print("     step 26/34 remove join")
        Veg_Summarized_Polygons_Laye2 = arcpy.management.RemoveJoin(
            in_layer_or_view=Veg_Summarized_Polygons_Laye_6_,
            join_name="Veg_Summarized_Join2_RCD",
        )

        # Count4 = arcpy.management.GetCount(Veg_Summarized_Polygons_Laye2)
        # print("{} has {} records".format(Veg_Summarized_Polygons_Laye2, Count4[0]))

        print("     step 27/34 Calculating Years...")
        # Process: 2h Calculate Year (2h Calculate Year) (PC414CWIMillionAcres)
        Veg_Summarized_Polygons_Laye3_7_ = Year(Year_Input=Veg_Summarized_Polygons_Laye2)
        
        print("   step 28/34 Initiating Crosswalk...")
        # Process: Crosswalk
        crosswalk_table = Crosswalk(Input_Table=Veg_Summarized_Polygons_Laye3_7_)
        print("   Crosswalk Complete, Continuing Enrichment...")

        # Count5 = arcpy.management.GetCount(crosswalk_table)
        # print('{} has {} records'.format(crosswalk_table, Count5[0]))

        print("     step 29/34 Calculating Latitude and Longitude...")
        # Process: Calculate Geometry Attributes (3) (Calculate Geometry Attributes) (management)
        Veg_Summarized_Polygons_Laye_4_ = arcpy.management.CalculateGeometryAttributes(
            in_features=Veg_Summarized_Polygons_Laye3_7_,
            geometry_property=[
                ["LATITUDE", "INSIDE_Y"], 
                ["LONGITUDE", "INSIDE_X"]],
            length_unit="",
            area_unit="",
            coordinate_system='GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]',
            coordinate_format="DD",
        )

        # Process: Calculate Geometry Attributes (4) (Calculate Geometry Attributes) (management)
        print("     step 30/34 calculate treatment acres")
        Veg_Summarized_Polygons_Laye_8_ = arcpy.management.CalculateGeometryAttributes(
            in_features=Veg_Summarized_Polygons_Laye_4_,
            geometry_property=[["TREATMENT_AREA", "AREA"]],
            length_unit="",
            area_unit="ACRES_US",
            coordinate_system='PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]',
            coordinate_format="SAME_AS_INPUT",
        )

        # # Process: Keep Fields (Delete Field) (management)
        print("     step 31/34 removing unnecessary fields")
        Veg_Summarized_Polygons_Laye_11_ = KeepFields(Veg_Summarized_Polygons_Laye_8_)       
        
        # Count6 = arcpy.management.GetCount(Veg_Summarized_Polygons_Laye_11_)
        # print('{} has {} records'.format(Veg_Summarized_Polygons_Laye_11_, Count6[0]))

        # Process: Select (Select) (analysis)
        print("     step 33/34 delete if County is Null")
        Veg_Summarized_Polygons_Laye_13_ = arcpy.analysis.Select(
            in_features=Veg_Summarized_Polygons_Laye_11_,
            out_feature_class=enrich_out,
            where_clause="County IS NOT NULL",
        )

        # Count7 = arcpy.management.GetCount(Veg_Summarized_Polygons_Laye_13_)
        # print("{} has {} records".format(Veg_Summarized_Polygons_Laye_13_, Count7[0]))

        print("     step 34/34 delete scratch files")

        if delete_scratch:
            print('Deleting Scratch Files')
            delete_scratch_files(
                gdb=scratch_workspace,
                delete_fc="yes",
                delete_table="yes",
                delete_ds="yes",
            )

        print("Enrich Polygons Complete...")
