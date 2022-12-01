# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2022-11-29 12:11:19
"""
import arcpy
import os
from sys import argv
from utils import init_gdb, runner
original_gdb, workspace, scratch_workspace = init_gdb()
def AddFields2(Input_Table):  # 1b Add Fields

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False


    # Process: Add Projects Fields (multiple) (Add Fields (multiple)) (management)
    WFRTF_Template_2_ = arcpy.management.AddFields(in_table=Input_Table, field_description=[["PROJECTID_USER", "TEXT", "PROJECT ID USER", "40", "", ""], 
                                                                                            ["AGENCY", "TEXT", "AGENCY_DEPARTMENT", "55", "", "D_ORGANIZATION"], 
                                                                                            ["ORG_ADMIN_p", "TEXT", "ORG DATA STEWARD", "55", "", "D_ORGANIZATION"], 
                                                                                            ["PROJECT_CONTACT", "TEXT", "PROJECT CONTACT", "40", "", ""], 
                                                                                            ["PROJECT_EMAIL", "TEXT", "PROJECT EMAIL", "40", "", ""], 
                                                                                            ["ADMINISTERING_ORG", "TEXT", "ADMINISTERING ORG", "55", "", "D_ORGANIZATION"], 
                                                                                            ["PROJECT_NAME", "TEXT", "PROJECT NAME", "125", "", ""], 
                                                                                            ["PROJECT_STATUS", "TEXT", "PROJECT STATUS", "25", "", "D_STATUS"], 
                                                                                            ["PROJECT_START", "DATE", "PROJECT START", "8", "", ""], 
                                                                                            ["PROJECT_END", "DATE", "PROJECT END", "8", "", ""], 
                                                                                            ["PRIMARY_FUNDING_SOURCE", "TEXT", "PRIMARY_FUNDING_SOURCE", "130", "", "D_FNDSRC"], 
                                                                                            ["PRIMARY_FUNDING_ORG", "TEXT", "PRIMARY_FUNDING_ORG", "130", "", "D_ORGANIZATION"], 
                                                                                            ["IMPLEMENTING_ORG", "TEXT", "IMPLEMENTING_ORG", "55", "", ""], 
                                                                                            ["LATITUDE", "DOUBLE", "LATITUDE CENTROID", "8", "", ""], 
                                                                                            ["LONGITUDE", "DOUBLE", "LONGITUDE CENTROID", "8", "", ""], 
                                                                                            ["BatchID_p", "TEXT", "Batch ID", "40", "", ""], 
                                                                                            ["Val_Status_p", "TEXT", "Validation Status", "15", "", "D_DATASTATUS"], 
                                                                                            ["Val_Message_p", "TEXT", "Validation Message", "15", "", "D_VERFIEDMSG"], 
                                                                                            ["Val_RunDate_p", "DATE", "Validation Run Date", "8", "", ""], 
                                                                                            ["Review_Status_p", "TEXT", "Review Status", "15", "", "D_DATASTATUS"], 
                                                                                            ["Review_Message_p", "TEXT", "Review Message", "15", "", "D_VERFIEDMSG"], 
                                                                                            ["Review_RunDate_p", "DATE", "Review Run Date", "8", "", ""], 
                                                                                            ["Dataload_Status_p", "TEXT", "Dataload Status", "15", "", "D_DATASTATUS"], 
                                                                                            ["Dataload_Msg_p", "TEXT", "Dataload Message", "15", "", "D_DATAMSG"]], 
                                                                                            )[0]

    # Process: Add Treatments Fields (multiple) (Add Fields (multiple)) (management)
    WFRTF_Template_3_ = arcpy.management.AddFields(in_table=WFRTF_Template_2_, field_description=[["TRMTID_USER", "TEXT", "TREATMENT ID USER", "40", "", ""], 
                                                                                                  ["PROJECTID", "TEXT", "PROJECTID", "50", "", ""], 
                                                                                                  ["PROJECTNAME_", "TEXT", "PROJECT NAME", "125", "", ""], 
                                                                                                  ["ORG_ADMIN_t", "TEXT", "ORG DATA STEWARD", "255", "", "D_ORGANIZATION"], 
                                                                                                  ["PRIMARY_OWNERSHIP_GROUP", "TEXT", "PRIMARY OWNERSHIP GROUP", "25", "", "D_PR_OWN_GR"], 
                                                                                                  ["PRIMARY_OBJECTIVE", "TEXT", "PRIMARY OBJECTIVE", "65", "", "D_OBJECTIVE"], 
                                                                                                  ["SECONDARY_OBJECTIVE", "TEXT", "SECONDARY OBJECTIVE", "65", "", "D_OBJECTIVE"], 
                                                                                                  ["TERTIARY_OBJECTIVE", "TEXT", "TERTIARY OBJECTIVE", "65", "", "D_OBJECTIVE"], 
                                                                                                  ["TREATMENT_STATUS", "TEXT", "TREATMENT STATUS", "25", "", "D_STATUS"], 
                                                                                                  ["COUNTY", "TEXT", "COUNTY", "25", "", "D_CNTY"], 
                                                                                                  ["IN_WUI", "TEXT", "IN WUI", "30", "", "D_IN_WUI"], 
                                                                                                  ["REGION", "TEXT", "TASK FORCE REGION", "25", "", "D_TASKFORCE"], 
                                                                                                  ["TREATMENT_AREA", "DOUBLE", "TREATMENT AREA (GIS ACRES)", "8", "", ""], 
                                                                                                  ["TREATMENT_START", "DATE", "TREATMENT START", "8", "", ""], 
                                                                                                  ["TREATMENT_END", "DATE", "TREATMENT END", "8", "", ""], 
                                                                                                  ["RETREATMENT_DATE_EST", "DATE", "RETREATMENT DATE ESTIMATE", "8", "", ""], 
                                                                                                  ["TREATMENT_NAME", "TEXT", "TREATMENT NAME", "125", "", ""], 
                                                                                                  ["BatchID", "TEXT", "BATCH ID (TREATMENT)", "40", "", ""], 
                                                                                                  ["Val_Status_t", "TEXT", "Validation Status", "15", "", "D_DATASTATUS"], 
                                                                                                  ["Val_Message_t", "TEXT", "Validation Message", "15", "", "D_VERFIEDMSG"], 
                                                                                                  ["Val_RunDate_t", "DATE", "Validation Run Date", "8", "", ""], 
                                                                                                  ["Review_Status_t", "TEXT", "Review Status", "15", "", "D_DATASTATUS"], 
                                                                                                  ["Review_Message_t", "TEXT", "Review Message", "15", "", "D_VERFIEDMSG"], 
                                                                                                  ["Review_RunDate_t", "DATE", "Review Run Date", "8", "", ""], 
                                                                                                  ["Dataload_Status_t", "TEXT", "Dataload Status", "15", "", "D_DATASTATUS"], 
                                                                                                  ["Dataload_Msg_t", "TEXT", "Dataload Message", "15", "", "D_DATAMSG"]], 
                                                                                                  )[0]

    # Process: Add Activities Fields (multiple) (Add Fields (multiple)) (management)
    WFRTF_Template_4_ = arcpy.management.AddFields(in_table=WFRTF_Template_3_, field_description=[["ACTIVID_USER", "TEXT", "ACTIVITYID USER", "50", "", ""], 
                                                                                                  ["TREATMENTID_", "TEXT", "TREATMENTID", "50", "", ""], 
                                                                                                  ["ORG_ADMIN_a", "TEXT", "ORG DATA STEWARD", "150", "", "D_ORGANIZATION"], 
                                                                                                  ["ACTIVITY_DESCRIPTION", "TEXT", "ACTIVITY DESCRIPTION", "70", "", "D_ACTVDSCRP"], 
                                                                                                  ["ACTIVITY_CAT", "TEXT", "ACTIVITY CATEGORY", "40", "", "D_ACTVCAT"], 
                                                                                                  ["BROAD_VEGETATION_TYPE", "TEXT", "BROAD VEGETATION TYPE", "50", "", "D_BVT"], 
                                                                                                  ["BVT_USERD", "TEXT", "IS BVT USER DEFINED", "3", "", "D_USERDEFINED"], 
                                                                                                  ["ACTIVITY_STATUS", "TEXT", "ACTIVITY STATUS", "25", "", "D_STATUS"], 
                                                                                                  ["ACTIVITY_QUANTITY", "DOUBLE", "ACTIVITY QUANTITY", "8", "", ""], 
                                                                                                  ["ACTIVITY_UOM", "TEXT", "ACTIVITY UNITS", "15", "", "D_UOM"], 
                                                                                                  ["ACTIVITY_START", "DATE", "ACTIVITY START", "8", "", ""], 
                                                                                                  ["ACTIVITY_END", "DATE", "ACTIVITY END", "8", "", ""], 
                                                                                                  ["ADMIN_ORG_NAME", "TEXT", "ADMINISTRATION ORGANIZATION NAME", "150", "", "D_ORGANIZATION"], 
                                                                                                  ["IMPLEM_ORG_NAME", "TEXT", "IMPLEMENTATION ORGANIZATION NAME", "150", "", "D_ORGANIZATION"], 
                                                                                                  ["PRIMARY_FUND_SRC_NAME", "TEXT", "PRIMARY FUND SOURCE NAME", "100", "", "D_FNDSRC"], 
                                                                                                  ["PRIMARY_FUND_ORG_NAME", "TEXT", "PRIMARY FUND ORGANIZATION NAME", "100", "", "D_ORGANIZATION"], 
                                                                                                  ["SECONDARY_FUND_SRC_NAME", "TEXT", "SECONDARY FUND SOURCE NAME", "100", "", "D_FNDSRC"], 
                                                                                                  ["SECONDARY_FUND_ORG_NAME", "TEXT", "SECONDARY FUND ORGANIZATION NAME", "100", "", "D_ORGANIZATION"], 
                                                                                                  ["TERTIARY_FUND_SRC_NAME", "TEXT", "TERTIARY FUND SOURCE NAME", "100", "", "D_FNDSRC"], 
                                                                                                  ["TERTIARY_FUND_ORG_NAME", "TEXT", "TERTIARY FUND ORGANIZATION NAME", "100", "", ""], 
                                                                                                  ["ACTIVITY_PRCT", "SHORT", "ACTIVITY PERCENT", "3", "", ""], 
                                                                                                  ["RESIDUE_FATE", "TEXT", "RESIDUE FATE", "35", "", "D_RESIDUEFATE"], 
                                                                                                  ["RESIDUE_FATE_QUANTITY", "DOUBLE", "RESIDUE FATE QUANTITY", "8", "", ""], 
                                                                                                  ["RESIDUE_FATE_UNITS", "TEXT", "RESIDUE FATE UNITS", "5", "", "D_UOM"], 
                                                                                                  ["ACTIVITY_NAME", "TEXT", "ACTIVITY NAME", "150", "", ""], 
                                                                                                  ["VAL_STATUS_a", "TEXT", "VALIDATION STATUS", "15", "", "D_DATASTATUS"], 
                                                                                                  ["VAL_MSG_a", "TEXT", "VALIDATION MESSAGE", "15", "", "D_VERFIEDMSG"], 
                                                                                                  ["VAL_RUNDATE_a", "DATE", "VALIDATION RUN DATE", "8", "", ""], 
                                                                                                  ["REVIEW_STATUS_a", "TEXT", "REVIEW STATUS", "15", "", "D_DATASTATUS"], 
                                                                                                  ["REVIEW_MSG_a", "TEXT", "REVIEW MESSAGE", "15", "", "D_VERFIEDMSG"], 
                                                                                                  ["REVIEW_RUNDATE_a", "DATE", "REVIEW RUN DATE", "8", "", ""], 
                                                                                                  ["DATALOAD_STATUS_a", "TEXT", "DATALOAD STATUS", "15", "", "D_DATASTATUS"], 
                                                                                                  ["DATALOAD_MSG_a", "TEXT", "DATALOAD MESSAGE", "15", "", "D_DATAMSG"], 
                                                                                                  ["Source", "TEXT", "Source", "65", "", ""], 
                                                                                                  ["Year", "LONG", "Calendar Year", "", "", ""], 
                                                                                                  ["Year_txt", "TEXT", "Year as Text", "255", "", ""], 
                                                                                                  ["Act_Code", "LONG", "USFS Activity Code", "", "", ""], 
                                                                                                  ["Crosswalk", "TEXT", "Crosswalk Activities", "150", "", ""], 
                                                                                                  ["Federal_FY", "LONG", "Federal FY", "", "", ""], 
                                                                                                  ["State_FY", "LONG", "State FY", "", "", ""]], 
                                                                                                  )[0]

    return WFRTF_Template_4_

if __name__ == '__main__':
    # Global Environment settings
    # run desired function with environment settings set by arcpy.EnvManager
    # trying a one-line execution of the below.. might not be so easy
    # runner(workspace,scratch_workspace,AddFields2)

    
    # Global Environment settings
    # to fix syntax errors in extent and outputCoordinateSystem args, wrap string values in triple quotes
    with arcpy.EnvManager(
    extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""", 
    outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""", 
    preserveGlobalIds=True, 
    qualifiedFieldNames=False, 
    scratchWorkspace=scratch_workspace, 
    transferDomains=True, 
    transferGDBAttributeProperties=True, 
    workspace=workspace):
        
        AddFields2(*argv[1:])