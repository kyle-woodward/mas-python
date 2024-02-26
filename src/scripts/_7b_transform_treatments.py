"""
# Description: This is the start of the dataset transformation scripts.
#              This script will transform the flat appended files into the
#              relational database.
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import arcpy
from .utils import init_gdb

workspace, scratch_workspace = init_gdb()

def TransformTreatments(
        In_Poly,
        In_Pts,
        In_Lns,
        Out_poly,
        Out_pts,
        Out_lns,
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
        
        ## Start Poly Tool Chain
        dissolve_1 = arcpy.management.Dissolve(
            in_features=In_Poly,
            out_feature_class=Out_poly,
            dissolve_field=[
                "TRMTID_USER",
                "PROJECTID_USER",
                "PROJECTID",
                "PROJECTNAME_",
                "ORG_ADMIN_t",
                "PRIMARY_OWNERSHIP_GROUP",
                "PRIMARY_OBJECTIVE",
                "SECONDARY_OBJECTIVE",
                "TERTIARY_OBJECTIVE",
                "TREATMENT_STATUS",
                "COUNTY",
                "IN_WUI",
                "REGION",
                "TREATMENT_START",
                "TREATMENT_END",
                "RETREATMENT_DATE_EST",
                "TREATMENT_NAME",
                "BatchID",
                "Val_Status_t",
                "Val_Message_t",
                "Val_RunDate_t",
                "Review_Status_t",
                "Review_Message_t",
                "Review_RunDate_t",
                "Dataload_Status_t",
                "Dataload_Msg_t",
                # "created_user",
                # "created_date",
                # "last_edited_user",
                # "last_edited_date"
            ],
        )

        addfield_1 = arcpy.management.AddField(
            in_table=dissolve_1,
            field_name="TREATMENT_AREA",
            field_type="DOUBLE",
            field_alias="TREATMENT AREA (GIS ACRES)",
        )

        calcgeom_1 = arcpy.CalculateGeometryAttributes_management(
            in_features=addfield_1,
            geometry_property=[["TREATMENT_AREA","AREA"]],
            area_unit="ACRES_US"
            )

        GUID_1 = arcpy.management.AddGlobalIDs(
            in_datasets=[calcgeom_1]
        )


        ## Start Point Tool Chain
        dissolve_2 = arcpy.management.Dissolve(
            in_features=In_Pts,
            out_feature_class=Out_pts,
            dissolve_field=[
                "TRMTID_USER",
                "PROJECTID_USER",
                "PROJECTID",
                "PROJECTNAME_",
                "ORG_ADMIN_t",
                "PRIMARY_OWNERSHIP_GROUP",
                "PRIMARY_OBJECTIVE",
                "SECONDARY_OBJECTIVE",
                "TERTIARY_OBJECTIVE",
                "TREATMENT_STATUS",
                "COUNTY",
                "IN_WUI",
                "REGION",
                "TREATMENT_START",
                "TREATMENT_END",
                "RETREATMENT_DATE_EST",
                "TREATMENT_NAME",
                "BatchID",
                "Val_Status_t",
                "Val_Message_t",
                "Val_RunDate_t",
                "Review_Status_t",
                "Review_Message_t",
                "Review_RunDate_t",
                "Dataload_Status_t",
                "Dataload_Msg_t",
                # "created_user",
                # "created_date",
                # "last_edited_user",
                # "last_edited_date"
            ],
        )

        addfield_3 = arcpy.management.AddField(
            in_table=dissolve_2,
            field_name="TREATMENT_AREA",
            field_type="DOUBLE",
            field_alias="TREATMENT AREA (GIS ACRES)",
        )

        GUID_2 = arcpy.management.AddGlobalIDs(
            in_datasets=[addfield_3]
        )

        ## Start Line Tool Chain
        dissolve_3 = arcpy.management.Dissolve(
            in_features=In_Lns,
            out_feature_class=Out_lns,
            dissolve_field=[
                "TRMTID_USER",
                "PROJECTID_USER",
                "PROJECTID",
                "PROJECTNAME_",
                "ORG_ADMIN_t",
                "PRIMARY_OWNERSHIP_GROUP",
                "PRIMARY_OBJECTIVE",
                "SECONDARY_OBJECTIVE",
                "TERTIARY_OBJECTIVE",
                "TREATMENT_STATUS",
                "COUNTY",
                "IN_WUI",
                "REGION",
                "TREATMENT_START",
                "TREATMENT_END",
                "RETREATMENT_DATE_EST",
                "TREATMENT_NAME",
                "BatchID",
                "Val_Status_t",
                "Val_Message_t",
                "Val_RunDate_t",
                "Review_Status_t",
                "Review_Message_t",
                "Review_RunDate_t",
                "Dataload_Status_t",
                "Dataload_Msg_t",
                # "created_user",
                # "created_date",
                # "last_edited_user",
                # "last_edited_date"
            ],
        )

        addfield_5 = arcpy.management.AddField(
            in_table=dissolve_3,
            field_name="TREATMENT_AREA",
            field_type="DOUBLE",
            field_alias="TREATMENT AREA (GIS ACRES)",
        )

        GUID_3 = arcpy.management.AddGlobalIDs(
            in_datasets=[addfield_5]
        )

        return Out_poly, Out_pts, Out_lns
