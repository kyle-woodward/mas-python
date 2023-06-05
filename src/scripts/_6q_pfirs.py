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

def Model72(input_fc, output_standardized, output_enriched, treat_poly):  
    start = time.time()
    print(f'Start Time {time.ctime()}')
    arcpy.env.overwriteOutput = True

    # Model Environment settings
    with arcpy.EnvManager(outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]"""):
        print('Performing Standardization')
        # Process: Select Layer By Attribute (3) (Select Layer By Attribute) (management)
        PFIRS_2018_2022_Layer, Count_3_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view= input_fc, 
                                                                                  selection_type="NEW_SELECTION", 
                                                                                  where_clause="AGENCY <> 'Cal Fire' And AGENCY <> 'US Forest Service' And AGENCY <> 'US Fish and Wildlife Services' And AGENCY <> 'Bureau of Land Management' And AGENCY <> 'National Park Service'", 
                                                                                  invert_where_clause="")

        # Process: Copy Features (2) (Copy Features) (management)
        Output_Feature_Class = os.path.join(scratch_workspace, "PFIRS_2018_2022_CopyFeatures")
        arcpy.management.CopyFeatures(in_features=PFIRS_2018_2022_Layer, 
                                      out_feature_class=Output_Feature_Class,  
                                      config_keyword="", 
                                      spatial_grid_1=None, 
                                      spatial_grid_2=None, 
                                      spatial_grid_3=None)

        # Process: Alter Field (Alter Field) (management)
        PFIRS_2018_2022_CopyFeatures = arcpy.management.AlterField(in_table=Output_Feature_Class, 
                                                                   field="AGENCY", 
                                                                   new_field_name="AGENCY_", 
                                                                   new_field_alias="", 
                                                                   field_type="TEXT",
                                                                   #field_length=55, 
                                                                   field_is_nullable="NULLABLE", 
                                                                   clear_field_alias="DO_NOT_CLEAR")

        # Process: Alter Field (2) (Alter Field) (management)
        PFIRS_2018_2022_CopyFeatures_2_ = arcpy.management.AlterField(in_table=PFIRS_2018_2022_CopyFeatures, 
                                                                      field="COUNTY", 
                                                                      new_field_name="COUNTY_", 
                                                                      new_field_alias="", 
                                                                      field_type="TEXT", 
                                                                      #field_length=25, 
                                                                      field_is_nullable="NULLABLE", 
                                                                      clear_field_alias="DO_NOT_CLEAR")

        # Process: 1b Add Fields (1b Add Fields) (PC414CWIMillionAcres)
        WFRTF_Template_4_ = AddFields(Input_Table=PFIRS_2018_2022_CopyFeatures_2_)

        # Process: Calculate Project ID (Calculate Field) (management)
        Activity_SilvTSI_20220627_Se2_2_ = arcpy.management.CalculateField(in_table=WFRTF_Template_4_, 
                                                                           field="PROJECTID_USER", 
                                                                           expression="'PFIRS'+'-'+str(!OBJECTID!)", 
                                                                           expression_type="PYTHON3", 
                                                                           code_block="", 
                                                                           field_type="TEXT", 
                                                                           enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Agency (Calculate Field) (management)
        Updated_Input_Table_30_ = arcpy.management.CalculateField(in_table=Activity_SilvTSI_20220627_Se2_2_, 
                                                                  field="AGENCY", 
                                                                  expression="\"CARB\"", 
                                                                  expression_type="PYTHON3", 
                                                                  code_block="", 
                                                                  field_type="TEXT", 
                                                                  enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Data Steward (Calculate Field) (management)
        Updated_Input_Table = arcpy.management.CalculateField(in_table=Updated_Input_Table_30_, 
                                                              field="ORG_ADMIN_p", 
                                                              expression="\"CARB\"", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Project Contact (Calculate Field) (management)
        Updated_Input_Table_3_ = arcpy.management.CalculateField(in_table=Updated_Input_Table, 
                                                                 field="PROJECT_CONTACT", 
                                                                 expression="\"Jason Branz\"", 
                                                                 expression_type="PYTHON3", 
                                                                 code_block="", 
                                                                 field_type="TEXT", 
                                                                 enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Project Email (Calculate Field) (management)
        Updated_Input_Table_5_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_3_, 
                                                                 field="PROJECT_EMAIL", 
                                                                 expression="\"jason.branz@arb.ca.gov\"", 
                                                                 expression_type="PYTHON3", 
                                                                 code_block="", 
                                                                 field_type="TEXT", 
                                                                 enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Admin Org (Calculate Field) (management)
        Updated_Input_Table_31_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_5_, 
                                                                  field="ADMINISTERING_ORG", 
                                                                  expression="\"CARB\"", 
                                                                  expression_type="PYTHON3", 
                                                                  code_block="", 
                                                                  field_type="TEXT", 
                                                                  enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Project Name (Calculate Field) (management)
        Updated_Input_Table_33_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_31_, 
                                                                  field="PROJECT_NAME", 
                                                                  expression="!BURN_UNIT!", 
                                                                  expression_type="PYTHON3", 
                                                                  code_block="", 
                                                                  field_type="TEXT", 
                                                                  enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Fund Source (Calculate Field) (management)
        Updated_Input_Table_6_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_33_, 
                                                                 field="PRIMARY_FUNDING_SOURCE", 
                                                                 expression="\"LOCAL\"", 
                                                                 expression_type="PYTHON3", 
                                                                 code_block="", 
                                                                 field_type="TEXT", 
                                                                 enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Fund Org (Calculate Field) (management)
        Updated_Input_Table_7_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_6_, 
                                                                 field="PRIMARY_FUNDING_ORG", 
                                                                 expression="\"OTHER\"", 
                                                                 expression_type="PYTHON3", 
                                                                 code_block="", 
                                                                 field_type="TEXT", 
                                                                 enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Imp Org (Calculate Field) (management)
        Updated_Input_Table_32_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_7_, 
                                                                  field="IMPLEMENTING_ORG", 
                                                                  expression="!AGENCY_!", 
                                                                  expression_type="PYTHON3", 
                                                                  code_block="", 
                                                                  field_type="TEXT", 
                                                                  enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Treatment ID (Calculate Field) (management)
        Activity_SilvTSI_20220627_Se2_3_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_32_, 
                                                                           field="TRMTID_USER", 
                                                                           expression="'PFIRS'+'-'+str(!OBJECTID!)", 
                                                                           expression_type="PYTHON3", 
                                                                           code_block="", 
                                                                           field_type="TEXT", 
                                                                           enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Project Name (2) (Calculate Field) (management)
        Updated_Input_Table_14_ = arcpy.management.CalculateField(in_table=Activity_SilvTSI_20220627_Se2_3_, 
                                                                  field="PROJECTNAME_", 
                                                                  expression="None", 
                                                                  expression_type="PYTHON3", 
                                                                  code_block="", 
                                                                  field_type="TEXT", 
                                                                  enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Data Steward 2 (Calculate Field) (management)
        Updated_Input_Table_8_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_14_, 
                                                                 field="ORG_ADMIN_t", 
                                                                 expression="None", 
                                                                 expression_type="PYTHON3", 
                                                                 code_block="", 
                                                                 field_type="TEXT", 
                                                                 enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Veg User Defined (Calculate Field) (management)
        Updated_Input_Table_9_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_8_, 
                                                                 field="BVT_USERD", 
                                                                 expression="\"NO\"", 
                                                                 expression_type="PYTHON3", 
                                                                 code_block="", 
                                                                 field_type="TEXT", 
                                                                 enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Activity End Date (Calculate Field) (management)
        Updated_Input_Table_2_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_9_, 
                                                                 field="ACTIVITY_END", 
                                                                 expression="!BURN_DATE!", 
                                                                 expression_type="PYTHON3", 
                                                                 code_block="", 
                                                                 field_type="TEXT", 
                                                                 enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Status (Calculate Field) (management)
        Updated_Input_Table_35_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_2_, 
                                                                  field="ACTIVITY_STATUS", 
                                                                  expression="\"COMPLETE\"", 
                                                                  expression_type="PYTHON3", 
                                                                  code_block="", 
                                                                  field_type="TEXT", 
                                                                  enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Activity Quantity (3) (Calculate Field) (management)
        Activity_SilvTSI_20220627_Se2_6_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_35_, 
                                                                           field="ACTIVITY_QUANTITY", 
                                                                           expression="!ACRES_BURNED!", 
                                                                           expression_type="PYTHON3", 
                                                                           code_block="", 
                                                                           field_type="DOUBLE", 
                                                                           enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Activity UOM (3) (Calculate Field) (management)
        Activity_SilvTSI_20220627_Se2_5_ = arcpy.management.CalculateField(in_table=Activity_SilvTSI_20220627_Se2_6_, 
                                                                           field="ACTIVITY_UOM", 
                                                                           expression="\"AC\"", 
                                                                           expression_type="PYTHON3", 
                                                                           code_block="", 
                                                                           field_type="TEXT", 
                                                                           enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Admin Org2 (Calculate Field) (management)
        Updated_Input_Table_10_ = arcpy.management.CalculateField(in_table=Activity_SilvTSI_20220627_Se2_5_, 
                                                                  field="ADMIN_ORG_NAME", 
                                                                  expression="\"CARB\"", 
                                                                  expression_type="PYTHON3", 
                                                                  code_block="", 
                                                                  field_type="TEXT", 
                                                                  enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Implementation Org 2 (Calculate Field) (management)
        Updated_Input_Table_11_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_10_, 
                                                                  field="IMPLEM_ORG_NAME", 
                                                                  expression="!AGENCY_!", 
                                                                  expression_type="PYTHON3", 
                                                                  code_block="", 
                                                                  field_type="TEXT", 
                                                                  enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Primary Fund Source (Calculate Field) (management)
        Updated_Input_Table_12_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_11_, 
                                                                  field="PRIMARY_FUND_SRC_NAME", 
                                                                  expression="\"LOCAL\"", 
                                                                  expression_type="PYTHON3", 
                                                                  code_block="", 
                                                                  field_type="TEXT", 
                                                                  enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Fund Org 2 (Calculate Field) (management)
        Updated_Input_Table_13_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_12_, 
                                                                  field="PRIMARY_FUND_ORG_NAME", 
                                                                  expression="\"OTHER\"", 
                                                                  expression_type="PYTHON3", 
                                                                  code_block="", 
                                                                  field_type="TEXT", 
                                                                  enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Source (Calculate Field) (management)
        Updated_Input_Table_36_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_13_, 
                                                                  field="Source", 
                                                                  expression="\"PIFIRS\"", 
                                                                  expression_type="PYTHON3", 
                                                                  code_block="", 
                                                                  field_type="TEXT", 
                                                                  enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Crosswalk (Calculate Field) (management)
        Updated_Input_Table_39_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_36_, 
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
        arcpy.management.CopyFeatures(in_features=Updated_Input_Table_39_, 
                                      out_feature_class=output_standardized, 
                                      config_keyword="", 
                                      spatial_grid_1=None, 
                                      spatial_grid_2=None, 
                                      spatial_grid_3=None)

        # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
        Treat_n_harvests_polygons_20, Count_2_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=treat_poly, 
                                                                                         selection_type="NEW_SELECTION", 
                                                                                         where_clause="ACTIVITY_DESCRIPTION = 'BROADCAST_BURN' Or ACTIVITY_DESCRIPTION = 'PILE_BURN'", 
                                                                                         invert_where_clause="")

        # Process: Select Layer By Location (Select Layer By Location) (management)
        Layer_With_Selection, Output_Layer_Names, Count = arcpy.management.SelectLayerByLocation(in_layer=[output_standardized], 
                                                                                                 overlap_type="INTERSECT", 
                                                                                                 select_features=Treat_n_harvests_polygons_20, 
                                                                                                 search_distance="", 
                                                                                                 selection_type="NEW_SELECTION", invert_spatial_relationship="NOT_INVERT")

        # Process: Delete Rows (Delete Rows) (management)
        Updated_Input_With_Rows_Removed = arcpy.management.DeleteRows(in_rows=Layer_With_Selection)

        # Process: Delete Field (Delete Field) (management)
        PFIRS_standardized_2_ = KeepFields(Updated_Input_With_Rows_Removed) 

        # Process: 2b Assign Domains (2b Assign Domains) (PC414CWIMillionAcres)
        usfs_silviculture_reforestation_enriched_20220629_2_ = AssignDomains(in_table=PFIRS_standardized_2_)
        output_standardized_copy = os.path.join(scratch_workspace, "hope_this_works")
        arcpy.CopyFeatures_management(usfs_silviculture_reforestation_enriched_20220629_2_, output_standardized_copy)

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
        usfs_silviculture_reforestation_enriched_20220629_3_ = AssignDomains(in_table=output_enriched)

        print('Deleting Scratch Files')
        delete_scratch_files(gdb = scratch_workspace, delete_fc = 'yes', delete_table = 'yes', delete_ds = 'yes')
        end = time.time()
        print(f'Time Elapsed: {(end-start)/60} minutes')
if __name__ == '__main__':
     runner(workspace,scratch_workspace,Model72, '*argv[1:]')
    # # Global Environment settings
    #  with arcpy.EnvManager(
    # extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""",  outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""", 
    # preserveGlobalIds=True, 
    # qualifiedFieldNames=False, 
    # scratchWorkspace=scratch_workspace, 
    # transferDomains=True, 
    # transferGDBAttributeProperties=True, 
    # workspace=workspace):
    #     Model72(*argv[1:])
