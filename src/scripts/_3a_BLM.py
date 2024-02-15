"""
# Description: Converts the U.S. Department of Interior, Bureau 
#              of Land Management's fuels treatments dataset 
#              into the Task Force standardized schema.  Dataset
#              is enriched with vegetation, ownership, county, WUI, 
#              Task Force Region, and year.             
# Author: Spatial Informatics Group LLC
# Version: 1.0.0
# Date Created: Jan 24, 2024
"""
import datetime
start1 = datetime.datetime.now()

import os
import arcpy
from ._1_add_fields import AddFields
from ._1_assign_domains import AssignDomains
from ._3_enrichments_polygon import enrich_polygons
from ._3_keep_fields import KeepFields
from .utils import init_gdb, delete_scratch_files

workspace, scratch_workspace = init_gdb()

def Model_BLM(
    output_enriched, 
    input_fc, 
    startyear, 
    endyear, 
    California, 
    delete_scratch=True
):
    # Model Environment settings
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
        overwriteOutput = True
    ):
        print(f"Start Time {start1}")

        # define intermediary objects in scratch
        BLM_clip = os.path.join(scratch_workspace, "BLM_clip")
        BLM_copy = os.path.join(scratch_workspace, "BLM_copy")
        output_standardized = os.path.join(scratch_workspace, "BLM_standardized")

        ### BEGIN TOOL CHAIN
        print("Performing Standardization...")
        print("   step 1/13 Clip Features...")
        arcpy.analysis.Clip(
            in_features=input_fc, 
            clip_features=California, 
            out_feature_class=BLM_clip
        )

        print("   step 2/13 Repairing Geometry...")
        repair_geom = arcpy.management.RepairGeometry(BLM_clip)

        arcpy.management.CopyFeatures(
            in_features=repair_geom, 
            out_feature_class=BLM_copy
        )
        print("   step 3/13 Adding Fields...")
        standardized_1 = AddFields(Input_Table=BLM_copy)

        print("   step 4/13 Transfering Attributes...")
        calc_field_1 = arcpy.management.CalculateField(
            in_table=standardized_1,
            field="PROJECTID_USER",
            expression="!UNIQUE_ID!",
        )

        calc_field_2 = arcpy.management.CalculateField(
            in_table=calc_field_1, 
            field="AGENCY", 
            expression='"DOI"'
        )

        calc_field_3 = arcpy.management.CalculateField(
            in_table=calc_field_2, 
            field="ORG_ADMIN_p", 
            expression="'BLM'"
        )

        calc_field_4 = arcpy.management.CalculateField(
            in_table=calc_field_3, 
            field="ORG_ADMIN_t", 
            expression="'BLM'"
        )

        calc_field_5 = arcpy.management.CalculateField(
            in_table=calc_field_4, 
            field="ORG_ADMIN_a", 
            expression="'BLM'"
        )

        calc_field_6 = arcpy.management.CalculateField(
            in_table=calc_field_5, 
            field="PROJECT_CONTACT", 
            expression="None"
        )

        calc_field_7 = arcpy.management.CalculateField(
            in_table=calc_field_6, 
            field="PROJECT_EMAIL", 
            expression="None"
        )

        calc_field_7 = arcpy.management.CalculateField(
            in_table=calc_field_7, 
            field="ADMINISTERING_ORG", 
            expression="'BLM'"
        )

        calc_field_8 = arcpy.management.CalculateField(
            in_table=calc_field_7, 
            field="PROJECT_NAME", 
            expression="!TRTMNT_NM!"
        )

        calc_field_9 = arcpy.management.CalculateField(
            in_table=calc_field_8,
            field="PRIMARY_FUNDING_SOURCE",
            expression='"FEDERAL"',
        )

        calc_field_10 = arcpy.management.CalculateField(
            in_table=calc_field_9,
            field="PRIMARY_FUNDING_ORG",
            expression='"NPS"',
        )

        calc_field_11 = arcpy.management.CalculateField(
            in_table=calc_field_10, 
            field="IMPLEMENTING_ORG", 
            expression="'BLM'"
        )

        calc_field_12 = arcpy.management.CalculateField(
            in_table=calc_field_11,
            field="ACTIVITY_NAME",
            expression="!TRTMNT_NM!",
        )

        calc_field_13 = arcpy.management.CalculateField(
            in_table=calc_field_12, 
            field="BVT_USERD", 
            expression='"NO"'
        )

        calc_field_14 = arcpy.management.CalculateField(
            in_table=calc_field_13,
            field="ACTIVITY_START",
            expression="!TRTMNT_START_DT!",
        )

        print("   step 5/13 Calculating End Date...")
        calc_field_15 = arcpy.management.CalculateField(
            in_table=calc_field_14,
            field="ACTIVITY_END",
            expression="!TRTMNT_END_DT!",
        )

        print("   step 6/13 Calculating Status...")
        calc_field_16 = arcpy.management.CalculateField(
            in_table=calc_field_15,
            field="ACTIVITY_STATUS",
            expression="'COMPLETE'",
        )

        print("   step 7/13 Activity Quantity...")
        calc_field_17 = arcpy.management.CalculateField(
            in_table=calc_field_16,
            field="ACTIVITY_QUANTITY",
            expression="ifelse(!BLM_ACRES!, !GIS_ACRES!)",
            code_block="""def ifelse(BLM, GIS):
                            if BLM == 0 or BLM is None:
                                return GIS
                            else:
                                return BLM""",
            field_type="DOUBLE",
        )

        calc_field_18 = arcpy.management.CalculateField(
            in_table=calc_field_17, 
            field="ACTIVITY_UOM", 
            expression='"AC"'
        )

        print("   step 8/13 Enter Field Values...")
        calc_field_19 = arcpy.management.CalculateField(
            in_table=calc_field_18, 
            field="ADMIN_ORG_NAME", 
            expression='"BLM"'
        )
        
        calc_field_20 = arcpy.management.CalculateField(
            in_table=calc_field_19, 
            field="IMPLEM_ORG_NAME", 
            expression="'BLM'"
        )
        
        calc_field_21 = arcpy.management.CalculateField(
            in_table=calc_field_20,
            field="PRIMARY_FUND_SRC_NAME",
            expression='"FEDERAL"',
        )
        
        calc_field_22 = arcpy.management.CalculateField(
            in_table=calc_field_21,
            field="PRIMARY_FUND_ORG_NAME",
            expression='"BLM"',
        )
        
        calc_field_23 = arcpy.management.CalculateField(
            in_table=calc_field_22, 
            field="Source", 
            expression="'BLM'"
        )
        
        calc_field_24 = arcpy.management.CalculateField(
            in_table=calc_field_23,
            field="Year",
            expression="Year($feature.ACTIVITY_END)",
            expression_type="ARCADE",
        )
        
        calc_field_25 = arcpy.management.CalculateField(
            in_table=calc_field_24,
            field="TRTMNT_NM",
            expression="!TRTMNT_NM!",
        )
        
        calc_field_26 = arcpy.management.CalculateField(
            in_table=calc_field_25,
            field="TRTMNT_COMMENTS",
            expression="!TRTMNT_COMMENTS!",
        )

        print("   step 9/13 Adding original activity description to Crosswalk Field...")
        calc_field_27 = arcpy.management.CalculateField(
            in_table=calc_field_26,
            field="Crosswalk",
            expression="ifelse(!TRTMNT_TYPE_CD!,!TRTMNT_SUBTYPE!,!Crosswalk!)",
            code_block="""def ifelse(type, sub, cross): 
                            if (type == 'BIOLOGICAL' or type == 1) and sub == 'CLASSICAL':
                                return 'PRESCRB_HERBIVORY'
                            if (type == 'BIOLOGICAL' or type == 1) and sub == 'NON-CLASSICAL':
                                return 'PRESCRB_HERBIVORY'
                            if sub == 'FERTILIZER':
                                return 'NOT_DEFINED'
                            if sub == 'PESTICIDE':
                                return 'PEST_CNTRL'
                            if type == 'PRESCRIBED FIRE' or type == 3:
                                return 'BROADCAST_BURN'
                            if (type == 'PHYSICAL' or type == 4) and sub == 'OTHER':
                                return 'THIN_MECH'
                            if (type == 'PHYSICAL' or type == 4) and sub == 'REMOVE':
                                return 'THIN_MECH'
                            if (type == 'PHYSICAL' or type == 4) and sub == 'PLANT':
                                return 'HABITAT_REVEG'
                            else:
                                return cross""",
        )
        
        calc_field_28 = arcpy.management.CalculateField(
            in_table=calc_field_27,
            field="Crosswalk",
            expression="ifelse(!TRTMNT_NM!,!TRTMNT_TYPE_CD!,!TRTMNT_SUBTYPE!,!TRTMNT_COMMENTS!,!Crosswalk!)",
            code_block="""def ifelse(Nm, type, sub, com, cross):
                            if Nm is None:
                                return cross
                            elif (type == 'PRESCRIBED FIRE' or type == 3) and 'pile' in Nm:
                                return 'PILE_BURN'
                            elif (type == 'PRESCRIBED FIRE' or type == 3) and 'hp' in Nm:
                                return 'PILE_BURN'
                            elif (type == 'PRESCRIBED FIRE' or type == 3) and 'hand' in Nm:
                                return 'PILE_BURN'
                            elif (type == 'PHYSICAL' or type == 4) and 'road' in Nm:
                                return 'ROAD_CLEAR'
                            elif (type == 'PHYSICAL' or type == 4) and 'chip' in Nm:
                                return 'CHIPPING'
                            elif (type == 'PHYSICAL' or type == 4) and 'hand' in Nm:
                                return 'THIN_MAN'
                            elif (type == 'PHYSICAL' or type == 4) and 'masticat' in Nm:
                                return 'MASTICATION'
                            else:
                                return cross""",
        )
        
        calc_field_29 = arcpy.management.CalculateField(
            in_table=calc_field_28,
            field="Crosswalk",
            expression="ifelse(!TRTMNT_NM!,!TRTMNT_TYPE_CD!,!TRTMNT_SUBTYPE!,!TRTMNT_COMMENTS!,!Crosswalk!)",
            code_block="""def ifelse(Nm, type, sub, com, cross):
                            if com is None:
                                return cross
                            elif (type == 'PRESCRIBED FIRE' or type == 3) and 'pile' in com:
                                return 'PILE_BURN'
                            elif (type == 'PRESCRIBED FIRE' or type == 3) and 'broadcast' in com:
                                return 'BROADCAST_BURN'
                            elif (type == 'PHYSICAL' or type == 4) and 'hand' in com:
                                return 'THIN_MAN'
                            elif (type == 'PHYSICAL' or type == 4) and 'chip' in com:
                                return 'CHIPPING'
                            elif (type == 'PHYSICAL' or type == 4) and 'lop' in com:
                                return 'LOP_AND_SCAT'
                            elif (type == 'PHYSICAL' or type == 4) and 'masticat' in com:
                                return 'MASTICATION'
                            elif (type == 'PHYSICAL' or type == 4) and 'mow' in com:
                                return 'MOWING'
                            elif (type == 'PHYSICAL' or type == 4) and 'biomass' in com:
                                return 'BIOMASS_REMOVAL'
                            elif (type == 'PHYSICAL' or type == 4) and 'machine pile' in com:
                                return 'PILING'
                            else:
                                return cross""",
        )
        
        print(f"Saving Standardized Output")
        arcpy.analysis.Select(
            in_features=calc_field_29,
            out_feature_class=output_standardized,
            where_clause="Year >= %d And Year <= %d" % (startyear, endyear),
        )
        
        Count1 = arcpy.management.GetCount(output_standardized)
        print("output_standardized has {} records".format(Count1[0]))

        print("   step 10/13 Calculate Geometry...")
        calc_field_30 = arcpy.management.CalculateField(
            in_table=output_standardized, 
            field="TRMT_GEOM", 
            expression="'POLYGON'"
        )

        keepfields_1 = KeepFields(Keep_table=calc_field_30)

        print("   step 11/13 Enriching Dataset...")
        enrich_polygons(
            enrich_in=keepfields_1, 
            enrich_out=output_enriched
            )
        print(f"Saving Enriched Output")

        Count2 = arcpy.management.GetCount(output_enriched)
        print("output_enriched has {} records".format(Count2[0]))

        print("   step 12/13 Calculate Treatment ID...")
        calc_field_31 = arcpy.management.CalculateField(
            in_table=output_enriched,
            field="TRMTID_USER",
            expression="str(!PROJECTID_USER!)[:7]+'-'+str(!COUNTY!)[:3]+'-'+str(!PRIMARY_OWNERSHIP_GROUP!)[:4]+'-'+str(!IN_WUI![:3])+'-'+str(!PRIMARY_OBJECTIVE!)[:8]"
        )

        print("   step 13/13 Assign Domains...")
        AssignDomains(in_table=calc_field_31)

        if delete_scratch:
            print('Deleting Scratch Files')
            delete_scratch_files(
                gdb=scratch_workspace,
                delete_fc="yes",
                delete_table="yes",
                delete_ds="yes",
            )

        end2 = datetime.datetime.now()
        elapsed2 = (end2-start1)
        hours, remainder4 = divmod(elapsed2.total_seconds(), 3600)
        minutes, remainder5 = divmod(remainder4, 60)
        seconds, remainder6 = divmod(remainder5, 1)
        print(f"BLM script took: {int(hours)}h, {int(minutes)}m, {seconds}s to complete")

