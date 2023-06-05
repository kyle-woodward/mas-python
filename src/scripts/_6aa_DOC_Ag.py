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

def DOC6(DOC_Ag_Standardized, 
            DOC_Ag_enriched,
            DOC_Ag_OG):  

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    # # Model Environment settings
    # with arcpy.EnvManager(qualifiedFieldNames=False, transferDomains=False, transferGDBAttributeProperties=False):
    #     DOC_Ag_easements_Range2022 = os.path.join(workspace, "a_Originals", "DOC_Ag_easements_Range2022")

    #scratch outputs
    DOC_Ag_OG_Dissolve = os.path.join(scratch_workspace, "DOC_Ag_OG_Dissolve")
    DOC_Summarized_Polygons = os.path.join(scratch_workspace, "DOC_Summarized_Polygons")

    with arcpy.EnvManager(qualifiedFieldNames=False, transferDomains=False, transferGDBAttributeProperties=False): 
        # Process: Dissolve (Dissolve) (management)
        arcpy.management.Dissolve(in_features=DOC_Ag_OG, 
                                  out_feature_class=DOC_Ag_OG_Dissolve, 
                                  dissolve_field=["ACRES", 
                                                  "FUNDER1", 
                                                  "FUNDER2", 
                                                  "FUNDER3", 
                                                  "HOLDER", 
                                                  "PROJECT", 
                                                  "PROVIDER", 
                                                  "Grant_Nm", 
                                                  "ClosingDat"])

        # Process: Repair Geometry (Repair Geometry) (management)
        DOC_Repaired_Geometry = arcpy.management.RepairGeometry(in_features=DOC_Ag_OG_Dissolve)

        # Process: 1b Add Fields (1b Add Fields) (PC414CWIMillionAcres)
        DOC_w_Fields = AddFields(Input_Table=DOC_Repaired_Geometry)

        # Process: Calculate Project ID (Calculate Field) (management)
        DOC_calc_proj_id = arcpy.management.CalculateField(in_table=DOC_w_Fields, 
                                                                  field="PROJECTID_USER", 
                                                                  expression="!Grant_Nm!")

        # Process: Calculate Agency (Calculate Field) (management)
        DOC_calc_agency = arcpy.management.CalculateField(in_table=DOC_calc_proj_id, 
                                                                  field="AGENCY", 
                                                                  expression="\"CNRA\"")

        # Process: Calculate Administering Org (Calculate Field) (management)
        DOC_calc_admin_org = arcpy.management.CalculateField(in_table=DOC_calc_agency, 
                                                                 field="ADMINISTERING_ORG", 
                                                                 expression="\"DOC\"")

        # Process: Calculate Project Name (Calculate Field) (management)
        DOC_calc_proj_name = arcpy.management.CalculateField(in_table=DOC_calc_admin_org, 
                                                                 field="PROJECT_NAME", 
                                                                 expression="!PROJECT!")

        # Process: Calculate Implementing Org (Calculate Field) (management)
        DOC_calc_imp_org = arcpy.management.CalculateField(in_table=DOC_calc_proj_name, 
                                                                  field="IMPLEMENTING_ORG", 
                                                                  expression="!HOLDER!")

        # Process: Calculate Treatment ID (Calculate Field) (management)
        DOC_calc_treat_id = arcpy.management.CalculateField(in_table=DOC_calc_imp_org, 
                                                                  field="TRMTID_USER", 
                                                                  expression="!Grant_Nm! + '-' + !PROJECT![:12]+'-'+!PRIMARY_OWNERSHIP_GROUP![:11]+'-'+!IN_WUI![:3]")

        # Process: Calculate BVT (Calculate Field) (management)
        DOC_calc_bvt = arcpy.management.CalculateField(in_table=DOC_calc_treat_id, 
                                                                  field="BVT_USERD", 
                                                                  expression="\"NO\"")

        # Process: Calculate Activity Status (Calculate Field) (management)
        DOC_calc_act_stat = arcpy.management.CalculateField(in_table=DOC_calc_bvt, 
                                                                  field="ACTIVITY_STATUS", 
                                                                  expression="\"ACTIVE\"")

        # Process: Calculate Activity Quantity (Calculate Field) (management)
        DOC_calc_act_quant = arcpy.management.CalculateField(in_table=DOC_calc_act_stat, 
                                                              field="ACTIVITY_QUANTITY", 
                                                              expression="!ACRES!")

        # Process: Calculate UOM (Calculate Field) (management)
        DOC_calc_uom = arcpy.management.CalculateField(in_table=DOC_calc_act_quant, 
                                                                 field="ACTIVITY_UOM", 
                                                                 expression="\"AC\"")

        # Process: Calculate Activity End (Calculate Field) (management)
        DOC_calc_act_end = arcpy.management.CalculateField(in_table=DOC_calc_uom, 
                                                                  field="ACTIVITY_END", 
                                                                  expression="!ClosingDat!")
        
        # Process: Calculate Primary Funding Org (Calculate Field) (management)
        DOC_calc_prim_fund_org = arcpy.management.CalculateField(in_table=DOC_calc_act_end, 
                                                                 field="PRIMARY_FUND_ORG_NAME", 
                                                                 expression="!PROVIDER!")

        # Process: Calculate Primary Funding Source (Calculate Field) (management)
        DOC_calc_prim_fund_src = arcpy.management.CalculateField(in_table=DOC_calc_prim_fund_org, 
                                                                 field="PRIMARY_FUND_SRC_NAME", 
                                                                 expression="!FUNDER1!")

        # Process: Calculate SecondaryFunding Src Name (Calculate Field) (management)
        DOC_calc_sec_fund_src_name = arcpy.management.CalculateField(in_table=DOC_calc_prim_fund_src, 
                                                                 field="SECONDARY_FUND_SRC_NAME", 
                                                                 expression="!FUNDER2!")

        # Process: Calculate Tertiary Funding Src Name (Calculate Field) (management)
        DOC_calc_tert_fund_src_name = arcpy.management.CalculateField(in_table=DOC_calc_sec_fund_src_name, 
                                                                  field="TERTIARY_FUND_SRC_NAME", 
                                                                  expression="!FUNDER3!")

        # Process: Calculate Crosswalk (Calculate Field) (management)
        DOC_calc_xwalk = arcpy.management.CalculateField(in_table=DOC_calc_tert_fund_src_name, 
                                                                  field="Crosswalk", 
                                                                  expression="\"EASEMENT\"")

        # Process: Calculate Source (Calculate Field) (management)
        DOC_calc_src = arcpy.management.CalculateField(in_table=DOC_calc_xwalk, 
                                                                  field="Source", 
                                                                  expression="\"DOC_Ag_easements_Range2022\"")

        # Process: Copy Features (Copy Features) (management)
        arcpy.management.CopyFeatures(in_features=DOC_calc_src, 
                                      out_feature_class=DOC_Ag_Standardized.__str__().format(**locals(),**globals()))

        # Process: 7a Enrichments Polygon (7a Enrichments Polygon) (PC414CWIMillionAcres)
        enrich_polygons(enrich_out=DOC_Summarized_Polygons, 
                             enrich_in=DOC_Ag_Standardized.__str__().format(**locals(),**globals()))

        # Process: Copy Features (2) (Copy Features) (management)
        arcpy.management.CopyFeatures(in_features=DOC_Summarized_Polygons, 
                                      out_feature_class=DOC_Ag_enriched.__str__().format(**locals(),**globals()))

        # Process: 2b Assign Domains (2b Assign Domains) (PC414CWIMillionAcres)
        WFR_TF_Template_2_ = AssignDomains(in_table=DOC_Ag_enriched.__str__().format(**locals(),**globals()))[0]

if __name__ == '__main__':
    runner(workspace,scratch_workspace,DOC6, '*argv[1:]')
    # # Global Environment settings
    # with arcpy.EnvManager(extent="-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", outputCoordinateSystem="PROJCS[\"NAD_1983_California_Teale_Albers\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Albers\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",-4000000.0],PARAMETER[\"Central_Meridian\",-120.0],PARAMETER[\"Standard_Parallel_1\",34.0],PARAMETER[\"Standard_Parallel_2\",40.5],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]", preserveGlobalIds=True, 
    #                       scratchWorkspace="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb", workspace="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb"):
    #     aaDOCAg(*argv[1:])
