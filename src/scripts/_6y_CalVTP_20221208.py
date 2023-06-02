"""
"""
import arcpy
from scripts._1b_add_fields import AddFields2
from scripts._2b_assign_domains import AssignDomains
from scripts._7a_enrichments_polygon import aEnrichmentsPolygon1
from scripts.utils import runner, init_gdb
from sys import argv
import os
original_gdb, workspace, scratch_workspace = init_gdb()

def CalVTP(CalVTP_enriched,
           CalVTP_standardized,
           CalVTP_OG):
    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

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
                                                     delete_null="KEEP_NULL")[0]

    # Process: Alter Field (Alter Field) (management)
    print("step 4/30 alter field...")
    CALVTP_alter_field = arcpy.management.AlterField(in_table=CALVTP_repair_geom, 
                                              field="County", 
                                              new_field_name="County_")[0]

    # Process: 1b Add Fields (1b Add Fields) (PC414CWIMillionAcres)
    print("step 5/30 add fields...")
    CalVTP_add_fields = AddFields2(Input_Table=CALVTP_alter_field)

    # Process: Calculate Project User ID (Calculate Field) (management)
    print("step 6/30 calculate field...")
    CALVTP_calc_proj_user_id = arcpy.management.CalculateField(in_table=CalVTP_add_fields, 
                                                                   field="PROJECTID_USER", 
                                                                   expression="!PROJECT_ID!")[0]

    # Process: Calculate Agency (Calculate Field) (management)
    print("step 7/30 calculate field...")
    CalVTP_calc_agency = arcpy.management.CalculateField(in_table=CALVTP_calc_proj_user_id, 
                                                              field="AGENCY", 
                                                              expression="\"CNRA\"")[0]

    # Process: Calculate Org Steward (Calculate Field) (management)
    print("step 8/30 calculate field...")
    CalVTP_calc_org_stew = arcpy.management.CalculateField(in_table=CalVTP_calc_agency, 
                                                              field="ORG_ADMIN_p", 
                                                              expression="\"BOF\"")[0]

    # Process: Calculate Prj Contact (Calculate Field) (management)
    print("step 9/30 calculate field...")
    CalVTP_calc_proj_contact = arcpy.management.CalculateField(in_table=CalVTP_calc_org_stew, 
                                                              field="PROJECT_CONTACT", 
                                                              expression="\"Kristina Wolf\"")[0]

    # Process: Calculate Prj Email (Calculate Field) (management)
    print("step 10/30 calculate field...")
    CALVTP_calc_proj_email = arcpy.management.CalculateField(in_table=CalVTP_calc_proj_contact, 
                                                     field="PROJECT_EMAIL", 
                                                     expression="\"Kristina.Wolf@bof.ca.gov\"")[0]

    # Process: Calculate Admin Org (Calculate Field) (management)
    print("step 11/30 calculate field...")
    CalVTP_calc_admin_org = arcpy.management.CalculateField(in_table=CALVTP_calc_proj_email, 
                                                              field="ADMINISTERING_ORG", 
                                                              expression="\"BOF\"")[0]

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
        return Fund""")[0]

    # Process: Calculate Primary Funding Org (Calculate Field) (management)
    print("step 13/30 calculate field...")
    CalVTP_calc_prim_fund_org = arcpy.management.CalculateField(in_table=CalVTP_calc_prim_fund_src, 
                                                              field="PRIMARY_FUNDING_ORG", 
                                                              expression="\"BOF\"")[0]

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
        return Treat""")[0]

    # Process: Calculate Implementing Org (Calculate Field) (management)
    print("step 15/30 calculate field...")
    CalVTP_calc_imp_org = arcpy.management.CalculateField(in_table=CalVTP_calc_obj, 
                                                              field="IMPLEMENTING_ORG", 
                                                              expression="\"BOF\"")[0]

    # Process: Calculate Geometry Attributes (Calculate Geometry Attributes) (management)
    print("step 16/30 calculkate geometry attributes...")
    CALVTP_calc_geom_att = arcpy.management.CalculateGeometryAttributes(in_features=CalVTP_calc_imp_org, 
                                                                  geometry_property=[["LATITUDE", "INSIDE_Y"], ["LONGITUDE", "INSIDE_X"]], 
                                                                  coordinate_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", 
                                                                  coordinate_format="DD")[0]

    # Process: Calculate Geometry Attributes (2) (Calculate Geometry Attributes) (management)
    print("step 17/30 calculate geometry attributes...")
    CALVTP_calc_geom_att_2 = arcpy.management.CalculateGeometryAttributes(in_features=CALVTP_calc_geom_att, 
                                                                  geometry_property=[["TREATMENT_AREA", "AREA"]], 
                                                                  area_unit="ACRES_US")[0]

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
        return Veg""")[0]

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
        return Status""")[0]

    # Process: Calculate Activity Quantity (Calculate Field) (management)
    print("step 20/30 calculate field...")
    CalVTP_calc_act_quant = arcpy.management.CalculateField(in_table=CalVTP_calc_act_stat, 
                                                             field="ACTIVITY_QUANTITY", 
                                                             expression="!Treatment_Acres!")[0]

    # Process: Calculate Activity Units (Calculate Field) (management)
    print("step 21/30 calculate field...")
    CalVTP_calc_act_units = arcpy.management.CalculateField(in_table=CalVTP_calc_act_quant, 
                                                             field="ACTIVITY_UOM", 
                                                             expression="\"AC\"")[0]

    # Process: Calculate Activity end (Calculate Field) (management)
    print("step 22/30 calculate field...")
    CalVTP_calc_act_end = arcpy.management.CalculateField(in_table=CalVTP_calc_act_units, 
                                                             field="ACTIVITY_END", 
                                                             expression="!DATE_COMPLETED!")[0]

    # Process: Calculate Source (Calculate Field) (management)
    print("step 23/30 calculate field...")
    CALVTP_calc_src = arcpy.management.CalculateField(in_table=CalVTP_calc_act_end, 
                                                     field="Source", 
                                                     expression="\"calvtp\"")[0]

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
    """)[0]

    # Process: Copy Features (2) (Copy Features) (management)
    print("step 25/30 copy features...")
    arcpy.management.CopyFeatures(in_features=CalVTP_calc_xwalk, 
                                  out_feature_class=CalVTP_standardized.__str__().format(**locals(),**globals()))

    # Process: 2b Assign Domains (2b Assign Domains) (PC414CWIMillionAcres)
    print("step 26/30 assign domains...")
    CalVTP_Standardized = AssignDomains(in_table=CalVTP_standardized.__str__().format(**locals(),**globals()))[0]

    # Process: 7a Enrichments Polygon (7a Enrichments Polygon) (PC414CWIMillionAcres)
    print("step 27/30 enrich polygons...")
    aEnrichmentsPolygon1(enrich_out=CalVTP_enriched_scratch, 
                         enrich_in=CalVTP_Standardized)

    # Process: Copy Features (3) (Copy Features) (management)
    print("step 28/30 copy features...")
    arcpy.management.CopyFeatures(in_features=CalVTP_enriched_scratch, 
                                  out_feature_class=CalVTP_enriched.__str__().format(**locals(),**globals()))

    # Process: Calculate Treatment ID (Calculate Field) (management)
    print("step 29/30 calculate field...")
    Updated_Input_Table_6_ = arcpy.management.CalculateField(in_table=CalVTP_enriched.__str__().format(**locals(),**globals()), 
                                                             field="TRMTID_USER", 
                                                             expression="!PROJECTID_USER![:7]+'-'+(!IN_WUI![:3])+'-'+(!PRIMARY_OWNERSHIP_GROUP![:1])")[0]

    # Process: 2b Assign Domains (2) (2b Assign Domains) (PC414CWIMillionAcres)
    print("step 30/30 assign domains...")
    CalVTP_Enriched = AssignDomains(in_table=Updated_Input_Table_6_)[0]

    print("6y complete...")

    #delete_scratch_files(gdb = scratch_workspace, delete_fc = 'yes', delete_table = 'yes', delete_ds = 'yes')

if __name__ == '__main__':
    runner(workspace,scratch_workspace,CalVTP, '*argv[1:]')
    # # Global Environment settings
    # with arcpy.EnvManager(extent="-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", outputCoordinateSystem="PROJCS[\"NAD_1983_California_Teale_Albers\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Albers\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",-4000000.0],PARAMETER[\"Central_Meridian\",-120.0],PARAMETER[\"Standard_Parallel_1\",34.0],PARAMETER[\"Standard_Parallel_2\",40.5],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]", preserveGlobalIds=True, 
    #                       qualifiedFieldNames=False, scratchWorkspace="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb", transferGDBAttributeProperties=True, 
    #                       workspace="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb"):
    #     CalVTP(*argv[1:])
