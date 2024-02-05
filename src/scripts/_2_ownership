"""
# Description:  Updates the CalFire's Ownership layer with the US Forest  
#               Service's "Forest ownership in the conterminious United  
#               States", and US Census California Counties
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""

import os
import arcpy
from .utils import init_gdb, delete_scratch_files

# from arcpy.sa import *

workspace, scratch_workspace = init_gdb()

# TODO add print steps, rename variables

def ownership(delete_scratch=False):
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

        # Check out any necessary licenses.
        # arcpy.CheckOutExtension("3D")
        # arcpy.CheckOutExtension("spatial")
        # arcpy.CheckOutExtension("Foundation")
        # arcpy.CheckOutExtension("Defense")
        # arcpy.CheckOutExtension("BusinessPrem")
        # arcpy.CheckOutExtension("Business")

        # arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")
        # arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Conversion Tools.tbx")
        # Model Environment settings

        # Download Forest_own1.tif from https://www.fs.usda.gov/rds/archive/catalog/RDS-2020-0044
        forest_own1_tif = os.path.join("..", "forest_own1.tif")

        California = os.path.join(workspace, "a_Reference", "California")
        Land_Ownership = "https://egis.fire.ca.gov/arcgis/rest/services/FRAP/ownership/FeatureServer/0"
        Counties = os.path.join(workspace, "a_Counties")
        Ownership_Update = os.path.join(
            workspace, "a_Reference", "CALFIRE_Ownership_Update"
        )

        # for I_Ownership_Update_COUNTY, Value in #  NOT  IMPLEMENTED(Ownership_Update, [["COUNTY", ""]], True):

        # Process: Reclassify (Reclassify) (sa)
        Reclass_forest_own = os.path.join(scratch_workspace, "Reclass_forest_own")
        # Reclass_forest_own2 = arcpy.CopyRaster_management(forest_own1_tif, Reclass_forest_own)
        # Reclassify = Reclass_forest_own
        Reclass_forest_own = arcpy.sa.Reclassify(
            forest_own1_tif, "Value", "1 1;2 2;3 3;4 4;5 5;6 6;7 7;8 8;NODATA 1", "DATA"
        )
        Reclass_forest_own.save(Reclass_forest_own)
        # Reclass_forest_own.save(Reclassify)

        # Process: Clip Raster (Clip Raster) (management)
        forest_own1_Clip = os.path.join(scratch_workspace, "forest_own1_Clip")
        arcpy.management.Clip(
            in_raster=Reclass_forest_own,
            rectangle="-374445.3268 -604500.6078 540038.467 450022.046",
            out_raster=forest_own1_Clip,
            in_template_dataset=California,
            clipping_geometry="ClippingGeometry",
        )
        forest_own1_Clip = arcpy.Raster(forest_own1_Clip)

        # Process: Raster to Polygon (Raster to Polygon) (conversion)
        Forest_Ownership_2020 = os.path.join(scratch_workspace, "Forest_Ownership_2020")
        # with arcpy.EnvManager(outputMFlag="Disabled", outputZFlag="Disabled"):
        arcpy.conversion.RasterToPolygon(
            in_raster=forest_own1_Clip,
            out_polygon_features=Forest_Ownership_2020,
            simplify="SIMPLIFY",
            create_multipart_features="SINGLE_OUTER_PART",
        )

        # Process: Select (6) (Select) (analysis)
        RasterT_forest_1_EliminatePo1 = os.path.join(
            scratch_workspace, "RasterT_forest_1_EliminatePo1"
        )
        arcpy.analysis.Select(
            in_features=Forest_Ownership_2020,
            out_feature_class=RasterT_forest_1_EliminatePo1,
            where_clause="GRIDCODE = 1 Or GRIDCODE = 2 Or GRIDCODE = 3 Or GRIDCODE = 4",
        )

        # Process: Add Fields (multiple) (5) (Add Fields (multiple)) (management)
        RasterT_forest_1_EliminatePo1_5_ = arcpy.management.AddFields(
            in_table=RasterT_forest_1_EliminatePo1,
            field_description=[
                ["Own_Level", "TEXT", "", "30", "", ""],
                ["Own_Agency", "TEXT", "", "70", "", ""],
                ["Own_Group", "TEXT", "", "50", "", ""],
                ["AGNCY_LEV", "TEXT", "", "255", "", ""],
            ],
        )

        # Process: Calculate Field (22) (Calculate Field) (management)
        RasterT_forest_1_EliminatePo1_7_ = arcpy.management.CalculateField(
            in_table=RasterT_forest_1_EliminatePo1_5_,
            field="Own_Level",
            expression="ifelse(!GRIDCODE!)",
            code_block="""def ifelse(GRIDCODE):
                    if GRIDCODE == 1:
                        return \"PRIVATE_NON-INDUSTRY\"
                    if GRIDCODE == 2:
                        return \"PRIVATE_INDUSTRY\"
                    if GRIDCODE == 3:
                        return \"PRIVATE_NON-INDUSTRY\"
                    if GRIDCODE == 4:
                        return \"PRIVATE_NON-INDUSTRY\"
                    if GRIDCODE == 5:
                        return \"Federal\"
                    if GRIDCODE == 6:
                        return \"STATE\"
                    if GRIDCODE == 7:
                        return \"LOCAL\"
                    if GRIDCODE == 8:
                        return \"TRIBAL\"
                    else:
                        return None
                    """,
        )

        # Process: Calculate Field (23) (Calculate Field) (management)
        RasterT_forest_1_EliminatePo1_3_ = arcpy.management.CalculateField(
            in_table=RasterT_forest_1_EliminatePo1_7_,
            field="Own_Agency",
            expression="ifelse(!GRIDCODE!)",
            code_block="""def ifelse(GRIDCODE):
                if GRIDCODE == 1:
                    return \"PRIVATE_NON-INDUSTRY\"
                if GRIDCODE == 2:
                    return \"PRIVATE_INDUSTRY\"
                if GRIDCODE == 3:
                    return \"PRIVATE_NON-INDUSTRY\"
                if GRIDCODE == 4:
                    return \"PRIVATE_NON-INDUSTRY\"
                if GRIDCODE == 5:
                    return \"Federal\"
                if GRIDCODE == 6:
                    return \"STATE\"
                if GRIDCODE == 7:
                    return \"LOCAL\"
                if GRIDCODE == 8:
                    return \"TRIBAL\"
                else:
                    return None""",
        )

        # Process: Calculate Field (24) (Calculate Field) (management)
        RasterT_forest_1_EliminatePo1_2_ = arcpy.management.CalculateField(
            in_table=RasterT_forest_1_EliminatePo1_3_,
            field="Own_Group",
            expression="ifelse(!GRIDCODE!)",
            code_block="""def ifelse(GRIDCODE):
                if GRIDCODE == 1:
                    return \"PRIVATE_NON-INDUSTRY\"
                if GRIDCODE == 2:
                    return \"PRIVATE_INDUSTRY\"
                if GRIDCODE == 3:
                    return \"PRIVATE_NON-INDUSTRY\"
                if GRIDCODE == 4:
                    return \"PRIVATE_NON-INDUSTRY\"
                if GRIDCODE == 5:
                    return \"Federal\"
                if GRIDCODE == 6:
                    return \"STATE\"
                if GRIDCODE == 7:
                    return \"LOCAL\"
                if GRIDCODE == 8:
                    return \"TRIBAL\"
                else:
                    return None""",
        )

        # Process: Calculate Field (5) (Calculate Field) (management)
        RasterT_forest_1_EliminatePo1_8_ = arcpy.management.CalculateField(
            in_table=RasterT_forest_1_EliminatePo1_2_,
            field="AGNCY_LEV",
            expression="ifelse(!GRIDCODE!)",
            code_block="""def ifelse(GRIDCODE):
                    if GRIDCODE == 1:
                        return \"PRIVATE_NON-INDUSTRY\"
                    if GRIDCODE == 2:
                        return \"PRIVATE_INDUSTRY\"
                    if GRIDCODE == 3:
                        return \"PRIVATE_NON-INDUSTRY\"
                    if GRIDCODE == 4:
                        return \"PRIVATE_NON-INDUSTRY\"
                    if GRIDCODE == 5:
                        return \"Federal\"
                    if GRIDCODE == 6:
                        return \"STATE\"
                    if GRIDCODE == 7:
                        return \"LOCAL\"
                    if GRIDCODE == 8:
                        return \"TRIBAL\"
                    else:
                        return None""",
        )

        # Process: Repair Geometry (7) (Repair Geometry) (management)
        Repaired_Input_Features_7_ = arcpy.management.RepairGeometry(
            in_features=RasterT_forest_1_EliminatePo1_8_
        )

        # Process: Delete Field (2) (Delete Field) (management)
        RasterT_forest_1_EliminatePo1_6_ = arcpy.management.DeleteField(
            in_table=Repaired_Input_Features_7_,
            drop_field=["Own_Level", "Own_Agency", "Own_Group", "AGNCY_LEV"],
            method="KEEP_FIELDS",
        )

        # Process: Repair Geometry (3) (Repair Geometry) (management)
        Repaired_Input_Features_3_ = arcpy.management.RepairGeometry(
            in_features=RasterT_forest_1_EliminatePo1_6_
        )

        # Process: Copy Features (Copy Features) (management)
        Output_Feature_Class_3_ = os.path.join(
            scratch_workspace, "LandOwnership_CopyFeatures"
        )
        arcpy.management.CopyFeatures(
            in_features=Land_Ownership, out_feature_class=Output_Feature_Class_3_
        )

        # Process: Add Field (Add Field) (management)
        Land_Ownership_2_ = arcpy.management.AddField(
            in_table=Output_Feature_Class_3_,
            field_name="AGNCY_LEV",
            field_type="TEXT",
            field_length=50,
        )

        # Process: Calculate Field (34) (Calculate Field) (management)
        Land_Ownership_3_ = arcpy.management.CalculateField(
            in_table=Land_Ownership_2_,
            field="AGNCY_LEV",
            expression="ifelse(!OWN_LEVEL!)",
            expression_type="PYTHON3",
            code_block="""def ifelse(NAME):
                        if NAME == \"City\":
                            return \"LOCAL\"
                        if NAME == \"County\":
                            return \"LOCAL\"
                        if NAME == \"Federal\":
                            return \"FEDERAL\"
                        if NAME == \"Non Profit\":
                            return \"NGO\"
                        if NAME == \"Special District\":
                            return \"LOCAL\"
                        if NAME == \"State\":
                            return \"STATE\"
                        if NAME == \"Tribal\":
                            return \"TRIBAL\"
                        else:
                            return NAME""",
        )

        # Process: Update (Update) (analysis)
        Output_Feature_Class_5_ = os.path.join(
            scratch_workspace, "RasterT_forest_1_Elim_Update"
        )
        arcpy.analysis.Update(
            in_features=Repaired_Input_Features_3_,
            update_features=Land_Ownership_3_,
            out_feature_class=Output_Feature_Class_5_,
        )

        # Process: Select (4) (Select) (analysis)
        Counties_Select = os.path.join(scratch_workspace, "Counties_Select")
        arcpy.analysis.Select(
            in_features=Counties,
            out_feature_class=Counties_Select,
            where_clause="STATE_NAME = 'California'",
        )

        # Process: Alter Field (3) (Alter Field) (management)
        Counties_Select_8_ = arcpy.management.AlterField(
            in_table=Counties_Select,
            field="NAME",
            new_field_name="COUNTY",
            new_field_alias="COUNTY",
        )

        # Process: Repair Geometry (2) (Repair Geometry) (management)
        Repaired_Input_Features_2_ = arcpy.management.RepairGeometry(
            in_features=Counties_Select_8_
        )

        # Process: Delete Field (Delete Field) (management)
        Counties_Select_3_ = arcpy.management.DeleteField(
            in_table=Repaired_Input_Features_2_,
            drop_field=["COUNTY"],
            method="KEEP_FIELDS",
        )

        # Process: Union (Union) (analysis)
        Output_Feature_Class_6_ = os.path.join(
            scratch_workspace, "Counties_Select_Union"
        )
        arcpy.analysis.Union(
            in_features=[[Output_Feature_Class_5_, ""], [Counties_Select_3_, ""]],
            out_feature_class=Output_Feature_Class_6_,
        )

        # Process: Calculate Field (Calculate Field) (management)
        Counties_Select_Union = arcpy.management.CalculateField(
            in_table=Output_Feature_Class_6_,
            field="AGNCY_LEV",
            expression="ifelse(!AGNCY_LEV!)",
            code_block="""def ifelse(AGNCY):
                if AGNCY is None or AGNCY == '':
                    return \"PRIVATE_NON-INDUSTRY\"
                else:
                    return AGNCY""",
        )

        # Process: Dissolve (Dissolve) (management)
        arcpy.management.Dissolve(
            in_features=Counties_Select_Union,
            out_feature_class=Ownership_Update,
            dissolve_field=["AGNCY_LEV", "COUNTY"],
            multi_part="MULTI_PART",
        )

        # Process: Repair Geometry (Repair Geometry) (management)
        Repaired_Input_Features = arcpy.management.RepairGeometry(
            in_features=Ownership_Update
        )

        # Process: Calculate County (Calculate Field) (management)
        Updated_Input_Table_10_ = arcpy.management.CalculateField(
            in_table=Repaired_Input_Features,
            field="COUNTY",
            expression="ifelse(!COUNTY!)",
            code_block="""def ifelse(County):
                    if County == 'Alameda' or County == 'Alameda County' or County == 'ALAMEDA':
                        return 'ALA'
                    elif County == 'Alpine' or County == 'Alpine County' or County == 'ALPINE':
                        return 'ALP'
                    elif County == 'Amador' or County == 'Amador County' or County == 'AMADOR':
                        return 'AMA'
                    elif County == 'Butte' or County == 'Butte County' or County == 'BUTTE':
                        return 'BUT'
                    elif County == 'Calaveras' or County == 'Calaveras County' or County == 'CALAVERAS':
                        return 'CAL'
                    elif County == 'Colusa' or County == 'Colusa County' or County == 'COLUSA':
                        return 'COL'
                    elif County == 'Contra Costa' or County == 'Contra Costa County' or County == 'CONTRA COSTA':
                        return 'CC'
                    elif County == 'Del Norte' or County == 'Del Norte County' or County == 'DEL NORTE':
                        return 'DN'
                    elif County == 'El Dorado' or County == 'El Dorado County' or County == 'EL DORADO':
                        return 'ED'
                    elif County == 'Fresno' or County == 'Fresno County' or County == 'FRESNO':
                        return 'FRE'
                    elif County == 'Glenn' or County == 'Glenn County' or County == 'GLENN':
                        return 'GLE'
                    elif County == 'Humboldt' or County == 'Humboldt County' or County == 'HUMBOLDT':
                        return 'HUM'
                    elif County == 'Imperial' or County == 'Imperial County' or County == 'IMPERIAL':
                        return 'IMP'
                    elif County == 'Inyo' or County == 'Inyo County' or County == 'INYO':
                        return 'INY'
                    elif County == 'Kern' or County == 'Kern County' or County == 'KERN':
                        return 'KER'
                    elif County == 'Kings' or County == 'Kings County' or County == 'KINGS':
                        return 'KIN'
                    elif County == 'Lake' or County == 'Lake County' or County == 'LAKE':
                        return 'LAK'
                    elif County == 'Lassen' or County == 'Lassen County' or County == 'LASSEN':
                        return 'LAS'
                    elif County == 'Los Angeles' or County == 'Los Angeles County' or County == 'LOS ANGELES':
                        return 'LA'
                    elif County == 'Madera' or County == 'Madera County' or County == 'MADERA':
                        return 'MAD'
                    elif County == 'Marin' or County == 'Marin County' or County == 'MARIN':
                        return 'MRN'
                    elif County == 'Mariposa' or County == 'Mariposa County' or County == 'MARIPOSA':
                        return 'MPA'
                    elif County == 'Mendocino' or County == 'Mendocino County' or County == 'MENDOCINO':
                        return 'MEN'
                    elif County == 'Merced' or County == 'Merced County' or County == 'MERCED':
                        return 'MER'
                    elif County == 'Modoc' or County == 'Modoc County' or County == 'MODOC':
                        return 'MOD'
                    elif County == 'Monterey' or County == 'Monterey County' or County == 'MONTEREY':
                        return 'MON'
                    elif County == 'Mono' or County == 'Mono County' or County == 'MONO':
                        return 'MNO'
                    elif County == 'Napa' or County == 'Napa County' or County == 'NAPA':
                        return 'NAP'
                    elif County == 'Nevada' or County == 'Nevada County' or County == 'NEVADA':
                        return 'NEV'
                    elif County == 'Orange' or County == 'Orange County' or County == 'ORANGE':
                        return 'ORA'
                    elif County == 'Placer' or County == 'Placer County' or County == 'PLACER':
                        return 'PLA'
                    elif County == 'Plumas' or County == 'Plumas County' or County == 'PLUMAS':
                        return 'PLU'
                    elif County == 'Riverside' or County == 'Riverside County' or County == 'RIVERSIDE':
                        return 'RIV'
                    elif County == 'Sacramento' or County == 'Sacramento County' or County == 'SACRAMENTO':
                        return 'SAC'
                    elif County == 'San Benito' or County == 'San Benito County' or County == 'SAN BENITO':
                        return 'SBT'
                    elif County == 'San Bernardino' or County == 'San Bernardino County' or County == 'SAN BERNARDINO':
                        return 'SBD'
                    elif County == 'San Diego' or County == 'San Diego County' or County == 'SAN DIEGO':
                        return 'SD'
                    elif County == 'San Francisco' or County == 'San Francisco County' or County == 'SAN FRANCISCO':
                        return 'SF'
                    elif County == 'San Joaquin' or County == 'San Joaquin County' or County == 'SAN JOAQUIN':
                        return 'SJ'
                    elif County == 'San Luis Obispo' or County == 'San Luis Obispo County' or County == 'SAN LUIS OBISPO':
                        return 'SLO'
                    elif County == 'San Mateo' or County == 'San Mateo County' or County == 'SAN MATEO':
                        return 'SM'
                    elif County == 'Santa Barbara' or County == 'Santa Barbara County' or County == 'SANTA BARBARA':
                        return 'SB'
                    elif County == 'Santa Clara' or County == 'Santa Clara County' or County == 'SANTA CLARA':
                        return 'SCL'
                    elif County == 'Santa Cruz' or County == 'Santa Cruz County' or County == 'SANTA CRUZ':
                        return 'SCR'
                    elif County == 'Shasta' or County == 'Shasta County' or County == 'SHASTA':
                        return 'SHA'
                    elif County == 'Sierra' or County == 'Sierra County' or County == 'SIERRA':
                        return 'SIE'
                    elif County == 'Siskiyou' or County == 'Siskiyou County' or County == 'SISKIYOU':
                        return 'SIS'
                    elif County == 'Solano' or County == 'Solano County' or County == 'SOLANO':
                        return 'SOL'
                    elif County == 'Sonoma' or County == 'Sonoma County' or County == 'SONOMA':
                        return 'SON'
                    elif County == 'Stanislaus' or County == 'Stanislaus County' or County == 'STANISLAUS':
                        return 'STA'
                    elif County == 'Sutter' or County == 'Sutter County' or County == 'SUTTER':
                        return 'SUT'
                    elif County == 'Tehama' or County == 'Tehama County' or County == 'TEHAMA':
                        return 'TEH'
                    elif County == 'Tuolumne' or County == 'Tuolumne County' or County == 'TUOLUMNE':
                        return 'TUO'
                    elif County == 'Trinity' or County == 'Trinity County' or County == 'TRINITY':
                        return 'TRI'
                    elif County == 'Tulare' or County == 'Tulare County' or County == 'TULARE':
                        return 'TUL'
                    elif County == 'Ventura' or County == 'Ventura County' or County == 'VENTURA':
                        return 'VEN'
                    elif County == 'Yolo' or County == 'Yolo County' or County == 'YOLO':
                        return 'YOL'
                    elif County == 'Yuba' or County == 'Yuba County' or County == 'YUBA':
                        return 'YUB'
                    else:
                        return County""",
        )

        # Process: Calculate Geometry Attributes (Calculate Geometry Attributes) (management)
        CPAD_Ownership_Update_3_ = arcpy.management.CalculateGeometryAttributes(
            in_features=Updated_Input_Table_10_,
            geometry_property=[["GIS_ACRES", "AREA_GEODESIC"]],
            area_unit="ACRES",
            # coordinate_system='PROJCS["NAD_1983_California_Teale_Albers",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER["Standard_Parallel_2",40.5],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]',
        )

        # Process: Table To Excel (Table To Excel) (conversion)
        # CPAD_Ownership_Update_TableToExcel_xlsx = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\2-Map Exports\\CPAD_Ownership_Update_TableToExcel.xlsx"
        # arcpy.conversion.TableToExcel(Input_Table=CPAD_Ownership_Update_3_, Output_Excel_File=CPAD_Ownership_Update_TableToExcel_xlsx, Use_field_alias_as_column_header="ALIAS")

        # # Process: Fill Gaps (Fill Gaps) (topographic)
        # Updated_Features = arcpy.topographic.FillGaps(
        #     input_features=[Repaired_Input_Features], max_gap_area="100 AcresUS"
        # )

        # # Process: Remove Overlap (Remove Overlap) (ba)
        # Output_Feature_Class_4_ = os.path.join(
        #     scratch_workspace, "Ownership_Update_RemoveOverlap"
        # )
        # arcpy.ba.RemoveOverlap(
        #     in_features=I_Ownership_Update_COUNTY,
        #     out_feature_class=Output_Feature_Class_4_,
        #     ring_id_field="",
        #     store_id="",
        #     in_stores_layer="",
        #     link_field="",
        # )

        if delete_scratch:
            delete_scratch_files(
                gdb=scratch_workspace,
                delete_fc="yes",
                delete_table="yes",
                delete_ds="yes",
            )
        
        return CPAD_Ownership_Update_3_
