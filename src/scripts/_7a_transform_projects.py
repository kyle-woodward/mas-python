"""
# Description: This is the start of the dataset transformation scripts.
#              This script is not complete.  This script will transform
#              the flat appended files into the relational database.
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""

import os
import time
import arcpy
from ._7c_transform_check_duplicates import TransformCheck
from datetime import datetime
from .utils import init_gdb, delete_scratch_files

workspace, scratch_workspace = init_gdb()

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
):
    with arcpy.EnvManager(
            workspace=workspace,
            scratchWorkspace=scratch_workspace, 
            outputCoordinateSystem= arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"), #WKID 3310
            cartographicCoordinateSystem=arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"), #WKID 3310
            extent="xmin=-374900, ymin=-604500, xmax=540100, ymax=450000, spatial_reference='NAD 1983 California (Teale) Albers (Meters)'", 
            preserveGlobalIds=True, 
            qualifiedFieldNames=False, 
            transferDomains=False, 
            transferGDBAttributeProperties=False, 
            overwriteOutput = True,
    ):

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

        CNRA_Projects_Select = arcpy.analysis.Select(
            in_features=CNRA_Projects.__str__().format(**locals(), **globals()),
            out_feature_class=CNRA_Projects_Select,
        )

        # Value = datetime.utcnow().strftime("%Y-%m-%d").replace('-','')

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

        if Value:
            Treat_n_harves_Project_SpatialJoin1_2_ = arcpy.management.AddField(
                in_table=project_poly,
                field_name="GlobalID",
                field_type="GUID",
                field_alias="PROJECTID",
            )

        if Treat_n_harves_Project_SpatialJoin1_2_ and Value:
            Updated_Datasets_4_ = arcpy.management.AddGlobalIDs(
                in_datasets=[project_poly]
            )

        if Treat_n_harves_Project_SpatialJoin1_2_ and Updated_Datasets_4_ and Value:
            treat_spatialjoin = arcpy.management.CalculateField(
                in_table=Treat_n_harves_Project_SpatialJoin1_2_,
                field="GlobalID",
                expression="!GlobalID_1!",
            )

        # if Treat_n_harves_Project_SpatialJoin1_2_ and Updated_Datasets_4_ and Value:
        #     Project_2_ = arcpy.management.DeleteField(in_table=Treat_n_harves_Project_SpatialJoin1_3_,
        #                                               drop_field=["GlobalID_1"])

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

        if Treat_n_harves_Project_SpatialJoin1_2_ and Updated_Datasets_4_ and Value:
            project_poly = arcpy.management.Append(
                inputs=buffered_projects,
                target=buffered_treat,
                schema_type="NO_TEST",
                field_mapping='PROJECTID_USER "PROJECT ID USER" true true false 40 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECTID_USER,0,50;AGENCY "AGENCY/DEPARTMENT" true true false 55 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,AGENCY,0,150;ORG_ADMIN_p "ORG DATA STEWARD" true true false 55 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,ORG_ADMIN_p,0,150;PROJECT_CONTACT "PROJECT CONTACT" true true false 40 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_CONTACT,0,100;PROJECT_EMAIL "PROJECT EMAIL" true true false 40 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_EMAIL,0,100;ADMINISTERING_ORG "ADMINISTERING ORG" true true false 55 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,ADMINISTERING_ORG,0,150;PROJECT_NAME "PROJECT NAME" true true false 125 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_NAME,0,150;PROJECT_STATUS "PROJECT STATUS" true true false 25 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_STATUS,0,25;PROJECT_START "PROJECT START" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_START,-1,-1;PROJECT_END "PROJECT END" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PROJECT_END,-1,-1;PRIMARY_FUNDING_SOURCE "PRIMARY_FUNDING_SOURCE" true true false 130 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PRIMARY_FUNDING_SOURCE,0,130;PRIMARY_FUNDING_ORG "PRIMARY_FUNDING_ORG" true true false 130 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,PRIMARY_FUNDING_ORG,0,130;IMPLEMENTING_ORG "IMPLEMENTING_ORG" true true false 55 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,IMPLEMENTING_ORG,0,150;BatchID_p "Batch ID" true true false 40 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,BATCHID_p,0,40;Val_Status_p "Validation Status" true true false 15 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,VAL_STATUS_p,0,15;Val_Message_p "Validation Message" true true false 15 Text 0 0,First,#;Val_RunDate_p "Validation Run Date" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,VAL_RUNDATE_p,-1,-1;Review_Status_p "Review Status" true true false 15 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,REVIEW_STATUS_p,0,15;Review_Message_p "Review Message" true true false 15 Text 0 0,First,#;Review_RunDate_p "Review Run Date" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,REVIEW_RUNDATE_p,-1,-1;Source "Source" true true false 65 Text 0 0,First,#;GlobalID "PROJECTID" true true false 38 Guid 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Projects_2022121_Select,GlobalID,-1,-1',
            )

        if Treat_n_harves_Project_SpatialJoin1_2_ and Updated_Datasets_4_ and Value:
            TransformCheck(
                Input_Table=project_poly.__str__().format(**locals(), **globals()),
                Output_Duplicates=Output_Duplicate_Projects.__str__().format(
                    **locals(), **globals()
                ),
            )
