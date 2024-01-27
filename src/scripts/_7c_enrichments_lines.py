"""
# Description:  Adds vegetation, ownership, county, WUI, Task Force Region, and 
#               year attributes to the dataset.  
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import arcpy
# import os
from ._7b_enrichments_pts import enrich_points
from ._2k_keep_fields import KeepFields
# from sys import argv
from .utils import init_gdb, delete_scratch_files, runner

original_gdb, workspace, scratch_workspace = init_gdb()
# TODO add print steps

def enrich_lines(line_fc, delete_scratch=False):  # 7c Enrichments Lines
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

        WFR_TF_Template = os.path.join(workspace, "b_Reference", "WFR_TF_Template")

        # define intermediary scratch file paths
        Line_to_Pt = os.path.join(scratch_workspace, "Line_to_Pt")
        line_to_pt_enriched = os.path.join(scratch_workspace, "line_to_pt_enriched")
        Line_Layer_Temp_CopyFeatures = os.path.join(
            scratch_workspace, "Line_Layer_Temp_CopyFeatures"
        )
        Line_Enriched_Temp_CopyFeatures = os.path.join(
            scratch_workspace, "Line_Enriched_Temp_CopyFeatures"
        )

        # BEGIN TOOL CHAIN
        print("Executing Line Enrichments...")
        # Process: Feature To Point (Feature To Point) (management)
        # Kyle:skip to speed up debugging
        print("   step 1 convert to points")
        arcpy.management.FeatureToPoint(
            in_features=line_fc, out_feature_class=Line_to_Pt, point_location="INSIDE"
        )

        # Process: 7b Enrichments pts (7b Enrichments pts)
        # Kyle: skip to speed up debugging
        print("   step 2 execute enrich_points...")
        enrich_points(
            enrich_pts_out=line_to_pt_enriched,
            enrich_pts_in=Line_to_Pt,
            delete_scratch=False,
        )  # within 7c, we can set delete_scratch to false or true

        print("   step 3 importing point attributes")
        # Process: Add Join (Add Join) (management)
        CalTrans_act_ln_standardized = arcpy.management.AddJoin(
            in_layer_or_view=line_fc,
            in_field="PROJECTID_USER",
            join_table=line_to_pt_enriched,
            join_field="PROJECTID_USER",
            join_type="KEEP_ALL",
            index_join_fields="INDEX_JOIN_FIELDS",
        )  # changed to NO

        # field_names = [f.name for f in arcpy.ListFields(CalTrans_act_ln_standardized)]
        # print('field names after AddJoin\n',field_names,'\n')

        # Process: Copy Features (2) (Copy Features) (management)
        arcpy.management.CopyFeatures(
            in_features=CalTrans_act_ln_standardized,
            out_feature_class=Line_Layer_Temp_CopyFeatures,
            config_keyword="",
            spatial_grid_1=None,
            spatial_grid_2=None,
            spatial_grid_3=None,
        )
        # field_names = [f.name for f in arcpy.ListFields(Line_Layer_Temp_CopyFeatures)]
        # print('field names after CopyFeatures, no maintain fully qualified field names\n',field_names,'\n')

        # Process: Latitude (Calculate Field) (management)
        Updated_Input_Table_1_ = arcpy.management.CalculateField(
            in_table=Line_Layer_Temp_CopyFeatures,
            field="LATITUDE",
            expression="!LATITUDE_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Longitude (Calculate Field) (management)
        Updated_Input_Table_2_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_1_,
            field="LONGITUDE",
            expression="!LONGITUDE_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Owner (Calculate Field) (management)
        Updated_Input_Table_2A_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_2_,
            field="PRIMARY_OWNERSHIP_GROUP",
            expression="!PRIMARY_OWNERSHIP_GROUP_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Primary Objective (Calculate Field) (management)
        CDFW_lines_stand_SpatialJoin2_2_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_2A_,
            field="PRIMARY_OBJECTIVE",
            expression="!PRIMARY_OBJECTIVE_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate County (Calculate Field) (management)
        Updated_Input_Table_3_ = arcpy.management.CalculateField(
            in_table=CDFW_lines_stand_SpatialJoin2_2_,
            field="COUNTY",
            expression="!COUNTY_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate WUI (Calculate Field) (management)
        Updated_Input_Table = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_3_,
            field="IN_WUI",
            expression="!IN_WUI_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Region (Calculate Field) (management)
        Updated_Input_Table_4_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table,
            field="REGION",
            expression="!REGION_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Activity Description (Calculate Field) (management)
        Updated_Input_Table_5_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_4_,
            field="ACTIVITY_DESCRIPTION",
            expression="!ACTIVITY_DESCRIPTION_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Veg (Calculate Field) (management)
        CDFW_lines_stand_SpatialJoin2_3_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_5_,
            field="BROAD_VEGETATION_TYPE",
            expression="!BROAD_VEGETATION_TYPE_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Category (Calculate Field) (management)
        Updated_Input_Table_6_ = arcpy.management.CalculateField(
            in_table=CDFW_lines_stand_SpatialJoin2_3_,
            field="ACTIVITY_CAT",
            expression="!ACTIVITY_CAT_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Residue (Calculate Field) (management)
        Updated_Input_Table_7_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_6_,
            field="RESIDUE_FATE",
            expression="!RESIDUE_FATE_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Calendar Year (Calculate Field) (management)
        Updated_Input_Table_8_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_7_,
            field="Year",
            expression="!Year_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Year as Text (Calculate Field) (management)
        Updated_Input_Table_9_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_8_,
            field="Year_txt",
            expression="!Year!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Fed FY (Calculate Field) (management)
        Veg_Summarized_Polygons_Laye3_8_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_9_,
            field="Federal_FY",
            expression="!Federal_FY_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate State FY (Calculate Field) (management)
        Veg_Summarized_Polygons_Laye3_7_ = arcpy.management.CalculateField(
            in_table=Veg_Summarized_Polygons_Laye3_8_,
            field="State_FY",
            expression="!State_FY_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # field_names = [f.name for f in arcpy.ListFields(Veg_Summarized_Polygons_Laye3_7_)]
        # print('field names after all CalculateField operations\n',field_names,'\n')

        # Process: Delete Field (Delete Field) (management)
        # Line_Layer_Temp_CopyFeatures1_3_ = KeepFields(Veg_Summarized_Polygons_Laye3_7_)

        # field_names = [f.name for f in arcpy.ListFields(Line_Layer_Temp_CopyFeatures1_3_)]
        # print('field names after DeleteField\n',field_names,'\n')

        # template_field_names = [f.name for f in arcpy.ListFields(WFR_TF_Template)]
        # print('field names of WFR_TF_Template\n',template_field_names,'\n')

        # not_in_field_names = [f for f in template_field_names if f not in field_names]
        # print('template field names not in temp FC schema\n',not_in_field_names,'\n')

        print("Creating New FC off of Template, Appending final output to it...")
        # Process: Create Feature Class (Create Feature Class) (management)
        Line_Enriched_Temp_CopyFeatures = arcpy.management.CreateFeatureclass(
            out_path=scratch_workspace,
            out_name="Line_Enriched_Temp_CopyFeatures",
            geometry_type="POLYLINE",
            template=[WFR_TF_Template],
            has_m="DISABLED",
            has_z="DISABLED",
            spatial_reference='PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]];-16909700 -8597000 10000;#;#;0.001;#;#;IsHighPrecision',
            config_keyword="",
            spatial_grid_1=0,
            spatial_grid_2=0,
            spatial_grid_3=0,
            out_alias="",
        )

        # Appending final temp FC to a new blank dataset created off of WFR_TF_Template catches error
        # "~\scratch.gdb\Line_Layer_Temp_CopyFeatures does not match the schema of target ~\scratch.gdb\Line_Enriched_Temp_CopyFeatures"
        # looks like 'Shape_Area' field from WFR_TR_Template is not in the final output FC of this tool, makes sense cause wouldn't need Shape_Area for a PolyLine FC
        # Deleting Shape_Area field isn't possible because it is one of those grey-ed out auto generated fields..
        # So we changed schema_type from "TEST" to "NO_TEST" so that if a field does not have a match it is not carried over during the Append

        # Process: Append (Append) (management)
        Line_Enriched_Temp_CopyFeatures_append = arcpy.management.Append(
            inputs=[Veg_Summarized_Polygons_Laye3_7_],
            target=Line_Enriched_Temp_CopyFeatures,
            schema_type="NO_TEST",  # only field mismatch is Shape_Area which we don't care about
        )

        # if delete_scratch:
        #     print("Deleting Scratch Files")
        #     delete_scratch_files(
        #         gdb=scratch_workspace, delete_fc="yes", delete_table="yes", delete_ds="yes"
        #     )

        return Line_Enriched_Temp_CopyFeatures_append  # does this capture the object that has since been renamed or only the file path as defined by the variable ln469? # Line_Enriched_Temp_CopyFeatures


# if __name__ == "__main__":
#     runner(workspace, scratch_workspace, enrich_lines, "*argv[1:]")
    # # Global Environment settings
    # with arcpy.EnvManager(
    # extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""",  outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""",
    # preserveGlobalIds=True,
    # qualifiedFieldNames=False,
    # scratchWorkspace=scratch_workspace,
    # transferDomains=True,
    # transferGDBAttributeProperties=True,
    # workspace=workspace):
    #     enrich_lines(*argv[1:])
