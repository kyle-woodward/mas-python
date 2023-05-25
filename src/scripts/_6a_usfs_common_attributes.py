import arcpy
from ._1b_add_fields import AddFields2
from ._2b_assign_domains import AssignDomains
from ._7a_enrichments_polygon import aEnrichmentsPolygon1
from ._2k_keep_fields import KeepFields
from sys import argv
from .utils import init_gdb, delete_scratch_files, runner
import os
import time
original_gdb, workspace, scratch_workspace = init_gdb()

def Model_USFS(output_enriched, output_standardized, input_fc):
    start = time.time()
    print(f'Start Time {time.ctime()}')
    arcpy.env.overwriteOutput = True
    

    # define intermediary objects in scratch
    Output_Feature_Class = os.path.join(scratch_workspace,'Actv_CommonAttribute_PL_Laye_CopyFeatures')
    usfs_haz_fuels_treatments_reduction2_dissolve = os.path.join(scratch_workspace,'usfs_haz_fuels_treatments_reduction2_dissolve')
    Actv_CommonAttribute_PL_Laye_CopyFeatures2 = os.path.join(scratch_workspace,'Actv_CommonAttribute_PL_Laye_CopyFeatures2')
    

    # Model Environment settings
    with arcpy.EnvManager(outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]"""):
        print('Performing Standardization...')
        # Process: Select Layer By Attribute California (Select Layer By Attribute) (management)
        Actv_CommonAttribute_PL_Laye2, Count_4_ = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=input_fc, 
            selection_type="NEW_SELECTION", 
            where_clause="STATE_ABBR = 'CA'", 
            invert_where_clause=""
            )
        
        print("   Selecting Features...")
        # Process: Select Layer By Attribute Activity Code (Select Layer By Attribute) (management)
        Actv_CommonAttribute_PL_Laye2_2_, Count_3_ = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=Actv_CommonAttribute_PL_Laye2, 
            selection_type="SUBSET_SELECTION", 
            where_clause="""ACTIVITY_CODE = '1102' Or 
                            ACTIVITY_CODE = '1111' Or
                            ACTIVITY_CODE = '1112' Or
                            ACTIVITY_CODE = '1113' Or
                            ACTIVITY_CODE = '1115' Or
                            ACTIVITY_CODE = '1116' Or
                            ACTIVITY_CODE = '1117' Or
                            ACTIVITY_CODE = '1118' Or
                            ACTIVITY_CODE = '1119' Or
                            ACTIVITY_CODE = '1120' Or
                            ACTIVITY_CODE = '1130' Or
                            ACTIVITY_CODE = '1136' Or
                            ACTIVITY_CODE = '1139' Or
                            ACTIVITY_CODE = '1150' Or
                            ACTIVITY_CODE = '1152' Or
                            ACTIVITY_CODE = '1153' Or
                            ACTIVITY_CODE = '1154' Or
                            ACTIVITY_CODE = '1160' Or
                            ACTIVITY_CODE = '1180' Or
                            ACTIVITY_CODE = '2000' Or
                            ACTIVITY_CODE = '2341' Or
                            ACTIVITY_CODE = '2360' Or
                            ACTIVITY_CODE = '2370' Or
                            ACTIVITY_CODE = '2510' Or
                            ACTIVITY_CODE = '2530' Or
                            ACTIVITY_CODE = '2540' Or
                            ACTIVITY_CODE = '2560' Or
                            ACTIVITY_CODE = '3132' Or
                            ACTIVITY_CODE = '4101' Or
                            ACTIVITY_CODE = '4102' Or
                            ACTIVITY_CODE = '4111' Or
                            ACTIVITY_CODE = '4113' Or
                            ACTIVITY_CODE = '4115' Or
                            ACTIVITY_CODE = '4117' Or
                            ACTIVITY_CODE = '4121' Or
                            ACTIVITY_CODE = '4122' Or
                            ACTIVITY_CODE = '4131' Or
                            ACTIVITY_CODE = '4132' Or
                            ACTIVITY_CODE = '4141' Or
                            ACTIVITY_CODE = '4142' Or
                            ACTIVITY_CODE = '4143' Or
                            ACTIVITY_CODE = '4145' Or
                            ACTIVITY_CODE = '4146' Or
                            ACTIVITY_CODE = '4148' Or
                            ACTIVITY_CODE = '4151' Or
                            ACTIVITY_CODE = '4152' Or
                            ACTIVITY_CODE = '4162' Or
                            ACTIVITY_CODE = '4162' Or
                            ACTIVITY_CODE = '4175' Or
                            ACTIVITY_CODE = '4177' Or
                            ACTIVITY_CODE = '4183' Or
                            ACTIVITY_CODE = '4192' Or
                            ACTIVITY_CODE = '4193' Or
                            ACTIVITY_CODE = '4194' Or
                            ACTIVITY_CODE = '4196' Or
                            ACTIVITY_CODE = '4210' Or
                            ACTIVITY_CODE = '4211' Or
                            ACTIVITY_CODE = '4220' Or
                            ACTIVITY_CODE = '4231' Or
                            ACTIVITY_CODE = '4232' Or
                            ACTIVITY_CODE = '4241' Or
                            ACTIVITY_CODE = '4242' Or
                            ACTIVITY_CODE = '4250' Or
                            ACTIVITY_CODE = '4270' Or
                            ACTIVITY_CODE = '4280' Or
                            ACTIVITY_CODE = '4290' Or
                            ACTIVITY_CODE = '4291' Or
                            ACTIVITY_CODE = '4382' Or
                            ACTIVITY_CODE = '4411' Or
                            ACTIVITY_CODE = '4412' Or
                            ACTIVITY_CODE = '4431' Or
                            ACTIVITY_CODE = '4432' Or
                            ACTIVITY_CODE = '4455' Or
                            ACTIVITY_CODE = '4471' Or
                            ACTIVITY_CODE = '4472' Or
                            ACTIVITY_CODE = '4473' Or
                            ACTIVITY_CODE = '4474' Or
                            ACTIVITY_CODE = '4475' Or
                            ACTIVITY_CODE = '4481' Or
                            ACTIVITY_CODE = '4482' Or
                            ACTIVITY_CODE = '4483' Or
                            ACTIVITY_CODE = '4484' Or
                            ACTIVITY_CODE = '4485' Or
                            ACTIVITY_CODE = '4490' Or
                            ACTIVITY_CODE = '4491' Or
                            ACTIVITY_CODE = '4492' Or
                            ACTIVITY_CODE = '4493' Or
                            ACTIVITY_CODE = '4494' Or
                            ACTIVITY_CODE = '4495' Or
                            ACTIVITY_CODE = '4511' Or
                            ACTIVITY_CODE = '4521' Or
                            ACTIVITY_CODE = '4530' Or
                            ACTIVITY_CODE = '4540' Or
                            ACTIVITY_CODE = '4541' Or
                            ACTIVITY_CODE = '4550' Or
                            ACTIVITY_CODE = '4580' Or
                            ACTIVITY_CODE = '6101' Or
                            ACTIVITY_CODE = '6103' Or
                            ACTIVITY_CODE = '6104' Or
                            ACTIVITY_CODE = '6105' Or
                            ACTIVITY_CODE = '6106' Or
                            ACTIVITY_CODE = '6107' Or
                            ACTIVITY_CODE = '6133' Or
                            ACTIVITY_CODE = '6584' Or
                            ACTIVITY_CODE = '6684' Or
                            ACTIVITY_CODE = '7015' Or
                            ACTIVITY_CODE = '7050' Or
                            ACTIVITY_CODE = '7065' Or
                            ACTIVITY_CODE = '7067' Or
                            ACTIVITY_CODE = '9008' Or
                            ACTIVITY_CODE = '9400'""", invert_where_clause="")

        # Process: Select Layer By Attribute Non-Wildfire (Select Layer By Attribute) (management)
        usfs_haz_fuels_treatments_re, Count_6_ = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=Actv_CommonAttribute_PL_Laye2_2_, 
            selection_type="SUBSET_SELECTION", 
            where_clause="ACTIVITY_CODE = '1117' And FUELS_KEYPOINT_AREA <> '6'", 
            invert_where_clause="INVERT"
            )
        
        # Process: Select Layer By Attribute Non-Wildfire (Select Layer By Attribute) (management)
        usfs_haz_fuels_treatments_re, Count_6a_ = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=Actv_CommonAttribute_PL_Laye2_2_, 
            selection_type="SUBSET_SELECTION", 
            where_clause="ACTIVITY_CODE = '1117' And FUELS_KEYPOINT_AREA IS NULL", 
            invert_where_clause="INVERT"
            )

        # Process: Select Layer By Attribute Non-Wildfire (Select Layer By Attribute) (management)
        usfs_haz_fuels_treatments_re2, Count_6b_ = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=usfs_haz_fuels_treatments_re, 
            selection_type="SUBSET_SELECTION", 
            where_clause="ACTIVITY_CODE = '1119' And FUELS_KEYPOINT_AREA <> '6'", 
            invert_where_clause="INVERT"
            )
        
        # Process: Select Layer By Attribute Non-Wildfire (Select Layer By Attribute) (management)
        usfs_haz_fuels_treatments_re3, Count_6c_ = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=usfs_haz_fuels_treatments_re2, 
            selection_type="SUBSET_SELECTION", 
            where_clause="ACTIVITY_CODE = '1119' And FUELS_KEYPOINT_AREA IS NULL", 
            invert_where_clause="INVERT"
            )

        # Process: Select Layer By Attribute Date is not NULL (Select Layer By Attribute) (management)
        Actv_CommonAttribute_PL_Laye2_4_, Count_7_ = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=usfs_haz_fuels_treatments_re3, 
            selection_type="SUBSET_SELECTION", 
            where_clause="DATE_COMPLETED IS NULL And DATE_AWARDED IS NULL And NEPA_SIGNED_DATE IS NULL", 
            invert_where_clause="INVERT"
            )
        
        # Process: Select Layer By Attribute Date (Select Layer By Attribute) (management)
        Actv_CommonAttribute_PL_Laye2_4_1, Count_7_ = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=Actv_CommonAttribute_PL_Laye2_4_, 
            selection_type="SUBSET_SELECTION", 
            where_clause="DATE_COMPLETED > timestamp '1995-01-01 00:00:00' Or DATE_COMPLETED IS NULL", 
            invert_where_clause=""
            )
        
        # Process: Copy Features (2) (Copy Features) (management)
        usfs_haz_fuels_treatments_reduction2_Select2_2_2 = arcpy.management.CopyFeatures(
            Actv_CommonAttribute_PL_Laye2_4_1, 
            Output_Feature_Class
            )
        
        print("   Repairing Geometry...")
        # Process: Repair Geometry (Repair Geometry) (management)
        usfs_haz_fuels_treatments_reduction2_Select2_2_ = arcpy.management.RepairGeometry(
            in_features=usfs_haz_fuels_treatments_reduction2_Select2_2_2, 
            delete_null="KEEP_NULL", 
            validation_method="ESRI"
            )

        # Process: Dissolve (Dissolve) (management)
        usfs_haz_fuels_treatments_reduction2_Select2_2_2_3 = arcpy.management.Dissolve(
            in_features=usfs_haz_fuels_treatments_reduction2_Select2_2_, 
            out_feature_class=usfs_haz_fuels_treatments_reduction2_dissolve, 
            dissolve_field=["SUID", "NEPA_SIGNED_DATE", "DATE_COMPLETED", 
                            "NBR_UNITS_ACCOMPLISHED", "FACTS_ID", "UOM", 
                            "ACTIVITY", "NEPA_PROJECT_NAME", "DATE_AWARDED", 
                            "ACTIVITY_CODE", "NEPA_DOC_NBR", "WORKFORCE_CODE", 
                            "NBR_UNITS_PLANNED", "ISWUI"], 
            statistics_fields=[], 
            multi_part="MULTI_PART", 
            unsplit_lines="DISSOLVE_LINES", 
            concatenation_separator=""
            )

        print("   Adding Fields...")
        # Process: 1b Add Fields (1b Add Fields) (PC414CWIMillionAcres)
        WFRTF_Template_4_ = AddFields2(Input_Table=usfs_haz_fuels_treatments_reduction2_Select2_2_2_3)

        print("   Transfering Attributes...")
        # Process: Calculate Project ID (Calculate Field) (management)
        Activity_SilvTSI_20220627_Se2_2_ = arcpy.management.CalculateField(
            in_table=WFRTF_Template_4_, 
            field="PROJECTID_USER", 
            expression="!NEPA_DOC_NBR!", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Agency (Calculate Field) (management)
        Updated_Input_Table_30_ = arcpy.management.CalculateField(
            in_table=Activity_SilvTSI_20220627_Se2_2_, 
            field="AGENCY", 
            expression="\"USDA\"", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Data Steward (Calculate Field) (management)
        Updated_Input_Table = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_30_, 
            field="ORG_ADMIN_p", 
            expression="\"USFS\"", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Project Contact (Calculate Field) (management)
        Updated_Input_Table_3_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table, 
            field="PROJECT_CONTACT", 
            expression="\"Tawndria Melville\"", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Project Email (Calculate Field) (management)
        Updated_Input_Table_5_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_3_, 
            field="PROJECT_EMAIL", 
            expression="\"tawndria.melville@usda.gov\"", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Admin Org (Calculate Field) (management)
        Updated_Input_Table_31_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_5_, 
            field="ADMINISTERING_ORG", 
            expression="\"USFS\"", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )
       
        # Process: Calculate Project Name (Calculate Field) (management)
        # Updated_Input_Table_33_ = arcpy.management.CalculateField(
        #     in_table=Updated_Input_Table_31_, 
        #     field="PROJECT_NAME", 
        #     expression="\"None\"", # "NONE"
        #     expression_type="PYTHON3", 
        #     code_block="", 
        #     field_type="TEXT", 
        #     enforce_domains="NO_ENFORCE_DOMAINS"
        #     )

        # Process: Calculate Fund Source (Calculate Field) (management)
        Updated_Input_Table_6_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_31_, 
            field="PRIMARY_FUNDING_SOURCE", 
            expression="\"USFS\"", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Fund Org (Calculate Field) (management)
        Updated_Input_Table_7_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_6_, 
            field="PRIMARY_FUNDING_ORG", 
            expression="\"USFS\"", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Imp Org (Calculate Field) (management)
        Updated_Input_Table_32_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_7_, 
            field="IMPLEMENTING_ORG", 
            expression="\"Pacific Southwest Regional Office\"", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Treatment ID (Calculate Field) (management) after enrichment
        
        # Process: Calculate Data Steward 2 (Calculate Field) (management)
        Updated_Input_Table_8_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_32_, 
            field="ORG_ADMIN_t", 
            expression="\"USFS\"", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Activity User ID (Calculate Field) (management)
        Updated_Input_Table_8a_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_8_, 
            field="ACTIVID_USER", 
            expression="!SUID!", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Veg User Defined (Calculate Field) (management)
        Updated_Input_Table_9_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_8a_, 
            field="BVT_USERD", 
            expression="\"NO\"", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate WUI (Calculate Field) (management)
        Updated_Input_Table_2a_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_9_, 
            field="IN_WUI", 
            expression="ifelse(!ISWUI!)", 
            expression_type="PYTHON3", 
            code_block="""def ifelse(WUI):
                            if WUI == \"Y\":
                                return \"WUI_USER_DEFINED\"
                            elif WUI == \"N\":
                                return \"NON-WUI_USER_DEFINED\"
                            else:
                                return None""", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        print("   Calculating End Date...")
        # Process: Calculate Activity End Date (Calculate Field) (management)
        Updated_Input_Table_2_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_2a_, 
            field="ACTIVITY_END", 
            expression="ifelse(!DATE_COMPLETED!, !DATE_AWARDED!)", 
            expression_type="PYTHON3", 
            code_block="""def ifelse(DateComp, DateAw):
                            if DateComp != None:
                                return DateComp
                            elif DateComp == None:
                                return DateAw""", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
        usfs_haz_fuels_treatments_re_3_, Count = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=Updated_Input_Table_2_, 
            selection_type="NEW_SELECTION", 
            where_clause="ACTIVITY_END IS NULL", 
            invert_where_clause=""
            )

        # Process: Calculate Activity End Date (4) (Calculate Field) (management)
        Updated_Input_Table_4_ = arcpy.management.CalculateField(
            in_table=usfs_haz_fuels_treatments_re_3_, 
            field="ACTIVITY_END", 
            expression="!NEPA_SIGNED_DATE!", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Select Layer By Attribute (2) (Select Layer By Attribute) (management)
        usfs_silviculture_TSI_dissol_2_, Count_2_ = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=Updated_Input_Table_4_, 
            selection_type="CLEAR_SELECTION", 
            where_clause="", 
            invert_where_clause=""
            )

        print("   Calculating Status...")
        # Process: Calculate Status (Calculate Field) (management)
        # Based on Today's Date.  Need to add Date formula
        Updated_Input_Table_35_ = arcpy.management.CalculateField(
            in_table=usfs_silviculture_TSI_dissol_2_, 
            field="ACTIVITY_STATUS", 
            expression="ifelse(!DATE_COMPLETED!, !DATE_AWARDED!, !NEPA_SIGNED_DATE!)", 
            expression_type="PYTHON3", 
            code_block="""def ifelse(DateComp, DateAw, DatePl):
                            if DateComp != None:
                                return \"COMPLETE\"
                            elif DateAw != None:
                                return \"ACTIVE\"
                            elif DatePl >= datetime.datetime(2024, 10, 15):
                                return \"OUTYEAR\"
                            elif DatePl >= datetime.datetime(2012, 10, 15):
                                return \"PLANNED\"
                            else:
                                return \"CANCELLED\"""",
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Activity Quantity (3) (Calculate Field) (management)
        Activity_SilvTSI_20220627_Se2_6_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_35_, 
            field="ACTIVITY_QUANTITY", 
            expression="ifelse(!NBR_UNITS_ACCOMPLISHED!, !NBR_UNITS_PLANNED!)", 
            expression_type="PYTHON3", 
            code_block="""def ifelse(ACC, PLANNED):
                            if ACC != None:
                                return ACC
                            if ACC == None:
                                return PLANNED""", 
            field_type="DOUBLE", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Activity UOM (3) (Calculate Field) (management)
        Activity_SilvTSI_20220627_Se2_5_ = arcpy.management.CalculateField(
            in_table=Activity_SilvTSI_20220627_Se2_6_, 
            field="ACTIVITY_UOM", 
            expression="!UOM!", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Admin Org2 (Calculate Field) (management)
        Updated_Input_Table_10_ = arcpy.management.CalculateField(
            in_table=Activity_SilvTSI_20220627_Se2_5_, 
            field="ADMIN_ORG_NAME", 
            expression="\"USFS\"", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Implementation Org 2 (Calculate Field) (management)
        Updated_Input_Table_11_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_10_, 
            field="IMPLEM_ORG_NAME", 
            expression="!WORKFORCE_CODE!", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Primary Fund Source (Calculate Field) (management)
        Updated_Input_Table_12_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_11_, 
            field="PRIMARY_FUND_SRC_NAME", 
            expression="\"USFS\"", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Fund Org 2 (Calculate Field) (management)
        Updated_Input_Table_13_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_12_, 
            field="PRIMARY_FUND_ORG_NAME", 
            expression="\"USFS\"", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )
        
        # Process: Calculate Activity Name (Calculate Field) (management)
        Updated_Input_Table_14_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_13_, 
            field="ACTIVITY_NAME", 
            expression="None", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Source (Calculate Field) (management)
        Updated_Input_Table_36_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_14_, 
            field="Source", 
            expression="\"usfs_treatments\"", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Year (Calculate Field) (management)
        Updated_Input_Table_15_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_36_, 
            field="Year", 
            expression="Year($feature.ACTIVITY_END)", 
            expression_type="ARCADE", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )

        # Process: Calculate Crosswalk (Calculate Field) (management)
        Updated_Input_Table_39_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_15_, 
            field="Crosswalk", 
            expression="ifelse(!ACTIVITY!)", 
            expression_type="PYTHON3", 
            code_block="""def ifelse(Act):
                            if Act == \"Piling of Fuels, Hand or Machine \":
                                return \"Piling of Fuels, Hand or Machine\"
                            else:
                                return Act""", 
            field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")
        
        # Process: Treatment Geometry (Calculate Field) (management)
        Updated_Input_Table_40_ = arcpy.management.CalculateField(
            in_table=Updated_Input_Table_39_, 
            field="TRMT_GEOM", 
            expression="ifelse(!ACTIVITY!)", 
            expression_type="PYTHON3", 
            code_block="""def ifelse(Geom):
                            if Geom == \'A\':
                                return \'POLYGON\'
                            elif Geom == \'L\':
                                return \'LINE\'
                            elif Geom == \'P\':
                                return \'POINT\'
                            else: 
                                return Geom""", 
            field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")
        

        # Process: Calculate USFS Activity Code (Calculate Field) (management)
        Updated_Input_Table_41_ = arcpy.management.CalculateField(
           in_table=Updated_Input_Table_40_, 
           field="Act_Code", 
           expression="!ACTIVITY_CODE!", 
           expression_type="PYTHON3",
           code_block="", 
           field_type="TEXT", 
           enforce_domains="NO_ENFORCE_DOMAINS"
           )

        # Process: Copy Features (Copy Features) (management)
        arcpy.management.CopyFeatures(
            in_features=Updated_Input_Table_41_, 
            out_feature_class=Actv_CommonAttribute_PL_Laye_CopyFeatures2 
            )

        # Process: Delete Field (Delete Field) (management)
        usfs_haz_fuels_treatments_re_2_ = KeepFields(Actv_CommonAttribute_PL_Laye_CopyFeatures2)

        print(f'Saving Output Standardized: {output_standardized}')
        # Process: Select by Years (Select) (analysis)
        arcpy.analysis.Select(
            in_features=usfs_haz_fuels_treatments_re_2_, 
            out_feature_class=output_standardized, 
            where_clause="Year >= 1995 And Year <= 2025"
            )

        # Process: 2b Assign Domains (2b Assign Domains) (PC414CWIMillionAcres)
        usfs_silviculture_reforestation_enriched_20220629_2a_ = AssignDomains(
            in_table=output_standardized
            )

        # print("Enriching Dataset")
        # Process: 7a Enrichments Polygon (2) (7a Enrichments Polygon) (PC414CWIMillionAcres)
        aEnrichmentsPolygon1(
            enrich_in=usfs_silviculture_reforestation_enriched_20220629_2a_,
            enrich_out=output_enriched            
            )
        
        print(f'Saving Output Enriched: {output_enriched}')
        # output of enrichemnts function should be the output_enriched file not another scratch file, then we can delete all scratch files
        # Process: Copy Features (Copy Features) (management)
        # arcpy.management.CopyFeatures(
        #     in_features=Veg_Summarized_Polygons2_3_, 
        #     out_feature_class=output_enriched, 
        #     )

        arcpy.management.CalculateField(
            in_table=output_enriched, 
            field="TRMTID_USER", 
            expression="!ACTIVID_USER!+'-'+!PRIMARY_OBJECTIVE![:8]", 
            expression_type="PYTHON3", 
            code_block="", 
            field_type="TEXT", 
            enforce_domains="NO_ENFORCE_DOMAINS"
            )
        
        # Process: 2b Assign Domains (2) (2b Assign Domains) (PC414CWIMillionAcres)
        AssignDomains(
            in_table=output_enriched
            )
        
        # print('   Deleting Scratch Files')
        delete_scratch_files(gdb = scratch_workspace, delete_fc = 'yes', delete_table = 'yes', delete_ds = 'yes')
        
        end = time.time()
        print(f'Time Elapsed: {(end-start)/60} minutes')
        
if __name__ == '__main__':
     runner(workspace,scratch_workspace,Model_USFS, '*argv[1:]')
    # # Global Environment settings
    #  with arcpy.EnvManager(
    #     overwriteOutput=True,
    #     extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""",  outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""", 
    #     preserveGlobalIds=True, 
    #     qualifiedFieldNames=False, 
    #     scratchWorkspace=scratch_workspace, 
    #     transferDomains=True, 
    #     transferGDBAttributeProperties=True, 
    #     workspace=workspace):
    #         Model_USFS(*argv[1:])
