"""
# Description: Converts the California Department of Conservation Ag dataset 
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
from scripts._1_add_fields import AddFields
from scripts._1_assign_domains import AssignDomains
from scripts._3_enrichments_polygon import enrich_polygons
from scripts.utils import init_gdb, delete_scratch_files

workspace, scratch_workspace = init_gdb()

def DOC6(DOC_Ag_Standardized, 
         DOC_Ag_enriched, 
         DOC_Ag_OG, 
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
        # scratch outputs
        DOC_Ag_OG_Dissolve = os.path.join(scratch_workspace, "DOC_Ag_OG_Dissolve")
        DOC_Summarized_Polygons = os.path.join(scratch_workspace, "DOC_Summarized_Polygons")

        ### BEGIN TOOL CHAIN
        print("step 1/24  dissolve...")
        arcpy.management.Dissolve(
            in_features=DOC_Ag_OG,
            out_feature_class=DOC_Ag_OG_Dissolve,
            dissolve_field=[
                "ACRES",
                "FUNDER1",
                "FUNDER2",
                "FUNDER3",
                "HOLDER",
                "PROJECT",
                "PROVIDER",
                "Grant_Nm",
                "ClosingDat",
            ],
        )

        print("step 2/24  repair geometry...")
        repair_geom_1 = arcpy.management.RepairGeometry(in_features=DOC_Ag_OG_Dissolve)

        print("step 3/24  add fields...")
        alterfield_1 = AddFields(Input_Table=repair_geom_1)

        print("step 4/24  calculate field...")
        calc_field_1 = arcpy.management.CalculateField(
            in_table=alterfield_1, 
            field="PROJECTID_USER", 
            expression="!Grant_Nm!"
        )

        print("step 5/24  calculate field...")
        calc_field_2 = arcpy.management.CalculateField(
            in_table=calc_field_1, 
            field="AGENCY", 
            expression='"CNRA"'
        )

        print("step 6/24  calculate field...")
        calc_field_3 = arcpy.management.CalculateField(
            in_table=calc_field_2, 
            field="ADMINISTERING_ORG", 
            expression='"DOC"'
        )

        print("step 7/24  calculate field...")
        calc_field_4 = arcpy.management.CalculateField(
            in_table=calc_field_3, 
            field="PROJECT_NAME", 
            expression="!PROJECT!"
        )

        print("step 8/24  calculate field...")
        calc_field_5 = arcpy.management.CalculateField(
            in_table=calc_field_4, 
            field="IMPLEMENTING_ORG", 
            expression="!HOLDER!"
        )

        print("step 9/24  calculate field...")
        calc_field_6 = arcpy.management.CalculateField(
            in_table=calc_field_5,
            field="TRMTID_USER",
            expression="!Grant_Nm! + '-' + !PROJECT![:12]",
        )  # +'-'+!PRIMARY_OWNERSHIP_GROUP![:11]+'-'+!IN_WUI![:3]")

        print("step 10/24  calculate field...")
        calc_field_7 = arcpy.management.CalculateField(
            in_table=calc_field_6, 
            field="BVT_USERD", 
            expression='"NO"'
        )

        print("step 11/24  calculate field...")
        calc_field_8 = arcpy.management.CalculateField(
            in_table=calc_field_7, 
            field="ACTIVITY_STATUS", 
            expression='"ACTIVE"'
        )

        print("step 12/24  calculate field...")
        calc_field_9 = arcpy.management.CalculateField(
            in_table=calc_field_8, 
            field="ACTIVITY_QUANTITY", 
            expression="!ACRES!"
        )

        print("step 13/24  calculate field...")
        calc_field_10 = arcpy.management.CalculateField(
            in_table=calc_field_9, 
            field="ACTIVITY_UOM", 
            expression='"AC"'
        )

        print("step 14/24  calculate field...")
        calc_field_11 = arcpy.management.CalculateField(
            in_table=calc_field_10, 
            field="ACTIVITY_END", 
            expression="!ClosingDat!"
        )

        print("step 15/24  calculate field...")
        calc_field_12 = arcpy.management.CalculateField(
            in_table=calc_field_11,
            field="PRIMARY_FUND_ORG_NAME",
            expression="!PROVIDER!",
        )

        print("step 16/24  calculate field...")
        calc_field_13 = arcpy.management.CalculateField(
            in_table=calc_field_12,
            field="PRIMARY_FUND_SRC_NAME",
            expression="!FUNDER1!",
        )

        print("step 17/24  calculate field...")
        calc_field_14 = arcpy.management.CalculateField(
            in_table=calc_field_13,
            field="SECONDARY_FUND_SRC_NAME",
            expression="!FUNDER2!",
        )

        print("step 18/24  calculate field...")
        calc_field_15 = arcpy.management.CalculateField(
            in_table=calc_field_14,
            field="TERTIARY_FUND_SRC_NAME",
            expression="!FUNDER3!",
        )

        print("step 19/24  calculate field...")
        calc_field_16 = arcpy.management.CalculateField(
            in_table=calc_field_15,
            field="Crosswalk",
            expression='"EASEMENT"',
        )

        print("step 20/24  calculate field...")
        calc_field_17 = arcpy.management.CalculateField(
            in_table=calc_field_16,
            field="Source",
            expression='"DOC_Ag_easements_Range2022"',
        )

        print("step 21/24  copy features...")
        arcpy.management.CopyFeatures(
            in_features=calc_field_17, 
            out_feature_class=DOC_Ag_Standardized
        )

        Count1 = arcpy.management.GetCount(DOC_Ag_Standardized)
        print("standardized has {} records".format(Count1[0]))

        print("step 22/24  enrich polygons...")
        enrich_polygons(
            enrich_in=DOC_Ag_Standardized,
            enrich_out=DOC_Summarized_Polygons
        )

        Count2 = arcpy.management.GetCount(DOC_Summarized_Polygons)
        print("enriched has {} records".format(Count2[0]))

        print("step 23/24  copy features...")
        arcpy.management.CopyFeatures(
            in_features=DOC_Summarized_Polygons, 
            out_feature_class=DOC_Ag_enriched
        )

        print("step 24/24 assign domains...")
        AssignDomains(in_table=DOC_Ag_enriched)

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
        print(f"DOC script took: {int(hours)}h, {int(minutes)}m, {seconds}s to complete")
