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

def wui(delete_scratch=True):
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
        
        print("Reclassify WUI12_3 layer")
        Reclass_WUI11 = os.path.join(scratch_workspace, "Reclass_WUI11")
        Reclassify = Reclass_WUI11
        Reclass_WUI11 = arcpy.sa.Reclassify(WUI12_3, "WUI_DESC", "'Not WUI' NODATA;'Influence Zone' 1;Intermix 1;Interface 1", "NODATA")
        Reclass_WUI11.save(Reclassify)

        arcpy.conversion.RasterToPolygon(in_raster=Reclass_WUI11, out_polygon_features=WUI_Out, simplify="SIMPLIFY")

        Repaired_WUI_Features = arcpy.management.RepairGeometry(in_features=WUI_Out)
        print("Done")

        if delete_scratch:
            print('Deleting Scratch Files')
            delete_scratch_files(
                gdb=scratch_workspace,
                delete_fc="yes",
                delete_table="yes",
                delete_ds="yes",
            )
        
        return Repaired_WUI_Features