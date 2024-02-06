"""
# Description: Converts CalFire FRAP's WUI12_3 layer
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import arcpy
from .utils import init_gdb, delete_scratch_files

workspace, scratch_workspace = init_gdb()

# TODO add print steps, rename variables

def wui(delete_scratch=False):
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
        WUI12_3 = "https://egis.fire.ca.gov/arcgis/rest/services/FRAP/WUI/ImageServer"
        WUI_Out = os.path.join(workspace, "a_Reference", "WUI")
        
        # Process: Reclassify (Reclassify) (sa)
        Reclass_WUI11 = os.path.join(scratch_workspace, "Reclass_WUI11")
        Reclassify = Reclass_WUI11
        Reclass_WUI11 = arcpy.sa.Reclassify(WUI12_3, "WUI_DESC", "'Not WUI' NODATA;'Influence Zone' 1;Intermix 1;Interface 1", "NODATA")
        Reclass_WUI11.save(Reclassify)

        # Process: Raster to Polygon (Raster to Polygon) (conversion)
        # RasterT_Reclass_WUI = os.path.join(scratch_workspace, "RasterT_Reclass_WUI")
        arcpy.conversion.RasterToPolygon(in_raster=Reclass_WUI11, out_polygon_features=WUI_Out, simplify="SIMPLIFY")

        # Process: Repair Geometry (Repair Geometry) (management)
        Repaired_WUI_Features = arcpy.management.RepairGeometry(in_features=WUI_Out)

        if delete_scratch:
            delete_scratch_files(
                gdb=scratch_workspace,
                delete_fc="yes",
                delete_table="yes",
                delete_ds="yes",
            )
        
        return Repaired_WUI_Features