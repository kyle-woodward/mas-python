# NOTE: Skip for now, may want to adapt Dan Camboia's Data retriver geoprocess tool instead
"""
# Description: 
#               
#               
#              
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import arcpy
import time
from .utils import init_gdb, delete_scratch_files

workspace, scratch_workspace = init_gdb()

def GetData():
    with arcpy.EnvManager(
        outputCoordinateSystem= arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"), #WKID 3310
        cartographicCoordinateSystem=arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"), #WKID 3310
        extent="""-124.415162172178 32.5342699477235 -114.131212866967 42.0095193288898 GEOGCS["GCS_WGS_1984",
                DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],
                PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]""",
        preserveGlobalIds=True, 
        qualifiedFieldNames=False, 
        scratchWorkspace=scratch_workspace, 
        transferDomains=False, 
        transferGDBAttributeProperties=True, 
        workspace=workspace,
        overwriteOutput = True,
    ):
        EDW_Final_Fire_Perimeter_All_Years_ = "EDW Final Fire Perimeter (All Years)"
        BLM_Vegetation_Treatment_Area_Completed_Polygons = (
            "BLM Vegetation Treatment Area Completed Polygons"
        )
        NPS_Fuels_Treatment_Perimeters_Treatment_Type = (
            "NPS Fuels Treatment Perimeters - Treatment Type"
        )
        CAL_FIRE_Timber_Harvesting_Plans_WGS84 = (
            "CAL FIRE Timber Harvesting Plans WGS84"
        )
        CalFire_Treatment_Polygons = "CalFire Treatment Polygons"
        ForestHealth_AwardedProjects_2018_2019 = (
            "ForestHealth_AwardedProjects_2018_2019"
        )
        Stakeholder_projects = "Stakeholder_projects"
        CALMAPPER_CALVTP_TREATMENTS_VW = "CALMAPPER.CALVTP_TREATMENTS_VW"
        EDW_Hazardous_Fuel_Treatment_Reduction_Polygon_2_ = (
            "Treatments-Source\\EDW Hazardous Fuel Treatment Reduction: Polygon"
        )
        EDW_Timber_Harvest_All_Years_ = "EDW Timber Harvest (All Years)"
        NFPORS_Fuel_Treatment_Polygons = (
            "Treatments-Source\\NFPORS Fuel Treatment Polygons"
        )
        CAL_FIRE_Proposed_Harvest_Plans_TA83 = (
            "Treatments-Source\\CAL FIRE Proposed Harvest Plans TA83"
        )
        CalVTP_Treatment_Areas = "CalVTP_Treatment_Areas"
        PC414_CWI_Million_Acres_gdb = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb"
        CalVTP_Treatment_Areas_3_ = "Treatments-Source\\CalVTP_Treatment_Areas"
        a_Originals = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\a_Originals"
        Tahoe_Forest_Fuels_Tx = "Treatments-Source\\Tahoe_Forest_Fuels_Tx"

        Output_Feature_Class_5_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\EDWFinalFirePerimeterAllYear"
        arcpy.analysis.Select(
            in_features=EDW_Final_Fire_Perimeter_All_Years_,
            out_feature_class=Output_Feature_Class_5_,
            where_clause="",
        )

        Output_Feature_Class_11_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\BLMVegetationTreatmentAreaCo"
        arcpy.analysis.Select(
            in_features=BLM_Vegetation_Treatment_Area_Completed_Polygons,
            out_feature_class=Output_Feature_Class_11_,
            where_clause="",
        )

        Output_Feature_Class_10_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\NPSFuelsTreatmentPerimetersT"
        arcpy.analysis.Select(
            in_features=NPS_Fuels_Treatment_Perimeters_Treatment_Type,
            out_feature_class=Output_Feature_Class_10_,
            where_clause="",
        )

        Output_Feature_Class_9_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\CALFIRETimberHarvestingPlans"
        arcpy.analysis.Select(
            in_features=CAL_FIRE_Timber_Harvesting_Plans_WGS84,
            out_feature_class=Output_Feature_Class_9_,
            where_clause="",
        )

        CalFireTreatment_Select = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC381 FirstStreet\\Scratch.gdb\\CalFireTreatment_Select"
        arcpy.analysis.Select(
            in_features=CalFire_Treatment_Polygons,
            out_feature_class=CalFireTreatment_Select,
            where_clause="",
        )

        Output_Feature_Class_13_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\ForestHealth_AwardedProjects"
        arcpy.analysis.Select(
            in_features=ForestHealth_AwardedProjects_2018_2019,
            out_feature_class=Output_Feature_Class_13_,
            where_clause="",
        )

        South_Yuba_Stakeholder_projects_Select = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC381 FirstStreet\\Scratch.gdb\\South_Yuba_Stakeholder_projects_Select"
        arcpy.analysis.Select(
            in_features=Stakeholder_projects,
            out_feature_class=South_Yuba_Stakeholder_projects_Select,
            where_clause="Source <> 'CAL FIRE' And Source <> 'USDA Forest Service Tahoe'",
        )

        usfs_haz_fuels_treatments_reduction_20220607 = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\a_Originals\\usfs_haz_fuels_treatments_reduction_20220607"
        arcpy.analysis.Select(
            in_features=EDW_Hazardous_Fuel_Treatment_Reduction_Polygon_2_,
            out_feature_class=usfs_haz_fuels_treatments_reduction_20220607,
            where_clause="",
        )

        Output_Feature_Class = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\scratch.gdb\\EDWTimberHarvestAllYears_Sel"
        arcpy.analysis.Select(
            in_features=EDW_Timber_Harvest_All_Years_,
            out_feature_class=Output_Feature_Class,
            where_clause="",
        )

        nfpors_fuels_treatments_20220304 = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\Originals\\nfpors_fuels_treatments_20220304"
        arcpy.analysis.Select(
            in_features=NFPORS_Fuel_Treatment_Polygons,
            out_feature_class=nfpors_fuels_treatments_20220304,
            where_clause="",
        )

        CALFIRE_Timber_Harvest_Proposed_20220616 = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\a_Originals\\CALFIRE_Timber_Harvest_Proposed_20220616"
        arcpy.management.CopyFeatures(
            in_features=CAL_FIRE_Proposed_Harvest_Plans_TA83,
            out_feature_class=CALFIRE_Timber_Harvest_Proposed_20220616,
            config_keyword="",
            spatial_grid_1=None,
            spatial_grid_2=None,
            spatial_grid_3=None,
        )

        Repaired_Input_Features = arcpy.management.RepairGeometry(
            in_features=CALFIRE_Timber_Harvest_Proposed_20220616,
            delete_null="DELETE_NULL",
            validation_method="ESRI",
        )

        nfpors_fuels_treatments_20220304_2_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\Originals\\nfpors_fuels_treatments_20220304"
        arcpy.management.CopyFeatures(
            in_features=NFPORS_Fuel_Treatment_Polygons,
            out_feature_class=nfpors_fuels_treatments_20220304_2_,
            config_keyword="",
            spatial_grid_1=None,
            spatial_grid_2=None,
            spatial_grid_3=None,
        )

        CALFIRE_Timber_Harvest_Proposed_20220616_2_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\a_Originals\\CALFIRE_Timber_Harvest_Proposed_20220616"
        arcpy.analysis.Select(
            in_features=CAL_FIRE_Proposed_Harvest_Plans_TA83,
            out_feature_class=CALFIRE_Timber_Harvest_Proposed_20220616_2_,
            where_clause="",
        )

        CalVTP_20220915 = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\a_Originals\\CalVTP_20220915"
        arcpy.analysis.Select(
            in_features=CalVTP_Treatment_Areas,
            out_feature_class=CalVTP_20220915,
            where_clause="Affiliation = 'non-CAL FIRE'",
        )

        CalVTP_20220923 = arcpy.conversion.FeatureClassToFeatureClass(
            in_features=CalVTP_Treatment_Areas_3_,
            out_path=a_Originals,
            out_name="CalVTP_20220923",
            where_clause="",
            field_mapping='Project_ID "Project ID" true true false 50 Text 0 0,First,#,Treatments-Source\\CalVTP_Treatment_Areas,Project_ID,0,50;Date_Completed "Date Completed" true true false 8 Date 0 0,First,#,Treatments-Source\\CalVTP_Treatment_Areas,Date_Completed,-1,-1;Treatment_Type "Treatment Type" true true false 50 Text 0 0,First,#,Treatments-Source\\CalVTP_Treatment_Areas,Treatment_Type,0,50;Treatment_Activity "Treatment Activity" true true false 50 Text 0 0,First,#,Treatments-Source\\CalVTP_Treatment_Areas,Treatment_Activity,0,50;Treatment_Acres "Treatment Acres" true true false 0 Double 0 0,First,#,Treatments-Source\\CalVTP_Treatment_Areas,Treatment_Acres,-1,-1;County "County" true true false 50 Text 0 0,First,#,Treatments-Source\\CalVTP_Treatment_Areas,County,0,50;Fuel_Type "Fuel Type" true true false 50 Text 0 0,First,#,Treatments-Source\\CalVTP_Treatment_Areas,Fuel_Type,0,50;Coastal_Zone "Coastal Zone" true true false 3 Text 0 0,First,#,Treatments-Source\\CalVTP_Treatment_Areas,Coastal_Zone,0,3;Grant_Type "Grant Type" true true false 50 Text 0 0,First,#,Treatments-Source\\CalVTP_Treatment_Areas,Grant_Type,0,50;GlobalID "GlobalID" false false true 38 GlobalID 0 0,First,#,Treatments-Source\\CalVTP_Treatment_Areas,GlobalID,-1,-1;Status "Status" true true false 256 Text 0 0,First,#,Treatments-Source\\CalVTP_Treatment_Areas,Status,0,256;Affiliation "Affiliation" true true false 255 Text 0 0,First,#,Treatments-Source\\CalVTP_Treatment_Areas,Affiliation,0,255',
            config_keyword="",
        )

        Value = time.strftime("%Y%m%d")

        Tahoe_Forest_Fuels_Tx_value_ = "C:\\Users\\sageg\\Documents\\ArcGIS\\Projects\\PC414 CWI Million Acres\\PC414 CWI Million Acres.gdb\\a_Originals\\Tahoe_Forest_Fuels_Tx_%value%"
        if Value:
            arcpy.management.CopyFeatures(
                in_features=Tahoe_Forest_Fuels_Tx,
                out_feature_class=Tahoe_Forest_Fuels_Tx_value_
            )


