"""
# Description: This is the start of the dataset transformation scripts.
#              This script will transform the flat appended files into the 
#              relational database.
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import os
import arcpy
from .utils import init_gdb

workspace, scratch_workspace = init_gdb()

def TransformProjects(
    In_Poly,
    In_Pts,
    In_Lns,
    Out_Poly,
):
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
        # scratch outputs
        temp_poly = os.path.join(scratch_workspace, "temp_poly")
        temp_pts = os.path.join(scratch_workspace, "temp_pts")
        temp_lns = os.path.join(scratch_workspace, "temp_lns")
        pts_buffered = os.path.join(scratch_workspace, "pts_buffered")
        lns_buffered = os.path.join(scratch_workspace, "lns_buffered")

        ## START TOOL CHAIN
        # Buffer points and lines using activity quantity and line length
        copy_1 = arcpy.CopyFeatures_management(In_Pts, temp_pts)

        calc_buffer_1 = arcpy.management.CalculateField(
            copy_1,
            "BufferMeters",
            "math.sqrt((!ACTIVITY_QUANTITY!*4046.86)/3.14159)",
        )

        buffer_pts_1 = arcpy.analysis.PairwiseBuffer(
            in_features=calc_buffer_1,
            out_feature_class=pts_buffered,
            buffer_distance_or_field="BufferMeters",
            dissolve_option="NONE"
        )

        copy_2 = arcpy.CopyFeatures_management(In_Lns, temp_lns)
        
        calc_buffer_2 = arcpy.management.CalculateField(
            copy_2,
            "BufferMeters",
            "(!ACTIVITY_QUANTITY!*4046.86)/!Shape_Length!/2",
        )

        select_1 = arcpy.SelectLayerByAttribute_management(
            calc_buffer_2,
            "NEW_SELECTION", 
            "BufferMeters IS NOT NULL" 
        )

        buffer_lns_1 = arcpy.analysis.PairwiseBuffer(
            in_features=select_1,
            out_feature_class=lns_buffered,
            buffer_distance_or_field="BufferMeters",
            dissolve_option="NONE"
        )

        copy_3 = arcpy.CopyFeatures_management(In_Poly, temp_poly)

        add_field_2 = arcpy.AddField_management(
            copy_3, 
            "BufferMeters",
            field_type="TEXT"
        )

        # Append point and line buffers to polygons
        append_1 = arcpy.Append_management([
            buffer_pts_1, 
            buffer_lns_1
            ],
            add_field_2,
            schema_type="NO_TEST",
        )

        dissolve_1 = arcpy.management.Dissolve(
            in_features=append_1,
            out_feature_class=Out_Poly,
            dissolve_field=[
                "PROJECTID_USER",
                "AGENCY",
                "ORG_ADMIN_p",
                "PROJECT_CONTACT",
                "PROJECT_EMAIL",
                "ADMINISTERING_ORG",
                "PROJECT_NAME",
                "PROJECT_STATUS",
                "PROJECT_START",
                "PROJECT_END",
                "PRIMARY_FUNDING_SOURCE",
                "PRIMARY_FUNDING_ORG",
                "IMPLEMENTING_ORG",
                "BatchID_p",
                "Val_Status_p",
                "Val_Message_p",
                "Val_RunDate_p",
                "Review_Status_p",
                "Review_Message_p",
                "Review_RunDate_p",
                "Dataload_Status_p",
                "Dataload_Msg_p",
            ],
        )

        GUID_1 = arcpy.management.AddGlobalIDs(
            in_datasets=[Out_Poly]
        )

    return Out_Poly