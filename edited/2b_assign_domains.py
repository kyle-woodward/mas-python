# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2022-11-29 12:12:07
"""
import arcpy
from sys import argv

def AssignDomains(WFR_TF_Template="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\b_Reference\\WFR_TF_Template"):  # 2b Assign Domains

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False


    # Process: Assign Domain To AGENCY Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713 = arcpy.management.AssignDomainToField(in_table=WFR_TF_Template, field_name="AGENCY", domain_name="D_ORGANIZATION", subtype_code=[])[0]

    # Process: Assign Domain To ORG_ADMIN_p Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_3_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713, field_name="ORG_ADMIN_p", domain_name="D_ORGANIZATION", subtype_code=[])[0]

    # Process: Assign Domain To ADMINISTERING_ORG Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_4_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_3_, field_name="ADMINISTERING_ORG", domain_name="D_ORGANIZATION", subtype_code=[])[0]

    # Process: Assign Domain To PROJECT_STATUS Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_5_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_4_, field_name="PROJECT_STATUS", domain_name="D_STATUS", subtype_code=[])[0]

    # Process: Assign Domain To PRIMARY_FUNDING_SOURCE Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_6_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_5_, field_name="PRIMARY_FUNDING_SOURCE", domain_name="D_FNDSRC", subtype_code=[])[0]

    # Process: Assign Domain To PRIMARY_FUNDING_ORG Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_7_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_6_, field_name="PRIMARY_FUNDING_ORG", domain_name="D_ORGANIZATION", subtype_code=[])[0]

    # Process: Assign Domain To VAL_STATUS_p Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_9_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_7_, field_name="Val_Status_p", domain_name="D_DATASTATUS", subtype_code=[])[0]

    # Process: Assign Domain To VAL_MSG_p Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_10_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_9_, field_name="Val_Message_p", domain_name="D_VERFIEDMSG", subtype_code=[])[0]

    # Process: Assign Domain To REVIEW_STATUS_p Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_11_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_10_, field_name="Review_Status_p", domain_name="D_DATASTATUS", subtype_code=[])[0]

    # Process: Assign Domain To REVIEW_MSG_p Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_12_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_11_, field_name="Review_Message_p", domain_name="D_VERFIEDMSG", subtype_code=[])[0]

    # Process: Assign Domain To DATALOAD_STATUS_p Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_13_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_12_, field_name="Dataload_Status_p", domain_name="D_DATASTATUS", subtype_code=[])[0]

    # Process: Assign Domain To DATALOAD_MSG_p Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_14_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_13_, field_name="Dataload_Msg_p", domain_name="D_DATAMSG", subtype_code=[])[0]

    # Process: Assign Domain To ORG_ADMIN_t Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_15_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_14_, field_name="ORG_ADMIN_t", domain_name="D_ORGANIZATION", subtype_code=[])[0]

    # Process: Assign Domain To PRIMARY_OWNERSHIP_GROUP Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_16_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_15_, field_name="PRIMARY_OWNERSHIP_GROUP", domain_name="D_PR_OWN_GR", subtype_code=[])[0]

    # Process: Assign Domain To PRIMARY_OBJECTIVE Field (Assign Domain To Field) (management)
    Updated_Input_Table = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_16_, field_name="PRIMARY_OBJECTIVE", domain_name="D_OBJECTIVE", subtype_code=[])[0]

    # Process: Assign Domain To SECONDARY_OBJECTIVE Field (Assign Domain To Field) (management)
    Updated_Input_Table_2_ = arcpy.management.AssignDomainToField(in_table=Updated_Input_Table, field_name="SECONDARY_OBJECTIVE", domain_name="D_OBJECTIVE", subtype_code=[])[0]

    # Process: Assign Domain To TERTIARY_OBJECTIVE Field (Assign Domain To Field) (management)
    Updated_Input_Table_3_ = arcpy.management.AssignDomainToField(in_table=Updated_Input_Table_2_, field_name="TERTIARY_OBJECTIVE", domain_name="D_OBJECTIVE", subtype_code=[])[0]

    # Process: Assign Domain To TREATMENT_STATUS Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_17_ = arcpy.management.AssignDomainToField(in_table=Updated_Input_Table_3_, field_name="TREATMENT_STATUS", domain_name="D_STATUS", subtype_code=[])[0]

    # Process: Assign Domain To COUNTY Field (Assign Domain To Field) (management)
    Updated_Input_Table_4_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_17_, field_name="COUNTY", domain_name="D_CNTY", subtype_code=[])[0]

    # Process: Assign Domain To IN_WUI Field (Assign Domain To Field) (management)
    Updated_Input_Table_5_ = arcpy.management.AssignDomainToField(in_table=Updated_Input_Table_4_, field_name="IN_WUI", domain_name="D_IN_WUI", subtype_code=[])[0]

    # Process: Assign Domain To REGION Field (Assign Domain To Field) (management)
    Updated_Input_Table_6_ = arcpy.management.AssignDomainToField(in_table=Updated_Input_Table_5_, field_name="REGION", domain_name="D_TASKFORCE", subtype_code=[])[0]

    # Process: Assign Domain To VAL_STATUS_t Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_18_ = arcpy.management.AssignDomainToField(in_table=Updated_Input_Table_6_, field_name="Val_Status_t", domain_name="D_DATASTATUS", subtype_code=[])[0]

    # Process: Assign Domain To VAL_MSG_t Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_19_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_18_, field_name="Val_Message_t", domain_name="D_VERFIEDMSG", subtype_code=[])[0]

    # Process: Assign Domain To REVIEW_STATUS_t Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_20_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_19_, field_name="Review_Status_t", domain_name="D_DATASTATUS", subtype_code=[])[0]

    # Process: Assign Domain To REVIEW_MSG_t Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_21_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_20_, field_name="Review_Message_t", domain_name="D_VERFIEDMSG", subtype_code=[])[0]

    # Process: Assign Domain To DATALOAD_STATUS_t Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_22_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_21_, field_name="Dataload_Status_t", domain_name="D_DATASTATUS", subtype_code=[])[0]

    # Process: Assign Domain To DATALOAD_MSG_t Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_23_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_22_, field_name="Dataload_Msg_t", domain_name="D_DATAMSG", subtype_code=[])[0]

    # Process: Assign Domain To ORG_ADMIN_a Field (Assign Domain To Field) (management)
    Updated_Input_Table_7_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_23_, field_name="ORG_ADMIN_a", domain_name="D_ORGANIZATION", subtype_code=[])[0]

    # Process: Assign Domain To ACTIVITY_DESCRIPTION Field (Assign Domain To Field) (management)
    Updated_Input_Table_8_ = arcpy.management.AssignDomainToField(in_table=Updated_Input_Table_7_, field_name="ACTIVITY_DESCRIPTION", domain_name="D_ACTVDSCRP", subtype_code=[])[0]

    # Process: Assign Domain To ACTIVITY_CAT Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_24_ = arcpy.management.AssignDomainToField(in_table=Updated_Input_Table_8_, field_name="ACTIVITY_CAT", domain_name="D_ACTVCAT", subtype_code=[])[0]

    # Process: Assign Domain To BROAD_VEGETATION_TYPE Field (Assign Domain To Field) (management)
    Updated_Input_Table_9_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_24_, field_name="BROAD_VEGETATION_TYPE", domain_name="D_BVT", subtype_code=[])[0]

    # Process: Assign Domain To BVT_USERD Field (Assign Domain To Field) (management)
    Updated_Input_Table_10_ = arcpy.management.AssignDomainToField(in_table=Updated_Input_Table_9_, field_name="BVT_USERD", domain_name="D_USERDEFINED", subtype_code=[])[0]

    # Process: Assign Domain To ACTIVITY_STATUS Field (Assign Domain To Field) (management)
    Updated_Input_Table_11_ = arcpy.management.AssignDomainToField(in_table=Updated_Input_Table_10_, field_name="ACTIVITY_STATUS", domain_name="D_STATUS", subtype_code=[])[0]

    # Process: Assign Domain To ACTIVITY_UOM Field (Assign Domain To Field) (management)
    Updated_Input_Table_12_ = arcpy.management.AssignDomainToField(in_table=Updated_Input_Table_11_, field_name="ACTIVITY_UOM", domain_name="D_UOM", subtype_code=[])[0]

    # Process: Assign Domain To ADMIN_ORG_NAME Field (Assign Domain To Field) (management)
    Updated_Input_Table_13_ = arcpy.management.AssignDomainToField(in_table=Updated_Input_Table_12_, field_name="ADMIN_ORG_NAME", domain_name="D_ORGANIZATION", subtype_code=[])[0]

    # Process: Assign Domain To IMPLEM_ORG_NAME Field (Assign Domain To Field) (management)
    Updated_Input_Table_14_ = arcpy.management.AssignDomainToField(in_table=Updated_Input_Table_13_, field_name="IMPLEM_ORG_NAME", domain_name="D_ORGANIZATION", subtype_code=[])[0]

    # Process: Assign Domain To PRIMARY_FUND_SRC_NAME Field (Assign Domain To Field) (management)
    Updated_Input_Table_15_ = arcpy.management.AssignDomainToField(in_table=Updated_Input_Table_14_, field_name="PRIMARY_FUND_SRC_NAME", domain_name="D_FNDSRC", subtype_code=[])[0]

    # Process: Assign Domain To PRIMARY_FUND_ORG_NAME Field (Assign Domain To Field) (management)
    Updated_Input_Table_16_ = arcpy.management.AssignDomainToField(in_table=Updated_Input_Table_15_, field_name="PRIMARY_FUND_ORG_NAME", domain_name="D_ORGANIZATION", subtype_code=[])[0]

    # Process: Assign Domain To SECONDARY_FUND_SRC_NAME Field (Assign Domain To Field) (management)
    Updated_Input_Table_17_ = arcpy.management.AssignDomainToField(in_table=Updated_Input_Table_16_, field_name="SECONDARY_FUND_SRC_NAME", domain_name="D_FNDSRC", subtype_code=[])[0]

    # Process: Assign Domain To SECONDARY_FUND_ORG_NAME Field (Assign Domain To Field) (management)
    Updated_Input_Table_18_ = arcpy.management.AssignDomainToField(in_table=Updated_Input_Table_17_, field_name="SECONDARY_FUND_ORG_NAME", domain_name="D_ORGANIZATION", subtype_code=[])[0]

    # Process: Assign Domain To TERTIARY_FUND_SRC_NAME Field (Assign Domain To Field) (management)
    Updated_Input_Table_19_ = arcpy.management.AssignDomainToField(in_table=Updated_Input_Table_18_, field_name="TERTIARY_FUND_SRC_NAME", domain_name="D_FNDSRC", subtype_code=[])[0]

    # Process: Assign Domain To TERTIARY_FUND_ORG_NAME Field (Assign Domain To Field) (management)
    Updated_Input_Table_20_ = arcpy.management.AssignDomainToField(in_table=Updated_Input_Table_19_, field_name="TERTIARY_FUND_ORG_NAME", domain_name="D_ORGANIZATION", subtype_code=[])[0]

    # Process: Assign Domain To RESIDUE_FATE Field (Assign Domain To Field) (management)
    Updated_Input_Table_21_ = arcpy.management.AssignDomainToField(in_table=Updated_Input_Table_20_, field_name="RESIDUE_FATE", domain_name="D_RESIDUEFATE", subtype_code=[])[0]

    # Process: Assign Domain To RESIDUE_FATE_UNITS Field (Assign Domain To Field) (management)
    Updated_Input_Table_22_ = arcpy.management.AssignDomainToField(in_table=Updated_Input_Table_21_, field_name="RESIDUE_FATE_UNITS", domain_name="D_UOM", subtype_code=[])[0]

    # Process: Assign Domain To VAL_STATUS_a Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_25_ = arcpy.management.AssignDomainToField(in_table=Updated_Input_Table_22_, field_name="VAL_STATUS_a", domain_name="D_DATASTATUS", subtype_code=[])[0]

    # Process: Assign Domain To VAL_MSG_a Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_26_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_25_, field_name="VAL_MSG_a", domain_name="D_VERFIEDMSG", subtype_code=[])[0]

    # Process: Assign Domain To REVIEW_STATUS_a Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_27_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_26_, field_name="REVIEW_STATUS_a", domain_name="D_DATASTATUS", subtype_code=[])[0]

    # Process: Assign Domain To REVIEW_MSG_a Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_28_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_27_, field_name="REVIEW_MSG_a", domain_name="D_VERFIEDMSG", subtype_code=[])[0]

    # Process: Assign Domain To DATALOAD_STATUS_a Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_29_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_28_, field_name="DATALOAD_STATUS_a", domain_name="D_DATASTATUS", subtype_code=[])[0]

    # Process: Assign Domain To DATALOAD_MSG_a Field (Assign Domain To Field) (management)
    usfs_haz_fuels_treatments_standardized_20220713_30_ = arcpy.management.AssignDomainToField(in_table=usfs_haz_fuels_treatments_standardized_20220713_29_, field_name="DATALOAD_MSG_a", domain_name="D_DATAMSG", subtype_code=[])[0]

    return usfs_haz_fuels_treatments_standardized_20220713_30_

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(extent="-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]", outputCoordinateSystem="PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]", preserveGlobalIds=True, 
                          qualifiedFieldNames=False, scratchWorkspace=r"C:\Users\sageg\Documents\ArcGIS\Projects\PC414 CWI Million Acres\scratch.gdb", transferDomains=True, 
                          transferGDBAttributeProperties=True, workspace=r"C:\Users\sageg\Documents\ArcGIS\Projects\PC414 CWI Million Acres\PC414 CWI Million Acres.gdb"):
        AssignDomains(*argv[1:])
