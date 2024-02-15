"""
# Description: Converts the U.S. Forest Service EDW FACTS Common Attributes dataset 
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
from ._3_enrichments_polygon import enrich_polygons
from ._3_keep_fields import KeepFields
from .utils import init_gdb, delete_scratch_files

workspace, scratch_workspace = init_gdb()

def Model_USFS(
      input_fc, 
      startyear, 
      endyear, 
      output_enriched, 
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
        intermediate_scratch = os.path.join(scratch_workspace, "usfs_intermediate_scratch")
        scratch_standardized = os.path.join(scratch_workspace, "scratch_standardized")
        output_standardized = os.path.join(scratch_workspace, "USFS_standardized")

        ### BEGIN TOOL CHAIN
        print("Performing Standardization...")
        select_CA = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=input_fc,
            selection_type="NEW_SELECTION",
            where_clause="STATE_ABBR = 'CA'",
            invert_where_clause="",
        )

        print("   step 1/8 Selecting Features...")
        select_activities = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=select_CA,
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

        select_non_wildfire = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=select_activities,
            selection_type="SUBSET_SELECTION",
            where_clause="ACTIVITY_CODE = '1117' And FUELS_KEYPOINT_AREA <> '6'",
            invert_where_clause="INVERT",
        )

        select_non_wildfire_2 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=select_non_wildfire,
            selection_type="SUBSET_SELECTION",
            where_clause="ACTIVITY_CODE = '1117' And FUELS_KEYPOINT_AREA IS NULL",
            invert_where_clause="INVERT",
        )

        select_non_wildfire_3 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=select_non_wildfire_2,
            selection_type="SUBSET_SELECTION",
            where_clause="ACTIVITY_CODE = '1119' And FUELS_KEYPOINT_AREA <> '6'",
            invert_where_clause="INVERT",
        )

        select_non_wildfire_4 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=select_non_wildfire_3,
            selection_type="SUBSET_SELECTION",
            where_clause="ACTIVITY_CODE = '1119' And FUELS_KEYPOINT_AREA IS NULL",
            invert_where_clause="INVERT",
        )

        select_date_not_null = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=select_non_wildfire_4,
            selection_type="SUBSET_SELECTION",
            where_clause="DATE_COMPLETED IS NULL And DATE_AWARDED IS NULL And NEPA_SIGNED_DATE IS NULL",
            invert_where_clause="INVERT",
        )

        select_date_after_1995 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=select_date_not_null,
            selection_type="SUBSET_SELECTION",
            where_clause="DATE_COMPLETED > timestamp '%d-01-01 00:00:00' Or DATE_COMPLETED IS NULL" % startyear,
            invert_where_clause="",
        )

        save_selected = arcpy.management.CopyFeatures(
            select_date_after_1995, intermediate_scratch
        )

        Count1 = arcpy.management.GetCount(save_selected)
        print("Selected Activities have {} records".format(Count1[0]))

        print("   step 2/8 Repairing Geometry...")
        repair_geom = arcpy.management.RepairGeometry(
            in_features=save_selected,
            delete_null="KEEP_NULL",
            validation_method="ESRI",
        )

        alterfield_1 = arcpy.management.AlterField(
            repair_geom,
            "TREATMENT_NAME",
            "TREATMENT_NAME_FACTS",
        )

        alterfield_2 = arcpy.management.AlterField(
            alterfield_1,
            "LATITUDE",
            "LATITUDE_",
        )

        alterfield_3 = arcpy.management.AlterField(
            alterfield_2,
            "LONGITUDE",
            "LONGITUDE_",
        )

        print("   step 3/8 Adding Fields...")
        addfields_1 = AddFields(
            Input_Table=alterfield_3
        )

        print("   step 4/8 Transfering Attributes...")
        calc_field_1 = arcpy.management.CalculateField(
            in_table=addfields_1,
            field="PROJECTID_USER",
            expression="'USFS'+'-'+!NEPA_DOC_NBR!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_2 = arcpy.management.CalculateField(
            in_table=calc_field_1,
            field="AGENCY",
            expression='"USDA"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_3 = arcpy.management.CalculateField(
            in_table=calc_field_2,
            field="ORG_ADMIN_p",
            expression='"USFS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_4 = arcpy.management.CalculateField(
            in_table=calc_field_3,
            field="ORG_ADMIN_t",
            expression='"USFS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_5 = arcpy.management.CalculateField(
            in_table=calc_field_4,
            field="ORG_ADMIN_a",
            expression='"USFS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_6 = arcpy.management.CalculateField(
            in_table=calc_field_5,
            field="PROJECT_CONTACT",
            expression='"Tawndria Melville"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_7 = arcpy.management.CalculateField(
            in_table=calc_field_6,
            field="PROJECT_EMAIL",
            expression='"tawndria.melville@usda.gov"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_8 = arcpy.management.CalculateField(
            in_table=calc_field_7,
            field="ADMINISTERING_ORG",
            expression='"USFS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_9 = arcpy.management.CalculateField(
            in_table=calc_field_8,
            field="PRIMARY_FUNDING_SOURCE",
            expression='"FEDERAL"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_10 = arcpy.management.CalculateField(
            in_table=calc_field_9,
            field="PRIMARY_FUNDING_ORG",
            expression='"USFS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_11 = arcpy.management.CalculateField(
            in_table=calc_field_10,
            field="IMPLEMENTING_ORG",
            expression='"Pacific Southwest Regional Office"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_11a = arcpy.management.CalculateField(
            in_table=calc_field_11,
            field="TRMTID_USER",
            expression="!SUID!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_12 = arcpy.management.CalculateField(
            in_table=calc_field_11a,
            field="ACTIVID_USER",
            expression="!SUID!+'-'+!OBJECTID!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_13 = arcpy.management.CalculateField(
            in_table=calc_field_12,
            field="BVT_USERD",
            expression='"NO"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_14 = arcpy.management.CalculateField(
            in_table=calc_field_13,
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
        calc_field_15 = arcpy.management.CalculateField(
            in_table=calc_field_14, 
            field="ACTIVITY_END", 
            expression="!DATE_COMPLETED!", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="DATE", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        select_date_null_1 = arcpy.management.SelectLayerByAttribute(
                in_layer_or_view=calc_field_15,
                selection_type="NEW_SELECTION",
                where_clause="ACTIVITY_END IS NULL",
                invert_where_clause="",
            )

        calc_field_16 = arcpy.management.CalculateField(
            in_table=select_date_null_1,
            field="ACTIVITY_END",
            expression="!NEPA_SIGNED_DATE!",
            expression_type="PYTHON3",
            code_block="",
            field_type="DATE",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        clear_selection_1 = arcpy.management.SelectLayerByAttribute(
                in_layer_or_view=calc_field_16,
                selection_type="CLEAR_SELECTION",
                where_clause="",
                invert_where_clause="",
            )

        print("   step 6/8 Calculating Status...")
        # TODO: Based on Today's Date.  Need to add Date formula
        calc_field_17 = arcpy.management.CalculateField(
            in_table=clear_selection_1,
            field="ACTIVITY_STATUS",
            expression="ifelse(!DATE_COMPLETED!, !DATE_AWARDED!, !NEPA_SIGNED_DATE!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(DateComp, DateAw, DatePl):
                            if DateComp != None:
                                return \"COMPLETE\"
                            elif DateAw != None:
                                return \"ACTIVE\"
                            elif DatePl >= datetime.datetime(2025, 1, 24): # 2 years in the future
                                return \"OUTYEAR\"
                            elif DatePl >= datetime.datetime(2014, 1, 24): # 10 years in the past
                                return \"PLANNED\"
                            else:
                                return \"CANCELLED\"""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        print("   step 7/8 Activity Quantity...")
        calc_field_18 = arcpy.management.CalculateField(
            in_table=calc_field_17,
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

        calc_field_19 = arcpy.management.CalculateField(
            in_table=calc_field_18,
            field="ACTIVITY_UOM",
            expression="!UOM!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        print("   step 8/8 Enter Field Values...")
        calc_field_20 = arcpy.management.CalculateField(
            in_table=calc_field_19,
            field="ADMIN_ORG_NAME",
            expression='"USFS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_21 = arcpy.management.CalculateField(
            in_table=calc_field_20,
            field="IMPLEM_ORG_NAME",
            expression="!WORKFORCE_CODE!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_22 = arcpy.management.CalculateField(
            in_table=calc_field_21,
            field="PRIMARY_FUND_SRC_NAME",
            expression='"USFS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_23 = arcpy.management.CalculateField(
            in_table=calc_field_22,
            field="PRIMARY_FUND_ORG_NAME",
            expression='"USFS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_24 = arcpy.management.CalculateField(
            in_table=calc_field_23,
            field="ACTIVITY_NAME",
            expression="None",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_25 = arcpy.management.CalculateField(
            in_table=calc_field_24,
            field="Source",
            expression='"usfs_treatments"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_26 = arcpy.management.CalculateField(
            in_table=calc_field_25,
            field="Year",
            expression="Year($feature.ACTIVITY_END)",
            expression_type="ARCADE",
            code_block="",
            field_type="LONG",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_27 = arcpy.management.CalculateField(
            in_table=calc_field_26,
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

        calc_field_28 = arcpy.management.CalculateField(
            in_table=calc_field_27,
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
                                return \'POLYGON\'""", 
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_29 = arcpy.management.CalculateField(
            in_table=calc_field_28,
            field="Act_Code",
            expression="!ACTIVITY_CODE!",
            expression_type="PYTHON3",
            code_block="",
            field_type="LONG",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        arcpy.management.CopyFeatures(
            in_features=calc_field_29,
            out_feature_class=scratch_standardized,
        )

        keepfields_1 = KeepFields(scratch_standardized)

        print(f"Saving Standardized Output")
        select_years = arcpy.analysis.Select(
            in_features=keepfields_1,
            out_feature_class=output_standardized,
            where_clause="Year >= %d And Year <= %d" % (startyear, endyear),
        )

        print("Enriching Dataset")
        enrich_polygons(
            enrich_in=select_years,
            enrich_out=output_enriched            
        )
        print(f'Saving Enriched Output')

        Count2 = arcpy.management.GetCount(output_enriched)
        print("   output_enriched has {} records".format(Count2[0]))

        AssignDomains(in_table=output_enriched)

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
        print(f"USFS script took: {int(hours)}h, {int(minutes)}m, {seconds}s to complete")
