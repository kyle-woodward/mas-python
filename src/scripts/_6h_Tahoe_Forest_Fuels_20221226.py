"""
"""
import arcpy
from scripts._1b_add_fields import AddFields
from scripts._2b_assign_domains import AssignDomains
<<<<<<< HEAD
from scripts._7a_enrichments_polygon import enrich_polygons
from scripts.utils import runner, init_gdb
=======
from scripts._7a_enrichments_polygon import aEnrichmentsPolygon1
from scripts.utils import runner, init_gdb, delete_scratch_files, KeepFields
>>>>>>> 1f899f8affb0c4abb79e4204a32d440344232227
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
    TahoeFF_enriched_scratch = os.path.join(scratch_workspace, 'TahoeFF_enriched_scratch')

    # Model Environment settings
    with arcpy.EnvManager(extent="-415308.137838921 -608601.962396972 551888.996651875 458556.048364898 PROJCS[\"NAD_1983_California_Teale_Albers\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Albers\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",-4000000.0],PARAMETER[\"Central_Meridian\",-120.0],PARAMETER[\"Standard_Parallel_1\",34.0],PARAMETER[\"Standard_Parallel_2\",40.5],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]"):
        California = os.path.join(workspace, 'b_Reference', 'California')
        CPAD_Ownership_Update = os.path.join(workspace, 'b_Reference', 'CPAD_Ownership_Update')

        # Process: Pairwise Clip (Pairwise Clip) (analysis)
        print("Executing Step 1/40 : Pairwise clip...")
        arcpy.analysis.PairwiseClip(in_features=TahoeFF_Tx_OG, 
                                    clip_features=California, 
                                    out_feature_class=TahoeFF_pairwiseclip)

        # Process: Select no Fed or NV or Wildland Fire (Select) (analysis)
        print("Executing Step 2/40 : Select no Fed or NV or Wildland Fire (Select)...")
        arcpy.analysis.Select(in_features=TahoeFF_pairwiseclip, 
                              out_feature_class=TahoeFF_Tx_OG_Select, 
                              where_clause="CATEGORY <> 'Federal' And CATEGORY <> 'NV' And ACT <> 'Wildland Fire'")

        # Process: Repair Geometry (Repair Geometry) (management)
        print("Executing Step 3/40 : Repair Geometry...")
        TahoeFF_repair_geom = arcpy.management.RepairGeometry(in_features=TahoeFF_Tx_OG_Select, 
                                                                       delete_null="KEEP_NULL")

        # Process: Alter Field (Alter Field) (management)
        print("Executing Step 4/40 : Alter Field...")
        TahoeFF_alter_year = arcpy.management.AlterField(in_table=TahoeFF_repair_geom, 
                                                                             field="YEAR", 
                                                                             new_field_name="YEAR_", 
                                                                             new_field_alias="YEAR_")

        # Process: 1b Add Fields (2) (1b Add Fields) (PC414CWIMillionAcres)
<<<<<<< HEAD
        TahoeFF_add_fields = AddFields(Input_Table=TahoeFF_alter_year)
=======
        print("Executing Step 5/40 : Add Fields...")
        TahoeFF_add_fields = AddFields2(Input_Table=TahoeFF_alter_year)
>>>>>>> 1f899f8affb0c4abb79e4204a32d440344232227

        # Process: Calculate Project ID (Calculate Field) (management)
        print("Executing Step 5/40 : Calculate PROJECT_ID...")
        Tahoe_calc_proj_id = arcpy.management.CalculateField(in_table=TahoeFF_add_fields, 
                                                                 field="PROJECTID", 
                                                                 expression="None")

        # Process: Calculate Project ID Null (Calculate Field) (management)
        print("Executing Step 6/40 : Calculate Project_ID...")
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
        print("Executing Step 7/40 : Calculate EIP_Number...")
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
        print("Executing Step 8/40 : Calculate PROJ...")
        Tahoe_calc_proj_null = arcpy.management.CalculateField(in_table=Tahoe_calc_eip_null, 
                                                                  field="PROJ", 
                                                                  expression="ifelse(!PROJ!)", 
                                                                  code_block="""def ifelse(ID):
    if ID == '':
        return None
    return ID""")

        # Process: Calculate Year 0 (Calculate Field) (management)
        print("Executing Step 9/40 : Calculate YEAR_...")
        Tahoe_calc_year = arcpy.management.CalculateField(in_table=Tahoe_calc_proj_null, 
                                                                  field="YEAR_", 
                                                                  expression="ifelse(!YEAR_!)", 
                                                                  code_block="""def ifelse(ID):
    if ID == 0:
        return 0
    return ID""")

        # Process: Calculate Own Full Null (Calculate Field) (management)
        print("Executing Step 10/40 : Calculate OWN_FULL...")
        Tahoe_calc_own_full_null = arcpy.management.CalculateField(in_table=Tahoe_calc_year, 
                                                                  field="OWN_FULL", 
                                                                  expression="ifelse(!OWN_FULL!)", 
                                                                  code_block="""def ifelse(ID):
    if ID == '':
        return None
    return ID""")

        # Process: Calculate Project ID User (Calculate Field) (management)
        print("Executing Step 11/40 : Calculate PROJECTID_USER...")
        Tahoe_calc_proj_id_user = arcpy.management.CalculateField(in_table=Tahoe_calc_own_full_null, 
                                                                  field="PROJECTID_USER", 
                                                                  expression="ifelse(!PROJECTID_USER!,!Project_ID!)", 
                                                                  code_block="""def ifelse(ID, ID2):
    if ID == None:
        return ID2
    else:
        return ID""")

        # Process: Calculate Project ID User (2) (Calculate Field) (management)
        print("Executing Step 12/40 : Calculate PROJECTID_USER...")
        Tahoe_calc_proj_id_user_2 = arcpy.management.CalculateField(in_table=Tahoe_calc_proj_id_user, 
                                                                  field="PROJECTID_USER", 
                                                                  expression="ifelse(!PROJECTID_USER!,!EIP_Number!)", 
                                                                  code_block="""def ifelse(ID, EIP):
    if ID == None:
        return EIP
    else:
        return ID""")

        # Process: Calculate Project ID User (3) (Calculate Field) (management)
        print("Executing Step 13/40 : Calculate PROJECTID_USER...")
        Tahoe_calc_proj_id_user_3 = arcpy.management.CalculateField(in_table=Tahoe_calc_proj_id_user_2, 
                                                                  field="PROJECTID_USER", 
                                                                  expression="ifelse(!PROJECTID_USER!,!PROJ!)", 
                                                                  code_block="""def ifelse(ID, Proj):
    if ID == None:
        return Proj
    else:
        return ID""")

        # Process: Calculate Project ID User (4) (Calculate Field) (management)
        print("Executing Step 14/40 : Calculate PROJECTID_USER...")
        Tahoe_calc_proj_id_user_4 = arcpy.management.CalculateField(in_table=Tahoe_calc_proj_id_user_3, 
                                                                  field="PROJECTID_USER", 
                                                                  expression="ifelse(!PROJECTID_USER!, !JURIS!)", 
                                                                  code_block="""def ifelse(ID, Jur):
    if ID == None:
        return Jur
    else:
        return ID""")

        # Process: Calculate Agency (Calculate Field) (management)
        print("Executing Step 15/40 : Calculate AGENCY...")
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
        print("Executing Step 16/40 : Calculate ADMINISTERING_ORG...")
        Tahoe_calc_admin_org = arcpy.management.CalculateField(in_table=Tahoe_calc_agency, 
                                                              field="ADMINISTERING_ORG", 
                                                              expression="!OWN_FULL!")

        # Process: Select (Select) (analysis) 
        print("Executing Step 17/40 : Select California Department of Parks and Recreation...")
        arcpy.analysis.Select(in_features=CPAD_Ownership_Update, 
                              out_feature_class=CPAD_Ownership_StateParks, 
                              where_clause="AGNCY_NAME = 'California Department of Parks and Recreation'")

        # Process: Select Layer By State Parks Location (Select Layer By Location) (management)
        print("Executing Step 18/40 : Calculate Select CPAD_Ownership_stateparks...")
        TahoeFF_select_SP = arcpy.management.SelectLayerByLocation(in_layer=Tahoe_calc_admin_org,
                                                                   overlap_type="HAVE_THEIR_CENTER_IN",
                                                                   select_features=CPAD_Ownership_StateParks,
                                                                   search_distance="1 Meters")

        # Process: Calculate Admin Org Parks (Calculate Field) (management)
        print("Executing Step 19/40 : Calculate ADMINISTERING_ORG...")
        TahoeFF_SP_calc_admin_org_parks = arcpy.management.CalculateField(in_table=TahoeFF_select_SP, 
                                                                          field="ADMINISTERING_ORG", 
                                                                          expression="\"PARKS\"")

        # Process: Clear Selection (Select Layer By Attribute) (management)
        print("Executing Step 20/40 : clear selection...")
        TahoeFF_SP_clear_select = arcpy.management.SelectLayerByAttribute(in_layer_or_view=TahoeFF_SP_calc_admin_org_parks, 
                                                                                            selection_type="CLEAR_SELECTION")

        # Process: Calculate Project ID User (5) (Calculate Field) (management)
        print("Executing Step 21/40 : Calculate PROJECTID_USER...")
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
        print("Executing Step 22/40 : Calculate TRMTID_USER...")
        TahoeFF_calc_treat_id_user = arcpy.management.CalculateField(in_table=TahoeFF_calc_proj_id_user, 
                                                                  field="TRMTID_USER", 
                                                                  expression="'TAHOE-'+(!PROJECTID_USER![:15])+(!PROJECTID_USER![-1:])+'-'+str(!Shape_Area!)[:8]")

        # Process: Calculate Org Data Steward (Calculate Field) (management)
        print("Executing Step 23/40 : Calculate ORG_ADMIN_p...")
        TahoeFF_calc_org_data_stew = arcpy.management.CalculateField(in_table=TahoeFF_calc_treat_id_user, 
                                                                        field="ORG_ADMIN_p", 
                                                                        expression="\"Tahoe RCD\"")

        # Process: Calculate Project Contact (Calculate Field) (management)
        print("Executing Step 24/40 : Calculate PROJECT_CONTACT...")
        TahoeFF_calc_proj_contact = arcpy.management.CalculateField(in_table=TahoeFF_calc_org_data_stew, 
                                                                  field="PROJECT_CONTACT", 
                                                                  expression="\"Cara Moore\"")

        # Process: Calculate Project Email (Calculate Field) (management)
        print("Executing Step 25/40 : Calculate PROJECT_EMAIL...")
        TahoeFF_calc_proj_email = arcpy.management.CalculateField(in_table=TahoeFF_calc_proj_contact, 
                                                                                 field="PROJECT_EMAIL", 
                                                                                 expression="\"cmoore@tahoercd.org\"")

        # Process: Calculate Treatment Name (Calculate Field) (management)
        print("Executing Step 26/40 : Calculate TREATMENT_NAME...")
        TahoeFF_calc_treat_name = arcpy.management.CalculateField(in_table=TahoeFF_calc_proj_email, 
                                                                 field="TREATMENT_NAME", 
                                                                 expression="!PROJ!")

        # Process: Calculate Primary Funding Source (Calculate Field) (management)
        print("Executing Step 27/40 : Calculate PRIMARY_FUNDING_ORG...")
        TahoeFF_calc_prim_fund_src = arcpy.management.CalculateField(in_table=TahoeFF_calc_treat_name, 
                                                                 field="PRIMARY_FUNDING_ORG", 
                                                                 expression="!CATEGORY!")

        # Process: Calculate Is BVT User Defined (Calculate Field) (management)
        print("Executing Step 28/40 : Calculate BVT_USERD...")
        TahoeFF_calc_bvt_def = arcpy.management.CalculateField(in_table=TahoeFF_calc_prim_fund_src, 
                                                                 field="BVT_USERD", 
                                                                 expression="\"NO\"")

        # Process: Calculate Activity Status (Calculate Field) (management)
        print("Executing Step 29/40 : Calculate ACTIVITY_STATUS...")
        TahoeFF_calc_act_stat = arcpy.management.CalculateField(in_table=TahoeFF_calc_bvt_def, 
                                                                  field="ACTIVITY_STATUS", 
                                                                  expression="\"Complete\"")

        # Process: Calculate Field Activity Quantity (Calculate Field) (management)
        print("Executing Step 30/40 : Calculate ACTIVITY_QUANTITY...")
        TahoeFF_calc_field_act_quant = arcpy.management.CalculateField(in_table=TahoeFF_calc_act_stat, 
                                                                 field="ACTIVITY_QUANTITY", 
                                                                 expression="!ACRES!")

        # Process: Calculate Field UOM (Calculate Field) (management)
        print("Executing Step 31/40 : Calculate ACTIVITY_UOM...")
        TahoeFF_calc_field_uom = arcpy.management.CalculateField(in_table=TahoeFF_calc_field_act_quant, 
                                                                 field="ACTIVITY_UOM", 
                                                                 expression="\"AC\"")

        # Process: Calculate Field Implementing Org Name (Calculate Field) (management)
        print("Executing Step 32/40 : Calculate IMPLEM_ORG_NAME...")
        TahoeFF_calc_field_imp_org_name = arcpy.management.CalculateField(in_table=TahoeFF_calc_field_uom, 
                                                                 field="IMPLEM_ORG_NAME", 
                                                                 expression="!FPD!")

        # Process: Calculate Activity End (Calculate Field) (management)
        print("Executing Step 33/40 : Calculate ACTIVITY_END...")
        TahoeFF_calc_act_end = arcpy.management.CalculateField(in_table=TahoeFF_calc_field_imp_org_name, 
                                                                  field="ACTIVITY_END", 
                                                                  expression="str('6/1/') + str(!YEAR_!)")

        # Process: Calculate Crosswalk (Calculate Field) (management)
        print("Executing Step 34/40 : Calculate Crosswalk...")
        TahoeFF_calc_xwalk = arcpy.management.CalculateField(in_table=TahoeFF_calc_act_end, 
                                                                  field="Crosswalk", 
                                                                  expression="!ACT!")

        # Process: Calculate Source (Calculate Field) (management)
        print("Executing Step 35/40 : Calculate Source...")
        TahoeFF_calc_src = arcpy.management.CalculateField(in_table=TahoeFF_calc_xwalk, 
                                                                  field="Source", 
                                                                  expression="'Tahoe RCD'")

        # Process: Copy Features (Copy Features) (management)
        print("Executing Step 36/40 : Copy Features...")
        arcpy.management.CopyFeatures(in_features=TahoeFF_calc_src, 
                                      out_feature_class=TahoeFF_Tx_standardized.__str__().format(**locals(),**globals()))

        # Process: Delete Field (Delete Field) (management)
        print("Executing Step 37/40 : Keep Fields...")
        TahoeFF_Tx_standardized_keep_fields = KeepFields(TahoeFF_Tx_standardized.__str__().format(**locals(),**globals()))
        

        # check_this_out = os.path.join(scratch_workspace, "check_this_one")
        # arcpy.management.CopyFeatures(in_features=TahoeFF_Tx_standardized_keep_fields, 
        #                               out_feature_class = check_this_out.__str__().format(**locals(),**globals()))
        
        # Process: 7a Enrichments Polygon (7a Enrichments Polygon) (PC414CWIMillionAcres)
<<<<<<< HEAD
        enrich_polygons(enrich_out=TahoeFF_enriched_scratch, 
=======
        print("Executing Step 38/40 : Enrich Polygons...")
        aEnrichmentsPolygon1(enrich_out=TahoeFF_enriched_scratch, 
>>>>>>> 1f899f8affb0c4abb79e4204a32d440344232227
                             enrich_in=TahoeFF_Tx_standardized_keep_fields)

        # Process: Copy Features (2) (Copy Features) (management)
        print("Executing Step 39/40 : Calculate Copy Features...")
        arcpy.management.CopyFeatures(in_features=TahoeFF_enriched_scratch, 
                                      out_feature_class=TahoeFF_Tx_enriched.__str__().format(**locals(),**globals()))

        # Process: 2b Assign Domains (2b Assign Domains) (PC414CWIMillionAcres)
        print("Executing Step 40/40 : AssignDomains...")
        WFR_TF_Template_2_ = AssignDomains(in_table=TahoeFF_Tx_enriched.__str__().format(**locals(),**globals()))

        print("completed step 40/40")
        #delete_scratch_files(gdb = scratch_workspace, delete_fc = 'yes', delete_table = 'yes', delete_ds = 'yes')

if __name__ == '__main__':
    # runner(workspace,scratch_workspace,TahoeFF6, '*argv[1:]')
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
        TahoeFF6(*argv[1:])
