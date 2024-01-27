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
import arcpy
from ._1b_add_fields import AddFields
from ._2b_assign_domains import AssignDomains
from ._2j_standardize_domains import StandardizeDomains
from ._7a_enrichments_polygon import enrich_polygons
from ._2k_keep_fields import KeepFields
# from sys import argv
from .utils import init_gdb, delete_scratch_files, runner
# import os
import time

original_gdb, workspace, scratch_workspace = init_gdb()


def Model_BLM(
    output_enriched, output_standardized, input_fc, startyear, endyear, California
):  # 6t BLM 20230814
    start = time.time()
    print(f"Start Time {time.ctime()}")
    arcpy.env.overwriteOutput = True

    # define intermediary objects in scratch
    BLM_clip = os.path.join(scratch_workspace, "BLM_clip")
    BLM_copy = os.path.join(scratch_workspace, "BLM_copy")

    # Model Environment settings
    with arcpy.EnvManager(
        outputCoordinateSystem= arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"), #WKID 3310
        cartographicCoordinateSystem=arcpy.SpatialReference("NAD 1983 California (Teale) Albers (Meters)"), #WKID 3310
        extent="""450000, -374900, 540100, -604500,
                  DATUM["NAD 1983 California (Teale) Albers (Meters)"]""",
        preserveGlobalIds=True, 
        qualifiedFieldNames=False, 
        scratchWorkspace=scratch_workspace, 
        transferDomains=False, 
        transferGDBAttributeProperties=True, 
        workspace=workspace,
        overwriteOutput = True,
    ):
        
        print("Performing Standardization...")
        # To allow overwriting outputs change overwriteOutput option to True.
        arcpy.env.overwriteOutput = True

        print("   step 1/13 Clip Features...")
        # Process: Clip (Clip) (analysis)
        arcpy.analysis.Clip(
            in_features=input_fc, clip_features=California, out_feature_class=BLM_clip
        )

        print("   step 2/13 Repairing Geometry...")
        # Process: Repair Geometry (Repair Geometry) (management)
        Repaired_Input_Features = arcpy.management.RepairGeometry(in_features=BLM_clip)

        # Process: Copy Features (2) (Copy Features) (management)
        arcpy.management.CopyFeatures(
            in_features=Repaired_Input_Features, out_feature_class=BLM_copy
        )
        print("   step 3/13 Adding Fields...")
        # Process: 1b Add Fields (1b Add Fields) 
        BLM_standardized_1 = AddFields(Input_Table=BLM_copy)

        print("   step 4/13 Transfering Attributes...")
        # Process: Calculate Project ID (Calculate Field) (management)
        BLM_standardized_2 = arcpy.management.CalculateField(
            in_table=BLM_standardized_1,
            field="PROJECTID_USER",
            expression="!UNIQUE_ID!",
        )

        # Process: Calculate Agency (Calculate Field) (management)
        BLM_standardized_3 = arcpy.management.CalculateField(
            in_table=BLM_standardized_2, field="AGENCY", expression='"DOI"'
        )

        # Process: Calculate Data Steward (Calculate Field) (management)
        BLM_standardized_4 = arcpy.management.CalculateField(
            in_table=BLM_standardized_3, field="ORG_ADMIN_p", expression="'BLM'"
        )

        # Process: Calculate Data Steward (2) (Calculate Field) (management)
        BLM_standardized_5 = arcpy.management.CalculateField(
            in_table=BLM_standardized_4, field="ORG_ADMIN_t", expression="'BLM'"
        )

        # Process: Calculate Data Steward (3) (Calculate Field) (management)
        BLM_standardized_6 = arcpy.management.CalculateField(
            in_table=BLM_standardized_5, field="ORG_ADMIN_a", expression="'BLM'"
        )

        # Process: Calculate Project Contact (Calculate Field) (management)
        BLM_standardized_7 = arcpy.management.CalculateField(
            in_table=BLM_standardized_6, field="PROJECT_CONTACT", expression="None"
        )

        # Process: Calculate Project Email (Calculate Field) (management)
        BLM_standardized_8 = arcpy.management.CalculateField(
            in_table=BLM_standardized_7, field="PROJECT_EMAIL", expression="None"
        )

        # Process: Calculate Admin Org (Calculate Field) (management)
        BLM_standardized_9 = arcpy.management.CalculateField(
            in_table=BLM_standardized_8, field="ADMINISTERING_ORG", expression="'BLM'"
        )

        # Process: Calculate Project Name (Calculate Field) (management)
        BLM_standardized_10 = arcpy.management.CalculateField(
            in_table=BLM_standardized_9, field="PROJECT_NAME", expression="!TRTMNT_NM!"
        )

        # Process: Calculate Fund Source (Calculate Field) (management)
        BLM_standardized_11 = arcpy.management.CalculateField(
            in_table=BLM_standardized_10,
            field="PRIMARY_FUNDING_SOURCE",
            expression='"FEDERAL"',
        )

        # Process: Calculate Fund Org (Calculate Field) (management)
        BLM_standardized_12 = arcpy.management.CalculateField(
            in_table=BLM_standardized_11,
            field="PRIMARY_FUNDING_ORG",
            expression='"NPS"',
        )

        # Process: Calculate Imp Org (Calculate Field) (management)
        BLM_standardized_13 = arcpy.management.CalculateField(
            in_table=BLM_standardized_12, field="IMPLEMENTING_ORG", expression="'BLM'"
        )

        # Process: Calculate Activity Name (Calculate Field) (management)
        BLM_standardized_14 = arcpy.management.CalculateField(
            in_table=BLM_standardized_13,
            field="ACTIVITY_NAME",
            expression="!TRTMNT_NM!",
        )

        # Process: Calculate Veg User Defined (Calculate Field) (management)
        BLM_standardized_15 = arcpy.management.CalculateField(
            in_table=BLM_standardized_14, field="BVT_USERD", expression='"NO"'
        )

        # Process: Calculate Activity Start (Calculate Field) (management)
        BLM_standardized_16 = arcpy.management.CalculateField(
            in_table=BLM_standardized_15,
            field="ACTIVITY_START",
            expression="!TRTMNT_START_DT!",
        )

        print("   step 5/13 Calculating End Date...")
        # Process: Calculate Activity End Date (Calculate Field) (management)
        BLM_standardized_17 = arcpy.management.CalculateField(
            in_table=BLM_standardized_16,
            field="ACTIVITY_END",
            expression="!TRTMNT_END_DT!",
        )

        print("   step 6/13 Calculating Status...")
        # Process: Calculate Status (Calculate Field) (management)
        BLM_standardized_18 = arcpy.management.CalculateField(
            in_table=BLM_standardized_17,
            field="ACTIVITY_STATUS",
            expression="'COMPLETE'",
        )

        print("   step 7/13 Activity Quantity...")
        # Process: Calculate Activity Quantity (3) (Calculate Field) (management)
        BLM_standardized_19 = arcpy.management.CalculateField(
            in_table=BLM_standardized_18,
            field="ACTIVITY_QUANTITY",
            expression="ifelse(!BLM_ACRES!, !GIS_ACRES!)",
            code_block="""def ifelse(BLM, GIS):
                            if BLM == 0 or BLM is None:
                                return GIS
                            else:
                                return BLM""",
            field_type="DOUBLE",
        )

        # Process: Calculate Activity UOM (3) (Calculate Field) (management)
        BLM_standardized_20 = arcpy.management.CalculateField(
            in_table=BLM_standardized_19, field="ACTIVITY_UOM", expression='"AC"'
        )

        print("   step 8/13 Enter Field Values...")
        # Process: Calculate Admin Org2 (Calculate Field) (management)
        BLM_standardized_21 = arcpy.management.CalculateField(
            in_table=BLM_standardized_20, field="ADMIN_ORG_NAME", expression='"BLM"'
        )
        
        # Process: Calculate Implementation Org 2 (Calculate Field) (management)
        BLM_standardized_22 = arcpy.management.CalculateField(
            in_table=BLM_standardized_21, field="IMPLEM_ORG_NAME", expression="'BLM'"
        )
        
        # Process: Calculate Primary Fund Source (Calculate Field) (management)
        BLM_standardized_23 = arcpy.management.CalculateField(
            in_table=BLM_standardized_22,
            field="PRIMARY_FUND_SRC_NAME",
            expression='"FEDERAL"',
        )
        
        # Process: Calculate Fund Org 2 (Calculate Field) (management)
        BLM_standardized_24 = arcpy.management.CalculateField(
            in_table=BLM_standardized_23,
            field="PRIMARY_FUND_ORG_NAME",
            expression='"BLM"',
        )
        
        # Process: Calculate Source (Calculate Field) (management)
        BLM_standardized_25 = arcpy.management.CalculateField(
            in_table=BLM_standardized_24, field="Source", expression="'BLM'"
        )
        
        # Process: Calculate Year (Calculate Field) (management)
        BLM_standardized_26 = arcpy.management.CalculateField(
            in_table=BLM_standardized_25,
            field="Year",
            expression="Year($feature.ACTIVITY_END)",
            expression_type="ARCADE",
        )
        
        # Process: Calculate Treatment Name Lowercase (Calculate Field) (management)
        BLM_standardized_27 = arcpy.management.CalculateField(
            in_table=BLM_standardized_26,
            field="TRTMNT_NM",
            # expression="!TRTMNT_NM!.lower()"
            expression="!TRTMNT_NM!",
        )
        
        # Process: Calculate Treatment Comments Lowercase (Calculate Field) (management)
        BLM_standardized_28 = arcpy.management.CalculateField(
            in_table=BLM_standardized_27,
            field="TRTMNT_COMMENTS",
            # expression="!TRTMNT_COMMENTS!.lower()"
            expression="!TRTMNT_COMMENTS!",
        )
        print("   step 9/13 Adding original activity description to Crosswalk Field...")
        # Process: Calculate Crosswalk (Calculate Field) (management)
        BLM_standardized_29 = arcpy.management.CalculateField(
            in_table=BLM_standardized_28,
            # field="Crosswalk",
            # expression="ifelse(!TRTMNT_NM!,!TRTMNT_TYPE_CD!,!TRTMNT_SUBTYPE!,!TRTMNT_COMMENTS!,!Crosswalk!)",
            # code_block="""def ifelse(Nm, type, sub, com, cross):
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
        
        # Process: Calculate Crosswalk 2 (Calculate Field) (management)
        BLM_standardized_30 = arcpy.management.CalculateField(
            in_table=BLM_standardized_29,
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
        
        # Process: Calculate Crosswalk 3 (Calculate Field) (management)
        BLM_standardized_31 = arcpy.management.CalculateField(
            in_table=BLM_standardized_30,
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
        
        print(f"Saving Standardized Output: {output_standardized}")
        # Process: Select by Years (Select) (analysis)
        arcpy.analysis.Select(
            in_features=BLM_standardized_31,
            out_feature_class=output_standardized,
            where_clause="Year >= %d And Year <= %d" % (startyear, endyear),
        )
        print("   step 10/13 Calculate Geometry...")
        # Process: Calculate Geometry (Calculate Field) (management)
        BLM_standardized_32 = arcpy.management.CalculateField(
            in_table=output_standardized, field="TRMT_GEOM", expression="'POLYGON'"
        )

        # Process: 2j Standardize Domains (2j Standardize Domains) 
        BLM_standardized_33 = StandardizeDomains(Input_Table=BLM_standardized_32)

        # Process: 2k Keep Fields (2k Keep Fields) 
        Output_Table = KeepFields(Keep_table=BLM_standardized_33)

        print("   step 11/13 Enriching Dataset...")
        # Process: 7a Enrichments Polygon (2) (7a Enrichments Polygon) 
        enrich_polygons(enrich_in=BLM_standardized_33, enrich_out=output_enriched)
        print(f"Saving Enriched Output: {output_enriched}")

        print("   step 12/13 Calculate Treatment ID...")
        # Process: Calculate Treatment ID (Calculate Field) (management)
        BLM_standardized_34 = arcpy.management.CalculateField(
            in_table=output_enriched,
            field="TRMTID_USER",
            expression="!PROJECTID_USER![:7]+'-'+!COUNTY![:3]+'-'+!PRIMARY_OWNERSHIP_GROUP![:4]+'-'+!IN_WUI![:3]+'-'+!PRIMARY_OBJECTIVE![:8]"
        )
        print("   step 13/13 Assign Domains...")
        # Process: 2b Assign Domains (2b Assign Domains) 
        BLM_standardized_35 = AssignDomains(in_table=BLM_standardized_34)

        print('   Deleting Scratch Files')
        delete_scratch_files(
            gdb=scratch_workspace, delete_fc="yes", delete_table="yes", delete_ds="yes"
        )

        end = time.time()
        print(f"Time Elapsed: {(end-start)/60} minutes")


# if __name__ == "__main__":
#     runner(workspace, scratch_workspace, Model_BLM, "*argv[1:]")
