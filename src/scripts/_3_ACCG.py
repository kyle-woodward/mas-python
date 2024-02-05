"""
# Description: Converts the Amador-Calaveras Conservation Group fuels treatments dataset 
#              into the Task Force standardized schema.  Dataset
#              is enriched with vegetation, ownership, county, WUI, 
#              Task Force Region, and year.            
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import arcpy
import os
from .utils import init_gdb, delete_scratch_files, runner
from ._2k_keep_fields import KeepFields
# add 2j standardize domains
import time

workspace, scratch_workspace = init_gdb()
# TODO add print steps, rename variables

def ACCG(input_fc, output_standardized):
    start = time.time()
    print(f"Start Time {time.ctime()}")
    
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
        # _scratchgdb_ = f"{arcpy.env.scratchGDB}" replaced with "scratch_workspace"
        Fuels_Treatments_Piles_Crosswalk = os.path.join(
            workspace, "Fuels_Treatments_Piles_Crosswalk"
        )
        # PC414_CWI_Million_Acres_gdb = "C:\\Users\\sageg\\SIG Dropbox\\Carl Rudeen\\PC414 Million Acre\\PC414 CWI Million Acres.gdb" replaced with "workspace"
        California = os.path.join(workspace, "b_Reference", "California")

        # Process: Table To Table (Table To Table) (conversion)
        ACCG_Project_table = arcpy.conversion.TableToTable(
            in_rows=input_fc,
            out_path=scratch_workspace,
            out_name="ACCG_Project_table",
            where_clause="SHAPE_Length = 0 Or SHAPE_Area = 0",
            field_mapping="",
            config_keyword="",
        )

        # Process: Table Select (Table Select) (analysis)
        ACCG_Project_table2 = os.path.join(scratch_workspace, "ACCG_Project_table2")

        #### ExecuteError: ERROR 160144: An expected Field was not found or could not be retrieved properly.Failed to execute (TableSelect).
        arcpy.analysis.TableSelect(
            in_table=ACCG_Project_table,
            out_table=ACCG_Project_table2,
            where_clause="PROCLAIMED_FOREST_CODE = '0417' Or PROCLAIMED_FOREST_CODE = '0501' Or PROCLAIMED_FOREST_CODE = '0502' Or PROCLAIMED_FOREST_CODE = '0503' Or PROCLAIMED_FOREST_CODE = '0504' Or PROCLAIMED_FOREST_CODE = '0505' Or PROCLAIMED_FOREST_CODE = '0506' Or PROCLAIMED_FOREST_CODE = '0507' Or PROCLAIMED_FOREST_CODE = '0508' Or PROCLAIMED_FOREST_CODE = '0509' Or PROCLAIMED_FOREST_CODE = '0510' Or PROCLAIMED_FOREST_CODE = '0511' Or PROCLAIMED_FOREST_CODE = '0512' Or PROCLAIMED_FOREST_CODE = '0513' Or PROCLAIMED_FOREST_CODE = '0514' Or PROCLAIMED_FOREST_CODE = '0515' Or PROCLAIMED_FOREST_CODE = '0516' Or PROCLAIMED_FOREST_CODE = '0517' Or PROCLAIMED_FOREST_CODE = '0519' Or PROCLAIMED_FOREST_CODE = '0602' Or PROCLAIMED_FOREST_CODE = '0610'",
        )

        # Process: Add Projects Fields (multiple) (2) (Add Fields (multiple)) (management)
        accg_project_table_add_fields = arcpy.management.AddFields(
            in_table=ACCG_Project_table2,
            field_description=[
                ["Prj_ID", "TEXT", "Project ID", "50", "", ""],
                ["Prj_Name", "TEXT", "Project Name", "150", "", ""],
                ["Prj_FundNM", "TEXT", "Primary Funding Source Name", "130", "", ""],
                ["Prj_FndOrg", "TEXT", "Primary Funding Org Name", "130", "", ""],
                ["Prj_Admin", "TEXT", "Primary Administering Org Name", "130", "", ""],
                ["Prj_Implem", "TEXT", "Primary Implementing Org Name", "130", "", ""],
                ["Prj_RptOrg", "TEXT", "Reporting Org Name", "130", "", ""],
                ["Prj_Contct", "TEXT", "Project Contact", "100", "", ""],
                ["Prj_Email", "TEXT", "Project Email", "100", "", ""],
                ["Prj_Start", "DATE", "Project Start Date", "", "", ""],
                ["Prj_End", "DATE", "Project End Date", "", "", ""],
                ["Prj_Status", "TEXT", "Projec Status", "25", "", "Prj_Status"],
                ["Lat", "DOUBLE", "Latitude", "", "", ""],
                ["Lon", "DOUBLE", "Longitude", "", "", ""],
            ],
            template=[],
        )

        # Process: Add Treatments Fields (multiple) (2) (Add Fields (multiple)) (management)
        accg_project_table_add_fields_v2 = arcpy.management.AddFields(
            in_table=accg_project_table_add_fields,
            field_description=[
                ["TreatID", "TEXT", "TreatmentID", "50", "", ""],
                ["Treat_Name", "TEXT", "Treatment Name", "100", "", ""],
                ["County", "TEXT", "County", "35", "", "County"],
                ["WUI", "TEXT", "WUI", "3", "", "WUI"],
                ["Prim_Obj", "TEXT", "Primary Objective", "65", "", "Objective"],
                ["Sec_Obj", "TEXT", "Secondary Objective", "65", "", "Objective"],
                ["Tert_Obj", "TEXT", "Tertiary Objective", "65", "", "Objective"],
                ["Category", "TEXT", "Objective Category", "35", "", "Category"],
                ["Retrt_Date", "DATE", "Estimated Retreatment Date", "", "", ""],
                ["Trt_Status", "TEXT", "Treatment Status", "10", "", "Treat_Status"],
                ["TreatStart", "DATE", "Treatment Start Date", "", "", ""],
                ["Treat_End", "DATE", "Treatment End Date", "", "", ""],
                ["Treat_Acre", "DOUBLE", "Treatment Area (Acres)", "255", "", ""],
                ["Ownership", "TEXT", "Ownership Group", "35", "", "Ownership"],
            ],
            template=[],
        )

        # Process: Add Activities Fields (multiple) (2) (Add Fields (multiple)) (management)
        accg_project_table_add_fields_v3 = arcpy.management.AddFields(
            in_table=accg_project_table_add_fields_v2,
            field_description=[
                ["ActivityID", "TEXT", "Activity Id", "50", "", ""],
                ["Act_Name", "TEXT", "Activity Name", "100", "", ""],
                ["P_Fund_Src", "TEXT", "Primary Funding Source Name", "100", "", ""],
                ["P_Fnd_Org", "TEXT", "Primary Funding Org Name", "100", "", ""],
                ["S_Fnd_Src", "TEXT", "Secondary Funding Source Name", "100", "", ""],
                ["S_Fnd_Org", "TEXT", "Secondary Funding Org Name", "100", "", ""],
                ["T_Fnd_Src", "TEXT", "Tertiary Funding Source Name", "100", "", ""],
                ["T_Fnd_Org", "TEXT", "Tertiary Funding Org Name", "100", "", ""],
                ["Admin_Org", "TEXT", "Administering Org Name", "100", "", ""],
                ["Imp_Org", "TEXT", "Implementing Org Name", "100", "", ""],
                ["Act_Desc", "TEXT", "Activity Description", "70", "", "Activity"],
                ["UOM_", "TEXT", "Activity_Unit_of_Measure", "15", "", ""],
                ["Act_Quant", "DOUBLE", "Activity_Quantity", "", "", ""],
                ["Act_Status", "TEXT", "Activity Status", "10", "", "Treat_Status"],
                ["Veg_Type", "TEXT", "Broad Vegetation Type", "50", "", "Veg_Type"],
                ["Residue_Q", "DOUBLE", "Residue Quantity", "", "", ""],
                ["Residue_Fa", "TEXT", "Residue Fate", "35", "", "Residue"],
                ["Act_Start", "DATE", "Activity Start Date", "", "", ""],
                ["Act_End", "DATE", "Activity End Date", "", "", ""],
                ["Act_Percnt", "DOUBLE", "Activity Percent Complete", "", "", ""],
                ["Source", "TEXT", "Source", "65", "", ""],
                ["Year", "LONG", "Calendar Year", "", "", ""],
                ["Year_txt", "TEXT", "Year as Text", "4", "", ""],
                ["Crosswalk", "TEXT", "Crosswalk Activities", "150", "", ""],
                ["Region", "TEXT", "CalFire Region", "35", "", ""],
                ["Act_Code", "LONG", "USFS Activity Code", "", "", ""],
            ],
            template=[],
        )

        # Process: Calculate Admin Org (2) (Calculate Field) (management)
        accg_project_table_calc_field_v1 = arcpy.management.CalculateField(
            in_table=accg_project_table_add_fields_v3,
            field="Prj_Admin",
            expression="!ORGANIZATI!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Reporting Org (2) (Calculate Field) (management)
        accg_project_table_calc_field_v2 = arcpy.management.CalculateField(
            in_table=accg_project_table_calc_field_v1,
            field="Prj_RptOrg",
            expression="!ORGANIZATI!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Field (Calculate Field) (management)
        accg_project_table_calc_field_v3 = arcpy.management.CalculateField(
            in_table=accg_project_table_calc_field_v2,
            field="Prj_Name",
            expression="!NAME!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Projet ID (2) (Calculate Field) (management)
        accg_project_table_calc_field_v4 = arcpy.management.CalculateField(
            in_table=accg_project_table_calc_field_v3,
            field="Prj_ID",
            expression="!OBJECTID!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Treatment ID (2) (Calculate Field) (management)
        accg_project_table_calc_field_v5 = arcpy.management.CalculateField(
            in_table=accg_project_table_calc_field_v4,
            field="TreatmentID",
            expression="!MAINTENANC!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Activity UOM (2) (Calculate Field) (management)
        accg_project_table_calc_field_v6 = arcpy.management.CalculateField(
            in_table=accg_project_table_calc_field_v5,
            field="UOM_",
            expression="!ACRES!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Activity Quantity (2) (Calculate Field) (management)
        accg_project_table_calc_field_v7 = arcpy.management.CalculateField(
            in_table=accg_project_table_calc_field_v6,
            field="Act_Quant",
            expression="!ACRES!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Field (5) (Calculate Field) (management)
        accg_project_table_calc_field_v8 = arcpy.management.CalculateField(
            in_table=accg_project_table_calc_field_v7,
            field="Act_Code",
            expression='"NULL"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Activity End Date (3) (Calculate Field) (management)
        accg_project_table_calc_field_v9 = arcpy.management.CalculateField(
            in_table=accg_project_table_calc_field_v8,
            field="Act_End",
            expression="ifelse(!DATE_COMPLETED!, !DATE_AWARDED!, !DATE_PLANNED!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(DateComp, DateAw, DatePl):
                                                                                    if DateComp != None:
                                                                                        return DateComp
                                                                                    elif DateComp == None:
                                                                                        return DateAw
                                                                                    elif DateAw != None:
                                                                                        return DatePl""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Activity End Date (4) (Calculate Field) (management)
        accg_project_table_calc_field_v10 = arcpy.management.CalculateField(
            in_table=accg_project_table_calc_field_v9,
            field="Act_End",
            expression="ifelse(!DATE_COMPLETED!, !DATE_AWARDED!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(DateComp, DateAw):
                                                                        if DateComp != None:
                                                                            return DateComp
                                                                        elif DateComp == None:
                                                                            return DateAw
                                                                        """,
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Select Layer By Attribute (3) (Select Layer By Attribute) (management)
        accg_project_table_select = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=accg_project_table_calc_field_v10,
            selection_type="NEW_SELECTION",
            where_clause="Act_End IS NULL",
            invert_where_clause="",
        )

        # Process: Calculate Activity End Date (5) (Calculate Field) (management)
        accg_project_table_calc_field_v11 = arcpy.management.CalculateField(
            in_table=accg_project_table_select,
            field="Act_End",
            expression="!DATE_PLANNED!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Select Layer By Attribute (4) (Select Layer By Attribute) (management)
        accg_project_table_calc_field_v12 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=accg_project_table_calc_field_v11,
            selection_type="CLEAR_SELECTION",
            where_clause="",
            invert_where_clause="",
        )

        # Process: Calculate Status (2) (Calculate Field) (management)
        accg_project_table_calc_field_v13 = arcpy.management.CalculateField(
            in_table=accg_project_table_calc_field_v12,
            field="Act_Status",
            expression="ifelse(!DATE_COMPLETED!, !DATE_AWARDED!, !DATE_PLANNED!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(DateComp, DateAw, DatePl):
                                                                                    if DateComp != None:
                                                                                        return \"Complete\"
                                                                                    elif DateAw != None:
                                                                                        return \"Complete\"
                                                                                    elif DatePl >= datetime.datetime(2024, 6, 7):
                                                                                        return \"Out-Year\"
                                                                                    elif DatePl >= datetime.datetime(2012, 6, 7):
                                                                                        return \"Planned\"
                                                                                    else:
                                                                                        return \"Canceled\"
                                                                                    """,
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Source (2) (Calculate Field) (management)
        accg_project_table_calc_field_v14 = arcpy.management.CalculateField(
            in_table=accg_project_table_calc_field_v13,
            field="Source",
            expression='"usfs_timber_harvests"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Year (2) (Calculate Field) (management)
        accg_project_table_calc_field_v15 = arcpy.management.CalculateField(
            in_table=accg_project_table_calc_field_v14,
            field="Year",
            expression="Year($feature.Act_End)",
            expression_type="ARCADE",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Year Text (2) (Calculate Field) (management)
        accg_project_table_calc_field_v16 = arcpy.management.CalculateField(
            in_table=accg_project_table_calc_field_v15,
            field="Year_txt",
            expression="!Year!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Crosswalk (2) (Calculate Field) (management)
        accg_project_table_calc_field_v17 = arcpy.management.CalculateField(
            in_table=accg_project_table_calc_field_v16,
            field="Crosswalk",
            expression="!ACTIVITY_NAME!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="ENFORCE_DOMAINS",
        )

        # Process: Add Join (Add Join) (management)
        accg_addjoin = arcpy.management.AddJoin(
            in_layer_or_view=accg_project_table_calc_field_v17,
            in_field="Act_Code",
            join_table=Fuels_Treatments_Piles_Crosswalk,
            join_field="USFS_Activity_Code",
            join_type="KEEP_ALL",
            index_join_fields="NO_INDEX_JOIN_FIELDS",
        )

        # Process: Calculate Field (2) (Calculate Field) (management)
        accg_addjoin_calc_field_v1 = arcpy.management.CalculateField(
            in_table=accg_addjoin,
            field="usfs_harvests_table2.Prim_Obj",
            expression="!Fuels_Treatments_Piles_Crosswalk.Objective!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Field (3) (Calculate Field) (management)
        accg_addjoin_calc_field_v2 = arcpy.management.CalculateField(
            in_table=accg_addjoin_calc_field_v1,
            field="usfs_harvests_table2.Category",
            expression="!Fuels_Treatments_Piles_Crosswalk.Category!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Field (4) (Calculate Field) (management)
        accg_addjoin_calc_field_v3 = arcpy.management.CalculateField(
            in_table=accg_addjoin_calc_field_v2,
            field="usfs_harvests_table2.Act_Desc",
            expression="!Fuels_Treatments_Piles_Crosswalk.Activity!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Remove Join (Remove Join) (management)
        accg_removejoin = arcpy.management.RemoveJoin(
            in_layer_or_view=accg_addjoin_calc_field_v3,
            join_name="Fuels_Treatments_Piles_Crosswalk",
        )

        # Process: Delete Field (Delete Field) (management)
        accg_keepfields = KeepFields(accg_removejoin)

        # Process: Table To Table (2) (Table To Table) (conversion)
        accg_copy = arcpy.conversion.TableToTable(
            in_rows=accg_keepfields,
            out_path=workspace,
            out_name="accg_copy",
            where_clause="",
            field_mapping="",
            config_keyword="",
        )

        # Process: Select (Select) (analysis)
        ACCG_Project_Select = os.path.join(scratch_workspace, "ACCG_Project_Select")
        with arcpy.EnvManager(
            outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]"""
        ):
            arcpy.analysis.Select(
                in_features=input_fc,
                out_feature_class=ACCG_Project_Select,
                where_clause="DATE_COMPLETED > timestamp '1995-01-01 00:00:00' Or DATE_COMPLETED IS NULL",
            )

        # Process: Repair Geometry (2) (Repair Geometry) (management)
        accg_select_repair_geom = arcpy.management.RepairGeometry(
            in_features=ACCG_Project_Select,
            delete_null="DELETE_NULL",
            validation_method="ESRI",
        )

        # Process: Pairwise Clip (Pairwise Clip) (analysis)
        ACCG_Project_clip = os.path.join(scratch_workspace, "ACCG_Project_clip")
        arcpy.analysis.PairwiseClip(
            in_features=accg_select_repair_geom,
            clip_features=California,
            out_feature_class=ACCG_Project_clip,
            cluster_tolerance="",
        )

        # Process: Dissolve (Dissolve) (management)
        ACCG_Project_dissolved = os.path.join(scratch_workspace, "ACCG_Project_dissolved")
        arcpy.management.Dissolve(
            in_features=ACCG_Project_clip,
            out_feature_class=ACCG_Project_dissolved,
            dissolve_field=[
                "OBJECTID_1",
                "ACRES",
                "STATUS",
                "ORGANIZATI",
                "NEPA_CEQA_",
                "MAINTENANC",
                "MAINTENA_1",
                "NAME",
                "ACTIVITY",
                "TREATMENT",
                "YEAR",
                "OBJECTID",
                "PROJECT",
                "MERGE_SRC",
                "STATUS_ACT",
            ],
            statistics_fields=[],
            multi_part="MULTI_PART",
            unsplit_lines="DISSOLVE_LINES",
            concatenation_separator="",
        )

        # Process: Add Projects Fields (multiple) (3) (Add Fields (multiple)) (management)
        accg_project_fields = arcpy.management.AddFields(
            in_table=ACCG_Project_dissolved,
            field_description=[
                ["Prj_ID", "TEXT", "Project ID", "50", "", ""],
                ["Prj_Name", "TEXT", "Project Name", "150", "", ""],
                ["Prj_FundNM", "TEXT", "Primary Funding Source Name", "130", "", ""],
                ["Prj_FndOrg", "TEXT", "Primary Funding Org Name", "130", "", ""],
                ["Prj_Admin", "TEXT", "Primary Administering Org Name", "130", "", ""],
                ["Prj_Implem", "TEXT", "Primary Implementing Org Name", "130", "", ""],
                ["Prj_RptOrg", "TEXT", "Reporting Org Name", "130", "", ""],
                ["Prj_Contct", "TEXT", "Project Contact", "100", "", ""],
                ["Prj_Email", "TEXT", "Project Email", "100", "", ""],
                ["Prj_Start", "DATE", "Project Start Date", "", "", ""],
                ["Prj_End", "DATE", "Project End Date", "", "", ""],
                ["Prj_Status", "TEXT", "Projec Status", "25", "", ""],
                ["Lat", "DOUBLE", "Latitude", "", "", ""],
                ["Lon", "DOUBLE", "Longitude", "", "", ""],
            ],
            template=[],
        )

        # Process: Add Treatments Fields (multiple) (3) (Add Fields (multiple)) (management)
        accg_treatment_fields = arcpy.management.AddFields(
            in_table=accg_project_fields,
            field_description=[
                ["TreatID", "TEXT", "TreatmentID", "50", "", ""],
                ["Treat_Name", "TEXT", "Treatment Name", "100", "", ""],
                ["County", "TEXT", "County", "35", "", ""],
                ["WUI", "TEXT", "WUI", "3", "", ""],
                ["Prim_Obj", "TEXT", "Primary Objective", "65", "", ""],
                ["Sec_Obj", "TEXT", "Secondary Objective", "65", "", ""],
                ["Tert_Obj", "TEXT", "Tertiary Objective", "65", "", ""],
                ["Category", "TEXT", "Objective Category", "35", "", ""],
                ["Retrt_Date", "DATE", "Estimated Retreatment Date", "", "", ""],
                ["Trt_Status", "TEXT", "Treatment Status", "10", "", ""],
                ["TreatStart", "DATE", "Treatment Start Date", "", "", ""],
                ["Treat_End", "DATE", "Treatment End Date", "", "", ""],
                ["Treat_Acre", "DOUBLE", "Treatment Area (Acres)", "255", "", ""],
                ["Ownership", "TEXT", "Ownership Group", "35", "", ""],
            ],
            template=[],
        )

        # Process: Add Activities Fields (multiple) (3) (Add Fields (multiple)) (management)
        accg_activity_fields = arcpy.management.AddFields(
            in_table=accg_treatment_fields,
            field_description=[
                ["ActivityID", "TEXT", "Activity Id", "50", "", ""],
                ["Act_Name", "TEXT", "Activity Name", "100", "", ""],
                ["P_Fund_Src", "TEXT", "Primary Funding Source Name", "100", "", ""],
                ["P_Fnd_Org", "TEXT", "Primary Funding Org Name", "100", "", ""],
                ["S_Fnd_Src", "TEXT", "Secondary Funding Source Name", "100", "", ""],
                ["S_Fnd_Org", "TEXT", "Secondary Funding Org Name", "100", "", ""],
                ["T_Fnd_Src", "TEXT", "Tertiary Funding Source Name", "100", "", ""],
                ["T_Fnd_Org", "TEXT", "Tertiary Funding Org Name", "100", "", ""],
                ["Admin_Org", "TEXT", "Administering Org Name", "100", "", ""],
                ["Imp_Org", "TEXT", "Implementing Org Name", "150", "", ""],
                ["Act_Desc", "TEXT", "Activity Description", "70", "", ""],
                ["UOM_", "TEXT", "Activity Unit of Measure", "15", "", ""],
                ["Act_Quant", "DOUBLE", "Activity Quantity", "", "", ""],
                ["Act_Status", "TEXT", "Activity Status", "10", "", ""],
                ["Veg_Type", "TEXT", "Broad Vegetation Type", "50", "", ""],
                ["Residue_Q", "DOUBLE", "Residue Quantity", "", "", ""],
                ["Residue_Fa", "TEXT", "Residue Fate", "35", "", ""],
                ["Act_Start", "DATE", "Activity Start Date", "", "", ""],
                ["Act_End", "DATE", "Activity End Date", "", "", ""],
                ["Act_Percnt", "DOUBLE", "Activity Percent Complete", "", "", ""],
                ["Source", "TEXT", "Source", "65", "", ""],
                ["Year", "LONG", "Calendar Year", "", "", ""],
                ["Year_txt", "TEXT", "Year as Text", "4", "", ""],
                ["Crosswalk", "TEXT", "Crosswalk Activities", "150", "", ""],
                ["Region", "TEXT", "CalFire Region", "35", "", ""],
                ["Federal_FY", "LONG", "Federal FY", "", "", ""],
                ["State_FY", "LONG", "State FY", "", "", ""],
                ["Act_Code", "LONG", "USFS Activity Code", "", "", ""],
            ],
            template=[],
        )

        # Process: Calculate Admin Org (3) (Calculate Field) (management)
        accg_calc_field_v1 = arcpy.management.CalculateField(
            in_table=accg_activity_fields,
            field="Admin_Org",
            expression="!ORGANIZATI!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Reporting Org (3) (Calculate Field) (management)
        accg_calc_field_v2 = arcpy.management.CalculateField(
            in_table=accg_calc_field_v1,
            field="Prj_RptOrg",
            expression="!ORGANIZATI!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Imp Org (3) (Calculate Field) (management)
        accg_calc_field_v3 = arcpy.management.CalculateField(
            in_table=accg_calc_field_v2,
            field="Imp_Org",
            expression="!ORGANIZATI!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Project Name (Calculate Field) (management)
        accg_calc_field_v4 = arcpy.management.CalculateField(
            in_table=accg_calc_field_v3,
            field="Prj_Name",
            expression="!PROJECT!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Project ID (Calculate Field) (management)
        accg_calc_field_v5 = arcpy.management.CalculateField(
            in_table=accg_calc_field_v4,
            field="Prj_ID",
            expression="!OBJECTID!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Treatment ID (3) (Calculate Field) (management)
        accg_calc_field_v6 = arcpy.management.CalculateField(
            in_table=accg_calc_field_v5,
            field="TreatID",
            expression="!MAINTENANC!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Activity UOM (3) (Calculate Field) (management)
        accg_calc_field_v7 = arcpy.management.CalculateField(
            in_table=accg_calc_field_v6,
            field="UOM_",
            expression='"ACRES"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Activity Quantity (3) (Calculate Field) (management)
        accg_calc_field_v8 = arcpy.management.CalculateField(
            in_table=accg_calc_field_v7,
            field="Act_Quant",
            expression="!ACRES!",
            expression_type="PYTHON3",
            code_block="",
            field_type="DOUBLE",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Activity End Date (Calculate Field) (management)
        accg_calc_field_v9 = arcpy.management.CalculateField(
            in_table=accg_calc_field_v8,
            field="Act_End",
            expression='!YEAR! + "-12-31"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
        accg_year_not_null = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=accg_calc_field_v9,
            selection_type="NEW_SELECTION",
            where_clause="YEAR IS NOT NULL",
            invert_where_clause="",
        )

        # Process: Calculate Activity End Date (2) (Calculate Field) (management)
        accg_calc_act_end = arcpy.management.CalculateField(
            in_table=accg_year_not_null,
            field="Act_End",
            expression='!YEAR! + "-12-31"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Select Layer By Attribute (2) (Select Layer By Attribute) (management)
        accg_clear_selection = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=accg_calc_act_end,
            selection_type="CLEAR_SELECTION",
            where_clause="",
            invert_where_clause="",
        )

        # Process: Calculate Status (3) (Calculate Field) (management)
        accg_calc_status = arcpy.management.CalculateField(
            in_table=accg_clear_selection,
            field="Act_Status",
            expression="ifelse(!STATUS!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(STATUS):
                                                                if STATUS != None:
                                                                        return \"Complete\"
                                                                elif STATUS != None:
                                                                        return \"Complete\"
                                                                elif STATUS >= datetime.datetime(2024):
                                                                        return \"Implementation\"
                                                                elif STATUS >= datetime.datetime(2007):
                                                                        return \"Planned\"
                                                                else:
                                                                        return \"Canceled\"
                                                                """,
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Source (3) (Calculate Field) (management)
        accg_calc_src = arcpy.management.CalculateField(
            in_table=accg_calc_status,
            field="Source",
            expression='"ACCG_Stakeholder"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Year (3) (Calculate Field) (management)
        accg_calc_year = arcpy.management.CalculateField(
            in_table=accg_calc_src,
            field="Year",
            expression="Year($feature.Act_End)",
            expression_type="ARCADE",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Year Text (3) (Calculate Field) (management)
        accg_calc_text = arcpy.management.CalculateField(
            in_table=accg_calc_year,
            field="Year_txt",
            expression="!Year!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Crosswalk (3) (Calculate Field) (management)
        accg_calc_xwalk = arcpy.management.CalculateField(
            in_table=accg_calc_text,
            field="Crosswalk",
            expression="!ACTIVITY!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate USFS Activity Code (Calculate Field) (management)
        accg_calc_usfs_act_code = arcpy.management.CalculateField(
            in_table=accg_calc_xwalk,
            field="Act_Code",
            expression='"NULL"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Geometry Attributes (3) (Calculate Geometry Attributes) (management)
        accg_calc_latlong = arcpy.management.CalculateGeometryAttributes(
            in_features=accg_calc_usfs_act_code,
            geometry_property=[["Lat", "INSIDE_Y"], ["Lon", "INSIDE_X"]],
            length_unit="",
            area_unit="",
            coordinate_system='GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]',
            coordinate_format="DD",
        )

        # Process: Calculate Geometry Attributes (4) (Calculate Geometry Attributes) (management)
        accg_calc_acres = arcpy.management.CalculateGeometryAttributes(
            in_features=accg_calc_latlong,
            geometry_property=[["Treat_Acre", "AREA"]],
            length_unit="",
            area_unit="ACRES",
            coordinate_system='PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]',
            coordinate_format="SAME_AS_INPUT",
        )

        # Process: Copy Features (3) (Copy Features) (management)
        # ACCG_Stakeholder_standardized_20220828 = os.path.join(scratch_workspace, "ACCG_Stakeholder_standardized_20220828")
        arcpy.management.CopyFeatures(
            in_features=accg_calc_acres,
            out_feature_class=output_standardized,
            config_keyword="",
            spatial_grid_1=None,
            spatial_grid_2=None,
            spatial_grid_3=None,
        )

        print("Deleting Scratch Files")
        delete_scratch_files(
            gdb=scratch_workspace, delete_fc="yes", delete_table="yes", delete_ds="yes"
        )

        end = time.time()
        print(f"Time Elapsed: {(end-start)/60} minutes")
    return accg_copy

