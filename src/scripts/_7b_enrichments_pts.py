import arcpy
from ._2d_calculate_activity import Activity
from ._2f_calculate_category import Category
from ._2e_calculate_objective import Objective
from ._2g_calculate_residue_fate import Residue
from ._2k_keep_fields import KeepFields
from ._2h_calculate_year import Year
from sys import argv
from .utils import init_gdb, delete_scratch_files, runner
import os
original_gdb, workspace, scratch_workspace = init_gdb()

def enrich_points(enrich_pts_out, enrich_pts_in, delete_scratch=False):  # 7b Enrichments pts

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False
    arcpy.env.qualifiedFieldNames = False 
    
    WUI = os.path.join(workspace, "b_Reference", "RasterT_Reclass_WUI")
    Fuels_Treatments_Piles_Crosswalk_2_ = os.path.join(workspace, "Fuels_Treatments_Piles_Crosswalk")
    CPAD_Ownership_Update = os.path.join(workspace, "b_Reference", "CPAD_Ownership_Update")
    WFRTF_Regions_Draft = os.path.join(workspace, "b_Reference", "WFRTF_Regions_Draft")
    RasterT_fveg1 = os.path.join(workspace, "b_Reference", "RasterT_fveg1")

    Pts_enrichment_Veg = os.path.join(scratch_workspace, "Pts_enrichment_Veg")
    Pts_enrichment_copy = os.path.join(scratch_workspace, "Pts_enrichment_copy")
    Pts_enrichment_Own = os.path.join(scratch_workspace, "Pts_enrichment_Own")
    Pts_enrichment_RCD = os.path.join(scratch_workspace, "Pts_enrichment_RCD")

    # Process: Copy Features (Copy Features) (management)
    arcpy.management.CopyFeatures(in_features=enrich_pts_in, 
                                  out_feature_class=Pts_enrichment_copy,
                                  config_keyword="",
                                  spatial_grid_1=None,
                                  spatial_grid_2=None,
                                  spatial_grid_3=None)

    # Process: Select WUI Null (Select Layer By Attribute) (management)
    Pts_enrichment_copy_Layer1, Count = arcpy.management.SelectLayerByAttribute(in_layer_or_view=Pts_enrichment_copy,
                                                                                selection_type="NEW_SELECTION",
                                                                                where_clause="IN_WUI IS NULL Or IN_WUI = ''",
                                                                                invert_where_clause="")

    # Process: Select WUI Intersect (Select Layer By Location) (management)
    Pts_enrichment_copy_Layer, Output_Layer_Names_2_, Count_2_ = arcpy.management.SelectLayerByLocation(in_layer=[Pts_enrichment_copy_Layer1],
                                                                                                        overlap_type="INTERSECT",
                                                                                                        select_features=WUI,
                                                                                                        search_distance="",
                                                                                                        selection_type="SUBSET_SELECTION",
                                                                                                        invert_spatial_relationship="NOT_INVERT")

    # Process: Calculate In WUI (Calculate Field) (management)
    Pts_enrichment_copy_Layer_2_ = arcpy.management.CalculateField(in_table=Pts_enrichment_copy_Layer,
                                                                   field="IN_WUI",
                                                                   expression="\"WUI_AUTO_POP\"",
                                                                   expression_type="PYTHON3",
                                                                   code_block="",
                                                                   field_type="TEXT",
                                                                   enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Select WUI Null 2 (Select Layer By Attribute) (management)
    Pts_enrichment_copy_Layer_3_, Count_3_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=Pts_enrichment_copy_Layer_2_,
                                                                                     selection_type="NEW_SELECTION",
                                                                                     where_clause="IN_WUI IS NULL Or IN_WUI = ''",
                                                                                     invert_where_clause="")

    # Process: Calculate Non WUI (Calculate Field) (management)
    Pts_enrichment_copy_Layer_4_ = arcpy.management.CalculateField(in_table=Pts_enrichment_copy_Layer_3_,
                                                                   field="IN_WUI",
                                                                   expression="\"NON-WUI_AUTO_POP\"",
                                                                   expression_type="PYTHON3",
                                                                   code_block="",
                                                                   field_type="TEXT",
                                                                   enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Clear Selection (Select Layer By Attribute) (management)
    Treatments_Merge3_California_5_, Count_4_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=Pts_enrichment_copy_Layer_4_,
                                                                                        selection_type="CLEAR_SELECTION",
                                                                                        where_clause="",
                                                                                        invert_where_clause="")

    # Process: Spatial Join (Spatial Join) (analysis)
    if Treatments_Merge3_California_5_:
        arcpy.analysis.SpatialJoin(target_features=Pts_enrichment_copy,
                                   join_features=CPAD_Ownership_Update,
                                   out_feature_class=Pts_enrichment_Own,
                                   join_operation="JOIN_ONE_TO_ONE",
                                   join_type="KEEP_ALL",
                                   field_mapping="",
                                   match_option="CLOSEST",
                                   search_radius="",
                                   distance_field_name="")

    # Process: Spatial Join (2) (Spatial Join) (analysis)
    if Treatments_Merge3_California_5_:
        arcpy.analysis.SpatialJoin(target_features=Pts_enrichment_Own,
                                   join_features=WFRTF_Regions_Draft,
                                   out_feature_class=Pts_enrichment_RCD,
                                   join_operation="JOIN_ONE_TO_ONE",
                                   join_type="KEEP_ALL",
                                   field_mapping="",
                                   match_option="CLOSEST",
                                   search_radius="",
                                   distance_field_name="")

    # Process: Spatial Join (3) (Spatial Join) (analysis)
    if Treatments_Merge3_California_5_:
        arcpy.analysis.SpatialJoin(target_features=Pts_enrichment_RCD,
                                   join_features=RasterT_fveg1,
                                   out_feature_class=Pts_enrichment_Veg,
                                   join_operation="JOIN_ONE_TO_ONE",
                                   join_type="KEEP_ALL",
                                   field_mapping="",
                                   match_option="CLOSEST",
                                   search_radius="",
                                   distance_field_name="")


    # Process: Calculate Owner (Calculate Field) (management)
    if Treatments_Merge3_California_5_:
        Veg_Summarized_Polygons_Laye_3_ = arcpy.management.CalculateField(in_table=Pts_enrichment_Veg, 
                                                                          field="PRIMARY_OWNERSHIP_GROUP",
                                                                          expression="ifelse(!AGNCY_LEV!)",
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
        return Own""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate County (Calculate Field) (management)    
    if Treatments_Merge3_California_5_:
        Veg_Summarized_Polygons_Laye_4_ = arcpy.management.CalculateField(in_table=Veg_Summarized_Polygons_Laye_3_,
                                                                          field="COUNTY",
                                                                          expression="ifelse(!COUNTY_1!)",
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
        return CO
""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Region (Calculate Field) (management)
    if Treatments_Merge3_California_5_:
        Veg_Summarized_Polygons_Laye_6_ = arcpy.management.CalculateField(in_table=Veg_Summarized_Polygons_Laye_4_,
                                                                          field="REGION",
                                                                          expression="ifelse(!RFFC_tier1!)",
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
                                            return Reg""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Veg (Calculate Field) (management)
    if Treatments_Merge3_California_5_:
        Veg_Summarized_Polygons_Laye_2_ = arcpy.management.CalculateField(in_table=Veg_Summarized_Polygons_Laye_6_,
                                                                          field="BROAD_VEGETATION_TYPE",
                                                                          expression="ifelse(!WHR13NAME!)",
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
        return VEG""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate BVT User Defined (Calculate Field) (management)
    if Treatments_Merge3_California_5_:
        Pts_enrichment_Veg_2_ = arcpy.management.CalculateField(in_table=Veg_Summarized_Polygons_Laye_2_,
                                                                field="BVT_USERD",
                                                                expression="\"NO\"",
                                                                expression_type="PYTHON3",
                                                                code_block="",
                                                                field_type="TEXT",
                                                                enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Add Join (Add Join) (management)
    if Pts_enrichment_Veg_2_ and Treatments_Merge3_California_5_:
        Pts_enrichment_Veg_Layer = arcpy.management.AddJoin(in_layer_or_view=Pts_enrichment_Veg,
                                                            in_field="Crosswalk",
                                                            join_table=Fuels_Treatments_Piles_Crosswalk_2_,
                                                            join_field="Original_Activity",
                                                            join_type="KEEP_ALL",
                                                            index_join_fields="INDEX_JOIN_FIELDS")
    # Process: Select by Attribute (management)
    if Pts_enrichment_Veg_2_ and Treatments_Merge3_California_5_: 
        Pts_enrichment_Veg_Layer_4_, Count_7_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=Pts_enrichment_Veg_Layer, where_clause="ACTIVITY_DESCRIPTION IS NULL")

    # Process: Calculate Activity Description (Calculate Field) (management)
    if Pts_enrichment_Veg_2_ and Treatments_Merge3_California_5_:
        Updated_Input_Table_3_ = arcpy.management.CalculateField(in_table=Pts_enrichment_Veg_Layer_4_, field="Pts_enrichment_Veg.ACTIVITY_DESCRIPTION", expression="!Fuels_Treatments_Piles_Crosswalk.Activity!", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Select Layer By Attribute (4) (Select Layer By Attribute) (management)
        Updated_Input_Table_4_, Count_8_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=Updated_Input_Table_3_, selection_type="CLEAR_SELECTION")

    # Process: 2d Calculate Activity (2d Calculate Activity) (PC414CWIMillionAcres)
    if Pts_enrichment_Veg_2_ and Treatments_Merge3_California_5_:
        Veg_Summarized_Polygons_Laye3_3_ = Activity(Input_Table=Updated_Input_Table_4_)

    # Process: Calculate Residue Fate (Calculate Field) (management)
    if Pts_enrichment_Veg_2_ and Treatments_Merge3_California_5_:
        Veg_Summarized_Polygons_Laye3_4_ = arcpy.management.CalculateField(in_table=Veg_Summarized_Polygons_Laye3_3_, field="Pts_enrichment_Veg.RESIDUE_FATE", expression="!Fuels_Treatments_Piles_Crosswalk.Residue_Fate!", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: 2g Calculate Residue Fate (2g Calculate Residue Fate) (PC414CWIMillionAcres)
    if Pts_enrichment_Veg_2_ and Treatments_Merge3_California_5_:
        Veg_Summarized_Polygons_Laye3_5_ = Residue(Input_Table=Veg_Summarized_Polygons_Laye3_4_)

    # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
    if Pts_enrichment_Veg_2_ and Treatments_Merge3_California_5_:
        Pts_enrichment_Veg_Layer_3_, Count_5_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=Veg_Summarized_Polygons_Laye3_5_,
                                                                                        selection_type="NEW_SELECTION",
                                                                                        where_clause="Pts_enrichment_Veg.PRIMARY_OBJECTIVE IS NULL",
                                                                                        invert_where_clause="")

    # Process: Calculate Objective (Calculate Field) (management)
    if Pts_enrichment_Veg_2_ and Treatments_Merge3_California_5_:
        Updated_Input_Table_5_ = arcpy.management.CalculateField(in_table=Pts_enrichment_Veg_Layer_3_, field="Pts_enrichment_Veg.PRIMARY_OBJECTIVE", expression="!Fuels_Treatments_Piles_Crosswalk.Objective!", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: 2e Calculate Objective (2e Calculate Objective) (PC414CWIMillionAcres)
    if Pts_enrichment_Veg_2_ and Treatments_Merge3_California_5_:
        Veg_Summarized_Polygons_Laye3_2_ = Objective(Input_Table=Updated_Input_Table_5_)

    # Process: Select Layer By Attribute (2) (Select Layer By Attribute) (management)
    if Pts_enrichment_Veg_2_ and Treatments_Merge3_California_5_:
        Pts_enrichment_Veg_Layer_5_, Count_6_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=Veg_Summarized_Polygons_Laye3_2_,
                                                                                        selection_type="CLEAR_SELECTION",
                                                                                        where_clause="", 
                                                                                        invert_where_clause="")

    # Process: Remove Join (2) (Remove Join) (management)
    if Pts_enrichment_Veg_2_ and Treatments_Merge3_California_5_:
        Pts_enrichment_Veg_Layer_2_ = arcpy.management.RemoveJoin(in_layer_or_view=Pts_enrichment_Veg_Layer_5_,
                                                                  join_name="Fuels_Treatments_Piles_Crosswalk")

    # Process: 2f Calculate Category (2f Calculate Category) (PC414CWIMillionAcres)
    if Pts_enrichment_Veg_2_ and Treatments_Merge3_California_5_:
        Updated_Input_Table = Category(Input_Table=Pts_enrichment_Veg_Layer_2_)

    # Process: 2h Calculate Year (2h Calculate Year) (PC414CWIMillionAcres)
    if Pts_enrichment_Veg_2_ and Treatments_Merge3_California_5_:
        Veg_Summarized_Polygons_Laye3_7_ = Year(Input_Table=Updated_Input_Table)

    # Process: Delete Field (3) (Delete Field) (management)
    ## Had to remove "ORG_ADMIN" from drop list for CalVTP dataset
    if Pts_enrichment_Veg_2_ and Treatments_Merge3_California_5_:
        Pts_enrichment_Veg_Layer2 = KeepFields(Veg_Summarized_Polygons_Laye3_7_)

    # Process: Calculate Geometry Attributes (Calculate Geometry Attributes) (management)
    Pts_enrichment_Veg_Layer3 = arcpy.management.CalculateGeometryAttributes(in_features=Pts_enrichment_Veg_Layer2, 
                                geometry_property=[["LATITUDE", "Point y-coordinate"], ["LONGITUDE", "Point x-coordinate"]], 
                                length_unit="", area_unit="", 
                                coordinate_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", 
                                coordinate_format="DD"
                                )

    # Process: Delete Identical (Delete Identical) (management)
    Pts_enrichment_Veg_Layer4 = arcpy.management.DeleteIdentical(
                                in_dataset=Pts_enrichment_Veg_Layer3, 
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
                                        "Federal_FY", "State_FY", "TRMT_GEOM"], 
                                xy_tolerance="", 
                                z_tolerance=0
                                )        

    # Process: Select (Select) (analysis)
    if Pts_enrichment_Veg_2_ and Treatments_Merge3_California_5_:
        arcpy.analysis.Select(in_features=Pts_enrichment_Veg_Layer4, 
                              out_feature_class=enrich_pts_out,
                              where_clause="County IS NOT NULL")

    if delete_scratch:
        print('Deleting Scratch Files')
        delete_scratch_files(gdb = scratch_workspace, delete_fc = 'yes', delete_table = 'yes', delete_ds = 'yes')
    
if __name__ == '__main__':
    runner(workspace,scratch_workspace,enrich_points, '*argv[1:]')
    # # Global Environment settings
    # with arcpy.EnvManager(
    # extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""",  outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""", 
    # preserveGlobalIds=True, 
    # qualifiedFieldNames=False, 
    # scratchWorkspace=scratch_workspace, 
    # transferDomains=True, 
    # transferGDBAttributeProperties=True, 
    # workspace=workspace):
    #     enrich_points(*argv[1:])
