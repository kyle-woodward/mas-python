# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2022-11-29 12:15:24
"""
import arcpy
from _1b_add_fields import AddFields2
from _2b_assign_domains import AssignDomains
from _7b_enrichments_pts import bEnrichmentsPoints
from _7c_enrichments_lines import cEnrichmentsLines
from sys import argv
from utils import init_gdb, runner

original_gdb, workspace, scratch_workspace = init_gdb()

def CalTrans(CalTrans_act_ln_standardized_20220712b="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\c_Standardized\\CalTrans_act_ln_standardized_20220712b", CalTrans_act_pts_standardized_20220712b="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\c_Standardized\\CalTrans_act_pts_standardized_20220712b", CalTrans_act_pts_enriched_20220712="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\d_Enriched\\CalTrans_act_pts_enriched_20220712", CalTrans_act_ln_enriched_20220712="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\d_Enriched\\CalTrans_act_ln_enriched_20220712"):  # 6m CalTrans_Activities 20221123

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")
    Vegetation_Control_FY2022_Statewide_Point_Activities_2_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\1-Spatial Data\\CalTrans\\Vegetation_Control_FY2021_2022.gdb\\Vegetation_Control_FY2022_Statewide_Point_Activities"
    Vegetation_Control_FY2022_Statewide_Polyline_Activities = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\a_Originals\\Vegetation_Control_FY2022_Statewide_Polyline_Activities"

    # Process: Feature To Point (Feature To Point) (management)
    Output_Feature_Class = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Vegetation_Con_FeatureToPoin"
    arcpy.management.FeatureToPoint(in_features=Vegetation_Control_FY2022_Statewide_Point_Activities_2_, out_feature_class=Output_Feature_Class, point_location="CENTROID")

    # Process: Alter Field County (Alter Field) (management)
    Updated_Input_Table_2_ = arcpy.management.AlterField(in_table=Output_Feature_Class, field="County", new_field_name="County_", new_field_alias="", field_type="", field_length=25, field_is_nullable="NON_NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Alter Field Activity Description (Alter Field) (management)
    Updated_Input_Table_4_ = arcpy.management.AlterField(in_table=Updated_Input_Table_2_, field="Activity_Description", new_field_name="Activity_Description_", new_field_alias="", field_type="", field_length=70, field_is_nullable="NON_NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Alter Field Veg (Alter Field) (management)
    CalTrans_pts_Copy_2_ = arcpy.management.AlterField(in_table=Updated_Input_Table_4_, field="Broad_Vegetation_Type", new_field_name="BVT", new_field_alias="", field_type="", field_length=50, field_is_nullable="NON_NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Alter Field Activity Status (Alter Field) (management)
    Updated_Input_Table_18_ = arcpy.management.AlterField(in_table=CalTrans_pts_Copy_2_, field="Activity_Status", new_field_name="Act_Status", new_field_alias="", field_type="", field_length=25, field_is_nullable="NON_NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Alter Activity Quantity (Alter Field) (management)
    Updated_Input_Table_9_ = arcpy.management.AlterField(in_table=Updated_Input_Table_18_, field="Activity_Quantity", new_field_name="Production_Quantity", new_field_alias="", field_type="", field_length=8, field_is_nullable="NON_NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Alter Field Residue Fate (Alter Field) (management)
    CalTrans_pts_Copy_3_ = arcpy.management.AlterField(in_table=Updated_Input_Table_9_, field="Residue_Fate", new_field_name="Fate", new_field_alias="", field_type="", field_length=35, field_is_nullable="NON_NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Alter Field Fate Units (Alter Field) (management)
    Updated_Input_Table_19_ = arcpy.management.AlterField(in_table=CalTrans_pts_Copy_3_, field="Residue_Fate_Units", new_field_name="FateUnits", new_field_alias="", field_type="", field_length=5, field_is_nullable="NON_NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Alter Residue Quantity (Alter Field) (management)
    CalTrans_pts_Copy_4_ = arcpy.management.AlterField(in_table=Updated_Input_Table_19_, field="Residue_Fate_Quantity", new_field_name="FateQuantity", new_field_alias="", field_type="", field_length=8, field_is_nullable="NON_NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: 1b Add Fields (1b Add Fields) (PC414CWIMillionAcres)
    WFRTF_Template_4_ = AddFields2(Input_Table=CalTrans_pts_Copy_4_)[0]

    # Process: Calculate Project ID (Calculate Field) (management)
    Updated_Input_Table_8_ = arcpy.management.CalculateField(in_table=WFRTF_Template_4_, field="PROJECTID_USER", expression="!HighwayID!", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Agency (Calculate Field) (management)
    Updated_Input_Table_3_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_8_, field="AGENCY", expression="\"CALSTA\"", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Admin Org (4) (Calculate Field) (management)
    Updated_Input_Table_5_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_3_, field="ORG_ADMIN_p", expression="!District!", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Project Contact (Calculate Field) (management)
    Updated_Input_Table_7_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_5_, field="PROJECT_CONTACT", expression="\"Division of Maintenance\"", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Email (Calculate Field) (management)
    Updated_Input_Table = arcpy.management.CalculateField(in_table=Updated_Input_Table_7_, field="PROJECT_EMAIL", expression="\"andrew.lozano@dot.ca.gov\"", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Admin Org (Calculate Field) (management)
    CalTrans_pts_Copy_5_ = arcpy.management.CalculateField(in_table=Updated_Input_Table, field="ADMINISTERING_ORG", expression="\"CALTRANS\"", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Primary Funding Source (Calculate Field) (management)
    Updated_Input_Table_6_ = arcpy.management.CalculateField(in_table=CalTrans_pts_Copy_5_, field="PRIMARY_FUNDING_SOURCE", expression="\"OTHER_STATE_FUNDS\"", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Primary Funding Org (Calculate Field) (management)
    Updated_Input_Table_10_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_6_, field="PRIMARY_FUNDING_ORG", expression="\"GENERAL_FUND\"", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Treatment ID (Calculate Field) (management)
    Updated_Input_Table_45_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_10_, field="TRMTID_USER", expression="!IMMS_ID!+'-'+!COUNTY![:5]+'-'+!REGION![:3]+'-'+!IN_WUI![:3]", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate WUI (Calculate Field) (management)
    Updated_Input_Table_11_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_45_, field="IN_WUI", expression="ifelse(!WUI!)", expression_type="PYTHON3", code_block="""def ifelse(WUI):
    if WUI == \"Yes\":
        return \"WUI_USER_DEFINED\"
    elif WUI == \"No\":
        return \"NON-WUI_USER_DEFINED\"
    else:
        return WUI""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Treatment Area (Calculate Field) (management)
    Updated_Input_Table_21_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_11_, field="TREATMENT_AREA", expression="ifelse(!Activity_Unit_of_Measure!, !Production_Quantity!)", expression_type="PYTHON3", code_block="""def ifelse(UOM, Q):
    if UOM == \"ACRE\":
        return Q
    else:
        return None""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Activity ID (Calculate Field) (management)
    Vegetation_Con_FeatureToPoin = arcpy.management.CalculateField(in_table=Updated_Input_Table_21_, field="ACTIVID_USER", expression="!Work_Order_Number!", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Implementing Org (Calculate Field) (management)
    Updated_Input_Table_20_ = arcpy.management.CalculateField(in_table=Vegetation_Con_FeatureToPoin, field="IMPLEMENTING_ORG", expression="!IMMS_Unit_ID!", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Activity UOM (Calculate Field) (management)
    Updated_Input_Table_12_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_20_, field="ACTIVITY_UOM", expression="!Activity_Unit_of_Measure!", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Activity Quantity (Calculate Field) (management)
    Updated_Input_Table_13_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_12_, field="ACTIVITY_QUANTITY", expression="!Production_Quantity!", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Status (Calculate Field) (management)
    Updated_Input_Table_15_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_13_, field="ACTIVITY_STATUS", expression="ifelse(!Act_Status!)", expression_type="PYTHON3", code_block="""def ifelse(Status):
    if Status == \"Complete\":
        return \"COMPLETE\"
    else:
        return Status""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Activity End (Calculate Field) (management)
    Updated_Input_Table_22_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_15_, field="ACTIVITY_END", expression="\"6/30/2022\"", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Source (Calculate Field) (management)
    Updated_Input_Table_16_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_22_, field="Source", expression="\"CALTRANS\"", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Crosswalk (Calculate Field) (management)
    Updated_Input_Table_17_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_16_, field="Crosswalk", expression="!Activity_Description_!", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Geometry Attributes (Calculate Geometry Attributes) (management)
    CalTrans_pts_Copy_7_ = arcpy.management.CalculateGeometryAttributes(in_features=Updated_Input_Table_17_, geometry_property=[["LATITUDE", "POINT_Y"], ["LONGITUDE", "POINT_X"]], length_unit="", area_unit="", coordinate_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", coordinate_format="DD")[0]

    # Process: Delete Field (3) (Delete Field) (management)
    CalTrans_pts_Copy_16_ = arcpy.management.DeleteField(in_table=CalTrans_pts_Copy_7_, drop_field=["PROJECTID_USER", "AGENCY", "ORG_ADMIN_p", "PROJECT_CONTACT", "PROJECT_EMAIL", "ADMINISTERING_ORG", "PROJECT_NAME", "PROJECT_STATUS", "PROJECT_START", "PROJECT_END", "PRIMARY_FUNDING_SOURCE", "PRIMARY_FUNDING_ORG", "IMPLEMENTING_ORG", "LATITUDE", "LONGITUDE", "BatchID_p", "Val_Status_p", "Val_Message_p", "Val_RunDate_p", "Review_Status_p", "Review_Message_p", "Review_RunDate_p", "Dataload_Status_p", "Dataload_Msg_p", "TRMTID_USER", "PROJECTID", "PROJECTNAME_", "ORG_ADMIN_t", "PRIMARY_OWNERSHIP_GROUP", "PRIMARY_OBJECTIVE", "SECONDARY_OBJECTIVE", "TERTIARY_OBJECTIVE", "TREATMENT_STATUS", "COUNTY", "IN_WUI", "REGION", "TREATMENT_AREA", "TREATMENT_START", "TREATMENT_END", "RETREATMENT_DATE_EST", "TREATMENT_NAME", "BatchID", "Val_Status_t", "Val_Message_t", "Val_RunDate_t", "Review_Status_t", "Review_Message_t", "Review_RunDate_t", "Dataload_Status_t", "Dataload_Msg_t", "ACTIVID_USER", "TREATMENTID_", "ORG_ADMIN_a", "ACTIVITY_DESCRIPTION", "ACTIVITY_CAT", "BROAD_VEGETATION_TYPE", "BVT_USERD", "ACTIVITY_STATUS", "ACTIVITY_QUANTITY", "ACTIVITY_UOM", "ACTIVITY_START", "ACTIVITY_END", "ADMIN_ORG_NAME", "IMPLEM_ORG_NAME", "PRIMARY_FUND_SRC_NAME", "PRIMARY_FUND_ORG_NAME", "SECONDARY_FUND_SRC_NAME", "SECONDARY_FUND_ORG_NAME", "TERTIARY_FUND_SRC_NAME", "TERTIARY_FUND_ORG_NAME", "ACTIVITY_PRCT", "RESIDUE_FATE", "RESIDUE_FATE_QUANTITY", "RESIDUE_FATE_UNITS", "ACTIVITY_NAME", "VAL_STATUS_a", "VAL_MSG_a", "VAL_RUNDATE_a", "REVIEW_STATUS_a", "REVIEW_MSG_a", "REVIEW_RUNDATE_a", "DATALOAD_STATUS_a", "DATALOAD_MSG_a", "Source", "Year", "Year_txt", "Act_Code", "Crosswalk", "Federal_FY", "State_FY"], method="KEEP_FIELDS")[0]

    # Process: Copy Features (Copy Features) (management)
    arcpy.management.CopyFeatures(in_features=CalTrans_pts_Copy_16_, out_feature_class=CalTrans_act_pts_standardized_20220712b, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)

    # Process: 2b Assign Domains (2b Assign Domains) (PC414CWIMillionAcres)
    usfs_silviculture_reforestation_enriched_20220629_2_ = AssignDomains(WFR_TF_Template=CalTrans_act_pts_standardized_20220712b)[0]

    # Process: 7b Enrichments pts (7b Enrichments pts) (PC414CWIMillionAcres)
    Pts_enrichment_Veg2 = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\Pts_enrichment_Veg2"
    bEnrichmentsPoints(Pts_enrichment_Veg2=Pts_enrichment_Veg2, nfpors_fuels_treatments_pts_standardized_20221110=usfs_silviculture_reforestation_enriched_20220629_2_)

    # Process: Copy Features (5) (Copy Features) (management)
    arcpy.management.CopyFeatures(in_features=Pts_enrichment_Veg2, out_feature_class=CalTrans_act_pts_enriched_20220712, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)

    # Process: Calculate Owner State (Calculate Field) (management)
    Updated_Input_Table_23_ = arcpy.management.CalculateField(in_table=CalTrans_act_pts_enriched_20220712, field="PRIMARY_OWNERSHIP_GROUP", expression="\"STATE\"", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: 2b Assign Domains (2) (2b Assign Domains) (PC414CWIMillionAcres)
    CalTrans_Activity_Points = AssignDomains(WFR_TF_Template=Updated_Input_Table_23_)[0]

    # Process: Copy Features (2) (Copy Features) (management)
    CalTrans_pts_Copy_8_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CalTrans_pts_Copy"
    arcpy.management.CopyFeatures(in_features=Vegetation_Control_FY2022_Statewide_Polyline_Activities, out_feature_class=CalTrans_pts_Copy_8_, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)

    # Process: Repair Geometry (Repair Geometry) (management)
    CalTrans_pts_Copy_13_ = arcpy.management.RepairGeometry(in_features=CalTrans_pts_Copy_8_, delete_null="KEEP_NULL", validation_method="ESRI")[0]

    # Process: Alter Field County (2) (Alter Field) (management)
    Updated_Input_Table_14_ = arcpy.management.AlterField(in_table=CalTrans_pts_Copy_13_, field="County", new_field_name="County2", new_field_alias="County2", field_type="TEXT", field_length=25, field_is_nullable="NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Alter Field Activity Description (2) (Alter Field) (management)
    Updated_Input_Table_24_ = arcpy.management.AlterField(in_table=Updated_Input_Table_14_, field="Activity_Description", new_field_name="Activity_Description_", new_field_alias="", field_type="TEXT", field_length=70, field_is_nullable="NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Alter Field Veg (2) (Alter Field) (management)
    CalTrans_pts_Copy_9_ = arcpy.management.AlterField(in_table=Updated_Input_Table_24_, field="Broad_Vegetation_Type", new_field_name="BVT", new_field_alias="", field_type="TEXT", field_length=50, field_is_nullable="NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Alter Field Activity Status (2) (Alter Field) (management)
    Updated_Input_Table_25_ = arcpy.management.AlterField(in_table=CalTrans_pts_Copy_9_, field="Activity_Status", new_field_name="Act_Status", new_field_alias="", field_type="TEXT", field_length=25, field_is_nullable="NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Alter Activity Quantity (2) (Alter Field) (management)
    Updated_Input_Table_26_ = arcpy.management.AlterField(in_table=Updated_Input_Table_25_, field="Activity_Quantity", new_field_name="Production_Quantity", new_field_alias="", field_type="DOUBLE", field_length=8, field_is_nullable="NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Alter Field Residue Fate (2) (Alter Field) (management)
    CalTrans_pts_Copy_10_ = arcpy.management.AlterField(in_table=Updated_Input_Table_26_, field="Residue_Fate", new_field_name="Fate", new_field_alias="", field_type="TEXT", field_length=35, field_is_nullable="NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Alter Field Fate Units (2) (Alter Field) (management)
    Updated_Input_Table_27_ = arcpy.management.AlterField(in_table=CalTrans_pts_Copy_10_, field="Residue_Fate_Units", new_field_name="FateUnits", new_field_alias="", field_type="TEXT", field_length=5, field_is_nullable="NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Alter Residue Quantity (2) (Alter Field) (management)
    CalTrans_pts_Copy_11_ = arcpy.management.AlterField(in_table=Updated_Input_Table_27_, field="Residue_Fate_Quantity", new_field_name="FateQuantity", new_field_alias="", field_type="DOUBLE", field_length=8, field_is_nullable="NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: 1b Add Fields (2) (1b Add Fields) (PC414CWIMillionAcres)
    WFRTF_Template_2_ = AddFields2(Input_Table=CalTrans_pts_Copy_11_)[0]

    # Process: Calculate Project ID (2) (Calculate Field) (management)
    Updated_Input_Table_28_ = arcpy.management.CalculateField(in_table=WFRTF_Template_2_, field="PROJECTID_USER", expression="!HighwayID!", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Agency (2) (Calculate Field) (management)
    Updated_Input_Table_29_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_28_, field="AGENCY", expression="\"CALSTA\"", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Admin Org (5) (Calculate Field) (management)
    Updated_Input_Table_30_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_29_, field="ORG_ADMIN_p", expression="!District!", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Project Contact (2) (Calculate Field) (management)
    Updated_Input_Table_31_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_30_, field="PROJECT_CONTACT", expression="\"Division of Maintenance\"", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Email (2) (Calculate Field) (management)
    Updated_Input_Table_32_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_31_, field="PROJECT_EMAIL", expression="\"andrew.lozano@dot.ca.gov\"", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Admin Org (2) (Calculate Field) (management)
    CalTrans_pts_Copy_12_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_32_, field="ADMINISTERING_ORG", expression="\"CALTRANS\"", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Primary Funding Source (2) (Calculate Field) (management)
    Updated_Input_Table_33_ = arcpy.management.CalculateField(in_table=CalTrans_pts_Copy_12_, field="PRIMARY_FUNDING_SOURCE", expression="\"OTHER_STATE_FUNDS\"", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Primary Funding Org (2) (Calculate Field) (management)
    Updated_Input_Table_34_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_33_, field="PRIMARY_FUNDING_ORG", expression="\"CALTRANS\"", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Treatment ID (2) (Calculate Field) (management)
    Updated_Input_Table_46_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_34_, field="TRMTID_USER", expression="!IMMS_ID!+'-'+!COUNTY![:5]+'-'+!REGION![:3]+'-'+!IN_WUI![:3]", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate WUI (2) (Calculate Field) (management)
    Updated_Input_Table_36_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_46_, field="IN_WUI", expression="ifelse(!WUI!)", expression_type="PYTHON3", code_block="""def ifelse(WUI):
    if WUI == \"Yes\":
        return \"WUI_USER_DEFINED\"
    elif WUI == \"No\":
        return \"NON-WUI_USER_DEFINED\"
    else:
        return WUI""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Treatment Area (2) (Calculate Field) (management)
    Updated_Input_Table_37_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_36_, field="TREATMENT_AREA", expression="ifelse(!Activity_Unit_of_Measure!, !Production_Quantity!)", expression_type="PYTHON3", code_block="""def ifelse(UOM, Q):
    if UOM == \"ACRE\":
        return Q
    else:
        return None""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Activity ID (2) (Calculate Field) (management)
    Vegetation_Con_FeatureToPoin_2_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_37_, field="ACTIVID_USER", expression="!Work_Order_Number!", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Implementing Org (2) (Calculate Field) (management)
    Updated_Input_Table_35_ = arcpy.management.CalculateField(in_table=Vegetation_Con_FeatureToPoin_2_, field="IMPLEMENTING_ORG", expression="!IMMS_ID!", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Activity UOM (2) (Calculate Field) (management)
    Updated_Input_Table_38_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_35_, field="ACTIVITY_UOM", expression="!Activity_Unit_of_Measure!", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Activity Quantity (2) (Calculate Field) (management)
    Updated_Input_Table_39_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_38_, field="ACTIVITY_QUANTITY", expression="!Production_Quantity!", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Status (2) (Calculate Field) (management)
    Updated_Input_Table_40_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_39_, field="ACTIVITY_STATUS", expression="ifelse(!Act_Status!)", expression_type="PYTHON3", code_block="""def ifelse(Status):
    if Status == \"Complete\":
        return \"COMPLETE\"
    else:
        return Status""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Activity End (2) (Calculate Field) (management)
    Updated_Input_Table_41_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_40_, field="ACTIVITY_END", expression="\"6/30/2022\"", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Source (2) (Calculate Field) (management)
    Updated_Input_Table_42_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_41_, field="Source", expression="\"CALTRANS\"", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Crosswalk (2) (Calculate Field) (management)
    Updated_Input_Table_43_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_42_, field="Crosswalk", expression="!Activity_Description_!", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Geometry Attributes (2) (Calculate Geometry Attributes) (management)
    CalTrans_pts_Copy_15_ = arcpy.management.CalculateGeometryAttributes(in_features=Updated_Input_Table_43_, geometry_property=[["LATITUDE", "INSIDE_Y"], ["LONGITUDE", "INSIDE_X"]], length_unit="", area_unit="", coordinate_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", coordinate_format="DD")[0]

    # Process: Delete Field (2) (Delete Field) (management)
    CalTrans_pts_Copy_14_ = arcpy.management.DeleteField(in_table=CalTrans_pts_Copy_15_, drop_field=["PROJECTID_USER", "AGENCY", "ORG_ADMIN_p", "PROJECT_CONTACT", "PROJECT_EMAIL", "ADMINISTERING_ORG", "PROJECT_NAME", "PROJECT_STATUS", "PROJECT_START", "PROJECT_END", "PRIMARY_FUNDING_SOURCE", "PRIMARY_FUNDING_ORG", "IMPLEMENTING_ORG", "LATITUDE", "LONGITUDE", "BatchID_p", "Val_Status_p", "Val_Message_p", "Val_RunDate_p", "Review_Status_p", "Review_Message_p", "Review_RunDate_p", "Dataload_Status_p", "Dataload_Msg_p", "TRMTID_USER", "PROJECTID", "PROJECTNAME_", "ORG_ADMIN_t", "PRIMARY_OWNERSHIP_GROUP", "PRIMARY_OBJECTIVE", "SECONDARY_OBJECTIVE", "TERTIARY_OBJECTIVE", "TREATMENT_STATUS", "COUNTY", "IN_WUI", "REGION", "TREATMENT_AREA", "TREATMENT_START", "TREATMENT_END", "RETREATMENT_DATE_EST", "TREATMENT_NAME", "BatchID", "Val_Status_t", "Val_Message_t", "Val_RunDate_t", "Review_Status_t", "Review_Message_t", "Review_RunDate_t", "Dataload_Status_t", "Dataload_Msg_t", "ACTIVID_USER", "TREATMENTID_", "ORG_ADMIN_a", "ACTIVITY_DESCRIPTION", "ACTIVITY_CAT", "BROAD_VEGETATION_TYPE", "BVT_USERD", "ACTIVITY_STATUS", "ACTIVITY_QUANTITY", "ACTIVITY_UOM", "ACTIVITY_START", "ACTIVITY_END", "ADMIN_ORG_NAME", "IMPLEM_ORG_NAME", "PRIMARY_FUND_SRC_NAME", "PRIMARY_FUND_ORG_NAME", "SECONDARY_FUND_SRC_NAME", "SECONDARY_FUND_ORG_NAME", "TERTIARY_FUND_SRC_NAME", "TERTIARY_FUND_ORG_NAME", "ACTIVITY_PRCT", "RESIDUE_FATE", "RESIDUE_FATE_QUANTITY", "RESIDUE_FATE_UNITS", "ACTIVITY_NAME", "VAL_STATUS_a", "VAL_MSG_a", "VAL_RUNDATE_a", "REVIEW_STATUS_a", "REVIEW_MSG_a", "REVIEW_RUNDATE_a", "DATALOAD_STATUS_a", "DATALOAD_MSG_a", "Source", "Year", "Year_txt", "Act_Code", "Crosswalk", "Federal_FY", "State_FY"], method="KEEP_FIELDS")[0]

    # Process: Copy Features (3) (Copy Features) (management)
    arcpy.management.CopyFeatures(in_features=CalTrans_pts_Copy_14_, out_feature_class=CalTrans_act_ln_standardized_20220712b, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)

    # Process: 2b Assign Domains (3) (2b Assign Domains) (PC414CWIMillionAcres)
    usfs_silviculture_reforestation_enriched_20220629_3_ = AssignDomains(WFR_TF_Template=CalTrans_act_ln_standardized_20220712b)[0]

    # Process: 7c Enrichments Lines (2) (7c Enrichments Lines) (PC414CWIMillionAcres)
    Line_Enriched_Temp_CopyFeatures_3_ = cEnrichmentsLines(CM_CNRAExtract_TrtLn_standardized_20221110=usfs_silviculture_reforestation_enriched_20220629_3_)[0]

    # Process: Copy Features (4) (Copy Features) (management)
    arcpy.management.CopyFeatures(in_features=Line_Enriched_Temp_CopyFeatures_3_, out_feature_class=CalTrans_act_ln_enriched_20220712, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)

    # Process: Calculate Owner State (2) (Calculate Field) (management)
    Updated_Input_Table_44_ = arcpy.management.CalculateField(in_table=CalTrans_act_ln_enriched_20220712, field="PRIMARY_OWNERSHIP_GROUP", expression="\"STATE\"", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: 2b Assign Domains (4) (2b Assign Domains) (PC414CWIMillionAcres)
    CalTrans_Activity_Points_2_ = AssignDomains(WFR_TF_Template=Updated_Input_Table_44_)[0]

if __name__ == '__main__':
    # Global Environment settings
     with arcpy.EnvManager(
    extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""",  outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""", 
    preserveGlobalIds=True, 
    qualifiedFieldNames=False, 
    scratchWorkspace=scratch_workspace, 
    transferDomains=True, 
    transferGDBAttributeProperties=True, 
    workspace=workspace):
        CalTrans(*argv[1:])
