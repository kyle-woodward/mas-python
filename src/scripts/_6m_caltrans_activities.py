import arcpy
from ._1b_add_fields import AddFields
from ._2b_assign_domains import AssignDomains
# from ._7b_enrichments_pts import enrich_points
from ._7c_enrichments_lines import enrich_lines
from ._2k_keep_fields import KeepFields
import os
from sys import argv
from .utils import init_gdb, delete_scratch_files #, runner
import time

original_gdb, workspace, scratch_workspace = init_gdb()
# TODO add print steps

# 6m CalTrans_Activities 20221123
def CalTrans(
    input_lines21,
    input_lines22,
    input_table21,
    input_table22,
    output_lines_standardized,
    output_lines_enriched,
):

    start = time.time()
    print(f"Start Time {time.ctime()}")
    arcpy.env.overwriteOutput = True
    arcpy.env.qualifiedFieldNames = False

    arcpy.ImportToolbox(
        r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx"
    )

    # define intermediary objects in scratch
    CalTrans21_scratch = os.path.join(scratch_workspace, "CalTrans21_scratch")
    CalTrans22_scratch = os.path.join(scratch_workspace, "CalTrans22_scratch")

    
    # #TODO Verify joined input Treatments and Activities

    ### BEGIN POLYLINE WORKFLOW
    # Process: Add Join (2) (Add Join) (management)
    print("     step 3/33 add join")
    input_table21_join = arcpy.management.AddJoin(
        in_layer_or_view=input_lines21,
        in_field="HIghwayID",
        join_table=input_table21,
        join_field="HighwayID",
        join_type="KEEP_COMMON",
        index_join_fields="INDEX_JOIN_FIELDS",
    )

    # Process: Copy Features (Copy Features) (management)
    input_table21_join_copy = arcpy.management.CopyFeatures(
        input_table21_join, CalTrans21_scratch
    )

    input_table22_join = arcpy.management.AddJoin(
        in_layer_or_view=input_lines22,
        in_field="HIghwayID",
        join_table=input_table22,
        join_field="Highway_ID",
        join_type="KEEP_COMMON",
        index_join_fields="INDEX_JOIN_FIELDS",
    )

    # Process: Copy Features (2) (Copy Features) (management)
    input_table22_join_copy = arcpy.management.CopyFeatures(
        input_table22_join, CalTrans22_scratch
    )

    print("Appending Lines")
    # Process: Create Feature Class (Create Feature Class) (management)
    CalTransLns_scratch = arcpy.management.CreateFeatureclass(out_path=scratch_workspace, out_name="CalTransLns_scratch", geometry_type="POLYLINE", template=CalTrans22_scratch)

    # Process: Append (Append) (management)
    # CalTransLns_append = arcpy.management.Append(
    #     inputs=[input_table21_join_copy, input_table22_join_copy], 
    #     target=CalTransLns_scratch, 
    #     schema_type="TEST", 
    #     field_mapping=""
    # )

    CalTransLns_append = arcpy.management.Append(
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

    print("Performing Line Standardization")
    # Process: Copy Features (2) (Copy Features) (management)
    # CalTransLns_append_2 = os.path.join(scratch_workspace, "CalTransLns_Copy")
    # arcpy.management.CopyFeatures(
    #     in_features=CalTransLns_append,
    #     out_feature_class=CalTransLns_append_2,
    #     config_keyword="",
    #     spatial_grid_1=None,
    #     spatial_grid_2=None,
    #     spatial_grid_3=None,
    # )

    # Process: Repair Geometry (Repair Geometry) (management)
    caltrans_poly_copy_repaired_geom = arcpy.management.RepairGeometry(
        in_features=CalTransLns_append,
        delete_null="KEEP_NULL",
        validation_method="ESRI",
    )

    # Process: Alter Field County (2) (Alter Field) (management)
    caltrans_poly_alterfield_v1 = arcpy.management.AlterField(
        in_table=caltrans_poly_copy_repaired_geom,
        field="County",
        new_field_name="County2",
        new_field_alias="County2",
        field_type="TEXT",
        # field_length=25,
        # field_is_nullable="NULLABLE",
        clear_field_alias="DO_NOT_CLEAR",
    )

    # Process: Alter Field Activity Description (2) (Alter Field) (management)
    caltrans_poly_alterfield_v2 = arcpy.management.AlterField(
        in_table=caltrans_poly_alterfield_v1,
        field="Activity_Description",
        new_field_name="Activity_Description_",
        new_field_alias="Activity_Description_",
        field_type="TEXT",
        # field_length=70,
        # field_is_nullable="NULLABLE",
        clear_field_alias="DO_NOT_CLEAR",
    )

    # # Process: Alter Field Veg (2) (Alter Field) (management)
    # caltrans_poly_alterfield_v3 = arcpy.management.AlterField(
    #     in_table=caltrans_poly_alterfield_v2,
    #     field="Broad_Vegetation_Type",
    #     new_field_name="BVT",
    #     new_field_alias="BVT",
    #     field_type="TEXT",
    #     # field_length=50,
    #     # field_is_nullable="NULLABLE",
    #     clear_field_alias="DO_NOT_CLEAR",
    # )

    # # Process: Alter Field Activity Status (2) (Alter Field) (management)
    # caltrans_poly_alterfield_v4 = arcpy.management.AlterField(
    #     in_table=caltrans_poly_alterfield_v2,
    #     field="Activity_Status",
    #     new_field_name="Act_Status",
    #     new_field_alias="Act_Status",
    #     field_type="TEXT",
    #     # field_length=25,
    #     # field_is_nullable="NULLABLE",
    #     clear_field_alias="DO_NOT_CLEAR",
    # )

    # # Process: Alter Activity Quantity (2) (Alter Field) (management)
    # caltrans_poly_alterfield_v5 = arcpy.management.AlterField(
    #     in_table=caltrans_poly_alterfield_v4,
    #     field="Activity_Quantity",
    #     new_field_name="Production_Quantity",
    #     new_field_alias="Production_Quantity",
    #     field_type="DOUBLE",
    #     # field_length=8,
    #     # field_is_nullable="NULLABLE",
    #     clear_field_alias="DO_NOT_CLEAR",
    # )

    # # Process: Alter Field Residue Fate (2) (Alter Field) (management)
    # caltrans_poly_alterfield_v6 = arcpy.management.AlterField(
    #     in_table=caltrans_poly_alterfield_v5,
    #     field="Residue_Fate",
    #     new_field_name="Fate",
    #     new_field_alias="Fate",
    #     field_type="TEXT",
    #     # field_length=35,
    #     # field_is_nullable="NULLABLE",
    #     clear_field_alias="DO_NOT_CLEAR",
    # )

    # # Process: Alter Field Fate Units (2) (Alter Field) (management)
    # caltrans_poly_alterfield_v7 = arcpy.management.AlterField(
    #     in_table=caltrans_poly_alterfield_v6,
    #     field="Residue_Fate_Units",
    #     new_field_name="FateUnits",
    #     new_field_alias="FateUnits",
    #     field_type="TEXT",
    #     # field_length=5,
    #     # field_is_nullable="NULLABLE",
    #     clear_field_alias="DO_NOT_CLEAR",
    # )

    # # Process: Alter Residue Quantity (2) (Alter Field) (management)
    # caltrans_poly_alterfield_v8 = arcpy.management.AlterField(
    #     in_table=caltrans_poly_alterfield_v7,
    #     field="Residue_Fate_Quantity",
    #     new_field_name="FateQuantity",
    #     new_field_alias="FateQuantity",
    #     field_type="DOUBLE",
    #     # field_length=8,
    #     # field_is_nullable="NULLABLE",
    #     clear_field_alias="DO_NOT_CLEAR",
    # )

    # Process: Treatment User ID (Alter Field) (management)
    caltrans_poly_alterfield_v9 = arcpy.management.AlterField(
        in_table=caltrans_poly_copy_repaired_geom,
        field="TRMTID_USER",
        new_field_name="TRMTID_USER_2",
        new_field_alias="TRMTID_USER_2",
        field_type="TEXT",
        # field_length=30,
        # field_is_nullable="NULLABLE",
        clear_field_alias="DO_NOT_CLEAR",
    )

    # Process: 1b Add Fields (2) (1b Add Fields) (PC414CWIMillionAcres)
    caltrans_poly_addfields = AddFields(Input_Table=caltrans_poly_alterfield_v9)

    # Process: Calculate Project ID (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v1 = arcpy.management.CalculateField(
        in_table=caltrans_poly_addfields,
        field="PROJECTID_USER",
        expression="!HighwayID!",
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Agency (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v2 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v1,
        field="AGENCY",
        expression='"CALSTA"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Data Steward (Calculate Field) (management)
    caltrans_poly_calc_field_v3 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v2,
        field="ORG_ADMIN_p",
        expression='"CALTRANS"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )
    
    # Process: Calculate Data Steward (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v3a = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v3,
        field="ORG_ADMIN_t",
        expression='"CALTRANS"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )
    
    # Process: Calculate Data Steward (3) (Calculate Field) (management)
    caltrans_poly_calc_field_v3b = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v3a,
        field="ORG_ADMIN_a",
        expression='"CALTRANS"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Project Contact (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v4 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v3b,
        field="PROJECT_CONTACT",
        expression='"Division of Maintenance"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Email (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v5 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v4,
        field="PROJECT_EMAIL",
        expression='"andrew.lozano@dot.ca.gov"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Admin Org (Calculate Field) (management)
    caltrans_poly_calc_field_v6 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v5,
        field="ADMINISTERING_ORG",
        expression='"CALTRANS"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Admin Org (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v6a = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v6,
        field="ADMIN_ORG_NAME",
        expression='"CALTRANS"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Primary Funding Source (Calculate Field) (management)
    caltrans_poly_calc_field_v7 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v6a,
        field="PRIMARY_FUNDING_SOURCE",
        expression='"GENERAL_FUND"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Primary Funding Source (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v7a = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v7,
        field="PRIMARY_FUND_SRC_NAME",
        expression='"GENERAL_FUND"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Primary Funding Org (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v8 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v7a,
        field="PRIMARY_FUNDING_ORG",
        expression='"CALTRANS"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Primary Funding Org (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v8a = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v8,
        field="PRIMARY_FUND_ORG_NAME",
        expression='"CALTRANS"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )
    
    # Process: Calculate Treatment ID (2) (Calculate Field) (management)
    Updated_Input_Table_46_ = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v8a,
        field="TRMTID_USER",
        expression="str(!HIghwayID!)+'-'+str(!From_PM!)+'-'+str(!To_PM!)",
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS"
    )

    # # Process: Calculate WUI (2) (Calculate Field) (management)
    # caltrans_poly_calc_field_v9 = arcpy.management.CalculateField(
    #     in_table=Updated_Input_Table_46_,
    #     field="IN_WUI",
    #     expression="ifelse(!WUI!)",
    #     expression_type="PYTHON3",
    #     code_block="""def ifelse(WUI):
    #                     if WUI == "Yes":
    #                         return "WUI_USER_DEFINED"
    #                     elif WUI == "No":
    #                         return "NON-WUI_USER_DEFINED"
    #                     else:
    #                         return WUI""",
    #     field_type="TEXT",
    #     enforce_domains="NO_ENFORCE_DOMAINS",
    # )

    # Process: Calculate Treatment Area (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v10 = arcpy.management.CalculateField(
        in_table=Updated_Input_Table_46_,
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

    # Process: Calculate Activity ID (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v11 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v10,
        field="ACTIVID_USER",
        expression="!Work_Order_Number!",
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Implementing Org (Calculate Field) (management)
    caltrans_poly_calc_field_v12 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v11,
        field="IMPLEMENTING_ORG",
        expression="!DISTRICT_CODE!",
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Implementing Org (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v12a = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v12,
        field="IMPLEM_ORG_NAME",
        expression="!DISTRICT_CODE!",
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Activity UOM (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v13 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v12a,
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

    # Process: Calculate Activity Quantity (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v14 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v13,
        field="ACTIVITY_QUANTITY",
        expression="!Production_Quantity!",
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Status (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v15 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v14,
        field="ACTIVITY_STATUS",
        expression='"COMPLETE"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Activity Start (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v16 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v15,
        field="ACTIVITY_START",
        expression="None",
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Activity End (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v17 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v16,
        field="ACTIVITY_END",
        expression="!Charge_Date!",
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Source (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v18 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v17,
        field="Source",
        expression='"CALTRANS"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Crosswalk (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v19 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v18,
        field="Crosswalk",
        expression="!Activity_Description_!",
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Geometry Attributes (2) (Calculate Geometry Attributes) (management)
    # CalTrans_pts_Copy_15_ = arcpy.management.CalculateGeometryAttributes(in_features=caltrans_poly_calc_field_v19,
    #                                                                      geometry_property=[["LATITUDE", "INSIDE_Y"], ["LONGITUDE", "INSIDE_X"]],
    #                                                                      length_unit="",
    #                                                                      area_unit="",
    #                                                                      coordinate_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]",
    #                                                                      coordinate_format="DD")

    # Process: Keep Fields (Delete Field) (management)
    caltrans_poly_keepfields = KeepFields(caltrans_poly_calc_field_v19)

    print(f"Saving Output Lines Standardized: {output_lines_standardized}")
    # Process: Copy Features (3) (Copy Features) (management)
    arcpy.management.CopyFeatures(
        in_features=caltrans_poly_keepfields,
        out_feature_class=output_lines_standardized,
        config_keyword="",
        spatial_grid_1=None,
        spatial_grid_2=None,
        spatial_grid_3=None,
    )

    # Process: 2b Assign Domains (3) (2b Assign Domains) (PC414CWIMillionAcres)
    caltrans_line_standardized_assigndomains = AssignDomains(
        in_table=output_lines_standardized
    )

    print("Performing Lines Enrichments")
    # Process: 7c Enrichments Lines (2) (7c Enrichments Lines) (PC414CWIMillionAcres)
    caltrans_lines_enriched = enrich_lines(
        line_fc=caltrans_line_standardized_assigndomains
    )  # don't delete scratch

    print(f"Saving Output Lines Enriched: {output_lines_enriched}")
    # Process: Copy Features (4) (Copy Features) (management)
    arcpy.management.CopyFeatures(
        in_features=caltrans_lines_enriched,
        out_feature_class=output_lines_enriched,
        config_keyword="",
        spatial_grid_1=None,
        spatial_grid_2=None,
        spatial_grid_3=None,
    )

    # Process: Calculate Owner State (2) (Calculate Field) (management)
    caltrans_lines_enriched_calc_field_v1 = arcpy.management.CalculateField(
        in_table=output_lines_enriched,
        field="PRIMARY_OWNERSHIP_GROUP",
        expression='"STATE"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    ## *** IMMS_Unit_ID and IMMS_ID no longer exist after running a 7 tool on the data, so changed to 'TREATMENT_ID_USER' since that was filled with IMMS
    ## *** prior to the 7 tool being ran. Get non-specific error (no line traceback) that nontypes and string types cannot be concatenated when
    ## *** running the script with this block of code intact. The output table "caltrans_lines_enriched_calc_field_v2" should be fed into AssignDomains below once functioning.
    # Process: Calculate Treatment ID (2) (Calculate Field) (management)
    # caltrans_lines_enriched_calc_field_v2 = arcpy.management.CalculateField(
    #     in_table=caltrans_lines_enriched_calc_field_v1,
    #     field="TREATMENT_ID_USER",
    #     expression="!PROJECTID_USER!+'-'+!COUNTY![:8]+'-'+!REGION![:3]+'-'+!IN_WUI![:3]",
    #     expression_type="PYTHON3",
    #     code_block="",
    #     field_type="TEXT",
    #     enforce_domains="NO_ENFORCE_DOMAINS",
    # )

    # Process: 2b Assign Domains (4) (2b Assign Domains) (PC414CWIMillionAcres)
    caltrans_lines_enriched_assigndomains = AssignDomains(
        in_table=caltrans_lines_enriched_calc_field_v1
    )

    # print("Deleting Scratch Files")
    # delete_scratch_files(
    #     gdb=scratch_workspace, delete_fc="yes", delete_table="yes", delete_ds="yes"
    # )

    end = time.time()
    print(f"Time Elapsed: {(end-start)/60} minutes")


if __name__ == "__main__":
    runner(workspace, scratch_workspace, CalTrans, "*argv[1:]")
# # Global Environment settings
#  with arcpy.EnvManager(
# extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""",  outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""",
# preserveGlobalIds=True,
# qualifiedFieldNames=False,
# scratchWorkspace=scratch_workspace,
# transferDomains=True,
# transferGDBAttributeProperties=True,
# workspace=workspace):
#     CalTrans(*argv[1:])
