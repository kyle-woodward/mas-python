"""
# Description: Converts the California Department of Conservation Ag dataset 
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
from scripts.utils import init_gdb

workspace, scratch_workspace = init_gdb()

def DOC6(DOC_Ag_Standardized, 
            DOC_Ag_enriched,
            DOC_Ag_OG):  

    #scratch outputs
    DOC_Ag_OG_Dissolve = os.path.join(scratch_workspace, "DOC_Ag_OG_Dissolve")
    DOC_Summarized_Polygons = os.path.join(scratch_workspace, "DOC_Summarized_Polygons")

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
        # Process: Dissolve (Dissolve) (management)
        print("step 1/24  dissolve...")
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
        print("step 2/24  repair geometry...")
        DOC_Repaired_Geometry = arcpy.management.RepairGeometry(in_features=DOC_Ag_OG_Dissolve)

        # Process: 1b Add Fields (1b Add Fields) 
        print("step 3/24  add fields...")
        DOC_w_Fields = AddFields(Input_Table=DOC_Repaired_Geometry)

        # Process: Calculate Project ID (Calculate Field) (management)
        print("step 4/24  calculate field...")
        DOC_calc_proj_id = arcpy.management.CalculateField(in_table=DOC_w_Fields, 
                                                                  field="PROJECTID_USER", 
                                                                  expression="!Grant_Nm!")

        # Process: Calculate Agency (Calculate Field) (management)
        print("step 5/24  calculate field...")
        DOC_calc_agency = arcpy.management.CalculateField(in_table=DOC_calc_proj_id, 
                                                                  field="AGENCY", 
                                                                  expression="\"CNRA\"")

        # Process: Calculate Administering Org (Calculate Field) (management)
        print("step 6/24  calculate field...")
        DOC_calc_admin_org = arcpy.management.CalculateField(in_table=DOC_calc_agency, 
                                                                 field="ADMINISTERING_ORG", 
                                                                 expression="\"DOC\"")

        # Process: Calculate Project Name (Calculate Field) (management)
        print("step 7/24  calculate field...")
        DOC_calc_proj_name = arcpy.management.CalculateField(in_table=DOC_calc_admin_org, 
                                                                 field="PROJECT_NAME", 
                                                                 expression="!PROJECT!")

        # Process: Calculate Implementing Org (Calculate Field) (management)
        print("step 8/24  calculate field...")
        DOC_calc_imp_org = arcpy.management.CalculateField(in_table=DOC_calc_proj_name, 
                                                                  field="IMPLEMENTING_ORG", 
                                                                  expression="!HOLDER!")

        # Process: Calculate Treatment ID (Calculate Field) (management)
        print("step 9/24  calculate field...")
        DOC_calc_treat_id = arcpy.management.CalculateField(in_table=DOC_calc_imp_org, 
                                                                  field="TRMTID_USER", 
                                                                  expression="!Grant_Nm! + '-' + !PROJECT![:12]")#+'-'+!PRIMARY_OWNERSHIP_GROUP![:11]+'-'+!IN_WUI![:3]")

        # Process: Calculate BVT (Calculate Field) (management)
        print("step 10/24  calculate field...")
        DOC_calc_bvt = arcpy.management.CalculateField(in_table=DOC_calc_treat_id, 
                                                                  field="BVT_USERD", 
                                                                  expression="\"NO\"")

        # Process: Calculate Activity Status (Calculate Field) (management)
        print("step 11/24  calculate field...")
        DOC_calc_act_stat = arcpy.management.CalculateField(in_table=DOC_calc_bvt, 
                                                                  field="ACTIVITY_STATUS", 
                                                                  expression="\"ACTIVE\"")

        # Process: Calculate Activity Quantity (Calculate Field) (management)
        print("step 12/24  calculate field...")
        DOC_calc_act_quant = arcpy.management.CalculateField(in_table=DOC_calc_act_stat, 
                                                              field="ACTIVITY_QUANTITY", 
                                                              expression="!ACRES!")

        # Process: Calculate UOM (Calculate Field) (management)
        print("step 13/24  calculate field...")
        DOC_calc_uom = arcpy.management.CalculateField(in_table=DOC_calc_act_quant, 
                                                                 field="ACTIVITY_UOM", 
                                                                 expression="\"AC\"")

        # Process: Calculate Activity End (Calculate Field) (management)
        print("step 14/24  calculate field...")
        DOC_calc_act_end = arcpy.management.CalculateField(in_table=DOC_calc_uom, 
                                                                  field="ACTIVITY_END", 
                                                                  expression="!ClosingDat!")
        
        # Process: Calculate Primary Funding Org (Calculate Field) (management)
        print("step 15/24  calculate field...")
        DOC_calc_prim_fund_org = arcpy.management.CalculateField(in_table=DOC_calc_act_end, 
                                                                 field="PRIMARY_FUND_ORG_NAME", 
                                                                 expression="!PROVIDER!")

        # Process: Calculate Primary Funding Source (Calculate Field) (management)
        print("step 16/24  calculate field...")
        DOC_calc_prim_fund_src = arcpy.management.CalculateField(in_table=DOC_calc_prim_fund_org, 
                                                                 field="PRIMARY_FUND_SRC_NAME", 
                                                                 expression="!FUNDER1!")

        # Process: Calculate SecondaryFunding Src Name (Calculate Field) (management)
        print("step 17/24  calculate field...")
        DOC_calc_sec_fund_src_name = arcpy.management.CalculateField(in_table=DOC_calc_prim_fund_src, 
                                                                 field="SECONDARY_FUND_SRC_NAME", 
                                                                 expression="!FUNDER2!")

        # Process: Calculate Tertiary Funding Src Name (Calculate Field) (management)
        print("step 18/24  calculate field...")
        DOC_calc_tert_fund_src_name = arcpy.management.CalculateField(in_table=DOC_calc_sec_fund_src_name, 
                                                                  field="TERTIARY_FUND_SRC_NAME", 
                                                                  expression="!FUNDER3!")

        # Process: Calculate Crosswalk (Calculate Field) (management)
        print("step 19/24  calculate field...")
        DOC_calc_xwalk = arcpy.management.CalculateField(in_table=DOC_calc_tert_fund_src_name, 
                                                                  field="Crosswalk", 
                                                                  expression="\"EASEMENT\"")

        # Process: Calculate Source (Calculate Field) (management)
        print("step 20/24  calculate field...")
        DOC_calc_src = arcpy.management.CalculateField(in_table=DOC_calc_xwalk, 
                                                                  field="Source", 
                                                                  expression="\"DOC_Ag_easements_Range2022\"")

        # Process: Copy Features (Copy Features) (management)
        print("step 21/24  copy features...")
        arcpy.management.CopyFeatures(in_features=DOC_calc_src, 
                                      out_feature_class=DOC_Ag_Standardized)

        # Process: 7a Enrichments Polygon
        print("step 22/24  enrich polygons...")
        enrich_polygons(enrich_out=DOC_Summarized_Polygons, 
                             enrich_in=DOC_Ag_Standardized)

        # Process: Copy Features (2) (Copy Features) (management)
        print("step 23/24  copy features...")
        arcpy.management.CopyFeatures(in_features=DOC_Summarized_Polygons, 
                                      out_feature_class=DOC_Ag_enriched)

        # Process: 2b Assign Domains (2b Assign Domains) 
        print("step 24/24 assign domains...")
        WFR_TF_Template_2_ = AssignDomains(in_table=DOC_Ag_enriched)

        print("6aa complete...")

