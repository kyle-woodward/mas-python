"""
# Description: Converts the "California Vegetation by Wildlife Habitat 
#              Relationship Type 2015" raster dataset to a polygon
#              dataset for use in the enrichment steps.
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import arcpy
from .utils import init_gdb

workspace, scratch_workspace = init_gdb()

def veg():
    with arcpy.EnvManager(
        workspace=workspace,
        scratchWorkspace=scratch_workspace, 
        outputCoordinateSystem= arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"), #WKID 3310
        cartographicCoordinateSystem=arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"), #WKID 3310
        extent="xmin=-374900, ymin=-604500, xmax=540100, ymax=450000, spatial_reference='NAD 1983 California (Teale) Albers (Meters)'", 
        preserveGlobalIds=True, 
        qualifiedFieldNames=False, 
        transferDomains=False, 
        transferGDBAttributeProperties=False, 
        overwriteOutput = True,
    ):

        CalVeg = arcpy.Raster("https://egis.fire.ca.gov/arcgis/services/FRAP/fveg/ImageServer")
        BVT = os.path.join(workspace, "a_Reference", "Broad_Vegetation_Types2")

        print("Vegetation Types Layer")
        print("step 1/2: Convert Raster to Polygon")
        RasterT_poly = arcpy.conversion.RasterToPolygon(
            in_raster=CalVeg, 
            out_polygon_features=BVT, 
            raster_field="WHR13NAME")

        print("step 2/2: repair geometry")
        Veg_Layer = arcpy.management.RepairGeometry(in_features=RasterT_poly)
        print("Done")

    return Veg_Layer