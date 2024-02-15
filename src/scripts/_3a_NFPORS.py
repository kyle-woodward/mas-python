"""
# Description: Converts the U.S. Department of Interior's National 
#              Fire Plan Operations and Reporting System (NFPORS) dataset 
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
from ._3_enrichments_pts import enrich_points
from ._3_enrichments_polygon import enrich_polygons
from ._3_keep_fields import KeepFields
from .utils import init_gdb, delete_scratch_files

workspace, scratch_workspace = init_gdb()

def Model_NFPORS_poly(
    input_original_polys,
    output_polys_enriched,
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
        overwriteOutput=True
    ):
        # define intermediary objects in scratch
        nfpors_DOI = os.path.join(scratch_workspace, "nfpors_DOI")
        nfpors_DOI_after_1995 = os.path.join(scratch_workspace, "nfpors_DOI_after_1995")
        nfpors_DOI_CA = os.path.join(scratch_workspace, "nfpors_DOI_CA")
        output_polys_standardized = os.path.join(scratch_workspace, 'nfpors_fuels_treatments_polys_standardized')

        ### BEGIN TOOL CHAIN
        ### BEGIN POLYGONS WORKFLOW (points workflow below)

        print("Performing Polygons Standardization")
        print("   step 1/7 select by DOI agency (BIA, FWS, NPS)")
        select_service = arcpy.analysis.Select(
            in_features=input_original_polys,
            out_feature_class=nfpors_DOI,
            where_clause="agency = 'BIA' Or agency = 'FWS' Or agency = 'NPS'",
        )

        print("   step 2/7 select after 1995")
        select_date_after_1995 = arcpy.analysis.Select(
            in_features=select_service,
            out_feature_class=nfpors_DOI_after_1995,
            where_clause="act_comp_dt >= timestamp '1995-01-01 00:00:00' Or act_comp_dt IS NULL",
        )

        print("   step 3/7 select CA")
        select_CA = arcpy.analysis.Select(
            in_features=select_date_after_1995,
            out_feature_class=nfpors_DOI_CA,
            where_clause="st_abbr = 'CA'",
        )

        ## NOTE: This may need to be enabled depending on how the source pulls
        # print("   step 3a/7 define projection")
        # define_projection_1 = arcpy.management.DefineProjection(
        #     in_dataset=select_CA,
        #     coor_system=3857 # "WGS_1984_Web_Mercator_Auxiliary_Sphere"
        # )
        
        print("   step 4/7 repair geometry")
        repair_geom_1 = arcpy.management.RepairGeometry(
            in_features=select_CA, 
            delete_null="KEEP_NULL", 
            validation_method="ESRI"
        )

        print("   step 5/7 rename and add fields")
        alterfield_1 = arcpy.management.AlterField(
            in_table=repair_geom_1,
            field="agency",
            new_field_name="agency_",
            new_field_alias="",
            field_type="TEXT",
            field_length=55,
            field_is_nullable="NULLABLE",
            clear_field_alias="CLEAR_ALIAS",
        )

        addfields_1 = AddFields(Input_Table=alterfield_1)

        print("   step 6/7 import attributes")
        calc_field_1 = arcpy.management.CalculateField(
            in_table=addfields_1,
            field="PROJECTID_USER",
            expression='"NFPORS"+!trt_id!',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_2 = arcpy.management.CalculateField(
            in_table=calc_field_1,
            field="AGENCY",
            expression='"DOI"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # TODO Add Data Stewards & Contacts

        calc_field_3 = arcpy.management.CalculateField(
            in_table=calc_field_2,
            field="ADMINISTERING_ORG",
            expression="!agency_!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_4 = arcpy.management.CalculateField(
            in_table=calc_field_3,
            field="IMPLEMENTING_ORG",
            expression="!agency_!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_5 = arcpy.management.CalculateField(
            in_table=calc_field_4,
            field="ACTIVITY_NAME",
            expression="!trt_nm!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_7 = arcpy.management.CalculateField(
            in_table=calc_field_5,
            field="ACTIVITY_UOM",
            expression='"AC"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_8 = arcpy.management.CalculateField(
            in_table=calc_field_7,
            field="ACTIVITY_QUANTITY",
            expression="ifelse(!act_acc_ac!, !gis_acres!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(Actual, GIS):
                            if Actual == 0:
                                return GIS
                            else:
                                return Actual""",
            field_type="DOUBLE",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_9 = arcpy.management.CalculateField(
            in_table=calc_field_8,
            field="ACTIVITY_START",
            expression="!modifiedon!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_10 = arcpy.management.CalculateField(
            in_table=calc_field_9,
            field="ACTIVITY_END",
            expression="ifelse(!act_comp_dt!, !modifiedon!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(DateComp, DatePl):
                            if DateComp != None:
                                return DateComp
                            else:
                                return DatePl""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_11 = arcpy.management.CalculateField(
            in_table=calc_field_10,
            field="ACTIVITY_STATUS",
            expression='"COMPLETE"',
            expression_type="PYTHON3",
            code_block="""def ifelse(Status):
                            if Status == \"Accomplished\":
                                return \"Complete\"
                            elif Status == \"Initiated\":
                                return \"Active\"
                            else:
                                return Status""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_12 = arcpy.management.CalculateField(
            in_table=calc_field_11,
            field="Source",
            expression='"nfpors_haz_fuels_treatments_reduction"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_field_13 = arcpy.management.CalculateField(
            in_table=calc_field_12,
            field="Crosswalk",
            expression="!type_name!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="ENFORCE_DOMAINS",
        )

        keepfields_1 = KeepFields(calc_field_13)

        print(f"   Standardization Complete")
        arcpy.management.CopyFeatures(
            in_features=keepfields_1,
            out_feature_class=output_polys_standardized
        )

        Count1 = arcpy.management.GetCount(output_polys_standardized)
        print("     standardized has {} records".format(Count1[0]))

        enrich_polygons(
            enrich_in=output_polys_standardized,
            enrich_out=output_polys_enriched
        )

        Count2 = arcpy.management.GetCount(output_polys_enriched)
        print("     enriched has {} records".format(Count2[0]))

        print("   step 7/7 add project user ID")
        calc_field_14 = arcpy.management.CalculateField(
            in_table=output_polys_enriched,
            field="TRMTID_USER",
            expression="str(!PROJECTID_USER!)[-7:]+'-'+str(!IN_WUI!)[:3]+'-'+str(!PRIMARY_OWNERSHIP_GROUP!)[:1]+'-'+str(!COUNTY!)[:8]+'-'+str(!PRIMARY_OBJECTIVE!)[:12]",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        AssignDomains(in_table=output_polys_enriched)
        print(f"   Polygon Enrichment Complete")

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
        print(f"NFPORS polygon script took: {int(hours)}h, {int(minutes)}m, {seconds}s to complete")

def Model_NFPORS_point(
    input_original_pts_BIA,
    input_original_pts_FWS,
    output_pts_enriched,
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
        overwriteOutput=True
    ):
        # define intermediary objects in scratch
        BIA_pts_CA = os.path.join(scratch_workspace, "BIA_pts_CA")
        FWS_pts_CA = os.path.join(scratch_workspace, "FWS_pts_CA")
        output_pts_standardized = os.path.join(scratch_workspace, 'nfpors_fuels_treatments_pts_standardized')
        
        ### BEGIN POINTS WORKFLOW

        print("Points Standardization")
        print("   step 1/6 select BIA points in CA")
        arcpy.analysis.Select(
            in_features=input_original_pts_BIA,
            out_feature_class=BIA_pts_CA,
            where_clause="statename = 'California'",
        )
        Count3 = arcpy.management.GetCount(BIA_pts_CA)
        print("     BIA Selected points has {} records".format(Count3[0]))

        print("   step 2/6 select FWS points in CA")
        arcpy.analysis.Select(
            in_features=input_original_pts_FWS,
            out_feature_class=FWS_pts_CA,
            where_clause="statename = 'California'",
        )
        
        Count4 = arcpy.management.GetCount(FWS_pts_CA)
        print("     FWS Selected points has {} records".format(Count4[0]))

        print("   step 3/6 combine points layers")
        append_1 = arcpy.management.Append(
            inputs=BIA_pts_CA,
            target=FWS_pts_CA,
            schema_type="TEST",
            field_mapping="",
            subtype="",
            expression="",
        )
        
        Count5 = arcpy.management.GetCount(append_1)
        print("     appended points has {} records".format(Count5[0]))

        print("   step 4/6 rename and add fields")
        alterfield_1 = arcpy.management.AlterField(
            in_table=append_1,
            field="source",
            new_field_name="source_",
            new_field_alias="",
            field_type="TEXT",
            field_is_nullable="NULLABLE",
            clear_field_alias="CLEAR_ALIAS",
        )

        alterfield_2 = arcpy.management.AlterField(
            in_table=alterfield_1,
            field="projectid",
            new_field_name="project_id",
            new_field_alias="",
            field_type="TEXT",
            field_is_nullable="NULLABLE",
            clear_field_alias="CLEAR_ALIAS",
        )

        alterfield_3 = arcpy.management.AlterField(
            in_table=alterfield_2,
            field="latitude",
            new_field_name="latitude_",
            new_field_alias="",
            field_type="DOUBLE",
            field_is_nullable="NULLABLE",
            clear_field_alias="CLEAR_ALIAS",
        )

        alterfield_4 = arcpy.management.AlterField(
            in_table=alterfield_3,
            field="longitude",
            new_field_name="longitude_",
            new_field_alias="",
            field_type="DOUBLE",
            field_is_nullable="NULLABLE",
            clear_field_alias="CLEAR_ALIAS",
        )

        addfields_2 = AddFields(Input_Table=alterfield_4)

        print("   step 5/6 import attributes")
        calc_pt_field_1 = arcpy.management.CalculateField(
            in_table=addfields_2,
            field="PROJECTID_USER",
            expression='"NFPORS"+str(!project_id!)',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_pt_field_2 = arcpy.management.CalculateField(
            in_table=calc_pt_field_1,
            field="AGENCY",
            expression='"DOI"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # TODO Calculate Data Stewards & Contacts
        
        calc_pt_field_3 = arcpy.management.CalculateField(
            in_table=calc_pt_field_2,
            field="ADMINISTERING_ORG",
            expression="!agencyname!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_pt_field_4 = arcpy.management.CalculateField(
            in_table=calc_pt_field_3,
            field="IMPLEMENTING_ORG",
            expression="!agencyname!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_pt_field_5 = arcpy.management.CalculateField(
            in_table=calc_pt_field_4,
            field="IN_WUI",
            expression="ifelse(!iswui!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(WUI):
                            if WUI == \"Y\":
                                return \"WUI_USER_DEFINED\"
                            elif WUI == \"N\":
                                return \"NON-WUI_USER_DEFINED\"
                            else:
                                return WUI""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_pt_field_6 = arcpy.management.CalculateField(
            in_table=calc_pt_field_5,
            field="ACTIVITY_NAME",
            expression="!treatmentname!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_pt_field_7 = arcpy.management.CalculateField(
            in_table=calc_pt_field_6,
            field="ACTIVITY_UOM",
            expression="!unitofmeas!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_pt_field_8 = arcpy.management.CalculateField(
            in_table=calc_pt_field_7,
            field="ACTIVITY_QUANTITY",
            expression="ifelse(!totalaccomplishment!, !plannedaccomplishment!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(Actual, Planned):
                            if Actual == 0:
                                return Planned
                            else:
                                return Actual""",
            field_type="DOUBLE",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_pt_field_9 = arcpy.management.CalculateField(
            in_table=calc_pt_field_8,
            field="TREATMENT_AREA",
            expression="ifelse(!ACTIVITY_UOM!,!ACTIVITY_QUANTITY!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(Units, Quant):
                            if Units == \"AC\":
                                return Quant""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_pt_field_10 = arcpy.management.CalculateField(
            in_table=calc_pt_field_9,
            field="ACTIVITY_START",
            expression="ifelse(!actualinitiationdate!, !plannedinitiationdate!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(Initiated, Planned):
                            if Initiated >= datetime.datetime(1901, 1, 1):
                                return Initiated
                            else:
                                return Planned""",
            field_type="TEXT",
            enforce_domains="ENFORCE_DOMAINS",
        )

        calc_pt_field_11 = arcpy.management.CalculateField(
            in_table=calc_pt_field_10,
            field="ACTIVITY_END",
            expression="ifelse(!actualcompletiondate!, !plannedinitiationdate!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(DateComp, DatePl):
                            if DateComp >= datetime.datetime(1901, 1, 1):
                                return DateComp
                            else:
                                return DatePl""",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_pt_field_12 = arcpy.management.CalculateField(
            in_table=calc_pt_field_11,
            field="ACTIVITY_STATUS",
            expression='"Active"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_pt_field_13 = arcpy.management.CalculateField(
            in_table=calc_pt_field_12,
            field="Source",
            expression='"nfpors_current_fy_treatments"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_pt_field_14 = arcpy.management.CalculateField(
            in_table=calc_pt_field_13,
            field="Crosswalk",
            expression="!typename!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        calc_pt_field_15 = arcpy.management.CalculateField(
            in_table=calc_pt_field_14,
            field="TRMT_GEOM",
            expression='"POINT"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="ENFORCE_DOMAINS",
        )

        arcpy.management.CopyFeatures(
            in_features=calc_pt_field_15,
            out_feature_class=output_pts_standardized
        )

        keepfields_2 = KeepFields(output_pts_standardized)

        print(f"Standardization Complete")
        Count6 = arcpy.management.GetCount(keepfields_2)
        print("     standardized points has {} records".format(Count6[0]))

        enrich_points(
            enrich_pts_in=keepfields_2,
            enrich_pts_out=output_pts_enriched
        )

        Count6 = arcpy.management.GetCount(output_pts_enriched)
        print("     enriched points has {} records".format(Count6[0]))

        print("   step 6/6 add project user ID")
        calc_pt_field_16 = arcpy.management.CalculateField(
            in_table=output_pts_enriched,
            field="TRMTID_USER",
            expression="str(!PROJECTID_USER![-7:])+'-'+str(!IN_WUI![:3])+'-'+str(!PRIMARY_OWNERSHIP_GROUP!)[:1]+'-'+str(!COUNTY!)[:8]+'-'+str(!PRIMARY_OBJECTIVE!)[:12]",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        AssignDomains(in_table=calc_pt_field_16)
        print("Point Enrichment Complete")

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
        print(f"NFPORS point script took: {int(hours)}h, {int(minutes)}m, {seconds}s to complete")


