import arcpy
from ._1b_add_fields import AddFields
from ._2b_assign_domains import AssignDomains
from ._7b_enrichments_pts import enrich_points
from ._7c_enrichments_lines import enrich_lines
from ._2k_keep_fields import KeepFields
import os
from sys import argv
from .utils import init_gdb, delete_scratch_files, runner
import time

original_gdb, workspace, scratch_workspace = init_gdb()


# 6m CalTrans_Activities 20221123
# def CalTrans(input_pts, input_polys, output_lines_standardized, output_points_standardized, output_points_enriched, output_lines_enriched):
def CalTrans(
    input_polys21,
    input_polys22,
    input_table21,
    input_table22,
    output_lines_standardized,
    output_lines_enriched,
):
    start = time.time()
    print(f"Start Time {time.ctime()}")
    arcpy.env.overwriteOutput = True

    arcpy.ImportToolbox(
        r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx"
    )

    # define intermediary objects in scratch
    CalTrans21_scratch = os.path.join(scratch_workspace, "CalTrans21_scratch")
    CalTrans22_scratch = os.path.join(scratch_workspace, "CalTrans22_scratch")

    # ### BEGIN POINTS WORKFLOW
    # print('Performing Points Standardization')
    # # Process: Feature To Point (Feature To Point) (management)
    # #TODO Revisit whether we should stay with multi-point features
    # #TODO Verify joined input Treatments and Activities
    # caltrans_FeatureToPoint = os.path.join(scratch_workspace, "caltrans_FeatureToPoint")
    # arcpy.management.FeatureToPoint(in_features=input_pts,
    #                                 out_feature_class=caltrans_FeatureToPoint,
    #                                 point_location="CENTROID")

    # # Process: Alter Field County (Alter Field) (management)
    # caltrans_alterfield_v1 = arcpy.management.AlterField(in_table=caltrans_FeatureToPoint,
    #                                                      field="County",
    #                                                      new_field_name="County_",
    #                                                      new_field_alias="",
    #                                                      field_type="",
    #                                                      #field_length=25,
    #                                                      #field_is_nullable="NULLABLE",
    #                                                      clear_field_alias="DO_NOT_CLEAR")

    # # Process: Alter Field Activity Description (Alter Field) (management)
    # caltrans_alterfield_v2 = arcpy.management.AlterField(in_table=caltrans_alterfield_v1,
    #                                                      field="Activity_Description",
    #                                                      new_field_name="Activity_Description_",
    #                                                      new_field_alias="",
    #                                                      field_type="",
    #                                                      #field_length=70,
    #                                                      #field_is_nullable="NON_NULLABLE",
    #                                                      clear_field_alias="DO_NOT_CLEAR")

    # # Process: Alter Field Veg (Alter Field) (management)
    # caltrans_alterfield_v3 = arcpy.management.AlterField(in_table=caltrans_alterfield_v2,
    #                                                    field="Broad_Vegetation_Type",
    #                                                    new_field_name="BVT",
    #                                                    new_field_alias="",
    #                                                    field_type="",
    #                                                    #field_length=50,
    #                                                    #field_is_nullable="NON_NULLABLE",
    #                                                    clear_field_alias="DO_NOT_CLEAR")

    # # Process: Alter Field Activity Status (Alter Field) (management)
    # caltrans_alterfield_v4 = arcpy.management.AlterField(in_table=caltrans_alterfield_v3,
    #                                                       field="Activity_Status",
    #                                                       new_field_name="Act_Status",
    #                                                       new_field_alias="",
    #                                                       field_type="",
    #                                                       #field_length=25,
    #                                                       #field_is_nullable="NON_NULLABLE",
    #                                                       clear_field_alias="DO_NOT_CLEAR")

    # # Process: Alter Activity Quantity (Alter Field) (management)
    # caltrans_alterfield_v5 = arcpy.management.AlterField(in_table=caltrans_alterfield_v4,
    #                                                      field="Activity_Quantity",
    #                                                      new_field_name="Production_Quantity",
    #                                                      new_field_alias="",
    #                                                      field_type="",
    #                                                      #field_length=8,
    #                                                      #field_is_nullable="NON_NULLABLE",
    #                                                      clear_field_alias="DO_NOT_CLEAR")

    # # Process: Alter Field Residue Fate (Alter Field) (management)
    # caltrans_alterfield_v6 = arcpy.management.AlterField(in_table=caltrans_alterfield_v5,
    #                                                    field="Residue_Fate",
    #                                                    new_field_name="Fate",
    #                                                    new_field_alias="",
    #                                                    field_type="",
    #                                                    #field_length=35,
    #                                                    #field_is_nullable="NON_NULLABLE",
    #                                                    clear_field_alias="DO_NOT_CLEAR")

    # # Process: Alter Field Fate Units (Alter Field) (management)
    # caltrans_alterfield_v7 = arcpy.management.AlterField(in_table=caltrans_alterfield_v6,
    #                                                       field="Residue_Fate_Units",
    #                                                       new_field_name="FateUnits",
    #                                                       new_field_alias="",
    #                                                       field_type="",
    #                                                       #field_length=5,
    #                                                       #field_is_nullable="NON_NULLABLE",
    #                                                       clear_field_alias="DO_NOT_CLEAR")

    # # Process: Alter Residue Quantity (Alter Field) (management)
    # caltrans_alterfield_v8 = arcpy.management.AlterField(in_table=caltrans_alterfield_v7,
    #                                                    field="Residue_Fate_Quantity",
    #                                                    new_field_name="FateQuantity",
    #                                                    new_field_alias="",
    #                                                    field_type="",
    #                                                    #field_length=8,
    #                                                    #field_is_nullable="NON_NULLABLE",
    #                                                    clear_field_alias="DO_NOT_CLEAR")

    # # Process: 1b Add Fields (1b Add Fields) (PC414CWIMillionAcres)
    # caltrans_addfields = AddFields(Input_Table=caltrans_alterfield_v8)

    # # Process: Calculate Project ID (Calculate Field) (management)
    # caltrans_calc_field_v1 = arcpy.management.CalculateField(in_table=caltrans_addfields,
    #                                                          field="PROJECTID_USER",
    #                                                          expression="!HighwayID!",
    #                                                          expression_type="PYTHON3",
    #                                                          code_block="",
    #                                                          field_type="TEXT",
    #                                                          enforce_domains="NO_ENFORCE_DOMAINS")

    # # Process: Calculate Agency (Calculate Field) (management)
    # caltrans_calc_field_v2 = arcpy.management.CalculateField(in_table=caltrans_calc_field_v1,
    #                                                          field="AGENCY",
    #                                                          expression="\"CALSTA\"",
    #                                                          expression_type="PYTHON3",
    #                                                          code_block="",
    #                                                          field_type="TEXT",
    #                                                          enforce_domains="NO_ENFORCE_DOMAINS")

    # # Process: Calculate Org Data Steward (Calculate Field) (management)
    # caltrans_calc_field_v3 = arcpy.management.CalculateField(in_table=caltrans_calc_field_v2,
    #                                                         field="ORG_ADMIN_p",
    #                                                         expression="\"CALTRANS\"",
    #                                                         expression_type="PYTHON3",
    #                                                         code_block="",
    #                                                         field_type="TEXT",
    #                                                         enforce_domains="NO_ENFORCE_DOMAINS")

    # # Process: Calculate Project Contact (Calculate Field) (management)
    # caltrans_calc_field_v4 = arcpy.management.CalculateField(in_table=caltrans_calc_field_v3,
    #                                                          field="PROJECT_CONTACT",
    #                                                          expression="\"Division of Maintenance\"",
    #                                                          expression_type="PYTHON3",
    #                                                          code_block="",
    #                                                          field_type="TEXT",
    #                                                          enforce_domains="NO_ENFORCE_DOMAINS")

    # # Process: Calculate Email (Calculate Field) (management)
    # caltrans_calc_field_v5 = arcpy.management.CalculateField(in_table=caltrans_calc_field_v4,
    #                                                       field="PROJECT_EMAIL",
    #                                                       expression="\"andrew.lozano@dot.ca.gov\"",
    #                                                       expression_type="PYTHON3",
    #                                                       code_block="",
    #                                                       field_type="TEXT",
    #                                                       enforce_domains="NO_ENFORCE_DOMAINS")

    # # Process: Calculate Admin Org (Calculate Field) (management)
    # caltrans_calc_field_v6 = arcpy.management.CalculateField(in_table=caltrans_calc_field_v5,
    #                                                        field="ADMINISTERING_ORG",
    #                                                        expression="\"CALTRANS\"",
    #                                                        expression_type="PYTHON3",
    #                                                        code_block="",
    #                                                        field_type="TEXT",
    #                                                        enforce_domains="NO_ENFORCE_DOMAINS")

    # # Process: Calculate Primary Funding Source (Calculate Field) (management)
    # caltrans_calc_field_v7 = arcpy.management.CalculateField(in_table=caltrans_calc_field_v6,
    #                                                          field="PRIMARY_FUNDING_SOURCE",
    #                                                          expression="\"GENERAL_FUND\"",
    #                                                          expression_type="PYTHON3",
    #                                                          code_block="",
    #                                                          field_type="TEXT",
    #                                                          enforce_domains="NO_ENFORCE_DOMAINS")

    # # Process: Calculate Primary Funding Org (Calculate Field) (management)
    # caltrans_calc_field_v8 = arcpy.management.CalculateField(in_table=caltrans_calc_field_v7,
    #                                                           field="PRIMARY_FUNDING_ORG",
    #                                                           expression="\"CALTRANS\"",
    #                                                           expression_type="PYTHON3",
    #                                                           code_block="",
    #                                                           field_type="TEXT",
    #                                                           enforce_domains="NO_ENFORCE_DOMAINS")

    # # Process: Calculate Treatment ID (Calculate Field) (management)
    # # Updated_Input_Table_45_ = arcpy.management.CalculateField(in_table=caltrans_calc_field_v8,
    # #                                                           field="TRMTID_USER",
    # #                                                           expression="!IMMS_Unit_ID!", #+'-'+!COUNTY!+'-'+!REGION!+'-'+!IN_WUI!",
    # #                                                           expression_type="PYTHON3",
    # #                                                           code_block="",
    # #                                                           field_type="TEXT",
    # #                                                           enforce_domains="NO_ENFORCE_DOMAINS")

    # # Process: Calculate WUI (Calculate Field) (management)
    # caltrans_calc_field_v9 = arcpy.management.CalculateField(in_table=caltrans_calc_field_v8,
    #                                                           field="IN_WUI",
    #                                                           expression="ifelse(!WUI!)",
    #                                                           expression_type="PYTHON3",
    #                                                           code_block="""def ifelse(WUI):
    #                                                                 if WUI == \"Yes\":
    #                                                                     return \"WUI_USER_DEFINED\"
    #                                                                 elif WUI == \"No\":
    #                                                                     return \"NON-WUI_USER_DEFINED\"
    #                                                                 else:
    #                                                                     return WUI""", field_type="TEXT",
    #                                                           enforce_domains="NO_ENFORCE_DOMAINS"
    #                                                                 )

    # # Process: Calculate Treatment Area (Calculate Field) (management)
    # caltrans_calc_field_v10 = arcpy.management.CalculateField(in_table=caltrans_calc_field_v9,
    #                                                           field="TREATMENT_AREA",
    #                                                           expression="ifelse(!Activity_Unit_of_Measure!, !Production_Quantity!)",
    #                                                           expression_type="PYTHON3",
    #                                                           code_block="""def ifelse(UOM, Q):
    #                                                                 if UOM == \"ACRE\":
    #                                                                     return Q
    #                                                                 else:
    #                                                                     return None""", field_type="TEXT",
    #                                                           enforce_domains="NO_ENFORCE_DOMAINS")

    # # Process: Calculate Activity ID (Calculate Field) (management)
    # caltrans_calc_field_v11 = arcpy.management.CalculateField(in_table=caltrans_calc_field_v10,
    #                                                                field="ACTIVID_USER",
    #                                                                expression="!Work_Order_Number!",
    #                                                                expression_type="PYTHON3",
    #                                                                code_block="",
    #                                                                field_type="TEXT",
    #                                                                enforce_domains="NO_ENFORCE_DOMAINS")

    # # Process: Calculate Implementing Org (Calculate Field) (management)
    # caltrans_calc_field_v12 = arcpy.management.CalculateField(in_table=caltrans_calc_field_v11,
    #                                                           field="IMPLEMENTING_ORG",
    #                                                           expression="!IMMS_Unit_ID!",
    #                                                           expression_type="PYTHON3",
    #                                                           code_block="",
    #                                                           field_type="TEXT",
    #                                                           enforce_domains="NO_ENFORCE_DOMAINS")

    # # Process: Calculate Activity UOM (Calculate Field) (management)
    # caltrans_calc_field_v13 = arcpy.management.CalculateField(in_table=caltrans_calc_field_v12,
    #                                                           field="ACTIVITY_UOM",
    #                                                           expression="ifelse(!Activity_Unit_of_Measure!)",
    #                                                           expression_type="PYTHON3",
    #                                                           code_block="""def ifelse(Unit):
    #                                                                         if Unit == 'ACRE':
    #                                                                             return 'AC'
    #                                                                         else:
    #                                                                             return Unit""",
    #                                                           field_type="TEXT",
    #                                                           enforce_domains="NO_ENFORCE_DOMAINS")

    # # Process: Calculate Activity Quantity (Calculate Field) (management)
    # caltrans_calc_field_v14 = arcpy.management.CalculateField(in_table=caltrans_calc_field_v13,
    #                                                           field="ACTIVITY_QUANTITY",
    #                                                           expression="!Production_Quantity!",
    #                                                           expression_type="PYTHON3",
    #                                                           code_block="",
    #                                                           field_type="TEXT",
    #                                                           enforce_domains="NO_ENFORCE_DOMAINS")

    # # Process: Calculate Status (Calculate Field) (management)
    # caltrans_calc_field_v15 = arcpy.management.CalculateField(in_table=caltrans_calc_field_v14,
    #                                                           field="ACTIVITY_STATUS",
    #                                                           expression="ifelse(!Act_Status!)",
    #                                                           expression_type="PYTHON3",
    #                                                           code_block="""def ifelse(Status):
    #                                                                     if Status == \"Complete\":
    #                                                                         return \"COMPLETE\"
    #                                                                     else:
    #                                                                         return Status""", field_type="TEXT",
    #                                                           enforce_domains="NO_ENFORCE_DOMAINS")

    # # Process: Calculate Activity Start (Calculate Field) (management)
    # caltrans_calc_field_v16 = arcpy.management.CalculateField(in_table=caltrans_calc_field_v15,
    #                                                           field="ACTIVITY_START",
    #                                                           expression="!Start!",
    #                                                           expression_type="PYTHON3",
    #                                                           code_block="",
    #                                                           field_type="TEXT",
    #                                                           enforce_domains="NO_ENFORCE_DOMAINS")

    # # Process: Calculate Activity End (Calculate Field) (management)
    # caltrans_calc_field_v17 = arcpy.management.CalculateField(in_table=caltrans_calc_field_v16,
    #                                                           field="ACTIVITY_END",
    #                                                           expression="!End_!",
    #                                                           expression_type="PYTHON3",
    #                                                           code_block="",
    #                                                           field_type="TEXT",
    #                                                           enforce_domains="NO_ENFORCE_DOMAINS")

    # # Process: Calculate Source (Calculate Field) (management)
    # caltrans_calc_field_v18 = arcpy.management.CalculateField(in_table=caltrans_calc_field_v17,
    #                                                           field="Source",
    #                                                           expression="\"CALTRANS\"",
    #                                                           expression_type="PYTHON3",
    #                                                           code_block="",
    #                                                           field_type="TEXT",
    #                                                           enforce_domains="NO_ENFORCE_DOMAINS")

    # # Process: Calculate Crosswalk (Calculate Field) (management)
    # caltrans_calc_field_v19 = arcpy.management.CalculateField(in_table=caltrans_calc_field_v18,
    #                                                           field="Crosswalk",
    #                                                           expression="!Activity_Description_!",
    #                                                           expression_type="PYTHON3",
    #                                                           code_block="",
    #                                                           field_type="TEXT",
    #                                                           enforce_domains="NO_ENFORCE_DOMAINS")

    # # Process: Calculate Geometry Attributes (Calculate Geometry Attributes) (management)
    # # CalTrans_pts_Copy_7_ = arcpy.management.CalculateGeometryAttributes(in_features=caltrans_calc_field_v19,
    # #                                                                     geometry_property=[["LATITUDE", "POINT_Y"], ["LONGITUDE", "POINT_X"]],
    # #                                                                     length_unit="",
    # #                                                                     area_unit="",
    # #                                                                     coordinate_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]",
    # #                                                                     coordinate_format="DD")

    # # Process: Delete Field (3) (Delete Field) (management)
    # caltrans_keepfields = KeepFields(caltrans_calc_field_v1)

    # print(f'Saving Output Points Standardized: {output_points_standardized}')
    # # Process: Copy Features (Copy Features) (management)
    # arcpy.management.CopyFeatures(in_features=caltrans_keepfields,
    #                               out_feature_class=output_points_standardized,
    #                               config_keyword="",
    #                               spatial_grid_1=None,
    #                               spatial_grid_2=None,
    #                               spatial_grid_3=None)

    # # Process: 2b Assign Domains (2b Assign Domains) (PC414CWIMillionAcres)
    # caltrans_assigndomains = AssignDomains(in_table=output_points_standardized)

    # print('Performing Points Enrichments')
    # # Process: 7b Enrichments pts (7b Enrichments pts) (PC414CWIMillionAcres)
    # # Pts_enrichment_Veg2 = os.path.join(scratch_workspace, "Pts_enrichment_Veg2")
    # enrich_points(enrich_pts_out=output_points_enriched,
    #                    enrich_pts_in=caltrans_assigndomains,
    #                    delete_scratch=True) # need to delete scratch here because we call enrich_points again for Line Enrichments and we'll catch a 'dataset already exists' error

    # # Process: Copy Features (5) (Copy Features) (management)
    # # arcpy.management.CopyFeatures(in_features=Pts_enrichment_Veg2,
    # #                               out_feature_class=output_points_enriched,
    # #                               config_keyword="",
    # #                               spatial_grid_1=None,
    # #                               spatial_grid_2=None,
    # #                               spatial_grid_3=None)

    # # Process: Calculate Owner State (Calculate Field) (management)
    # caltrans_enriched_calc_field_v1 = arcpy.management.CalculateField(in_table=output_points_enriched,
    #                                                           field="PRIMARY_OWNERSHIP_GROUP",
    #                                                           expression="\"STATE\"",
    #                                                           expression_type="PYTHON3",
    #                                                           code_block="",
    #                                                           field_type="TEXT",
    #                                                           enforce_domains="NO_ENFORCE_DOMAINS")

    #     # Process: Calculate Treatment ID (Calculate Field) (management)
    # caltrans_enriched_calc_field_v2 = arcpy.management.CalculateField(in_table=caltrans_enriched_calc_field_v1,
    #                                                           field="TREATMENT_ID_USER",
    #                                                           expression="!PROJECTID_USER!+'-'+!COUNTY![:8]+'-'+!REGION![:3]+'-'+!IN_WUI![:3]",
    #                                                           expression_type="PYTHON3",
    #                                                           code_block="",
    #                                                           field_type="TEXT",
    #                                                           enforce_domains="NO_ENFORCE_DOMAINS")

    # # Process: 2b Assign Domains (2) (2b Assign Domains) (PC414CWIMillionAcres)
    # # caltrans_enriched_assigndomains =
    # AssignDomains(in_table=caltrans_enriched_calc_field_v2)

    ### BEGIN POLYLINE WORKFLOW
    # Process: Add Join (2) (Add Join) (management)
    print("     step 3/33 add join")
    input_table21_join = arcpy.management.AddJoin(
        in_layer_or_view=input_polys21,
        in_field="HIghwayID",
        join_table=input_table21,
        join_field="HIghwayID",
        join_type="KEEP_ALL",
        index_join_fields="INDEX_JOIN_FIELDS",
    )

    # Process: Copy Features (Copy Features) (management)
    input_table21_join_copy = arcpy.management.CopyFeatures(
        input_table21_join, CalTrans21_scratch
    )

    input_table22_join = arcpy.management.AddJoin(
        in_layer_or_view=input_polys22,
        in_field="HIghwayID",
        join_table=input_table22,
        join_field="HIghwayID",
        join_type="KEEP_ALL",
        index_join_fields="INDEX_JOIN_FIELDS",
    )

    # Process: Copy Features (2) (Copy Features) (management)
    input_table22_join_copy = arcpy.management.CopyFeatures(
        input_table22_join, CalTrans22_scratch
    )

    print("Appending Lines")

    print("Performing Line Standardization")
    # Process: Copy Features (2) (Copy Features) (management)
    caltrans_poly_copy = os.path.join(scratch_workspace, "CalTrans_pts_Copy")
    arcpy.management.CopyFeatures(
        in_features=input_polys,
        out_feature_class=caltrans_poly_copy,
        config_keyword="",
        spatial_grid_1=None,
        spatial_grid_2=None,
        spatial_grid_3=None,
    )

    # Process: Repair Geometry (Repair Geometry) (management)
    caltrans_poly_copy_repaired_geom = arcpy.management.RepairGeometry(
        in_features=caltrans_poly_copy,
        delete_null="KEEP_NULL",
        validation_method="ESRI",
    )

    # Process: Alter Field County (2) (Alter Field) (management)
    caltrans_poly_alterfield_v1 = arcpy.management.AlterField(
        in_table=caltrans_poly_copy_repaired_geom,
        field="County",
        new_field_name="County2",
        new_field_alias="County2",
        field_type="TEXT",
        # field_length=25,
        # field_is_nullable="NULLABLE",
        clear_field_alias="DO_NOT_CLEAR",
    )

    # Process: Alter Field Activity Description (2) (Alter Field) (management)
    caltrans_poly_alterfield_v2 = arcpy.management.AlterField(
        in_table=caltrans_poly_alterfield_v1,
        field="Activity_Description",
        new_field_name="Activity_Description_",
        new_field_alias="",
        field_type="TEXT",
        # field_length=70,
        # field_is_nullable="NULLABLE",
        clear_field_alias="DO_NOT_CLEAR",
    )

    # Process: Alter Field Veg (2) (Alter Field) (management)
    caltrans_poly_alterfield_v3 = arcpy.management.AlterField(
        in_table=caltrans_poly_alterfield_v2,
        field="Broad_Vegetation_Type",
        new_field_name="BVT",
        new_field_alias="",
        field_type="TEXT",
        # field_length=50,
        # field_is_nullable="NULLABLE",
        clear_field_alias="DO_NOT_CLEAR",
    )

    # Process: Alter Field Activity Status (2) (Alter Field) (management)
    caltrans_poly_alterfield_v4 = arcpy.management.AlterField(
        in_table=caltrans_poly_alterfield_v3,
        field="Activity_Status",
        new_field_name="Act_Status",
        new_field_alias="",
        field_type="TEXT",
        # field_length=25,
        # field_is_nullable="NULLABLE",
        clear_field_alias="DO_NOT_CLEAR",
    )

    # Process: Alter Activity Quantity (2) (Alter Field) (management)
    caltrans_poly_alterfield_v5 = arcpy.management.AlterField(
        in_table=caltrans_poly_alterfield_v4,
        field="Activity_Quantity",
        new_field_name="Production_Quantity",
        new_field_alias="",
        field_type="DOUBLE",
        # field_length=8,
        # field_is_nullable="NULLABLE",
        clear_field_alias="DO_NOT_CLEAR",
    )

    # Process: Alter Field Residue Fate (2) (Alter Field) (management)
    caltrans_poly_alterfield_v6 = arcpy.management.AlterField(
        in_table=caltrans_poly_alterfield_v5,
        field="Residue_Fate",
        new_field_name="Fate",
        new_field_alias="",
        field_type="TEXT",
        # field_length=35,
        # field_is_nullable="NULLABLE",
        clear_field_alias="DO_NOT_CLEAR",
    )

    # Process: Alter Field Fate Units (2) (Alter Field) (management)
    caltrans_poly_alterfield_v7 = arcpy.management.AlterField(
        in_table=caltrans_poly_alterfield_v6,
        field="Residue_Fate_Units",
        new_field_name="FateUnits",
        new_field_alias="",
        field_type="TEXT",
        # field_length=5,
        # field_is_nullable="NULLABLE",
        clear_field_alias="DO_NOT_CLEAR",
    )

    # Process: Alter Residue Quantity (2) (Alter Field) (management)
    caltrans_poly_alterfield_v8 = arcpy.management.AlterField(
        in_table=caltrans_poly_alterfield_v7,
        field="Residue_Fate_Quantity",
        new_field_name="FateQuantity",
        new_field_alias="",
        field_type="DOUBLE",
        # field_length=8,
        # field_is_nullable="NULLABLE",
        clear_field_alias="DO_NOT_CLEAR",
    )

    # Process: 1b Add Fields (2) (1b Add Fields) (PC414CWIMillionAcres)
    caltrans_poly_addfields = AddFields(Input_Table=caltrans_poly_alterfield_v8)

    # Process: Calculate Project ID (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v1 = arcpy.management.CalculateField(
        in_table=caltrans_poly_addfields,
        field="PROJECTID_USER",
        expression="!HighwayID!",
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Agency (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v2 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v1,
        field="AGENCY",
        expression='"CALSTA"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Data Steward (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v3 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v2,
        field="ORG_ADMIN_p",
        expression='"CALTRANS"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Project Contact (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v4 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v3,
        field="PROJECT_CONTACT",
        expression='"Division of Maintenance"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Email (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v5 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v4,
        field="PROJECT_EMAIL",
        expression='"andrew.lozano@dot.ca.gov"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Admin Org (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v6 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v5,
        field="ADMINISTERING_ORG",
        expression="!District!",
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Primary Funding Source (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v7 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v6,
        field="PRIMARY_FUNDING_SOURCE",
        expression='"GENERAL_FUND"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Primary Funding Org (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v8 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v7,
        field="PRIMARY_FUNDING_ORG",
        expression='"CALTRANS"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Treatment ID (2) (Calculate Field) (management)
    # Updated_Input_Table_46_ = arcpy.management.CalculateField(in_table=caltrans_poly_calc_field_v8,
    #                                                           field="TRMTID_USER",
    #                                                           expression="!IMMS_ID!", #+'-'+!COUNTY!+'-'+!REGION!"+'-'+!IN_WUI!",
    #                                                           expression_type="PYTHON3",
    #                                                           code_block="",
    #                                                           field_type="TEXT",
    #                                                           enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate WUI (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v9 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v8,
        field="IN_WUI",
        expression="ifelse(!WUI!)",
        expression_type="PYTHON3",
        code_block="""def ifelse(WUI):
                                                                if WUI == \"Yes\":
                                                                    return \"WUI_USER_DEFINED\"
                                                                elif WUI == \"No\":
                                                                    return \"NON-WUI_USER_DEFINED\"
                                                                else:
                                                                    return WUI""",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Treatment Area (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v10 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v9,
        field="TREATMENT_AREA",
        expression="ifelse(!Activity_Unit_of_Measure!, !Production_Quantity!)",
        expression_type="PYTHON3",
        code_block="""def ifelse(UOM, Q):
                                                                if UOM == \"ACRE\":
                                                                    return Q
                                                                else:
                                                                    return None""",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Activity ID (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v11 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v10,
        field="ACTIVID_USER",
        expression="!Work_Order_Number!",
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Implementing Org (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v12 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v11,
        field="IMPLEMENTING_ORG",
        expression="!IMMS_ID!",
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Activity UOM (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v13 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v12,
        field="ACTIVITY_UOM",
        expression="ifelse(!Activity_Unit_of_Measure!)",
        expression_type="PYTHON3",
        code_block="""def ifelse(Unit):
                                                                            if Unit == 'ACRE':
                                                                                return 'AC'
                                                                            else:
                                                                                return Unit""",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Activity Quantity (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v14 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v13,
        field="ACTIVITY_QUANTITY",
        expression="!Production_Quantity!",
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Status (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v15 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v14,
        field="ACTIVITY_STATUS",
        expression="ifelse(!Act_Status!)",
        expression_type="PYTHON3",
        code_block="""def ifelse(Status):
                                                                if Status == \"Complete\":
                                                                    return \"COMPLETE\"
                                                                else:
                                                                    return Status""",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Activity Start (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v16 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v15,
        field="ACTIVITY_START",
        expression="!Start!",
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Activity End (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v17 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v16,
        field="ACTIVITY_END",
        expression="!End_!",
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Source (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v18 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v17,
        field="Source",
        expression='"CALTRANS"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Crosswalk (2) (Calculate Field) (management)
    caltrans_poly_calc_field_v19 = arcpy.management.CalculateField(
        in_table=caltrans_poly_calc_field_v18,
        field="Crosswalk",
        expression="!Activity_Description_!",
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: Calculate Geometry Attributes (2) (Calculate Geometry Attributes) (management)
    # CalTrans_pts_Copy_15_ = arcpy.management.CalculateGeometryAttributes(in_features=caltrans_poly_calc_field_v19,
    #                                                                      geometry_property=[["LATITUDE", "INSIDE_Y"], ["LONGITUDE", "INSIDE_X"]],
    #                                                                      length_unit="",
    #                                                                      area_unit="",
    #                                                                      coordinate_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]",
    #                                                                      coordinate_format="DD")

    # Process: Delete Field (2) (Delete Field) (management)
    caltrans_poly_keepfields = KeepFields(caltrans_poly_calc_field_v19)

    print(f"Saving Output Lines Standardized: {output_lines_standardized}")
    # Process: Copy Features (3) (Copy Features) (management)
    arcpy.management.CopyFeatures(
        in_features=caltrans_poly_keepfields,
        out_feature_class=output_lines_standardized,
        config_keyword="",
        spatial_grid_1=None,
        spatial_grid_2=None,
        spatial_grid_3=None,
    )

    # Process: 2b Assign Domains (3) (2b Assign Domains) (PC414CWIMillionAcres)
    caltrans_line_standardized_assigndomains = AssignDomains(
        in_table=output_lines_standardized
    )

    print("Performing Lines Enrichments")
    # Process: 7c Enrichments Lines (2) (7c Enrichments Lines) (PC414CWIMillionAcres)
    caltrans_lines_enriched = enrich_lines(
        line_fc=caltrans_line_standardized_assigndomains
    )  # don't delete scratch

    print(f"Saving Output Lines Enriched: {output_lines_enriched}")
    # Process: Copy Features (4) (Copy Features) (management)
    arcpy.management.CopyFeatures(
        in_features=caltrans_lines_enriched,
        out_feature_class=output_lines_enriched,
        config_keyword="",
        spatial_grid_1=None,
        spatial_grid_2=None,
        spatial_grid_3=None,
    )

    # Process: Calculate Owner State (2) (Calculate Field) (management)
    caltrans_lines_enriched_calc_field_v1 = arcpy.management.CalculateField(
        in_table=output_lines_enriched,
        field="PRIMARY_OWNERSHIP_GROUP",
        expression='"STATE"',
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    ## *** IMMS_Unit_ID and IMMS_ID no longer exist after running a 7 tool on the data, so changed to 'TREATMENT_ID_USER' since that was filled with IMMS
    ## *** prior to the 7 tool being ran. Get non-specific error (no line traceback) that nontypes and string types cannot be concatenated when
    ## *** running the script with this block of code intact. The output table "caltrans_lines_enriched_calc_field_v2" should be fed into AssignDomains below once functioning.
    # Process: Calculate Treatment ID (2) (Calculate Field) (management)
    caltrans_lines_enriched_calc_field_v2 = arcpy.management.CalculateField(
        in_table=caltrans_lines_enriched_calc_field_v1,
        field="TREATMENT_ID_USER",
        expression="!PROJECTID_USER!+'-'+!COUNTY![:8]+'-'+!REGION![:3]+'-'+!IN_WUI![:3]",
        expression_type="PYTHON3",
        code_block="",
        field_type="TEXT",
        enforce_domains="NO_ENFORCE_DOMAINS",
    )

    # Process: 2b Assign Domains (4) (2b Assign Domains) (PC414CWIMillionAcres)
    caltrans_lines_enriched_assigndomains = AssignDomains(
        in_table=caltrans_lines_enriched_calc_field_v2
    )

    print("Deleting Scratch Files")
    delete_scratch_files(
        gdb=scratch_workspace, delete_fc="yes", delete_table="yes", delete_ds="yes"
    )

    end = time.time()
    print(f"Time Elapsed: {(end-start)/60} minutes")


if __name__ == "__main__":
    runner(workspace, scratch_workspace, CalTrans, "*argv[1:]")
# # Global Environment settings
#  with arcpy.EnvManager(
# extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""",  outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""",
# preserveGlobalIds=True,
# qualifiedFieldNames=False,
# scratchWorkspace=scratch_workspace,
# transferDomains=True,
# transferGDBAttributeProperties=True,
# workspace=workspace):
#     CalTrans(*argv[1:])
