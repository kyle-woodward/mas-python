"""
# Description: This is the start of the dataset transformation scripts.
#              This script will transform the flat appended files into the
#              relational database. 
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import arcpy
from .utils import init_gdb , delete_scratch_files

workspace, scratch_workspace = init_gdb()

def TransformActivities(
    In_Poly,
    In_Pts,
    In_Lns,
    Out_Table,
    delete_scratch = True
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

        Table_1 = arcpy.conversion.TableToTable(
                in_rows=In_Pts,
                out_path=scratch_workspace,
                out_name="Activities_Table_pts",
            )

        Table_2 = arcpy.conversion.TableToTable(
            in_rows=In_Lns,
            out_path=scratch_workspace,
            out_name="Activities_Table_lns",
        )

        Table_3 = arcpy.conversion.TableToTable(
            in_rows=In_Poly,
            out_path=scratch_workspace,
            out_name="Activities_Table",
        )

        append_1 = arcpy.management.Append(
            inputs=[Table_1, Table_2],
            target=Table_3,
            schema_type="NO_TEST",
            field_mapping="",
        )

        GUID_1 = arcpy.management.AddGlobalIDs(
            in_datasets=[append_1]
        )

        delete_field_1 = arcpy.management.DeleteField(
            in_table=GUID_1,
            drop_field=[
                "GlobalID",
                "ACTIVID_USER",
                "TRMTID_USER",
                "TREATMENTID_",
                "ORG_ADMIN_a",
                "ACTIVITY_DESCRIPTION",
                "ACTIVITY_CAT",
                "BROAD_VEGETATION_TYPE",
                "BVT_USERD",
                "ACTIVITY_STATUS",
                "ACTIVITY_QUANTITY",
                "ACTIVITY_UOM",
                "ACTIVITY_START",
                "ACTIVITY_END",
                "ADMIN_ORG_NAME",
                "IMPLEM_ORG_NAME",
                "PRIMARY_FUND_SRC_NAME",
                "PRIMARY_FUND_ORG_NAME",
                "SECONDARY_FUND_SRC_NAME",
                "SECONDARY_FUND_ORG_NAME",
                "TERTIARY_FUND_SRC_NAME",
                "TERTIARY_FUND_ORG_NAME",
                "ACTIVITY_PRCT",
                "RESIDUE_FATE",
                "RESIDUE_FATE_QUANTITY",
                "RESIDUE_FATE_UNITS",
                "ACTIVITY_NAME",
                "VAL_STATUS_a",
                "VAL_MSG_a",
                "VAL_RUNDATE_a",
                "REVIEW_STATUS_a",
                "REVIEW_MSG_a",
                "REVIEW_RUNDATE_a",
                "DATALOAD_STATUS_a",
                "DATALOAD_MSG_a",
                # "created_user",
                # "created_date",
                # "last_edited_user",
                # "last_edited_date",
                "TRMT_GEOM",
                "COUNTS_TO_MAS"
            ],
            method="KEEP_FIELDS",
        )

        arcpy.Copy_management(
            in_data=delete_field_1, 
            out_data=Out_Table
            )

        if delete_scratch:
            print("Deleting Scratch Files")
            delete_scratch_files(
                gdb=scratch_workspace,
                delete_fc="yes",
                delete_table="yes",
                delete_ds="yes",
            )

        return Out_Table