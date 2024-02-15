"""
# Description: Converts the California Department of Natural Resources,
#              Wildlife Conservation Board's fuels treatments dataset 
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
from ._1_assign_domains import AssignDomains
from ._3_enrichments_polygon import enrich_polygons
from ._3_keep_fields import KeepFields
from .utils import init_gdb, delete_scratch_files

date_id = datetime.datetime.now().strftime("%Y-%m-%d").replace("-", "")

workspace, scratch_workspace = init_gdb()

def WCB(WCB_standardized, 
        WCB_OG, 
        delete_scratch=True
):
    with arcpy.EnvManager(
        workspace=workspace,
        scratchWorkspace=scratch_workspace,
        outputCoordinateSystem=arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"),  # WKID 3310
        cartographicCoordinateSystem=arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"),  # WKID 3310
        extent="xmin=-374900, ymin=-604500, xmax=540100, ymax=450000, spatial_reference='NAD 1983 California (Teale) Albers (Meters)'",
        preserveGlobalIds=True,
        qualifiedFieldNames=False,
        transferDomains=False,
        transferGDBAttributeProperties=False,
        overwriteOutput=True,
    ):

        # define intermediary objects in scratch
        WCB_CopyFeatures = os.path.join(scratch_workspace, "WCB_CopyFeatures")
        WCB_Dissolve = os.path.join(scratch_workspace, "WCB_Dissolve")
        WCB_enriched_scratch = os.path.join(scratch_workspace, "WCB_enriched_scratch")

        # workspace outputs
        WCB_enriched = os.path.join(workspace, "d_Enriched", f"WCB_enriched_{date_id}")

        print("Executing Step 1/34 : Select Layer by Attribute...")
        select_function = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=WCB_OG,
            where_clause="Function = 'Disposal/Sale' Or Function = 'Other (Plan, Study, Etc.)' Or Function = 'Infrastructure' Or Function = 'Lease' Or Function = 'Public Access' Or Function = 'Transfer of Control'",
            invert_where_clause="INVERT",
        )

        print("Executing Step 2/34 : Select Layer by Attribute...")
        select_date_after_1995 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=select_function,
            selection_type="SUBSET_SELECTION",
            where_clause="dtmBoardAp >= timestamp '1995-01-01 00:00:00'",
        )

        print("Executing Step 3/34 : Copy Features...")
        arcpy.management.CopyFeatures(
            in_features=select_date_after_1995, 
            out_feature_class=WCB_CopyFeatures
        )
        
        Count1 = arcpy.management.GetCount(WCB_CopyFeatures)
        print("selected features have {} records".format(Count1[0]))

        print("Executing Step 4/34 : Dissolve...")
        arcpy.management.Dissolve(
            in_features=WCB_CopyFeatures,
            out_feature_class=WCB_Dissolve,
            dissolve_field=[
                "County",
                "dtmBoardAp",
                "Function",
                "PrimGrante",
                "PrimPurp",
                "Program",
                "ProjectID",
                "ProjName",
                "TotalAcres",
                "Type",
                "WCBFunding",
            ],
        )

        Count2 = arcpy.management.GetCount(WCB_Dissolve)
        print("WCB_Dissolve has {} records".format(Count2[0]))

        print("Executing Step 5/34 : Repair Geometry...")
        repair_geom_1 = arcpy.management.RepairGeometry(
            in_features=WCB_Dissolve, 
            delete_null="KEEP_NULL"
        )

        print("Executing Step 6/34 : Alter Field...")
        alterfield_1 = arcpy.management.AlterField(
            in_table=repair_geom_1,
            field="ProjectID",
            new_field_name="ProjectID2",
        )

        print("Executing Step 7/34 : Alter Field...")
        alterfield_2 = arcpy.management.AlterField(
            in_table=alterfield_1, field="County", new_field_name="County_"
        )

        print("Executing Step 8/34 : Add Fields...")
        addfields_1 = AddFields(Input_Table=alterfield_2)

        print("Executing Step 9/34 : Calculate PROJECTID_USER...")
        calc_field_1 = arcpy.management.CalculateField(
            in_table=addfields_1, 
            field="PROJECTID_USER", 
            expression="!ProjectID2!"
        )

        print("Executing Step 10/34 : Calculate TRMTID_USER...")
        calc_field_2 = arcpy.management.CalculateField(
            in_table=calc_field_1,
            field="TRMTID_USER",
            expression="!PROJECTID_USER!",
        )  # +'-'+!PRIMARY_OWNERSHIP_GROUP![:4]")#+'-'+!IN_WUI![:3]")

        print("Executing Step 11/34 : Calculate AGENCY...")
        calc_field_3 = arcpy.management.CalculateField(
            in_table=calc_field_2, 
            field="AGENCY", 
            expression='"CNRA"'
        )

        print("Executing Step 12/34 : Calculate PROJECT_CONTACT...")
        calc_field_4 = arcpy.management.CalculateField(
            in_table=calc_field_3,
            field="PROJECT_CONTACT",
            expression='"Scott McFarlin"',
        )

        print("Executing Step 13/34 : Calculate PROJECT_EMAIL...")
        calc_field_5 = arcpy.management.CalculateField(
            in_table=calc_field_4,
            field="PROJECT_EMAIL",
            expression='"Scott.McFarlin@wildlife.ca.gov"',
        )

        print("Executing Step 14/34 : Calculate ADMINISTERING_ORG...")
        calc_field_6 = arcpy.management.CalculateField(
            in_table=calc_field_5, 
            field="ADMINISTERING_ORG", 
            expression='"WCB"'
        )

        print("Executing Step 15/34 : PROJECT_NAME...")
        calc_field_7 = arcpy.management.CalculateField(
            in_table=calc_field_6, 
            field="PROJECT_NAME", 
            expression="!ProjName!"
        )

        print("Executing Step 16/34 : Calculate PROJECT_START...")
        calc_field_8 = arcpy.management.CalculateField(
            in_table=calc_field_7,
            field="PROJECT_START",
            expression="!dtmBoardAp!",
        )

        print("Executing Step 17/34 : Calculate PRIMARY_OBJECTIVE...")
        calc_field_9 = arcpy.management.CalculateField(
            in_table=calc_field_8,
            field="PRIMARY_OBJECTIVE",
            expression="!PrimPurp!",
        )

        print("Executing Step 18/34 : Calculate SECONDARY_OBJECTIVE...")
        calc_field_10 = arcpy.management.CalculateField(
            in_table=calc_field_9, 
            field="SECONDARY_OBJECTIVE", 
            expression="!Type!"
        )

        print("Executing Step 19/34 : Calculate TERTIARY_OBJECTIVE...")
        calc_field_11 = arcpy.management.CalculateField(
            in_table=calc_field_10,
            field="TERTIARY_OBJECTIVE",
            expression="!Function!",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        print("Executing Step 20/34 : Calculate PRIMARY_FUNDING_SOURCE...")
        calc_field_12 = arcpy.management.CalculateField(
            in_table=calc_field_11,
            field="PRIMARY_FUNDING_SOURCE",
            expression="!Program!",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        print("Executing Step 21/34 : Calculate ACTIVITY_QUANTITY...")
        calc_field_13 = arcpy.management.CalculateField(
            in_table=calc_field_12,
            field="ACTIVITY_QUANTITY",
            expression="!TotalAcres!",
        )

        print("Executing Step 22/34 : Calculate ACTIVITY_UOM...")
        calc_field_14 = arcpy.management.CalculateField(
            in_table=calc_field_13, 
            field="ACTIVITY_UOM", 
            expression='"AC"'
        )

        print("Executing Step 23/34 : Calculate ACTIVITY_END...")
        calc_field_15 = arcpy.management.CalculateField(
            in_table=calc_field_14, 
            field="ACTIVITY_END", 
            expression="!dtmBoardAp!"
        )

        print("Executing Step 24/34 : Calculate ACTIVITY_STATUS...")
        calc_field_16 = arcpy.management.CalculateField(
            in_table=calc_field_15,
            field="ACTIVITY_STATUS",
            expression='"ACTIVE"',
        )

        print("Executing Step 25/34 : Calculate IMPLEM_ORG_NAME...")
        calc_field_17 = arcpy.management.CalculateField(
            in_table=calc_field_16,
            field="IMPLEM_ORG_NAME",
            expression="!PrimGrante!",
        )

        print("Executing Step 26/34 : Calculate Source...")
        calc_field_18 = arcpy.management.CalculateField(
            in_table=calc_field_17, 
            field="Source", 
            expression='"WCB"'
        )

        print("Executing Step 27/34 : Calculate Crosswalk...")
        calc_field_19 = arcpy.management.CalculateField(
            in_table=calc_field_18,
            field="Crosswalk",
            expression='!Function! + " " + !PrimPurp!',
        )

        print("Executing Step 28/34 : Calculate Year...")
        calc_field_20 = arcpy.management.CalculateField(
            in_table=calc_field_19,
            field="Year",
            expression="Year($feature.dtmBoardAp)",
            expression_type="ARCADE",
        )

        print("Executing Step 29/34 : Copy Features...")
        standardized_1 = arcpy.management.CopyFeatures(
            in_features=calc_field_20,
            out_feature_class=WCB_standardized
        )

        keepfields_1 = KeepFields(standardized_1)

        print("Executing Step 31/34 : Enrich Polygons...")
        enrich_polygons(
            enrich_in=keepfields_1,
            enrich_out=WCB_enriched_scratch
            )

        Count3 = arcpy.management.GetCount(WCB_enriched_scratch)
        print("enriched has {} records".format(Count3[0]))

        print("Executing Step 32/34 : Select Layer by Attribute...")
        select_2 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=WCB_enriched_scratch,
            where_clause="ACTIVITY_DESCRIPTION <> 'NOT_DEFINED'",
        )

        print("Executing Step 33/34 : Copy Features...")
        arcpy.management.CopyFeatures(
            in_features=select_2, 
            out_feature_class=WCB_enriched
        )

        print("Executing Step 34/34 : AssignDomains to enriched...")
        AssignDomains(in_table=WCB_enriched)

        if delete_scratch:
            print("Deleting Scratch Files")
            delete_scratch_files(
                gdb=scratch_workspace,
                delete_fc="yes",
                delete_table="yes",
                delete_ds="yes",
            )

        end1 = datetime.datetime.now()
        elapsed1 = end1 - start1
        hours, remainder1 = divmod(elapsed1.total_seconds(), 3600)
        minutes, remainder2 = divmod(remainder1, 60)
        seconds, remainder3 = divmod(remainder2, 1)
        print(f"WCB script took: {int(hours)}h, {int(minutes)}m, {seconds}s to complete")
