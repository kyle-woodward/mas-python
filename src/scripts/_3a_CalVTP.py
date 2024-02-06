"""
# Description: Converts the California Board of Forestry and Fire Protection's 
#              Vegetation Treatment Program (CalVTP) dataset 
#              into the Task Force standardized schema.  Dataset
#              is enriched with vegetation, ownership, county, WUI, 
#              Task Force Region, and year.            
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import arcpy
from scripts._1_add_fields import AddFields
from scripts._1_assign_domains import AssignDomains
from scripts._3_enrichments_polygon import enrich_polygons
from scripts.utils import  init_gdb

workspace, scratch_workspace = init_gdb()

def CalVTP(CalVTP_enriched,
           CalVTP_standardized,
           CalVTP_OG
           ):

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

        # scratch outputs
        CALVTP_select_2 = os.path.join(scratch_workspace, 'CALVTP_Copy') 
        CalVTP_enriched_scratch = os.path.join(scratch_workspace, 'CalVTP_enriched_scratch')

        # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
        print("step 1/30 select layer by attribute...")
        CalVTP_select = arcpy.management.SelectLayerByAttribute(in_layer_or_view=CalVTP_OG, 
                                                                            where_clause="Affiliation = 'non-CAL FIRE'")

        # Process: Select (Select) (analysis)
        print("step 2/30 select...")
        arcpy.analysis.Select(in_features=CalVTP_select, 
                            out_feature_class=CALVTP_select_2, 
                            where_clause="DATE_COMPLETED IS NOT NULL")

        # Process: Repair Geometry (Repair Geometry) (management)
        print("step 3/30 repair geometry...")
        CALVTP_repair_geom = arcpy.management.RepairGeometry(in_features=CALVTP_select_2, 
                                                        delete_null="KEEP_NULL")

        # Process: Alter Field (Alter Field) (management)
        print("step 4/30 alter field...")
        CALVTP_alter_field = arcpy.management.AlterField(in_table=CALVTP_repair_geom, 
                                                field="County", 
                                                new_field_name="County_")

        # Process: 1b Add Fields (1b Add Fields) 
        print("step 5/30 add fields...")
        CalVTP_add_fields = AddFields(Input_Table=CALVTP_alter_field)

        # Process: Calculate Project User ID (Calculate Field) (management)
        print("step 6/30 calculate field...")
        CALVTP_calc_proj_user_id = arcpy.management.CalculateField(in_table=CalVTP_add_fields, 
                                                                    field="PROJECTID_USER", 
                                                                    expression="!PROJECT_ID!")

        # Process: Calculate Agency (Calculate Field) (management)
        print("step 7/30 calculate field...")
        CalVTP_calc_agency = arcpy.management.CalculateField(in_table=CALVTP_calc_proj_user_id, 
                                                                field="AGENCY", 
                                                                expression="\"CNRA\"")

        # Process: Calculate Org Steward (Calculate Field) (management)
        print("step 8/30 calculate field...")
        CalVTP_calc_org_stew = arcpy.management.CalculateField(in_table=CalVTP_calc_agency, 
                                                                field="ORG_ADMIN_p", 
                                                                expression="\"BOF\"")

        # Process: Calculate Prj Contact (Calculate Field) (management)
        print("step 9/30 calculate field...")
        CalVTP_calc_proj_contact = arcpy.management.CalculateField(in_table=CalVTP_calc_org_stew, 
                                                                field="PROJECT_CONTACT", 
                                                                expression="\"Kristina Wolf\"")

        # Process: Calculate Prj Email (Calculate Field) (management)
        print("step 10/30 calculate field...")
        CALVTP_calc_proj_email = arcpy.management.CalculateField(in_table=CalVTP_calc_proj_contact, 
                                                        field="PROJECT_EMAIL", 
                                                        expression="\"Kristina.Wolf@bof.ca.gov\"")

        # Process: Calculate Admin Org (Calculate Field) (management)
        print("step 11/30 calculate field...")
        CalVTP_calc_admin_org = arcpy.management.CalculateField(in_table=CALVTP_calc_proj_email, 
                                                                field="ADMINISTERING_ORG", 
                                                                expression="\"BOF\"")

        # Process: Calculate Primary Funding Source (Calculate Field) (management)
        print("step 12/30 calculate field...")
        CalVTP_calc_prim_fund_src = arcpy.management.CalculateField(in_table=CalVTP_calc_admin_org, 
                                                                field="PRIMARY_FUNDING_SOURCE", 
                                                                expression="ifelse(!GRANT_TYPE!)", 
                                                                code_block="""def ifelse(Fund):
        if Fund == \"1\":
            return \"CAL FIRE Forest Health\"
        elif Fund == \"CAL FIRE Forest Health Grant\":
            return \"CAL FIRE Forest Health\"    
        elif Fund == \"2\":
            return \"CAL FIRE Fire Prevention\"
        elif Fund == \"3\":
            return \"CAL FIRE Urban Forestry\"
        else:
            return Fund""")

        # Process: Calculate Primary Funding Org (Calculate Field) (management)
        print("step 13/30 calculate field...")
        CalVTP_calc_prim_fund_org = arcpy.management.CalculateField(in_table=CalVTP_calc_prim_fund_src, 
                                                                field="PRIMARY_FUNDING_ORG", 
                                                                expression="\"BOF\"")

        # Process: Calculate Objective (Calculate Field) (management)
        print("step 14/30 calculate field...")
        CalVTP_calc_obj = arcpy.management.CalculateField(in_table=CalVTP_calc_prim_fund_org, 
                                                                field="PRIMARY_OBJECTIVE", 
                                                                expression="elseif(!Treatment_Type!)", 
                                                                code_block="""def elseif(Treat):
        if Treat == \"1\":
            return \"FUEL_BREAK\"
        elif Treat == \"2\":
            return \"FUEL_BREAK\"
        elif Treat == \"3\":
            return \"ECO_RESTOR\"
        else:
            return Treat""")

        # Process: Calculate Implementing Org (Calculate Field) (management)
        print("step 15/30 calculate field...")
        CalVTP_calc_imp_org = arcpy.management.CalculateField(in_table=CalVTP_calc_obj, 
                                                                field="IMPLEMENTING_ORG", 
                                                                expression="\"BOF\"")

        # Process: Calculate Geometry Attributes (Calculate Geometry Attributes) (management)
        print("step 16/30 calculkate geometry attributes...")
        CALVTP_calc_geom_att = arcpy.management.CalculateGeometryAttributes(in_features=CalVTP_calc_imp_org, 
                                                                    geometry_property=[["LATITUDE", "INSIDE_Y"], ["LONGITUDE", "INSIDE_X"]], 
                                                                    coordinate_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", 
                                                                    coordinate_format="DD")

        # Process: Calculate Geometry Attributes (2) (Calculate Geometry Attributes) (management)
        print("step 17/30 calculate geometry attributes...")
        CALVTP_calc_geom_att_2 = arcpy.management.CalculateGeometryAttributes(in_features=CALVTP_calc_geom_att, 
                                                                    geometry_property=[["TREATMENT_AREA", "AREA"]], 
                                                                    area_unit="ACRES_US")

        # Process: Calculate Veg (Calculate Field) (management)
        print("step 18/30 calculate field...")
        CalVTP_calc_veg = arcpy.management.CalculateField(in_table=CALVTP_calc_geom_att_2, 
                                                            field="BROAD_VEGETATION_TYPE", 
                                                            expression="ifelse(!Fuel_Type!)", 
                                                            code_block="""def ifelse(Veg):
        if Veg == \"1\":
            return \"GRASS_HERB\"
        elif Veg == \"2\":
            return \"SHRB_CHAP\"
        elif Veg == \"3\":
            return \"FOREST\"
        else:
            return Veg""")

        # Process: Calculate Activity Status (Calculate Field) (management)
        print("step 19/30 calculate field...")
        CalVTP_calc_act_stat = arcpy.management.CalculateField(in_table=CalVTP_calc_veg, 
                                                                field="ACTIVITY_STATUS", 
                                                                expression="ifelse(!Status!)", 
                                                                code_block="""def ifelse(Status):
        if Status == \"1\":
            return \"PLANNED\"
        elif Status == \"2\":
            return \"ACTIVE\"
        elif Status == \"3\":
            return \"COMPLETE\"
        elif Status == \"4\":
            return \"PROPOSED\"
        else:
            return Status""")

        # Process: Calculate Activity Quantity (Calculate Field) (management)
        print("step 20/30 calculate field...")
        CalVTP_calc_act_quant = arcpy.management.CalculateField(in_table=CalVTP_calc_act_stat, 
                                                                field="ACTIVITY_QUANTITY", 
                                                                expression="!Treatment_Acres!")

        # Process: Calculate Activity Units (Calculate Field) (management)
        print("step 21/30 calculate field...")
        CalVTP_calc_act_units = arcpy.management.CalculateField(in_table=CalVTP_calc_act_quant, 
                                                                field="ACTIVITY_UOM", 
                                                                expression="\"AC\"")

        # Process: Calculate Activity end (Calculate Field) (management)
        print("step 22/30 calculate field...")
        CalVTP_calc_act_end = arcpy.management.CalculateField(in_table=CalVTP_calc_act_units, 
                                                                field="ACTIVITY_END", 
                                                                expression="!DATE_COMPLETED!")

        # Process: Calculate Source (Calculate Field) (management)
        print("step 23/30 calculate field...")
        CALVTP_calc_src = arcpy.management.CalculateField(in_table=CalVTP_calc_act_end, 
                                                        field="Source", 
                                                        expression="\"calvtp\"")

        # Process: Calculate Crosswalk (Calculate Field) (management)
        print("step 24/30 calculate field...")
        CalVTP_calc_xwalk = arcpy.management.CalculateField(in_table=CALVTP_calc_src, 
                                                                field="Crosswalk", 
                                                                expression="ifelse(!TREATMENT_ACTIVITY!)", 
                                                                code_block="""def ifelse(Act):
        if Act == \"1\":
            return \"Prescribed Fire (Broadcast)\"
        elif Act == \"2\":
            return \"Prescribed Fire (Pile Burning)\"
        elif Act == \"3\":
            return \"Mechanical Treatment\"
        elif Act == \"4\":
            return \"Manual Treatment\"
        else:
            return Act
        """)

        # Process: Copy Features (2) (Copy Features) (management)
        print("step 25/30 copy features...")
        arcpy.management.CopyFeatures(in_features=CalVTP_calc_xwalk, 
                                    out_feature_class=CalVTP_standardized)

        # Process: 2b Assign Domains (2b Assign Domains) 
        print("step 26/30 assign domains...")
        CalVTP_Standardized = AssignDomains(in_table=CalVTP_standardized)

        # Process: 7a Enrichments Polygon (7a Enrichments Polygon) 
        print("step 27/30 enrich polygons...")
        enrich_polygons(enrich_out=CalVTP_enriched_scratch, 
                                enrich_in=CalVTP_Standardized)

        # Process: Copy Features (3) (Copy Features) (management)
        print("step 28/30 copy features...")
        arcpy.management.CopyFeatures(in_features=CalVTP_enriched_scratch, 
                                    out_feature_class=CalVTP_enriched)

        # Process: Calculate Treatment ID (Calculate Field) (management)
        print("step 29/30 calculate field...")
        Updated_Input_Table_6_ = arcpy.management.CalculateField(in_table=CalVTP_enriched, 
                                                                field="TRMTID_USER", 
                                                                expression="!PROJECTID_USER![:7]+'-'+(!IN_WUI![:3])+'-'+(!PRIMARY_OWNERSHIP_GROUP![:1])")

        # Process: 2b Assign Domains (2) (2b Assign Domains) 
        print("step 30/30 assign domains...")
        CalVTP_Enriched = AssignDomains(in_table=Updated_Input_Table_6_)

        print("6y complete...")

        #delete_scratch_files(gdb = scratch_workspace, delete_fc = 'yes', delete_table = 'yes', delete_ds = 'yes')

