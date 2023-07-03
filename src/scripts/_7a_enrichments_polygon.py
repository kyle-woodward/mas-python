import arcpy
from ._2d_calculate_activity import Activity
from ._2f_calculate_category import Category
from ._2e_calculate_objective import Objective
from ._2g_calculate_residue_fate import Residue
from ._2h_calculate_year import Year
from ._2k_keep_fields import KeepFields
from sys import argv
from scripts.utils import init_gdb, delete_scratch_files, runner
import os
original_gdb, workspace, scratch_workspace = init_gdb()

# first arg is the output fc path and the other is the input fc you are enriching
def enrich_polygons(enrich_out, enrich_in, delete_scratch=False):  # 7a Enrichments Polygon
    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Analysis Tools.tbx")
    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\GeoAnalytics Desktop Tools.tbx")
    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")
    
    # wrapping entire process within an arcpy.EnvManager() instance fixes the SummarizeWithin tool failed error 
    with arcpy.EnvManager(
    overwriteOutput=True,
    extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""", 
    outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""", 
    preserveGlobalIds=True, 
    qualifiedFieldNames=False, 
    scratchWorkspace=scratch_workspace, 
    transferDomains=True, 
    transferGDBAttributeProperties=True, 
    workspace=workspace
    ):
    
        # define file paths to required input datasets (mostly from b_Reference featuredataset in original GDB)
        RasterT_fveg1 = os.path.join(workspace,'b_Reference','RasterT_fveg1')
        RasterT_Reclass_WUI = os.path.join(workspace,'b_Reference','RasterT_Reclass_WUI')
        CPAD_Ownership_Update = os.path.join(workspace,'b_Reference','CPAD_Ownership_Update')
        WFRTF_Regions_Draft = os.path.join(workspace,'b_Reference','WFRTF_Regions_Draft')
        Fuels_Treatments_Piles_Crosswalk = os.path.join(workspace,'Fuels_Treatments_Piles_Crosswalk')
        
        # define file paths to intermediary outputs in scratch gdb
        Veg_Summarized_Polygons = os.path.join(scratch_workspace,'Veg_Summarized_Polygons')
        WHR13NAME_Summary = os.path.join(scratch_workspace,'WHR13NAME_Summary')
        WHR13NAME_Summary_SummarizeAttributes = os.path.join(scratch_workspace,'WHR13NAME_Summary_SummarizeAttributes') 
        Veg_Summarized_Centroids = os.path.join(scratch_workspace,'Veg_Summarized_Centroids')
        Veg_Summarized_Join1_Own = os.path.join(scratch_workspace,'Veg_Summarized_Join1_Own')
        Veg_Summarized_Join2_RCD = os.path.join(scratch_workspace,'Veg_Summarized_Join2_RCD')
        WHR13NAME_Summary_temp = os.path.join(scratch_workspace,"WHR13NAME_Summary_temp")
        # Begin tool chain processes

        print('Executing Polygon Enrichments...')
        print("   Calculating Broad Vegetation Type...")
        # Process: Summarize Within (Summarize Within) (analysis)
        print("     step 1/47 summarize within")
        arcpy.analysis.SummarizeWithin(
                                    in_polygons=enrich_in, 
                                    in_sum_features=RasterT_fveg1, 
                                    out_feature_class=Veg_Summarized_Polygons, 
                                    keep_all_polygons="KEEP_ALL", 
                                    sum_fields=None,  # changed from []
                                    sum_shape="ADD_SHAPE_SUM", 
                                    shape_unit="ACRES", 
                                    group_field="WHR13NAME", 
                                    add_min_maj="NO_MIN_MAJ", 
                                    add_group_percent="NO_PERCENT", 
                                    out_group_table=WHR13NAME_Summary
                                    )

        # Process: Summarize Attributes (Summarize Attributes) (gapro)
        print("     step 2/47 summarize attributes")
        arcpy.gapro.SummarizeAttributes(
                                        input_layer=WHR13NAME_Summary, 
                                        out_table=WHR13NAME_Summary_SummarizeAttributes, 
                                        fields=["Join_ID"], 
                                        summary_fields=[["Sum_Area_ACRES", "MAX"]], 
                                        time_step_interval="", 
                                        time_step_repeat="", 
                                        time_step_reference=""
                                        )

        # print('   Performing Field Modifications...')
        # Process: Add Join (2) (Add Join) (management)
        print("     step 3/47 add join")
        WHR13NAME_Summary_SummarizeA = arcpy.management.AddJoin(
                                    in_layer_or_view=WHR13NAME_Summary_SummarizeAttributes, 
                                    in_field="MAX_Sum_Area_ACRES", 
                                    join_table=WHR13NAME_Summary, 
                                    join_field="sum_Area_ACRES", 
                                    join_type="KEEP_ALL", 
                                    index_join_fields="INDEX_JOIN_FIELDS"
                                    )

        # Process: Table To Table (Table To Table) (conversion)
        print("     step 4/47 convert table to table")
        WHR13NAME_Summary_temp = arcpy.conversion.TableToTable(
                            in_rows=WHR13NAME_Summary_SummarizeA, 
                            out_path=scratch_workspace, 
                            out_name="WHR13NAME_Summary_temp", 
                            where_clause="",
                            # ideally want to chunk out field mapping string to reduce line length .. 
                            field_mapping="Join_ID \"Join_ID\" true true false 4 Long 0 0,First,#,WHR13NAME_Summary_SummarizeA:WHR13NAME_Summary_SummarizeA,WHR13NAME_Summary_SummarizeAttributes.Join_ID,-1,-1;COUNT \"COUNT\" true true false 8 Double 0 0,First,#,WHR13NAME_Summary_SummarizeA:WHR13NAME_Summary_SummarizeA,WHR13NAME_Summary_SummarizeAttributes.COUNT,-1,-1;MAX_Sum_Area_ACRES \"MAX_Sum_Area_ACRES\" true true false 8 Double 0 0,First,#,WHR13NAME_Summary_SummarizeA:WHR13NAME_Summary_SummarizeA,WHR13NAME_Summary_SummarizeAttributes.MAX_Sum_Area_ACRES,-1,-1;OBJECTID \"OBJECTID\" false true false 4 Long 0 9,First,#,WHR13NAME_Summary_SummarizeA:WHR13NAME_Summary_SummarizeA,WHR13NAME_Summary.OBJECTID,-1,-1;Join_ID \"Join ID\" true true false 4 Long 0 0,First,#,WHR13NAME_Summary_SummarizeA:WHR13NAME_Summary_SummarizeA,WHR13NAME_Summary.Join_ID,-1,-1;WHR13NAME \"WHR13NAME\" true true false 255 Text 0 0,First,#,WHR13NAME_Summary_SummarizeA:WHR13NAME_Summary_SummarizeA,WHR13NAME_Summary.WHR13NAME,0,255;sum_Area_ACRES \"Summarized Area in ACRES\" true true false 8 Double 0 0,First,#,WHR13NAME_Summary_SummarizeA:WHR13NAME_Summary_SummarizeA,WHR13NAME_Summary.sum_Area_ACRES,-1,-1;Polygon_Count \"Count of Polygons\" true true false 4 Long 0 0,First,#,WHR13NAME_Summary_SummarizeA:WHR13NAME_Summary_SummarizeA,WHR13NAME_Summary.Polygon_Count,-1,-1", 
                            config_keyword=""
                            )

        # Process: Delete Identical (Delete Identical) (management)
        print("     step 5/47 delete identical")
        WHR13NAME_Summary_temp_2_ = arcpy.management.DeleteIdentical(
                                in_dataset=WHR13NAME_Summary_temp, 
                                fields=["Join_ID", "MAX_Sum_Area_ACRES", "WHR13NAME"], 
                                xy_tolerance="", 
                                z_tolerance=0
                                )

        # Process: Add Join (3) (Add Join) (management)
        print("     step 6/47 add join")
        usfs_haz_fuels_treatments_re = arcpy.management.AddJoin(
                                    in_layer_or_view=Veg_Summarized_Polygons, 
                                    in_field="Join_ID", 
                                    join_table=WHR13NAME_Summary_temp_2_, 
                                    join_field="Join_ID", 
                                    join_type="KEEP_ALL", 
                                    index_join_fields="INDEX_JOIN_FIELDS"
                                    )

        # Process: Select Layer By BVT Not Null (Select Layer By Attribute) (management)
#<<<<<<< HEAD
#        Veg_Summarized_Polygons_Laye_3_ = arcpy.management.SelectLayerByAttribute(
#=======
        print("     step 7/47 select layer by attribute")
        Veg_Summarized_Polygons_Laye_3_, Count = arcpy.management.SelectLayerByAttribute(
#>>>>>>> 1f899f8affb0c4abb79e4204a32d440344232227
                                            in_layer_or_view=usfs_haz_fuels_treatments_re, 
                                            selection_type="NEW_SELECTION", 
                                            where_clause="BROAD_VEGETATION_TYPE IS NOT NULL", 
                                            invert_where_clause=""
                                            )

        # Process: Calculate BVT User Defined Yes (Calculate Field) (management)
        print("     step 8/47 calculate field")
        Updated_Input_Table_2_ = arcpy.management.CalculateField(
                            in_table=Veg_Summarized_Polygons_Laye_3_, 
                            field="BVT_USERD", 
                            expression="\"YES\"", 
                            expression_type="PYTHON3", 
                            code_block="", 
                            field_type="TEXT", 
                            enforce_domains="NO_ENFORCE_DOMAINS"
                            )

        # Process: Switch Selection (Select Layer By Attribute) (management)
# <<<<<<< HEAD
        # Updated_Layer_Or_Table_View = arcpy.management.SelectLayerByAttribute(
# =======
        print("     step 9/47 select layer by attribute")
        Updated_Layer_Or_Table_View, Count_5_ = arcpy.management.SelectLayerByAttribute(
# >>>>>>> 1f899f8affb0c4abb79e4204a32d440344232227
                                            in_layer_or_view=Updated_Input_Table_2_, 
                                            selection_type="SWITCH_SELECTION", 
                                            where_clause="", 
                                            invert_where_clause=""
                                            )

        # Process: Calculate Veg (Calculate Field) (management)
        print("     step 10/47 calculate field")
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
                                                return VEG""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS"
                                        )

        # Process: Calculate BVT User Defined No (Calculate Field) (management)
        print("     step 11/47 calculate field")
        Updated_Input_Table_4_ = arcpy.management.CalculateField(
                            in_table=Veg_Summarized_Polygons_Laye_2_, 
                            field="BVT_USERD", 
                            expression="\"NO\"", 
                            expression_type="PYTHON3", 
                            code_block="", 
                            field_type="TEXT", 
                            enforce_domains="NO_ENFORCE_DOMAINS"
                            )

        # Process: Remove Join (Remove Join) (management)
        print("     step 12/47 remove join")
        Layer_With_Join_Removed = arcpy.management.RemoveJoin(
                                in_layer_or_view=Updated_Input_Table_4_, 
                                join_name="WHR13NAME_Summary_temp"
                                )

        print("   Calculating WUI...")
        # Process: Select Layer WUI Null (Select Layer By Attribute) (management)
# <<<<<<< HEAD
        # Veg_Summarized_Polygons_Laye_7_ = arcpy.management.SelectLayerByAttribute(
# =======
        print("     step 13/47 select layer by attribute")
        Veg_Summarized_Polygons_Laye_7_, Count_8_ = arcpy.management.SelectLayerByAttribute(
# >>>>>>> 1f899f8affb0c4abb79e4204a32d440344232227
                                                in_layer_or_view=Layer_With_Join_Removed, 
                                                selection_type="NEW_SELECTION", 
                                                where_clause="IN_WUI IS NULL Or IN_WUI = ''", 
                                                invert_where_clause="")

        # Process: Select Layer By WUI (Select Layer By Location) (management)
# <<<<<<< HEAD
        # Veg_Summarized_Polygons_Laye1_2_ = arcpy.management.SelectLayerByLocation(
# =======
        print("     step 14/47 select layer by location")
        Veg_Summarized_Polygons_Laye1_2_, Output_Layer_Names_2_, Count_2_ = arcpy.management.SelectLayerByLocation(
# >>>>>>> 1f899f8affb0c4abb79e4204a32d440344232227
                                                                        in_layer=[Veg_Summarized_Polygons_Laye_7_], 
                                                                        overlap_type="INTERSECT", 
                                                                        select_features=RasterT_Reclass_WUI, 
                                                                        search_distance="", 
                                                                        selection_type="SUBSET_SELECTION", 
                                                                        invert_spatial_relationship="NOT_INVERT")

        # Process: Calculate WUI Auto Yes (Calculate Field) (management)
        print("     step 15/47 calculate field")
        usfs_haz_fuels_treatments_re3 = arcpy.management.CalculateField(
                                    in_table=Veg_Summarized_Polygons_Laye1_2_, 
                                    field="IN_WUI", 
                                    expression="\"WUI_AUTO_POP\"", 
                                    expression_type="PYTHON3", 
                                    code_block="", 
                                    field_type="TEXT", 
                                    enforce_domains="NO_ENFORCE_DOMAINS"
                                    )

        # Process: Select Layer WUI Auto No (Select Layer By Attribute) (management)
# <<<<<<< HEAD
        # Veg_Summarized_Polygons_Laye_5_ = arcpy.management.SelectLayerByAttribute(
# =======
        print("     step 16/47 select layer by attribute")
        Veg_Summarized_Polygons_Laye_5_, Count_6_ = arcpy.management.SelectLayerByAttribute(
# >>>>>>> 1f899f8affb0c4abb79e4204a32d440344232227
                                                in_layer_or_view=usfs_haz_fuels_treatments_re3, 
                                                selection_type="NEW_SELECTION", 
                                                where_clause="IN_WUI IS NULL Or IN_WUI = ''", 
                                                invert_where_clause=""
                                                )

        # Process: Calculate WUI No (Calculate Field) (management)
        print("     step 17/47 calculate field")
        usfs_haz_fuels_treatments_re3_2_ = arcpy.management.CalculateField(
                                        in_table=Veg_Summarized_Polygons_Laye_5_, 
                                        field="IN_WUI", 
                                        expression="\"NON-WUI_AUTO_POP\"",
                                        expression_type="PYTHON3", 
                                        code_block="", 
                                        field_type="TEXT", 
                                        enforce_domains="NO_ENFORCE_DOMAINS"
                                        )

        # Process: Clear Selection (Select Layer By Attribute) (management)
# <<<<<<< HEAD
        # Treatments_Merge3_California_5_ = arcpy.management.SelectLayerByAttribute(
# =======
        print("     step 18/47 sleect layer by attribute")
        Treatments_Merge3_California_5_, Count_4_ = arcpy.management.SelectLayerByAttribute(
# >>>>>>> 1f899f8affb0c4abb79e4204a32d440344232227
                                                in_layer_or_view=usfs_haz_fuels_treatments_re3_2_, 
                                                selection_type="CLEAR_SELECTION", 
                                                where_clause="", 
                                                invert_where_clause=""
                                                )

        
        # Process: Feature To Point (Feature To Point) (management)
        print("     step 19/47 feature to point")
        arcpy.management.FeatureToPoint(
                                        in_features=Treatments_Merge3_California_5_, 
                                        out_feature_class=Veg_Summarized_Centroids, 
                                        point_location="INSIDE"
                                        )

        print("   Calculating Ownership and Counties...")
        # Process: Spatial Join (Spatial Join) (analysis)
        print("     step 20/47 spatial join")
        arcpy.analysis.SpatialJoin(
                                target_features=Veg_Summarized_Centroids, 
                                join_features=CPAD_Ownership_Update, 
                                out_feature_class=Veg_Summarized_Join1_Own, 
                                join_operation="JOIN_ONE_TO_ONE", 
                                join_type="KEEP_ALL", 
                                field_mapping="YEAR \"YEAR\" true true false 4 Long 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Centroids,YEAR,-1,-1;ACRES \"ACRES\" true true false 8 Double 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Centroids,ACRES,-1,-1;ProjectID \"Project ID\" true true false 50 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Centroids,ProjectID,0,50;ProjectNM \"Project Name\" true true false 100 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Centroids,ProjectNM,0,100;Date \"Date\" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Centroids,Date,-1,-1;Status \"Status\" true true false 25 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Centroids,Status,0,25;TreatmentID \"Treatment ID\" true true false 100 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Centroids,TreatmentID,0,100;Agency_LEV \"Agency Level\" true true false 50 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Centroids,Agency_LEV,0,50;Agncy_Name \"Agency Name\" true true false 100 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Centroids,Agncy_Name,0,100;Source \"Source\" true true false 255 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Centroids,Source,0,255;Veg_Type \"Veg Type\" true true false 50 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Centroids,Veg_Type,0,50;WUI \"WUI\" true true false 3 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Centroids,WUI,0,3;CPUC \"CPUC Tier\" true true false 6 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Centroids,CPUC,0,6;RCD \"RCD\" true true false 150 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Centroids,RCD,0,150;FPD \"Fire Pro District\" true true false 155 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Centroids,FPD,0,155;Unit_Name \"Unit Name\" true true false 255 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Centroids,Unit_Name,0,255;ORIG_FID \"ORIG_FID\" true true false 4 Long 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Centroids,ORIG_FID,-1,-1;UNIT_NAME_1 \"UNIT_NAME\" true true false 80 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\b_Reference\\CPAD_Ownership_Update,UNIT_NAME,0,80;AGNCY_NAME_1 \"AGNCY_NAME\" true true false 100 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\b_Reference\\CPAD_Ownership_Update,AGNCY_NAME,0,100;AGNCY_LEV \"AGNCY_LEV\" true true false 50 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\b_Reference\\CPAD_Ownership_Update,AGNCY_LEV,0,50;MNG_AGNCY \"MNG_AGNCY\" true true false 100 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\b_Reference\\CPAD_Ownership_Update,MNG_AGNCY,0,100;MNG_AG_LEV \"MNG_AG_LEV\" true true false 50 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\b_Reference\\CPAD_Ownership_Update,MNG_AG_LEV,0,50;MNG_AG_TYP \"MNG_AG_TYP\" true true false 50 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\b_Reference\\CPAD_Ownership_Update,MNG_AG_TYP,0,50;SITE_NAME \"SITE_NAME\" true true false 100 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\b_Reference\\CPAD_Ownership_Update,SITE_NAME,0,100;LABEL_NAME \"LABEL_NAME\" true true false 255 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\b_Reference\\CPAD_Ownership_Update,LABEL_NAME,0,255;AGNCY_TYP \"AGNCY_TYP\" true true false 50 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\b_Reference\\CPAD_Ownership_Update,AGNCY_TYP,0,50;COUNTY \"COUNTY\" true true false 35 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\b_Reference\\CPAD_Ownership_Update,COUNTY,0,35;Shape_Length \"Shape_Length\" false true true 8 Double 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\b_Reference\\CPAD_Ownership_Update,Shape_Length,-1,-1;Shape_Area \"Shape_Area\" false true true 8 Double 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\b_Reference\\CPAD_Ownership_Update,Shape_Area,-1,-1", 
                                match_option="INTERSECT", 
                                search_radius="", 
                                distance_field_name=""
                                )

        print("   Calculating Task Force Regions...")
        # Process: Spatial Join (2) (Spatial Join) (analysis)
        print("     step 21/47 spatial join")
        arcpy.analysis.SpatialJoin(
                                target_features=Veg_Summarized_Join1_Own, 
                                join_features=WFRTF_Regions_Draft, 
                                out_feature_class=Veg_Summarized_Join2_RCD, 
                                join_operation="JOIN_ONE_TO_ONE", 
                                join_type="KEEP_ALL", 
                                field_mapping="Join_Count \"Join_Count\" true true false 0 Long 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,Join_Count,-1,-1;TARGET_FID \"TARGET_FID\" true true false 0 Long 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,TARGET_FID,-1,-1;YEAR \"YEAR\" true true false 4 Long 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,YEAR,-1,-1;ACRES \"ACRES\" true true false 8 Double 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,ACRES,-1,-1;ProjectID \"Project ID\" true true false 50 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,ProjectID,0,50;ProjectNM \"Project Name\" true true false 100 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,ProjectNM,0,100;Date \"Date\" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,Date,-1,-1;Status \"Status\" true true false 25 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,Status,0,25;TreatmentID \"Treatment ID\" true true false 100 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,TreatmentID,0,100;Agency_LEV \"Agency Level\" true true false 50 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,Agency_LEV,0,50;Agncy_Name \"Agency Name\" true true false 100 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,Agncy_Name,0,100;Source \"Source\" true true false 255 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,Source,0,255;Veg_Type \"Veg Type\" true true false 50 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,Veg_Type,0,50;WUI \"WUI\" true true false 3 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,WUI,0,3;CPUC \"CPUC Tier\" true true false 6 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,CPUC,0,6;RCD \"RCD\" true true false 150 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,RCD,0,150;FPD \"Fire Pro District\" true true false 155 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,FPD,0,155;Unit_Name \"Unit Name\" true true false 255 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,Unit_Name,0,255;ORIG_FID \"ORIG_FID\" true true false 4 Long 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,ORIG_FID,-1,-1;UNIT_NAME_1 \"UNIT_NAME\" true true false 80 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,UNIT_NAME_1,0,80;AGNCY_NAME_1 \"AGNCY_NAME\" true true false 100 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,AGNCY_NAME_1,0,100;AGNCY_LEV \"AGNCY_LEV\" true true false 50 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,AGNCY_LEV,0,50;MNG_AGNCY \"MNG_AGNCY\" true true false 100 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,MNG_AGNCY,0,100;MNG_AG_LEV \"MNG_AG_LEV\" true true false 50 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,MNG_AG_LEV,0,50;MNG_AG_TYP \"MNG_AG_TYP\" true true false 50 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,MNG_AG_TYP,0,50;SITE_NAME \"SITE_NAME\" true true false 100 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,SITE_NAME,0,100;LABEL_NAME \"LABEL_NAME\" true true false 255 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,LABEL_NAME,0,255;AGNCY_TYP \"AGNCY_TYP\" true true false 50 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,AGNCY_TYP,0,50;COUNTY \"COUNTY\" true true false 35 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,COUNTY,0,35;Shape_Length \"Shape_Length\" false true true 8 Double 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,Shape_Length,-1,-1;Shape_Area \"Shape_Area\" false true true 8 Double 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Veg_Summarized_Join1_Own,Shape_Area,-1,-1;Shape_Leng \"Shape_Leng\" true true false 8 Double 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\b_Reference\\WFRTF_Regions_Draft,Shape_Leng,-1,-1;RFFC_tier1 \"RFFC_tier1\" true true false 50 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\b_Reference\\WFRTF_Regions_Draft,RFFC_tier1,0,50;Shape_STAr \"Shape_STAr\" true true false 8 Double 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\b_Reference\\WFRTF_Regions_Draft,Shape_STAr,-1,-1;Shape_STLe \"Shape_STLe\" true true false 8 Double 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\b_Reference\\WFRTF_Regions_Draft,Shape_STLe,-1,-1;Shape_Length_1 \"Shape_Length\" false true true 8 Double 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\b_Reference\\WFRTF_Regions_Draft,Shape_Length,-1,-1;Shape_Area_1 \"Shape_Area\" false true true 8 Double 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\b_Reference\\WFRTF_Regions_Draft,Shape_Area,-1,-1", 
                                match_option="INTERSECT", 
                                search_radius="", 
                                distance_field_name=""
                                )

        # Process: Add Join (19) (Add Join) (management)
        print("     step 22/47 add join")
        Veg_Summarized_Polygons_Laye2_2_ = arcpy.management.AddJoin(
                                        in_layer_or_view=Treatments_Merge3_California_5_, 
                                        in_field="OBJECTID", 
                                        join_table=Veg_Summarized_Join2_RCD, 
                                        join_field="ORIG_FID", 
                                        join_type="KEEP_ALL", 
                                        index_join_fields="INDEX_JOIN_FIELDS"
                                        )

        # Process: Calculate Owner (Calculate Field) (management)
        print("     step 23/47 calculate field")
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
                                    enforce_domains="NO_ENFORCE_DOMAINS"
                                    )

        # Process: Calculate County (Calculate Field) (management)
        print("     step 24/47 calculate field")
        Veg_Summarized_Polygons_Laye2_4_ = arcpy.management.CalculateField(
                                        in_table=Veg_Summarized_Polygons_Laye, 
                                        field="Veg_Summarized_Polygons.COUNTY", 
                                        expression="ifelse(!Veg_Summarized_Join2_RCD.County!)", 
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
                                        enforce_domains="NO_ENFORCE_DOMAINS"
                                        )

        # Process: Calculate Region (Calculate Field) (management)
        print("     step 25/47 calculate field")
        Veg_Summarized_Polygons_Laye_6_ = arcpy.management.CalculateField(
                                        in_table=Veg_Summarized_Polygons_Laye2_4_, 
                                        field="Veg_Summarized_Polygons.REGION", 
                                        expression="ifelse(!Veg_Summarized_Join2_RCD.RFFC_tier1!)", 
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
                                        enforce_domains="NO_ENFORCE_DOMAINS"
                                        )

        # Process: Remove Join (10) (Remove Join) (management)
        print("     step 26/47 remove join")
        Veg_Summarized_Polygons_Laye2 = arcpy.management.RemoveJoin(
                                    in_layer_or_view=Veg_Summarized_Polygons_Laye_6_, 
                                    join_name="Veg_Summarized_Join2_RCD"
                                    )

        print("   Calculating Crosswalking Activites...")
        # Process: Add Join (Add Join) (management)
        print("     step 27/47 add join")
        Veg_Summarized_Polygons_Laye4 = arcpy.management.AddJoin(
                                    in_layer_or_view=Veg_Summarized_Polygons_Laye2, 
                                    in_field="Crosswalk", 
                                    join_table=Fuels_Treatments_Piles_Crosswalk, 
                                    join_field="Original_Activity", 
                                    join_type="KEEP_ALL", 
                                    index_join_fields="INDEX_JOIN_FIELDS"
                                    )
        
        # Process: Select by Attribute (management)
# <<<<<<< HEAD
        # Pts_enrichment_Veg_Layer_4_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=Veg_Summarized_Polygons_Laye4, where_clause="ACTIVITY_DESCRIPTION IS NULL")
# =======
        print("     step 28/47 select layer by attribute")
        Pts_enrichment_Veg_Layer_4_= arcpy.management.SelectLayerByAttribute(in_layer_or_view=Veg_Summarized_Polygons_Laye4, 
                                                                                        where_clause="ACTIVITY_DESCRIPTION IS NULL")
# >>>>>>> 1f899f8affb0c4abb79e4204a32d440344232227

        # Process: Calculate Activity Description (Calculate Field) (management)
        print("     step 29/47 calculate field")
        Updated_Input_Table_3_ = arcpy.management.CalculateField(
                                in_table=Pts_enrichment_Veg_Layer_4_, 
                                field="Veg_Summarized_Polygons.ACTIVITY_DESCRIPTION", 
                                expression="!Fuels_Treatments_Piles_Crosswalk.Activity!", 
                                expression_type="PYTHON3", code_block="", field_type="TEXT", 
                                enforce_domains="NO_ENFORCE_DOMAINS"
                                )

        # Process: Select Layer By Attribute (4) (Select Layer By Attribute) (management)
#<<<<<<< HEAD
        # Updated_Input_Table_4_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=Updated_Input_Table_3_, selection_type="CLEAR_SELECTION")
# =======
        print("     step 30/47 select attribute by layer")
        Updated_Input_Table_4_= arcpy.management.SelectLayerByAttribute(in_layer_or_view=Updated_Input_Table_3_, selection_type="CLEAR_SELECTION")
#>>>>>>> 1f899f8affb0c4abb79e4204a32d440344232227
        
        # Process: 2d Calculate Activity (2d Calculate Activity) (PC414CWIMillionAcres)
        print("     step 31/47 calculate activities")
        Veg_Summarized_Polygons_Laye3_5_ = Activity(Input_Table=Updated_Input_Table_4_)
        
        print("   Calculating Residue Fate...")
        # Process: Calculate Residue Fate (Calculate Field) (management)
        print("     step 32/47 calculate field")
        usfs_edw_facts_common_attrib1 = arcpy.management.CalculateField(
                                in_table=Veg_Summarized_Polygons_Laye3_5_, 
                                field="Veg_Summarized_Polygons.RESIDUE_FATE", 
                                expression="!Fuels_Treatments_Piles_Crosswalk.Residue_Fate!", 
                                expression_type="PYTHON3", code_block="", field_type="TEXT", 
                                enforce_domains="NO_ENFORCE_DOMAINS"
                                )

        # Process: 2g Calculate Residue Fate (2g Calculate Residue Fate) (PC414CWIMillionAcres)
        print("     step 33/47 calculate residue")
        Veg_Summarized_Polygons_Laye3_3_ = Residue(Input_Table=usfs_edw_facts_common_attrib1)

        print("   Calculating Counts to Million Acres...")
        # Process: Calculate Counts to MAS (Calculate Field) (management)
        print("     step 34/47 calculate field")
        usfs_edw_facts_common_attrib2 = arcpy.management.CalculateField(
                                in_table=Veg_Summarized_Polygons_Laye3_3_, 
                                field="Veg_Summarized_Polygons.COUNTS_TO_MAS", 
                                expression="!Fuels_Treatments_Piles_Crosswalk.Counts_to_MAS!", 
                                expression_type="PYTHON3", code_block="", field_type="TEXT", 
                                enforce_domains="NO_ENFORCE_DOMAINS"
                                )

        # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
#<<<<<<< HEAD
        # Veg_Summarized_Polygons_Laye_9_ = arcpy.management.SelectLayerByAttribute(
# =======
        print("     step 35/47 select layer by attribute")
        Veg_Summarized_Polygons_Laye_9_, Count_3_ = arcpy.management.SelectLayerByAttribute(
#>>>>>>> 1f899f8affb0c4abb79e4204a32d440344232227
                                                in_layer_or_view=usfs_edw_facts_common_attrib2, 
                                                selection_type="NEW_SELECTION", 
                                                where_clause="PRIMARY_OBJECTIVE IS NULL", 
                                                invert_where_clause=""
                                                )
        
        print('   Calculating Objective...')
        # Process: Calculate Objective (Calculate Field) (management)
        print("     step 36/47 calculate field")
        Updated_Input_Table_5_ = arcpy.management.CalculateField(
                            in_table=Veg_Summarized_Polygons_Laye_9_, 
                            field="Veg_Summarized_Polygons.PRIMARY_OBJECTIVE", 
                            expression="!Fuels_Treatments_Piles_Crosswalk.Objective!", 
                            expression_type="PYTHON3", code_block="", field_type="TEXT", 
                            enforce_domains="NO_ENFORCE_DOMAINS"
                            )
                
        # Process: 2e Calculate Objective (2e Calculate Objective) (PC414CWIMillionAcres)
        print("     step 37/47 calculate objective")
        Veg_Summarized_Polygons_Laye3_2_ = Objective(Input_Table=Updated_Input_Table_5_)

        # Process: Select Layer By Attribute (2) (Select Layer By Attribute) (management)
#<<<<<<< HEAD
        # Veg_Summarized_Polygons_Laye_10_ = arcpy.management.SelectLayerByAttribute(
# =======
        print("     step 38/47 select layer by attribute")
        Veg_Summarized_Polygons_Laye_10_, Count_7_ = arcpy.management.SelectLayerByAttribute(
#>>>>>>> 1f899f8affb0c4abb79e4204a32d440344232227
                                                in_layer_or_view=Veg_Summarized_Polygons_Laye3_2_, 
                                                selection_type="CLEAR_SELECTION", 
                                                where_clause="", 
                                                invert_where_clause=""
                                                )

        # Process: Remove Join (2) (Remove Join) (management)
        print("     step 39/47 remove join")
        Layer_With_Join_Removed_2_ = arcpy.management.RemoveJoin(
                                in_layer_or_view=Veg_Summarized_Polygons_Laye_10_, 
                                join_name="Fuels_Treatments_Piles_Crosswalk"
                                )

        print('   Calculating Activity Category...')
        # Process: 2f Calculate Category (2f Calculate Category) (PC414CWIMillionAcres)
        print("     step 40/47 calculate category")
        Updated_Input_Table = Category(Input_Table=Layer_With_Join_Removed_2_)

        print('     step 41/47 Calculating Years...')
        # Process: 2h Calculate Year (2h Calculate Year) (PC414CWIMillionAcres)
        Veg_Summarized_Polygons_Laye3_7_ = Year(Input_Table=Updated_Input_Table)

        print("     step 42/47 Calculating Latitude and Longitude...")
        # Process: Calculate Geometry Attributes (3) (Calculate Geometry Attributes) (management)
        Veg_Summarized_Polygons_Laye_4_ = arcpy.management.CalculateGeometryAttributes(
                                        in_features=Veg_Summarized_Polygons_Laye3_7_, 
                                        geometry_property=[["LATITUDE", "INSIDE_Y"], ["LONGITUDE", "INSIDE_X"]], 
                                        length_unit="", 
                                        area_unit="", 
                                        coordinate_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", 
                                        coordinate_format="DD"
                                        )

        # Process: Calculate Geometry Attributes (4) (Calculate Geometry Attributes) (management)
        print("     step 43/47 calculate geometry attributes")
        Veg_Summarized_Polygons_Laye_8_ = arcpy.management.CalculateGeometryAttributes(
                                        in_features=Veg_Summarized_Polygons_Laye_4_, 
                                        geometry_property=[["TREATMENT_AREA", "AREA"]], 
                                        length_unit="", 
                                        area_unit="ACRES_US", 
                                        coordinate_system="PROJCS[\"NAD_1983_California_Teale_Albers\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Albers\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",-4000000.0],PARAMETER[\"Central_Meridian\",-120.0],PARAMETER[\"Standard_Parallel_1\",34.0],PARAMETER[\"Standard_Parallel_2\",40.5],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]", 
                                        coordinate_format="SAME_AS_INPUT"
                                        )

        # # Process: Keep Fields (Delete Field) (management)
        print("     step 44/47 keep fields")
        Veg_Summarized_Polygons_Laye_11_ = KeepFields(Veg_Summarized_Polygons_Laye_8_)

        # Process: Delete Identical (Delete Identical) (management)
        print("     step 45/47 delete identical")
        Veg_Summarized_Polygons_Laye_12_ = arcpy.management.DeleteIdentical(
                                in_dataset=Veg_Summarized_Polygons_Laye_11_, 
                                fields=["PROJECTID_USER", "AGENCY", "ORG_ADMIN_p", 
                                        "PROJECT_CONTACT", "PROJECT_EMAIL", "ADMINISTERING_ORG", 
                                        "PROJECT_NAME", "PROJECT_STATUS", "PROJECT_START", 
                                        "PROJECT_END", "PRIMARY_FUNDING_SOURCE", "PRIMARY_FUNDING_ORG", 
                                        "IMPLEMENTING_ORG", "LATITUDE", "LONGITUDE", 
                                        "BatchID_p", "Val_Status_p", "Val_Message_p", 
                                        "Val_RunDate_p", "Review_Status_p", "Review_Message_p", 
                                        "Review_RunDate_p", "Dataload_Status_p", "Dataload_Msg_p", 
                                        "TRMTID_USER", "PROJECTID", "PROJECTNAME_", 
                                        "ORG_ADMIN_t", "PRIMARY_OWNERSHIP_GROUP", "PRIMARY_OBJECTIVE", 
                                        "SECONDARY_OBJECTIVE", "TERTIARY_OBJECTIVE", "TREATMENT_STATUS", 
                                        "COUNTY", "IN_WUI", "REGION", "TREATMENT_AREA", "TREATMENT_START", 
                                        "TREATMENT_END", "RETREATMENT_DATE_EST", "TREATMENT_NAME", "BatchID", 
                                        "Val_Status_t", "Val_Message_t", "Val_RunDate_t", "Review_Status_t", 
                                        "Review_Message_t", "Review_RunDate_t", "Dataload_Status_t", "Dataload_Msg_t", 
                                        "ACTIVID_USER", "TREATMENTID_", "ORG_ADMIN_a", "ACTIVITY_DESCRIPTION", 
                                        "ACTIVITY_CAT", "BROAD_VEGETATION_TYPE", "BVT_USERD", "ACTIVITY_STATUS", 
                                        "ACTIVITY_QUANTITY", "ACTIVITY_UOM", "ACTIVITY_START", "ACTIVITY_END", 
                                        "ADMIN_ORG_NAME", "IMPLEM_ORG_NAME", "PRIMARY_FUND_SRC_NAME", 
                                        "PRIMARY_FUND_ORG_NAME", "SECONDARY_FUND_SRC_NAME", "SECONDARY_FUND_ORG_NAME", 
                                        "TERTIARY_FUND_SRC_NAME", "TERTIARY_FUND_ORG_NAME", "ACTIVITY_PRCT", 
                                        "RESIDUE_FATE", "RESIDUE_FATE_QUANTITY", "RESIDUE_FATE_UNITS", 
                                        "ACTIVITY_NAME", "VAL_STATUS_a", "VAL_MSG_a", "VAL_RUNDATE_a", 
                                        "REVIEW_STATUS_a", "REVIEW_MSG_a", "REVIEW_RUNDATE_a", "DATALOAD_STATUS_a", 
                                        "DATALOAD_MSG_a", "Source", "Year", "Year_txt", "Act_Code", "Crosswalk", 
                                        "Federal_FY", "State_FY", "TRMT_GEOM", "COUNTS_TO_MAS"], 
                                xy_tolerance="", 
                                z_tolerance=0
                                )        
        
        # Process: Select (Select) (analysis)
        print("     step 46/47 select")
        Veg_Summarized_Polygons_Laye_13_ = arcpy.analysis.Select(
            in_features=Veg_Summarized_Polygons_Laye_12_, 
            out_feature_class=enrich_out, 
            where_clause="County IS NOT NULL"
            )
        
        print("     step 47/47 delete scratch files")
        if delete_scratch:
            # print('Deleting Scratch Files')
            delete_scratch_files(gdb = scratch_workspace, delete_fc = 'yes', delete_table = 'yes', delete_ds = 'yes')

        print("enrich polygons complete...")    

if __name__ == '__main__':
#<<<<<<< HEAD
    runner(workspace,scratch_workspace,enrich_polygons, '*argv[1:]')
    # # Global Environment settings
    # with arcpy.EnvManager(
    # extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""", 
    # outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""", 
    # preserveGlobalIds=True, 
    # qualifiedFieldNames=False, 
    # scratchWorkspace=scratch_workspace, 
    # transferDomains=True, 
    # transferGDBAttributeProperties=True, 
    # workspace=workspace):
    #     enrich_polygons(*argv[1:])
# =======
    # runner(workspace,scratch_workspace,aEnrichmentsPolygon1, '*argv[1:]')
    # Global Environment settings
    with arcpy.EnvManager(
    extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""", 
    outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""", 
    preserveGlobalIds=True, 
    qualifiedFieldNames=False, 
    scratchWorkspace=scratch_workspace, 
    transferDomains=True, 
    transferGDBAttributeProperties=True, 
    workspace=workspace):
        enrich_polygons(*argv[1:])
#>>>>>>> 1f899f8affb0c4abb79e4204a32d440344232227
