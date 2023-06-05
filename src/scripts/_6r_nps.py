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

# def rFlatFuelsTreatmentDraft(nps_flat_fuels_enriched_20221102="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\d_Enriched\\nps_flat_fuels_enriched_20221102", usfs_haz_fuels_treatments_standardized_20220713_2_="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\c_Standardized\\nps_flat_fuels_standardized_20221102"):  # 6r NPS 20221123
def rFlatFuelsTreatmentDraft(input_fc, output_standardized,output_enriched):
    start = time.time()
    print(f'Start Time {time.ctime()}')
    arcpy.env.overwriteOutput = True

    # TODO: download from feature service upon run-time
    # in meantime have access to copy of the file from Dropbox 1/3/23
    nps_flat_fuels_20021102 = os.path.join(original_gdb, 'a_Originals', 'nps_flat_fuels_20021102')
    California = os.path.join(workspace,'b_Reference','California')

    # define intermediary scratch files 
    FLAT_FUELSTREATMENT_PAST_select = os.path.join(scratch_workspace,'FLAT_FUELSTREATMENT_PAST_select')
    FLAT_FUELSTREATMENT_PAS_clip = os.path.join(scratch_workspace,'FLAT_FUELSTREATMENT_PAS_clip')
    FLAT_FUELSTREATMENT_PAS_disso = os.path.join(scratch_workspace,'FLAT_FUELSTREATMENT_PAS_disso')
    Veg_Summarized_Polygons2 = os.path.join(scratch_workspace,'Veg_Summarized_Polygons2')

    print('Performing Standardization')
    # Process: Select (Select) (analysis)
    arcpy.analysis.Select(
        in_features=input_fc, 
        out_feature_class=FLAT_FUELSTREATMENT_PAST_select, 
        where_clause="ActualCompletionDate> timestamp '1995-01-01 00:00:00' Or ActualCompletionDate IS NULL"
        )

    # Process: Repair Geometry (Repair Geometry) (management)
    usfs_haz_fuels_treatments_reduction2_Select2_2_ = arcpy.management.RepairGeometry(
        in_features=FLAT_FUELSTREATMENT_PAST_select, 
        delete_null="KEEP_NULL", 
        validation_method="ESRI"
        )

    # Process: Pairwise Clip (Pairwise Clip) (analysis)
    arcpy.analysis.PairwiseClip(
        in_features=usfs_haz_fuels_treatments_reduction2_Select2_2_, 
        clip_features=California, 
        out_feature_class=FLAT_FUELSTREATMENT_PAS_clip, 
        cluster_tolerance=""
        )

    # Process: Pairwise Dissolve (Pairwise Dissolve) (analysis)
    arcpy.analysis.PairwiseDissolve(
        in_features=FLAT_FUELSTREATMENT_PAS_clip, 
        out_feature_class=FLAT_FUELSTREATMENT_PAS_disso, 
        dissolve_field=["TreatmentID", "LocalTreatmentID", "TreatmentIdentifierDatabase", 
                        "NWCGUnitID", "ProjectID", "TreatmentName", 
                        "TreatmentCategory", "TreatmentType", "ActualCompletionDate", 
                        "ActualCompletionFiscalYear", "TreatmentAcres", "GISAcres", 
                        "TreatmentStatus", "TreatmentNotes", "DateCurrent", 
                        "PublicDisplay", "DataAccess", "UnitCode", 
                        "UnitName", "GroupCode", "GroupName", 
                        "RegionCode", "CreateDate", "CreateUser", 
                        "LastEditDate", "LastEditor", "MapMethod", 
                        "MapSource", "SourceDate", 
                        "XYAccuracy", "Notes", "EventID"], 
        statistics_fields=[], 
        multi_part="MULTI_PART", 
        concatenation_separator=""
        )

    # Process: Alter Field (Alter Field) (management)
    FLAT_FUELSTREATMENT_PAS_disso_3_ = arcpy.management.AlterField(
        in_table=FLAT_FUELSTREATMENT_PAS_disso, 
        field="ProjectID", 
        new_field_name="PrjID", 
        new_field_alias="", 
        #field_type="TEXT", # otherwise get Error Cannot alter field types on populated tables.
        field_length=50, 
        field_is_nullable="NULLABLE", 
        clear_field_alias="DO_NOT_CLEAR"
        )

    # Process: 1b Add Fields (1b Add Fields) (PC414CWIMillionAcres)
    WFRTF_Template_4_ = AddFields(Input_Table=FLAT_FUELSTREATMENT_PAS_disso_3_)

    # Process: Calculate Project ID (Calculate Field) (management)
    Activity_SilvTSI_20220627_Se2_2_ = arcpy.management.CalculateField(
        in_table=WFRTF_Template_4_, 
        field="PROJECTID_USER", 
        expression="ifelse(!PrjID!, !TreatmentID!)", 
        expression_type="PYTHON3", 
        code_block="""def ifelse(Prj, Treat):
                        if Prj is not None:
                            return Prj
                        elif Prj is None:
                            return Treat""", 
        field_type="TEXT", 
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Agency (Calculate Field) (management)
    Updated_Input_Table_30_ = arcpy.management.CalculateField(
        in_table=Activity_SilvTSI_20220627_Se2_2_, 
        field="AGENCY", 
        expression="\"NPS\"", 
        expression_type="PYTHON3", 
        code_block="", 
        field_type="TEXT", 
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Data Steward (Calculate Field) (management)
    Updated_Input_Table = arcpy.management.CalculateField(
        in_table=Updated_Input_Table_30_, 
        field="ORG_ADMIN_p", 
        expression="!UnitName!", 
        expression_type="PYTHON3", 
        code_block="", 
        field_type="TEXT", 
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Project Contact (Calculate Field) (management)
    Updated_Input_Table_3_ = arcpy.management.CalculateField(
        in_table=Updated_Input_Table, 
        field="PROJECT_CONTACT", 
        expression="\"Kent van Wagtendonk\"", 
        expression_type="PYTHON3", 
        code_block="", 
        field_type="TEXT", 
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Project Email (Calculate Field) (management)
    Updated_Input_Table_5_ = arcpy.management.CalculateField(
        in_table=Updated_Input_Table_3_, 
        field="PROJECT_EMAIL", 
        expression="\"Kent_Van_Wagtendonk@nps.gov\"", 
        expression_type="PYTHON3", 
        code_block="", 
        field_type="TEXT", 
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Admin Org (Calculate Field) (management)
    Updated_Input_Table_31_ = arcpy.management.CalculateField(
        in_table=Updated_Input_Table_5_, 
        field="ADMINISTERING_ORG", 
        expression="!UnitCode!", 
        expression_type="PYTHON3", 
        code_block="", 
        field_type="TEXT", 
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Project Name (Calculate Field) (management)
    Updated_Input_Table_33_ = arcpy.management.CalculateField(
        in_table=Updated_Input_Table_31_, 
        field="PROJECT_NAME", 
        expression="!TreatmentName!", 
        expression_type="PYTHON3", 
        code_block="", 
        field_type="TEXT", 
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Fund Source (Calculate Field) (management)
    Updated_Input_Table_6_ = arcpy.management.CalculateField(
        in_table=Updated_Input_Table_33_, 
        field="PRIMARY_FUNDING_SOURCE", 
        expression="\"NPS\"", 
        expression_type="PYTHON3", 
        code_block="", 
        field_type="TEXT", 
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Fund Org (Calculate Field) (management)
    Updated_Input_Table_7_ = arcpy.management.CalculateField(
        in_table=Updated_Input_Table_6_, 
        field="PRIMARY_FUNDING_ORG", 
        expression="\"OTHER\"", 
        expression_type="PYTHON3", 
        code_block="", 
        field_type="TEXT", 
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Imp Org (Calculate Field) (management)
    Updated_Input_Table_32_ = arcpy.management.CalculateField(
        in_table=Updated_Input_Table_7_, 
        field="IMPLEMENTING_ORG", 
        expression="!UnitName!", 
        expression_type="PYTHON3", 
        code_block="", 
        field_type="TEXT", 
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Project Name (2) (Calculate Field) (management)
    Updated_Input_Table_14_ = arcpy.management.CalculateField(
        in_table=Updated_Input_Table_32_, 
        field="PROJECTNAME_", 
        expression="!TreatmentName!", 
        expression_type="PYTHON3", 
        code_block="", 
        field_type="TEXT", 
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Data Steward 2 (Calculate Field) (management)
    Updated_Input_Table_8_ = arcpy.management.CalculateField(
        in_table=Updated_Input_Table_14_, 
        field="ORG_ADMIN_t", 
        expression="None", 
        expression_type="PYTHON3", 
        code_block="", 
        field_type="TEXT", 
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Veg User Defined (Calculate Field) (management)
    Updated_Input_Table_9_ = arcpy.management.CalculateField(
        in_table=Updated_Input_Table_8_, 
        field="BVT_USERD", 
        expression="\"NO\"", 
        expression_type="PYTHON3", 
        code_block="", 
        field_type="TEXT", 
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Activity End Date (Calculate Field) (management)
    Updated_Input_Table_2_ = arcpy.management.CalculateField(
        in_table=Updated_Input_Table_9_, 
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
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Status (Calculate Field) (management)
    Updated_Input_Table_35_ = arcpy.management.CalculateField(
        in_table=Updated_Input_Table_2_, 
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
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Activity Quantity (3) (Calculate Field) (management)
    Activity_SilvTSI_20220627_Se2_6_ = arcpy.management.CalculateField(
        in_table=Updated_Input_Table_35_, 
        field="ACTIVITY_QUANTITY", 
        expression="!TreatmentAcres!", 
        expression_type="PYTHON3", 
        code_block="", 
        field_type="DOUBLE", 
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Activity UOM (3) (Calculate Field) (management)
    Activity_SilvTSI_20220627_Se2_5_ = arcpy.management.CalculateField(
        in_table=Activity_SilvTSI_20220627_Se2_6_, 
        field="ACTIVITY_UOM", 
        expression="\"AC\"", 
        expression_type="PYTHON3", 
        code_block="", 
        field_type="TEXT", 
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Admin Org2 (Calculate Field) (management)
    Updated_Input_Table_10_ = arcpy.management.CalculateField(
        in_table=Activity_SilvTSI_20220627_Se2_5_, 
        field="ADMIN_ORG_NAME", 
        expression="\"NPS\"", 
        expression_type="PYTHON3", 
        code_block="", 
        field_type="TEXT", 
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Implementation Org 2 (Calculate Field) (management)
    Updated_Input_Table_11_ = arcpy.management.CalculateField(
        in_table=Updated_Input_Table_10_, 
        field="IMPLEM_ORG_NAME", 
        expression="!UnitName!", 
        expression_type="PYTHON3", 
        code_block="", 
        field_type="TEXT", 
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Primary Fund Source (Calculate Field) (management)
    Updated_Input_Table_12_ = arcpy.management.CalculateField(
        in_table=Updated_Input_Table_11_, 
        field="PRIMARY_FUND_SRC_NAME", 
        expression="\"NPS\"", 
        expression_type="PYTHON3", 
        code_block="", 
        field_type="TEXT", 
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Fund Org 2 (Calculate Field) (management)
    Updated_Input_Table_13_ = arcpy.management.CalculateField(
        in_table=Updated_Input_Table_12_, 
        field="PRIMARY_FUND_ORG_NAME", 
        expression="\"NPS\"", 
        expression_type="PYTHON3", 
        code_block="", 
        field_type="TEXT", 
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Source (Calculate Field) (management)
    Updated_Input_Table_36_ = arcpy.management.CalculateField(
        in_table=Updated_Input_Table_13_, 
        field="Source", 
        expression="\"nps_flat_fuelstreatments\"", 
        expression_type="PYTHON3", 
        code_block="", 
        field_type="TEXT", 
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Year (Calculate Field) (management)
    Updated_Input_Table_37_ = arcpy.management.CalculateField(
        in_table=Updated_Input_Table_36_, 
        field="Year", 
        expression="Year($feature.ActualCompletionDate)", 
        expression_type="ARCADE", 
        code_block="", 
        field_type="TEXT", 
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Calculate Crosswalk (Calculate Field) (management)
    Updated_Input_Table_39_ = arcpy.management.CalculateField(
        in_table=Updated_Input_Table_37_, 
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
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: Select by Years (Select) (analysis)
    arcpy.analysis.Select(
        in_features=Updated_Input_Table_39_, 
        out_feature_class=output_standardized, 
        where_clause="Year >= 1995 And Year <= 2025"
        )
    print(f'Saving Output Standardized: {output_standardized}')
    # Process: Delete Field (Delete Field) (management)
    FLAT_FUELSTREATMENT_PAS_disso_2_ = KeepFields(output_standardized)
    
    print('Performing Enrichments')
    # Process: 7a Enrichments Polygon (2) (7a Enrichments Polygon) (PC414CWIMillionAcres)
    enrich_polygons(enrich_out=Veg_Summarized_Polygons2, enrich_in=FLAT_FUELSTREATMENT_PAS_disso_2_)

    print(f'Saving Output Enriched: {output_enriched}')
    # Process: Copy Features (Copy Features) (management)
    arcpy.management.CopyFeatures(
        in_features=Veg_Summarized_Polygons2, 
        out_feature_class=output_enriched, 
        config_keyword="", 
        spatial_grid_1=None, 
        spatial_grid_2=None, 
        spatial_grid_3=None)

    # Process: Calculate Treatment ID (Calculate Field) (management)
    Updated_Input_Table_4_ = arcpy.management.CalculateField(
        in_table=output_enriched, 
        field="TRMTID_USER", 
        expression="!PROJECTID_USER![:7]+'-'+(!COUNTY![:3])+'-'+(!PRIMARY_OWNERSHIP_GROUP![:4])+'-'+!IN_WUI![:3]+'-'+!PRIMARY_OBJECTIVE![:8]", 
        expression_type="PYTHON3", 
        code_block="", 
        field_type="TEXT", 
        enforce_domains="NO_ENFORCE_DOMAINS"
        )

    # Process: 2b Assign Domains (2b Assign Domains) (PC414CWIMillionAcres)
    WFR_TF_Template_2_ = AssignDomains(in_table=output_enriched)
    
    print('Deleting Scratch Files')
    delete_scratch_files(gdb = scratch_workspace, delete_fc = 'yes', delete_table = 'yes', delete_ds = 'yes')
 
    end = time.time()
    print(f'Time Elapsed: {(end-start)/60} minutes')
if __name__ == '__main__':
    runner(workspace,scratch_workspace,rFlatFuelsTreatmentDraft, '*argv[1:]')
    # # Global Environment settings
    # with arcpy.EnvManager(
    # extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""",  outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""", 
    # preserveGlobalIds=True, 
    # qualifiedFieldNames=False, 
    # scratchWorkspace=scratch_workspace, 
    # transferDomains=True, 
    # transferGDBAttributeProperties=True, 
    # workspace=workspace):
    #     rFlatFuelsTreatmentDraft(*argv[1:])
