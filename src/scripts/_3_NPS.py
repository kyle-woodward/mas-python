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
import arcpy
from ._1b_add_fields import AddFields
from ._2b_assign_domains import AssignDomains
from ._7a_enrichments_polygon import enrich_polygons
from ._2k_keep_fields import KeepFields
# from sys import argv
from .utils import init_gdb, delete_scratch_files, runner
# import os
import time

original_gdb, workspace, scratch_workspace = init_gdb()


# def NPS(nps_flat_fuels_enriched_20221102="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\d_Enriched\\nps_flat_fuels_enriched_20221102", usfs_haz_fuels_treatments_standardized_20220713_2_="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\c_Standardized\\nps_flat_fuels_standardized_20221102"):  # 6r NPS 20221123
def NPS(input_fc, output_standardized, output_enriched):
    start = time.time()
    print(f"Start Time {time.ctime()}")
    with arcpy.EnvManager(
        outputCoordinateSystem= arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"), #WKID 3310
        cartographicCoordinateSystem=arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"), #WKID 3310
        extent="""450000, -374900, 540100, -604500,
                  DATUM["NAD 1983 California (Teale) Albers (Meters)"]""",
        preserveGlobalIds=True, 
        qualifiedFieldNames=False, 
        scratchWorkspace=scratch_workspace, 
        transferDomains=False, 
        transferGDBAttributeProperties=True, 
        workspace=workspace,
        overwriteOutput = True,
    ):

        # TODO: download from feature service upon run-time
        # in meantime have access to copy of the file from Dropbox 1/3/23
        California = os.path.join(workspace, "b_Reference", "California")

        # define intermediary scratch files
        nps_selection = os.path.join(scratch_workspace, "nps_selection")
        nps_clipped = os.path.join(scratch_workspace, "nps_clipped")
        nps_dissolved = os.path.join(scratch_workspace, "nps_dissolved")
        nps_enriched_scratch = os.path.join(scratch_workspace, "nps_enriched_scratch")

        print("Performing Standardization")
        # Process: Select (Select) (analysis)
        arcpy.analysis.Select(
            in_features=input_fc,
            out_feature_class=nps_selection,
            where_clause="ActualCompletionDate> timestamp '1995-01-01 00:00:00' Or ActualCompletionDate IS NULL",
        )

        # Process: Repair Geometry (Repair Geometry) (management)
        nps_repaired_geom = arcpy.management.RepairGeometry(
            in_features=nps_selection, delete_null="KEEP_NULL", validation_method="ESRI"
        )

        # Process: Pairwise Clip (Pairwise Clip) (analysis)
        arcpy.analysis.PairwiseClip(
            in_features=nps_repaired_geom,
            clip_features=California,
            out_feature_class=nps_clipped,
            cluster_tolerance="",
        )

        # Process: Pairwise Dissolve (Pairwise Dissolve) (analysis)
        arcpy.analysis.PairwiseDissolve(
            in_features=nps_clipped,
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

        # Process: Alter Field (Alter Field) (management)
        nps_altered_prjid = arcpy.management.AlterField(
            in_table=nps_dissolved,
            field="ProjectID",
            new_field_name="PrjID",
            new_field_alias="",
            # field_type="TEXT", # otherwise get Error Cannot alter field types on populated tables.
            field_length=50,
            field_is_nullable="NULLABLE",
            clear_field_alias="DO_NOT_CLEAR",
        )

        # Process: 1b Add Fields (1b Add Fields) (PC414CWIMillionAcres)
        nps_addfields = AddFields(Input_Table=nps_altered_prjid)

        # Process: Calculate Project ID (Calculate Field) (management)
        nps_calc_prjid = arcpy.management.CalculateField(
            in_table=nps_addfields,
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

        # Process: Calculate Agency (Calculate Field) (management)
        nps_calc_agency = arcpy.management.CalculateField(
            in_table=nps_calc_prjid,
            field="AGENCY",
            expression='"NPS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Data Steward (Calculate Field) (management)
        nps_calc_data_stew = arcpy.management.CalculateField(
            in_table=nps_calc_agency,
            field="ORG_ADMIN_p",
            expression="!UnitName!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Project Contact (Calculate Field) (management)
        nps_calc_contact = arcpy.management.CalculateField(
            in_table=nps_calc_data_stew,
            field="PROJECT_CONTACT",
            expression='"Kent van Wagtendonk"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Project Email (Calculate Field) (management)
        nps_calc_email = arcpy.management.CalculateField(
            in_table=nps_calc_contact,
            field="PROJECT_EMAIL",
            expression='"Kent_Van_Wagtendonk@nps.gov"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Admin Org (Calculate Field) (management)
        nps_calc_admin_org = arcpy.management.CalculateField(
            in_table=nps_calc_email,
            field="ADMINISTERING_ORG",
            expression="!UnitCode!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Project Name (Calculate Field) (management)
        nps_calc_pjtname = arcpy.management.CalculateField(
            in_table=nps_calc_admin_org,
            field="PROJECT_NAME",
            expression="!TreatmentName!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Fund Source (Calculate Field) (management)
        nps_calc_fund_src = arcpy.management.CalculateField(
            in_table=nps_calc_pjtname,
            field="PRIMARY_FUNDING_SOURCE",
            expression='"NPS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Fund Org (Calculate Field) (management)
        nps_calc_fund_org = arcpy.management.CalculateField(
            in_table=nps_calc_fund_src,
            field="PRIMARY_FUNDING_ORG",
            expression='"OTHER"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Imp Org (Calculate Field) (management)
        nps_calc_imp_org = arcpy.management.CalculateField(
            in_table=nps_calc_fund_org,
            field="IMPLEMENTING_ORG",
            expression="!UnitName!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Project Name (2) (Calculate Field) (management)
        nps_calc_pjtname_2 = arcpy.management.CalculateField(
            in_table=nps_calc_imp_org,
            field="PROJECTNAME_",
            expression="!TreatmentName!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Data Steward 2 (Calculate Field) (management)
        nps_calc_data_stew_2 = arcpy.management.CalculateField(
            in_table=nps_calc_pjtname_2,
            field="ORG_ADMIN_t",
            expression="None",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Veg User Defined (Calculate Field) (management)
        nps_calc_bvt_user = arcpy.management.CalculateField(
            in_table=nps_calc_data_stew_2,
            field="BVT_USERD",
            expression='"NO"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Activity End Date (Calculate Field) (management)
        nps_calc_act_end = arcpy.management.CalculateField(
            in_table=nps_calc_bvt_user,
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

        # Process: Calculate Status (Calculate Field) (management)
        nps_calc_status = arcpy.management.CalculateField(
            in_table=nps_calc_act_end,
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

        # Process: Calculate Activity Quantity (3) (Calculate Field) (management)
        nps_calc_act_qnt = arcpy.management.CalculateField(
            in_table=nps_calc_status,
            field="ACTIVITY_QUANTITY",
            expression="!TreatmentAcres!",
            expression_type="PYTHON3",
            code_block="",
            field_type="DOUBLE",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Activity UOM (3) (Calculate Field) (management)
        nps_calc_act_uom = arcpy.management.CalculateField(
            in_table=nps_calc_act_qnt,
            field="ACTIVITY_UOM",
            expression='"AC"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Admin Org2 (Calculate Field) (management)
        nps_calc_admin_org2 = arcpy.management.CalculateField(
            in_table=nps_calc_act_uom,
            field="ADMIN_ORG_NAME",
            expression='"NPS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Implementation Org 2 (Calculate Field) (management)
        nps_calc_imp_org2 = arcpy.management.CalculateField(
            in_table=nps_calc_admin_org2,
            field="IMPLEM_ORG_NAME",
            expression="!UnitName!",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Primary Fund Source (Calculate Field) (management)
        nps_calc_fund_src = arcpy.management.CalculateField(
            in_table=nps_calc_imp_org2,
            field="PRIMARY_FUND_SRC_NAME",
            expression='"NPS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Fund Org 2 (Calculate Field) (management)
        nps_calc_fund_org2 = arcpy.management.CalculateField(
            in_table=nps_calc_fund_src,
            field="PRIMARY_FUND_ORG_NAME",
            expression='"NPS"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Source (Calculate Field) (management)
        nps_calc_src = arcpy.management.CalculateField(
            in_table=nps_calc_fund_org2,
            field="Source",
            expression='"nps_flat_fuelstreatments"',
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Year (Calculate Field) (management)
        nps_calc_year = arcpy.management.CalculateField(
            in_table=nps_calc_src,
            field="Year",
            expression="Year($feature.ActualCompletionDate)",
            expression_type="ARCADE",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: Calculate Crosswalk (Calculate Field) (management)
        nps_calc_xwalk = arcpy.management.CalculateField(
            in_table=nps_calc_year,
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

        # Process: Select by Years (Select) (analysis)
        arcpy.analysis.Select(
            in_features=nps_calc_xwalk,
            out_feature_class=output_standardized,
            where_clause="Year >= 1995 And Year <= 2025",
        )
        print(f"Saving Output Standardized: {output_standardized}")
        # Process: Delete Field (Delete Field) (management)
        nps_standardized_keepfields = KeepFields(output_standardized)

        print("Performing Enrichments")
        # Process: 7a Enrichments Polygon (2) (7a Enrichments Polygon) (PC414CWIMillionAcres)
        enrich_polygons(
            enrich_out=nps_enriched_scratch, enrich_in=nps_standardized_keepfields
        )

        print(f"Saving Output Enriched: {output_enriched}")
        # Process: Copy Features (Copy Features) (management)
        arcpy.management.CopyFeatures(
            in_features=nps_enriched_scratch,
            out_feature_class=output_enriched,
            config_keyword="",
            spatial_grid_1=None,
            spatial_grid_2=None,
            spatial_grid_3=None,
        )

        # Process: Calculate Treatment ID (Calculate Field) (management)
        # nps_calc_trt_id =
        arcpy.management.CalculateField(
            in_table=output_enriched,
            field="TRMTID_USER",
            expression="!PROJECTID_USER![:7]+'-'+(!COUNTY![:3])+'-'+(!PRIMARY_OWNERSHIP_GROUP![:4])+'-'+!IN_WUI![:3]+'-'+!PRIMARY_OBJECTIVE![:8]",
            expression_type="PYTHON3",
            code_block="",
            field_type="TEXT",
            enforce_domains="NO_ENFORCE_DOMAINS",
        )

        # Process: 2b Assign Domains (2b Assign Domains) (PC414CWIMillionAcres)
        # nps_enriched_assign_domains =
        AssignDomains(in_table=output_enriched)

        print("Deleting Scratch Files")
        delete_scratch_files(
            gdb=scratch_workspace, delete_fc="yes", delete_table="yes", delete_ds="yes"
        )

        end = time.time()
        print(f"Time Elapsed: {(end-start)/60} minutes")


# if __name__ == "__main__":
#     runner(workspace, scratch_workspace, NPS, "*argv[1:]")
    # # Global Environment settings
    # with arcpy.EnvManager(
    # extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""",  outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""",
    # preserveGlobalIds=True,
    # qualifiedFieldNames=False,
    # scratchWorkspace=scratch_workspace,
    # transferDomains=True,
    # transferGDBAttributeProperties=True,
    # workspace=workspace):
    #     NPS(*argv[1:])
