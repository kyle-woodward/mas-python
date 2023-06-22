import arcpy
from ._1b_add_fields import AddFields
from ._2b_assign_domains import AssignDomains
from ._7b_enrichments_pts import enrich_points
from ._2k_keep_fields import KeepFields
import os
from sys import argv
from .utils import init_gdb, delete_scratch_files, runner
import time 
original_gdb, workspace, scratch_workspace = init_gdb()

def PFIRS(input_fc, output_standardized, output_enriched, treat_poly):  
    start = time.time()
    print(f'Start Time {time.ctime()}')
    arcpy.env.overwriteOutput = True

    # Model Environment settings
    with arcpy.EnvManager(outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]"""):
        print('Performing Standardization')
        # Process: Select Layer By Attribute (3) (Select Layer By Attribute) (management)
        pfirs_agencies = arcpy.management.SelectLayerByAttribute(in_layer_or_view= input_fc, 
                                                                                  selection_type="NEW_SELECTION", 
                                                                                  where_clause="AGENCY <> 'Cal Fire' And AGENCY <> 'US Forest Service' And AGENCY <> 'US Fish and Wildlife Services' And AGENCY <> 'Bureau of Land Management' And AGENCY <> 'National Park Service'", 
                                                                                  invert_where_clause="")

        # Process: Copy Features (2) (Copy Features) (management)
        pfirs_input_Copy = os.path.join(scratch_workspace, "pfirs_input_Copy")
        arcpy.management.CopyFeatures(in_features=pfirs_agencies, 
                                      out_feature_class=pfirs_input_Copy,  
                                      config_keyword="", 
                                      spatial_grid_1=None, 
                                      spatial_grid_2=None, 
                                      spatial_grid_3=None)

        # Process: Alter Field (Alter Field) (management)
        pfirs_alter_agency = arcpy.management.AlterField(in_table=pfirs_input_Copy, 
                                                                   field="AGENCY", 
                                                                   new_field_name="AGENCY_", 
                                                                   new_field_alias="", 
                                                                   field_type="TEXT",
                                                                   #field_length=55, 
                                                                   field_is_nullable="NULLABLE", 
                                                                   clear_field_alias="DO_NOT_CLEAR")

        # Process: Alter Field (2) (Alter Field) (management)
        pfirs_alter_county = arcpy.management.AlterField(in_table=pfirs_alter_agency, 
                                                                      field="COUNTY", 
                                                                      new_field_name="COUNTY_", 
                                                                      new_field_alias="", 
                                                                      field_type="TEXT", 
                                                                      #field_length=25, 
                                                                      field_is_nullable="NULLABLE", 
                                                                      clear_field_alias="DO_NOT_CLEAR")

        # Process: 1b Add Fields (1b Add Fields) (PC414CWIMillionAcres)
        pfirs_add_fields = AddFields(Input_Table=pfirs_alter_county)

        # Process: Calculate Project ID (Calculate Field) (management)
        pfirs_calc_prt_id = arcpy.management.CalculateField(in_table=pfirs_add_fields, 
                                                                           field="PROJECTID_USER", 
                                                                           expression="'PFIRS'+'-'+str(!OBJECTID!)", 
                                                                           expression_type="PYTHON3", 
                                                                           code_block="", 
                                                                           field_type="TEXT", 
                                                                           enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Agency (Calculate Field) (management)
        pfirs_calc_agency = arcpy.management.CalculateField(in_table=pfirs_calc_prt_id, 
                                                                  field="AGENCY", 
                                                                  expression="\"CARB\"", 
                                                                  expression_type="PYTHON3", 
                                                                  code_block="", 
                                                                  field_type="TEXT", 
                                                                  enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Data Steward (Calculate Field) (management)
        pfirs_calc_org_admin = arcpy.management.CalculateField(in_table=pfirs_calc_agency, 
                                                              field="ORG_ADMIN_p", 
                                                              expression="\"CARB\"", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Project Contact (Calculate Field) (management)
        pfirs_calc_contact = arcpy.management.CalculateField(in_table=pfirs_calc_org_admin, 
                                                                 field="PROJECT_CONTACT", 
                                                                 expression="\"Jason Branz\"", 
                                                                 expression_type="PYTHON3", 
                                                                 code_block="", 
                                                                 field_type="TEXT", 
                                                                 enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Project Email (Calculate Field) (management)
        pfirs_calc_email = arcpy.management.CalculateField(in_table=pfirs_calc_contact, 
                                                                 field="PROJECT_EMAIL", 
                                                                 expression="\"jason.branz@arb.ca.gov\"", 
                                                                 expression_type="PYTHON3", 
                                                                 code_block="", 
                                                                 field_type="TEXT", 
                                                                 enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Admin Org (Calculate Field) (management)
        pfirs_calc_admin = arcpy.management.CalculateField(in_table=pfirs_calc_email, 
                                                                  field="ADMINISTERING_ORG", 
                                                                  expression="\"CARB\"", 
                                                                  expression_type="PYTHON3", 
                                                                  code_block="", 
                                                                  field_type="TEXT", 
                                                                  enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Project Name (Calculate Field) (management)
        pfirs_calc_prt_name = arcpy.management.CalculateField(in_table=pfirs_calc_admin, 
                                                                  field="PROJECT_NAME", 
                                                                  expression="!BURN_UNIT!", 
                                                                  expression_type="PYTHON3", 
                                                                  code_block="", 
                                                                  field_type="TEXT", 
                                                                  enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Fund Source (Calculate Field) (management)
        pfirs_calc_fund_src = arcpy.management.CalculateField(in_table=pfirs_calc_prt_name, 
                                                                 field="PRIMARY_FUNDING_SOURCE", 
                                                                 expression="\"LOCAL\"", 
                                                                 expression_type="PYTHON3", 
                                                                 code_block="", 
                                                                 field_type="TEXT", 
                                                                 enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Fund Org (Calculate Field) (management)
        pfirs_calc_fund_org = arcpy.management.CalculateField(in_table=pfirs_calc_fund_src, 
                                                                 field="PRIMARY_FUNDING_ORG", 
                                                                 expression="\"OTHER\"", 
                                                                 expression_type="PYTHON3", 
                                                                 code_block="", 
                                                                 field_type="TEXT", 
                                                                 enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Imp Org (Calculate Field) (management)
        pfirs_calc_imp_org = arcpy.management.CalculateField(in_table=pfirs_calc_fund_org, 
                                                                  field="IMPLEMENTING_ORG", 
                                                                  expression="!AGENCY_!", 
                                                                  expression_type="PYTHON3", 
                                                                  code_block="", 
                                                                  field_type="TEXT", 
                                                                  enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Treatment ID (Calculate Field) (management)
        pfirs_calc_trt_id = arcpy.management.CalculateField(in_table=pfirs_calc_imp_org, 
                                                                           field="TRMTID_USER", 
                                                                           expression="'PFIRS'+'-'+str(!OBJECTID!)", 
                                                                           expression_type="PYTHON3", 
                                                                           code_block="", 
                                                                           field_type="TEXT", 
                                                                           enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Project Name (2) (Calculate Field) (management)
        pfirs_calc_prt_name_2 = arcpy.management.CalculateField(in_table=pfirs_calc_trt_id, 
                                                                  field="PROJECTNAME_", 
                                                                  expression="None", 
                                                                  expression_type="PYTHON3", 
                                                                  code_block="", 
                                                                  field_type="TEXT", 
                                                                  enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Data Steward 2 (Calculate Field) (management)
        pfirs_calc_data_stew = arcpy.management.CalculateField(in_table=pfirs_calc_prt_name_2, 
                                                                 field="ORG_ADMIN_t", 
                                                                 expression="None", 
                                                                 expression_type="PYTHON3", 
                                                                 code_block="", 
                                                                 field_type="TEXT", 
                                                                 enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Veg User Defined (Calculate Field) (management)
        pfirs_calc_bvt_user = arcpy.management.CalculateField(in_table=pfirs_calc_data_stew, 
                                                                 field="BVT_USERD", 
                                                                 expression="\"NO\"", 
                                                                 expression_type="PYTHON3", 
                                                                 code_block="", 
                                                                 field_type="TEXT", 
                                                                 enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Activity End Date (Calculate Field) (management)
        pfirs_calc_act_end = arcpy.management.CalculateField(in_table=pfirs_calc_bvt_user, 
                                                                 field="ACTIVITY_END", 
                                                                 expression="!BURN_DATE!", 
                                                                 expression_type="PYTHON3", 
                                                                 code_block="", 
                                                                 field_type="TEXT", 
                                                                 enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Status (Calculate Field) (management)
        pfirs_calc_status = arcpy.management.CalculateField(in_table=pfirs_calc_act_end, 
                                                                  field="ACTIVITY_STATUS", 
                                                                  expression="\"COMPLETE\"", 
                                                                  expression_type="PYTHON3", 
                                                                  code_block="", 
                                                                  field_type="TEXT", 
                                                                  enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Activity Quantity (3) (Calculate Field) (management)
        pfirs_calc_act_qnt = arcpy.management.CalculateField(in_table=pfirs_calc_status, 
                                                                           field="ACTIVITY_QUANTITY", 
                                                                           expression="!ACRES_BURNED!", 
                                                                           expression_type="PYTHON3", 
                                                                           code_block="", 
                                                                           field_type="DOUBLE", 
                                                                           enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Activity UOM (3) (Calculate Field) (management)
        pfirs_calc_act_uom = arcpy.management.CalculateField(in_table=pfirs_calc_act_qnt, 
                                                                           field="ACTIVITY_UOM", 
                                                                           expression="\"AC\"", 
                                                                           expression_type="PYTHON3", 
                                                                           code_block="", 
                                                                           field_type="TEXT", 
                                                                           enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Admin Org2 (Calculate Field) (management)
        pfirs_calc_admin_org = arcpy.management.CalculateField(in_table=pfirs_calc_act_uom, 
                                                                  field="ADMIN_ORG_NAME", 
                                                                  expression="\"CARB\"", 
                                                                  expression_type="PYTHON3", 
                                                                  code_block="", 
                                                                  field_type="TEXT", 
                                                                  enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Implementation Org 2 (Calculate Field) (management)
        pfirs_calc_imp_org2 = arcpy.management.CalculateField(in_table=pfirs_calc_admin_org, 
                                                                  field="IMPLEM_ORG_NAME", 
                                                                  expression="!AGENCY_!", 
                                                                  expression_type="PYTHON3", 
                                                                  code_block="", 
                                                                  field_type="TEXT", 
                                                                  enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Primary Fund Source (Calculate Field) (management)
        pfirs_calc_fund_src_name = arcpy.management.CalculateField(in_table=pfirs_calc_imp_org2, 
                                                                  field="PRIMARY_FUND_SRC_NAME", 
                                                                  expression="\"LOCAL\"", 
                                                                  expression_type="PYTHON3", 
                                                                  code_block="", 
                                                                  field_type="TEXT", 
                                                                  enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Fund Org 2 (Calculate Field) (management)
        pfirs_calc_fund_org2 = arcpy.management.CalculateField(in_table=pfirs_calc_fund_src_name, 
                                                                  field="PRIMARY_FUND_ORG_NAME", 
                                                                  expression="\"OTHER\"", 
                                                                  expression_type="PYTHON3", 
                                                                  code_block="", 
                                                                  field_type="TEXT", 
                                                                  enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Source (Calculate Field) (management)
        pfirs_calc_src = arcpy.management.CalculateField(in_table=pfirs_calc_fund_org2, 
                                                                  field="Source", 
                                                                  expression="\"PIFIRS\"", 
                                                                  expression_type="PYTHON3", 
                                                                  code_block="", 
                                                                  field_type="TEXT", 
                                                                  enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Crosswalk (Calculate Field) (management)
        pfirs_calc_xwalk = arcpy.management.CalculateField(in_table=pfirs_calc_src, 
                                                                  field="Crosswalk", 
                                                                  expression="ifelse(!BURN_TYPE!)", 
                                                                  expression_type="PYTHON3", code_block="""def ifelse(Act):
    if Act == \"Broadcast\":
        return \"Broadcast Burn\"
    elif Act == \"Unknown\":
        return \"Broadcast Burn\"
    elif Act == \"Hand Pile\":
        return \"Hand Pile Burn\"
    elif Act == \"Machine Pile\":
        return \"Machine Pile Burn\"
    elif Act == \"Landing Pile\":
        return \"Landing Pile Burn\"
    elif Act == \"Multiple Fuels\":
        return \"Broadcast Burn\"
    elif Act == \"UNK\":
        return \"Broadcast Burn\"
    else:
        return Act""", 
    field_type="TEXT", 
    enforce_domains="NO_ENFORCE_DOMAINS")

        print(f'Saving Output Standardized: {output_standardized}')
        # Process: Copy Features (3) (Copy Features) (management)
        arcpy.management.CopyFeatures(in_features=pfirs_calc_xwalk, 
                                      out_feature_class=output_standardized, 
                                      config_keyword="", 
                                      spatial_grid_1=None, 
                                      spatial_grid_2=None, 
                                      spatial_grid_3=None)

        # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
        pfirs_rx_burns = arcpy.management.SelectLayerByAttribute(in_layer_or_view=treat_poly, 
                                                                                         selection_type="NEW_SELECTION", 
                                                                                         where_clause="ACTIVITY_DESCRIPTION = 'BROADCAST_BURN' Or ACTIVITY_DESCRIPTION = 'PILE_BURN'", 
                                                                                         invert_where_clause="")

        # Process: Select Layer By Location (Select Layer By Location) (management)
        pfirs_intersect = arcpy.management.SelectLayerByLocation(in_layer=[output_standardized], 
                                                                                                 overlap_type="INTERSECT", 
                                                                                                 select_features=pfirs_rx_burns, 
                                                                                                 search_distance="", 
                                                                                                 selection_type="NEW_SELECTION", invert_spatial_relationship="NOT_INVERT")

        # Process: Delete Rows (Delete Rows) (management)
        pfirs_rows_deleted = arcpy.management.DeleteRows(in_rows=pfirs_intersect)

        # Process: Delete Field (Delete Field) (management)
        pfirs_keep_field = KeepFields(pfirs_rows_deleted) 

        # Process: 2b Assign Domains (2b Assign Domains) (PC414CWIMillionAcres)
        pfirs_assign_domains = AssignDomains(in_table=pfirs_keep_field)
        output_standardized_copy = os.path.join(scratch_workspace, "pfirs_standardized_copy")
        arcpy.CopyFeatures_management(pfirs_assign_domains, output_standardized_copy)

        print('Performing Enrichments')
        # Process: 7b Enrichments pts (7b Enrichments pts) (PC414CWIMillionAcres)
        # Pts_enrichment_Veg2 = os.path.join(scratch_workspace, "Pts_enrichment_Veg2") # no point in having final output be a scratch file
        enrich_points(enrich_pts_out=output_enriched, 
                           enrich_pts_in=output_standardized_copy)

        print(f'Saving Output Enriched: {output_enriched}')
        # Process: Copy Features (Copy Features) (management)
        # arcpy.management.CopyFeatures(in_features=Pts_enrichment_Veg2, 
        #                               out_feature_class=output_enriched)

        # Process: 2b Assign Domains (2) (2b Assign Domains) (PC414CWIMillionAcres)
        # pfirs_enriched_assign_domains = 
        AssignDomains(in_table=output_enriched)

        print('Deleting Scratch Files')
        delete_scratch_files(gdb = scratch_workspace, delete_fc = 'yes', delete_table = 'yes', delete_ds = 'yes')
        end = time.time()
        print(f'Time Elapsed: {(end-start)/60} minutes')
if __name__ == '__main__':
     runner(workspace,scratch_workspace,PFIRS, '*argv[1:]')
    # # Global Environment settings
    #  with arcpy.EnvManager(
    # extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""",  outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""", 
    # preserveGlobalIds=True, 
    # qualifiedFieldNames=False, 
    # scratchWorkspace=scratch_workspace, 
    # transferDomains=True, 
    # transferGDBAttributeProperties=True, 
    # workspace=workspace):
    #     PFIRS(*argv[1:])
