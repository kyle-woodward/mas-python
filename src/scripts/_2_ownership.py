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

workspace, scratch_workspace = init_gdb()

def ownership(delete_scratch=True):
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
        # define intermediary objects in scratch
        Reclass_forest_own = os.path.join(scratch_workspace, "Reclass_forest_own")
        forest_own1_Clip = os.path.join(scratch_workspace, "forest_own1_Clip")
        Forest_Ownership_2020 = os.path.join(scratch_workspace, "Forest_Ownership_2020")
        RasterT_forest_1_EliminatePo1 = os.path.join(scratch_workspace, "RasterT_forest_1_EliminatePo1")
        CalFire_copy = os.path.join(scratch_workspace, "LandOwnership_CopyFeatures")
        USFS_CalFire = os.path.join(scratch_workspace, "RasterT_forest_1_Elim_Update")
        Counties_Select = os.path.join(scratch_workspace, "Counties_Select")
        USFS_CalFire_Counties = os.path.join(scratch_workspace, "Counties_Select_Union")

        # Download Forest_own1.tif from https://www.fs.usda.gov/rds/archive/catalog/RDS-2020-0044
        forest_own1_tif = os.path.join("..", "forest_own1.tif")

        California = os.path.join(workspace, "a_Reference", "California") #from AGOL Living Atlas 
        Land_Ownership = "https://egis.fire.ca.gov/arcgis/rest/services/FRAP/ownership/FeatureServer/0"
        Counties = os.path.join(workspace, "a_Reference", "Counties") #from AGOL Living Atlas 
        Ownership_Update = os.path.join(workspace, "a_Reference", "CALFIRE_Ownership_Update")

        ### BEGIN TOOL CHAIN
        ## Part 1 formats the USFS raster, Part 2 formats Calfire Ownership.  Part 3 combines the 2 datasets
        print("Part 1: Format USFS forest ownership")
        copy_1 = arcpy.CopyRaster_management(forest_own1_tif, Reclass_forest_own)
        reclas_own = arcpy.sa.Reclassify(
            Reclass_forest_own, "Value", "1 1;2 2;3 3;4 4;5 5;6 6;7 7;8 8;NODATA 1", "DATA"
        )

        reclas_own.save(reclas_own)

        print("   step 1/7: clip to California")
        clip_raster = arcpy.management.Clip(
            in_raster=reclas_own,
            rectangle="-374445.3268 -604500.6078 540038.467 450022.046",
            out_raster=forest_own1_Clip,
            in_template_dataset=California,
            clipping_geometry="ClippingGeometry",
        )
        save_raster = arcpy.Raster(clip_raster)

        print("   step 2/7: convert to polygon")
        to_poly = arcpy.conversion.RasterToPolygon(
            in_raster=save_raster,
            out_polygon_features=Forest_Ownership_2020,
            simplify="SIMPLIFY",
            create_multipart_features="SINGLE_OUTER_PART",
        )

        print("   setp 3/7: select non-federal ownership")
        select_1 = arcpy.analysis.Select(
            in_features=to_poly,
            out_feature_class=RasterT_forest_1_EliminatePo1,
            where_clause="GRIDCODE = 1 Or GRIDCODE = 2 Or GRIDCODE = 3 Or GRIDCODE = 4",
        )

        print("   setp 4/7: add fields")
        add_fields_1 = arcpy.management.AddFields(
            in_table=select_1,
            field_description=[
                ["Own_Level", "TEXT", "", "30", "", ""],
                ["Own_Agency", "TEXT", "", "70", "", ""],
                ["Own_Group", "TEXT", "", "50", "", ""],
                ["AGNCY_LEV", "TEXT", "", "255", "", ""],
            ],
        )

        print("   setp 5/7: standardize ownership attributes")
        calc_field_1 = arcpy.management.CalculateField(
            in_table=add_fields_1,
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

        calc_field_2 = arcpy.management.CalculateField(
            in_table=calc_field_1,
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

        calc_field_3 = arcpy.management.CalculateField(
            in_table=calc_field_2,
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

        calc_field_4 = arcpy.management.CalculateField(
            in_table=calc_field_3,
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

        print("   setp 6/7: delete unnecessary fields")
        delete_field = arcpy.management.DeleteField(
            in_table=calc_field_4,
            drop_field=["Own_Level", "Own_Agency", "Own_Group", "AGNCY_LEV"],
            method="KEEP_FIELDS",
        )

        print("   setp 7/7: repair geometry")
        repair_geom_1 = arcpy.management.RepairGeometry(
            in_features=delete_field
        )

        print("Part 2: Format CalFire ownership layer")
        print("   setp 1/3: copy feature service")
        save_features_1 = arcpy.management.CopyFeatures(
            in_features=Land_Ownership, 
            out_feature_class=CalFire_copy
        )

        print("   setp 2/3: add field")
        add_field_1 = arcpy.management.AddField(
            in_table=save_features_1,
            field_name="AGNCY_LEV",
            field_type="TEXT",
            field_length=50,
        )

        print("   setp 3/3: standardize ownership attributes")
        calc_field_5 = arcpy.management.CalculateField(
            in_table=add_field_1,
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

        print("Part 3: Combine Parts 1 & 2")
        print("   setp 1/10: update USFS layer to CalFire Ownership layer")
        USFS_CalFire_update = arcpy.analysis.Update(
            in_features=repair_geom_1,
            update_features=calc_field_5,
            out_feature_class=USFS_CalFire,
        )

        print("   setp 2/10: delete slivers")
        CA_counties = arcpy.analysis.Select(
            in_features=Counties,
            out_feature_class=Counties_Select,
            where_clause="STATE_NAME = 'California'",
        )

        alter_field_1 = arcpy.management.AlterField(
            in_table=CA_counties,
            field="NAME",
            new_field_name="COUNTY",
            new_field_alias="COUNTY",
        )

        print("   setp 3/10: repair geometry")
        repair_geom_2 = arcpy.management.RepairGeometry(
            in_features=alter_field_1
        )

        print("   setp 4/10: delete unnecessary field")
        delete_field_2 = arcpy.management.DeleteField(
            in_table=repair_geom_2,
            drop_field=["COUNTY"],
            method="KEEP_FIELDS",
        )

        print("   step5/10: Add counties to fill in the gaps in the 2 datasets.  Gaps are assumed to be 'Private Non-Industry'")
        USFS_CalFire_Counties_update = arcpy.analysis.Union(
            in_features=[[USFS_CalFire_update, ""], [delete_field_2, ""]],
            out_feature_class=USFS_CalFire_Counties,
        )

        print("   setp 6/10: standardize attributes")
        calc_field_6 = arcpy.management.CalculateField(
            in_table=USFS_CalFire_Counties_update,
            field="AGNCY_LEV",
            expression="ifelse(!AGNCY_LEV!)",
            code_block="""def ifelse(AGNCY):
                if AGNCY is None or AGNCY == '':
                    return \"PRIVATE_NON-INDUSTRY\"
                else:
                    return AGNCY""",
        )

        print("   setp 7/10: dissolve by agency and county")
        dissolve_1 = arcpy.management.Dissolve(
            in_features=calc_field_6,
            out_feature_class=Ownership_Update,
            dissolve_field=["AGNCY_LEV", "COUNTY"],
            multi_part="MULTI_PART",
        )

        print("   setp 8/10: repair geometry")
        repair_geom_3 = arcpy.management.RepairGeometry(
            in_features=dissolve_1
        )

        print("   setp 9/10: standardize county attributes")
        calc_field_7 = arcpy.management.CalculateField(
            in_table=repair_geom_3,
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

        print("   setp 10/10: calculate acres")
        Ownership_Update_Final = arcpy.management.CalculateGeometryAttributes(
            in_features=calc_field_7,
            geometry_property=[["GIS_ACRES", "AREA_GEODESIC"]],
            area_unit="ACRES"
        )
        print("Done")
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
            print('Deleting Scratch Files')
            delete_scratch_files(
                gdb=scratch_workspace,
                delete_fc="yes",
                delete_table="yes",
                delete_ds="yes",
            )
        
        return Ownership_Update_Final
