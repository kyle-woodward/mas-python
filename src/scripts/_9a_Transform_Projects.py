"""
# Description: 
#               
#               
#              
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import arcpy
from scripts._9c_Transform_Check_Duplicates import TransformCheck
# from sys import argv
from datetime import datetime
import time
from .utils import init_gdb, runner, delete_scratch_files
# import os

original_gdb, workspace, scratch_workspace = init_gdb()

# date value
Value = datetime.utcnow().strftime("%Y-%m-%d").replace("-", "")
Value2 = time.strftime("%Y%m%d-%H%M%S").replace("-", "")


def TransformProjects(
    Input_Features,
    project_poly,
    CNRA_Projects="CNRA_Projects",
    Output_Duplicate_Projects=os.path.join(
        scratch_workspace, rf"Duplicate_Projects_{Value2}"
    ),
):  # 9a Transform Projects
    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    # scratch outputs
    CNRA_Projects_Select = os.path.join(scratch_workspace, "CNRA_Projects_Select")
    treat_buffered = os.path.join(scratch_workspace, "treatment_buffered")
    project_buffered = os.path.join(scratch_workspace, "project_buffered")
    treat_spatialjoin = os.path.join(scratch_workspace, "treat_spatialjoin")

    # # workspace outputs
    # Output_Features = os.path.join(workspace, 'f_Transformed', fr"{Input_Features}_transformed_{Value}")
    # Project = os.path.join(workspace, 'f_Transformed', fr"Project_poly_{Value}")

    # singlepart_output = os.path.join(scratch_workspace, 'singlepart_transformed')
    # singlepart_output2 = os.path.join(scratch_workspace, 'singlepart_transformed2')

    # Process: Select (6) (Select) (analysis)
    CNRA_Projects_Select = arcpy.analysis.Select(
        in_features=CNRA_Projects.__str__().format(**locals(), **globals()),
        out_feature_class=CNRA_Projects_Select,
    )

    # Process: Calculate Date Value (Calculate Value) ()
    # Value = datetime.utcnow().strftime("%Y-%m-%d").replace('-','')

    # Process: Dissolve (Dissolve) (management)
    if Value:
        arcpy.management.Dissolve(
            in_features=Input_Features.__str__().format(**locals(), **globals()),
            out_feature_class=project_poly,
            dissolve_field=[
                "PROJECTID_USER",
                "AGENCY",
                "ORG_ADMIN_p",
                "PROJECT_CONTACT",
                "PROJECT_EMAIL",
                "ADMINISTERING_ORG",
                "PROJECT_NAME",
                "PROJECT_STATUS",
                "PROJECT_START",
                "PROJECT_END",
                "PRIMARY_FUNDING_SOURCE",
                "PRIMARY_FUNDING_ORG",
                "IMPLEMENTING_ORG",
                "BatchID_p",
                "Val_Status_p",
                "Val_Message_p",
                "Val_RunDate_p",
                "Review_Status_p",
                "Review_Message_p",
                "Review_RunDate_p",
                "Source",
            ],
        )

    # Process: Add Field (3) (Add Field) (management)
    if Value:
        Treat_n_harves_Project_SpatialJoin1_2_ = arcpy.management.AddField(
            in_table=project_poly,
            field_name="GlobalID",
            field_type="GUID",
            field_alias="PROJECTID",
        )

    # Process: Add Global IDs (4) (Add Global IDs) (management)
    if Treat_n_harves_Project_SpatialJoin1_2_ and Value:
        Updated_Datasets_4_ = arcpy.management.AddGlobalIDs(in_datasets=[project_poly])

    # Process: Calculate Field (5) (Calculate Field) (management)
    if Treat_n_harves_Project_SpatialJoin1_2_ and Updated_Datasets_4_ and Value:
        treat_spatialjoin = arcpy.management.CalculateField(
            in_table=Treat_n_harves_Project_SpatialJoin1_2_,
            field="GlobalID",
            expression="!GlobalID_1!",
        )

    # # Process: Delete Field (4) (Delete Field) (management)
    # if Treat_n_harves_Project_SpatialJoin1_2_ and Updated_Datasets_4_ and Value:
    #     Project_2_ = arcpy.management.DeleteField(in_table=Treat_n_harves_Project_SpatialJoin1_3_,
    #                                               drop_field=["GlobalID_1"])

    # # Process: Append (2) (Append) (management)
    # if Treat_n_harves_Project_SpatialJoin1_2_ and Updated_Datasets_4_ and Value:
    #     Output_Features = arcpy.management.Append(inputs=[CNRA_Projects_Select],
    #                                               target=Project_2_,
    #                                               schema_type="NO_TEST",
    #                                               field_mapping="PROJECTID_USER \"PROJECT ID USER\" true true false 40 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECTID_USER,0,50;AGENCY \"AGENCY/DEPARTMENT\" true true false 55 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,AGENCY,0,150;ORG_ADMIN_p \"ORG DATA STEWARD\" true true false 55 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,ORG_ADMIN_p,0,150;PROJECT_CONTACT \"PROJECT CONTACT\" true true false 40 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_CONTACT,0,100;PROJECT_EMAIL \"PROJECT EMAIL\" true true false 40 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_EMAIL,0,100;ADMINISTERING_ORG \"ADMINISTERING ORG\" true true false 55 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,ADMINISTERING_ORG,0,150;PROJECT_NAME \"PROJECT NAME\" true true false 125 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_NAME,0,150;PROJECT_STATUS \"PROJECT STATUS\" true true false 25 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_STATUS,0,25;PROJECT_START \"PROJECT START\" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_START,-1,-1;PROJECT_END \"PROJECT END\" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_END,-1,-1;PRIMARY_FUNDING_SOURCE \"PRIMARY_FUNDING_SOURCE\" true true false 130 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PRIMARY_FUNDING_SOURCE,0,130;PRIMARY_FUNDING_ORG \"PRIMARY_FUNDING_ORG\" true true false 130 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PRIMARY_FUNDING_ORG,0,130;IMPLEMENTING_ORG \"IMPLEMENTING_ORG\" true true false 55 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,IMPLEMENTING_ORG,0,150;BatchID_p \"Batch ID\" true true false 40 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,BATCHID_p,0,40;Val_Status_p \"Validation Status\" true true false 15 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,VAL_STATUS_p,0,15;Val_Message_p \"Validation Message\" true true false 15 Text 0 0,First,#;Val_RunDate_p \"Validation Run Date\" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,VAL_RUNDATE_p,-1,-1;Review_Status_p \"Review Status\" true true false 15 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,REVIEW_STATUS_p,0,15;Review_Message_p \"Review Message\" true true false 15 Text 0 0,First,#;Review_RunDate_p \"Review Run Date\" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,REVIEW_RUNDATE_p,-1,-1;Source \"Source\" true true false 65 Text 0 0,First,#;GlobalID \"PROJECTID\" true true false 38 Guid 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,GlobalID,-1,-1")

    # # make multipart into single part
    # arcpy.management.MultipartToSinglepart(in_features = CNRA_Projects_Select,
    #                                                     out_feature_class = singlepart_output)

    # arcpy.management.MultipartToSinglepart(in_features = Treat_n_harves_Project_SpatialJoin1_3_,
    #                                                     out_feature_class = singlepart_output2)

    #    # Process: Append (2) (Append) (management)
    #     if Treat_n_harves_Project_SpatialJoin1_2_ and Updated_Datasets_4_ and Value:
    #         Output_Features = arcpy.management.Append(inputs=singlepart_output,
    #                                                   target=singlepart_output2,
    #                                                   schema_type="NO_TEST",
    #                                                   field_mapping="PROJECTID_USER \"PROJECT ID USER\" true true false 40 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECTID_USER,0,50;AGENCY \"AGENCY/DEPARTMENT\" true true false 55 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,AGENCY,0,150;ORG_ADMIN_p \"ORG DATA STEWARD\" true true false 55 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,ORG_ADMIN_p,0,150;PROJECT_CONTACT \"PROJECT CONTACT\" true true false 40 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_CONTACT,0,100;PROJECT_EMAIL \"PROJECT EMAIL\" true true false 40 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_EMAIL,0,100;ADMINISTERING_ORG \"ADMINISTERING ORG\" true true false 55 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,ADMINISTERING_ORG,0,150;PROJECT_NAME \"PROJECT NAME\" true true false 125 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_NAME,0,150;PROJECT_STATUS \"PROJECT STATUS\" true true false 25 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_STATUS,0,25;PROJECT_START \"PROJECT START\" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_START,-1,-1;PROJECT_END \"PROJECT END\" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_END,-1,-1;PRIMARY_FUNDING_SOURCE \"PRIMARY_FUNDING_SOURCE\" true true false 130 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PRIMARY_FUNDING_SOURCE,0,130;PRIMARY_FUNDING_ORG \"PRIMARY_FUNDING_ORG\" true true false 130 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PRIMARY_FUNDING_ORG,0,130;IMPLEMENTING_ORG \"IMPLEMENTING_ORG\" true true false 55 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,IMPLEMENTING_ORG,0,150;BatchID_p \"Batch ID\" true true false 40 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,BATCHID_p,0,40;Val_Status_p \"Validation Status\" true true false 15 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,VAL_STATUS_p,0,15;Val_Message_p \"Validation Message\" true true false 15 Text 0 0,First,#;Val_RunDate_p \"Validation Run Date\" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,VAL_RUNDATE_p,-1,-1;Review_Status_p \"Review Status\" true true false 15 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,REVIEW_STATUS_p,0,15;Review_Message_p \"Review Message\" true true false 15 Text 0 0,First,#;Review_RunDate_p \"Review Run Date\" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,REVIEW_RUNDATE_p,-1,-1;Source \"Source\" true true false 65 Text 0 0,First,#;GlobalID \"PROJECTID\" true true false 38 Guid 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,GlobalID,-1,-1")

    #   buffer inputs
    buffered_treat = arcpy.analysis.Buffer(treat_spatialjoin, treat_buffered, 10)
    buffered_projects = arcpy.analysis.Buffer(
        CNRA_Projects_Select, project_buffered, 10
    )

    # Process: Append (2) (Append) (management)
    if Treat_n_harves_Project_SpatialJoin1_2_ and Updated_Datasets_4_ and Value:
        project_poly = arcpy.management.Append(
            inputs=buffered_projects,
            target=buffered_treat,
            schema_type="NO_TEST",
            field_mapping='PROJECTID_USER "PROJECT ID USER" true true false 40 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECTID_USER,0,50;AGENCY "AGENCY/DEPARTMENT" true true false 55 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,AGENCY,0,150;ORG_ADMIN_p "ORG DATA STEWARD" true true false 55 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,ORG_ADMIN_p,0,150;PROJECT_CONTACT "PROJECT CONTACT" true true false 40 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_CONTACT,0,100;PROJECT_EMAIL "PROJECT EMAIL" true true false 40 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_EMAIL,0,100;ADMINISTERING_ORG "ADMINISTERING ORG" true true false 55 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,ADMINISTERING_ORG,0,150;PROJECT_NAME "PROJECT NAME" true true false 125 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_NAME,0,150;PROJECT_STATUS "PROJECT STATUS" true true false 25 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_STATUS,0,25;PROJECT_START "PROJECT START" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_START,-1,-1;PROJECT_END "PROJECT END" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_END,-1,-1;PRIMARY_FUNDING_SOURCE "PRIMARY_FUNDING_SOURCE" true true false 130 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PRIMARY_FUNDING_SOURCE,0,130;PRIMARY_FUNDING_ORG "PRIMARY_FUNDING_ORG" true true false 130 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PRIMARY_FUNDING_ORG,0,130;IMPLEMENTING_ORG "IMPLEMENTING_ORG" true true false 55 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,IMPLEMENTING_ORG,0,150;BatchID_p "Batch ID" true true false 40 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,BATCHID_p,0,40;Val_Status_p "Validation Status" true true false 15 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,VAL_STATUS_p,0,15;Val_Message_p "Validation Message" true true false 15 Text 0 0,First,#;Val_RunDate_p "Validation Run Date" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,VAL_RUNDATE_p,-1,-1;Review_Status_p "Review Status" true true false 15 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,REVIEW_STATUS_p,0,15;Review_Message_p "Review Message" true true false 15 Text 0 0,First,#;Review_RunDate_p "Review Run Date" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,REVIEW_RUNDATE_p,-1,-1;Source "Source" true true false 65 Text 0 0,First,#;GlobalID "PROJECTID" true true false 38 Guid 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,GlobalID,-1,-1',
        )

    # Process: 9c Transform Check Duplicates (9c Transform Check Duplicates) (PC414CWIMillionAcres)
    if Treat_n_harves_Project_SpatialJoin1_2_ and Updated_Datasets_4_ and Value:
        TransformCheck(
            Input_Table=project_poly.__str__().format(**locals(), **globals()),
            Output_Duplicates=Output_Duplicate_Projects.__str__().format(
                **locals(), **globals()
            ),
        )

    # if __name__ == "__main__":
    #     runner(workspace, scratch_workspace, TransformProjects, "*argv[1:]")
    # # Global Environment settings
    #     with arcpy.EnvManager(
    #     extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""",  outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""",
    #     preserveGlobalIds=True,
    #     qualifiedFieldNames=False,
    #     scratchWorkspace=scratch_workspace,
    #     transferDomains=True,
    #     transferGDBAttributeProperties=True,
    #     workspace=workspace):
    #         TransformProjects(*argv[1:])
