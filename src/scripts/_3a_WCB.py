"""
# Description: Converts the California Department of Natural Resources,
#              Wildlife Conservation Board's fuels treatments dataset 
#              into the Task Force standardized schema.  Dataset
#              is enriched with vegetation, ownership, county, WUI, 
#              Task Force Region, and year.              
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import datetime
import arcpy
from scripts._1_add_fields import AddFields
from scripts._1_assign_domains import AssignDomains
from scripts._3_enrichments_polygon import enrich_polygons
from scripts.utils import init_gdb

original_gdb, workspace, scratch_workspace = init_gdb()

def WCB(WCB_standardized, WCB_OG): 

    date_id = datetime.datetime.now().strftime("%Y-%m-%d").replace('-','')

    # scratch outputs
    WCB_CopyFeatures = os.path.join(scratch_workspace, 'WCB_CopyFeatures')
    WCB_Dissolve = os.path.join(scratch_workspace, 'WCB_Dissolve') 
    WCB_enriched_scratch = os.path.join(scratch_workspace, 'WCB_enriched_scratch') 

    # workspace outputs
    WCB_enriched = os.path.join(workspace, 'd_Enriched', f'WCB_enriched_{date_id}') 

    # Model Environment settings
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

        # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
        print("Executing Step 1/34 : Select Layer by Attribute...")
        WCB_select = arcpy.management.SelectLayerByAttribute(in_layer_or_view=WCB_OG, 
                                                                             where_clause="Function = 'Disposal/Sale' Or Function = 'Other (Plan, Study, Etc.)' Or Function = 'Infrastructure' Or Function = 'Lease' Or Function = 'Public Access' Or Function = 'Transfer of Control'", 
                                                                             invert_where_clause="INVERT")

        # Process: Select Layer By Attribute (2) (Select Layer By Attribute) (management)
        print("Executing Step 2/34 : Select Layer by Attribute...")
        WCB_select_2 = arcpy.management.SelectLayerByAttribute(in_layer_or_view=WCB_select, 
                                                                                  selection_type="SUBSET_SELECTION", 
                                                                                  where_clause="dtmBoardAp >= timestamp '1995-01-01 00:00:00'")

        # Process: Copy Features (2) (Copy Features) (management)
        print("Executing Step 3/34 : Copy Features...")
        arcpy.management.CopyFeatures(in_features=WCB_select_2, 
                                      out_feature_class=WCB_CopyFeatures)

        # Process: Dissolve (Dissolve) (management)
        print("Executing Step 4/34 : Dissolve...")
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
        print("Executing Step 5/34 : Repair Geometry...")
        WCB_Dissolve_repair_geom = arcpy.management.RepairGeometry(in_features=WCB_Dissolve, 
                                                                delete_null="KEEP_NULL")

        # Process: Alter Field (Alter Field) (management)
        print("Executing Step 6/34 : Alter Field...")
        WCB_Dissolve_alter_field = arcpy.management.AlterField(in_table=WCB_Dissolve_repair_geom, 
                                                               field="ProjectID", 
                                                               new_field_name="ProjectID2")

        # Process: Alter Field (2) (Alter Field) (management)
        print("Executing Step 7/34 : Alter Field...")
        WCB_Dissolve_alter_field_2 = arcpy.management.AlterField(in_table=WCB_Dissolve_alter_field, 
                                                               field="County", 
                                                               new_field_name="County_")

        # Process: 1b Add Fields (1b Add Fields)
        print("Executing Step 8/34 : Add Fields...")
        WCB_add_fields = AddFields(Input_Table=WCB_Dissolve_alter_field_2)

        # Process: Calculate Project ID User (Calculate Field) (management)
        print("Executing Step 9/34 : Calculate PROJECTID_USER...")
        WCB_calc_proj_id_user = arcpy.management.CalculateField(in_table=WCB_add_fields, 
                                                              field="PROJECTID_USER", 
                                                              expression="!ProjectID2!")

        # Process: Calculate Treatment ID User (Calculate Field) (management)
        print("Executing Step 10/34 : Calculate TRMTID_USER...")
        WCB_calc_treat_id_user = arcpy.management.CalculateField(in_table=WCB_calc_proj_id_user, 
                                                                    field="TRMTID_USER", 
                                                                    expression="!PROJECTID_USER!")#+'-'+!PRIMARY_OWNERSHIP_GROUP![:4]")#+'-'+!IN_WUI![:3]")

        # Process: Calculate Agency (Calculate Field) (management)
        print("Executing Step 11/34 : Calculate AGENCY...")
        WCB_calc_agency = arcpy.management.CalculateField(in_table=WCB_calc_treat_id_user,
                                                                  field="AGENCY", 
                                                                  expression="\"CNRA\"")

        # Process: Calculate Project Contact (Calculate Field) (management)
        print("Executing Step 12/34 : Calculate PROJECT_CONTACT...")
        WCB_calc_proj_contact = arcpy.management.CalculateField(in_table=WCB_calc_agency, 
                                                                  field="PROJECT_CONTACT", 
                                                                  expression="\"Scott McFarlin\"")

        # Process: Calculate Project Email (Calculate Field) (management)
        print("Executing Step 13/34 : Calculate PROJECT_EMAIL...")
        WCB_calc_proj_email = arcpy.management.CalculateField(in_table=WCB_calc_proj_contact, 
                                                                  field="PROJECT_EMAIL", 
                                                                  expression="\"Scott.McFarlin@wildlife.ca.gov\"")

        # Process: Calculate Admin Org (Calculate Field) (management)
        print("Executing Step 14/34 : Calculate ADMINISTERING_ORG...")
        WCB_calc_admin_org = arcpy.management.CalculateField(in_table=WCB_calc_proj_email, 
                                                                  field="ADMINISTERING_ORG", 
                                                                  expression="\"WCB\"")

        # Process: Calculate Project Name (Calculate Field) (management)
        print("Executing Step 15/34 : PROJECT_NAME...")
        WCB_calc_proj_name = arcpy.management.CalculateField(in_table=WCB_calc_admin_org, 
                                                                 field="PROJECT_NAME", 
                                                                 expression="!ProjName!")

        # Process: Calculate Project Start (Calculate Field) (management)
        print("Executing Step 16/34 : Calculate PROJECT_START...")
        WCB_calc_proj_start = arcpy.management.CalculateField(in_table=WCB_calc_proj_name, 
                                                                 field="PROJECT_START", 
                                                                 expression="!dtmBoardAp!")

        # Process: Calculate Primary Objective (Calculate Field) (management)
        print("Executing Step 17/34 : Calculate PRIMARY_OBJECTIVE...")
        WCB_calc_prim_obj = arcpy.management.CalculateField(in_table=WCB_calc_proj_start, 
                                                                 field="PRIMARY_OBJECTIVE", 
                                                                 expression="!PrimPurp!")

        # Process: Calculate Secondary Objective (Calculate Field) (management)
        print("Executing Step 18/34 : Calculate SECONDARY_OBJECTIVE...")
        WCB_calc_sec_obj = arcpy.management.CalculateField(in_table=WCB_calc_prim_obj, 
                                                                 field="SECONDARY_OBJECTIVE", 
                                                                 expression="!Type!")

        # Process: Calculate Tertiary Objective (Calculate Field) (management)
        print("Executing Step 19/34 : Calculate TERTIARY_OBJECTIVE...")
        WCB_calc_tert_obj = arcpy.management.CalculateField(in_table=WCB_calc_sec_obj, 
                                                                 field="TERTIARY_OBJECTIVE", 
                                                                 expression="!Function!", 
                                                                 enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Primary Funding Source (Calculate Field) (management)
        print("Executing Step 20/34 : Calculate PRIMARY_FUNDING_SOURCE...")
        WCB_calc_prim_fund_src = arcpy.management.CalculateField(in_table=WCB_calc_tert_obj, 
                                                                 field="PRIMARY_FUNDING_SOURCE", 
                                                                 expression="!Program!", 
                                                                 enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Activity Acres (Calculate Field) (management)
        print("Executing Step 21/34 : Calculate ACTIVITY_QUANTITY...")
        WCB_calc_act_ac = arcpy.management.CalculateField(in_table=WCB_calc_prim_fund_src, 
                                                                 field="ACTIVITY_QUANTITY", 
                                                                 expression="!TotalAcres!")

        # Process: Calculate UOM (Calculate Field) (management)
        print("Executing Step 22/34 : Calculate ACTIVITY_UOM...")
        WCB_calc_uom = arcpy.management.CalculateField(in_table=WCB_calc_act_ac, 
                                                                  field="ACTIVITY_UOM", 
                                                                  expression="\"AC\"")

        # Process: Calculate Activity End Date (Calculate Field) (management)
        print("Executing Step 23/34 : Calculate ACTIVITY_END...")
        WCB_calc_act_end_date = arcpy.management.CalculateField(in_table=WCB_calc_uom, 
                                                                  field="ACTIVITY_END", 
                                                                  expression="!dtmBoardAp!")

        # Process: Calculate Activity Status (Calculate Field) (management)
        print("Executing Step 24/34 : Calculate ACTIVITY_STATUS...")
        WCB_calc_act_stat = arcpy.management.CalculateField(in_table=WCB_calc_act_end_date, 
                                                                   field="ACTIVITY_STATUS", 
                                                                   expression="\"ACTIVE\"")

        # Process: Calculate Implementing Org (Calculate Field) (management)
        print("Executing Step 25/34 : Calculate IMPLEM_ORG_NAME...")
        WCB_calc_imp_org = arcpy.management.CalculateField(in_table=WCB_calc_act_stat, 
                                                                 field="IMPLEM_ORG_NAME", 
                                                                 expression="!PrimGrante!")

        # Process: Calculate Source (Calculate Field) (management)
        print("Executing Step 26/34 : Calculate Source...")
        WCB_calc_src = arcpy.management.CalculateField(in_table=WCB_calc_imp_org, 
                                                            field="Source", 
                                                            expression="\"WCB\"")

        # Process: Calculate Crosswalk (Calculate Field) (management)
        print("Executing Step 27/34 : Calculate Crosswalk...")
        WCB_calc_xwalk = arcpy.management.CalculateField(in_table=WCB_calc_src, 
                                                                  field="Crosswalk", 
                                                                  expression="!Function! + \" \" + !PrimPurp!")

        # Process: Calculate Year (Calculate Field) (management)
        print("Executing Step 28/34 : Calculate Year...")
        WCB_calc_year = arcpy.management.CalculateField(in_table=WCB_calc_xwalk, 
                                                                  field="Year", 
                                                                  expression="Year($feature.dtmBoardAp)", 
                                                                  expression_type="ARCADE")

        # Process: Copy Features (Copy Features) (management)
        print("Executing Step 29/34 : Copy Features...")
        arcpy.management.CopyFeatures(in_features=WCB_calc_year, 
                                      out_feature_class=WCB_standardized.__str__().format(**locals(),**globals()))
        
        WCB_standardized_keep_fields = KeepFields(WCB_standardized.__str__().format(**locals(),**globals()))

        # Process: 2b Assign Domains (2b Assign Domains)
        print("Executing Step 30/34 : AssignDomains to standardized...")
        WCB_w_domains = AssignDomains(in_table=WCB_standardized_keep_fields)

        # Process: 7a Enrichments Polygon (7a Enrichments Polygon)
        print("Executing Step 31/34 : Enrich Polygons...")
        enrich_polygons(enrich_out=WCB_enriched_scratch, 
                             enrich_in=WCB_w_domains)

        # Process: Select Layer By Attribute (3) (Select Layer By Attribute) (management)
        print("Executing Step 32/34 : Select Layer by Attribute...")
        WCB_enriched_scratch_select = arcpy.management.SelectLayerByAttribute(in_layer_or_view=WCB_enriched_scratch, 
                                                                                         where_clause="ACTIVITY_DESCRIPTION <> 'NOT_DEFINED'")

        # Process: Copy Features (3) (Copy Features) (management)
        print("Executing Step 33/34 : Copy Features...")
        arcpy.management.CopyFeatures(in_features=WCB_enriched_scratch_select, 
                                      out_feature_class=WCB_enriched)

        # Process: 2b Assign Domains (2) (2b Assign Domains)
        print("Executing Step 34/34 : AssignDomains to enriched...")
        WFR_TF_Template_4_ = AssignDomains(in_table=WCB_enriched)

        #delete_scratch_files(gdb = scratch_workspace, delete_fc = 'yes', delete_table = 'yes', delete_ds = 'yes')
