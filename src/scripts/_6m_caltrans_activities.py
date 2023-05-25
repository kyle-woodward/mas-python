import arcpy
from ._1b_add_fields import AddFields2
from ._2b_assign_domains import AssignDomains
from ._7b_enrichments_pts import bEnrichmentsPoints
from ._7c_enrichments_lines import cEnrichmentsLines
from ._2k_keep_fields import KeepFields
import os
from sys import argv
from .utils import init_gdb, delete_scratch_files, runner
import time

original_gdb, workspace, scratch_workspace = init_gdb()

# 6m CalTrans_Activities 20221123
def CalTrans(input_pts, input_polys, output_lines_standardized, output_points_standardized, output_points_enriched, output_lines_enriched):  
    start = time.time()
    print(f'Start Time {time.ctime()}')
    arcpy.env.overwriteOutput = True

    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")

    ### BEGIN POINTS WORKFLOW
    print('Performing Points Standardization')
    # Process: Feature To Point (Feature To Point) (management)
    #TODO Revisit whether we should stay with multi-point features
    #TODO Verify joined input Treatments and Activities
    Output_Feature_Class = os.path.join(scratch_workspace, "Vegetation_Con_FeatureToPoint")
    arcpy.management.FeatureToPoint(in_features=input_pts, 
                                    out_feature_class=Output_Feature_Class, 
                                    point_location="CENTROID")

    # Process: Alter Field County (Alter Field) (management)
    Updated_Input_Table_2_ = arcpy.management.AlterField(in_table=Output_Feature_Class, 
                                                         field="County", 
                                                         new_field_name="County_", 
                                                         new_field_alias="", 
                                                         field_type="", 
                                                         #field_length=25, 
                                                         #field_is_nullable="NULLABLE", 
                                                         clear_field_alias="DO_NOT_CLEAR")

    # Process: Alter Field Activity Description (Alter Field) (management)
    Updated_Input_Table_4_ = arcpy.management.AlterField(in_table=Updated_Input_Table_2_, 
                                                         field="Activity_Description", 
                                                         new_field_name="Activity_Description_", 
                                                         new_field_alias="", 
                                                         field_type="", 
                                                         #field_length=70, 
                                                         #field_is_nullable="NON_NULLABLE", 
                                                         clear_field_alias="DO_NOT_CLEAR")

    # Process: Alter Field Veg (Alter Field) (management)
    CalTrans_pts_Copy_2_ = arcpy.management.AlterField(in_table=Updated_Input_Table_4_, 
                                                       field="Broad_Vegetation_Type", 
                                                       new_field_name="BVT", 
                                                       new_field_alias="", 
                                                       field_type="", 
                                                       #field_length=50, 
                                                       #field_is_nullable="NON_NULLABLE", 
                                                       clear_field_alias="DO_NOT_CLEAR")

    # Process: Alter Field Activity Status (Alter Field) (management)
    Updated_Input_Table_18_ = arcpy.management.AlterField(in_table=CalTrans_pts_Copy_2_, 
                                                          field="Activity_Status", 
                                                          new_field_name="Act_Status", 
                                                          new_field_alias="", 
                                                          field_type="", 
                                                          #field_length=25, 
                                                          #field_is_nullable="NON_NULLABLE", 
                                                          clear_field_alias="DO_NOT_CLEAR")

    # Process: Alter Activity Quantity (Alter Field) (management)
    Updated_Input_Table_9_ = arcpy.management.AlterField(in_table=Updated_Input_Table_18_, 
                                                         field="Activity_Quantity", 
                                                         new_field_name="Production_Quantity", 
                                                         new_field_alias="", 
                                                         field_type="", 
                                                         #field_length=8, 
                                                         #field_is_nullable="NON_NULLABLE", 
                                                         clear_field_alias="DO_NOT_CLEAR")

    # Process: Alter Field Residue Fate (Alter Field) (management)
    CalTrans_pts_Copy_3_ = arcpy.management.AlterField(in_table=Updated_Input_Table_9_, 
                                                       field="Residue_Fate", 
                                                       new_field_name="Fate", 
                                                       new_field_alias="", 
                                                       field_type="", 
                                                       #field_length=35, 
                                                       #field_is_nullable="NON_NULLABLE", 
                                                       clear_field_alias="DO_NOT_CLEAR")

    # Process: Alter Field Fate Units (Alter Field) (management)
    Updated_Input_Table_19_ = arcpy.management.AlterField(in_table=CalTrans_pts_Copy_3_, 
                                                          field="Residue_Fate_Units", 
                                                          new_field_name="FateUnits", 
                                                          new_field_alias="", 
                                                          field_type="", 
                                                          #field_length=5, 
                                                          #field_is_nullable="NON_NULLABLE", 
                                                          clear_field_alias="DO_NOT_CLEAR")

    # Process: Alter Residue Quantity (Alter Field) (management)
    CalTrans_pts_Copy_4_ = arcpy.management.AlterField(in_table=Updated_Input_Table_19_, 
                                                       field="Residue_Fate_Quantity", 
                                                       new_field_name="FateQuantity", 
                                                       new_field_alias="", 
                                                       field_type="", 
                                                       #field_length=8, 
                                                       #field_is_nullable="NON_NULLABLE", 
                                                       clear_field_alias="DO_NOT_CLEAR")

    # Process: 1b Add Fields (1b Add Fields) (PC414CWIMillionAcres)
    WFRTF_Template_4_ = AddFields2(Input_Table=CalTrans_pts_Copy_4_)

    # Process: Calculate Project ID (Calculate Field) (management)
    Updated_Input_Table_8_ = arcpy.management.CalculateField(in_table=WFRTF_Template_4_, 
                                                             field="PROJECTID_USER", 
                                                             expression="!HighwayID!", 
                                                             expression_type="PYTHON3", 
                                                             code_block="", 
                                                             field_type="TEXT", 
                                                             enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Agency (Calculate Field) (management)
    Updated_Input_Table_3_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_8_, 
                                                             field="AGENCY", 
                                                             expression="\"CALSTA\"", 
                                                             expression_type="PYTHON3", 
                                                             code_block="", 
                                                             field_type="TEXT", 
                                                             enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Org Data Steward (Calculate Field) (management)
    Updated_Input_Table_5_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_3_, 
                                                            field="ORG_ADMIN_p", 
                                                            expression="\"CALTRANS\"", 
                                                            expression_type="PYTHON3", 
                                                            code_block="", 
                                                            field_type="TEXT", 
                                                            enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Project Contact (Calculate Field) (management)
    Updated_Input_Table_7_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_5_, 
                                                             field="PROJECT_CONTACT", 
                                                             expression="\"Division of Maintenance\"", 
                                                             expression_type="PYTHON3", 
                                                             code_block="", 
                                                             field_type="TEXT", 
                                                             enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Email (Calculate Field) (management)
    Updated_Input_Table = arcpy.management.CalculateField(in_table=Updated_Input_Table_7_, 
                                                          field="PROJECT_EMAIL", 
                                                          expression="\"andrew.lozano@dot.ca.gov\"", 
                                                          expression_type="PYTHON3", 
                                                          code_block="", 
                                                          field_type="TEXT", 
                                                          enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Admin Org (Calculate Field) (management)
    CalTrans_pts_Copy_5_ = arcpy.management.CalculateField(in_table=Updated_Input_Table, 
                                                           field="ADMINISTERING_ORG", 
                                                           expression="\"CALTRANS\"", 
                                                           expression_type="PYTHON3", 
                                                           code_block="", 
                                                           field_type="TEXT", 
                                                           enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Primary Funding Source (Calculate Field) (management)
    Updated_Input_Table_6_ = arcpy.management.CalculateField(in_table=CalTrans_pts_Copy_5_, 
                                                             field="PRIMARY_FUNDING_SOURCE", 
                                                             expression="\"GENERAL_FUND\"", 
                                                             expression_type="PYTHON3", 
                                                             code_block="", 
                                                             field_type="TEXT", 
                                                             enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Primary Funding Org (Calculate Field) (management)
    Updated_Input_Table_10_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_6_, 
                                                              field="PRIMARY_FUNDING_ORG", 
                                                              expression="\"CALTRANS\"", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Treatment ID (Calculate Field) (management)
    # Updated_Input_Table_45_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_10_, 
    #                                                           field="TRMTID_USER", 
    #                                                           expression="!IMMS_Unit_ID!", #+'-'+!COUNTY!+'-'+!REGION!+'-'+!IN_WUI!", 
    #                                                           expression_type="PYTHON3", 
    #                                                           code_block="", 
    #                                                           field_type="TEXT", 
    #                                                           enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate WUI (Calculate Field) (management)
    Updated_Input_Table_11_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_10_, 
                                                              field="IN_WUI", 
                                                              expression="ifelse(!WUI!)", 
                                                              expression_type="PYTHON3", 
                                                              code_block="""def ifelse(WUI):
                                                                    if WUI == \"Yes\":
                                                                        return \"WUI_USER_DEFINED\"
                                                                    elif WUI == \"No\":
                                                                        return \"NON-WUI_USER_DEFINED\"
                                                                    else:
                                                                        return WUI""", field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS"
                                                                    )

    # Process: Calculate Treatment Area (Calculate Field) (management)
    Updated_Input_Table_21_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_11_, 
                                                              field="TREATMENT_AREA", 
                                                              expression="ifelse(!Activity_Unit_of_Measure!, !Production_Quantity!)", 
                                                              expression_type="PYTHON3", 
                                                              code_block="""def ifelse(UOM, Q):
                                                                    if UOM == \"ACRE\":
                                                                        return Q
                                                                    else:
                                                                        return None""", field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Activity ID (Calculate Field) (management)
    Vegetation_Con_FeatureToPoin = arcpy.management.CalculateField(in_table=Updated_Input_Table_21_, 
                                                                   field="ACTIVID_USER", 
                                                                   expression="!Work_Order_Number!", 
                                                                   expression_type="PYTHON3", 
                                                                   code_block="", 
                                                                   field_type="TEXT", 
                                                                   enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Implementing Org (Calculate Field) (management)
    Updated_Input_Table_20_ = arcpy.management.CalculateField(in_table=Vegetation_Con_FeatureToPoin, 
                                                              field="IMPLEMENTING_ORG", 
                                                              expression="!IMMS_Unit_ID!", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Activity UOM (Calculate Field) (management)
    Updated_Input_Table_12_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_20_, 
                                                              field="ACTIVITY_UOM", 
                                                              expression="ifelse(!Activity_Unit_of_Measure!)", 
                                                              expression_type="PYTHON3", 
                                                              code_block="""def ifelse(Unit):
                                                                            if Unit == 'ACRE':
                                                                                return 'AC'
                                                                            else:
                                                                                return Unit""", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Activity Quantity (Calculate Field) (management)
    Updated_Input_Table_13_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_12_, 
                                                              field="ACTIVITY_QUANTITY", 
                                                              expression="!Production_Quantity!", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Status (Calculate Field) (management)
    Updated_Input_Table_15_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_13_, 
                                                              field="ACTIVITY_STATUS", 
                                                              expression="ifelse(!Act_Status!)", 
                                                              expression_type="PYTHON3", 
                                                              code_block="""def ifelse(Status):
                                                                        if Status == \"Complete\":
                                                                            return \"COMPLETE\"
                                                                        else:
                                                                            return Status""", field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Activity Start (Calculate Field) (management)
    Updated_Input_Table_22_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_15_, 
                                                              field="ACTIVITY_START", 
                                                              expression="!Start!", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Activity End (Calculate Field) (management)
    Updated_Input_Table_22a_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_22_, 
                                                              field="ACTIVITY_END", 
                                                              expression="!End_!", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Source (Calculate Field) (management)
    Updated_Input_Table_16_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_22a_, 
                                                              field="Source", 
                                                              expression="\"CALTRANS\"", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Crosswalk (Calculate Field) (management)
    Updated_Input_Table_17_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_16_, 
                                                              field="Crosswalk", 
                                                              expression="!Activity_Description_!", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Geometry Attributes (Calculate Geometry Attributes) (management)
    # CalTrans_pts_Copy_7_ = arcpy.management.CalculateGeometryAttributes(in_features=Updated_Input_Table_17_, 
    #                                                                     geometry_property=[["LATITUDE", "POINT_Y"], ["LONGITUDE", "POINT_X"]], 
    #                                                                     length_unit="", 
    #                                                                     area_unit="", 
    #                                                                     coordinate_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", 
    #                                                                     coordinate_format="DD")

    # Process: Delete Field (3) (Delete Field) (management)
    CalTrans_pts_Copy_16_ = KeepFields(Updated_Input_Table_17_)

    print(f'Saving Output Points Standardized: {output_points_standardized}')
    # Process: Copy Features (Copy Features) (management)
    arcpy.management.CopyFeatures(in_features=CalTrans_pts_Copy_16_, 
                                  out_feature_class=output_points_standardized, 
                                  config_keyword="", 
                                  spatial_grid_1=None, 
                                  spatial_grid_2=None, 
                                  spatial_grid_3=None)

    # Process: 2b Assign Domains (2b Assign Domains) (PC414CWIMillionAcres)
    usfs_silviculture_reforestation_enriched_20220629_2_ = AssignDomains(in_table=output_points_standardized)

    print('Performing Points Enrichments')
    # Process: 7b Enrichments pts (7b Enrichments pts) (PC414CWIMillionAcres)
    Pts_enrichment_Veg2 = os.path.join(scratch_workspace, "Pts_enrichment_Veg2")
    bEnrichmentsPoints(enrich_pts_out=output_points_enriched, 
                       enrich_pts_in=usfs_silviculture_reforestation_enriched_20220629_2_,
                       delete_scratch=True) # need to delete scratch here because we call bEnrichmentsPoints again for Line Enrichments and we'll catch a 'dataset already exists' error

    # Process: Copy Features (5) (Copy Features) (management)
    # arcpy.management.CopyFeatures(in_features=Pts_enrichment_Veg2, 
    #                               out_feature_class=output_points_enriched, 
    #                               config_keyword="", 
    #                               spatial_grid_1=None, 
    #                               spatial_grid_2=None, 
    #                               spatial_grid_3=None)

    # Process: Calculate Owner State (Calculate Field) (management)
    Updated_Input_Table_23_ = arcpy.management.CalculateField(in_table=output_points_enriched, 
                                                              field="PRIMARY_OWNERSHIP_GROUP", 
                                                              expression="\"STATE\"", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

        # Process: Calculate Treatment ID (Calculate Field) (management)
    Updated_Input_Table_X_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_23_, 
                                                              field="TREATMENT_ID_USER", 
                                                              expression="!PROJECTID_USER!+'-'+!COUNTY![:8]+'-'+!REGION![:3]+'-'+!IN_WUI![:3]", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: 2b Assign Domains (2) (2b Assign Domains) (PC414CWIMillionAcres)
    CalTrans_Activity_Points = AssignDomains(in_table=Updated_Input_Table_X_)



    ### BEGIN POLYLINE WORKFLOW
    print('Performing Line Standardization')
    # Process: Copy Features (2) (Copy Features) (management)
    CalTrans_pts_Copy_8_ = os.path.join(scratch_workspace, "CalTrans_pts_Copy")
    arcpy.management.CopyFeatures(in_features=input_polys, 
                                  out_feature_class=CalTrans_pts_Copy_8_, 
                                  config_keyword="", 
                                  spatial_grid_1=None, 
                                  spatial_grid_2=None, 
                                  spatial_grid_3=None)

    # Process: Repair Geometry (Repair Geometry) (management)
    CalTrans_pts_Copy_13_ = arcpy.management.RepairGeometry(in_features=CalTrans_pts_Copy_8_, 
                                                            delete_null="KEEP_NULL", 
                                                            validation_method="ESRI")

    # Process: Alter Field County (2) (Alter Field) (management)
    Updated_Input_Table_14_ = arcpy.management.AlterField(in_table=CalTrans_pts_Copy_13_, 
                                                          field="County", 
                                                          new_field_name="County2", 
                                                          new_field_alias="County2", 
                                                          field_type="TEXT", 
                                                          #field_length=25, 
                                                          #field_is_nullable="NULLABLE", 
                                                          clear_field_alias="DO_NOT_CLEAR")

    # Process: Alter Field Activity Description (2) (Alter Field) (management)
    Updated_Input_Table_24_ = arcpy.management.AlterField(in_table=Updated_Input_Table_14_, 
                                                          field="Activity_Description", 
                                                          new_field_name="Activity_Description_", 
                                                          new_field_alias="", 
                                                          field_type="TEXT", 
                                                          #field_length=70, 
                                                          #field_is_nullable="NULLABLE", 
                                                          clear_field_alias="DO_NOT_CLEAR")

    # Process: Alter Field Veg (2) (Alter Field) (management)
    CalTrans_pts_Copy_9_ = arcpy.management.AlterField(in_table=Updated_Input_Table_24_, 
                                                       field="Broad_Vegetation_Type", 
                                                       new_field_name="BVT", 
                                                       new_field_alias="", 
                                                       field_type="TEXT", 
                                                       #field_length=50, 
                                                       #field_is_nullable="NULLABLE", 
                                                       clear_field_alias="DO_NOT_CLEAR")

    # Process: Alter Field Activity Status (2) (Alter Field) (management)
    Updated_Input_Table_25_ = arcpy.management.AlterField(in_table=CalTrans_pts_Copy_9_, 
                                                          field="Activity_Status", 
                                                          new_field_name="Act_Status", 
                                                          new_field_alias="", 
                                                          field_type="TEXT", 
                                                          #field_length=25, 
                                                          #field_is_nullable="NULLABLE", 
                                                          clear_field_alias="DO_NOT_CLEAR")

    # Process: Alter Activity Quantity (2) (Alter Field) (management)
    Updated_Input_Table_26_ = arcpy.management.AlterField(in_table=Updated_Input_Table_25_, 
                                                          field="Activity_Quantity", 
                                                          new_field_name="Production_Quantity", 
                                                          new_field_alias="", 
                                                          field_type="DOUBLE", 
                                                          #field_length=8, 
                                                          #field_is_nullable="NULLABLE", 
                                                          clear_field_alias="DO_NOT_CLEAR")

    # Process: Alter Field Residue Fate (2) (Alter Field) (management)
    CalTrans_pts_Copy_10_ = arcpy.management.AlterField(in_table=Updated_Input_Table_26_, 
                                                        field="Residue_Fate", 
                                                        new_field_name="Fate", 
                                                        new_field_alias="", 
                                                        field_type="TEXT", 
                                                        #field_length=35, 
                                                        #field_is_nullable="NULLABLE", 
                                                        clear_field_alias="DO_NOT_CLEAR")

    # Process: Alter Field Fate Units (2) (Alter Field) (management)
    Updated_Input_Table_27_ = arcpy.management.AlterField(in_table=CalTrans_pts_Copy_10_, 
                                                          field="Residue_Fate_Units", 
                                                          new_field_name="FateUnits", 
                                                          new_field_alias="", 
                                                          field_type="TEXT", 
                                                          #field_length=5, 
                                                          #field_is_nullable="NULLABLE", 
                                                          clear_field_alias="DO_NOT_CLEAR")

    # Process: Alter Residue Quantity (2) (Alter Field) (management)
    CalTrans_pts_Copy_11_ = arcpy.management.AlterField(in_table=Updated_Input_Table_27_, 
                                                        field="Residue_Fate_Quantity", 
                                                        new_field_name="FateQuantity", 
                                                        new_field_alias="", 
                                                        field_type="DOUBLE", 
                                                        #field_length=8, 
                                                        #field_is_nullable="NULLABLE", 
                                                        clear_field_alias="DO_NOT_CLEAR")

    # Process: 1b Add Fields (2) (1b Add Fields) (PC414CWIMillionAcres)
    WFRTF_Template_2_ = AddFields2(Input_Table=CalTrans_pts_Copy_11_)

    # Process: Calculate Project ID (2) (Calculate Field) (management)
    Updated_Input_Table_28_ = arcpy.management.CalculateField(in_table=WFRTF_Template_2_, 
                                                              field="PROJECTID_USER", 
                                                              expression="!HighwayID!", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Agency (2) (Calculate Field) (management)
    Updated_Input_Table_29_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_28_, 
                                                              field="AGENCY", 
                                                              expression="\"CALSTA\"", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Data Steward (2) (Calculate Field) (management)
    Updated_Input_Table_30_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_29_, 
                                                              field="ORG_ADMIN_p", 
                                                              expression="\"CALTRANS\"", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Project Contact (2) (Calculate Field) (management)
    Updated_Input_Table_31_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_30_, 
                                                              field="PROJECT_CONTACT", 
                                                              expression="\"Division of Maintenance\"", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Email (2) (Calculate Field) (management)
    Updated_Input_Table_32_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_31_, 
                                                              field="PROJECT_EMAIL", 
                                                              expression="\"andrew.lozano@dot.ca.gov\"", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Admin Org (2) (Calculate Field) (management)
    CalTrans_pts_Copy_12_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_32_, 
                                                            field="ADMINISTERING_ORG", 
                                                            expression="!District!", 
                                                            expression_type="PYTHON3", 
                                                            code_block="", 
                                                            field_type="TEXT", 
                                                            enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Primary Funding Source (2) (Calculate Field) (management)
    Updated_Input_Table_33_ = arcpy.management.CalculateField(in_table=CalTrans_pts_Copy_12_, 
                                                              field="PRIMARY_FUNDING_SOURCE", 
                                                              expression="\"GENERAL_FUND\"", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Primary Funding Org (2) (Calculate Field) (management)
    Updated_Input_Table_34_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_33_, 
                                                              field="PRIMARY_FUNDING_ORG", 
                                                              expression="\"CALTRANS\"", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Treatment ID (2) (Calculate Field) (management)
    # Updated_Input_Table_46_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_34_, 
    #                                                           field="TRMTID_USER", 
    #                                                           expression="!IMMS_ID!", #+'-'+!COUNTY!+'-'+!REGION!"+'-'+!IN_WUI!", 
    #                                                           expression_type="PYTHON3", 
    #                                                           code_block="", 
    #                                                           field_type="TEXT", 
    #                                                           enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate WUI (2) (Calculate Field) (management)
    Updated_Input_Table_36_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_34_, 
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
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Treatment Area (2) (Calculate Field) (management)
    Updated_Input_Table_37_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_36_, 
                                                              field="TREATMENT_AREA", 
                                                              expression="ifelse(!Activity_Unit_of_Measure!, !Production_Quantity!)", 
                                                              expression_type="PYTHON3", 
                                                              code_block="""def ifelse(UOM, Q):
                                                                if UOM == \"ACRE\":
                                                                    return Q
                                                                else:
                                                                    return None""", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Activity ID (2) (Calculate Field) (management)
    Vegetation_Con_FeatureToPoin_2_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_37_, 
                                                                      field="ACTIVID_USER", 
                                                                      expression="!Work_Order_Number!", 
                                                                      expression_type="PYTHON3", 
                                                                      code_block="", 
                                                                      field_type="TEXT", 
                                                                      enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Implementing Org (2) (Calculate Field) (management)
    Updated_Input_Table_35_ = arcpy.management.CalculateField(in_table=Vegetation_Con_FeatureToPoin_2_, 
                                                              field="IMPLEMENTING_ORG", 
                                                              expression="!IMMS_ID!", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Activity UOM (2) (Calculate Field) (management)
    Updated_Input_Table_38_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_35_, 
                                                              field="ACTIVITY_UOM", 
                                                              expression="ifelse(!Activity_Unit_of_Measure!)", 
                                                              expression_type="PYTHON3", 
                                                              code_block="""def ifelse(Unit):
                                                                            if Unit == 'ACRE':
                                                                                return 'AC'
                                                                            else:
                                                                                return Unit""", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Activity Quantity (2) (Calculate Field) (management)
    Updated_Input_Table_39_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_38_, 
                                                              field="ACTIVITY_QUANTITY", 
                                                              expression="!Production_Quantity!", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Status (2) (Calculate Field) (management)
    Updated_Input_Table_40_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_39_, 
                                                              field="ACTIVITY_STATUS", 
                                                              expression="ifelse(!Act_Status!)", 
                                                              expression_type="PYTHON3", 
                                                              code_block="""def ifelse(Status):
                                                                if Status == \"Complete\":
                                                                    return \"COMPLETE\"
                                                                else:
                                                                    return Status""", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Activity Start (2) (Calculate Field) (management)
    Updated_Input_Table_41_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_40_, 
                                                              field="ACTIVITY_START", 
                                                              expression="!Start!", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")
                                                              
    # Process: Calculate Activity End (2) (Calculate Field) (management)
    Updated_Input_Table_41a_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_41_, 
                                                              field="ACTIVITY_END", 
                                                              expression="!End_!", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Source (2) (Calculate Field) (management)
    Updated_Input_Table_42_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_41a_, 
                                                              field="Source", 
                                                              expression="\"CALTRANS\"", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Crosswalk (2) (Calculate Field) (management)
    Updated_Input_Table_43_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_42_, 
                                                              field="Crosswalk", 
                                                              expression="!Activity_Description_!", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Geometry Attributes (2) (Calculate Geometry Attributes) (management)
    # CalTrans_pts_Copy_15_ = arcpy.management.CalculateGeometryAttributes(in_features=Updated_Input_Table_43_, 
    #                                                                      geometry_property=[["LATITUDE", "INSIDE_Y"], ["LONGITUDE", "INSIDE_X"]], 
    #                                                                      length_unit="", 
    #                                                                      area_unit="", 
    #                                                                      coordinate_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", 
    #                                                                      coordinate_format="DD")

    # Process: Delete Field (2) (Delete Field) (management)
    CalTrans_pts_Copy_14_ = KeepFields(Updated_Input_Table_43_)

    print(f'Saving Output Lines Standardized: {output_lines_standardized}')
    # Process: Copy Features (3) (Copy Features) (management)
    arcpy.management.CopyFeatures(in_features=CalTrans_pts_Copy_14_, 
                                  out_feature_class=output_lines_standardized, 
                                  config_keyword="", 
                                  spatial_grid_1=None, 
                                  spatial_grid_2=None, 
                                  spatial_grid_3=None)

    # Process: 2b Assign Domains (3) (2b Assign Domains) (PC414CWIMillionAcres)
    usfs_silviculture_reforestation_enriched_20220629_3_ = AssignDomains(in_table=output_lines_standardized)

    print('Performing Lines Enrichments')
    # Process: 7c Enrichments Lines (2) (7c Enrichments Lines) (PC414CWIMillionAcres)
    Line_Enriched_Temp_CopyFeatures_3_ = cEnrichmentsLines(line_fc=usfs_silviculture_reforestation_enriched_20220629_3_) # don't delete scratch

    print(f'Saving Output Lines Enriched: {output_lines_enriched}')
    # Process: Copy Features (4) (Copy Features) (management)
    arcpy.management.CopyFeatures(in_features=Line_Enriched_Temp_CopyFeatures_3_, 
                                  out_feature_class=output_lines_enriched, 
                                  config_keyword="", 
                                  spatial_grid_1=None, 
                                  spatial_grid_2=None, 
                                  spatial_grid_3=None)

    # Process: Calculate Owner State (2) (Calculate Field) (management)
    Updated_Input_Table_44_ = arcpy.management.CalculateField(in_table=output_lines_enriched, 
                                                              field="PRIMARY_OWNERSHIP_GROUP", 
                                                              expression="\"STATE\"", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")
    
    ## *** IMMS_Unit_ID and IMMS_ID no longer exist after running a 7 tool on the data, so changed to 'TREATMENT_ID_USER' since that was filled with IMMS 
    ## *** prior to the 7 tool being ran. Get non-specific error (no line traceback) that nontypes and string types cannot be concatenated when 
    ## *** running the script with this block of code intact. The output table "Updated_Input_Table_Y_" should be fed into AssignDomains below once functioning.
    # Process: Calculate Treatment ID (2) (Calculate Field) (management)
    Updated_Input_Table_Y_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_44_, 
                                                              field="TREATMENT_ID_USER", 
                                                              expression="!PROJECTID_USER!+'-'+!COUNTY![:8]+'-'+!REGION![:3]+'-'+!IN_WUI![:3]", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: 2b Assign Domains (4) (2b Assign Domains) (PC414CWIMillionAcres)
    CalTrans_Activity_Points_2_ = AssignDomains(in_table=Updated_Input_Table_Y_)

    print('Deleting Scratch Files')
    delete_scratch_files(gdb = scratch_workspace, delete_fc = 'yes', delete_table = 'yes', delete_ds = 'yes')

    end = time.time()
    print(f'Time Elapsed: {(end-start)/60} minutes')
if __name__ == '__main__':
     runner(workspace,scratch_workspace,CalTrans, '*argv[1:]')
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
