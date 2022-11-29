# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2022-11-29 12:11:56
"""
import arcpy

def TablesToDomains():  # 2a Tables to Domains

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    D_VERFIEDMSG_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\3-Documents\\Domain Tables 20221129.xlsx\\D_VERFIEDMSG$"
    PC414_CWI_Million_Acres_gdb_19_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb"
    D_USERDEFINED_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\3-Documents\\Domain Tables 20221129.xlsx\\D_USERDEFINED$"
    D_OBJECTIVE_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\3-Documents\\Domain Tables 20221129.xlsx\\D_OBJECTIVE$"
    D_STATUS_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\3-Documents\\Domain Tables 20221129.xlsx\\D_STATUS$"
    D_CNTY_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\3-Documents\\Domain Tables 20221129.xlsx\\D_CNTY$"
    D_IN_WUI_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\3-Documents\\Domain Tables 20221129.xlsx\\D_IN_WUI$"
    D_ACTVDSCRP_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\3-Documents\\Domain Tables 20221129.xlsx\\D_ACTVDSCRP$"
    D_ACTVCAT_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\3-Documents\\Domain Tables 20221129.xlsx\\D_ACTVCAT$"
    D_BVT_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\3-Documents\\Domain Tables 20221129.xlsx\\D_BVT$"
    D_RESIDUEFATE_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\3-Documents\\Domain Tables 20221129.xlsx\\D_RESIDUEFATE$"
    D_UOM_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\3-Documents\\Domain Tables 20221129.xlsx\\D_UOM$"
    D_TASKFORCE_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\3-Documents\\Domain Tables 20221129.xlsx\\D_TASKFORCE$"
    D_PR_OWN_GR_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\3-Documents\\Domain Tables 20221129.xlsx\\D_PR_OWN_GR$"
    D_FNDSRC_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\3-Documents\\Domain Tables 20221129.xlsx\\D_FNDSRC$"
    D_ORGANIZATION_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\3-Documents\\Domain Tables 20221129.xlsx\\D_ORGANIZATION$"
    D_DATASTATUS_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\3-Documents\\Domain Tables 20221129.xlsx\\D_DATASTATUS$"
    D_DATAMSG_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\3-Documents\\Domain Tables 20221129.xlsx\\D_DATAMSG$"

    # Process: Table To Validated Domain (Table To Domain) (management)
    PC414_CWI_Million_Acres_gdb = arcpy.management.TableToDomain(in_table=D_VERFIEDMSG_, code_field="CODE__v2_", description_field="Descr", in_workspace=PC414_CWI_Million_Acres_gdb_19_, domain_name="D_VERFIEDMSG", domain_description="Validated or Reviewed", update_option="REPLACE")[0]

    # Process: Table To User Defined Domain (Table To Domain) (management)
    PC414_CWI_Million_Acres_gdb_3_ = arcpy.management.TableToDomain(in_table=D_USERDEFINED_, code_field="CODE__v2_", description_field="Descr", in_workspace=PC414_CWI_Million_Acres_gdb_19_, domain_name="D_USERDEFINED", domain_description="Yes / No", update_option="REPLACE")[0]

    # Process: Table To Objectives Domain (Table To Domain) (management)
    PC414_CWI_Million_Acres_gdb_4_ = arcpy.management.TableToDomain(in_table=D_OBJECTIVE_, code_field="CODE__v2_", description_field="Descr", in_workspace=PC414_CWI_Million_Acres_gdb_19_, domain_name="D_OBJECTIVE", domain_description="Objectives", update_option="REPLACE")[0]

    # Process: Table To Status Domain (Table To Domain) (management)
    PC414_CWI_Million_Acres_gdb_5_ = arcpy.management.TableToDomain(in_table=D_STATUS_, code_field="CODE__v2_", description_field="Descr", in_workspace=PC414_CWI_Million_Acres_gdb_19_, domain_name="D_STATUS", domain_description="Status", update_option="REPLACE")[0]

    # Process: Table To County Domain (Table To Domain) (management)
    PC414_CWI_Million_Acres_gdb_6_ = arcpy.management.TableToDomain(in_table=D_CNTY_, code_field="CODE__v2_", description_field="Descr", in_workspace=PC414_CWI_Million_Acres_gdb_19_, domain_name="D_CNTY", domain_description="County", update_option="REPLACE")[0]

    # Process: Table To WUI Domain (Table To Domain) (management)
    PC414_CWI_Million_Acres_gdb_7_ = arcpy.management.TableToDomain(in_table=D_IN_WUI_, code_field="CODE__v2_", description_field="Descr", in_workspace=PC414_CWI_Million_Acres_gdb_19_, domain_name="D_IN_WUI", domain_description="In WUI", update_option="REPLACE")[0]

    # Process: Table To Activity Description Domain (Table To Domain) (management)
    PC414_CWI_Million_Acres_gdb_8_ = arcpy.management.TableToDomain(in_table=D_ACTVDSCRP_, code_field="CODE__v2_", description_field="Descr", in_workspace=PC414_CWI_Million_Acres_gdb_19_, domain_name="D_ACTVDSCRP", domain_description="Activity Description", update_option="REPLACE")[0]

    # Process: Table To Category Domain (Table To Domain) (management)
    PC414_CWI_Million_Acres_gdb_9_ = arcpy.management.TableToDomain(in_table=D_ACTVCAT_, code_field="CODE__v2_", description_field="Descr", in_workspace=PC414_CWI_Million_Acres_gdb_19_, domain_name="D_ACTVCAT", domain_description="Activity Category", update_option="REPLACE")[0]

    # Process: Table To Veg Domain (Table To Domain) (management)
    PC414_CWI_Million_Acres_gdb_10_ = arcpy.management.TableToDomain(in_table=D_BVT_, code_field="CODE__v2_", description_field="Descr", in_workspace=PC414_CWI_Million_Acres_gdb_19_, domain_name="D_BVT", domain_description="Broad Vegetation Type", update_option="REPLACE")[0]

    # Process: Table To Residue Domain (Table To Domain) (management)
    PC414_CWI_Million_Acres_gdb_11_ = arcpy.management.TableToDomain(in_table=D_RESIDUEFATE_, code_field="CODE__v2_", description_field="Descr", in_workspace=PC414_CWI_Million_Acres_gdb_19_, domain_name="D_RESIDUEFATE", domain_description="Residue Fate", update_option="REPLACE")[0]

    # Process: Table To UOM Domain (Table To Domain) (management)
    PC414_CWI_Million_Acres_gdb_12_ = arcpy.management.TableToDomain(in_table=D_UOM_, code_field="CODE__v2_", description_field="Descr", in_workspace=PC414_CWI_Million_Acres_gdb_19_, domain_name="D_UOM", domain_description="Unit of Measure", update_option="REPLACE")[0]

    # Process: Table To Region Domain (Table To Domain) (management)
    PC414_CWI_Million_Acres_gdb_13_ = arcpy.management.TableToDomain(in_table=D_TASKFORCE_, code_field="CODE__v2_", description_field="Descr", in_workspace=PC414_CWI_Million_Acres_gdb_19_, domain_name="D_TASKFORCE", domain_description="Task Force Region", update_option="REPLACE")[0]

    # Process: Table To Owner Domain (Table To Domain) (management)
    PC414_CWI_Million_Acres_gdb_14_ = arcpy.management.TableToDomain(in_table=D_PR_OWN_GR_, code_field="CODE__v2_", description_field="Descr", in_workspace=PC414_CWI_Million_Acres_gdb_19_, domain_name="D_PR_OWN_GR", domain_description="Ownership Group", update_option="REPLACE")[0]

    # Process: Table To Funding Source Domain (Table To Domain) (management)
    PC414_CWI_Million_Acres_gdb_15_ = arcpy.management.TableToDomain(in_table=D_FNDSRC_, code_field="CODE__v2_", description_field="Descr", in_workspace=PC414_CWI_Million_Acres_gdb_19_, domain_name="D_FNDSRC", domain_description="Funding Source", update_option="REPLACE")[0]

    # Process: Table To Organization Domain (Table To Domain) (management)
    PC414_CWI_Million_Acres_gdb_16_ = arcpy.management.TableToDomain(in_table=D_ORGANIZATION_, code_field="CODE__v2_", description_field="Descr", in_workspace=PC414_CWI_Million_Acres_gdb_19_, domain_name="D_ORGANIZATION", domain_description="Organization or Agency", update_option="REPLACE")[0]

    # Process: Table To Date Status Domain (Table To Domain) (management)
    PC414_CWI_Million_Acres_gdb_17_ = arcpy.management.TableToDomain(in_table=D_DATASTATUS_, code_field="CODE__v2_", description_field="Descr", in_workspace=PC414_CWI_Million_Acres_gdb_19_, domain_name="D_DATASTATUS", domain_description="Data Status", update_option="REPLACE")[0]

    # Process: Table To Data Load Domain (Table To Domain) (management)
    PC414_CWI_Million_Acres_gdb_18_ = arcpy.management.TableToDomain(in_table=D_DATAMSG_, code_field="CODE__v2_", description_field="Descr", in_workspace=PC414_CWI_Million_Acres_gdb_19_, domain_name="D_DATAMSG", domain_description="Data Load Message", update_option="REPLACE")[0]

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(
        extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""", 
        outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""", 
        preserveGlobalIds=True, 
        qualifiedFieldNames=False, 
        scratchWorkspace=r"C:\Users\sageg\Documents\ArcGIS\Projects\PC414 CWI Million Acres\scratch.gdb", 
        transferDomains=True, 
        transferGDBAttributeProperties=True, 
        workspace=r"C:\Users\sageg\Documents\ArcGIS\Projects\PC414 CWI Million Acres\PC414 CWI Million Acres.gdb"):
        
        TablesToDomains()
