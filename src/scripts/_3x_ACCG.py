"""
# Description: Converts the Amador-Calaveras Conservation Group fuels treatments dataset 
#              into the Task Force standardized schema.  Dataset
#              is enriched with vegetation, ownership, county, WUI, 
#              Task Force Region, and year.            
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import datetime
start1 = datetime.datetime.now()
print(f"Start Time {start1}")

import os
import arcpy
from ._1_add_fields import AddFields
from ._3_enrichments_polygon import enrich_polygons
from ._3_keep_fields import KeepFields
from .utils import init_gdb, delete_scratch_files

workspace, scratch_workspace = init_gdb()

def ACCG(input_fc, 
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
    overwriteOutput = True,
    ):
        
        Crosswalk = os.path.join(workspace, "Crosswalk")
        California = os.path.join(workspace, "a_Reference", "California")

        # define intermediary objects in scratch
        ACCG_Project_table2 = os.path.join(scratch_workspace, "ACCG_Project_table2")
        ACCG_Project_Select = os.path.join(scratch_workspace, "ACCG_Project_Select")
        clip_1 = os.path.join(scratch_workspace, "ACCG_Project_clip")
        ACCG_Project_dissolved = os.path.join(scratch_workspace, "ACCG_Project_dissolved")
        output_standardized = os.path.join(scratch_workspace, "ACCG_Standardized")

        ### BEGIN TOOL CHAIN
        TableToTable_1 = arcpy.conversion.TableToTable(
            in_rows=input_fc,
            out_path=scratch_workspace,
            out_name="ACCG_Project_table",
            where_clause="SHAPE_Length = 0 Or SHAPE_Area = 0",
            field_mapping="",
            config_keyword="",
        )

        select_1 = arcpy.analysis.TableSelect(
            in_table=TableToTable_1,
            out_table=ACCG_Project_table2,
            where_clause="PROCLAIMED_FOREST_CODE = '0417' Or PROCLAIMED_FOREST_CODE = '0501' Or PROCLAIMED_FOREST_CODE = '0502' Or PROCLAIMED_FOREST_CODE = '0503' Or PROCLAIMED_FOREST_CODE = '0504' Or PROCLAIMED_FOREST_CODE = '0505' Or PROCLAIMED_FOREST_CODE = '0506' Or PROCLAIMED_FOREST_CODE = '0507' Or PROCLAIMED_FOREST_CODE = '0508' Or PROCLAIMED_FOREST_CODE = '0509' Or PROCLAIMED_FOREST_CODE = '0510' Or PROCLAIMED_FOREST_CODE = '0511' Or PROCLAIMED_FOREST_CODE = '0512' Or PROCLAIMED_FOREST_CODE = '0513' Or PROCLAIMED_FOREST_CODE = '0514' Or PROCLAIMED_FOREST_CODE = '0515' Or PROCLAIMED_FOREST_CODE = '0516' Or PROCLAIMED_FOREST_CODE = '0517' Or PROCLAIMED_FOREST_CODE = '0519' Or PROCLAIMED_FOREST_CODE = '0602' Or PROCLAIMED_FOREST_CODE = '0610'",
        )

        print("   step 3/8 Adding Fields...")
        addfields_1 = AddFields(
            Input_Table=select_1
        )

        calc_field_1 = arcpy.management.CalculateField(
            in_table=addfields_1,
            field="Prj_Admin",
            expression="!ORGANIZATI!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_2 = arcpy.management.CalculateField(
            in_table=calc_field_1,
            field="Prj_RptOrg",
            expression="!ORGANIZATI!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_3 = arcpy.management.CalculateField(
            in_table=calc_field_2,
            field="Prj_Name",
            expression="!NAME!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_4 = arcpy.management.CalculateField(
            in_table=calc_field_3,
            field="Prj_ID",
            expression="!OBJECTID!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_5 = arcpy.management.CalculateField(
            in_table=calc_field_4,
            field="TreatmentID",
            expression="!MAINTENANC!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_6 = arcpy.management.CalculateField(
            in_table=calc_field_5,
            field="UOM_",
            expression="!ACRES!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_7 = arcpy.management.CalculateField(
            in_table=calc_field_6,
            field="Act_Quant",
            expression="!ACRES!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_8 = arcpy.management.CalculateField(
            in_table=calc_field_7,
            field="Act_Code",
            expression='"NULL"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_9 = arcpy.management.CalculateField(
            in_table=calc_field_8,
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

        calc_field_10 = arcpy.management.CalculateField(
            in_table=calc_field_9,
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

        select_2 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=calc_field_10,
            selection_type="NEW_SELECTION",
            where_clause="Act_End IS NULL",
            invert_where_clause="",
        )

        calc_field_11 = arcpy.management.CalculateField(
            in_table=select_2,
            field="Act_End",
            expression="!DATE_PLANNED!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_12 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=calc_field_11,
            selection_type="CLEAR_SELECTION",
            where_clause="",
            invert_where_clause="",
        )

        calc_field_13 = arcpy.management.CalculateField(
            in_table=calc_field_12,
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

        calc_field_14 = arcpy.management.CalculateField(
            in_table=calc_field_13,
            field="Source",
            expression='"usfs_timber_harvests"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_15 = arcpy.management.CalculateField(
            in_table=calc_field_14,
            field="Year",
            expression="Year($feature.Act_End)",
            expression_type="ARCADE",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_16 = arcpy.management.CalculateField(
            in_table=calc_field_15,
            field="Year_txt",
            expression="!Year!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_17 = arcpy.management.CalculateField(
            in_table=calc_field_16,
            field="Crosswalk",
            expression="!ACTIVITY_NAME!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="ENFORCE_DOMAINS",
        )

        addjoin_1 = arcpy.management.AddJoin(
            in_layer_or_view=calc_field_17,
            in_field="Act_Code",
            join_table=Crosswalk,
            join_field="USFS_Activity_Code",
            join_type="KEEP_ALL",
            index_join_fields="NO_INDEX_JOIN_FIELDS",
        )

        calc_field_18 = arcpy.management.CalculateField(
            in_table=addjoin_1,
            field="usfs_harvests_table2.Prim_Obj",
            expression="!Fuels_Treatments_Piles_Crosswalk.Objective!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_19 = arcpy.management.CalculateField(
            in_table=calc_field_18,
            field="usfs_harvests_table2.Category",
            expression="!Fuels_Treatments_Piles_Crosswalk.Category!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_20 = arcpy.management.CalculateField(
            in_table=calc_field_19,
            field="usfs_harvests_table2.Act_Desc",
            expression="!Fuels_Treatments_Piles_Crosswalk.Activity!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        removejoin_1 = arcpy.management.RemoveJoin(
            in_layer_or_view=calc_field_20,
            join_name="Fuels_Treatments_Piles_Crosswalk",
        )

        keepfields_1 = KeepFields(removejoin_1)

        TableToTable_2 = arcpy.conversion.TableToTable(
            in_rows=keepfields_1,
            out_path=workspace,
            out_name="accg_copy",
            where_clause="",
            field_mapping="",
            config_keyword="",
        )

        #TODO Check that the input is correct
        select_date_after_1995 = arcpy.analysis.Select(
                in_features=input_fc,
                out_feature_class=ACCG_Project_Select,
                where_clause="DATE_COMPLETED > timestamp '1995-01-01 00:00:00' Or DATE_COMPLETED IS NULL",
        )

        repair_geom_1 = arcpy.management.RepairGeometry(
            in_features=select_date_after_1995,
            delete_null="DELETE_NULL",
            validation_method="ESRI",
        )

        clip_CA = arcpy.analysis.PairwiseClip(
            in_features=repair_geom_1,
            clip_features=California,
            out_feature_class=clip_1,
            cluster_tolerance="",
        )

        dissolve_1=arcpy.management.Dissolve(
            in_features=clip_CA,
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

        Count1 = arcpy.management.GetCount(dissolve_1)
        print("selected featues have {} records".format(Count1[0]))

        print("   step 3/13 Adding Fields...")
        addfields_2 = AddFields(Input_Table=dissolve_1)

        accg_calc_field_v1 = arcpy.management.CalculateField(
            in_table=addfields_2,
            field="Admin_Org",
            expression="!ORGANIZATI!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_21 = arcpy.management.CalculateField(
            in_table=accg_calc_field_v1,
            field="Prj_RptOrg",
            expression="!ORGANIZATI!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_22 = arcpy.management.CalculateField(
            in_table=calc_field_21,
            field="Imp_Org",
            expression="!ORGANIZATI!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_23 = arcpy.management.CalculateField(
            in_table=calc_field_22,
            field="Prj_Name",
            expression="!PROJECT!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_24 = arcpy.management.CalculateField(
            in_table=calc_field_23,
            field="Prj_ID",
            expression="!OBJECTID!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_25 = arcpy.management.CalculateField(
            in_table=calc_field_24,
            field="TreatID",
            expression="!MAINTENANC!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_26 = arcpy.management.CalculateField(
            in_table=calc_field_25,
            field="UOM_",
            expression='"ACRES"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_27 = arcpy.management.CalculateField(
            in_table=calc_field_26,
            field="Act_Quant",
            expression="!ACRES!",
            expression_type="PYTHON3",
            code_block="",
            field_type="DOUBLE",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_28 = arcpy.management.CalculateField(
            in_table=calc_field_27,
            field="Act_End",
            expression='!YEAR! + "-12-31"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        select_4 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=calc_field_28,
            selection_type="NEW_SELECTION",
            where_clause="YEAR IS NOT NULL",
            invert_where_clause="",
        )

        calc_field_29 = arcpy.management.CalculateField(
            in_table=select_4,
            field="Act_End",
            expression='!YEAR! + "-12-31"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        select_5 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=calc_field_29,
            selection_type="CLEAR_SELECTION",
            where_clause="",
            invert_where_clause="",
        )

        calc_field_30 = arcpy.management.CalculateField(
            in_table=select_5,
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

        calc_field_31 = arcpy.management.CalculateField(
            in_table=calc_field_30,
            field="Source",
            expression='"ACCG_Stakeholder"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_32 = arcpy.management.CalculateField(
            in_table=calc_field_31,
            field="Year",
            expression="Year($feature.Act_End)",
            expression_type="ARCADE",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_33 = arcpy.management.CalculateField(
            in_table=calc_field_32,
            field="Crosswalk",
            expression="!ACTIVITY!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_34 = arcpy.management.CalculateField(
            in_table=calc_field_33,
            field="Act_Code",
            expression='"NULL"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        standardized_1 = arcpy.management.CopyFeatures(
            in_features=calc_field_34,
            out_feature_class=output_standardized
        )

        Count2 = arcpy.management.GetCount(standardized_1)
        print("output_standardized has {} records".format(Count2[0]))

        keepfields_1 = KeepFields(standardized_1)

        print("Enriching Dataset")
        enrich_polygons(
            enrich_in=keepfields_1,
            enrich_out=output_enriched            
        )
        print(f'Saving Enriched Output')

        Count4 = arcpy.management.GetCount(output_enriched)
        print("   output_enriched has {} records".format(Count4[0]))


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
        print(f"ACCG script took: {int(hours)}h, {int(minutes)}m, {seconds}s to complete")

    return output_standardized

