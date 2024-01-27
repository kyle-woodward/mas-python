"""
# Description: This is the start of the dataset transformation scripts.
#              This script is not complete.  This script will transform
#              the flat appended files into the relational database.
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import arcpy
from scripts._9c_Transform_Check_Duplicates import TransformCheck
# from sys import argv
from datetime import datetime
import time
from .utils import init_gdb, delete_scratch_files, runner
# import os

original_gdb, workspace, scratch_workspace = init_gdb()

Value2 = time.strftime("%Y%m%d-%H%M%S").replace("-", "")


def TransformTreatments(
    treatment_poly,
    Input_Features,
    CNRA_Treatments,
    Output_Duplicate_Treatments=os.path.join(
        scratch_workspace, rf"Duplicate_Treatments_{Value2}"
    ),
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

        # date value
        Value = datetime.utcnow().strftime("%Y-%m-%d").replace("-", "")

        # scratch outputs
        CNRA_Treatments_Select = os.path.join(scratch_workspace, "CNRA_Treatments_Select")
        treat_buffered2 = os.path.join(scratch_workspace, "treatment_buffered2")
        # treat_spatialjoin2 = os.path.join(scratch_workspace, "treat_spatialjoin2")
        project_buffered2 = os.path.join(scratch_workspace, "project_buffered2")

        # workspace outputs
        # Treatment = os.path.join(workspace, 'f_Transformed', fr"{Input_Features}_transformed_{Value}")

        # # workspace outputs
        # Treatment2 = os.path.join(workspace, 'f_Transformed', fr"Treatment_poly_{Value}")

        # Process: Select (7) (Select) (analysis)
        CNRA_Treatments_Select = arcpy.analysis.Select(
            in_features=CNRA_Treatments.__str__().format(**locals(), **globals()),
            out_feature_class=CNRA_Treatments_Select,
        )

        # Process: Dissolve (2) (Dissolve) (management)
        if Value:
            arcpy.management.Dissolve(
                in_features=Input_Features.__str__().format(**locals(), **globals()),
                out_feature_class=treatment_poly,
                dissolve_field=[
                    "TRMTID_USER",
                    "PROJECTID",
                    "PROJECTNAME_",
                    "ORG_ADMIN_t",
                    "PRIMARY_OWNERSHIP_GROUP",
                    "PRIMARY_OBJECTIVE",
                    "SECONDARY_OBJECTIVE",
                    "TERTIARY_OBJECTIVE",
                    "TREATMENT_STATUS",
                    "COUNTY",
                    "IN_WUI",
                    "REGION",
                    "TREATMENT_START",
                    "TREATMENT_END",
                    "RETREATMENT_DATE_EST",
                    "TREATMENT_NAME",
                    "BatchID",
                    "Val_Status_t",
                    "Val_Message_t",
                    "Val_RunDate_t",
                    "Review_Status_t",
                    "Review_Message_t",
                    "Review_RunDate_t",
                    "Dataload_Status_t",
                    "Dataload_Msg_t",
                    "PROJECTID_USER",
                    "Source",
                ],
            )

        # Process: Add Field (2) (Add Field) (management)
        if Value:
            Transform_Treatments_Dissolve = arcpy.management.AddField(
                in_table=treatment_poly,
                field_name="GlobalID",
                field_type="GUID",
                field_alias="TREATMENTID",
            )

        # Process: Add Global IDs (3) (Add Global IDs) (management)
        if Transform_Treatments_Dissolve and Value:
            Updated_Datasets_3_ = arcpy.management.AddGlobalIDs(
                in_datasets=[treatment_poly]
            )

        # Process: Calculate Field (4) (Calculate Field) (management)
        if Transform_Treatments_Dissolve and Updated_Datasets_3_ and Value:
            Treat_n_harves_Treatments_SpatialJoin_2_ = arcpy.management.CalculateField(
                in_table=Transform_Treatments_Dissolve,
                field="GlobalID",
                expression="!GlobalID_1!",
            )

        # # Process: Delete Field (2) (Delete Field) (management)
        # if Transform_Treatments_Dissolve and Updated_Datasets_3_ and Value:
        #     Treatment_2_ = arcpy.management.DeleteField(in_table=Treat_n_harves_Treatments_SpatialJoin_2_,
        #                                                 drop_field=["GlobalID_1"])

        # # Process: Append (Append) (management)
        # if Transform_Treatments_Dissolve and Updated_Datasets_3_ and Value:
        #     Treatment_poly_20221229 = arcpy.management.Append(inputs=[CNRA_Treatments_Select],
        #                                                       target=Treatment_2_,
        #                                                       schema_type="NO_TEST",
        #                                                       field_mapping="TRMTID_USER \"TREATMENT ID USER\" true true false 40 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,TRMTID_USER,0,50;PROJECTID \"PROJECT ID\" true true false 50 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,PROJECTID,-1,-1;PROJECTNAME_ \"PROJECT NAME\" true true false 125 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,PROJECTNAME_,0,150;ORG_ADMIN_t \"ORG DATA STEWARD\" true true false 255 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,ORG_ADMIN_t,0,150;PRIMARY_OWNERSHIP_GROUP \"PRIMARY OWNERSHIP GROUP\" true true false 25 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,PRIMARY_OWNERSHIP_GROUP,0,25;PRIMARY_OBJECTIVE \"PRIMARY OBJECTIVE\" true true false 65 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,PRIMARY_OBJECTIVE,0,65;SECONDARY_OBJECTIVE \"SECONDARY OBJECTIVE\" true true false 65 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,SECONDARY_OBJECTIVE,0,65;TERTIARY_OBJECTIVE \"TERTIARY OBJECTIVE\" true true false 65 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,TERTIARY_OBJECTIVE,0,65;TREATMENT_STATUS \"TREATMENT STATUS\" true true false 25 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,TREATMENT_STATUS,0,25;COUNTY \"COUNTY\" true true false 25 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,COUNTY,0,35;IN_WUI \"IN WUI\" true true false 30 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,IN_WUI,0,30;REGION \"TASK FORCE REGION\" true true false 25 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,REGION,0,25;TREATMENT_START \"TREATMENT START\" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,TREATMENT_START,-1,-1;TREATMENT_END \"TREATMENT END\" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,TREATMENT_END,-1,-1;RETREATMENT_DATE_EST \"RETREATMENT DATE ESTIMATE\" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,RETREATMENT_DATE_EST,-1,-1;TREATMENT_NAME \"TREATMENT NAME\" true true false 125 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,TREATMENT_NAME,0,150;BatchID \"BATCH ID (TREATMENT)\" true true false 40 Text 0 0,First,#;Val_Status_t \"Validation Status\" true true false 15 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,VAL_STATUS_t,0,15;Val_Message_t \"Validation Message\" true true false 15 Text 0 0,First,#;Val_RunDate_t \"Validation Run Date\" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,VAL_RUNDATE_t,-1,-1;Review_Status_t \"Review Status\" true true false 15 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,REVIEW_STATUS_t,0,15;Review_Message_t \"Review Message\" true true false 15 Text 0 0,First,#;Review_RunDate_t \"Review Run Date\" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,REVIEW_RUNDATE_t,-1,-1;Dataload_Status_t \"Dataload Status\" true true false 15 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,DATALOAD_STATUS_t,0,15;Dataload_Msg_t \"Dataload Message\" true true false 15 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,DATALOAD_MSG_t,0,15;PROJECTID_USER \"PROJECT ID USER\" true true false 40 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,PROJECTID_USER,0,50;Source \"Source\" true true false 65 Text 0 0,First,#;GlobalID \"TREATMENTID\" true true false 0 Guid 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,GlobalID,-1,-1"
        #                                                       )

        #   buffer inputs
        buffered_treat2 = arcpy.analysis.Buffer(
            Treat_n_harves_Treatments_SpatialJoin_2_, treat_buffered2, 10
        )
        buffered_projects2 = arcpy.analysis.Buffer(
            CNRA_Treatments_Select, project_buffered2, 10
        )

        # Process: Append (Append) (management)
        if Transform_Treatments_Dissolve and Updated_Datasets_3_ and Value:
            treatment_poly = arcpy.management.Append(
                inputs=buffered_projects2,
                target=buffered_treat2,
                schema_type="NO_TEST",
                field_mapping='TRMTID_USER "TREATMENT ID USER" true true false 40 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,TRMTID_USER,0,50;PROJECTID "PROJECT ID" true true false 50 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,PROJECTID,-1,-1;PROJECTNAME_ "PROJECT NAME" true true false 125 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,PROJECTNAME_,0,150;ORG_ADMIN_t "ORG DATA STEWARD" true true false 255 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,ORG_ADMIN_t,0,150;PRIMARY_OWNERSHIP_GROUP "PRIMARY OWNERSHIP GROUP" true true false 25 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,PRIMARY_OWNERSHIP_GROUP,0,25;PRIMARY_OBJECTIVE "PRIMARY OBJECTIVE" true true false 65 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,PRIMARY_OBJECTIVE,0,65;SECONDARY_OBJECTIVE "SECONDARY OBJECTIVE" true true false 65 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,SECONDARY_OBJECTIVE,0,65;TERTIARY_OBJECTIVE "TERTIARY OBJECTIVE" true true false 65 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,TERTIARY_OBJECTIVE,0,65;TREATMENT_STATUS "TREATMENT STATUS" true true false 25 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,TREATMENT_STATUS,0,25;COUNTY "COUNTY" true true false 25 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,COUNTY,0,35;IN_WUI "IN WUI" true true false 30 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,IN_WUI,0,30;REGION "TASK FORCE REGION" true true false 25 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,REGION,0,25;TREATMENT_START "TREATMENT START" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,TREATMENT_START,-1,-1;TREATMENT_END "TREATMENT END" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,TREATMENT_END,-1,-1;RETREATMENT_DATE_EST "RETREATMENT DATE ESTIMATE" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,RETREATMENT_DATE_EST,-1,-1;TREATMENT_NAME "TREATMENT NAME" true true false 125 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,TREATMENT_NAME,0,150;BatchID "BATCH ID (TREATMENT)" true true false 40 Text 0 0,First,#;Val_Status_t "Validation Status" true true false 15 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,VAL_STATUS_t,0,15;Val_Message_t "Validation Message" true true false 15 Text 0 0,First,#;Val_RunDate_t "Validation Run Date" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,VAL_RUNDATE_t,-1,-1;Review_Status_t "Review Status" true true false 15 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,REVIEW_STATUS_t,0,15;Review_Message_t "Review Message" true true false 15 Text 0 0,First,#;Review_RunDate_t "Review Run Date" true true false 8 Date 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,REVIEW_RUNDATE_t,-1,-1;Dataload_Status_t "Dataload Status" true true false 15 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,DATALOAD_STATUS_t,0,15;Dataload_Msg_t "Dataload Message" true true false 15 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,DATALOAD_MSG_t,0,15;PROJECTID_USER "PROJECT ID USER" true true false 40 Text 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,PROJECTID_USER,0,50;Source "Source" true true false 65 Text 0 0,First,#;GlobalID "TREATMENTID" true true false 0 Guid 0 0,First,#,C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CNRA_Treatments_20221_Select1,GlobalID,-1,-1',
            )

        # Process: 9c Transform Check Duplicates (9c Transform Check Duplicates) (PC414CWIMillionAcres)
        if Transform_Treatments_Dissolve and Updated_Datasets_3_ and Value:
            TransformCheck(
                Input_Table=treatment_poly.__str__().format(**locals(), **globals()),
                Output_Duplicates=Output_Duplicate_Treatments.__str__().format(
                    **locals(), **globals()
                ),
            )


# if __name__ == "__main__":
#     runner(workspace, scratch_workspace, TransformTreatments, "*argv[1:]")

    # # Global Environment settings
    # with arcpy.EnvManager(
    # extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""",  outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""",
    # preserveGlobalIds=True,
    # qualifiedFieldNames=False,
    # scratchWorkspace=scratch_workspace,
    # transferDomains=True,
    # transferGDBAttributeProperties=True,
    # workspace=workspace):
    #     TransformTreatments(*argv[1:])
