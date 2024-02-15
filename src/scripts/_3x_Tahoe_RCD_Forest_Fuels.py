"""
# Description: Converts the Tahoe Resource Conservation District's Forest and Fuels dataset 
#              into the Task Force standardized schema.  Dataset
#              is enriched with vegetation, ownership, county, WUI, 
#              Task Force Region, and year.             
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""

import datetime
start1 = datetime.datetime.now()
print(f"Start Time {start1}")

import os
import arcpy
from ._1_add_fields import AddFields
from ._1_assign_domains import AssignDomains
from ._3_enrichments_polygon import enrich_polygons
from ._3_keep_fields import KeepFields
from .utils import init_gdb, delete_scratch_files

workspace, scratch_workspace = init_gdb()

def TahoeFFG(
    TahoeFF_Tx_enriched, 
    TahoeFF_Tx_standardized, 
    TahoeFF_Tx_OG, 
    delete_scratch=True
):
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

        California = os.path.join(workspace, "a_Reference", "California")
        CPAD_Ownership_Update = os.path.join(workspace, "a_Reference", "CPAD_Ownership_Update")

        # define intermediary objects in scratch
        TahoeFF_pairwiseclip = os.path.join(scratch_workspace, "TahoeFF_pairwiseclip")
        TahoeFF_Tx_OG_Select = os.path.join(scratch_workspace, "TahoeFF_Tx_OG_Select")
        CPAD_Ownership_StateParks = os.path.join(scratch_workspace, "CPAD_Ownership_StateParks")
        TahoeFF_enriched_scratch = os.path.join(scratch_workspace, "TahoeFF_enriched_scratch")

        print("Executing Step 1/40 : Pairwise clip...")
        clip_CA = arcpy.analysis.PairwiseClip(
            in_features=TahoeFF_Tx_OG,
            clip_features=California,
            out_feature_class=TahoeFF_pairwiseclip,
        )

        print("Executing Step 2/40 : Select no Fed or NV or Wildland Fire (Select)...")
        select_non_wildfire = arcpy.analysis.Select(
            in_features=clip_CA,
            out_feature_class=TahoeFF_Tx_OG_Select,
            where_clause="CATEGORY <> 'Federal' And CATEGORY <> 'NV' And ACT <> 'Wildland Fire'",
        )

        print("Executing Step 3/40 : Repair Geometry...")
        repair_geom_1 = arcpy.management.RepairGeometry(
            in_features=select_non_wildfire, 
            delete_null="KEEP_NULL"
        )

        print("Executing Step 4/40 : Alter Field...")
        alterfield_1 = arcpy.management.AlterField(
            in_table=repair_geom_1,
            field="YEAR",
            new_field_name="YEAR_",
            new_field_alias="YEAR_",
        )

        print("Executing Step 5/40 : Add Fields...")
        addfields_1 = AddFields(Input_Table=alterfield_1)

        print("Executing Step 5/40 : Calculate PROJECT_ID...")
        calc_field_1 = arcpy.management.CalculateField(
            in_table=addfields_1, 
            field="PROJECTID", 
            expression="None"
        )

        print("Executing Step 6/40 : Calculate Project_ID...")
        calc_field_2 = arcpy.management.CalculateField(
            in_table=calc_field_1,
            field="Project_ID",
            expression="ifelse(!Project_ID!)",
            code_block="""def ifelse(ID):
                            if ID == '':
                                return None
                            if ID == ' ':
                                return None
                            return ID""",
        )

        print("Executing Step 7/40 : Calculate EIP_Number...")
        calc_field_3 = arcpy.management.CalculateField(
            in_table=calc_field_2,
            field="EIP_Number",
            expression="ifelse(!EIP_Number!)",
            code_block="""def ifelse(ID):
                            if ID == '':
                                return None
                            elif ID == ' ':
                                return None
                            else:
                                return ID""",
        )

        print("Executing Step 8/40 : Calculate PROJ...")
        calc_field_4 = arcpy.management.CalculateField(
            in_table=calc_field_3,
            field="PROJ",
            expression="ifelse(!PROJ!)",
            code_block="""def ifelse(ID):
                            if ID == '':
                                return None
                            return ID""",
        )

        print("Executing Step 9/40 : Calculate YEAR_...")
        calc_field_5 = arcpy.management.CalculateField(
            in_table=calc_field_4,
            field="YEAR_",
            expression="ifelse(!YEAR_!)",
            code_block="""def ifelse(ID):
                            if ID == 0:
                                return 0
                            return ID""",
        )

        print("Executing Step 10/40 : Calculate OWN_FULL...")
        calc_field_6 = arcpy.management.CalculateField(
            in_table=calc_field_5,
            field="OWN_FULL",
            expression="ifelse(!OWN_FULL!)",
            code_block="""def ifelse(ID):
                            if ID == '':
                                return None
                            return ID""",
        )

        print("Executing Step 11/40 : Calculate PROJECTID_USER...")
        calc_field_7 = arcpy.management.CalculateField(
            in_table=calc_field_6,
            field="PROJECTID_USER",
            expression="ifelse(!PROJECTID_USER!,!Project_ID!)",
            code_block="""def ifelse(ID, ID2):
                            if ID == None:
                                return ID2
                            else:
                                return ID""",
        )

        print("Executing Step 12/40 : Calculate PROJECTID_USER...")
        calc_field_8 = arcpy.management.CalculateField(
            in_table=calc_field_7,
            field="PROJECTID_USER",
            expression="ifelse(!PROJECTID_USER!,!EIP_Number!)",
            code_block="""def ifelse(ID, EIP):
                            if ID == None:
                                return EIP
                            else:
                                return ID""",
        )

        print("Executing Step 13/40 : Calculate PROJECTID_USER...")
        calc_field_9 = arcpy.management.CalculateField(
            in_table=calc_field_8,
            field="PROJECTID_USER",
            expression="ifelse(!PROJECTID_USER!,!PROJ!)",
            code_block="""def ifelse(ID, Proj):
                            if ID == None:
                                return Proj
                            else:
                                return ID""",
        )

        print("Executing Step 14/40 : Calculate PROJECTID_USER...")
        calc_field_10 = arcpy.management.CalculateField(
            in_table=calc_field_9,
            field="PROJECTID_USER",
            expression="ifelse(!PROJECTID_USER!, !JURIS!)",
            code_block="""def ifelse(ID, Jur):
                            if ID == None:
                                return Jur
                            else:
                                return ID""",
        )

        print("Executing Step 15/40 : Calculate AGENCY...")
        calc_field_11 = arcpy.management.CalculateField(
            in_table=calc_field_10,
            field="AGENCY",
            expression="Reclass(!JURIS!)",
            code_block="""# Reclassify values to another value
                        # More calculator examples at esriurl.com/CalculatorExamples
                        def Reclass(JURIS):
                            if JURIS == \"CA\":
                                return \"CNRA\"
                            elif JURIS == \"Liberty Utilities\":
                                return \"OEIS\"
                            return \"OTHER\"""",
        )

        print("Executing Step 16/40 : Calculate ADMINISTERING_ORG...")
        calc_field_12 = arcpy.management.CalculateField(
            in_table=calc_field_11,
            field="ADMINISTERING_ORG",
            expression="!OWN_FULL!",
        )

        print("Executing Step 17/40 : Select California Department of Parks and Recreation...")
        select_parks = arcpy.analysis.Select(
            in_features=CPAD_Ownership_Update,
            out_feature_class=CPAD_Ownership_StateParks,
            where_clause="AGNCY_NAME = 'California Department of Parks and Recreation'",
        )

        print("Executing Step 18/40 : Calculate Select CPAD_Ownership_stateparks...")
        TahoeFF_select_SP = arcpy.management.SelectLayerByLocation(
            in_layer=calc_field_12,
            overlap_type="HAVE_THEIR_CENTER_IN",
            select_features=select_parks,
            search_distance="1 Meters",
        )

        print("Executing Step 19/40 : Calculate ADMINISTERING_ORG...")
        calc_field_13 = arcpy.management.CalculateField(
            in_table=TahoeFF_select_SP, 
            field="ADMINISTERING_ORG", 
            expression='"PARKS"'
        )

        print("Executing Step 20/40 : clear selection...")
        clear_selection_1 = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=calc_field_12,
            selection_type="CLEAR_SELECTION",
        )

        print("Executing Step 21/40 : Calculate PROJECTID_USER...")
        calc_field_13 = arcpy.management.CalculateField(
            in_table=clear_selection_1,
            field="PROJECTID_USER",
            expression="ifelse(!AGENCY!, !PROJECTID_USER!)",
            code_block="""def ifelse(Agency, ID):
                            if Agency == \"PARKS\":
                                return \"P_\"+ID
                            elif Agency == \"TAHOE\":
                                return \"T_\"+ID
                            elif Agency == \"OTHER\":
                                return \"R_\"+ID
                            elif Agency == \"OEIS\":
                                return \"U_\"+ID
                            else:
                                return ID""",
        )

        print("Executing Step 22/40 : Calculate TRMTID_USER...")
        calc_field_14 = arcpy.management.CalculateField(
            in_table=calc_field_13,
            field="TRMTID_USER",
            expression="'TAHOE-'+(!PROJECTID_USER![:15])+(!PROJECTID_USER![-1:])+'-'+str(!Shape_Area!)[:8]",
        )

        print("Executing Step 23/40 : Calculate ORG_ADMIN_p...")
        calc_field_15 = arcpy.management.CalculateField(
            in_table=calc_field_14,
            field="ORG_ADMIN_p",
            expression='"Tahoe RCD"',
        )

        print("Executing Step 24/40 : Calculate PROJECT_CONTACT...")
        calc_field_16 = arcpy.management.CalculateField(
            in_table=calc_field_15,
            field="PROJECT_CONTACT",
            expression='"Cara Moore"',
        )

        print("Executing Step 25/40 : Calculate PROJECT_EMAIL...")
        calc_field_17 = arcpy.management.CalculateField(
            in_table=calc_field_16,
            field="PROJECT_EMAIL",
            expression='"cmoore@tahoercd.org"',
        )

        print("Executing Step 26/40 : Calculate TREATMENT_NAME...")
        calc_field_18 = arcpy.management.CalculateField(
            in_table=calc_field_17,
            field="TREATMENT_NAME",
            expression="!PROJ!",
        )

        print("Executing Step 27/40 : Calculate PRIMARY_FUNDING_ORG...")
        calc_field_19 = arcpy.management.CalculateField(
            in_table=calc_field_18,
            field="PRIMARY_FUNDING_ORG",
            expression="!CATEGORY!",
        )

        print("Executing Step 28/40 : Calculate BVT_USERD...")
        calc_field_20 = arcpy.management.CalculateField(
            in_table=calc_field_19, 
            field="BVT_USERD", 
            expression='"NO"'
        )

        print("Executing Step 29/40 : Calculate ACTIVITY_STATUS...")
        calc_field_21 = arcpy.management.CalculateField(
            in_table=calc_field_20,
            field="ACTIVITY_STATUS",
            expression='"Complete"',
        )

        print("Executing Step 30/40 : Calculate ACTIVITY_QUANTITY...")
        calc_field_22 = arcpy.management.CalculateField(
            in_table=calc_field_21,
            field="ACTIVITY_QUANTITY",
            expression="!ACRES!",
        )

        print("Executing Step 31/40 : Calculate ACTIVITY_UOM...")
        calc_field_23 = arcpy.management.CalculateField(
            in_table=calc_field_22,
            field="ACTIVITY_UOM",
            expression='"AC"',
        )

        print("Executing Step 32/40 : Calculate IMPLEM_ORG_NAME...")
        calc_field_24 = arcpy.management.CalculateField(
            in_table=calc_field_23, 
            field="IMPLEM_ORG_NAME", 
            expression="!FPD!"
        )

        print("Executing Step 33/40 : Calculate ACTIVITY_END...")
        calc_field_25 = arcpy.management.CalculateField(
            in_table=calc_field_24,
            field="ACTIVITY_END",
            expression="str('6/1/') + str(!YEAR_!)",
        )

        print("Executing Step 34/40 : Calculate Crosswalk...")
        calc_field_26 = arcpy.management.CalculateField(
            in_table=calc_field_25, 
            field="Crosswalk", 
            expression="!ACT!"
        )

        print("Executing Step 35/40 : Calculate Source...")
        calc_field_27 = arcpy.management.CalculateField(
            in_table=calc_field_26, 
            field="Source", 
            expression="'Tahoe RCD'"
        )

        print("Executing Step 36/40 : Copy Features...")
        arcpy.management.CopyFeatures(
            in_features=calc_field_27,
            out_feature_class=TahoeFF_Tx_standardized
        )

        print("Executing Step 37/40 : Keep Fields...")
        keepfields_1 = KeepFields(TahoeFF_Tx_standardized)

        Count1 = arcpy.management.GetCount(input_table21_join_copy)
        print("standardized has {} records".format(Count1[0]))


        print("Executing Step 38/40 : Enrich Polygons...")
        enrich_polygons(
            enrich_in=keepfields_1,
            enrich_out=TahoeFF_enriched_scratch
        )

        Count2 = arcpy.management.GetCount(TahoeFF_enriched_scratch)
        print("enriched has {} records".format(Count2[0]))

        print("Executing Step 39/40 : Copy Features...")
        arcpy.management.CopyFeatures(
            in_features=TahoeFF_enriched_scratch, 
            out_feature_class=TahoeFF_Tx_enriched
        )

        print("Executing Step 40/40 : AssignDomains...")
        AssignDomains(in_table=TahoeFF_Tx_enriched)

        print("completed step 40/40")

        if delete_scratch:
            print("Deleting Scratch Files")
            delete_scratch_files(
                gdb=scratch_workspace,
                delete_fc="yes",
                delete_table="yes",
                delete_ds="yes",
            )

        end1 = datetime.datetime.now()
        elapsed1 = end1 - start1
        hours, remainder1 = divmod(elapsed1.total_seconds(), 3600)
        minutes, remainder2 = divmod(remainder1, 60)
        seconds, remainder3 = divmod(remainder2, 1)
        print(f"Tahoe RCD script took: {int(hours)}h, {int(minutes)}m, {seconds}s to complete")
