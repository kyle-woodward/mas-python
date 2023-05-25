import arcpy
from ._1b_add_fields import AddFields2
from ._2b_assign_domains import AssignDomains
from ._7b_enrichments_pts import bEnrichmentsPoints
from ._2c_units_domain import Units
from ._7a_enrichments_polygon import aEnrichmentsPolygon1
from ._2k_keep_fields import KeepFields
from sys import argv
from .utils import init_gdb, delete_scratch_files
import os,time
original_gdb, workspace, scratch_workspace = init_gdb()

# def Model71(nfpors_fuels_treatments_pts_standardized_20221110="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\c_Standardized\\nfpors_fuels_treatments_pts_standardized_20221110", nfpors_current_fy_20221110="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\a_Originals\\nfpors_current_fy_20221110", nfpors_fuels_treatments_pts_enriched_20221110="C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\d_Enriched\\nfpors_fuels_treatments_pts_enriched_20221110"):  # 6g nfpors_haz_fuels_treatments
def Model71(input_original_polys,
input_original_pts_BIA, 
input_original_pts_FWS, 
output_original_polys, 
output_polys_standardized, 
output_polys_enriched, 
output_pts_standardized, 
output_pts_enriched
):
    start = time.time()
    print(f'Start Time {time.ctime()}')
    arcpy.env.overwriteOutput = True
    
    #Define paths to required inputs
    California = os.path.join(workspace,'b_Reference','California')
    # TODO: Find download source for this dataset, determine how to automate the download 
    # nfpors_fuels_treatments_20220906 = os.path.join(workspace,'a_Originals','nfpors_fuels_treatments_20220906')
    # these two datasets were downloaded from the following web service using Dan's download service tool
    # https://usgs.nfpors.gov/ArcGIS/rest/services/nfpors_WM/MapServer
    # NFPORS_Current_FY_Treatments_BIA = os.path.join(workspace,'a_Originals','NFPORSCurrentFYTreatmentsBIA')
    # NFPORS_Current_FY_Treatments_FWS = os.path.join(workspace,'a_Originals','NFPORSCurrentFYTreatmentsFWS')
    
    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")
    
    # Model Environment settings
    with arcpy.EnvManager(outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]"""):
        
        ### BEGIN POLYGON WORKFLOW
        
        print('Performing Polygons Standardization')    
        # Process: Select (2) (Select) (analysis)
        nfpors_select1 = os.path.join(scratch_workspace,'nfpors_select1')
        arcpy.analysis.Select(
            in_features=input_original_polys, # nfpors_fuels_treatments_20220906
            out_feature_class=nfpors_select1, 
            where_clause="agency = 'BIA' Or agency = 'FWS' Or agency = 'NPS'"
            )

        # Process: Select (Select) (analysis)
        nfpors_select2 = os.path.join(scratch_workspace,'nfpors_select2')
        arcpy.analysis.Select(
            in_features=nfpors_select1, 
            out_feature_class=nfpors_select2, 
            where_clause="act_comp_dt >= timestamp '1995-01-01 00:00:00' Or act_comp_dt IS NULL"
            )

        # Process: Select (5) (Select) (analysis)
        nfpors_select2_Select = os.path.join(scratch_workspace,'nfpors_select2_Select')
        arcpy.analysis.Select(
            in_features=nfpors_select2, 
            out_feature_class=nfpors_select2_Select, 
            where_clause="st_abbr = 'CA'"
            )

        # Process: Repair Geometry (Repair Geometry) (management)
        nfpors_select2_2_ = arcpy.management.RepairGeometry(
            in_features=nfpors_select2_Select, 
            delete_null="KEEP_NULL", 
            validation_method="ESRI"
            )

        # Process: Pairwise Clip (Pairwise Clip) (analysis)
        # nfpors_select2_clip = os.path.join(scratch_workspace,'nfpors_select2_clip')
        # with arcpy.EnvManager(extent="DEFAULT"):
        #     arcpy.analysis.PairwiseClip(
        #         in_features=nfpors_select2_2_, 
        #         clip_features=California, 
        #         out_feature_class=nfpors_select2_clip, 
        #         cluster_tolerance=""
        #         )

        # Process: Dissolve (3) (Dissolve) (management)
        # arcgisscripting.ExecuteError: ERROR 160327: A column was specified that does not exist. Failed to execute (Dissolve).
        # nfpors_select2_clip does not have DateComp and DateMod fields.. excluding them for now to keep debugging script
        # nfpors_select2_dissolve = os.path.join(scratch_workspace,'nfpors_select2_dissolve')
        # arcpy.management.Dissolve(
        #     in_features=nfpors_select2_clip, 
        #     out_feature_class=nfpors_select2_dissolve, 
        #     dissolve_field=["agency", "trt_id", "trt_nm", 
        #                     "type_name", "act_acc_ac", "trt_statnm", 
        #                     #"DateComp", "DateMod", # TODO: figure out whether these fields are supposed to be in the input 
        #                     "unit_id"], 
        #     statistics_fields=[], 
        #     multi_part="MULTI_PART", 
        #     unsplit_lines="DISSOLVE_LINES", 
        #     concatenation_separator=""
        #     )

        # Process: Define Projection (Define Projection) (management)
        ## Note: This may need to be enabled depending on how the source is pulled
        nfpors_select1_2_ = arcpy.management.DefineProjection(
            in_dataset=nfpors_select1, 
            coor_system="PROJCS[\"WGS_1984_Web_Mercator_Auxiliary_Sphere\",GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Mercator_Auxiliary_Sphere\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",0.0],PARAMETER[\"Standard_Parallel_1\",0.0],PARAMETER[\"Auxiliary_Sphere_Type\",0.0],UNIT[\"Meter\",1.0]]"
            )
        
        # AddFields2() has this AlterFields functionality option in it, 
        # but it doesn't seem like Carl would want pre-existing fields to always be altered, just specific ones...
        # Process: Alter agency Field (Alter Field) (management)
        nfpors_select2_clip_dissolve_6_ = arcpy.management.AlterField(
            in_table=nfpors_select2_2_, 
            field="agency", 
            new_field_name="agency_", 
            new_field_alias="", 
            field_type="TEXT", 
            field_length=55, 
            field_is_nullable="NULLABLE", 
            clear_field_alias="CLEAR_ALIAS"
            )

        # Process: 1b Add Fields (1b Add Fields) (PC414CWIMillionAcres)
        WFRTF_Template_4_ = AddFields2(Input_Table=nfpors_select2_clip_dissolve_6_)

        # Process: Calculate Projet ID (Calculate Field) (management)
        usfs_haz_fuels_treatments_reduction2_2_ = arcpy.management.CalculateField(
            in_table=WFRTF_Template_4_, 
            field="PROJECTID_USER", 
            expression="\"NFPORS\"+!trt_id!", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Agency (Calculate Field) (management)
        usfs_haz_fuels_treatments_reduction2_dissolve_3_ = arcpy.management.CalculateField(
            in_table=usfs_haz_fuels_treatments_reduction2_2_, 
            field="AGENCY", 
            expression="\"DOI\"", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Admin Org (Calculate Field) (management)
        Updated_Input_Table_3_ = arcpy.management.CalculateField(
            in_table=usfs_haz_fuels_treatments_reduction2_dissolve_3_, 
            field="ADMINISTERING_ORG", 
            expression="!agency_!", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Imp Org (Calculate Field) (management)
        Updated_Input_Table_4_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_3_, 
            field="IMPLEMENTING_ORG", 
            expression="!agency_!", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Geometry Attributes (2) (Calculate Geometry Attributes) (management)
        # nfpors_select2_clip_dissolve_5_ = arcpy.management.CalculateGeometryAttributes(
        #     in_features=Updated_Input_Table_4_, 
        #     geometry_property=[["LATITUDE", "INSIDE_Y"], 
        #                         ["LONGITUDE", "INSIDE_X"]], 
        #     length_unit="", 
        #     area_unit="", 
        #     coordinate_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", 
        #     coordinate_format="DD"
        #     )

        # Process: Calculate Treatment ID (2) (Calculate Field) (management)
        # usfs_haz_fuels_treatments_reduction2_6_ = arcpy.management.CalculateField(
        #     in_table=nfpors_select2_clip_dissolve_5_, 
        #     field="TRMTID_USER", 
        #     expression="str(!trt_id!)", 
        #     expression_type="PYTHON3", 
        #     code_block="", 
        #     field_type="TEXT", 
        #     enforce_domains="NO_ENFORCE_DOMAINS"
        #     )

        # Process: Calculate Treatment Name (Calculate Field) (management)
        # Updated_Input_Table_6_ = arcpy.management.CalculateField(
        #     in_table=usfs_haz_fuels_treatments_reduction2_6_, 
        #     field="TREATMENT_NAME", 
        #     expression="!trt_nm!", 
        #     expression_type="PYTHON3", 
        #     code_block="", 
        #     field_type="TEXT", 
        #     enforce_domains="NO_ENFORCE_DOMAINS"
        #     )

        # Process: Calculate Activity Name (Calculate Field) (management)
        Updated_Input_Table_6_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_4_, 
            field="ACTIVITY_NAME", 
            expression="!trt_nm!", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )
        
        # Process: Calculate Geometry Attributes (3) (Calculate Geometry Attributes) (management)
        nfpors_select2_dissolve_2_ = arcpy.management.CalculateGeometryAttributes(
            in_features=Updated_Input_Table_6_, 
            geometry_property=[["TREATMENT_AREA", "AREA"]], 
            length_unit="", 
            area_unit="ACRES", 
            coordinate_system="PROJCS[\"NAD_1983_California_Teale_Albers\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Albers\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",-4000000.0],PARAMETER[\"Central_Meridian\",-120.0],PARAMETER[\"Standard_Parallel_1\",34.0],PARAMETER[\"Standard_Parallel_2\",40.5],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]", 
            coordinate_format="SAME_AS_INPUT"
            )

        # Process: Calculate Activity UOM (Calculate Field) (management)
        Updated_Input_Table_9_ = arcpy.management.CalculateField(
            in_table=nfpors_select2_dissolve_2_, 
            field="ACTIVITY_UOM", 
            expression="\"AC\"", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Activity Quantity (Calculate Field) (management)
        Updated_Input_Table_10_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_9_, 
            field="ACTIVITY_QUANTITY", 
            expression="ifelse(!act_acc_ac!, !gis_acres!)", 
            expression_type="PYTHON3", 
            code_block="""def ifelse(Actual, GIS):
                            if Actual == 0:
                                return GIS
                            else:
                                return Actual""", 
            field_type="DOUBLE", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Activity Start Date (Calculate Field) (management)
        nfpors_select2_clip_dissolve_2_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_10_, 
            field="ACTIVITY_START", 
            expression="!modifiedon!", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Activity End Date (Calculate Field) (management)
        usfs_haz_fuels_treatments_reduction2_14_ = arcpy.management.CalculateField(
            in_table=nfpors_select2_clip_dissolve_2_, 
            field="ACTIVITY_END", 
            expression="ifelse(!act_comp_dt!, !modifiedon!)", 
            expression_type="PYTHON3", 
            code_block="""def ifelse(DateComp, DatePl):
                            if DateComp != None:
                                return DateComp
                            else:
                                return DatePl""", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Status (2) (Calculate Field) (management)
        usfs_haz_fuels_treatments_reduction2_16_ = arcpy.management.CalculateField(
            in_table=usfs_haz_fuels_treatments_reduction2_14_, 
            field="ACTIVITY_STATUS", 
            expression="\"COMPLETE\"", 
            expression_type="PYTHON3", 
            code_block="""def ifelse(Status):
                            if Status == \"Accomplished\":
                                return \"Complete\"
                            elif Status == \"Initiated\":
                                return \"Active\"
                            else:
                                return Status""", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Source (2) (Calculate Field) (management)
        Updated_Input_Table_13_ = arcpy.management.CalculateField(
            in_table=usfs_haz_fuels_treatments_reduction2_16_, 
            field="Source", 
            expression="\"nfpors_haz_fuels_treatments_reduction\"", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Crosswalk (Calculate Field) (management)
        Updated_Input_Table_8_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_13_, 
            field="Crosswalk", 
            expression="!type_name!", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="ENFORCE_DOMAINS"
            )

        # Process: Delete Field (Delete Field) (management)
        nfpors_select2_Select_2_ = KeepFields(Updated_Input_Table_8_)

        print(f'Saving Output Polys Standardized: {output_polys_standardized}')
        # Process: Copy Features (2) (Copy Features) (management)
        nfpors_fuels_treatments_standardized = output_polys_standardized
        arcpy.management.CopyFeatures(
            in_features=nfpors_select2_Select_2_, 
            out_feature_class=nfpors_fuels_treatments_standardized, 
            config_keyword="", 
            spatial_grid_1=None, 
            spatial_grid_2=None, 
            spatial_grid_3=None
            )

        # Process: 2b Assign Domains (2b Assign Domains) (PC414CWIMillionAcres)
        usfs_silviculture_reforestation_enriched_20220629_2_ = AssignDomains(in_table=nfpors_fuels_treatments_standardized)

        print(f'Performing Polygon Enrichments')
        # Process: 7a Enrichments Polygon (7a Enrichments Polygon) (PC414CWIMillionAcres)
        Veg_Summarized_Polygons2 = os.path.join(scratch_workspace,'Veg_Summarized_Polygons2')
        aEnrichmentsPolygon1(enrich_out=output_polys_enriched, enrich_in=usfs_silviculture_reforestation_enriched_20220629_2_)

        print(f'Saving Output Polys Enriched: {output_polys_enriched}')
        # Process: Copy Features (4) (Copy Features) (management)
        # nfpors_fuels_treatments_enriched = output_polys_enriched
        # arcpy.management.CopyFeatures(
        #     in_features=Veg_Summarized_Polygons2, 
        #     out_feature_class=nfpors_fuels_treatments_enriched, 
        #     config_keyword="", 
        #     spatial_grid_1=None, 
        #     spatial_grid_2=None, 
        #     spatial_grid_3=None
        #     )
        # Process: Calculate Treatment ID (2) (Calculate Field) (management)
        usfs_haz_fuels_treatments_reduction2_6_ = arcpy.management.CalculateField(
            in_table=output_polys_enriched, 
            field="TRMTID_USER", 
            expression="!PROJECTID_USER![-7:]+'-'+!IN_WUI![:3]+'-'+!PRIMARY_OWNERSHIP_GROUP![:1]+'-'+!COUNTY![:8]+'-'+!PRIMARY_OBJECTIVE![:12]", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )
        
        # Process: 2b Assign Domains (4) (2b Assign Domains) (PC414CWIMillionAcres)
        nfpors_fuels_treatments_enriched_20220906_2_ = AssignDomains(in_table=output_polys_enriched)

        # Process: Calculate Geometry Attributes (Calculate Geometry Attributes) (management)
        # nfpors_select2_dissolve_5_ = arcpy.management.CalculateGeometryAttributes(
        #     in_features=nfpors_select2_clip, 
        #     geometry_property=[["gis_acres", "AREA"]], 
        #     length_unit="", 
        #     area_unit="ACRES_US", 
        #     coordinate_system="PROJCS[\"NAD_1983_California_Teale_Albers\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Albers\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",-4000000.0],PARAMETER[\"Central_Meridian\",-120.0],PARAMETER[\"Standard_Parallel_1\",34.0],PARAMETER[\"Standard_Parallel_2\",40.5],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]", 
        #     coordinate_format="SAME_AS_INPUT"
        #     )

        ### BEGIN POINTS WORKFLOW
        
        print('Performing Points Standardization')
        # Process: Select (7) (Select) (analysis)
        # ERROR 000732: Input Features: Dataset Treatments-Source\NFPORS Current FY Treatments - BIA does not exist or is not supported. # Failed to execute (Select).
        # See TODO at beginning of Model71() def
        NFPORSCurrentFYTreatm_Select2 = os.path.join(scratch_workspace,'NFPORSCurrentFY_BIA_CAselect')
        arcpy.analysis.Select(
            in_features=input_original_pts_BIA, # NFPORS_Current_FY_Treatments_BIA
            out_feature_class=NFPORSCurrentFYTreatm_Select2, 
            where_clause="statename = 'California'"
            )

        # Process: Select (6) (Select) (analysis)
        # See TODO at beginning of Model71() def
        arcpy.analysis.Select(
            in_features=input_original_pts_FWS, # NFPORS_Current_FY_Treatments_FWS
            out_feature_class=output_original_polys, 
            where_clause="statename = 'California'"
            )

        # Process: Append (Append) (management)
        Updated_Target_Dataset = arcpy.management.Append(
            inputs=[NFPORSCurrentFYTreatm_Select2], 
            target=output_original_polys, 
            schema_type="TEST", 
            field_mapping="", 
            subtype="", 
            expression=""
            )

        # Process: Alter source Field (Alter Field) (management)
        nfpors_select2p_clip_2_ = arcpy.management.AlterField(
            in_table=Updated_Target_Dataset, 
            field="source", 
            new_field_name="source_", 
            new_field_alias="", 
            field_type="TEXT", 
            field_length=65, 
            field_is_nullable="NULLABLE", 
            clear_field_alias="CLEAR_ALIAS"
            )

        # Process: Alter projectid Field (Alter Field) (management)
        nfpors_select2p_clip_6_ = arcpy.management.AlterField(
            in_table=nfpors_select2p_clip_2_, 
            field="projectid", 
            new_field_name="project_id", 
            new_field_alias="", 
            field_type="TEXT", 
            # field_length=50, 
            field_is_nullable="NULLABLE", 
            clear_field_alias="CLEAR_ALIAS"
            )

        # Process: Alter latitude Field (Alter Field) (management)
        nfpors_select2p_clip_4_ = arcpy.management.AlterField(
            in_table=nfpors_select2p_clip_6_, 
            field="latitude", 
            new_field_name="latitude_", 
            new_field_alias="", 
            field_type="DOUBLE", 
            # field_length=8, 
            field_is_nullable="NULLABLE", 
            clear_field_alias="CLEAR_ALIAS"
            )

        # Process: Alter longitude Field (Alter Field) (management)
        nfpors_select2p_clip_5_ = arcpy.management.AlterField(
            in_table=nfpors_select2p_clip_4_, 
            field="longitude", 
            new_field_name="longitude_", 
            new_field_alias="", 
            field_type="DOUBLE", 
            # field_length=8, 
            field_is_nullable="NULLABLE", 
            clear_field_alias="CLEAR_ALIAS"
            )

        # Process: 1b Add Fields (2) (1b Add Fields) (PC414CWIMillionAcres)
        WFRTF_Template_2_ = AddFields2(Input_Table=nfpors_select2p_clip_5_)

        # Process: Calculate Projet ID (2) (Calculate Field) (management)
        usfs_haz_fuels_treatments_reduction2_3_ = arcpy.management.CalculateField(
            in_table=WFRTF_Template_2_, 
            field="PROJECTID_USER", 
            expression="\"NFPORS\"+str(!project_id!)", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Agency (2) (Calculate Field) (management)
        usfs_haz_fuels_treatments_reduction2_dissolve_4_ = arcpy.management.CalculateField(
            in_table=usfs_haz_fuels_treatments_reduction2_3_, 
            field="AGENCY", 
            expression="\"DOI\"", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Admin Org (2) (Calculate Field) (management)
        Updated_Input_Table_16_ = arcpy.management.CalculateField(
            in_table=usfs_haz_fuels_treatments_reduction2_dissolve_4_, 
            field="ADMINISTERING_ORG", 
            expression="!agencyname!", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Imp Org (2) (Calculate Field) (management)
        Updated_Input_Table_17_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_16_, 
            field="IMPLEMENTING_ORG", 
            expression="!agencyname!", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Geometry Attributes (4) (Calculate Geometry Attributes) (management)
        # nfpors_select2p_clip_7_ = arcpy.management.CalculateGeometryAttributes(
        #     in_features=Updated_Input_Table_17_, 
        #     geometry_property=[["LATITUDE", "POINT_Y"], 
        #                         ["LONGITUDE", "POINT_X"]], 
        #     length_unit="", 
        #     area_unit="", 
        #     coordinate_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", 
        #     coordinate_format="DD"
        #     )

        # Process: Calculate Treatment ID (3) (Calculate Field) (management)
        # usfs_haz_fuels_treatments_reduction2_5_ = arcpy.management.CalculateField(
        #     in_table=nfpors_select2p_clip_7_, 
        #     field="TRMTID_USER", 
        #     expression="str(!OBJECTID!)", 
        #     expression_type="PYTHON3", 
        #     code_block="", 
        #     field_type="TEXT", 
        #     enforce_domains="NO_ENFORCE_DOMAINS"
        #     )

        # Process: Calculate WUI (2) (Calculate Field) (management)
        Updated_Input_Table_2_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_17_, 
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
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Activity Name (2) (Calculate Field) (management)
        Updated_Input_Table_19_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_2_, 
            field="ACTIVITY_NAME", 
            expression="!treatmentname!", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Activity UOM (2) (Calculate Field) (management)
        Updated_Input_Table_21_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_19_, 
            field="ACTIVITY_UOM", 
            expression="!unitofmeas!", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: 2c Units Domain (2c Units Domain) (PC414CWIMillionAcres)
        StateParks_XY_enriched_20220708_StateParks_XY_enriched_20220708_3_ = Units(in_table=Updated_Input_Table_21_)

        # Process: Calculate Activity Quantity (2) (Calculate Field) (management)
        Updated_Input_Table_22_ = arcpy.management.CalculateField(
            in_table=StateParks_XY_enriched_20220708_StateParks_XY_enriched_20220708_3_, 
            field="ACTIVITY_QUANTITY", 
            expression="ifelse(!totalaccomplishment!, !plannedaccomplishment!)", 
            expression_type="PYTHON3", 
            code_block="""def ifelse(Actual, Planned):
                            if Actual == 0:
                                return Planned
                            else:
                                return Actual""", 
            field_type="DOUBLE", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Treatment Area Field (Calculate Field) (management)
        nfpors_select2p_clip_9_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_22_, 
            field="TREATMENT_AREA", 
            expression="ifelse(!ACTIVITY_UOM!,!ACTIVITY_QUANTITY!)", 
            expression_type="PYTHON3", 
            code_block="""def ifelse(Units, Quant):
                            if Units == \"AC\":
                                return Quant""", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Activity Start Date (2) (Calculate Field) (management)
        nfpors_select2_clip_dissolve_4_ = arcpy.management.CalculateField(
            in_table=nfpors_select2p_clip_9_, 
            field="ACTIVITY_START", 
            expression="ifelse(!actualinitiationdate!, !plannedinitiationdate!)", 
            expression_type="PYTHON3", 
            code_block="""def ifelse(Initiated, Planned):
                            if Initiated >= datetime.datetime(1901, 1, 1):
                                return Initiated
                            else:
                                return Planned""", 
            field_type="TEXT", 
            enforce_domains="ENFORCE_DOMAINS"
            )

        # Process: Calculate Activity End Date (2) (Calculate Field) (management)
        usfs_haz_fuels_treatments_reduction2_7_ = arcpy.management.CalculateField(
            in_table=nfpors_select2_clip_dissolve_4_, 
            field="ACTIVITY_END", 
            expression="ifelse(!actualcompletiondate!, !plannedinitiationdate!)", 
            expression_type="PYTHON3", 
            code_block="""def ifelse(DateComp, DatePl):
                            if DateComp >= datetime.datetime(1901, 1, 1):
                                return DateComp
                            else:
                                return DatePl""", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Status (3) (Calculate Field) (management)
        usfs_haz_fuels_treatments_reduction2_8_ = arcpy.management.CalculateField(
            in_table=usfs_haz_fuels_treatments_reduction2_7_, 
            field="ACTIVITY_STATUS", 
            expression="\"Active\"", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Source (3) (Calculate Field) (management)
        Updated_Input_Table_23_ = arcpy.management.CalculateField(
            in_table=usfs_haz_fuels_treatments_reduction2_8_, 
            field="Source", 
            expression="\"nfpors_haz_fuels_treatments_reduction\"", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Crosswalk (2) (Calculate Field) (management)
        Updated_Input_Table_26_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_23_, 
            field="Crosswalk", 
            expression="!typename!", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="ENFORCE_DOMAINS"
            )

        print(f'Saving Output Points Standardized: {output_pts_standardized}')
        # Process: Copy Features (3) (Copy Features) (management)
        arcpy.management.CopyFeatures(
            in_features=Updated_Input_Table_26_, 
            out_feature_class=output_pts_standardized, 
            config_keyword="", 
            spatial_grid_1=None, 
            spatial_grid_2=None, 
            spatial_grid_3=None
            )

        # Process: Delete Field (2) (Delete Field) (management)
        nfpors_select2p_clip_8_ = KeepFields(output_original_polys)

        # Process: 2b Assign Domains (2) (2b Assign Domains) (PC414CWIMillionAcres)
        usfs_silviculture_reforestation_enriched_20220629_4_ = AssignDomains(in_table=nfpors_select2p_clip_8_)

        print('Performing Points Enrichments')
        # Process: 7b Enrichments pts (7b Enrichments pts) (PC414CWIMillionAcres)
        Pts_enrichment_Veg2 = os.path.join(scratch_workspace,'Pts_enrichment_Veg2')
        bEnrichmentsPoints(enrich_pts_out=output_pts_enriched, enrich_pts_in=usfs_silviculture_reforestation_enriched_20220629_4_)

        print(f'Saving Output Points Enriched: {output_pts_enriched}')
        # Process: Copy Features (Copy Features) (management)
        # arcpy.management.CopyFeatures(
        #     in_features=Pts_enrichment_Veg2, 
        #     out_feature_class=output_pts_enriched, 
        #     config_keyword="", 
        #     spatial_grid_1=None, 
        #     spatial_grid_2=None, 
        #     spatial_grid_3=None
        #     )

        # Process: Calculate Treatment ID (3) (Calculate Field) (management)
        usfs_haz_fuels_treatments_reduction2_5_ = arcpy.management.CalculateField(
            in_table=output_pts_enriched, 
            field="TRMTID_USER", 
            expression="!PROJECTID_USER![-7:]+'-'+!IN_WUI![:3]+'-'+!PRIMARY_OWNERSHIP_GROUP![:1]+'-'+!COUNTY![:8]+'-'+!PRIMARY_OBJECTIVE![:12])", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )
        
        # Process: 2b Assign Domains (3) (2b Assign Domains) (PC414CWIMillionAcres)
        WFR_TF_Template_2_ = AssignDomains(in_table=output_pts_enriched)
        
        print('Deleting Scratch Files')
        delete_scratch_files(gdb = scratch_workspace, delete_fc = 'yes', delete_table = 'yes', delete_ds = 'yes')
        
        end = time.time()
        print(f'Time Elapsed: {(end-start)/60} minutes')
if __name__ == '__main__':
    # Global Environment settings
     with arcpy.EnvManager(
    extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""",  outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""", 
    preserveGlobalIds=True, 
    qualifiedFieldNames=False, 
    scratchWorkspace=scratch_workspace, 
    transferDomains=True, 
    transferGDBAttributeProperties=True, 
    workspace=workspace):
        Model71(*argv[1:])
