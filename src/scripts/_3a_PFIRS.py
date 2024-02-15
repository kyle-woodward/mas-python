"""
# Description: Converts the California Department of Environmental Quality's 
#              Prescribed Fire Information Reporting System (PFIRS) dataset 
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
from ._3_enrichments_pts import enrich_points
from ._3_keep_fields import KeepFields
from .utils import init_gdb, delete_scratch_files

workspace, scratch_workspace = init_gdb()


def PFIRS(
        input_fc, 
        output_enriched, 
        treat_poly, 
        delete_scratch=False
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
        input_Copy = os.path.join(scratch_workspace, "pfirs_input_Copy")
        output_standardized = os.path.join(scratch_workspace, "pfirs_standardized")
        
        ### BEGIN TOOL CHAIN
        print("Performing Standardization")
        print("   step 1/4 remove some agencies")
        copy_features_1 = arcpy.Select_analysis(
            in_features=input_fc,
            out_feature_class=input_Copy,
            where_clause="AGENCY <> 'Cal Fire' And AGENCY <> 'US Forest Service' And AGENCY <> 'US Fish and Wildlife Services' And AGENCY <> 'Bureau of Land Management' And AGENCY <> 'National Park Service'"
        )

        print("   step 3/4 rename and add fields")
        alterfield_1 = arcpy.management.AlterField(
            in_table=copy_features_1,
            field="AGENCY",
            new_field_name="AGENCY_",
            new_field_alias="",
            field_type="TEXT",
            field_is_nullable="NULLABLE",
            clear_field_alias="DO_NOT_CLEAR",
        )

        alterfield_2 = arcpy.management.AlterField(
            in_table=alterfield_1,
            field="COUNTY",
            new_field_name="COUNTY_",
            new_field_alias="",
            field_type="TEXT",
            field_is_nullable="NULLABLE",
            clear_field_alias="DO_NOT_CLEAR",
        )

        addfields_1 = AddFields(Input_Table=alterfield_2)

        print("   step 2/4 import attributes")
        calc_field_1 = arcpy.management.CalculateField(
            in_table=addfields_1,
            field="PROJECTID_USER",
            expression="'PFIRS'+'-'+str(!OBJECTID!)",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_2 = arcpy.management.CalculateField(
            in_table=calc_field_1,
            field="AGENCY",
            expression='"CARB"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_3 = arcpy.management.CalculateField(
            in_table=calc_field_2,
            field="ORG_ADMIN_p",
            expression='"CARB"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_4 = arcpy.management.CalculateField(
            in_table=calc_field_3,
            field="PROJECT_CONTACT",
            expression='"Jason Branz"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_5 = arcpy.management.CalculateField(
            in_table=calc_field_4,
            field="PROJECT_EMAIL",
            expression='"jason.branz@arb.ca.gov"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_6 = arcpy.management.CalculateField(
            in_table=calc_field_5,
            field="ADMINISTERING_ORG",
            expression='"CARB"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_7 = arcpy.management.CalculateField(
            in_table=calc_field_6,
            field="PROJECT_NAME",
            expression="!BURN_UNIT!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_8 = arcpy.management.CalculateField(
            in_table=calc_field_7,
            field="PRIMARY_FUNDING_SOURCE",
            expression='"LOCAL"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_9 = arcpy.management.CalculateField(
            in_table=calc_field_8,
            field="PRIMARY_FUNDING_ORG",
            expression='"OTHER"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_10 = arcpy.management.CalculateField(
            in_table=calc_field_9,
            field="IMPLEMENTING_ORG",
            expression="!AGENCY_!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_11 = arcpy.management.CalculateField(
            in_table=calc_field_10,
            field="TRMTID_USER",
            expression="'PFIRS'+'-'+str(!OBJECTID!)",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_12 = arcpy.management.CalculateField(
            in_table=calc_field_11,
            field="PROJECTNAME_",
            expression="None",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_13 = arcpy.management.CalculateField(
            in_table=calc_field_12,
            field="ORG_ADMIN_t",
            expression="None",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_14 = arcpy.management.CalculateField(
            in_table=calc_field_13,
            field="BVT_USERD",
            expression='"NO"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_15 = arcpy.management.CalculateField(
            in_table=calc_field_14,
            field="ACTIVITY_END",
            expression="!BURN_DATE!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_16 = arcpy.management.CalculateField(
            in_table=calc_field_15,
            field="ACTIVITY_STATUS",
            expression='"COMPLETE"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_17 = arcpy.management.CalculateField(
            in_table=calc_field_16,
            field="ACTIVITY_QUANTITY",
            expression="!ACRES_BURNED!",
            expression_type="PYTHON3",
            code_block="",
            field_type="DOUBLE",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_18 = arcpy.management.CalculateField(
            in_table=calc_field_17,
            field="ACTIVITY_UOM",
            expression='"AC"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_19 = arcpy.management.CalculateField(
            in_table=calc_field_18,
            field="ADMIN_ORG_NAME",
            expression='"CARB"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_20 = arcpy.management.CalculateField(
            in_table=calc_field_19,
            field="IMPLEM_ORG_NAME",
            expression="!AGENCY_!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_21 = arcpy.management.CalculateField(
            in_table=calc_field_20,
            field="PRIMARY_FUND_SRC_NAME",
            expression='"LOCAL"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_22 = arcpy.management.CalculateField(
            in_table=calc_field_21,
            field="PRIMARY_FUND_ORG_NAME",
            expression='"OTHER"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_23 = arcpy.management.CalculateField(
            in_table=calc_field_22,
            field="Source",
            expression='"PIFIRS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_24 = arcpy.management.CalculateField(
            in_table=calc_field_23,
            field="Crosswalk",
            expression="ifelse(!BURN_TYPE!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(Act):
                            if Act == \"Broadcast\":
                                return \"Broadcast Burn\"
                            elif Act == \"Unknown\":
                                return \"Broadcast Burn\"
                            elif Act == \"Hand Pile\":
                                return \"Hand Pile Burn\"
                            elif Act == \"Machine Pile\":
                                return \"Machine Pile Burn\"
                            elif Act == \"Landing Pile\":
                                return \"Landing Pile Burn\"
                            elif Act == \"Multiple Fuels\":
                                return \"Broadcast Burn\"
                            elif Act == \"UNK\":
                                return \"Broadcast Burn\"
                            else:
                                return Act""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        print(f"Saving Output Standardized")
        arcpy.management.CopyFeatures(
            in_features=calc_field_24,
            out_feature_class=output_standardized
        )

        Count1 = arcpy.management.GetCount(output_standardized)
        print("standardized has {} records".format(Count1[0]))

        print("   step 3/4 remove points that intersect burn polygons")
        select_rx_burns = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=treat_poly,
            selection_type="NEW_SELECTION",
            where_clause="ACTIVITY_DESCRIPTION = 'BROADCAST_BURN' Or ACTIVITY_DESCRIPTION = 'PILE_BURN'",
            invert_where_clause="",
        )

        ## NOTE: Search Distance can be modified
        select_by_location = arcpy.management.SelectLayerByLocation(
            in_layer=[output_standardized],
            overlap_type="INTERSECT",
            select_features=select_rx_burns,
            search_distance="",
            selection_type="NEW_SELECTION",
            invert_spatial_relationship="NOT_INVERT",
        )

        rows_deleted = arcpy.management.DeleteRows(
            in_rows=select_by_location)

        keepfields_1 = KeepFields(rows_deleted)

        Count2 = arcpy.management.GetCount(keepfields_1)
        print("     standardized subset has {} records".format(Count2[0]))

        print("Performing Enrichments")
        enrich_points(
            enrich_pts_in=keepfields_1,
            enrich_pts_out=output_enriched
        )

        print(f"Saving Output Enriched")
        Count3 = arcpy.management.GetCount(output_enriched)
        print("     enriched has {} records".format(Count3[0]))

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
        print(f"PFIRS script took: {int(hours)}h, {int(minutes)}m, {seconds}s to complete")

