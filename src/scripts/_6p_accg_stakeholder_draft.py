import arcpy
import os
from sys import argv
from .utils import init_gdb, delete_scratch_files, runner
from ._2k_keep_fields import KeepFields
import time
original_gdb, workspace, scratch_workspace = init_gdb()

def pACCGStakeholderDraft(input_fc,output_standardized):  # 6p_ACCG_Stakeholder-Draft
    start = time.time()
    print(f'Start Time {time.ctime()}')
    arcpy.env.overwriteOutput = True

    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")

    # _scratchgdb_ = f"{arcpy.env.scratchGDB}" replaced with "scratch_workspace"
    Fuels_Treatments_Piles_Crosswalk = os.path.join(workspace, "Fuels_Treatments_Piles_Crosswalk")
    # PC414_CWI_Million_Acres_gdb = "C:\\Users\\sageg\\SIG Dropbox\\Carl Rudeen\\PC414 Million Acre\\PC414 CWI Million Acres.gdb" replaced with "workspace"
    California_2_ = os.path.join(workspace, "b_Reference", "California")

    # Process: Table To Table (Table To Table) (conversion)
    ACCG_Project_table = arcpy.conversion.TableToTable(in_rows=input_fc,
                                                       out_path=scratch_workspace, 
                                                       out_name="ACCG_Project_table", 
                                                       where_clause="SHAPE_Length = 0 Or SHAPE_Area = 0", 
                                                       field_mapping="", 
                                                       config_keyword="")

    # Process: Table Select (Table Select) (analysis)
    ACCG_Project_table2 = os.path.join(scratch_workspace, "ACCG_Project_table2")

#### ExecuteError: ERROR 160144: An expected Field was not found or could not be retrieved properly.Failed to execute (TableSelect).
    arcpy.analysis.TableSelect(in_table=ACCG_Project_table, 
                               out_table=ACCG_Project_table2, 
                               where_clause="PROCLAIMED_FOREST_CODE = '0417' Or PROCLAIMED_FOREST_CODE = '0501' Or PROCLAIMED_FOREST_CODE = '0502' Or PROCLAIMED_FOREST_CODE = '0503' Or PROCLAIMED_FOREST_CODE = '0504' Or PROCLAIMED_FOREST_CODE = '0505' Or PROCLAIMED_FOREST_CODE = '0506' Or PROCLAIMED_FOREST_CODE = '0507' Or PROCLAIMED_FOREST_CODE = '0508' Or PROCLAIMED_FOREST_CODE = '0509' Or PROCLAIMED_FOREST_CODE = '0510' Or PROCLAIMED_FOREST_CODE = '0511' Or PROCLAIMED_FOREST_CODE = '0512' Or PROCLAIMED_FOREST_CODE = '0513' Or PROCLAIMED_FOREST_CODE = '0514' Or PROCLAIMED_FOREST_CODE = '0515' Or PROCLAIMED_FOREST_CODE = '0516' Or PROCLAIMED_FOREST_CODE = '0517' Or PROCLAIMED_FOREST_CODE = '0519' Or PROCLAIMED_FOREST_CODE = '0602' Or PROCLAIMED_FOREST_CODE = '0610'")

    # Process: Add Projects Fields (multiple) (2) (Add Fields (multiple)) (management)
    WFR_TF_Template_2_ = arcpy.management.AddFields(in_table=ACCG_Project_table2, 
                                                    field_description=[["Prj_ID", "TEXT", "Project ID", "50", "", ""], 
                                                                       ["Prj_Name", "TEXT", "Project Name", "150", "", ""], 
                                                                       ["Prj_FundNM", "TEXT", "Primary Funding Source Name", "130", "", ""], 
                                                                       ["Prj_FndOrg", "TEXT", "Primary Funding Org Name", "130", "", ""], 
                                                                       ["Prj_Admin", "TEXT", "Primary Administering Org Name", "130", "", ""], 
                                                                       ["Prj_Implem", "TEXT", "Primary Implementing Org Name", "130", "", ""], 
                                                                       ["Prj_RptOrg", "TEXT", "Reporting Org Name", "130", "", ""], 
                                                                       ["Prj_Contct", "TEXT", "Project Contact", "100", "", ""], 
                                                                       ["Prj_Email", "TEXT", "Project Email", "100", "", ""], 
                                                                       ["Prj_Start", "DATE", "Project Start Date", "", "", ""], 
                                                                       ["Prj_End", "DATE", "Project End Date", "", "", ""], 
                                                                       ["Prj_Status", "TEXT", "Projec Status", "25", "", "Prj_Status"], 
                                                                       ["Lat", "DOUBLE", "Latitude", "", "", ""], 
                                                                       ["Lon", "DOUBLE", "Longitude", "", "", ""]], 
                                                                       template=[])

    # Process: Add Treatments Fields (multiple) (2) (Add Fields (multiple)) (management)
    Updated_Input_Table_26_ = arcpy.management.AddFields(in_table=WFR_TF_Template_2_, 
                                                         field_description=[["TreatID", "TEXT", "TreatmentID", "50", "", ""], 
                                                                            ["Treat_Name", "TEXT", "Treatment Name", "100", "", ""], 
                                                                            ["County", "TEXT", "County", "35", "", "County"], 
                                                                            ["WUI", "TEXT", "WUI", "3", "", "WUI"], 
                                                                            ["Prim_Obj", "TEXT", "Primary Objective", "65", "", "Objective"], 
                                                                            ["Sec_Obj", "TEXT", "Secondary Objective", "65", "", "Objective"], 
                                                                            ["Tert_Obj", "TEXT", "Tertiary Objective", "65", "", "Objective"], 
                                                                            ["Category", "TEXT", "Objective Category", "35", "", "Category"], 
                                                                            ["Retrt_Date", "DATE", "Estimated Retreatment Date", "", "", ""], 
                                                                            ["Trt_Status", "TEXT", "Treatment Status", "10", "", "Treat_Status"], 
                                                                            ["TreatStart", "DATE", "Treatment Start Date", "", "", ""], 
                                                                            ["Treat_End", "DATE", "Treatment End Date", "", "", ""], 
                                                                            ["Treat_Acre", "DOUBLE", "Treatment Area (Acres)", "255", "", ""], 
                                                                            ["Ownership", "TEXT", "Ownership Group", "35", "", "Ownership"]], 
                                                                            template=[])

    # Process: Add Activities Fields (multiple) (2) (Add Fields (multiple)) (management)
    Updated_Input_Table_2_ = arcpy.management.AddFields(in_table=Updated_Input_Table_26_, 
                                                        field_description=[["ActivityID", "TEXT", "Activity Id", "50", "", ""], 
                                                                           ["Act_Name", "TEXT", "Activity Name", "100", "", ""], 
                                                                           ["P_Fund_Src", "TEXT", "Primary Funding Source Name", "100", "", ""], 
                                                                           ["P_Fnd_Org", "TEXT", "Primary Funding Org Name", "100", "", ""], 
                                                                           ["S_Fnd_Src", "TEXT", "Secondary Funding Source Name", "100", "", ""], 
                                                                           ["S_Fnd_Org", "TEXT", "Secondary Funding Org Name", "100", "", ""], 
                                                                           ["T_Fnd_Src", "TEXT", "Tertiary Funding Source Name", "100", "", ""], 
                                                                           ["T_Fnd_Org", "TEXT", "Tertiary Funding Org Name", "100", "", ""], 
                                                                           ["Admin_Org", "TEXT", "Administering Org Name", "100", "", ""], 
                                                                           ["Imp_Org", "TEXT", "Implementing Org Name", "100", "", ""], 
                                                                           ["Act_Desc", "TEXT", "Activity Description", "70", "", "Activity"], 
                                                                           ["UOM_", "TEXT", "Activity_Unit_of_Measure", "15", "", ""], 
                                                                           ["Act_Quant", "DOUBLE", "Activity_Quantity", "", "", ""], 
                                                                           ["Act_Status", "TEXT", "Activity Status", "10", "", "Treat_Status"], 
                                                                           ["Veg_Type", "TEXT", "Broad Vegetation Type", "50", "", "Veg_Type"], 
                                                                           ["Residue_Q", "DOUBLE", "Residue Quantity", "", "", ""], 
                                                                           ["Residue_Fa", "TEXT", "Residue Fate", "35", "", "Residue"], 
                                                                           ["Act_Start", "DATE", "Activity Start Date", "", "", ""], 
                                                                           ["Act_End", "DATE", "Activity End Date", "", "", ""], 
                                                                           ["Act_Percnt", "DOUBLE", "Activity Percent Complete", "", "", ""], 
                                                                           ["Source", "TEXT", "Source", "65", "", ""], 
                                                                           ["Year", "LONG", "Calendar Year", "", "", ""], 
                                                                           ["Year_txt", "TEXT", "Year as Text", "4", "", ""], 
                                                                           ["Crosswalk", "TEXT", "Crosswalk Activities", "150", "", ""], 
                                                                           ["Region", "TEXT", "CalFire Region", "35", "", ""], 
                                                                           ["Act_Code", "LONG", "USFS Activity Code", "", "", ""]], 
                                                                           template=[])

    # Process: Calculate Admin Org (2) (Calculate Field) (management)
    Updated_Input_Table_3_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_2_, 
                                                             field="Prj_Admin", 
                                                             expression="!ORGANIZATI!", 
                                                             expression_type="PYTHON3", 
                                                             code_block="", 
                                                             field_type="TEXT", 
                                                             enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Reporting Org (2) (Calculate Field) (management)
    Updated_Input_Table_18_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_3_, 
                                                              field="Prj_RptOrg", 
                                                              expression="!ORGANIZATI!", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Field (Calculate Field) (management)
    ACCG_Project_table2_3_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_18_, 
                                                             field="Prj_Name", 
                                                             expression="!NAME!", 
                                                             expression_type="PYTHON3", 
                                                             code_block="", 
                                                             field_type="TEXT", 
                                                             enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Projet ID (2) (Calculate Field) (management)
    usfs_haz_fuels_treatments_reduction2_3_ = arcpy.management.CalculateField(in_table=ACCG_Project_table2_3_, 
                                                                              field="Prj_ID", 
                                                                              expression="!OBJECTID!", 
                                                                              expression_type="PYTHON3", 
                                                                              code_block="", 
                                                                              field_type="TEXT", 
                                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Treatment ID (2) (Calculate Field) (management)
    usfs_haz_fuels_treatments_reduction2_5_ = arcpy.management.CalculateField(in_table=usfs_haz_fuels_treatments_reduction2_3_, 
                                                                              field="TreatmentID", 
                                                                              expression="!MAINTENANC!", 
                                                                              expression_type="PYTHON3", 
                                                                              code_block="", 
                                                                              field_type="TEXT", 
                                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Activity UOM (2) (Calculate Field) (management)
    Updated_Input_Table_21_ = arcpy.management.CalculateField(in_table=usfs_haz_fuels_treatments_reduction2_5_, 
                                                              field="UOM_", 
                                                              expression="!ACRES!", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Activity Quantity (2) (Calculate Field) (management)
    Updated_Input_Table_22_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_21_, 
                                                              field="Act_Quant", 
                                                              expression="!ACRES!", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Field (5) (Calculate Field) (management)
    ACCG_Project_table2_4_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_22_, 
                                                             field="Act_Code", 
                                                             expression="\"NULL\"", 
                                                             expression_type="PYTHON3", 
                                                             code_block="", 
                                                             field_type="TEXT", 
                                                             enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Activity End Date (3) (Calculate Field) (management)
    usfs_haz_fuels_treatments_reduction2_7_ = arcpy.management.CalculateField(in_table=ACCG_Project_table2_4_, 
                                                                              field="Act_End", 
                                                                              expression="ifelse(!DATE_COMPLETED!, !DATE_AWARDED!, !DATE_PLANNED!)", 
                                                                              expression_type="PYTHON3", 
                                                                              code_block="""def ifelse(DateComp, DateAw, DatePl):
                                                                                if DateComp != None:
                                                                                    return DateComp
                                                                                elif DateComp == None:
                                                                                    return DateAw
                                                                                elif DateAw != None:
                                                                                    return DatePl""", 
                                                                              field_type="TEXT", 
                                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Activity End Date (4) (Calculate Field) (management)
    Updated_Input_Table_5_ = arcpy.management.CalculateField(in_table=usfs_haz_fuels_treatments_reduction2_7_, 
                                                             field="Act_End", 
                                                             expression="ifelse(!DATE_COMPLETED!, !DATE_AWARDED!)", 
                                                             expression_type="PYTHON3", 
                                                             code_block="""def ifelse(DateComp, DateAw):
                                                                    if DateComp != None:
                                                                        return DateComp
                                                                    elif DateComp == None:
                                                                        return DateAw
                                                                    """, 
                                                             field_type="TEXT", 
                                                             enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Select Layer By Attribute (3) (Select Layer By Attribute) (management)
    usfs_silviculture_TSI_dissol_3_, Count_3_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=Updated_Input_Table_5_, 
                                                                                        selection_type="NEW_SELECTION", 
                                                                                        where_clause="Act_End IS NULL", 
                                                                                        invert_where_clause="")

    # Process: Calculate Activity End Date (5) (Calculate Field) (management)
    Updated_Input_Table_6_ = arcpy.management.CalculateField(in_table=usfs_silviculture_TSI_dissol_3_, field="Act_End", 
                                                             expression="!DATE_PLANNED!", 
                                                             expression_type="PYTHON3", 
                                                             code_block="", 
                                                             field_type="TEXT", 
                                                             enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Select Layer By Attribute (4) (Select Layer By Attribute) (management)
    usfs_silviculture_TSI_dissol_4_, Count_4_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=Updated_Input_Table_6_, 
                                                                                        selection_type="CLEAR_SELECTION", 
                                                                                        where_clause="", 
                                                                                        invert_where_clause="")

    # Process: Calculate Status (2) (Calculate Field) (management)
    usfs_haz_fuels_treatments_reduction2_8_ = arcpy.management.CalculateField(in_table=usfs_silviculture_TSI_dissol_4_, 
                                                                              field="Act_Status", 
                                                                              expression="ifelse(!DATE_COMPLETED!, !DATE_AWARDED!, !DATE_PLANNED!)", 
                                                                              expression_type="PYTHON3", 
                                                                              code_block="""def ifelse(DateComp, DateAw, DatePl):
                                                                                if DateComp != None:
                                                                                    return \"Complete\"
                                                                                elif DateAw != None:
                                                                                    return \"Complete\"
                                                                                elif DatePl >= datetime.datetime(2024, 6, 7):
                                                                                    return \"Out-Year\"
                                                                                elif DatePl >= datetime.datetime(2012, 6, 7):
                                                                                    return \"Planned\"
                                                                                else:
                                                                                    return \"Canceled\"
                                                                                """, 
                                                                                field_type="TEXT", 
                                                                                enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Source (2) (Calculate Field) (management)
    Updated_Input_Table_23_ = arcpy.management.CalculateField(in_table=usfs_haz_fuels_treatments_reduction2_8_, 
                                                              field="Source", 
                                                              expression="\"usfs_timber_harvests\"", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Year (2) (Calculate Field) (management)
    Updated_Input_Table_24_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_23_, 
                                                              field="Year", 
                                                              expression="Year($feature.Act_End)", 
                                                              expression_type="ARCADE", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Year Text (2) (Calculate Field) (management)
    Updated_Input_Table_25_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_24_, 
                                                              field="Year_txt", 
                                                              expression="!Year!", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Crosswalk (2) (Calculate Field) (management)
    Updated_Input_Table_27_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_25_, 
                                                              field="Crosswalk", 
                                                              expression="!ACTIVITY_NAME!", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="ENFORCE_DOMAINS")

    # Process: Add Join (Add Join) (management)
    usfs_harvests_table2_View = arcpy.management.AddJoin(in_layer_or_view=Updated_Input_Table_27_, 
                                                         in_field="Act_Code", 
                                                         join_table=Fuels_Treatments_Piles_Crosswalk, 
                                                         join_field="USFS_Activity_Code", 
                                                         join_type="KEEP_ALL", 
                                                         index_join_fields="NO_INDEX_JOIN_FIELDS")

    # Process: Calculate Field (2) (Calculate Field) (management)
    usfs_harvests_table2_View_2_ = arcpy.management.CalculateField(in_table=usfs_harvests_table2_View, 
                                                                   field="usfs_harvests_table2.Prim_Obj", 
                                                                   expression="!Fuels_Treatments_Piles_Crosswalk.Objective!", 
                                                                   expression_type="PYTHON3", 
                                                                   code_block="", 
                                                                   field_type="TEXT", 
                                                                   enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Field (3) (Calculate Field) (management)
    usfs_harvests_table2_View_3_ = arcpy.management.CalculateField(in_table=usfs_harvests_table2_View_2_, 
                                                                   field="usfs_harvests_table2.Category", 
                                                                   expression="!Fuels_Treatments_Piles_Crosswalk.Category!", 
                                                                   expression_type="PYTHON3", 
                                                                   code_block="", 
                                                                   field_type="TEXT", 
                                                                   enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Field (4) (Calculate Field) (management)
    usfs_harvests_table2_View_4_ = arcpy.management.CalculateField(in_table=usfs_harvests_table2_View_3_, 
                                                                   field="usfs_harvests_table2.Act_Desc", 
                                                                   expression="!Fuels_Treatments_Piles_Crosswalk.Activity!", 
                                                                   expression_type="PYTHON3", 
                                                                   code_block="", 
                                                                   field_type="TEXT", 
                                                                   enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Remove Join (Remove Join) (management)
    Layer_With_Join_Removed = arcpy.management.RemoveJoin(in_layer_or_view=usfs_harvests_table2_View_4_, 
                                                          join_name="Fuels_Treatments_Piles_Crosswalk")

    # Process: Delete Field (Delete Field) (management)
    usfs_haz_fuels_treatments_re = KeepFields(Layer_With_Join_Removed)

    # Process: Table To Table (2) (Table To Table) (conversion)
    usfs_timber_harvest_table_standardized_20220715 = arcpy.conversion.TableToTable(in_rows=usfs_haz_fuels_treatments_re, 
                                                                                    out_path=workspace, 
                                                                                    out_name="usfs_timber_harvest_table_standardized_20220715", 
                                                                                    where_clause="", 
                                                                                    field_mapping="", 
                                                                                    config_keyword="")

    # Process: Select (Select) (analysis)
    ACCG_Project_Select = os.path.join(scratch_workspace, "ACCG_Project_Select")
    with arcpy.EnvManager(outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]"""):
                    arcpy.analysis.Select(in_features=input_fc, 
                          out_feature_class=ACCG_Project_Select, 
                          where_clause="DATE_COMPLETED > timestamp '1995-01-01 00:00:00' Or DATE_COMPLETED IS NULL")

    # Process: Repair Geometry (2) (Repair Geometry) (management)
    Repaired_Input_Features_2_ = arcpy.management.RepairGeometry(in_features=ACCG_Project_Select, 
                                                                 delete_null="DELETE_NULL", 
                                                                 validation_method="ESRI")

    # Process: Pairwise Clip (Pairwise Clip) (analysis)
    ACCG_Project_clip = os.path.join(scratch_workspace, "ACCG_Project_clip")
    arcpy.analysis.PairwiseClip(in_features=Repaired_Input_Features_2_, 
                                clip_features=California_2_, 
                                out_feature_class=ACCG_Project_clip, 
                                cluster_tolerance="")

    # Process: Dissolve (Dissolve) (management)
    ACCG_Project_TSI_dissolve = os.path.join(scratch_workspace, "ACCG_Project_TSI_dissolve")
    arcpy.management.Dissolve(in_features=ACCG_Project_clip, 
                              out_feature_class=ACCG_Project_TSI_dissolve, 
                              dissolve_field=["OBJECTID_1", 
                                              "ACRES", 
                                              "STATUS", 
                                              "ORGANIZATI", 
                                              "NEPA_CEQA_", 
                                              "MAINTENANC", 
                                              "MAINTENA_1", 
                                              "NAME", 
                                              "ACTIVITY", 
                                              "TREATMENT", 
                                              "YEAR", 
                                              "OBJECTID", 
                                              "PROJECT", 
                                              "MERGE_SRC", 
                                              "STATUS_ACT"], 
                              statistics_fields=[], 
                              multi_part="MULTI_PART", 
                              unsplit_lines="DISSOLVE_LINES", 
                              concatenation_separator="")

    # Process: Add Projects Fields (multiple) (3) (Add Fields (multiple)) (management)
    Updated_Input_Table_28_ = arcpy.management.AddFields(in_table=ACCG_Project_TSI_dissolve, 
                                                         field_description=[["Prj_ID", "TEXT", "Project ID", "50", "", ""], 
                                                                            ["Prj_Name", "TEXT", "Project Name", "150", "", ""], 
                                                                            ["Prj_FundNM", "TEXT", "Primary Funding Source Name", "130", "", ""], 
                                                                            ["Prj_FndOrg", "TEXT", "Primary Funding Org Name", "130", "", ""], 
                                                                            ["Prj_Admin", "TEXT", "Primary Administering Org Name", "130", "", ""], 
                                                                            ["Prj_Implem", "TEXT", "Primary Implementing Org Name", "130", "", ""], 
                                                                            ["Prj_RptOrg", "TEXT", "Reporting Org Name", "130", "", ""], 
                                                                            ["Prj_Contct", "TEXT", "Project Contact", "100", "", ""], 
                                                                            ["Prj_Email", "TEXT", "Project Email", "100", "", ""], 
                                                                            ["Prj_Start", "DATE", "Project Start Date", "", "", ""], 
                                                                            ["Prj_End", "DATE", "Project End Date", "", "", ""], 
                                                                            ["Prj_Status", "TEXT", "Projec Status", "25", "", ""], 
                                                                            ["Lat", "DOUBLE", "Latitude", "", "", ""], 
                                                                            ["Lon", "DOUBLE", "Longitude", "", "", ""]], 
                                                                            template=[])

    # Process: Add Treatments Fields (multiple) (3) (Add Fields (multiple)) (management)
    Updated_Input_Table = arcpy.management.AddFields(in_table=Updated_Input_Table_28_, 
                                                     field_description=[["TreatID", "TEXT", "TreatmentID", "50", "", ""], 
                                                                        ["Treat_Name", "TEXT", "Treatment Name", "100", "", ""], 
                                                                        ["County", "TEXT", "County", "35", "", ""], 
                                                                        ["WUI", "TEXT", "WUI", "3", "", ""], 
                                                                        ["Prim_Obj", "TEXT", "Primary Objective", "65", "", ""], 
                                                                        ["Sec_Obj", "TEXT", "Secondary Objective", "65", "", ""], 
                                                                        ["Tert_Obj", "TEXT", "Tertiary Objective", "65", "", ""], 
                                                                        ["Category", "TEXT", "Objective Category", "35", "", ""], 
                                                                        ["Retrt_Date", "DATE", "Estimated Retreatment Date", "", "", ""], 
                                                                        ["Trt_Status", "TEXT", "Treatment Status", "10", "", ""], 
                                                                        ["TreatStart", "DATE", "Treatment Start Date", "", "", ""], 
                                                                        ["Treat_End", "DATE", "Treatment End Date", "", "", ""], 
                                                                        ["Treat_Acre", "DOUBLE", "Treatment Area (Acres)", "255", "", ""], 
                                                                        ["Ownership", "TEXT", "Ownership Group", "35", "", ""]], 
                                                     template=[])

    # Process: Add Activities Fields (multiple) (3) (Add Fields (multiple)) (management)
    Updated_Input_Table_29_ = arcpy.management.AddFields(in_table=Updated_Input_Table, 
                                                         field_description=[["ActivityID", "TEXT", "Activity Id", "50", "", ""], 
                                                                            ["Act_Name", "TEXT", "Activity Name", "100", "", ""], 
                                                                            ["P_Fund_Src", "TEXT", "Primary Funding Source Name", "100", "", ""], 
                                                                            ["P_Fnd_Org", "TEXT", "Primary Funding Org Name", "100", "", ""], 
                                                                            ["S_Fnd_Src", "TEXT", "Secondary Funding Source Name", "100", "", ""], 
                                                                            ["S_Fnd_Org", "TEXT", "Secondary Funding Org Name", "100", "", ""], 
                                                                            ["T_Fnd_Src", "TEXT", "Tertiary Funding Source Name", "100", "", ""], 
                                                                            ["T_Fnd_Org", "TEXT", "Tertiary Funding Org Name", "100", "", ""], 
                                                                            ["Admin_Org", "TEXT", "Administering Org Name", "100", "", ""], 
                                                                            ["Imp_Org", "TEXT", "Implementing Org Name", "150", "", ""], 
                                                                            ["Act_Desc", "TEXT", "Activity Description", "70", "", ""], 
                                                                            ["UOM_", "TEXT", "Activity Unit of Measure", "15", "", ""], 
                                                                            ["Act_Quant", "DOUBLE", "Activity Quantity", "", "", ""], 
                                                                            ["Act_Status", "TEXT", "Activity Status", "10", "", ""], 
                                                                            ["Veg_Type", "TEXT", "Broad Vegetation Type", "50", "", ""], 
                                                                            ["Residue_Q", "DOUBLE", "Residue Quantity", "", "", ""], 
                                                                            ["Residue_Fa", "TEXT", "Residue Fate", "35", "", ""], 
                                                                            ["Act_Start", "DATE", "Activity Start Date", "", "", ""], 
                                                                            ["Act_End", "DATE", "Activity End Date", "", "", ""], 
                                                                            ["Act_Percnt", "DOUBLE", "Activity Percent Complete", "", "", ""], 
                                                                            ["Source", "TEXT", "Source", "65", "", ""], 
                                                                            ["Year", "LONG", "Calendar Year", "", "", ""], 
                                                                            ["Year_txt", "TEXT", "Year as Text", "4", "", ""], 
                                                                            ["Crosswalk", "TEXT", "Crosswalk Activities", "150", "", ""], 
                                                                            ["Region", "TEXT", "CalFire Region", "35", "", ""], 
                                                                            ["Federal_FY", "LONG", "Federal FY", "", "", ""], 
                                                                            ["State_FY", "LONG", "State FY", "", "", ""], 
                                                                            ["Act_Code", "LONG", "USFS Activity Code", "", "", ""]], 
                                                                            template=[])

    # Process: Calculate Admin Org (3) (Calculate Field) (management)
    Updated_Input_Table_30_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_29_, 
                                                              field="Admin_Org", 
                                                              expression="!ORGANIZATI!", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Reporting Org (3) (Calculate Field) (management)
    Updated_Input_Table_31_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_30_, 
                                                              field="Prj_RptOrg", 
                                                              expression="!ORGANIZATI!", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Imp Org (3) (Calculate Field) (management)
    Updated_Input_Table_32_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_31_, 
                                                              field="Imp_Org", 
                                                              expression="!ORGANIZATI!", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Project Name (Calculate Field) (management)
    Updated_Input_Table_33_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_32_, 
                                                              field="Prj_Name", 
                                                              expression="!PROJECT!", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Project ID (Calculate Field) (management)
    Activity_SilvTSI_20220627_Se2_2_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_33_, 
                                                                       field="Prj_ID", 
                                                                       expression="!OBJECTID!", 
                                                                       expression_type="PYTHON3", 
                                                                       code_block="", 
                                                                       field_type="TEXT", 
                                                                       enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Treatment ID (3) (Calculate Field) (management)
    Activity_SilvTSI_20220627_Se2_3_ = arcpy.management.CalculateField(in_table=Activity_SilvTSI_20220627_Se2_2_, 
                                                                       field="TreatID", 
                                                                       expression="!MAINTENANC!", 
                                                                       expression_type="PYTHON3", 
                                                                       code_block="", 
                                                                       field_type="TEXT", 
                                                                       enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Activity UOM (3) (Calculate Field) (management)
    Activity_SilvTSI_20220627_Se2_5_ = arcpy.management.CalculateField(in_table=Activity_SilvTSI_20220627_Se2_3_, 
                                                                       field="UOM_", 
                                                                       expression="\"ACRES\"", 
                                                                       expression_type="PYTHON3", 
                                                                       code_block="", 
                                                                       field_type="TEXT", 
                                                                       enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Activity Quantity (3) (Calculate Field) (management)
    Activity_SilvTSI_20220627_Se2_6_ = arcpy.management.CalculateField(in_table=Activity_SilvTSI_20220627_Se2_5_, 
                                                                       field="Act_Quant", 
                                                                       expression="!ACRES!", 
                                                                       expression_type="PYTHON3", 
                                                                       code_block="", 
                                                                       field_type="DOUBLE", 
                                                                       enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Activity End Date (Calculate Field) (management)
    Updated_Input_Table_34_ = arcpy.management.CalculateField(in_table=Activity_SilvTSI_20220627_Se2_6_, 
                                                              field="Act_End", 
                                                              expression="!YEAR! + \"-12-31\"", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
    ACCG_Project_TSI_dissolve_La, Count = arcpy.management.SelectLayerByAttribute(in_layer_or_view=Updated_Input_Table_34_, 
                                                                                  selection_type="NEW_SELECTION", 
                                                                                  where_clause="YEAR IS NOT NULL", 
                                                                                  invert_where_clause="")

    # Process: Calculate Activity End Date (2) (Calculate Field) (management)
    Updated_Input_Table_4_ = arcpy.management.CalculateField(in_table=ACCG_Project_TSI_dissolve_La, 
                                                             field="Act_End", 
                                                             expression="!YEAR! + \"-12-31\"", 
                                                             expression_type="PYTHON3", 
                                                             code_block="", 
                                                             field_type="TEXT", 
                                                             enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Select Layer By Attribute (2) (Select Layer By Attribute) (management)
    usfs_silviculture_TSI_dissol_2_, Count_2_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=Updated_Input_Table_4_, 
                                                                                        selection_type="CLEAR_SELECTION", 
                                                                                        where_clause="", 
                                                                                        invert_where_clause="")

    # Process: Calculate Status (3) (Calculate Field) (management)
    Updated_Input_Table_35_ = arcpy.management.CalculateField(in_table=usfs_silviculture_TSI_dissol_2_, 
                                                              field="Act_Status", 
                                                              expression="ifelse(!STATUS!)", 
                                                              expression_type="PYTHON3", 
                                                              code_block="""def ifelse(STATUS):
                                                              if STATUS != None:
                                                                    return \"Complete\"
                                                              elif STATUS != None:
                                                                    return \"Complete\"
                                                              elif STATUS >= datetime.datetime(2024):
                                                                    return \"Implementation\"
                                                              elif STATUS >= datetime.datetime(2007):
                                                                    return \"Planned\"
                                                              else:
                                                                    return \"Canceled\"
                                                              """, 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Source (3) (Calculate Field) (management)
    Updated_Input_Table_36_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_35_, 
                                                              field="Source", 
                                                              expression="\"ACCG_Stakeholder\"", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Year (3) (Calculate Field) (management)
    Updated_Input_Table_37_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_36_, 
                                                              field="Year", 
                                                              expression="Year($feature.Act_End)", 
                                                              expression_type="ARCADE", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Year Text (3) (Calculate Field) (management)
    Updated_Input_Table_38_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_37_, 
                                                              field="Year_txt", 
                                                              expression="!Year!", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Crosswalk (3) (Calculate Field) (management)
    Updated_Input_Table_39_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_38_, 
                                                              field="Crosswalk", 
                                                              expression="!ACTIVITY!", 
                                                              expression_type="PYTHON3", 
                                                              code_block="", 
                                                              field_type="TEXT", 
                                                              enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate USFS Activity Code (Calculate Field) (management)
    usfs_silviculture_TSI_dissolve_2_ = arcpy.management.CalculateField(in_table=Updated_Input_Table_39_, 
                                                                        field="Act_Code", 
                                                                        expression="\"NULL\"", 
                                                                        expression_type="PYTHON3", 
                                                                        code_block="", 
                                                                        field_type="TEXT", 
                                                                        enforce_domains="NO_ENFORCE_DOMAINS")

    # Process: Calculate Geometry Attributes (3) (Calculate Geometry Attributes) (management)
    Activity_SilvTSI_20220627_dissolve_4_ = arcpy.management.CalculateGeometryAttributes(in_features=usfs_silviculture_TSI_dissolve_2_, 
                                                                                         geometry_property=[["Lat", "INSIDE_Y"], 
                                                                                                            ["Lon", "INSIDE_X"]], 
                                                                                         length_unit="", 
                                                                                         area_unit="", 
                                                                                         coordinate_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", coordinate_format="DD")

    # Process: Calculate Geometry Attributes (4) (Calculate Geometry Attributes) (management)
    Activity_SilvTSI_20220627_dissolve_3_ = arcpy.management.CalculateGeometryAttributes(in_features=Activity_SilvTSI_20220627_dissolve_4_, 
                                                                                         geometry_property=[["Treat_Acre", "AREA"]], 
                                                                                         length_unit="", 
                                                                                         area_unit="ACRES", 
                                                                                         coordinate_system="PROJCS[\"NAD_1983_California_Teale_Albers\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Albers\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",-4000000.0],PARAMETER[\"Central_Meridian\",-120.0],PARAMETER[\"Standard_Parallel_1\",34.0],PARAMETER[\"Standard_Parallel_2\",40.5],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]", coordinate_format="SAME_AS_INPUT")

    # Process: Copy Features (3) (Copy Features) (management)
    # ACCG_Stakeholder_standardized_20220828 = os.path.join(scratch_workspace, "ACCG_Stakeholder_standardized_20220828")
    arcpy.management.CopyFeatures(in_features=Activity_SilvTSI_20220627_dissolve_3_, 
                                  out_feature_class=output_standardized, 
                                  config_keyword="", 
                                  spatial_grid_1=None, 
                                  spatial_grid_2=None, 
                                  spatial_grid_3=None)

    print('Deleting Scratch Files')
    delete_scratch_files(gdb = scratch_workspace, delete_fc = 'yes', delete_table = 'yes', delete_ds = 'yes')
    
    end = time.time()
    print(f'Time Elapsed: {(end-start)/60} minutes')
    return usfs_timber_harvest_table_standardized_20220715

if __name__ == '__main__':
    runner(workspace,scratch_workspace,pACCGStakeholderDraft, '*argv[1:]')
    # # Global Environment settings
    # with arcpy.EnvManager(
    # extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""",  outputCoordinateSystem="""PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]""", 
    # preserveGlobalIds=True, 
    # qualifiedFieldNames=False, 
    # scratchWorkspace=scratch_workspace, 
    # transferDomains=True, 
    # transferGDBAttributeProperties=True, 
    # workspace=workspace):
    #     pACCGStakeholderDraft(*argv[1:])
