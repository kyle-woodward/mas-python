"""
# Description: Converts the California Department of Transportation's Fuels Treatments dataset 
#              into the Task Force standardized schema.  Dataset
#              is enriched with vegetation, ownership, county, WUI, 
#              Task Force Region, and year.             
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import datetime
start1 = datetime.datetime.now()

import os
import arcpy
from ._1_add_fields import AddFields
from ._1_assign_domains import AssignDomains
from ._3_enrichments_lines import enrich_lines
from ._3_keep_fields import KeepFields
from .utils import init_gdb, delete_scratch_files

workspace, scratch_workspace = init_gdb()
# TODO add print steps

def CalTrans(
    input_lines21,
    input_lines22,
    input_table21,
    input_table22,
    output_lines_enriched,
    delete_scratch=True
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
        overwriteOutput = True
    ):
        print(f"Start Time {start1}")

        # define intermediary objects in scratch
        CalTrans21_scratch = os.path.join(scratch_workspace, "CalTrans21_scratch")
        CalTrans22_scratch = os.path.join(scratch_workspace, "CalTrans22_scratch")
        output_lines_standardized = os.path.join(scratch_workspace, "CalTrans_standardized")
        
        ### BEGIN TOOL CHAIN
        print("Part 1 join features and tables")
        print("     step 1/8 add 2021 join")
        input_table21_join = arcpy.management.AddJoin(
            in_layer_or_view=input_lines21,
            in_field="HIghwayID",
            join_table=input_table21,
            join_field="HighwayID",
            join_type="KEEP_ALL",
            index_join_fields="INDEX_JOIN_FIELDS",
        )

        print("     step 2/8 save features")
        input_table21_join_copy = arcpy.management.CopyFeatures(
            input_table21_join, CalTrans21_scratch
        )
        
        # remove join needed to prevent modification of original data set
        arcpy.RemoveJoin_management(input_table21_join)

        Count1 = arcpy.management.GetCount(input_table21_join_copy)
        print("        input_table21_join_copy has {} records".format(Count1[0]))

        print("     step 3/8 add 2022 join")
        input_table22_join = arcpy.management.AddJoin(
            in_layer_or_view=input_lines22,
            in_field="HIghwayID",
            join_table=input_table22,
            join_field="Highway_ID",
            join_type="KEEP_ALL",
            index_join_fields="INDEX_JOIN_FIELDS",
        )

        print("     step 4/8 save features")
        input_table22_join_copy = arcpy.management.CopyFeatures(
            input_table22_join, CalTrans22_scratch
        )
        
        Count2 = arcpy.management.GetCount(input_table22_join_copy)
        print("        input_table22_join_copy has {} records".format(Count2[0]))

        # remove join needed to prevent modification of original data set
        arcpy.RemoveJoin_management(input_table22_join)

        print("     step 5/8 combine 2021 and 2022")
        print("   Appending Lines")
        CalTransLns_scratch = arcpy.management.CreateFeatureclass(
            out_path=scratch_workspace, 
            out_name="CalTransLns_scratch", 
            geometry_type="POLYLINE", 
            template=CalTrans22_scratch
            )
        
        # Use this append or the following append with field mapping depending on the situation.
        # append_1 = arcpy.management.Append(
        #     inputs=[input_table21_join_copy, input_table22_join_copy], 
        #     target=CalTransLns_scratch, 
        #     schema_type="TEST", 
        #     field_mapping=""
        # )

        append_1 = arcpy.management.Append(
            inputs=[input_table21_join_copy, input_table22_join_copy], 
            target=CalTransLns_scratch, schema_type="NO_TEST", 
            field_mapping="""DISTRICT_CODE \"DISTRICT_CODE\" true true false 255 Text 0 0,First,#,input_table22_join_copy,DISTRICT_CODE,0,255,input_table21_join_copy,DISTRICT_CODE,0,255;
                CO \"COUNTY_CODE\" true true false 255 Text 0 0,First,#,input_table22_join_copy,CO,0,255,input_table21_join_copy,CO,0,255;
                RT \"ROUTE_NAME\" true true false 255 Text 0 0,First,#,input_table22_join_copy,RT,0,255,input_table21_join_copy,RT,0,255;
                ROUTE_SUFFIX_CODE \"ROUTE_SUFFIX_CODE\" true true false 255 Text 0 0,First,#,input_table22_join_copy,ROUTE_SUFFIX_CODE,0,255,input_table21_join_copy,ROUTE_SUFFIX_CODE,0,255;
                ROUTE_NUM \"ROUTE\" true true false 2 Short 0 0,First,#,input_table22_join_copy,ROUTE_NUM,-1,-1,input_table21_join_copy,ROUTE_NUM,-1,-1;
                ROUTE_C \"ROUTE_C\" true true false 255 Text 0 0,First,#,input_table22_join_copy,ROUTE_C,0,255,input_table21_join_copy,ROUTE_C,0,255;
                HIghwayID \"Highway ID\" true true false 255 Text 0 0,First,#,input_table22_join_copy,HIghwayID,0,255,input_table21_join_copy,HIghwayID,0,255;
                FREQUENCY \"FREQUENCY\" true true false 4 Long 0 0,First,#,input_table22_join_copy,FREQUENCY,-1,-1,input_table21_join_copy,FREQUENCY,-1,-1;
                SUM_Production_Quantity \"SUM_Production_Quantity\" true true false 8 Double 0 0,First,#,input_table22_join_copy,SUM_Production_Quantity,-1,-1,input_table21_join_copy,SUM_Production_Quantity,-1,-1;
                OBJECTID_1 \"OBJECTID_1\" true true false 4 Long 0 0,First,#,input_table22_join_copy,OBJECTID_1,-1,-1,input_table21_join_copy,OBJECTID_1,-1,-1;
                GISID \"GISID\" true true false 4 Long 0 0,First,#,input_table22_join_copy,GISID,-1,-1,input_table21_join_copy,GISID,-1,-1;R
                esp__District \"Resp__District\" true true false 4 Long 0 0,First,#,input_table22_join_copy,Resp__District,-1,-1;
                Resp__Region \"Resp__Region\" true true false 4 Long 0 0,First,#,input_table22_join_copy,Resp__Region,-1,-1;
                Resp__Area \"Resp__Area\" true true false 4 Long 0 0,First,#,input_table22_join_copy,Resp__Area,-1,-1;
                Resp_ \"Resp_\" true true false 4 Long 0 0,First,#,input_table22_join_copy,Resp_,-1,-1,input_table21_join_copy,Resp_,-1,-1;
                Work_Order_Number \"Work_Order_Number\" true true false 4 Long 0 0,First,#,input_table22_join_copy,Work_Order_Number,-1,-1,input_table21_join_copy,Work_Order_Number,-1,-1;
                County \"County\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,County,0,8000,input_table21_join_copy,County,0,8000;
                TwoCounties \"TwoCounties\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,TwoCounties,0,8000,input_table21_join_copy,TwoCounties,0,255;
                Route \"Route\" true true false 4 Text 0 0,First,#,input_table22_join_copy,Route,0,4,input_table21_join_copy,Route,0,4;
                From_PM \"From_PM\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,From_PM,0,8000,input_table21_join_copy,From_PM,0,8000;
                To_PM \"To_PM\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,To_PM,0,8000,input_table21_join_copy,To_PM,0,8000;
                Point_or_Line \"Point_or_Line\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,Point_or_Line,0,8000,input_table21_join_copy,Point_or_Line,0,255;
                Production_Quantity \"Production_Quantity\" true true false 8 Double 0 0,First,#,input_table22_join_copy,Production_Quantity,-1,-1,input_table21_join_copy,Production_Quantity,-1,-1;
                UOM \"UOM\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,UOM,0,8000,input_table21_join_copy,UOM,0,8000;
                Maintenance_Type \"Maintenance_Type\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,Maintenance_Type,0,8000,input_table21_join_copy,Maintenance_Type,0,8000;
                IMMS_Project_Code \"IMMS_Project_Code\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,IMMS_Project_Code,0,8000,input_table21_join_copy,IMMS_Project_Code,0,8000;
                EFIS_Reporting_Code \"EFIS_Reporting_Code\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,EFIS_Reporting_Code,0,8000,input_table21_join_copy,EFIS_Reporting_Code,0,8000;
                EFIS_Project_Code \"EFIS_Project_Code\" true true false 4 Long 0 0,First,#,input_table22_join_copy,EFIS_Project_Code,-1,-1,input_table21_join_copy,EFIS_Project_Code,-1,-1;
                Comments \"Comments\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,Comments,0,8000,input_table21_join_copy,Comments,0,8000;
                Work_Order_Priority \"Work_Order_Priority\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,Work_Order_Priority,0,8000,input_table21_join_copy,Work_Order_Priority,0,8000;
                Activity \"Activity\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,Activity,0,8000,input_table21_join_copy,Activity,0,8000;
                Activity_Description \"Activity_Description\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,Activity_Description,0,8000,input_table21_join_copy,Activity_Description,0,8000;
                IMMS_Unit_ID \"IMMS_Unit_ID\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,IMMS_Unit_ID,0,8000,input_table21_join_copy,IMMS_Unit_ID,0,8000;
                EFIS_Sobj \"EFIS_Sobj\" true true false 4 Long 0 0,First,#,input_table22_join_copy,EFIS_Sobj,-1,-1,input_table21_join_copy,EFIS_Sobj,-1,-1;
                Prob \"Prob\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,Prob,0,8000,input_table21_join_copy,Prob,0,8000;
                Fiscal_Year \"Fiscal_Year\" true true false 4 Long 0 0,First,#,input_table22_join_copy,Fiscal_Year,-1,-1,input_table21_join_copy,Fiscal_Year,-1,-1;
                Labor_Hours \"Labor_Hours\" true true false 8 Double 0 0,First,#,input_table22_join_copy,Labor_Hours,-1,-1,input_table21_join_copy,Labor_Hours,-1,-1;
                P_Y_s \"P_Y_s\" true true false 8 Double 0 0,First,#,input_table22_join_copy,P_Y_s,-1,-1;
                Labor_Cost \"Labor_Cost\" true true false 8 Double 0 0,First,#,input_table22_join_copy,Labor_Cost,-1,-1,input_table21_join_copy,Labor_Cost,-1,-1;
                Vehicle_Cost \"Vehicle_Cost\" true true false 8 Double 0 0,First,#,input_table22_join_copy,Vehicle_Cost,-1,-1,input_table21_join_copy,Vehicle_Cost,-1,-1;
                Material_Cost \"Material_Cost\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,Material_Cost,0,8000,input_table21_join_copy,Material_Cost,-1,-1;
                Other_Cost \"Other_Cost\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,Other_Cost,0,8000,input_table21_join_copy,Other_Cost,-1,-1;
                Total_Cost \"Total_Cost\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,Total_Cost,0,8000,input_table21_join_copy,Total_Cost,-1,-1;
                From_Miles \"From_Miles\" true true false 8 Double 0 0,First,#,input_table22_join_copy,From_Miles,-1,-1,input_table21_join_copy,From_Miles,-1,-1;
                To_Miles \"To_Miles\" true true false 8 Double 0 0,First,#,input_table22_join_copy,To_Miles,-1,-1,input_table21_join_copy,To_Miles,-1,-1;
                Secondary_Prod \"Secondary_Prod\" true true false 8 Double 0 0,First,#,input_table22_join_copy,Secondary_Prod,-1,-1,input_table21_join_copy,Secondary_Prod,-1,-1;
                Secondary_UOM \"Secondary_UOM\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,Secondary_UOM,0,8000,input_table21_join_copy,Secondary_UOM,0,8000;
                Route_Numeric \"Route_Numeric\" true true false 4 Long 0 0,First,#,input_table22_join_copy,Route_Numeric,-1,-1,input_table21_join_copy,Route_Numeric,-1,-1;
                Work_Order_Text \"Work_Order_Text\" true true false 255 Text 0 0,First,#,input_table22_join_copy,Work_Order_Text,0,255,input_table21_join_copy,Work_Order_Text,0,255;
                District_Text \"District_Text\" true true false 255 Text 0 0,First,#,input_table22_join_copy,District_Text,0,255,input_table21_join_copy,District_Text,0,255;
                GISID_Text \"GISID_Text\" true true false 255 Text 0 0,First,#,input_table22_join_copy,GISID_Text,0,255,input_table21_join_copy,GISID_Text,0,255;
                Highway_ID \"Highway_ID\" true true false 255 Text 0 0,First,#,input_table22_join_copy,Highway_ID,0,255;
                Route_Suffix \"Route_Suffix\" true true false 255 Text 0 0,First,#,input_table22_join_copy,Route_Suffix,0,255,input_table21_join_copy,Route_Suffix,0,255;
                TRMTID_USER \"TREATMENT ID USER\" true true false 255 Text 0 0,First,#,input_table22_join_copy,TRMTID_USER,0,255,input_table21_join_copy,TRMTID_USER,0,255;
                OBJECTID_12 \"OBJECTID\" true true false 4 Long 0 0,First,#,input_table22_join_copy,OBJECTID_12,-1,-1,input_table21_join_copy,OBJECTID_12,-1,-1;
                Work_Order \"Work Order\" true true false 4 Long 0 0,First,#,input_table22_join_copy,Work_Order,-1,-1,input_table21_join_copy,Work_Order,-1,-1;
                Resp1 \"Resp1\" true true false 4 Long 0 0,First,#,input_table22_join_copy,Resp1,-1,-1;
                Activity_1 \"Activity\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,Activity_1,0,8000,input_table21_join_copy,Activity_1,0,8000;
                Activity_Description_1 \"Activity Description\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,Activity_Description_1,0,8000,input_table21_join_copy,Activity_Description_1,0,8000;
                Field5 \"Field5\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,Field5,0,8000,input_table21_join_copy,Field5,0,8000;
                IMMS_Unit_ID_1 \"IMMS Unit ID\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,IMMS_Unit_ID_1,0,8000,input_table21_join_copy,IMMS_Unit_ID_1,0,8000;
                From_PM_1 \"From PM\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,From_PM_1,0,8000,input_table21_join_copy,From_PM_1,0,8000;
                To_PM_1 \"To PM\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,To_PM_1,0,8000,input_table21_join_copy,To_PM_1,0,8000;
                Comments_1 \"Comments\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,Comments_1,0,8000,input_table21_join_copy,Comments_1,0,8000;
                Field10 \"Field10\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,Field10,0,8000,input_table21_join_copy,Field10,0,8000;
                Field11 \"Field11\" true true false 8000 Text 0 0,First,#,input_table22_join_copy,Field11,0,8000,input_table21_join_copy,Field11,0,8000;
                Charge_Date \"Charge Date\" true true false 8 Date 0 0,First,#,input_table22_join_copy,Charge_Date,-1,-1,input_table21_join_copy,Charge_Date,-1,-1;
                TRMTID_USER_1 \"TREATMENT ID USER\" true true false 255 Text 0 0,First,#,input_table22_join_copy,TRMTID_USER_1,0,255,input_table21_join_copy,TRMTID_USER_1,0,255;
                Calendar_Year \"Calendar Year\" true true false 4 Long 0 0,First,#,input_table22_join_copy,Calendar_Year,-1,-1,input_table21_join_copy,Calendar_Year,-1,-1;
                Work_Order_Text_1 \"Work Order Text\" true true false 255 Text 0 0,First,#,input_table22_join_copy,Work_Order_Text_1,0,255
                """
        )

        Count3 = arcpy.management.GetCount(append_1)
        print("       CalTransLns_append has {} records".format(Count3[0]))

        print("Part 2: Performing Standardization")
        print("     step 6/8 repair geometry")
        repair_geom_1 = arcpy.management.RepairGeometry(
            in_features=append_1,
            delete_null="KEEP_NULL",
            validation_method="ESRI",
        )

        print("     step 7/8 alter & add fields")
        alterfield_1 = arcpy.management.AlterField(
            in_table=repair_geom_1,
            field="County",
            new_field_name="County2",
            new_field_alias="County2",
            field_type="TEXT",
            clear_field_alias="DO_NOT_CLEAR",
        )

        alterfield_2 = arcpy.management.AlterField(
            in_table=alterfield_1,
            field="Activity_Description",
            new_field_name="Activity_Description_",
            new_field_alias="Activity_Description_",
            field_type="TEXT",
            clear_field_alias="DO_NOT_CLEAR",
        )

        alterfield_3 = arcpy.management.AlterField(
            in_table=alterfield_2,
            field="TRMTID_USER",
            new_field_name="TRMTID_USER_2",
            new_field_alias="TRMTID_USER_2",
            field_type="TEXT",
            clear_field_alias="DO_NOT_CLEAR",
        )

        addfields_1 = AddFields(Input_Table=alterfield_3)

        print("     step 8/8 transfer attributes")
        calc_field_1 = arcpy.management.CalculateField(
            in_table=addfields_1,
            field="PROJECTID_USER",
            expression="!HighwayID!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_2 = arcpy.management.CalculateField(
            in_table=calc_field_1,
            field="AGENCY",
            expression='"CALSTA"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_3 = arcpy.management.CalculateField(
            in_table=calc_field_2,
            field="ORG_ADMIN_p",
            expression='"CALTRANS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )
        
        calc_field_4 = arcpy.management.CalculateField(
            in_table=calc_field_3,
            field="ORG_ADMIN_t",
            expression='"CALTRANS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )
        
        calc_field_5 = arcpy.management.CalculateField(
            in_table=calc_field_4,
            field="ORG_ADMIN_a",
            expression='"CALTRANS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_6 = arcpy.management.CalculateField(
            in_table=calc_field_5,
            field="PROJECT_CONTACT",
            expression='"Division of Maintenance"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_7 = arcpy.management.CalculateField(
            in_table=calc_field_6,
            field="PROJECT_EMAIL",
            expression='"andrew.lozano@dot.ca.gov"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_8 = arcpy.management.CalculateField(
            in_table=calc_field_7,
            field="ADMINISTERING_ORG",
            expression='"CALTRANS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_9 = arcpy.management.CalculateField(
            in_table=calc_field_8,
            field="ADMIN_ORG_NAME",
            expression='"CALTRANS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_10 = arcpy.management.CalculateField(
            in_table=calc_field_9,
            field="PRIMARY_FUNDING_SOURCE",
            expression='"GENERAL_FUND"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_11 = arcpy.management.CalculateField(
            in_table=calc_field_10,
            field="PRIMARY_FUND_SRC_NAME",
            expression='"GENERAL_FUND"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_12 = arcpy.management.CalculateField(
            in_table=calc_field_11,
            field="PRIMARY_FUNDING_ORG",
            expression='"CALTRANS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_13 = arcpy.management.CalculateField(
            in_table=calc_field_12,
            field="PRIMARY_FUND_ORG_NAME",
            expression='"CALTRANS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )
        
        calc_field_14 = arcpy.management.CalculateField(
            in_table=calc_field_13,
            field="TRMTID_USER",
            expression="str(!HIghwayID!)+'-'+str(!From_PM!)+'-'+str(!To_PM!)",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS"
        )

        calc_field_15 = arcpy.management.CalculateField(
            in_table=calc_field_14,
            field="TREATMENT_AREA",
            expression="ifelse(!UOM!, !Production_Quantity!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(UOM, Q):
                            if UOM == "ACRE" or UOM == 'AC':
                                return Q
                            else:
                                return None""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # NOTE: A unique Activity ID for each record is required for the line enrichment tool to work properly
        calc_field_16 = arcpy.management.CalculateField(
            in_table=calc_field_15,
            field="ACTIVID_USER",
            expression="'CALTRANS-'+str(!Work_Order!)+'-'+str(!OBJECTID!)",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_17 = arcpy.management.CalculateField(
            in_table=calc_field_16,
            field="IMPLEMENTING_ORG",
            expression="!DISTRICT_CODE!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_18 = arcpy.management.CalculateField(
            in_table=calc_field_17,
            field="IMPLEM_ORG_NAME",
            expression="!DISTRICT_CODE!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_19 = arcpy.management.CalculateField(
            in_table=calc_field_18,
            field="ACTIVITY_UOM",
            expression="ifelse(!UOM!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(Unit):
                            if Unit == 'ACRE':
                                return 'AC'
                            else:
                                return Unit""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_20 = arcpy.management.CalculateField(
            in_table=calc_field_19,
            field="ACTIVITY_QUANTITY",
            expression="!Production_Quantity!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_21 = arcpy.management.CalculateField(
            in_table=calc_field_20,
            field="ACTIVITY_STATUS",
            expression='"COMPLETE"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_22 = arcpy.management.CalculateField(
            in_table=calc_field_21,
            field="ACTIVITY_START",
            expression="None",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_23 = arcpy.management.CalculateField(
            in_table=calc_field_22,
            field="ACTIVITY_END",
            expression="!Charge_Date!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_24 = arcpy.management.CalculateField(
            in_table=calc_field_23,
            field="Source",
            expression='"CALTRANS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_25 = arcpy.management.CalculateField(
            in_table=calc_field_24,
            field="Crosswalk",
            expression="!Activity_Description_!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_26 = arcpy.management.CalculateField(
            in_table=calc_field_25,
            field="TRMT_GEOM",
            expression="'LINE'",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        print("Saving Standardized Output")
        standardized_1 = arcpy.management.CopyFeatures(
            in_features=calc_field_26,
            out_feature_class=output_lines_standardized,
        )

        keepfields_1 = KeepFields(standardized_1)

        print("Enriching Dataset")
        lines_enriched_1 = enrich_lines(
            line_fc=keepfields_1
        ) 

        print(f"Saving Enriched Output")
        lines_enriched_2 = arcpy.management.CopyFeatures(
            in_features=lines_enriched_1,
            out_feature_class=output_lines_enriched,
        )

        Count4 = arcpy.management.GetCount(output_lines_enriched)
        print("   output_enriched has {} records".format(Count4[0]))

        calc_field_27 = arcpy.management.CalculateField(
            in_table=lines_enriched_2,
            field="PRIMARY_OWNERSHIP_GROUP",
            expression='"STATE"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_28 = arcpy.management.CalculateField(
            in_table=calc_field_27,
            field="TREATMENT_ID_USER",
            expression="!PROJECTID_USER!+'-'+str(!COUNTY!)[:8]+'-'+str(!REGION!)[:3]+'-'+str(!IN_WUI!)[:3]",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        AssignDomains(
            in_table=calc_field_28
        )

        if delete_scratch:
            print('Deleting Scratch Files')
            delete_scratch_files(
                gdb=scratch_workspace,
                delete_fc="yes",
                delete_table="yes",
                delete_ds="yes",
            )

        end1 = datetime.datetime.now()
        elapsed1 = (end1-start1)
        hours, remainder1 = divmod(elapsed1.total_seconds(), 3600)
        minutes, remainder2 = divmod(remainder1, 60)
        seconds, remainder3 = divmod(remainder2, 1)
        print(f"CalTrans script took: {int(hours)}h, {int(minutes)}m, {seconds}s to complete")


