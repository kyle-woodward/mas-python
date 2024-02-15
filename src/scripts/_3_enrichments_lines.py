"""
# Description:  Adds vegetation, ownership, county, WUI, Task Force Region, and 
#               year attributes to the dataset.  
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import datetime
start_ln = datetime.datetime.now()

import arcpy
from scripts._3_enrichments_pts import enrich_points
from .utils import init_gdb

workspace, scratch_workspace = init_gdb()

def enrich_lines(line_fc): 
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
        print("   Executing Line Enrichments...")
        print(f"     Line Enrichment Start Time {start_ln}")

        WFR_TF_Template = os.path.join(workspace, "a_Reference", "WFR_TF_Template")

        # define intermediary scratch file paths
        Line_to_Pt = os.path.join(scratch_workspace, "Line_to_Pt")
        line_to_pt_enriched = os.path.join(scratch_workspace, "line_to_pt_enriched")
        Line_Layer_Temp_CopyFeatures = os.path.join(scratch_workspace, "Line_Layer_Temp_CopyFeatures")

        # BEGIN TOOL CHAIN
        print("       enrich step 1/4 convert to points")
        arcpy.management.FeatureToPoint(
            in_features=line_fc, 
            out_feature_class=Line_to_Pt, 
            point_location="INSIDE"
        )

        print("       enrich step 2/4 execute enrich_points...")
        enrich_points(
            enrich_pts_in=Line_to_Pt,
            enrich_pts_out=line_to_pt_enriched
        )

        print("       enrich step 3/4 importing attributes")
        standardized_1 = arcpy.management.AddJoin(
            in_layer_or_view=line_fc,
            in_field="ACTIVID_USER",
            join_table=line_to_pt_enriched,
            join_field="ACTIVID_USER",
            join_type="KEEP_ALL",
            index_join_fields="INDEX_JOIN_FIELDS",
        )

        copy_1 = arcpy.management.CopyFeatures(
            in_features=standardized_1,
            out_feature_class=Line_Layer_Temp_CopyFeatures,
        )

        calc_field_1 = arcpy.management.CalculateField(
            in_table=copy_1,
            field="LATITUDE",
            expression="!LATITUDE_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_2 = arcpy.management.CalculateField(
            in_table=calc_field_1,
            field="LONGITUDE",
            expression="!LONGITUDE_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_3 = arcpy.management.CalculateField(
            in_table=calc_field_2,
            field="PRIMARY_OWNERSHIP_GROUP",
            expression="!PRIMARY_OWNERSHIP_GROUP_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_4 = arcpy.management.CalculateField(
            in_table=calc_field_3,
            field="PRIMARY_OBJECTIVE",
            expression="!PRIMARY_OBJECTIVE_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_5 = arcpy.management.CalculateField(
            in_table=calc_field_4,
            field="COUNTY",
            expression="!COUNTY_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_6 = arcpy.management.CalculateField(
            in_table=calc_field_5,
            field="IN_WUI",
            expression="!IN_WUI_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_7 = arcpy.management.CalculateField(
            in_table=calc_field_6,
            field="REGION",
            expression="!REGION_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_8 = arcpy.management.CalculateField(
            in_table=calc_field_7,
            field="ACTIVITY_DESCRIPTION",
            expression="!ACTIVITY_DESCRIPTION_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_9 = arcpy.management.CalculateField(
            in_table=calc_field_8,
            field="BROAD_VEGETATION_TYPE",
            expression="!BROAD_VEGETATION_TYPE_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )
        
        calc_field_10 = arcpy.management.CalculateField(
            in_table=calc_field_9,
            field="BVT_USERD",
            expression="!BVT_USERD_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_11 = arcpy.management.CalculateField(
            in_table=calc_field_10,
            field="ACTIVITY_CAT",
            expression="!ACTIVITY_CAT_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_12 = arcpy.management.CalculateField(
            in_table=calc_field_11,
            field="RESIDUE_FATE",
            expression="!RESIDUE_FATE_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_13 = arcpy.management.CalculateField(
            in_table=calc_field_12,
            field="Year",
            expression="!Year_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_14 = arcpy.management.CalculateField(
            in_table=calc_field_13,
            field="Year_txt",
            expression="!Year!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_15 = arcpy.management.CalculateField(
            in_table=calc_field_14,
            field="Federal_FY",
            expression="!Federal_FY_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_16 = arcpy.management.CalculateField(
            in_table=calc_field_15,
            field="State_FY",
            expression="!State_FY_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_17 = arcpy.management.CalculateField(
            in_table=calc_field_16,
            field="COUNTS_TO_MAS",
            expression="!COUNTS_TO_MAS_1!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_18 = arcpy.management.CalculateField(
            in_table=calc_field_17, 
            field="TRMT_GEOM", 
            expression="'LINE'"
        )

        print("       enrich step 4/4 align to template")
        Template_1 = arcpy.management.CreateFeatureclass(
            out_path=scratch_workspace,
            out_name="Line_Enriched_Temp_CopyFeatures",
            geometry_type="POLYLINE",
            template=[WFR_TF_Template],
            spatial_reference="NAD 1983 California (Teale) Albers (Meters)",
        )

        Line_Enriched_Final = arcpy.management.Append(
            inputs=[calc_field_18],
            target=Template_1,
            schema_type="NO_TEST",  # only field mismatch is Shape_Area which we don't care about
        )

        end_ln = datetime.datetime.now()
        elapsed_ln = (end_ln-start_ln)
        hours, remainder1 = divmod(elapsed_ln.total_seconds(), 3600)
        minutes, remainder2 = divmod(remainder1, 60)
        seconds, remainder3 = divmod(remainder2, 1)
        print("   Enrich Lines Complete...")
        print(f"     Enrichment Lines script took: {int(hours)}h, {int(minutes)}m, {seconds}s to complete")

        return Line_Enriched_Final

