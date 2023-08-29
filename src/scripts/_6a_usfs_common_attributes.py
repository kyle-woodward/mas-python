import arcpy
from ._1b_add_fields import AddFields
from ._2b_assign_domains import AssignDomains
from ._7a_enrichments_polygon import enrich_polygons
from ._2k_keep_fields import KeepFields
from sys import argv
from .utils import init_gdb, delete_scratch_files, runner
import os
import time

original_gdb, workspace, scratch_workspace = init_gdb()


def Model_USFS(output_enriched, output_standardized, input_fc):
    start = time.time()
    print(f"Start Time {time.ctime()}")
    arcpy.env.overwriteOutput = True

    # START and END YEARS
    startyear = 2020
    endyear = 2025

    # define intermediary objects in scratch
    usfs_intermediate_scratch = os.path.join(
        scratch_workspace, "usfs_intermediate_scratch"
    )
    usfs_intermediate_scratch_dissolved = os.path.join(
        scratch_workspace, "usfs_intermediate_scratch_dissolved"
    )
    usfs_scratch_standardized = os.path.join(
        scratch_workspace, "usfs_scratch_standardized"
    )

    # Model Environment settings
    with arcpy.EnvManager(
        outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]"""
    ):
        print("Performing Standardization...")
        # Process: Select Layer By Attribute California (Select Layer By Attribute) (management)
        usfs_CA = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=input_fc,
            selection_type="NEW_SELECTION",
            where_clause="STATE_ABBR = 'CA'",
            invert_where_clause="",
        )

        print("   step 1/8 Selecting Features...")
        # Process: Select Layer By Attribute Activity Code (Select Layer By Attribute) (management)
        usfs_select_activities, Count_3_ = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=usfs_CA,
            selection_type="SUBSET_SELECTION",
            where_clause="""ACTIVITY_CODE = '1102' Or 
                            ACTIVITY_CODE = '1111' Or
                            ACTIVITY_CODE = '1112' Or
                            ACTIVITY_CODE = '1113' Or
                            ACTIVITY_CODE = '1115' Or
                            ACTIVITY_CODE = '1116' Or
                            ACTIVITY_CODE = '1117' Or
                            ACTIVITY_CODE = '1118' Or
                            ACTIVITY_CODE = '1119' Or
                            ACTIVITY_CODE = '1120' Or
                            ACTIVITY_CODE = '1130' Or
                            ACTIVITY_CODE = '1136' Or
                            ACTIVITY_CODE = '1139' Or
                            ACTIVITY_CODE = '1150' Or
                            ACTIVITY_CODE = '1152' Or
                            ACTIVITY_CODE = '1153' Or
                            ACTIVITY_CODE = '1154' Or
                            ACTIVITY_CODE = '1160' Or
                            ACTIVITY_CODE = '1180' Or
                            ACTIVITY_CODE = '2000' Or
                            ACTIVITY_CODE = '2341' Or
                            ACTIVITY_CODE = '2360' Or
                            ACTIVITY_CODE = '2370' Or
                            ACTIVITY_CODE = '2510' Or
                            ACTIVITY_CODE = '2530' Or
                            ACTIVITY_CODE = '2540' Or
                            ACTIVITY_CODE = '2560' Or
                            ACTIVITY_CODE = '3132' Or
                            ACTIVITY_CODE = '4101' Or
                            ACTIVITY_CODE = '4102' Or
                            ACTIVITY_CODE = '4111' Or
                            ACTIVITY_CODE = '4113' Or
                            ACTIVITY_CODE = '4115' Or
                            ACTIVITY_CODE = '4117' Or
                            ACTIVITY_CODE = '4121' Or
                            ACTIVITY_CODE = '4122' Or
                            ACTIVITY_CODE = '4131' Or
                            ACTIVITY_CODE = '4132' Or
                            ACTIVITY_CODE = '4141' Or
                            ACTIVITY_CODE = '4142' Or
                            ACTIVITY_CODE = '4143' Or
                            ACTIVITY_CODE = '4145' Or
                            ACTIVITY_CODE = '4146' Or
                            ACTIVITY_CODE = '4148' Or
                            ACTIVITY_CODE = '4151' Or
                            ACTIVITY_CODE = '4152' Or
                            ACTIVITY_CODE = '4162' Or
                            ACTIVITY_CODE = '4162' Or
                            ACTIVITY_CODE = '4175' Or
                            ACTIVITY_CODE = '4177' Or
                            ACTIVITY_CODE = '4183' Or
                            ACTIVITY_CODE = '4192' Or
                            ACTIVITY_CODE = '4193' Or
                            ACTIVITY_CODE = '4194' Or
                            ACTIVITY_CODE = '4196' Or
                            ACTIVITY_CODE = '4210' Or
                            ACTIVITY_CODE = '4211' Or
                            ACTIVITY_CODE = '4220' Or
                            ACTIVITY_CODE = '4231' Or
                            ACTIVITY_CODE = '4232' Or
                            ACTIVITY_CODE = '4241' Or
                            ACTIVITY_CODE = '4242' Or
                            ACTIVITY_CODE = '4250' Or
                            ACTIVITY_CODE = '4270' Or
                            ACTIVITY_CODE = '4280' Or
                            ACTIVITY_CODE = '4290' Or
                            ACTIVITY_CODE = '4291' Or
                            ACTIVITY_CODE = '4382' Or
                            ACTIVITY_CODE = '4411' Or
                            ACTIVITY_CODE = '4412' Or
                            ACTIVITY_CODE = '4431' Or
                            ACTIVITY_CODE = '4432' Or
                            ACTIVITY_CODE = '4455' Or
                            ACTIVITY_CODE = '4471' Or
                            ACTIVITY_CODE = '4472' Or
                            ACTIVITY_CODE = '4473' Or
                            ACTIVITY_CODE = '4474' Or
                            ACTIVITY_CODE = '4475' Or
                            ACTIVITY_CODE = '4481' Or
                            ACTIVITY_CODE = '4482' Or
                            ACTIVITY_CODE = '4483' Or
                            ACTIVITY_CODE = '4484' Or
                            ACTIVITY_CODE = '4485' Or
                            ACTIVITY_CODE = '4490' Or
                            ACTIVITY_CODE = '4491' Or
                            ACTIVITY_CODE = '4492' Or
                            ACTIVITY_CODE = '4493' Or
                            ACTIVITY_CODE = '4494' Or
                            ACTIVITY_CODE = '4495' Or
                            ACTIVITY_CODE = '4511' Or
                            ACTIVITY_CODE = '4521' Or
                            ACTIVITY_CODE = '4530' Or
                            ACTIVITY_CODE = '4540' Or
                            ACTIVITY_CODE = '4541' Or
                            ACTIVITY_CODE = '4550' Or
                            ACTIVITY_CODE = '4580' Or
                            ACTIVITY_CODE = '6101' Or
                            ACTIVITY_CODE = '6103' Or
                            ACTIVITY_CODE = '6104' Or
                            ACTIVITY_CODE = '6105' Or
                            ACTIVITY_CODE = '6106' Or
                            ACTIVITY_CODE = '6107' Or
                            ACTIVITY_CODE = '6133' Or
                            ACTIVITY_CODE = '6584' Or
                            ACTIVITY_CODE = '6684' Or
                            ACTIVITY_CODE = '7015' Or
                            ACTIVITY_CODE = '7050' Or
                            ACTIVITY_CODE = '7065' Or
                            ACTIVITY_CODE = '7067' Or
                            ACTIVITY_CODE = '9008' Or
                            ACTIVITY_CODE = '9400'""",
            invert_where_clause="",
        )

        # Process: Select Layer By Attribute Non-Wildfire (Select Layer By Attribute) (management)
        usfs_non_wildfire = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=usfs_select_activities,
            selection_type="SUBSET_SELECTION",
            where_clause="ACTIVITY_CODE = '1117' And FUELS_KEYPOINT_AREA <> '6'",
            invert_where_clause="INVERT",
        )

        # Process: Select Layer By Attribute Non-Wildfire (Select Layer By Attribute) (management)
        usfs_non_wildfire = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=usfs_non_wildfire,
            selection_type="SUBSET_SELECTION",
            where_clause="ACTIVITY_CODE = '1117' And FUELS_KEYPOINT_AREA IS NULL",
            invert_where_clause="INVERT",
        )

        # Process: Select Layer By Attribute Non-Wildfire (Select Layer By Attribute) (management)
        usfs_non_wildfire_v2 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=usfs_non_wildfire,
            selection_type="SUBSET_SELECTION",
            where_clause="ACTIVITY_CODE = '1119' And FUELS_KEYPOINT_AREA <> '6'",
            invert_where_clause="INVERT",
        )

        # Process: Select Layer By Attribute Non-Wildfire (Select Layer By Attribute) (management)
        usfs_non_wildfire_v3 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=usfs_non_wildfire_v2,
            selection_type="SUBSET_SELECTION",
            where_clause="ACTIVITY_CODE = '1119' And FUELS_KEYPOINT_AREA IS NULL",
            invert_where_clause="INVERT",
        )

        # Process: Select Layer By Attribute Date is not NULL (Select Layer By Attribute) (management)
        usfs_non_wildfire_date_not_null = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=usfs_non_wildfire_v3,
            selection_type="SUBSET_SELECTION",
            where_clause="DATE_COMPLETED IS NULL And DATE_AWARDED IS NULL And NEPA_SIGNED_DATE IS NULL",
            invert_where_clause="INVERT",
        )

        # Process: Select Layer By Attribute Date (Select Layer By Attribute) (management)
        usfs_non_wildfire_after_1995 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=usfs_non_wildfire_date_not_null,
            selection_type="SUBSET_SELECTION",
            # where_clause="DATE_COMPLETED > timestamp '1995-01-01 00:00:00' Or DATE_COMPLETED IS NULL",
            where_clause="DATE_COMPLETED > timestamp '%d-01-01 00:00:00' Or DATE_COMPLETED IS NULL"
            % startyear,
            invert_where_clause="",
        )

        # Process: Copy Features (2) (Copy Features) (management)
        usfs_non_wildfire_after_1995_copy = arcpy.management.CopyFeatures(
            usfs_non_wildfire_after_1995, usfs_intermediate_scratch
        )

        print("   step 2/8 Repairing Geometry...")
        # Process: Repair Geometry (Repair Geometry) (management)
        usfs_non_wildfire_after_1995_repaired_geom = arcpy.management.RepairGeometry(
            in_features=usfs_non_wildfire_after_1995_copy,
            delete_null="KEEP_NULL",
            validation_method="ESRI",
        )

        # Process: Alter Field Treatment Name
        usfs_non_wildfire_after_1995_repaired_geom2 = arcpy.management.AlterField(
            usfs_non_wildfire_after_1995_repaired_geom,
            "TREATMENT_NAME",
            "TREATMENT_NAME_FACTS",
        )

        print("   step 3/8 Adding Fields...")
        # Process: 1b Add Fields (1b Add Fields) (PC414CWIMillionAcres)
        usfs_non_wildfire_after_1995_w_fields = AddFields(
            Input_Table=usfs_non_wildfire_after_1995_repaired_geom2
        )

        print("   step 4/8 Transfering Attributes...")
        # Process: Calculate Project ID (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v1 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_w_fields,
            field="PROJECTID_USER",
            expression="!NEPA_DOC_NBR!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Agency (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v2 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v1,
            field="AGENCY",
            expression='"USDA"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Data Steward (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v3 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v2,
            field="ORG_ADMIN_p",
            expression='"USFS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Data Steward 2 (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v3a = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v3,
            field="ORG_ADMIN_t",
            expression='"USFS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Data Steward 3 (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v3b = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v3a,
            field="ORG_ADMIN_a",
            expression='"USFS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Project Contact (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v4 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v3b,
            field="PROJECT_CONTACT",
            expression='"Tawndria Melville"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Project Email (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v5 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v4,
            field="PROJECT_EMAIL",
            expression='"tawndria.melville@usda.gov"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Admin Org (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v6 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v5,
            field="ADMINISTERING_ORG",
            expression='"USFS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Project Name (Calculate Field) (management)
        # Updated_Input_Table_33_ = arcpy.management.CalculateField(
        #     in_table=Updated_Input_Table_31_,
        #     field="PROJECT_NAME",
        #     expression="\"None\"", # "NONE"
        #     expression_type="PYTHON3",
        #     code_block="",
        #     field_type="TEXT",
        #     enforce_domains="NO_ENFORCE_DOMAINS"
        #     )

        # Process: Calculate Fund Source (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v7 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v6,
            field="PRIMARY_FUNDING_SOURCE",
            expression='"USFS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Fund Org (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v8 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v7,
            field="PRIMARY_FUNDING_ORG",
            expression='"USFS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Imp Org (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v9 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v8,
            field="IMPLEMENTING_ORG",
            expression='"Pacific Southwest Regional Office"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Treatment ID (Calculate Field) (management) after enrichment

        # Process: Calculate Activity User ID (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v11 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v9,
            field="ACTIVID_USER",
            expression="!SUID!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Veg User Defined (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v12 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v11,
            field="BVT_USERD",
            expression='"NO"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate WUI (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v13 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v12,
            field="IN_WUI",
            expression="ifelse(!ISWUI!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(WUI):
                            if WUI == \"Y\":
                                return \"WUI_USER_DEFINED\"
                            elif WUI == \"N\":
                                return \"NON-WUI_USER_DEFINED\"
                            else:
                                return None""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        print("   step 5/8 Calculating End Date...")
        # Process: Calculate Activity End Date (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v14 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v13,
            field="ACTIVITY_END",
            expression="ifelse(!DATE_COMPLETED!, !DATE_AWARDED!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(DateComp, DateAw):
                            if DateComp != None:
                                return DateComp
                            elif DateComp == None:
                                return DateAw""",
            field_type="DATE",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
        usfs_non_wildfire_after_1995_selection = (
            arcpy.management.SelectLayerByAttribute(
                in_layer_or_view=usfs_non_wildfire_after_1995_calc_field_v14,
                selection_type="NEW_SELECTION",
                where_clause="ACTIVITY_END IS NULL",
                invert_where_clause="",
            )
        )

        # Process: Calculate Activity End Date (4) (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v15 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_selection,
            field="ACTIVITY_END",
            expression="!NEPA_SIGNED_DATE!",
            expression_type="PYTHON3",
            code_block="",
            field_type="DATE",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Select Layer By Attribute (2) (Select Layer By Attribute) (management)
        usfs_non_wildfire_after_1995_clear_selection = (
            arcpy.management.SelectLayerByAttribute(
                in_layer_or_view=usfs_non_wildfire_after_1995_calc_field_v15,
                selection_type="CLEAR_SELECTION",
                where_clause="",
                invert_where_clause="",
            )
        )

        print("   step 6/8 Calculating Status...")
        # Process: Calculate Status (Calculate Field) (management)
        # TODO: Based on Today's Date.  Need to add Date formula
        usfs_non_wildfire_after_1995_calc_field_v16 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_clear_selection,
            field="ACTIVITY_STATUS",
            expression="ifelse(!DATE_COMPLETED!, !DATE_AWARDED!, !NEPA_SIGNED_DATE!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(DateComp, DateAw, DatePl):
                            if DateComp != None:
                                return \"COMPLETE\"
                            elif DateAw != None:
                                return \"ACTIVE\"
                            elif DatePl >= datetime.datetime(2024, 10, 15):
                                return \"OUTYEAR\"
                            elif DatePl >= datetime.datetime(2012, 10, 15):
                                return \"PLANNED\"
                            else:
                                return \"CANCELLED\"""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Activity Quantity (3) (Calculate Field) (management)
        print("   step 7/8 Activity Quantity...")
        usfs_non_wildfire_after_1995_calc_field_v17 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v16,
            field="ACTIVITY_QUANTITY",
            expression="ifelse(!NBR_UNITS_ACCOMPLISHED!, !NBR_UNITS_PLANNED!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(ACC, PLANNED):
                            if ACC != None:
                                return ACC
                            if ACC == None:
                                return PLANNED""",
            field_type="DOUBLE",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Activity UOM (3) (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v18 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v17,
            field="ACTIVITY_UOM",
            expression="!UOM!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Admin Org2 (Calculate Field) (management)
        print("   step 8/8 Enter Field Values...")
        usfs_non_wildfire_after_1995_calc_field_v19 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v18,
            field="ADMIN_ORG_NAME",
            expression='"USFS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Implementation Org 2 (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v20 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v19,
            field="IMPLEM_ORG_NAME",
            expression="!WORKFORCE_CODE!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Primary Fund Source (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v21 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v20,
            field="PRIMARY_FUND_SRC_NAME",
            expression='"USFS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Fund Org 2 (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v22 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v21,
            field="PRIMARY_FUND_ORG_NAME",
            expression='"USFS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Activity Name (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v23 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v22,
            field="ACTIVITY_NAME",
            expression="None",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Source (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v24 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v23,
            field="Source",
            expression='"usfs_treatments"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Year (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v25 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v24,
            field="Year",
            expression="Year($feature.ACTIVITY_END)",
            expression_type="ARCADE",
            code_block="",
            field_type="LONG",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Crosswalk (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v26 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v25,
            field="Crosswalk",
            expression="ifelse(!ACTIVITY!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(Act):
                            if Act == \"Piling of Fuels, Hand or Machine \":
                                return \"Piling of Fuels, Hand or Machine\"
                            else:
                                return Act""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Treatment Geometry (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v27 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v26,
            field="TRMT_GEOM",
            expression="ifelse(!ACTIVITY!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(Geom):
                            if Geom == \'A\':
                                return \'POLYGON\'
                            elif Geom == \'L\':
                                return \'LINE\'
                            elif Geom == \'P\':
                                return \'POINT\'
                            else: 
                                return Geom""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate USFS Activity Code (Calculate Field) (management)
        usfs_non_wildfire_after_1995_calc_field_v28 = arcpy.management.CalculateField(
            in_table=usfs_non_wildfire_after_1995_calc_field_v27,
            field="Act_Code",
            expression="!ACTIVITY_CODE!",
            expression_type="PYTHON3",
            code_block="",
            field_type="LONG",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Copy Features (Copy Features) (management)
        arcpy.management.CopyFeatures(
            in_features=usfs_non_wildfire_after_1995_calc_field_v28,
            out_feature_class=usfs_scratch_standardized,
        )

        # Process: Delete Field (Delete Field) (management)
        usfs_scratch_standardized_keep_fields = KeepFields(usfs_scratch_standardized)

        print(f"Saving Standardized Output: {output_standardized}")
        # Process: Select by Years (Select) (analysis)
        arcpy.analysis.Select(
            in_features=usfs_scratch_standardized_keep_fields,
            out_feature_class=output_standardized,
            where_clause="Year >= %d And Year <= %d" % (startyear, endyear),
        )

        # Process: 2b Assign Domains (2b Assign Domains) (PC414CWIMillionAcres)
        usfs_standardized_w_domains = AssignDomains(in_table=output_standardized)

        # print("Enriching Dataset")
        # Process: 7a Enrichments Polygon (2) (7a Enrichments Polygon) (PC414CWIMillionAcres)
        enrich_polygons(
            enrich_in=usfs_standardized_w_domains, enrich_out=output_enriched
        )

        print(f"Saving Enriched Output: {output_enriched}")

        arcpy.management.CalculateField(
            in_table=output_enriched,
            field="TRMTID_USER",
            expression="!ACTIVID_USER!+'-'+!PRIMARY_OBJECTIVE![:8]",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: 2b Assign Domains (2) (2b Assign Domains) (PC414CWIMillionAcres)
        AssignDomains(in_table=output_enriched)

        # print('   Deleting Scratch Files')
        delete_scratch_files(
            gdb=scratch_workspace, delete_fc="yes", delete_table="yes", delete_ds="yes"
        )

        end = time.time()
        print(f"Time Elapsed: {(end-start)/60} minutes")


if __name__ == "__main__":
    runner(workspace, scratch_workspace, Model_USFS, "*argv[1:]")
# # Global Environment settings
#  with arcpy.EnvManager(
#     overwriteOutput=True,
#     extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""",  outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""",
#     preserveGlobalIds=True,
#     qualifiedFieldNames=False,
#     scratchWorkspace=scratch_workspace,
#     transferDomains=True,
#     transferGDBAttributeProperties=True,
#     workspace=workspace):
#         Model_USFS(*argv[1:])
