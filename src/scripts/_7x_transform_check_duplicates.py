"""
# Description: This is the start of the dataset transformation scripts.
#              This script is not complete.  This script will transform
#              the flat appended files into the relational database.
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import time
import arcpy
from .utils import init_gdb

workspace, scratch_workspace = init_gdb()

def TransformCheck(Input_Table, Output_Duplicates): 
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

        Value = time.strftime("%Y%m%d-%H%M%S").replace("-", "")
        Transform_Treatmen_Frequency_3_ = os.path.join(
            scratch_workspace, rf"duplicates_{Value}"
        )
        arcpy.analysis.Frequency(
            in_table=Input_Table.__str__().format(**locals(), **globals()),
            out_table=Transform_Treatmen_Frequency_3_,
            frequency_fields=["PROJECTID_USER"],
        )

        Transform_Projects_Dissolve_ = arcpy.management.AddJoin(
            in_layer_or_view=Input_Table.__str__().format(**locals(), **globals()),
            in_field="PROJECTID_USER",
            join_table=Transform_Treatmen_Frequency_3_,
            join_field="PROJECTID_USER",
        )

        arcpy.analysis.Select(
            in_features=Transform_Projects_Dissolve_,
            out_feature_class=Output_Duplicates.__str__().format(**locals(), **globals()),
            where_clause="FREQUENCY <> 1",
        )

        if Output_Duplicates:
            Layer_With_Join_Removed = arcpy.management.RemoveJoin(
                in_layer_or_view=Transform_Projects_Dissolve_
            )
