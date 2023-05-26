"""
"""
import arcpy
from scripts._1b_add_fields import AddFields2
from scripts._2b_assign_domains import AssignDomains
from scripts._7a_enrichments_polygon import aEnrichmentsPolygon1
from scripts.utils import runner, init_gdb
from sys import argv
import os
import datetime
original_gdb, workspace, scratch_workspace = init_gdb()

def WCB(WCB_standardized, WCB_OG):  # 6u WCB 20221226

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False
    date_id = datetime.datetime.utcnow().strftime("%Y-%m-%d").replace('-','')

    # scratch outputs
    WCB_CopyFeatures = os.path.join(scratch_workspace, 'WCB_CopyFeatures')
    WCB_Dissolve = os.path.join(scratch_workspace, 'WCB_Dissolve') 
    WCB_enriched_scratch = os.path.join(scratch_workspace, 'WCB_enriched_scratch') 

    # workspace outputs
    WCB_enriched = os.path.join(workspace, 'd_Enriched', f'WCB_enriched_{date_id}') 

    # Model Environment settings
    with arcpy.EnvManager(unionDimension=False):

        # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
        WCB_select = arcpy.management.SelectLayerByAttribute(in_layer_or_view=WCB_OG, 
                                                                             where_clause="Function = 'Disposal/Sale' Or Function = 'Other (Plan, Study, Etc.)' Or Function = 'Infrastructure' Or Function = 'Lease' Or Function = 'Public Access' Or Function = 'Transfer of Control'", 
                                                                             invert_where_clause="INVERT")

        # Process: Select Layer By Attribute (2) (Select Layer By Attribute) (management)
        WCB_select_2 = arcpy.management.SelectLayerByAttribute(in_layer_or_view=WCB_select, 
                                                                                  selection_type="SUBSET_SELECTION", 
                                                                                  where_clause="dtmBoardAp >= timestamp '1995-01-01 00:00:00'")

        # Process: Copy Features (2) (Copy Features) (management)
        arcpy.management.CopyFeatures(in_features=WCB_select_2, 
                                      out_feature_class=WCB_CopyFeatures)

        # Process: Dissolve (Dissolve) (management)
        arcpy.management.Dissolve(in_features=WCB_CopyFeatures, 
                                  out_feature_class=WCB_Dissolve, 
                                  dissolve_field=["County", 
                                                  "dtmBoardAp", 
                                                  "Function", 
                                                  "PrimGrante", 
                                                  "PrimPurp", 
                                                  "Program", 
                                                  "ProjectID", 
                                                  "ProjName", 
                                                  "TotalAcres", 
                                                  "Type", 
                                                  "WCBFunding"])

        # Process: Repair Geometry (Repair Geometry) (management)
        WCB_Dissolve_repair_geom = arcpy.management.RepairGeometry(in_features=WCB_Dissolve, 
                                                                delete_null="KEEP_NULL")

        # Process: Alter Field (Alter Field) (management)
        WCB_Dissolve_alter_field = arcpy.management.AlterField(in_table=WCB_Dissolve_repair_geom, 
                                                               field="ProjectID", 
                                                               new_field_name="ProjectID2")

        # Process: Alter Field (2) (Alter Field) (management)
        WCB_Dissolve_alter_field_2 = arcpy.management.AlterField(in_table=WCB_Dissolve_alter_field, 
                                                               field="County", 
                                                               new_field_name="County_")

        # Process: 1b Add Fields (1b Add Fields) (PC414CWIMillionAcres)
        WCB_add_fields = AddFields2(Input_Table=WCB_Dissolve_alter_field_2)

        # Process: Calculate Project ID User (Calculate Field) (management)
        WCB_calc_proj_id_user = arcpy.management.CalculateField(in_table=WCB_add_fields, 
                                                              field="PROJECTID_USER", 
                                                              expression="!ProjectID2!")

        # Process: Calculate Treatment ID User (Calculate Field) (management)
        WCB_calc_treat_id_user = arcpy.management.CalculateField(in_table=WCB_calc_proj_id_user, 
                                                                                   field="TRMTID_USER", 
                                                                                   expression="!PROJECTID_USER!+'-'+!PRIMARY_OWNERSHIP_GROUP![:4]+'-'+!IN_WUI![:3]")

        # Process: Calculate Agency (Calculate Field) (management)
        WCB_calc_agency = arcpy.management.CalculateField(in_table=WCB_calc_treat_id_user,
                                                                  field="AGENCY", 
                                                                  expression="\"CNRA\"")

        # Process: Calculate Project Contact (Calculate Field) (management)
        WCB_calc_proj_contact = arcpy.management.CalculateField(in_table=WCB_calc_agency, 
                                                                  field="PROJECT_CONTACT", 
                                                                  expression="\"Scott McFarlin\"")

        # Process: Calculate Project Email (Calculate Field) (management)
        WCB_calc_proj_email = arcpy.management.CalculateField(in_table=WCB_calc_proj_contact, 
                                                                  field="PROJECT_EMAIL", 
                                                                  expression="\"Scott.McFarlin@wildlife.ca.gov\"")

        # Process: Calculate Admin Org (Calculate Field) (management)
        WCB_calc_admin_org = arcpy.management.CalculateField(in_table=WCB_calc_proj_email, 
                                                                  field="ADMINISTERING_ORG", 
                                                                  expression="\"WCB\"")

        # Process: Calculate Project Name (Calculate Field) (management)
        WCB_calc_proj_name = arcpy.management.CalculateField(in_table=WCB_calc_admin_org, 
                                                                 field="PROJECT_NAME", 
                                                                 expression="!ProjName!")

        # Process: Calculate Project Start (Calculate Field) (management)
        WCB_calc_proj_start = arcpy.management.CalculateField(in_table=WCB_calc_proj_name, 
                                                                 field="PROJECT_START", 
                                                                 expression="!dtmBoardAp!")

        # Process: Calculate Primary Objective (Calculate Field) (management)
        WCB_calc_prim_obj = arcpy.management.CalculateField(in_table=WCB_calc_proj_start, 
                                                                 field="PRIMARY_OBJECTIVE", 
                                                                 expression="!PrimPurp!")[0]

        # Process: Calculate Secondary Objective (Calculate Field) (management)
        WCB_calc_sec_obj = arcpy.management.CalculateField(in_table=WCB_calc_prim_obj, 
                                                                 field="SECONDARY_OBJECTIVE", 
                                                                 expression="!Type!")[0]

        # Process: Calculate Tertiary Objective (Calculate Field) (management)
        WCB_calc_tert_obj = arcpy.management.CalculateField(in_table=WCB_calc_sec_obj, 
                                                                 field="TERTIARY_OBJECTIVE", 
                                                                 expression="!Function!", 
                                                                 enforce_domains="NO_ENFORCE_DOMAINS")[0]

        # Process: Calculate Primary Funding Source (Calculate Field) (management)
        WCB_calc_prim_fund_src = arcpy.management.CalculateField(in_table=WCB_calc_tert_obj, 
                                                                 field="PRIMARY_FUNDING_SOURCE", 
                                                                 expression="!Program!", 
                                                                 enforce_domains="NO_ENFORCE_DOMAINS")[0]

        # Process: Calculate Activity Acres (Calculate Field) (management)
        WCB_calc_act_ac = arcpy.management.CalculateField(in_table=WCB_calc_prim_fund_src, 
                                                                 field="ACTIVITY_QUANTITY", 
                                                                 expression="!TotalAcres!")[0]

        # Process: Calculate UOM (Calculate Field) (management)
        WCB_calc_uom = arcpy.management.CalculateField(in_table=WCB_calc_act_ac, 
                                                                  field="ACTIVITY_UOM", 
                                                                  expression="\"AC\"")[0]

        # Process: Calculate Activity End Date (Calculate Field) (management)
        WCB_calc_act_end_date = arcpy.management.CalculateField(in_table=WCB_calc_uom, 
                                                                  field="ACTIVITY_END", 
                                                                  expression="!dtmBoardAp!")[0]

        # Process: Calculate Activity Status (Calculate Field) (management)
        WCB_calc_act_stat = arcpy.management.CalculateField(in_table=WCB_calc_act_end_date, 
                                                                   field="ACTIVITY_STATUS", 
                                                                   expression="\"ACTIVE\"")[0]

        # Process: Calculate Implementing Org (Calculate Field) (management)
        WCB_calc_imp_org = arcpy.management.CalculateField(in_table=WCB_calc_act_stat, 
                                                                 field="IMPLEM_ORG_NAME", 
                                                                 expression="!PrimGrante!")[0]

        # Process: Calculate Source (Calculate Field) (management)
        WCB_calc_src = arcpy.management.CalculateField(in_table=WCB_calc_imp_org, 
                                                            field="Source", 
                                                            expression="\"WCB\"")[0]

        # Process: Calculate Crosswalk (Calculate Field) (management)
        WCB_calc_xwalk = arcpy.management.CalculateField(in_table=WCB_calc_src, 
                                                                  field="Crosswalk", 
                                                                  expression="!Function! + \" \" + !PrimPurp!")[0]

        # Process: Calculate Year (Calculate Field) (management)
        WCB_calc_year = arcpy.management.CalculateField(in_table=WCB_calc_xwalk, 
                                                                  field="Year", 
                                                                  expression="Year($feature.dtmBoardAp)", 
                                                                  expression_type="ARCADE")[0]

        # Process: Copy Features (Copy Features) (management)
        arcpy.management.CopyFeatures(in_features=WCB_calc_year, 
                                      out_feature_class=WCB_standardized.__str__().format(**locals(),**globals()))

        # Process: Delete Field (Delete Field) (management)
        WCB_standardized_keep_fields = arcpy.management.DeleteField(in_table=WCB_standardized.__str__().format(**locals(),**globals()), 
                                                                    drop_field=["PROJECTID_USER", 
                                                                                "AGENCY", 
                                                                                "ORG_ADMIN_p", 
                                                                                "PROJECT_CONTACT", 
                                                                                "PROJECT_EMAIL", 
                                                                                "ADMINISTERING_ORG", 
                                                                                "PROJECT_NAME", 
                                                                                "PROJECT_STATUS", 
                                                                                "PROJECT_START", 
                                                                                "PROJECT_END", 
                                                                                "PRIMARY_FUNDING_SOURCE", 
                                                                                "PRIMARY_FUNDING_ORG", 
                                                                                "IMPLEMENTING_ORG", 
                                                                                "LATITUDE", 
                                                                                "LONGITUDE", 
                                                                                "BatchID_p", 
                                                                                "Val_Status_p", 
                                                                                "Val_Message_p", 
                                                                                "Val_RunDate_p", 
                                                                                "Review_Status_p", 
                                                                                "Review_Message_p", 
                                                                                "Review_RunDate_p", 
                                                                                "Dataload_Status_p", 
                                                                                "Dataload_Msg_p", 
                                                                                "TRMTID_USER", 
                                                                                "PROJECTID", 
                                                                                "PROJECTNAME_", 
                                                                                "ORG_ADMIN_t", 
                                                                                "PRIMARY_OWNERSHIP_GROUP", 
                                                                                "PRIMARY_OBJECTIVE", 
                                                                                "SECONDARY_OBJECTIVE", 
                                                                                "TERTIARY_OBJECTIVE", 
                                                                                "TREATMENT_STATUS", 
                                                                                "COUNTY", 
                                                                                "IN_WUI", 
                                                                                "REGION", 
                                                                                "TREATMENT_AREA", 
                                                                                "TREATMENT_START", 
                                                                                "TREATMENT_END", 
                                                                                "RETREATMENT_DATE_EST", 
                                                                                "TREATMENT_NAME", 
                                                                                "BatchID", 
                                                                                "Val_Status_t", 
                                                                                "Val_Message_t", 
                                                                                "Val_RunDate_t", 
                                                                                "Review_Status_t", 
                                                                                "Review_Message_t", 
                                                                                "Review_RunDate_t", 
                                                                                "Dataload_Status_t", 
                                                                                "Dataload_Msg_t", 
                                                                                "ACTIVID_USER", 
                                                                                "TREATMENTID_", 
                                                                                "ORG_ADMIN_a", 
                                                                                "ACTIVITY_DESCRIPTION", 
                                                                                "ACTIVITY_CAT", 
                                                                                "BROAD_VEGETATION_TYPE", 
                                                                                "BVT_USERD", 
                                                                                "ACTIVITY_STATUS", 
                                                                                "ACTIVITY_QUANTITY", 
                                                                                "ACTIVITY_UOM", 
                                                                                "ACTIVITY_START", 
                                                                                "ACTIVITY_END", 
                                                                                "ADMIN_ORG_NAME", 
                                                                                "IMPLEM_ORG_NAME", 
                                                                                "PRIMARY_FUND_SRC_NAME", 
                                                                                "PRIMARY_FUND_ORG_NAME", 
                                                                                "SECONDARY_FUND_SRC_NAME", 
                                                                                "SECONDARY_FUND_ORG_NAME", 
                                                                                "TERTIARY_FUND_SRC_NAME", 
                                                                                "TERTIARY_FUND_ORG_NAME", 
                                                                                "ACTIVITY_PRCT", 
                                                                                "RESIDUE_FATE", 
                                                                                "RESIDUE_FATE_QUANTITY", 
                                                                                "RESIDUE_FATE_UNITS", 
                                                                                "ACTIVITY_NAME", 
                                                                                "VAL_STATUS_a", 
                                                                                "VAL_MSG_a", 
                                                                                "VAL_RUNDATE_a", 
                                                                                "REVIEW_STATUS_a", 
                                                                                "REVIEW_MSG_a", 
                                                                                "REVIEW_RUNDATE_a", 
                                                                                "DATALOAD_STATUS_a", 
                                                                                "DATALOAD_MSG_a", 
                                                                                "Source", 
                                                                                "Year", 
                                                                                "Year_txt", 
                                                                                "Act_Code", 
                                                                                "Crosswalk", 
                                                                                "Federal_FY", 
                                                                                "State_FY"], 
                                                                            method="KEEP_FIELDS")[0]

        # Process: 2b Assign Domains (2b Assign Domains) (PC414CWIMillionAcres)
        WCB_w_domains = AssignDomains(in_table=WCB_standardized_keep_fields)[0]

        # Process: 7a Enrichments Polygon (7a Enrichments Polygon) (PC414CWIMillionAcres)
        aEnrichmentsPolygon1(enrich_out=WCB_enriched_scratch, 
                             enrich_in=WCB_w_domains)

        # Process: Select Layer By Attribute (3) (Select Layer By Attribute) (management)
        WCB_enriched_scratch_select = arcpy.management.SelectLayerByAttribute(in_layer_or_view=WCB_enriched_scratch, 
                                                                                         where_clause="ACTIVITY_DESCRIPTION <> 'NOT_DEFINED'")

        # Process: Copy Features (3) (Copy Features) (management)
        arcpy.management.CopyFeatures(in_features=WCB_enriched_scratch_select, 
                                      out_feature_class=WCB_enriched)

        # Process: 2b Assign Domains (2) (2b Assign Domains) (PC414CWIMillionAcres)
        WFR_TF_Template_4_ = AssignDomains(in_table=WCB_enriched)[0]

if __name__ == '__main__':
    runner(workspace,scratch_workspace,WCB, '*argv[1:]')
    # Global Environment settings
    # with arcpy.EnvManager(
    # extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""",  outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""", 
    # preserveGlobalIds=True, 
    # qualifiedFieldNames=False, 
    # scratchWorkspace=scratch_workspace, 
    # transferDomains=True, 
    # transferGDBAttributeProperties=True, 
    # workspace=workspace):
    #     WCB(*argv[1:])
