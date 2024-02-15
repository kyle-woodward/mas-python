"""
# Description: Converts the U.S. Department of Interior, National 
#              Park Service's fuels treatments dataset 
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

workspace, scratch_workspace = init_gdb()

def NPS(input_fc, 
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

        California = os.path.join(workspace, "a_Reference", "California")

        # define intermediary scratch files
        nps_selection = os.path.join(scratch_workspace, "nps_selection")
        nps_clipped = os.path.join(scratch_workspace, "nps_clipped")
        nps_dissolved = os.path.join(scratch_workspace, "nps_dissolved")
        output_standardized = os.path.join(scratch_workspace,'nps_flat_fuels_standardized')
        nps_enriched_scratch = os.path.join(scratch_workspace, "nps_enriched_scratch")

        ### BEGIN TOOL CHAIN
        print("Performing Standardization")
        print("   step 1/7 select after 1995")
        select_date_after_1995 = arcpy.analysis.Select(
            in_features=input_fc,
            out_feature_class=nps_selection,
            where_clause="ActualCompletionDate> timestamp '1995-01-01 00:00:00' Or ActualCompletionDate IS NULL",
        )

        print("   step 2/7 repairing geometry")
        repair_geom_1 = arcpy.management.RepairGeometry(
            in_features=select_date_after_1995, 
            delete_null="KEEP_NULL", 
            validation_method="ESRI"
        )

        print("   step 3/7 clip features by CA")
        clip_CA = arcpy.analysis.PairwiseClip(
            in_features=repair_geom_1,
            clip_features=California,
            out_feature_class=nps_clipped,
            cluster_tolerance="",
        )

        print("   step 4/7 dissolve to implement multipart polygons")
        dissolve_1 = arcpy.analysis.PairwiseDissolve(
            in_features=clip_CA,
            out_feature_class=nps_dissolved,
            dissolve_field=[
                "TreatmentID",
                "LocalTreatmentID",
                "TreatmentIdentifierDatabase",
                "NWCGUnitID",
                "ProjectID",
                "TreatmentName",
                "TreatmentCategory",
                "TreatmentType",
                "ActualCompletionDate",
                "ActualCompletionFiscalYear",
                "TreatmentAcres",
                "GISAcres",
                "TreatmentStatus",
                "TreatmentNotes",
                "DateCurrent",
                "PublicDisplay",
                "DataAccess",
                "UnitCode",
                "UnitName",
                "GroupCode",
                "GroupName",
                "RegionCode",
                "CreateDate",
                "CreateUser",
                "LastEditDate",
                "LastEditor",
                "MapMethod",
                "MapSource",
                "SourceDate",
                "XYAccuracy",
                "Notes",
                "EventID",
            ],
            statistics_fields=[],
            multi_part="MULTI_PART",
            concatenation_separator="",
        )

        print("   step 5/7 rename and add fields")
        alterfield_1 = arcpy.management.AlterField(
            in_table=dissolve_1,
            field="ProjectID",
            new_field_name="PrjID",
            new_field_alias="",
            field_is_nullable="NULLABLE",
            clear_field_alias="DO_NOT_CLEAR",
        )

        addfields_1 = AddFields(Input_Table=alterfield_1)

        print("   step 6/7 import attributes")
        calc_field_1 = arcpy.management.CalculateField(
            in_table=addfields_1,
            field="PROJECTID_USER",
            expression="ifelse(!PrjID!, !TreatmentID!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(Prj, Treat):
                            if Prj is not None:
                                return Prj
                            elif Prj is None:
                                return Treat""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_2 = arcpy.management.CalculateField(
            in_table=calc_field_1,
            field="AGENCY",
            expression='"NPS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_3 = arcpy.management.CalculateField(
            in_table=calc_field_2,
            field="ORG_ADMIN_p",
            expression="!UnitName!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_4 = arcpy.management.CalculateField(
            in_table=calc_field_3,
            field="PROJECT_CONTACT",
            expression='"Kent van Wagtendonk"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_5 = arcpy.management.CalculateField(
            in_table=calc_field_4,
            field="PROJECT_EMAIL",
            expression='"Kent_Van_Wagtendonk@nps.gov"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_6 = arcpy.management.CalculateField(
            in_table=calc_field_5,
            field="ADMINISTERING_ORG",
            expression="!UnitCode!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_7 = arcpy.management.CalculateField(
            in_table=calc_field_6,
            field="PROJECT_NAME",
            expression="!TreatmentName!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_8 = arcpy.management.CalculateField(
            in_table=calc_field_7,
            field="PRIMARY_FUNDING_SOURCE",
            expression='"NPS"',
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
            expression="!UnitName!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_11 = arcpy.management.CalculateField(
            in_table=calc_field_10,
            field="PROJECTNAME_",
            expression="!TreatmentName!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_12 = arcpy.management.CalculateField(
            in_table=calc_field_11,
            field="ORG_ADMIN_t",
            expression="None",
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
            field="ACTIVITY_END",
            expression="ifelse(!ActualCompletionDate! , !ActualCompletionFiscalYear!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(ActualCompletionDate, ActualCompletionFiscalYear):
                            if ActualCompletionDate != None:
                                return ActualCompletionDate
                            elif ActualCompletionDate == None and ActualCompletionFiscalYear != None:
                                return datetime.datetime(ActualCompletionFiscalYear, 10, 1)
                            return None""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_15 = arcpy.management.CalculateField(
            in_table=calc_field_14,
            field="ACTIVITY_STATUS",
            expression="ifelse(!TreatmentStatus!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(stat):
                            if stat == \"Completed\":
                                return \"COMPLETE\"
                            elif stat == \"Initiated\":
                                return \"ACTIVE\"
                            return \"TBD\"""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_16 = arcpy.management.CalculateField(
            in_table=calc_field_15,
            field="ACTIVITY_QUANTITY",
            expression="!TreatmentAcres!",
            expression_type="PYTHON3",
            code_block="",
            field_type="DOUBLE",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_17 = arcpy.management.CalculateField(
            in_table=calc_field_16,
            field="ACTIVITY_UOM",
            expression='"AC"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_18 = arcpy.management.CalculateField(
            in_table=calc_field_17,
            field="ADMIN_ORG_NAME",
            expression='"NPS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_19 = arcpy.management.CalculateField(
            in_table=calc_field_18,
            field="IMPLEM_ORG_NAME",
            expression="!UnitName!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_20 = arcpy.management.CalculateField(
            in_table=calc_field_19,
            field="PRIMARY_FUND_SRC_NAME",
            expression='"NPS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_21 = arcpy.management.CalculateField(
            in_table=calc_field_20,
            field="PRIMARY_FUND_ORG_NAME",
            expression='"NPS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_22 = arcpy.management.CalculateField(
            in_table=calc_field_21,
            field="Source",
            expression='"nps_flat_fuelstreatments"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_23 = arcpy.management.CalculateField(
            in_table=calc_field_22,
            field="Year",
            expression="Year($feature.ActualCompletionDate)",
            expression_type="ARCADE",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_24 = arcpy.management.CalculateField(
            in_table=calc_field_23,
            field="Crosswalk",
            expression="Reclass(!TreatmentType!, !TreatmentCategory!)",
            expression_type="PYTHON3",
            code_block="""def Reclass(type, cat):
                            if type != None:
                                return type
                            elif type is None and cat == \"Fire\":
                                return \"Broadcast Burn\"
                            elif type is None and cat == \"Mechanical\":
                                return \"Hand Pile Burn\"""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        select_years = arcpy.analysis.Select(
            in_features=calc_field_24,
            out_feature_class=output_standardized,
            where_clause="Year >= %d And Year <= %d" % (startyear, endyear),
        )

        print("   Saving Output Standardized:")
        keepfields_1 = KeepFields(select_years)

        Count1 = arcpy.management.GetCount(keepfields_1)
        print("     standardized has {} records".format(Count1[0]))

        print("   Performing Enrichments")
        enrich_polygons(
            enrich_in=keepfields_1,
            enrich_out=nps_enriched_scratch
        )
        
        print("   Saving Output Enriched")
        Count2 = arcpy.management.GetCount(nps_enriched_scratch)
        print("     enriched has {} records".format(Count2[0]))

        arcpy.management.CopyFeatures(
            in_features=nps_enriched_scratch,
            out_feature_class=output_enriched
        )

        print("   step 7/7 adding treatment ID")
        calc_field_25 = arcpy.management.CalculateField(
            in_table=output_enriched,
            field="TRMTID_USER",
            expression="str(!PROJECTID_USER!)[:7]+'-'+str(!COUNTY!)[:3]+'-'+str(!PRIMARY_OWNERSHIP_GROUP!)[:4]+'-'+str(!IN_WUI!)[:3]+'-'+str(!PRIMARY_OBJECTIVE!)[:8]",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        AssignDomains(in_table=calc_field_25)

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
        print(f"NPS script took: {int(hours)}h, {int(minutes)}m, {seconds}s to complete")
