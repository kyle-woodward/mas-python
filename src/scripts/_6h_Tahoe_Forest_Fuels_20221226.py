"""
"""
import arcpy
from scripts._1b_add_fields import AddFields
from scripts._2b_assign_domains import AssignDomains
from scripts._7a_enrichments_polygon import enrich_polygons
from scripts.utils import runner, init_gdb
from sys import argv
import os
original_gdb, workspace, scratch_workspace = init_gdb()

def TahoeFF6(TahoeFF_Tx_enriched,
             TahoeFF_Tx_standardized,
             TahoeFF_Tx_OG): 

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    # scratch outputs
    TahoeFF_pairwiseclip = os.path.join(scratch_workspace, 'TahoeFF_pairwiseclip')
    TahoeFF_Tx_OG_Select = os.path.join(scratch_workspace, 'TahoeFF_Tx_OG_Select')
    CPAD_Ownership_StateParks = os.path.join(scratch_workspace, 'CPAD_Ownership_StateParks')
    TahoeFF_enriched_scratch = os.path.join(scratch_workspace, TahoeFF_enriched_scratch)

    # Model Environment settings
    with arcpy.EnvManager(extent="-415308.137838921 -608601.962396972 551888.996651875 458556.048364898 PROJCS[\"NAD_1983_California_Teale_Albers\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Albers\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",-4000000.0],PARAMETER[\"Central_Meridian\",-120.0],PARAMETER[\"Standard_Parallel_1\",34.0],PARAMETER[\"Standard_Parallel_2\",40.5],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]"):
        California = os.path.join(workspace, 'b_Reference', 'California')
        CPAD_Ownership_Update = os.path.join(workspace, 'b_Reference', 'CPAD_Ownership_Update')

        # Process: Pairwise Clip (Pairwise Clip) (analysis)

        arcpy.analysis.PairwiseClip(in_features=TahoeFF_Tx_OG, 
                                    clip_features=California, 
                                    out_feature_class=TahoeFF_pairwiseclip)

        # Process: Select no Fed or NV or Wildland Fire (Select) (analysis)

        arcpy.analysis.Select(in_features=TahoeFF_pairwiseclip, 
                              out_feature_class=TahoeFF_Tx_OG_Select, 
                              where_clause="CATEGORY <> 'Federal' And CATEGORY <> 'NV' And ACT <> 'Wildland Fire'")

        # Process: Repair Geometry (Repair Geometry) (management)
        TahoeFF_pairwiseclip = arcpy.management.RepairGeometry(in_features=TahoeFF_Tx_OG_Select, 
                                                                       delete_null="KEEP_NULL")

        # Process: Alter Field (Alter Field) (management)
        TahoeFF_alter_year = arcpy.management.AlterField(in_table=TahoeFF_pairwiseclip, 
                                                                             field="YEAR", 
                                                                             new_field_name="YEAR_", 
                                                                             new_field_alias="YEAR_")

        # Process: 1b Add Fields (2) (1b Add Fields) (PC414CWIMillionAcres)
        TahoeFF_add_fields = AddFields(Input_Table=TahoeFF_alter_year)

        # Process: Calculate Project ID (Calculate Field) (management)
        Tahoe_calc_proj_id = arcpy.management.CalculateField(in_table=TahoeFF_add_fields, 
                                                                 field="PROJECTID", 
                                                                 expression="None")

        # Process: Calculate Project ID Null (Calculate Field) (management)
        Tahoe_calc_proj_id_null = arcpy.management.CalculateField(in_table=Tahoe_calc_proj_id, 
                                                                 field="Project_ID", 
                                                                 expression="ifelse(!Project_ID!)", 
                                                                 code_block="""def ifelse(ID):
    if ID == '':
        return None
    if ID == ' ':
        return None
    return ID""")

        # Process: Calculate EIP Null (Calculate Field) (management)
        Tahoe_calc_eip_null = arcpy.management.CalculateField(in_table=Tahoe_calc_proj_id_null, 
                                                                  field="EIP_Number", 
                                                                  expression="ifelse(!EIP_Number!)", 
                                                                  code_block="""def ifelse(ID):
    if ID == '':
        return None
    elif ID == ' ':
        return None
    else:
        return ID""")

        # Process: Calculate PROJ Null (Calculate Field) (management)
        Tahoe_calc_proj_null = arcpy.management.CalculateField(in_table=Tahoe_calc_eip_null, 
                                                                  field="PROJ", 
                                                                  expression="ifelse(!PROJ!)", 
                                                                  code_block="""def ifelse(ID):
    if ID == '':
        return None
    return ID""")

        # Process: Calculate Year 0 (Calculate Field) (management)
        Tahoe_calc_year = arcpy.management.CalculateField(in_table=Tahoe_calc_proj_null, 
                                                                  field="YEAR_", 
                                                                  expression="ifelse(!YEAR_!)", 
                                                                  code_block="""def ifelse(ID):
    if ID == 0:
        return None
    return ID""")

        # Process: Calculate Own Full Null (Calculate Field) (management)
        Tahoe_calc_own_full_null = arcpy.management.CalculateField(in_table=Tahoe_calc_year, 
                                                                  field="OWN_FULL", 
                                                                  expression="ifelse(!OWN_FULL!)", 
                                                                  code_block="""def ifelse(ID):
    if ID == '':
        return None
    return ID""")

        # Process: Calculate Project ID User (Calculate Field) (management)
        Tahoe_calc_proj_id_user = arcpy.management.CalculateField(in_table=Tahoe_calc_own_full_null, 
                                                                  field="PROJECTID_USER", 
                                                                  expression="ifelse(!PROJECTID_USER!,!Project_ID!)", 
                                                                  code_block="""def ifelse(ID, ID2):
    if ID == None:
        return ID2
    else:
        return ID""")

        # Process: Calculate Project ID User (2) (Calculate Field) (management)
        Tahoe_calc_proj_id_user_2 = arcpy.management.CalculateField(in_table=Tahoe_calc_proj_id_user, 
                                                                  field="PROJECTID_USER", 
                                                                  expression="ifelse(!PROJECTID_USER!,!EIP_Number!)", 
                                                                  code_block="""def ifelse(ID, EIP):
    if ID == None:
        return EIP
    else:
        return ID""")

        # Process: Calculate Project ID User (3) (Calculate Field) (management)
        Tahoe_calc_proj_id_user_3 = arcpy.management.CalculateField(in_table=Tahoe_calc_proj_id_user_2, 
                                                                  field="PROJECTID_USER", 
                                                                  expression="ifelse(!PROJECTID_USER!,!PROJ!)", 
                                                                  code_block="""def ifelse(ID, Proj):
    if ID == None:
        return Proj
    else:
        return ID""")

        # Process: Calculate Project ID User (4) (Calculate Field) (management)
        Tahoe_calc_proj_id_user_4 = arcpy.management.CalculateField(in_table=Tahoe_calc_proj_id_user_3, 
                                                                  field="PROJECTID_USER", 
                                                                  expression="ifelse(!PROJECTID_USER!, !JURIS!)", 
                                                                  code_block="""def ifelse(ID, Jur):
    if ID == None:
        return Jur
    else:
        return ID""")

        # Process: Calculate Agency (Calculate Field) (management)
        Tahoe_calc_agency = arcpy.management.CalculateField(in_table=Tahoe_calc_proj_id_user_4, 
                                                                  field="AGENCY", 
                                                                  expression="Reclass(!JURIS!)", 
                                                                  code_block="""# Reclassify values to another value
# More calculator examples at esriurl.com/CalculatorExamples
def Reclass(JURIS):
    if JURIS == \"CA\":
        return \"CNRA\"
    elif JURIS == \"Liberty Utilities\":
        return \"OEIS\"
    return \"OTHER\"""")

        # Process: Calculate Administering Org (Calculate Field) (management)
        Tahoe_calc_admin_org = arcpy.management.CalculateField(in_table=Tahoe_calc_agency, 
                                                              field="ADMINISTERING_ORG", 
                                                              expression="!OWN_FULL!")

        # Process: Select (Select) (analysis) 
        arcpy.analysis.Select(in_features=CPAD_Ownership_Update, 
                              out_feature_class=CPAD_Ownership_StateParks, 
                              where_clause="AGNCY_NAME = 'California Department of Parks and Recreation'")

        # Process: Select Layer By State Parks Location (Select Layer By Location) (management)
        TahoeFF_select_SP = arcpy.management.SelectLayerByLocation(in_layer=Tahoe_calc_admin_org, 
                                                                                                         overlap_type="HAVE_THEIR_CENTER_IN", 
                                                                                                         select_features=CPAD_Ownership_StateParks, 
                                                                                                         search_distance="1 Meters")

        # Process: Calculate Admin Org Parks (Calculate Field) (management)
        TahoeFF_SP_calc_admin_org_parks = arcpy.management.CalculateField(in_table=TahoeFF_select_SP, 
                                                                          field="ADMINISTERING_ORG", 
                                                                          expression="\"PARKS\"")

        # Process: Clear Selection (Select Layer By Attribute) (management)
        TahoeFF_SP_clear_select = arcpy.management.SelectLayerByAttribute(in_layer_or_view=TahoeFF_SP_calc_admin_org_parks, 
                                                                                            selection_type="CLEAR_SELECTION")

        # Process: Calculate Project ID User (5) (Calculate Field) (management)
        TahoeFF_calc_proj_id_user = arcpy.management.CalculateField(in_table=TahoeFF_SP_clear_select, 
                                                                          field="PROJECTID_USER", 
                                                                          expression="ifelse(!AGENCY!, !PROJECTID_USER!)", 
                                                                          code_block="""def ifelse(Agency, ID):
    if Agency == \"PARKS\":
        return \"P_\"+ID
    elif Agency == \"TAHOE\":
        return \"T_\"+ID
    elif Agency == \"OTHER\":
        return \"R_\"+ID
    elif Agency == \"OEIS\":
        return \"U_\"+ID
    else:
        return ID""")

        # Process: Calculate Treat ID User (Calculate Field) (management)
        TahoeFF_calc_treat_id_user = arcpy.management.CalculateField(in_table=TahoeFF_calc_proj_id_user, 
                                                                  field="TRMTID_USER", 
                                                                  expression="'TAHOE-'+(!PROJECTID_USER![:15])+(!PROJECTID_USER![-1:])+'-'+str(!Shape_Area!)[:8]")

        # Process: Calculate Org Data Steward (Calculate Field) (management)
        TahoeFF_calc_org_data_stew = arcpy.management.CalculateField(in_table=TahoeFF_calc_treat_id_user, 
                                                                        field="ORG_ADMIN_p", 
                                                                        expression="\"Tahoe RCD\"")

        # Process: Calculate Project Contact (Calculate Field) (management)
        TahoeFF_calc_proj_contact = arcpy.management.CalculateField(in_table=TahoeFF_calc_org_data_stew, 
                                                                  field="PROJECT_CONTACT", 
                                                                  expression="\"Cara Moore\"")

        # Process: Calculate Project Email (Calculate Field) (management)
        TahoeFF_calc_proj_email = arcpy.management.CalculateField(in_table=TahoeFF_calc_proj_contact, 
                                                                                 field="PROJECT_EMAIL", 
                                                                                 expression="\"cmoore@tahoercd.org\"")

        # Process: Calculate Treatment Name (Calculate Field) (management)
        TahoeFF_calc_treat_name = arcpy.management.CalculateField(in_table=TahoeFF_calc_proj_email, 
                                                                 field="TREATMENT_NAME", 
                                                                 expression="!PROJ!")

        # Process: Calculate Primary Funding Source (Calculate Field) (management)
        TahoeFF_calc_prim_fund_src = arcpy.management.CalculateField(in_table=TahoeFF_calc_treat_name, 
                                                                 field="PRIMARY_FUNDING_ORG", 
                                                                 expression="!CATEGORY!")

        # Process: Calculate Is BVT User Defined (Calculate Field) (management)
        TahoeFF_calc_bvt_def = arcpy.management.CalculateField(in_table=TahoeFF_calc_prim_fund_src, 
                                                                 field="BVT_USERD", 
                                                                 expression="\"NO\"")

        # Process: Calculate Activity Status (Calculate Field) (management)
        TahoeFF_calc_act_stat = arcpy.management.CalculateField(in_table=TahoeFF_calc_bvt_def, 
                                                                  field="ACTIVITY_STATUS", 
                                                                  expression="\"Complete\"")

        # Process: Calculate Field Activity Quantity (Calculate Field) (management)
        TahoeFF_calc_field_act_quant = arcpy.management.CalculateField(in_table=TahoeFF_calc_act_stat, 
                                                                 field="ACTIVITY_QUANTITY", 
                                                                 expression="!ACRES!")

        # Process: Calculate Field UOM (Calculate Field) (management)
        TahoeFF_calc_field_uom = arcpy.management.CalculateField(in_table=TahoeFF_calc_field_act_quant, 
                                                                 field="ACTIVITY_UOM", 
                                                                 expression="\"AC\"")

        # Process: Calculate Field Implementing Org Name (Calculate Field) (management)
        TahoeFF_calc_field_imp_org_name = arcpy.management.CalculateField(in_table=TahoeFF_calc_field_uom, 
                                                                 field="IMPLEM_ORG_NAME", 
                                                                 expression="!FPD!")

        # Process: Calculate Activity End (Calculate Field) (management)
        TahoeFF_calc_act_end = arcpy.management.CalculateField(in_table=TahoeFF_calc_field_imp_org_name, 
                                                                  field="ACTIVITY_END", 
                                                                  expression="str('6/1/') + str(!YEAR_!)")

        # Process: Calculate Crosswalk (Calculate Field) (management)
        TahoeFF_calc_xwalk = arcpy.management.CalculateField(in_table=TahoeFF_calc_act_end, 
                                                                  field="Crosswalk", 
                                                                  expression="!ACT!")

        # Process: Calculate Source (Calculate Field) (management)
        TahoeFF_calc_src = arcpy.management.CalculateField(in_table=TahoeFF_calc_xwalk, 
                                                                  field="Source", 
                                                                  expression="'Tahoe RCD'")

        # Process: Copy Features (Copy Features) (management)
        arcpy.management.CopyFeatures(in_features=TahoeFF_calc_src, 
                                      out_feature_class=TahoeFF_Tx_standardized.__str__().format(**locals(),**globals()))

        # Process: Delete Field (Delete Field) (management)
        TahoeFF_Tx_standardized_keep_fields = arcpy.management.DeleteField(in_table=TahoeFF_Tx_standardized.__str__().format(**locals(),**globals()), 
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
                                                                                      method="KEEP_FIELDS")

        # Process: 7a Enrichments Polygon (7a Enrichments Polygon) (PC414CWIMillionAcres)
        enrich_polygons(enrich_out=TahoeFF_enriched_scratch, 
                             enrich_in=TahoeFF_Tx_standardized_keep_fields)

        # Process: Copy Features (2) (Copy Features) (management)
        arcpy.management.CopyFeatures(in_features=TahoeFF_enriched_scratch, 
                                      out_feature_class=TahoeFF_Tx_enriched.__str__().format(**locals(),**globals()))

        # Process: 2b Assign Domains (2b Assign Domains) (PC414CWIMillionAcres)
        WFR_TF_Template_2_ = AssignDomains(WFR_TF_Template=TahoeFF_Tx_enriched.__str__().format(**locals(),**globals()))

if __name__ == '__main__':
    runner(workspace,scratch_workspace,TahoeFF6, '*argv[1:]')
    # # Global Environment settings
    # with arcpy.EnvManager(outputCoordinateSystem="PROJCS[\"NAD_1983_California_Teale_Albers\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Albers\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",-4000000.0],PARAMETER[\"Central_Meridian\",-120.0],PARAMETER[\"Standard_Parallel_1\",34.0],PARAMETER[\"Standard_Parallel_2\",40.5],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]", preserveGlobalIds=True, qualifiedFieldNames=False, 
    #                       scratchWorkspace="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb", transferGDBAttributeProperties=True, workspace="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb"):
    #     hTahoeForestFuels20221226(*argv[1:])
