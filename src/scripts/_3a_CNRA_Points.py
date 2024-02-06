"""
# Description: Converts the California Department of Natural Resources' 
#              Fuels Treatments Tracker points dataset 
#              into the Task Force standardized schema.  Dataset
#              is enriched with vegetation, ownership, county, WUI, 
#              Task Force Region, and year.             
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import time
import datetime
import arcpy
from ._1_assign_domains import AssignDomains
from ._3_calculate_category import Category
from ._4_counts_to_mas import CountsToMAS
from ._3_enrichments_pts import enrich_points
from ._3_standardize_domains import StandardizeDomains
from .utils import init_gdb, delete_scratch_files


date_id = datetime.datetime.now().strftime("%Y-%m-%d").replace("-", "")  # like 20221216

original_gdb, workspace, scratch_workspace = init_gdb()

def CNRA_pts_Model(
    input_pt_fc, Activity_Table, Project_Poly, WFR_TF_Template, output_pt_enriched
):
    start = time.time()
    print(f"Start Time {time.ctime()}")
    
    # Model Environment settings
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

        print("Part 1 Prepare Features")
        # Process: Copy Features (9) (Copy Features) (management)
        Input_Features_1 = os.path.join(
            scratch_workspace, "CNRA_Treatment_Point"
        )
        arcpy.management.CopyFeatures(input_pt_fc, Input_Features_1)
        # Input_Features_3 = arcpy.DefineProjection_management(Input_Features_2, "NAD 1983 California (Teale) Albers (Meters)") # WKID 3310
        
        # ## Attribute Validation
        # # Process: Calculate Project ID User Field (4) (Calculate Field) (management)
        # Input_Features_2a = arcpy.management.CalculateField(
        #     in_table=Input_Features_1,
        #     field="TRMTID_USER",
        #     expression="ifelse(!TRMTID_USER!, !TREATMENT_NAME!)",
        #     code_block="""def ifelse(ID, NAME):
        #                     if ID != None or ID == '' or ID == ' ':
        #                         return NAME
        #                     else:
        #                         return ID""",
        # )

        # ## Attribute Validation
        # # Process: Calculate Project ID User Field (4) (Calculate Field) (management)
        # Input_Features_2B = arcpy.management.CalculateField(
        #     in_table=Input_Features_2a,
        #     field="PROJECTID_USER",
        #     expression="ifelse(!PROJECTID_USER!, !TRMTID_USER!)",
        #     code_block="""def ifelse(ID, NAME):
        #                     if ID != None or ID == '' or ID == ' ':
        #                         return NAME
        #                     else:
        #                         return ID""",
        # )

        ## Eliminates numaric Project ID's that may be the same as in other datasets
        # Process: Calculate Project ID User Field (4) (Calculate Field) (management)
        Input_Features_2C = arcpy.management.CalculateField(
            in_table=Input_Features_1,
            field="PROJECTID_USER",
            expression="!PROJECTID_USER![:45]+'-CNRA'",
        )

        ## Eliminates numaric Treatment ID's that may be the same as in other datasets
        # Process: Calculate Treatment ID User Field (3) (Calculate Field) (management)
        Input_Features_3a = arcpy.management.CalculateField(
            in_table=Input_Features_2C,
            field="TRMTID_USER",
            expression="!TRMTID_USER![:45]+'-CNRA'",
        )

        print("Part 2 Prepare Activity Table")
        # Process: Export Table (Export Table) (conversion)
        Output_Table_1 = os.path.join(scratch_workspace, "CNRA_Activity_Table")
        arcpy.conversion.ExportTable(Activity_Table, Output_Table_1)

        # Process: Calculate Field (Calculate Field) (management)
        Output_Table_2 = arcpy.management.CalculateField(
            in_table=Output_Table_1,
            field="TREATMENTID_",
            expression="ifelse(!TREATMENTID_!,!TREATMENTID_LN!,!TREATMENTID_PT!)",
            code_block="""def ifelse(poly, ln, pt):
                            if ln != None:
                                return ln
                            if pt != None:
                                return pt
                            else:
                                return poly""",
        )

        # Process: Calculate Field (Calculate Field) (management)
        Output_Table_3A = arcpy.management.CalculateField(
            in_table=Output_Table_2,
            field="TRMTID_USER",
            expression="ifelse(!TRMTID_USER!, !ACTIVID_USER!)",
            code_block="""def ifelse(ID, Act):
                            if ID is None:
                                return Act
                            """,
            expression_type = "PYTHON3"
        )
        
        # Process: Calculate Field (Calculate Field) (management)
        Output_Table_3B = arcpy.management.CalculateField(
            in_table=Output_Table_3A,
            field="TRMTID_USER",
            expression="ifelse(!TRMTID_USER!, !ACTIVITY_NAME!)",
            code_block="""def ifelse(ID, Act):
                            if ID is None:
                                return Act
                            """,
            expression_type = "PYTHON3"
        )
        
        ## To eliminate miliseconds in date field
        MiliSeconds_1 = arcpy.AlterField_management(Output_Table_3B, "ACTIVITY_END", "ACTIVITY_END_1")
        MiliSeconds_2 = arcpy.AddField_management(MiliSeconds_1, "ACTIVITY_END", "DATEONLY")
        MiliSeconds_3 = arcpy.CalculateField_management(MiliSeconds_2, "ACTIVITY_END", "!ACTIVITY_END_1!", "PYTHON3")
        MiliSeconds_4 = arcpy.DeleteField_management(MiliSeconds_3, "ACTIVITY_END_1")
        MiliSeconds_5 = arcpy.AlterField_management(MiliSeconds_4, "ACTIVITY_START", "ACTIVITY_START_1")
        MiliSeconds_6 = arcpy.AddField_management(MiliSeconds_5, "ACTIVITY_END", "DATEONLY")
        MiliSeconds_7 = arcpy.CalculateField_management(MiliSeconds_6, "ACTIVITY_START", "!ACTIVITY_START_1!", "PYTHON3")
        MiliSeconds_8 = arcpy.DeleteField_management(MiliSeconds_7, "ACTIVITY_START_1")

        # Process: Create Table (Create Table) (management)
        WFRTF_Act_Template_1 = arcpy.management.CreateTable(
            scratch_workspace, "CNRA_Activity_Table_2"
        )

        # Process: Add Activities Fields (multiple) (Add Fields (multiple)) (management)
        WFRTF_Act_Template_2 = arcpy.management.AddFields(
            WFRTF_Act_Template_1,
            [
                ["ACTIVID_USER", "TEXT", "ACTIVITYID USER", "50", "", ""],
                ["TREATMENTID_", "TEXT", "TREATMENTID", "50", "", ""],
                ["ORG_ADMIN_a", "TEXT", "ORG DATA STEWARD", "150", "", ""],
                ["ACTIVITY_DESCRIPTION", "TEXT", "ACTIVITY DESCRIPTION", "70", "", ""],
                ["ACTIVITY_CAT", "TEXT", "ACTIVITY CATEGORY", "40", "", ""],
                ["BROAD_VEGETATION_TYPE", "TEXT", "BROAD VEGETATION TYPE", "50", "", ""],
                ["BVT_USERD", "TEXT", "IS BVT USER DEFINED", "3", "", ""],
                ["ACTIVITY_STATUS", "TEXT", "ACTIVITY STATUS", "25", "", ""],
                ["ACTIVITY_QUANTITY", "DOUBLE", "ACTIVITY QUANTITY", "8", "", ""],
                ["ACTIVITY_UOM", "TEXT", "ACTIVITY UNITS", "15", "", ""],
                ["ACTIVITY_START", "DATE", "ACTIVITY START", "8", "", ""],
                ["ACTIVITY_END", "DATE", "ACTIVITY END", "8", "", ""],
                ["ADMIN_ORG_NAME", "TEXT", "ADMINISTRATION ORGANIZATION NAME", "150", "", ""],
                ["IMPLEM_ORG_NAME", "TEXT", "IMPLEMENTATION ORGANIZATION NAME", "150", "", ""],
                ["PRIMARY_FUND_SRC_NAME", "TEXT", "PRIMARY FUND SOURCE NAME", "100", "", ""],
                ["PRIMARY_FUND_ORG_NAME", "TEXT", "PRIMARY FUND ORGANIZATION NAME", "100", "", ""],
                ["SECONDARY_FUND_SRC_NAME", "TEXT", "SECONDARY FUND SOURCE NAME", "100", "", ""],
                ["SECONDARY_FUND_ORG_NAME", "TEXT", "SECONDARY FUND ORGANIZATION NAME", "100", "", ""],
                ["TERTIARY_FUND_SRC_NAME", "TEXT", "TERTIARY FUND SOURCE NAME", "100", "", ""],
                ["TERTIARY_FUND_ORG_NAME", "TEXT", "TERTIARY FUND ORGANIZATION NAME", "100", "", ""],
                ["ACTIVITY_PRCT", "SHORT", "ACTIVITY PERCENT", "3", "", ""],
                ["RESIDUE_FATE", "TEXT", "RESIDUE FATE", "35", "", ""],
                ["RESIDUE_FATE_QUANTITY", "DOUBLE", "RESIDUE FATE QUANTITY", "8", "", ""],
                ["RESIDUE_FATE_UNITS", "TEXT", "RESIDUE FATE UNITS", "5", "", ""],
                ["ACTIVITY_NAME", "TEXT", "ACTIVITY NAME", "150", "", ""],
                ["VAL_STATUS_a", "TEXT", "VALIDATION STATUS", "15", "", ""],
                ["VAL_MSG_a", "TEXT", "VALIDATION MESSAGE", "15", "", ""],
                ["VAL_RUNDATE_a", "DATE", "VALIDATION RUN DATE", "8", "", ""],
                ["REVIEW_STATUS_a", "TEXT", "REVIEW STATUS", "15", "", ""],
                ["REVIEW_MSG_a", "TEXT", "REVIEW MESSAGE", "15", "", ""],
                ["REVIEW_RUNDATE_a", "DATE", "REVIEW RUN DATE", "8", "", ""],
                ["DATALOAD_STATUS_a", "TEXT", "DATALOAD STATUS", "15", "", ""],
                ["DATALOAD_MSG_a", "TEXT", "DATALOAD MESSAGE", "15", "", ""],
                ["Source", "TEXT", "Source", "65", "", ""],
                ["Year", "LONG", "Calendar Year", "", "", ""],
                ["Year_txt", "TEXT", "Year as Text", "255", "", ""],
                ["Act_Code", "LONG", "USFS Activity Code", "", "", ""],
                ["Crosswalk", "TEXT", "Crosswalk Activities", "150", "", ""],
                ["Federal_FY", "LONG", "Federal FY", "", "", ""],
                ["State_FY", "LONG", "State FY", "", "", ""],
                ["TRMTID_USER", "TEXT", "", "50", "", ""],
                ["BATCHID_a", "TEXT", "BATCH ID (ACTIVITY)", "40", "", ""],
                ["TRMT_GEOM", "TEXT", "TREATMENT GEOMETRY", "10", "", ""],
                ["COUNTS_TO_MAS", "TEXT", "COUNTS TOWARDS MAS", "3", "", ""],
            ],
        )

        # Process: Append (4) (Append) (management)
        ## Appending the CNRA table to the table we created ensures the schema is correct
        Output_Table_4 = arcpy.management.Append(
            inputs=[Output_Table_3B], 
            target=WFRTF_Act_Template_2, 
            schema_type="NO_TEST", 
            field_mapping="", 
            subtype="", 
            expression=""
            )
        
        # # Append with Field Mapping if Append wiht NO_TEST doesn't work
        # Output_Table_4 = arcpy.management.Append(
        #     [Output_Table_3],
        #     WFRTF_Act_Template_2,
        #     schema_type="NO_TEST",
        #     field_mapping="""'ACTIVID_USER "ACTIVITYID USER" true true false 50 Text 0 0,First,#,output_pt_enriched,ACTIVID_USER,0,50;
        #                     TREATMENTID_ "TREATMENTID" true true false 50 Text 0 0,First,#,output_pt_enriched,TREATMENTID_,0,50;
        #                     ORG_ADMIN_a "ORG DATA STEWARD" true true false 150 Text 0 0,First,#,output_pt_enriched,ORG_ADMIN_a,0,150;
        #                     ACTIVITY_DESCRIPTION "ACTIVITY DESCRIPTION" true true false 70 Text 0 0,First,#,output_pt_enriched,ACTIVITY_DESCRIPTION,0,70;
        #                     ACTIVITY_CAT "ACTIVITY CATEGORY" true true false 40 Text 0 0,First,#,output_pt_enriched,ACTIVITY_CAT,0,40;
        #                     BROAD_VEGETATION_TYPE "BROAD VEGETATION TYPE" true true false 50 Text 0 0,First,#,output_pt_enriched,BROAD_VEGETATION_TYPE,0,50;
        #                     BVT_USERD "IS BVT USER DEFINED" true true false 3 Text 0 0,First,#,output_pt_enriched,BVT_USERD,0,3;
        #                     ACTIVITY_STATUS "ACTIVITY STATUS" true true false 25 Text 0 0,First,#,output_pt_enriched,ACTIVITY_STATUS,0,25;
        #                     ACTIVITY_QUANTITY "ACTIVITY QUANTITY" true true false 8 Double 0 0,First,#,output_pt_enriched,ACTIVITY_QUANTITY,-1,-1;
        #                     ACTIVITY_UOM "ACTIVITY UNITS" true true false 15 Text 0 0,First,#,output_pt_enriched,ACTIVITY_UOM,0,15;
        #                     ACTIVITY_START "ACTIVITY START" true true false 8 Date 0 0,First,#,output_pt_enriched,ACTIVITY_START,-1,-1;
        #                     ACTIVITY_END "ACTIVITY END" true true false 8 Date 0 0,First,#,output_pt_enriched,ACTIVITY_END,-1,-1;
        #                     ADMIN_ORG_NAME "ADMINISTRATION ORGANIZATION NAME" true true false 150 Text 0 0,First,#,output_pt_enriched,ADMIN_ORG_NAME,0,150;
        #                     IMPLEM_ORG_NAME "IMPLEMENTATION ORGANIZATION NAME" true true false 150 Text 0 0,First,#,output_pt_enriched,IMPLEM_ORG_NAME,0,150;
        #                     PRIMARY_FUND_SRC_NAME "PRIMARY FUND SOURCE NAME" true true false 100 Text 0 0,First,#,output_pt_enriched,PRIMARY_FUND_SRC_NAME,0,100;
        #                     PRIMARY_FUND_ORG_NAME "PRIMARY FUND ORGANIZATION NAME" true true false 100 Text 0 0,First,#,output_pt_enriched,PRIMARY_FUND_ORG_NAME,0,100;
        #                     SECONDARY_FUND_SRC_NAME "SECONDARY FUND SOURCE NAME" true true false 100 Text 0 0,First,#,output_pt_enriched,SECONDARY_FUND_SRC_NAME,0,100;
        #                     SECONDARY_FUND_ORG_NAME "SECONDARY FUND ORGANIZATION NAME" true true false 100 Text 0 0,First,#,output_pt_enriched,SECONDARY_FUND_ORG_NAME,0,100;
        #                     TERTIARY_FUND_SRC_NAME "TERTIARY FUND SOURCE NAME" true true false 100 Text 0 0,First,#,output_pt_enriched,TERTIARY_FUND_SRC_NAME,0,100;
        #                     TERTIARY_FUND_ORG_NAME "TERTIARY FUND ORGANIZATION NAME" true true false 100 Text 0 0,First,#,output_pt_enriched,TERTIARY_FUND_ORG_NAME,0,100;
        #                     ACTIVITY_PRCT "ACTIVITY PERCENT" true true false 3 Short 0 0,First,#,output_pt_enriched,ACTIVITY_PRCT,-1,-1;
        #                     RESIDUE_FATE "RESIDUE FATE" true true false 35 Text 0 0,First,#,output_pt_enriched,RESIDUE_FATE,0,35;
        #                     RESIDUE_FATE_QUANTITY "RESIDUE FATE QUANTITY" true true false 8 Double 0 0,First,#,output_pt_enriched,RESIDUE_FATE_QUANTITY,-1,-1;
        #                     RESIDUE_FATE_UNITS "RESIDUE FATE UNITS" true true false 5 Text 0 0,First,#,output_pt_enriched,RESIDUE_FATE_UNITS,0,15;
        #                     ACTIVITY_NAME "ACTIVITY NAME" true true false 150 Text 0 0,First,#,output_pt_enriched,ACTIVITY_NAME,0,150;
        #                     VAL_STATUS_a "VALIDATION STATUS" true true false 15 Text 0 0,First,#;
        #                     VAL_MSG_a "VALIDATION MESSAGE" true true false 15 Text 0 0,First,#;
        #                     VAL_RUNDATE_a "VALIDATION RUN DATE" true true false 8 Date 0 0,First,#;
        #                     REVIEW_STATUS_a "REVIEW STATUS" true true false 15 Text 0 0,First,#;
        #                     REVIEW_MSG_a "REVIEW MESSAGE" true true false 15 Text 0 0,First,#;
        #                     REVIEW_RUNDATE_a "REVIEW RUN DATE" true true false 8 Date 0 0,First,#;
        #                     DATALOAD_STATUS_a "DATALOAD STATUS" true true false 15 Text 0 0,First,#;
        #                     DATALOAD_MSG_a "DATALOAD MESSAGE" true true false 15 Text 0 0,First,#;
        #                     Source "Source" true true false 65 Text 0 0,First,#;
        #                     Year "Calendar Year" true true false 0 Long 0 0,First,#;
        #                     Year_txt "Year as Text" true true false 255 Text 0 0,First,#;
        #                     Act_Code "USFS Activity Code" true true false 0 Long 0 0,First,#;
        #                     Crosswalk "Crosswalk Activities" true true false 150 Text 0 0,First,#;
        #                     Federal_FY "Federal FY" true true false 0 Long 0 0,First,#;
        #                     State_FY "State FY" true true false 0 Long 0 0,First,#;
        #                     TRMTID_USER "TRMTID_USER" true true false 50 Text 0 0,First,#,output_pt_enriched,TRMTID_USER,0,50;
        #                     BATCHID_a "BATCH ID (ACTIVITY)" true true false 40 Text 0 0,First,#;
        #                     TRMT_GEOM "TREATMENT GEOMETRY" true true false 10 Text 0 0,First,#,output_pt_enriched,TRMT_GEOM,0,10;
        #                     COUNTS_TO_MAS "COUNTS TOWARDS MAS" true true false 3 Text 0 0,First,#,output_pt_enriched,COUNTS_TO_MAS,0,3',"""
        # )

        print("   Calculate unique Treatment ID -CNRA")
        # Process: Calculate Treatment ID User Field (4) (Calculate Field) (management)
        Output_Table_5 = arcpy.management.CalculateField(
            in_table=Output_Table_4,
            field="TRMTID_USER",
            expression="ifelse(!TRMTID_USER!)",
            code_block="""def ifelse(ID):
                            if ID != None:
                                return ID[:45]+'-CNRA'
                            """,
            expression_type = "PYTHON3"
        )

        print("Part 3 - Combine CNRA Features and Activity Table") # One to Many
        # # Process: Add Join (5) (Add Join) (management)
        # Features_Join_Activities_1 = arcpy.management.AddJoin(
        #     Input_Features_3,
        #     "TRMTID_USER",
        #     Output_Table_5,
        #     join_field="TRMTID_USER",
        #     index_join_fields="INDEX_JOIN_FIELDS",
        # )

        print("   Join Points and Table")
        # Process: Add Join (5) (Add Join) (management)
        Features_Join_Activities_1 = arcpy.management.AddJoin(
            Input_Features_3a,
            "GlobalID",
            Output_Table_4,
            join_field="TREATMENTID_",
            index_join_fields="INDEX_JOIN_FIELDS",
        )

        # Process: Copy Features (3) (Copy Features) (management)
        Features_Join_Activities_2 = os.path.join(
            scratch_workspace, "Features_Join_Activities_2"
        )
        arcpy.management.CopyFeatures(
            Features_Join_Activities_1, Features_Join_Activities_2
        )

        print("Part 4 Prepare Project Table")
        # Process: Copy Features (8) (Copy Features) (management)
        Input_Projects_1 = os.path.join(
            scratch_workspace, "Project_Poly_CopyFeatures"
        )
        arcpy.management.CopyFeatures(Project_Poly, Input_Projects_1)

        # Process: Calculate Agency CALFIRE (Calculate Field) (management)
        Input_Projects_2a = arcpy.management.CalculateField(
            Input_Projects_1,
            field="AGENCY",
            expression="ifelse(!AGENCY!)",
            code_block="""def ifelse(agency):
                            if agency == 'CALFIRE':
                                return 'CNRA'
                            else:
                                return agency""",
        )

        ## Attribute Validation
        # Process: Calculate Project ID User Field (4) (Calculate Field) (management)
        Input_Projects_2b = arcpy.management.CalculateField(
            in_table=Input_Projects_2a,
            field="PROJECTID_USER",
            expression="ifelse(!PROJECTID_USER!, !PROJECT_NAME!)",
            code_block="""def ifelse(ID, NAME):
                            if ID != None or ID == '' or ID == ' ':
                                return NAME
                            else:
                                return ID""",
        )

        print("   Calculate unique Project ID -CNRA")
        # Process: Calculate Project ID User Field (Calculate Field) (management)
        Input_Projects_3 = arcpy.management.CalculateField(
            in_table=Input_Projects_2b,
            field="PROJECTID_USER",
            expression="ifelse(!PROJECTID_USER!)",
            code_block="""def ifelse(ID):
                            if ID != None:
                                return ID[:45]+'-CNRA'
                            """,
            expression_type = "PYTHON3"
        )

        print("Part 5 Join Project Table to Features/Activites") # Many to One
        # Process: Add Join (6) (Add Join) (management)
        CNRA_Flat_1 = arcpy.management.AddJoin(
            in_layer_or_view=Features_Join_Activities_2,
            in_field="PROJECTID_USER",
            join_table=Input_Projects_3,
            join_field="PROJECTID_USER",
            index_join_fields="INDEX_JOIN_FIELDS",
        )
        print("   Copy Featurs")
        # Process: Copy Features (11) (Copy Features) (management)
        CNRA_Flat_2 = os.path.join(
            scratch_workspace, "CNRA_Treatments_pt_Copy_Laye_CopyFeatures"
        )
        arcpy.management.CopyFeatures(
            in_features=CNRA_Flat_1,
            out_feature_class=CNRA_Flat_2,
        )
        print("   Create Features")
        # Process: Create Feature Class (3) (Create Feature Class) (management)
        CNRA_Standardized_pt_Value_ = arcpy.management.CreateFeatureclass(
            out_path=scratch_workspace,
            out_name=f"CNRA_Standardized_pt_{date_id}",
            # geometry_type="MULTIPOINT",
            geometry_type="POINT",
            template=WFR_TF_Template
        )
        print("   Append")
        # Process: Append (3) (Append) (management)
        ## Appending the CNRA table to the table we created ensures the schema is correct
        CNRA_Standardized_pt_Value_3_ = arcpy.management.Append(
            inputs=[CNRA_Flat_2], 
            target=CNRA_Standardized_pt_Value_, 
            schema_type="NO_TEST", 
            field_mapping="", 
            subtype="", 
            expression=""
            )
        
        ## Append with Field Mapping if Append wiht NO_TEST doesn't work
        # CNRA_Standardized_pt_Value_3_ = arcpy.management.Append(
        #     inputs=[CNRA_Flat_2],
        #     target=CNRA_Standardized_pt_Value_,
        #     schema_type="NO_TEST",
        #     field_mapping="""'PROJECTID_USER "PROJECT ID USER" true true false 40 Text 0 0,First,#,CNRA_Flat_2,PROJECTID_USER,0,50;
        #                     AGENCY "AGENCY/DEPARTMENT" true true false 55 Text 0 0,First,#,CNRA_Flat_2,AGENCY,0,150;
        #                     ORG_ADMIN_p "ORG DATA STEWARD" true true false 55 Text 0 0,First,#,CNRA_Flat_2,ORG_ADMIN_p,0,150;
        #                     PROJECT_CONTACT "PROJECT CONTACT" true true false 40 Text 0 0,First,#,CNRA_Flat_2,PROJECT_CONTACT,0,100;
        #                     PROJECT_EMAIL "PROJECT EMAIL" true true false 40 Text 0 0,First,#,CNRA_Flat_2,PROJECT_EMAIL,0,100;
        #                     ADMINISTERING_ORG "ADMINISTERING ORG" true true false 55 Text 0 0,First,#,CNRA_Flat_2,ADMINISTERING_ORG,0,150;
        #                     PROJECT_NAME "PROJECT NAME" true true false 125 Text 0 0,First,#,CNRA_Flat_2,PROJECT_NAME,0,150;
        #                     PROJECT_STATUS "PROJECT STATUS" true true false 25 Text 0 0,First,#,CNRA_Flat_2,PROJECT_STATUS,0,25;
        #                     PROJECT_START "PROJECT START" true true false 8 Date 0 0,First,#,CNRA_Flat_2,PROJECT_START,-1,-1;
        #                     PROJECT_END "PROJECT END" true true false 8 Date 0 0,First,#,CNRA_Flat_2,PROJECT_END,-1,-1;
        #                     PRIMARY_FUNDING_SOURCE "PRIMARY_FUNDING_SOURCE" true true false 130 Text 0 0,First,#,CNRA_Flat_2,PRIMARY_FUNDING_SOURCE,0,130;
        #                     PRIMARY_FUNDING_ORG "PRIMARY_FUNDING_ORG" true true false 130 Text 0 0,First,#,CNRA_Flat_2,PRIMARY_FUNDING_ORG,0,130;
        #                     IMPLEMENTING_ORG "IMPLEMENTING_ORG" true true false 55 Text 0 0,First,#,CNRA_Flat_2,IMPLEMENTING_ORG,0,150;
        #                     LATITUDE "LATITUDE CENTROID" true true false 8 Double 0 0,First,#,CNRA_Flat_2,LATITUDE,-1,-1;
        #                     LONGITUDE "LONGITUDE CENTROID" true true false 8 Double 0 0,First,#,CNRA_Flat_2,LONGITUDE,-1,-1;
        #                     BatchID_p "Batch ID" true true false 40 Text 0 0,First,#,CNRA_Flat_2,BATCHID_p,0,40;
        #                     Val_Status_p "Validation Status" true true false 15 Text 0 0,First,#,CNRA_Flat_2,VAL_STATUS_p,0,15;
        #                     Val_Message_p "Validation Message" true true false 15 Text 0 0,First,#;
        #                     Val_RunDate_p "Validation Run Date" true true false 8 Date 0 0,First,#,CNRA_Flat_2,VAL_RUNDATE_p,-1,-1;
        #                     Review_Status_p "Review Status" true true false 15 Text 0 0,First,#,CNRA_Flat_2,REVIEW_STATUS_p,0,15;
        #                     Review_Message_p "Review Message" true true false 15 Text 0 0,First,#;
        #                     Review_RunDate_p "Review Run Date" true true false 8 Date 0 0,First,#,CNRA_Flat_2,REVIEW_RUNDATE_p,-1,-1;
        #                     Dataload_Status_p "Dataload Status" true true false 15 Text 0 0,First,#,CNRA_Flat_2,DATALOAD_STATUS_p,0,15;
        #                     Dataload_Msg_p "Dataload Message" true true false 15 Text 0 0,First,#,CNRA_Flat_2,DATALOAD_MSG_p,0,15;
        #                     TRMTID_USER "TREATMENT ID USER" true true false 40 Text 0 0,First,#,CNRA_Flat_2,TRMTID_USER,0,50;
        #                     PROJECTID "PROJECT ID" true true false 50 Text 0 0,First,#,CNRA_Flat_2,PROJECTID,-1,-1;
        #                     PROJECTNAME_ "PROJECT NAME" true true false 125 Text 0 0,First,#,CNRA_Flat_2,PROJECTNAME_,0,100;
        #                     ORG_ADMIN_t "ORG DATA STEWARD" true true false 255 Text 0 0,First,#,CNRA_Flat_2,ORG_ADMIN_t,0,150;
        #                     PRIMARY_OWNERSHIP_GROUP "PRIMARY OWNERSHIP GROUP" true true false 25 Text 0 0,First,#,CNRA_Flat_2,PRIMARY_OWNERSHIP_GROUP,0,25;
        #                     PRIMARY_OBJECTIVE "PRIMARY OBJECTIVE" true true false 65 Text 0 0,First,#,CNRA_Flat_2,PRIMARY_OBJECTIVE,0,65;
        #                     SECONDARY_OBJECTIVE "SECONDARY OBJECTIVE" true true false 65 Text 0 0,First,#,CNRA_Flat_2,SECONDARY_OBJECTIVE,0,65;
        #                     TERTIARY_OBJECTIVE "TERTIARY OBJECTIVE" true true false 65 Text 0 0,First,#,CNRA_Flat_2,TERTIARY_OBJECTIVE,0,65;
        #                     TREATMENT_STATUS "TREATMENT STATUS" true true false 25 Text 0 0,First,#,CNRA_Flat_2,TREATMENT_STATUS,0,25;
        #                     COUNTY "COUNTY" true true false 25 Text 0 0,First,#,CNRA_Flat_2,COUNTY,0,35;
        #                     IN_WUI "IN WUI" true true false 30 Text 0 0,First,#,CNRA_Flat_2,IN_WUI,0,30;
        #                     REGION "TASK FORCE REGION" true true false 25 Text 0 0,First,#,CNRA_Flat_2,REGION,0,25;
        #                     TREATMENT_AREA "TREATMENT AREA (GIS ACRES)" true true false 8 Double 0 0,First,#,CNRA_Flat_2,TREATMENT_AREA,-1,-1;
        #                     TREATMENT_START "TREATMENT START" true true false 8 Date 0 0,First,#,CNRA_Flat_2,TREATMENT_START,-1,-1;
        #                     TREATMENT_END "TREATMENT END" true true false 8 Date 0 0,First,#,CNRA_Flat_2,TREATMENT_END,-1,-1;
        #                     RETREATMENT_DATE_EST "RETREATMENT DATE ESTIMATE" true true false 8 Date 0 0,First,#,CNRA_Flat_2,RETREATMENT_DATE_EST,-1,-1;
        #                     TREATMENT_NAME "TREATMENT NAME" true true false 125 Text 0 0,First,#,CNRA_Flat_2,TREATMENT_NAME,0,150;
        #                     BatchID "BATCH ID (TREATMENT)" true true false 40 Text 0 0,First,#;
        #                     Val_Status_t "Validation Status" true true false 15 Text 0 0,First,#,CNRA_Flat_2,VAL_STATUS_t,0,15;
        #                     Val_Message_t "Validation Message" true true false 15 Text 0 0,First,#;
        #                     Val_RunDate_t "Validation Run Date" true true false 8 Date 0 0,First,#,CNRA_Flat_2,VAL_RUNDATE_t,-1,-1;
        #                     Review_Status_t "Review Status" true true false 15 Text 0 0,First,#,CNRA_Flat_2,REVIEW_STATUS_t,0,15;
        #                     Review_Message_t "Review Message" true true false 15 Text 0 0,First,#;
        #                     Review_RunDate_t "Review Run Date" true true false 8 Date 0 0,First,#,CNRA_Flat_2,REVIEW_RUNDATE_t,-1,-1;
        #                     Dataload_Status_t "Dataload Status" true true false 15 Text 0 0,First,#,CNRA_Flat_2,DATALOAD_STATUS_t,0,15;
        #                     Dataload_Msg_t "Dataload Message" true true false 15 Text 0 0,First,#,CNRA_Flat_2,DATALOAD_MSG_t,0,15;
        #                     ACTIVID_USER "ACTIVITYID USER" true true false 50 Text 0 0,First,#,CNRA_Flat_2,ACTIVID_USER,0,50;
        #                     TREATMENTID_ "TREATMENTID" true true false 50 Text 0 0,First,#,CNRA_Flat_2,TREATMENTID_,0,50;
        #                     ORG_ADMIN_a "ORG DATA STEWARD" true true false 150 Text 0 0,First,#,CNRA_Flat_2,ORG_ADMIN_a,0,150;
        #                     ACTIVITY_DESCRIPTION "ACTIVITY DESCRIPTION" true true false 70 Text 0 0,First,#,CNRA_Flat_2,ACTIVITY_DESCRIPTION,0,70;
        #                     ACTIVITY_CAT "ACTIVITY CATEGORY" true true false 40 Text 0 0,First,#,CNRA_Flat_2,ACTIVITY_CAT,0,40;
        #                     BROAD_VEGETATION_TYPE "BROAD VEGETATION TYPE" true true false 50 Text 0 0,First,#,CNRA_Flat_2,BROAD_VEGETATION_TYPE,0,50;
        #                     BVT_USERD "IS BVT USER DEFINED" true true false 3 Text 0 0,First,#,CNRA_Flat_2,BVT_USERD,0,3;
        #                     ACTIVITY_STATUS "ACTIVITY STATUS" true true false 25 Text 0 0,First,#,CNRA_Flat_2,ACTIVITY_STATUS,0,25;
        #                     ACTIVITY_QUANTITY "ACTIVITY QUANTITY" true true false 8 Double 0 0,First,#,CNRA_Flat_2,ACTIVITY_QUANTITY,-1,-1;
        #                     ACTIVITY_UOM "ACTIVITY UNITS" true true false 15 Text 0 0,First,#,CNRA_Flat_2,ACTIVITY_UOM,0,15;
        #                     ACTIVITY_START "ACTIVITY START" true true false 8 Date 0 0,First,#,CNRA_Flat_2,ACTIVITY_START,-1,-1;
        #                     ACTIVITY_END "ACTIVITY END" true true false 8 Date 0 0,First,#,CNRA_Flat_2,ACTIVITY_END,-1,-1;
        #                     ADMIN_ORG_NAME "ADMINISTRATION ORGANIZATION NAME" true true false 150 Text 0 0,First,#,CNRA_Flat_2,ADMIN_ORG_NAME,0,150;
        #                     IMPLEM_ORG_NAME "IMPLEMENTATION ORGANIZATION NAME" true true false 150 Text 0 0,First,#,CNRA_Flat_2,IMPLEM_ORG_NAME,0,150;
        #                     PRIMARY_FUND_SRC_NAME "PRIMARY FUND SOURCE NAME" true true false 100 Text 0 0,First,#,CNRA_Flat_2,PRIMARY_FUND_SRC_NAME,0,100;
        #                     PRIMARY_FUND_ORG_NAME "PRIMARY FUND ORGANIZATION NAME" true true false 100 Text 0 0,First,#,CNRA_Flat_2,PRIMARY_FUND_ORG_NAME,0,100;
        #                     SECONDARY_FUND_SRC_NAME "SECONDARY FUND SOURCE NAME" true true false 100 Text 0 0,First,#,CNRA_Flat_2,SECONDARY_FUND_SRC_NAME,0,100;
        #                     SECONDARY_FUND_ORG_NAME "SECONDARY FUND ORGANIZATION NAME" true true false 100 Text 0 0,First,#,CNRA_Flat_2,SECONDARY_FUND_ORG_NAME,0,100;
        #                     TERTIARY_FUND_SRC_NAME "TERTIARY FUND SOURCE NAME" true true false 100 Text 0 0,First,#,CNRA_Flat_2,TERTIARY_FUND_SRC_NAME,0,100;
        #                     TERTIARY_FUND_ORG_NAME "TERTIARY FUND ORGANIZATION NAME" true true false 100 Text 0 0,First,#,CNRA_Flat_2,TERTIARY_FUND_ORG_NAME,0,100;
        #                     ACTIVITY_PRCT "ACTIVITY PERCENT" true true false 8 Double 0 0,First,#,CNRA_Flat_2,ACTIVITY_PRCT,-1,-1;
        #                     RESIDUE_FATE "RESIDUE FATE" true true false 35 Text 0 0,First,#,CNRA_Flat_2,RESIDUE_FATE,0,35;
        #                     RESIDUE_FATE_QUANTITY "RESIDUE FATE QUANTITY" true true false 8 Double 0 0,First,#,CNRA_Flat_2,RESIDUE_FATE_QUANTITY,-1,-1;
        #                     RESIDUE_FATE_UNITS "RESIDUE FATE UNITS" true true false 5 Text 0 0,First,#,CNRA_Flat_2,RESIDUE_FATE_UNITS,0,5;
        #                     ACTIVITY_NAME "ACTIVITY NAME" true true false 150 Text 0 0,First,#,CNRA_Flat_2,ACTIVITY_NAME,0,150;
        #                     VAL_STATUS_a "VALIDATION STATUS" true true false 15 Text 0 0,First,#,CNRA_Flat_2,VAL_STATUS_a,0,15;
        #                     VAL_MSG_a "VALIDATION MESSAGE" true true false 15 Text 0 0,First,#,CNRA_Flat_2,VAL_MSG_a,0,15;
        #                     VAL_RUNDATE_a "VALIDATION RUN DATE" true true false 8 Date 0 0,First,#,CNRA_Flat_2,VAL_RUNDATE_a,-1,-1;
        #                     REVIEW_STATUS_a "REVIEW STATUS" true true false 15 Text 0 0,First,#,CNRA_Flat_2,REVIEW_STATUS_a,0,15;
        #                     REVIEW_MSG_a "REVIEW MESSAGE" true true false 15 Text 0 0,First,#,CNRA_Flat_2,REVIEW_MSG_a,0,15;
        #                     REVIEW_RUNDATE_a "REVIEW RUN DATE" true true false 8 Date 0 0,First,#,CNRA_Flat_2,REVIEW_RUNDATE_a,-1,-1;
        #                     DATALOAD_STATUS_a "DATALOAD STATUS" true true false 15 Text 0 0,First,#,CNRA_Flat_2,DATALOAD_STATUS_a,0,15;
        #                     DATALOAD_MSG_a "DATALOAD MESSAGE" true true false 15 Text 0 0,First,#,CNRA_Flat_2,DATALOAD_MSG_a,0,15;
        #                     Source "Source" true true false 65 Text 0 0,First,#,CNRA_Flat_2,Source,0,65;
        #                     Year "Calendar Year" true true false 4 Long 0 0,First,#,CNRA_Flat_2,Year,-1,-1;
        #                     Year_txt "Year as Text" true true false 255 Text 0 0,First,#,CNRA_Flat_2,Year_txt,0,255;
        #                     Act_Code "USFS Activity Code" true true false 4 Long 0 0,First,#,CNRA_Flat_2,Act_Code,-1,-1;
        #                     Crosswalk "Crosswalk Activities" true true false 150 Text 0 0,First,#,CNRA_Flat_2,Crosswalk,0,150;
        #                     Federal_FY "Federal FY" true true false 4 Long 0 0,First,#,CNRA_Flat_2,Federal_FY,-1,-1;
        #                     State_FY "State FY" true true false 4 Long 0 0,First,#,CNRA_Flat_2,State_FY,-1,-1',"""
        # )

        print("Part 6 Standardize and Enrich")
        print("   Standardize Domains")
        # Process: 2j Standardize Domains (3) (2j Standardize Domains) 
        Updated_Input_Table_31_ = StandardizeDomains(
            Input_Table=CNRA_Standardized_pt_Value_3_
        )
        print("   Calc Cross")
        # Process: Calculate Crosswalk (3) (Calculate Field) (management)
        CNRA_Standardized_20221108_7_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_31_,
            field="Crosswalk",
            expression="!ACTIVITY_DESCRIPTION!",
        )
        print("   Calc Category")
        # Process: 2f Calculate Category (2) (2f Calculate Category) 
        Updated_Input_Table_42_ = Category(Input_Table=CNRA_Standardized_20221108_7_)
        print("   Calc Source")

        # Process: Calculate Source (3) (Calculate Field) (management)
        Updated_Input_Table_3_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_42_, field="Source", expression='"CNRA"'
        )

        print("   Calc admin")
        # Process: Calculate Org A Null (3) (Calculate Field) (management)
        Updated_Input_Table_6_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_3_,
            field="ORG_ADMIN_a",
            expression="ifelse(!ORG_ADMIN_a!,!ORG_ADMIN_t!)",
            code_block="""def ifelse(Org_a, Org_t):
                            if Org_a is None:
                                return Org_t
                            else:
                                return Org_a""",
        )

        # Process: Calculate Org P Null (3) (Calculate Field) (management)
        Updated_Input_Table_7_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_6_,
            field="ORG_ADMIN_p",
            expression="ifelse(!ORG_ADMIN_p!,!ORG_ADMIN_t!)",
            code_block="""def ifelse(Org_p, Org_t):
                            if Org_p is None:
                                return Org_t
                            else:
                                return Org_p""",
        )
        
        # Process: Calculate Admin Null (3) (Calculate Field) (management)
        Updated_Input_Table_9_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_7_,
            field="ADMINISTERING_ORG",
            expression="ifelse(!ADMINISTERING_ORG!,!ORG_ADMIN_t!)",
            code_block="""def ifelse(Admin, Org_t):
                            if Admin is None:
                                return Org_t
                            else:
                                return Admin""",
        )

        # Process: Calculate Agency Null (3) (Calculate Field) (management)
        Updated_Input_Table_10_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_9_,
            field="AGENCY",
            expression="ifelse(!AGENCY!)",
            code_block="""def ifelse(Agency):
                            if Agency is None:
                                return 'CNRA'
                            else:
                                return Agency""",
        )

        # Process: Calculate Status (Calculate Field) (management)
        Updated_Input_Table_5_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_10_,
            field="ACTIVITY_STATUS",
            expression="ifelse(!ACTIVITY_STATUS!)",
            code_block="""def ifelse(Stat):
                            if Stat == None:
                                return "COMPLETE"
                            else:
                                return Stat""",
        )
        print("   Status")
        # Process: Calculate End Date (4) (Calculate Field) (management)
        Updated_Input_Table_5a_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_5_,
            field="ACTIVITY_END",
            expression="ifelse(!ACTIVITY_STATUS!, !ACTIVITY_START!, !ACTIVITY_END!)",
            code_block="""def ifelse(Stat, Start, End):
                            if (Stat == 'ACTIVE' or Stat == 'Active') and End == None:
                                return datetime.datetime.now()
                            if (Stat == 'COMPLETE' or Stat == 'Complete') and End == None:
                                return datetime.datetime.now()
                            if (Stat == 'PLANNED' or Stat == 'Planned') and End == None and Start == None:
                                return datetime.datetime.now()
                            if (Stat == 'PLANNED' or Stat == 'Planned') and End == None:
                                return Start
                            else:
                                return End""",
        )
        print("   Activity End Date")

        # Process: Feature To Point (Feature To Point) (management)
        Output_Feature_Class_5_ = os.path.join(
            scratch_workspace, "CNRA_Standardi_FeatureToPoin1"
        )
        arcpy.management.FeatureToPoint(
            in_features=Updated_Input_Table_5a_,
            out_feature_class=Output_Feature_Class_5_,
        )

        # Process: 7b Enrichments pts (7b Enrichments pts) 
        Pts_enrichment_Veg2_3_ = os.path.join(scratch_workspace, "Pts_enrichment_Veg2")
        enrich_points(
            enrich_pts_out=Pts_enrichment_Veg2_3_,
            enrich_pts_in=Output_Feature_Class_5_,
        )

        print("Enrichment Complete")
        # Process: Calculate GEOM (3) (Calculate Field) (management)
        Updated_Input_Table_18_ = arcpy.management.CalculateField(
            in_table=Pts_enrichment_Veg2_3_, field="TRMT_GEOM", expression="'POINT'"
        )

        print("   Counts")
        # Process: 2m Counts to MAS (2m Counts to MAS) 
        CDFW_Enriched_Ln_Table_20230801_3_ = CountsToMAS(
            Input_Table=Updated_Input_Table_18_
        )

        print("   Delete Identical")
        # Process: Delete Identical (Delete Identical) (management)
        Pts_enrichment_Veg2_Layer = arcpy.management.DeleteIdentical(
            in_dataset=CDFW_Enriched_Ln_Table_20230801_3_,
            fields=[
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
                "LATITUDE",
                "LONGITUDE",
                "BatchID_p",
                "Val_Status_p",
                "Val_Message_p",
                "Val_RunDate_p",
                "Review_Status_p",
                "Review_Message_p",
                "Review_RunDate_p",
                "Dataload_Status_p",
                "Dataload_Msg_p",
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
                "TREATMENT_AREA",
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
                "ACTIVID_USER",
                "TREATMENTID_",
                "ORG_ADMIN_a",
                "ACTIVITY_DESCRIPTION",
                "ACTIVITY_CAT",
                "BROAD_VEGETATION_TYPE",
                "BVT_USERD",
                "ACTIVITY_STATUS",
                "ACTIVITY_QUANTITY",
                "ACTIVITY_UOM",
                "ACTIVITY_START",
                "ACTIVITY_END",
                "ADMIN_ORG_NAME",
                "IMPLEM_ORG_NAME",
                "PRIMARY_FUND_SRC_NAME",
                "PRIMARY_FUND_ORG_NAME",
                "SECONDARY_FUND_SRC_NAME",
                "SECONDARY_FUND_ORG_NAME",
                "TERTIARY_FUND_SRC_NAME",
                "TERTIARY_FUND_ORG_NAME",
                "ACTIVITY_PRCT",
                "RESIDUE_FATE",
                "RESIDUE_FATE_QUANTITY",
                "RESIDUE_FATE_UNITS",
                "ACTIVITY_NAME",
                "VAL_STATUS_a",
                "VAL_MSG_a",
                "VAL_RUNDATE_a",
                "REVIEW_STATUS_a",
                "REVIEW_MSG_a",
                "REVIEW_RUNDATE_a",
                "DATALOAD_STATUS_a",
                "DATALOAD_MSG_a",
                "Source",
                "Year",
                "Year_txt",
                "Act_Code",
                "Crosswalk",
                "Federal_FY",
                "State_FY",
                "Shape",
                "TRMT_GEOM",
                "COUNTS_TO_MAS",
            ],
        )

        print("Export Final")
        # Process: Copy Enriched Features (3) (Copy Features) (management)
        arcpy.management.CopyFeatures(
            in_features=Pts_enrichment_Veg2_Layer, out_feature_class=output_pt_enriched
        )

        print("   Assign Domains")
        # Process: 2b Assign Domains (5) (2b Assign Domains) 
        output_pt_enriched = AssignDomains(in_table=output_pt_enriched)

        print("Deleting Scratch Files")
        delete_scratch_files(
            gdb=scratch_workspace, delete_fc="yes", delete_table="yes", delete_ds="yes"
        )

        end = time.time()
        print(f"Time Elapsed: {(end-start)/60} minutes")

    return output_pt_enriched 
